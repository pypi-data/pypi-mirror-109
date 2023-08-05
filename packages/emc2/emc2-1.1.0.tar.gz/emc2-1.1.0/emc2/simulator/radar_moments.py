import xarray as xr
import numpy as np
import dask.bag as db
import dask.array as da
from time import time

from ..core import Instrument, Model
from .attenuation import calc_radar_atm_attenuation
from .psd import calc_mu_lambda
from ..core.instrument import ureg, quantity


def calc_total_reflectivity(model):
    """
    This method calculates the total (convective + stratiform) reflectivity (Ze).

    Parameters
    ----------
    model: :func:`emc2.core.Model` class
        The model to calculate the parameters for.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The xarray Dataset containing the calculated radar moments.
    """
    Ze_tot = np.where(np.isfinite(model.ds["sub_col_Ze_tot_strat"].values),
                      10 ** (model.ds["sub_col_Ze_tot_strat"].values / 10.), 0)
    Ze_tot = np.where(np.isfinite(model.ds["sub_col_Ze_tot_conv"].values), Ze_tot +
                      10 ** (model.ds["sub_col_Ze_tot_conv"].values / 10.), Ze_tot)

    model.ds['sub_col_Ze_tot'] = xr.DataArray(10 * np.log10(Ze_tot), dims=model.ds["sub_col_Ze_tot_strat"].dims)
    model.ds['sub_col_Ze_tot'].attrs["long_name"] = \
        "Total (convective + stratiform) equivalent radar reflectivity factor"
    model.ds['sub_col_Ze_tot'].attrs["units"] = "dBZ"
    model.ds['sub_col_Ze_att_tot'] = 10 * np.log10(Ze_tot *
                                                   model.ds['hyd_ext_conv'].fillna(1) * model.ds[
                                                       'hyd_ext_strat'].fillna(1) *
                                                   model.ds['atm_ext'].fillna(1))
    model.ds['sub_col_Ze_att_tot'].attrs["long_name"] = \
        "Total (convective + stratiform) attenuated (hydrometeor + gaseous) equivalent radar reflectivity factor"
    model.ds['sub_col_Ze_att_tot'].attrs["units"] = "dBZ"
    model.ds["sub_col_Ze_tot"] = model.ds["sub_col_Ze_tot"].where(np.isfinite(model.ds["sub_col_Ze_tot"]))
    model.ds["sub_col_Ze_att_tot"] = model.ds["sub_col_Ze_att_tot"].where(
        np.isfinite(model.ds["sub_col_Ze_att_tot"]))

    return model


def accumulate_attenuation(model, is_conv, z_values, hyd_ext, atm_ext, OD_from_sfc=True,
                           use_empiric_calc=False, **kwargs):
    """
    Accumulates atmospheric and condensate radar attenuation (linear units) from TOA or the surface.
    Output fields are condensate and atmospheric transmittance.

    Parameters
    ----------
    model: Model
        The model to generate the parameters for.
    is_conv: bool
        True if the cell is convective
    z_values: ndarray
        model output height array in m.
    hyd_ext: ndarray
        fwd calculated extinction due to condensate per layer (empirical - dB km^-1, m^-1 otherwise).
    atm_ext: ndarray
        atmospheric attenuation per layer (dB/km).
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    use_empirical_calc: bool
        When True using empirical relations from literature for the fwd calculations
        (the cloud fraction still follows the scheme logic set by use_rad_logic).

    Returns
    -------
    model: :func:`emc2.core.Model`
        The model with the added simulated lidar parameters.
    """
    if is_conv:
        cloud_str = "conv"
    else:
        cloud_str = "strat"

    if not use_empiric_calc:
        hyd_ext = hyd_ext * 1e3

    if OD_from_sfc:
        OD_str = "model layer base"
    else:
        OD_str = "model layer top"

    Dims = model.ds["%s_q_subcolumns_cl" % cloud_str].shape
    if OD_from_sfc:
        dz = np.diff(z_values / 1e3, axis=1, prepend=0.)
        hyd_ext = np.cumsum(np.tile(dz, (model.num_subcolumns, 1, 1)) *
                            np.concatenate((np.zeros(Dims[:2] + (1,)), hyd_ext[:, :, :-1]), axis=2), axis=2)
        atm_ext = np.cumsum(dz * np.concatenate((np.zeros((Dims[1],) + (1,)),
                                                 atm_ext[:, :-1]), axis=1), axis=1)
    else:
        dz = np.diff(z_values / 1e3, axis=1, append=0.)
        hyd_ext = np.flip(np.cumsum(np.flip(np.tile(dz, (model.num_subcolumns, 1, 1)) *
                                            np.concatenate((hyd_ext[:, :, 1:], np.zeros(Dims[:2] + (1,))), axis=2),
                                            axis=2), axis=2), axis=2)
        atm_ext = np.flip(np.cumsum(np.flip(dz * np.concatenate((atm_ext[:, 1:],
                                                                 np.zeros((Dims[1],) + (1,))), axis=1), axis=1),
                                    axis=1), axis=1)

    if use_empiric_calc:
        model.ds['hyd_ext_%s' % cloud_str] = xr.DataArray(10 ** (-2 * hyd_ext / 10.),
                                                          dims=model.ds["%s_q_subcolumns_cl" % cloud_str].dims)
    else:
        model.ds['hyd_ext_%s' % cloud_str] = \
            xr.DataArray(np.exp(-2 * hyd_ext), dims=model.ds["sub_col_Ze_tot_%s" % cloud_str].dims)
    model.ds['atm_ext'] = xr.DataArray(10 ** (-2 * atm_ext / 10), dims=model.ds[model.T_field].dims)

    model.ds['hyd_ext_%s' % cloud_str].attrs["long_name"] = \
        "Two-way %s hydrometeor transmittance at %s" % (cloud_str, OD_str)
    model.ds['hyd_ext_%s' % cloud_str].attrs["units"] = "1"
    model.ds['atm_ext'].attrs["long_name"] = \
        "Two-way atmospheric transmittance due to H2O and O2 at %s" % OD_str
    model.ds['atm_ext'].attrs["units"] = "1"

    return model


def calc_radar_empirical(instrument, model, is_conv, p_values, t_values, z_values, atm_ext,
                         OD_from_sfc=True, use_empiric_calc=False, hyd_types=None, **kwargs):
    """
    Calculates the radar stratiform or convective reflectivity and attenuation
    in a sub-columns using empirical formulation from literature.

    Parameters
    ----------
    instrument: :func:`emc2.core.Instrument` class
        The instrument to calculate the reflectivity parameters for.
    model: :func:`emc2.core.Model` class
        The model to calculate the parameters for.
    is_conv: bool
        True if the cell is convective
    p_values: ndarray
        model output pressure array in Pa.
    t_values: ndarray
        model output temperature array in C.
    z_values: ndarray
        model output height array in m.
    atm_ext: ndarray
        atmospheric attenuation per layer (dB/km).
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    hyd_types: list or None
        list of hydrometeor names to include in calcuation. using 4 classes if None.
    Additonal keyword arguments are passed into
    :py:func:`emc2.simulator.lidar_moments.accumulate_attenuation`.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The model with the added simulated lidar parameters.
    """
    if hyd_types is None:
        hyd_types = ["cl", "ci", "pl", "pi"]

    if is_conv:
        cloud_str = "conv"
    else:
        cloud_str = "strat"

    if not instrument.instrument_class.lower() == "radar":
        raise ValueError("Reflectivity can only be derived from a radar!")

    Dims = model.ds["%s_q_subcolumns_cl" % cloud_str].shape
    model.ds["sub_col_Ze_tot_%s" % cloud_str] = xr.DataArray(
        np.zeros(Dims), dims=model.ds["%s_q_subcolumns_cl" % cloud_str].dims)

    for hyd_type in hyd_types:
        q_field = "%s_q_subcolumns_%s" % (cloud_str, hyd_type)
        WC_tot = np.zeros(Dims)
        WC = model.ds["%s_q_subcolumns_%s" % (cloud_str, hyd_type)] * p_values / \
            (instrument.R_d * (t_values + 273.15)) * 1e3
        # Fox and Illingworth (1997)
        if hyd_type.lower() == "cl":
            Ze_emp = 0.031 * WC ** 1.56
            WC_tot += WC
        # Hagen and Yuter (2003)
        elif hyd_type.lower() == "pl":
            Ze_emp = ((WC * 1e3) / 3.4) ** 1.75
            WC_tot += WC
        else:
            # Hogan et al. (2006)
            if 2e9 <= instrument.freq < 4e9:
                Ze_emp = 10 ** (((np.log10(WC) + 0.0197 * t_values + 1.7) / 0.060) / 10.)
            elif 27e9 <= instrument.freq < 40e9:
                Ze_emp = 10 ** (((np.log10(WC) + 0.0186 * t_values + 1.63) /
                                 (0.000242 * t_values + 0.0699)) / 10.)
            elif 75e9 <= instrument.freq < 110e9:
                Ze_emp = 10 ** (((np.log10(WC) + 0.00706 * t_values + 0.992) /
                                 (0.000580 * t_values + 0.0923)) / 10.)
            else:
                Ze_emp = 10 ** (((np.log10(WC) + 0.0186 * t_values + 1.63) /
                                 (0.000242 * t_values + 0.0699)) / 10.)

        var_name = "sub_col_Ze_%s_%s" % (hyd_type, cloud_str)
        model.ds[var_name] = xr.DataArray(
            Ze_emp.values, dims=model.ds[q_field].dims)
        model.ds["sub_col_Ze_tot_%s" % cloud_str] += Ze_emp

    kappa_f = 6 * np.pi / (instrument.wavelength * model.Rho_hyd["cl"].magnitude) * \
        ((instrument.eps_liq - 1) / (instrument.eps_liq + 2)).imag * 4.34e6  # dB m^3 g^-1 km^-1
    model = accumulate_attenuation(model, is_conv, z_values, WC_tot * kappa_f, atm_ext,
                                   OD_from_sfc=OD_from_sfc, use_empiric_calc=True, **kwargs)

    return model


def calc_radar_bulk(instrument, model, is_conv, p_values, z_values, atm_ext, OD_from_sfc=True,
                    hyd_types=None, mie_for_ice=False, **kwargs):
    """
    Calculates the radar stratiform or convective reflectivity and attenuation
    in a sub-columns using bulk scattering LUTs assuming geometric scatterers
    (radiation scheme logic).
    Effective radii for each hydrometeor class must be provided (in model.ds).

    Parameters
    ----------
    instrument: Instrument
        The instrument to simulate. The instrument must be a lidar.
    model: Model
        The model to generate the parameters for.
    is_conv: bool
        True if the cell is convective
    p_values: ndarray
        model output pressure array in Pa.
    z_values: ndarray
        model output height array in m.
    atm_ext: ndarray
        atmospheric attenuation per layer (dB/km).
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    hyd_types: list or None
        list of hydrometeor names to include in calcuation. using 4 classes if None.
    mie_for_ice: bool
        If True, using bulk mie caculation LUTs. Otherwise, currently using the bulk C6
        scattering LUTs for 8-column severly roughned aggregate.
    Additonal keyword arguments are passed into
    :py:func:`emc2.simulator.lidar_moments.accumulate_attenuation`.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The model with the added simulated lidar parameters.
    """
    if hyd_types is None:
        hyd_types = ["cl", "ci", "pl", "pi"]

    if is_conv:
        cloud_str = "conv"
        re_fields = model.conv_re_fields
    else:
        cloud_str = "strat"
        re_fields = model.strat_re_fields

    Dims = model.ds["%s_q_subcolumns_cl" % cloud_str].shape
    model.ds["sub_col_Ze_tot_%s" % cloud_str] = xr.DataArray(
        np.zeros(Dims), dims=model.ds["%s_q_subcolumns_cl" % cloud_str].dims)
    hyd_ext = np.zeros(Dims)

    rhoa_dz = np.tile(np.abs(np.diff(p_values, axis=1, append=0.)) / instrument.g,
                      (model.num_subcolumns, 1, 1))
    dz = np.tile(np.diff(z_values, axis=1, append=0.), (model.num_subcolumns, 1, 1))
    for hyd_type in hyd_types:
        if hyd_type[-1] == 'l':
            rho_b = model.Rho_hyd[hyd_type]  # bulk water
            re_array = np.tile(model.ds[re_fields[hyd_type]], (model.num_subcolumns, 1, 1))
        else:
            rho_b = instrument.rho_i  # bulk ice
            fi_factor = model.fluffy[hyd_type] * model.Rho_hyd[hyd_type] / rho_b + \
                (1 - model.fluffy[hyd_type]) * (model.Rho_hyd[hyd_type] / rho_b) ** (1 / 3)
            re_array = np.tile(model.ds[re_fields[hyd_type]] * fi_factor,
                               (model.num_subcolumns, 1, 1))

        tau_hyd = np.where(model.ds["%s_q_subcolumns_%s" % (cloud_str, hyd_type)] > 0,
                           3 * model.ds["%s_q_subcolumns_%s" % (cloud_str, hyd_type)] * rhoa_dz /
                           (2 * rho_b * re_array * 1e-6), 0)
        A_hyd = tau_hyd / (2 * dz)  # model assumes geometric scatterers

        if np.isin(hyd_type, ["ci", "pi"]):
            if mie_for_ice:
                r_eff_bulk = instrument.bulk_table["mie_ice"]["r_e"].values
                Qback_bulk = instrument.bulk_table["mie_ice"]["Q_back"].values
                Qext_bulk = instrument.bulk_table["mie_ice"]["Q_ext"].values
            else:
                r_eff_bulk = instrument.bulk_table["8col_agg"]["r_e"].values
                Qback_bulk = instrument.bulk_table["8col_agg"]["Q_back"].values
                Qext_bulk = instrument.bulk_table["8col_agg"]["Q_ext"].values
        else:
            r_eff_bulk = instrument.bulk_table["mie_liq"]["r_e"].values
            Qback_bulk = instrument.bulk_table["mie_liq"]["Q_back"].values
            Qext_bulk = instrument.bulk_table["mie_liq"]["Q_ext"].values

        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)] = xr.DataArray(
            (np.interp(re_array, r_eff_bulk, Qback_bulk) * A_hyd * instrument.wavelength ** 4) /
            (instrument.K_w * np.pi ** 5) * 1e-6,
            dims=model.ds["%s_q_subcolumns_cl" % cloud_str].dims)

        model.ds["sub_col_Ze_tot_%s" % cloud_str] += model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)]
        hyd_ext += np.interp(re_array, r_eff_bulk, Qext_bulk) * A_hyd

    model = accumulate_attenuation(model, is_conv, z_values, hyd_ext, atm_ext,
                                   OD_from_sfc=OD_from_sfc, use_empiric_calc=False, **kwargs)

    return model


def calc_radar_micro(instrument, model, z_values, atm_ext, OD_from_sfc=True,
                     hyd_types=None, mie_for_ice=True, parallel=True, chunk=None, **kwargs):
    """
    Calculates the first 3 radar moments (reflectivity, mean Doppler velocity and spectral
    width) in a given column for the given radar using the microphysics (MG2) logic.

    Parameters
    ----------
    instrument: Instrument
        The instrument to simulate. The instrument must be a lidar.
    model: Model
        The model to generate the parameters for.
    z_values: ndarray
        model output height array in m.
    atm_ext: ndarray
        atmospheric attenuation per layer (dB/km).
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    hyd_types: list or None
        list of hydrometeor names to include in calcuation. using 4 classes if None.
    mie_for_ice: bool
        If True, using full mie caculation LUTs. Otherwise, currently using the C6
        scattering LUTs for 8-column severly roughned aggregate.
    parallel: bool
        If True, use parallelism in calculating lidar parameters.
    chunk: int or None
        The number of entries to process in one parallel loop. None will send all of
        the entries to the Dask worker queue at once. Sometimes, Dask will freeze if
        too many tasks are sent at once due to memory issues, so adjusting this number
        might be needed if that happens.
    Additonal keyword arguments are passed into
    :py:func:`emc2.simulator.psd.calc_mu_lambda`.
    :py:func:`emc2.simulator.lidar_moments.accumulate_attenuation`.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The model with the added simulated lidar parameters.
    """
    if hyd_types is None:
        hyd_types = ["cl", "ci", "pl", "pi"]

    method_str = "LUTs (microphysics logic)"

    Dims = model.ds["strat_q_subcolumns_cl"].values.shape

    if mie_for_ice:
        scat_str = "Mie"
    else:
        scat_str = "C6"

    moment_denom_tot = np.zeros(Dims)
    V_d_numer_tot = np.zeros(Dims)
    sigma_d_numer_tot = np.zeros(Dims)

    for hyd_type in hyd_types:
        frac_names = model.strat_frac_names[hyd_type]
        if not np.isin("sub_col_Ze_tot_strat", [x for x in model.ds.keys()]):
            model.ds["sub_col_Ze_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
            model.ds["sub_col_Vd_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
            model.ds["sub_col_sigma_d_tot_strat"] = xr.DataArray(
                np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
        model.ds["sub_col_Ze_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
        model.ds["sub_col_Vd_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
        model.ds["sub_col_sigma_d_%s_strat" % hyd_type] = xr.DataArray(
            np.zeros(Dims), dims=model.ds.strat_q_subcolumns_cl.dims)
        fits_ds = calc_mu_lambda(model, hyd_type, subcolumns=True, **kwargs).ds
        total_hydrometeor = model.ds[frac_names] * model.ds[model.N_field[hyd_type]]
        if np.logical_and(np.isin(hyd_type, ["ci", "pi"]), not mie_for_ice):
            p_diam = instrument.c6_table["8col_agg"]["p_diam_eq_V"].values
            beta_p = instrument.c6_table["8col_agg"]["beta_p"].values
            alpha_p = instrument.c6_table["8col_agg"]["alpha_p"].values
        else:
            p_diam = instrument.mie_table[hyd_type]["p_diam"].values
            beta_p = instrument.mie_table[hyd_type]["beta_p"].values
            alpha_p = instrument.mie_table[hyd_type]["alpha_p"].values
        num_subcolumns = model.num_subcolumns
        v_tmp = model.vel_param_a[hyd_type] * p_diam ** model.vel_param_b[hyd_type]
        v_tmp = -v_tmp.magnitude
        if hyd_type == "cl":
            N_0 = fits_ds["N_0"].values
            lambdas = fits_ds["lambda"].values
            mu = fits_ds["mu"].values

            _calc_liquid = lambda x: _calculate_observables_liquid(
                x, total_hydrometeor, N_0, lambdas, mu,
                alpha_p, beta_p, v_tmp, num_subcolumns, instrument, p_diam)
            if parallel:
                print("Doing parallel radar calculations for %s" % hyd_type)
                if chunk is None:
                    tt_bag = db.from_sequence(np.arange(0, Dims[1], 1))
                    my_tuple = tt_bag.map(_calc_liquid).compute()
                else:
                    my_tuple = []
                    j = 0
                    while j < Dims[1]:
                        if j + chunk >= Dims[1]:
                            ind_max = Dims[1]
                        else:
                            ind_max = j + chunk
                        print("Stage 1 of 2: processing columns %d-%d out of %d" % (j, ind_max, Dims[1]))
                        tt_bag = db.from_sequence(np.arange(j, ind_max, 1))
                        my_tuple += tt_bag.map(_calc_liquid).compute()
                        j += chunk
            else:
                my_tuple = [x for x in map(_calc_liquid, np.arange(0, Dims[1], 1))]

            V_d_numer_tot = np.nan_to_num(np.stack([x[0] for x in my_tuple], axis=1))
            moment_denom_tot = np.nan_to_num(np.stack([x[1] for x in my_tuple], axis=1))
            hyd_ext = np.nan_to_num(np.stack([x[2] for x in my_tuple], axis=1))

            model.ds["sub_col_Ze_cl_strat"][:, :, :] = np.stack([x[3] for x in my_tuple], axis=1)
            model.ds["sub_col_Vd_cl_strat"][:, :, :] = np.stack([x[4] for x in my_tuple], axis=1)
            model.ds["sub_col_sigma_d_cl_strat"][:, :, :] = np.stack([x[5] for x in my_tuple], axis=1)
            del my_tuple
        else:
            sub_q_array = model.ds["strat_q_subcolumns_%s" % hyd_type].values
            _calc_other = lambda x: _calculate_other_observables(
                x, total_hydrometeor, fits_ds, model, instrument, sub_q_array, hyd_type, p_diam, mie_for_ice)
            if parallel:
                print("Doing parallel radar calculation for %s" % hyd_type)
                if chunk is None:
                    tt_bag = db.from_sequence(np.arange(0, Dims[1], 1))
                    my_tuple = tt_bag.map(_calc_other).compute()
                else:
                    my_tuple = []
                    j = 0
                    while j < Dims[1]:
                        if j + chunk >= Dims[1]:
                            ind_max = Dims[1]
                        else:
                            ind_max = j + chunk
                        print("Stage 1 of 2: Processing columns %d-%d out of %d" % (j, ind_max, Dims[1]))
                        tt_bag = db.from_sequence(np.arange(j, ind_max, 1))
                        my_tuple += tt_bag.map(_calc_other).compute()
                        j += chunk
            else:
                my_tuple = [x for x in map(_calc_other, np.arange(0, Dims[1], 1))]

            V_d_numer_tot += np.nan_to_num(np.stack([x[0] for x in my_tuple], axis=1))
            moment_denom_tot += np.nan_to_num(np.stack([x[1] for x in my_tuple], axis=1))
            hyd_ext = np.nan_to_num(np.stack([x[2] for x in my_tuple], axis=1))
            model.ds["sub_col_Ze_%s_strat" % hyd_type][:, :, :] = np.stack([x[3] for x in my_tuple], axis=1)
            model.ds["sub_col_Vd_%s_strat" % hyd_type][:, :, :] = np.stack([x[4] for x in my_tuple], axis=1)
            model.ds["sub_col_sigma_d_%s_strat" % hyd_type][:, :, :] = np.stack([x[5] for x in my_tuple], axis=1)

        if "sub_col_Ze_tot_strat" in model.ds.variables.keys():
            model.ds["sub_col_Ze_tot_strat"] += model.ds["sub_col_Ze_%s_strat" % hyd_type].fillna(0)
        else:
            model.ds["sub_col_Ze_tot_strat"] = model.ds["sub_col_Ze_%s_strat" % hyd_type].fillna(0)

        model.ds["sub_col_Vd_%s_strat" % hyd_type].attrs["long_name"] = \
            "Mean Doppler velocity from stratiform %s hydrometeors" % hyd_type
        model.ds["sub_col_Vd_%s_strat" % hyd_type].attrs["units"] = "m s-1"
        model.ds["sub_col_Vd_%s_strat" % hyd_type].attrs["Processing method"] = method_str
        model.ds["sub_col_sigma_d_%s_strat" % hyd_type].attrs["long_name"] = \
            "Spectral width from stratiform %s hydrometeors" % hyd_type
        model.ds["sub_col_sigma_d_%s_strat" % hyd_type].attrs["units"] = "m s-1"
        model.ds["sub_col_sigma_d_%s_strat" % hyd_type].attrs["Processing method"] = method_str
    model.ds["sub_col_Vd_tot_strat"] = xr.DataArray(V_d_numer_tot / moment_denom_tot,
                                                    dims=model.ds["sub_col_Ze_tot_strat"].dims)
    print("Now calculating total spectral width (this may take some time)")
    for hyd_type in hyd_types:
        if np.logical_and(np.isin(hyd_type, ["ci", "pi"]), not mie_for_ice):
            p_diam = instrument.c6_table["8col_agg"]["p_diam_eq_V"].values
            beta_p = instrument.c6_table["8col_agg"]["beta_p"].values
            alpha_p = instrument.c6_table["8col_agg"]["alpha_p"].values
        else:
            p_diam = instrument.mie_table[hyd_type]["p_diam"].values
            beta_p = instrument.mie_table[hyd_type]["beta_p"].values
            alpha_p = instrument.mie_table[hyd_type]["alpha_p"].values
        v_tmp = model.vel_param_a[hyd_type] * p_diam ** model.vel_param_b[hyd_type]
        v_tmp = -v_tmp.magnitude
        fits_ds = calc_mu_lambda(model, hyd_type, subcolumns=True, **kwargs).ds
        frac_names = model.strat_frac_names[hyd_type]
        total_hydrometeor = model.ds[frac_names] * model.ds[model.N_field[hyd_type]]
        if hyd_type == "cl":
            Vd_tot = model.ds["sub_col_Vd_tot_strat"].values
            _calc_sigma_d_liq = lambda x: _calc_sigma_d_tot_cl(
                x, fits_ds, instrument, model, total_hydrometeor, p_diam, Vd_tot)
            if parallel:
                if chunk is None:
                    tt_bag = db.from_sequence(np.arange(0, Dims[1], 1))
                    sigma_d_numer = tt_bag.map(_calc_sigma_d_liq).compute()
                else:
                    sigma_d_numer = []
                    j = 0
                    while j < Dims[1]:
                        if j + chunk >= Dims[1]:
                            ind_max = Dims[1]
                        else:
                            ind_max = j + chunk
                        print("Stage 2 of 2: Processing columns %d-%d out of %d" % (j, ind_max, Dims[1]))
                        tt_bag = db.from_sequence(np.arange(j, ind_max, 1))
                        sigma_d_numer += tt_bag.map(_calc_sigma_d_liq).compute()
                        j += chunk
            else:
                sigma_d_numer = [x for x in map(_calc_sigma_d_liq, np.arange(0, Dims[1], 1))]

            sigma_d_numer_tot = np.nan_to_num(np.stack([x[0] for x in sigma_d_numer], axis=1))
        else:
            sub_q_array = model.ds["strat_q_subcolumns_%s" % hyd_type].values
            _calc_sigma = lambda x: _calc_sigma_d_tot(
                x, model, v_tmp, fits_ds, total_hydrometeor, Vd_tot, sub_q_array, p_diam, beta_p)
            if parallel:
                if chunk is None:
                    tt_bag = db.from_sequence(np.arange(0, Dims[1], 1))
                    sigma_d_numer = tt_bag.map(_calc_sigma).compute()
                else:
                    sigma_d_numer = []
                    j = 0
                    while j < Dims[1]:
                        if j + chunk >= Dims[1]:
                            ind_max = Dims[1]
                        else:
                            ind_max = j + chunk
                        print("Stage 2 of 2: processing columns %d-%d out of %d" % (j, ind_max, Dims[1]))
                        tt_bag = db.from_sequence(np.arange(j, ind_max, 1))
                        sigma_d_numer += tt_bag.map(_calc_sigma).compute()
                        j += chunk
            else:
                sigma_d_numer = [x for x in map(_calc_sigma, np.arange(0, Dims[1], 1))]
            sigma_d_numer_tot += np.nan_to_num(np.stack([x[0] for x in sigma_d_numer], axis=1))

    model.ds["lambda"].values = model.ds["lambda"].values.astype("float64")
    model.ds["N_0"].values = model.ds["N_0"].values.astype("float64")

    model.ds["sub_col_sigma_d_tot_strat"] = xr.DataArray(np.sqrt(sigma_d_numer_tot / moment_denom_tot),
                                                         dims=model.ds["sub_col_Vd_tot_strat"].dims)

    model = accumulate_attenuation(model, False, z_values, hyd_ext, atm_ext,
                                   OD_from_sfc=OD_from_sfc, use_empiric_calc=False, **kwargs)

    model.ds['sub_col_Vd_tot_strat'].attrs["long_name"] = \
        "Mean Doppler velocity from all stratiform hydrometeors"
    model.ds['sub_col_Vd_tot_strat'].attrs["units"] = "m s-1"
    model.ds['sub_col_Vd_tot_strat'].attrs["Processing method"] = method_str
    model.ds['sub_col_Vd_tot_strat'].attrs["Ice scattering database"] = scat_str
    model.ds['sub_col_sigma_d_tot_strat'].attrs["long_name"] = \
        "Spectral width from all stratiform hydrometeors"
    model.ds['sub_col_sigma_d_tot_strat'].attrs["units"] = "m s-1"
    model.ds["sub_col_sigma_d_tot_strat"].attrs["Processing method"] = method_str
    model.ds["sub_col_sigma_d_tot_strat"].attrs["Ice scattering database"] = scat_str

    return model


def calc_radar_moments(instrument, model, is_conv,
                       OD_from_sfc=True, parallel=True, chunk=None, mie_for_ice=False, use_rad_logic=True,
                       use_empiric_calc=False, **kwargs):
    """
    Calculates the reflectivity, doppler velocity, and spectral width
    in a given column for the given radar.

    NOTE:
    When starting a parallel task (in microphysics approach), it is recommended
    to wrap the top-level python script calling the EMC^2 processing ('lines_of_code')
    with the following command (just below the 'import' statements):
    if __name__ == “__main__”:
        lines_of_code

    Parameters
    ----------
    instrument: Instrument
        The instrument to simulate. The instrument must be a radar.
    model: Model
        The model to generate the parameters for.
    is_conv: bool
        True if the cell is convective
    z_field: str
        The name of the altitude field to use.
    OD_from_sfc: bool
        If True, then calculate optical depth from the surface.
    parallel: bool
        If True, then use parallelism to calculate each column quantity.
    chunk: None or int
        If using parallel processing, only send this number of time periods to the
        parallel loop at one time. Sometimes Dask will crash if there are too many
        tasks in the queue, so setting this value will help avoid that.
    mie_for_ice: bool
        If True, using full mie caculation LUTs. Otherwise, currently using the C6
        scattering LUTs for 8-column aggregate at 270 K.
    use_rad_logic: bool
        When True using radiation scheme logic in calculations, which includes using
        the cloud fraction fields utilized in a model radiative scheme, as well as bulk
        scattering LUTs (effective radii dependent scattering variables). Otherwise, and
        only in the stratiform case, using the microphysics scheme logic, which includes
        the cloud fraction fields utilized by the model microphysics scheme and single
        particle scattering LUTs.
        NOTE: because of its single-particle calculation method, the microphysics
        approach is significantly slower than the radiation approach. Also, the cloud
        fraction logic in these  schemes does not necessarilytly fully overlap.
    use_empirical_calc: bool
        When True using empirical relations from literature for the fwd calculations
        (the cloud fraction still follows the scheme logic set by use_rad_logic).
    Additonal keyword arguments are passed into
    :py:func:`emc2.simulator.psd.calc_mu_lambda`.
    :py:func:`emc2.simulator.lidar_moments.accumulate_attenuation`.
    :py:func:`emc2.simulator.lidar_moments.calc_radar_empirical`.
    :py:func:`emc2.simulator.lidar_moments.calc_radar_bulk`.
    :py:func:`emc2.simulator.lidar_moments.calc_radar_micro`.

    Returns
    -------
    model: :func:`emc2.core.Model`
        The xarray Dataset containing the calculated radar moments.
    """

    hyd_types = ["cl", "ci", "pl", "pi"]

    if is_conv:
        cloud_str = "conv"
        cloud_str_full = "convective"
        if np.logical_and(not use_empiric_calc, not use_rad_logic):
            use_rad_logic = True  # Force rad scheme logic if in conv scheme
    else:
        cloud_str = "strat"
        cloud_str_full = "stratiform"

    if use_empiric_calc:
        scat_str = "Empirical (no utilized scattering database)"
    elif mie_for_ice:
        scat_str = "Mie"
    else:
        scat_str = "C6"

    if not instrument.instrument_class.lower() == "radar":
        raise ValueError("Instrument must be a radar!")

    if "%s_q_subcolumns_cl" % cloud_str not in model.ds.variables.keys():
        raise KeyError("Water mixing ratio in %s subcolumns must be generated first!" % cloud_str_full)

    p_field = model.p_field
    t_field = model.T_field
    z_field = model.z_field

    # Do unit conversions using pint - pressure in Pa, T in K, z in m
    p_temp = model.ds[p_field].values * getattr(ureg, model.ds[p_field].attrs["units"])
    p_values = p_temp.to('pascal').magnitude
    t_temp = quantity(model.ds[t_field].values, model.ds[t_field].attrs["units"])
    t_values = t_temp.to('celsius').magnitude
    z_temp = model.ds[z_field].values * getattr(ureg, model.ds[z_field].attrs["units"])
    z_values = z_temp.to('meter').magnitude
    del p_temp, t_temp, z_temp

    kappa_ds = calc_radar_atm_attenuation(instrument, model)
    atm_ext = kappa_ds.ds["kappa_att"].values

    t0 = time()
    if use_empiric_calc:
        print("Generating %s radar variables using empirical formulation" % cloud_str_full)
        method_str = "Empirical"
        model = calc_radar_empirical(instrument, model, is_conv, p_values, t_values, z_values,
                                     atm_ext, OD_from_sfc=OD_from_sfc, hyd_types=hyd_types, **kwargs)
    elif use_rad_logic:
        print("Generating %s radar variables using radiation logic" % cloud_str_full)
        method_str = "Bulk (radiation logic)"
        model = calc_radar_bulk(instrument, model, is_conv, p_values, z_values,
                                atm_ext, OD_from_sfc=OD_from_sfc, mie_for_ice=mie_for_ice, hyd_types=hyd_types,
                                **kwargs)
    else:
        print("Generating %s radar variables using microphysics logic (slowest processing)" % cloud_str_full)
        method_str = "LUTs (microphysics logic)"
        calc_radar_micro(instrument, model, z_values, atm_ext, OD_from_sfc=OD_from_sfc,
                         hyd_types=hyd_types, mie_for_ice=mie_for_ice, parallel=parallel, chunk=chunk, **kwargs)

    for hyd_type in hyd_types:
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)] = 10 * np.log10(
            model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)])
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)] = model.ds[
            "sub_col_Ze_%s_%s" % (hyd_type, cloud_str)].where(
            np.isfinite(model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)]))
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)].attrs["long_name"] = \
            "Equivalent radar reflectivity factor from %s %s hydrometeors" % (cloud_str_full, hyd_type)
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)].attrs["units"] = "dBZ"
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)].attrs["Processing method"] = method_str
        model.ds["sub_col_Ze_%s_%s" % (hyd_type, cloud_str)].attrs["Ice scattering database"] = scat_str

    model.ds['sub_col_Ze_att_tot_%s' % cloud_str] = model.ds["sub_col_Ze_tot_%s" % cloud_str] * \
        model.ds['hyd_ext_%s' % cloud_str].fillna(1) * model.ds['atm_ext'].fillna(1)
    model.ds["sub_col_Ze_tot_%s" % cloud_str] = model.ds["sub_col_Ze_tot_%s" % cloud_str].where(
        np.isfinite(model.ds["sub_col_Ze_tot_%s" % cloud_str]))
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str] = model.ds["sub_col_Ze_att_tot_%s" % cloud_str].where(
        np.isfinite(model.ds["sub_col_Ze_att_tot_%s" % cloud_str]))
    model.ds["sub_col_Ze_tot_%s" % cloud_str] = 10 * np.log10(model.ds["sub_col_Ze_tot_%s" % cloud_str])
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str] = 10 * np.log10(model.ds["sub_col_Ze_att_tot_%s" % cloud_str])
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str].attrs["long_name"] = \
        "Attenuated equivalent radar reflectivity factor from all %s hydrometeors" % cloud_str_full
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str].attrs["units"] = "dBZ"
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str].attrs["Processing method"] = method_str
    model.ds["sub_col_Ze_att_tot_%s" % cloud_str].attrs["Ice scattering database"] = scat_str
    model.ds["sub_col_Ze_tot_%s" % cloud_str].attrs["long_name"] = \
        "Equivalent radar reflectivity factor from all %s hydrometeors" % cloud_str_full
    model.ds["sub_col_Ze_tot_%s" % cloud_str].attrs["units"] = "dBZ"
    model.ds["sub_col_Ze_tot_%s" % cloud_str].attrs["Processing method"] = method_str
    model.ds["sub_col_Ze_tot_%s" % cloud_str].attrs["Ice scattering database"] = scat_str
    model.ds['hyd_ext_%s' % cloud_str].attrs["Processing method"] = method_str
    model.ds['hyd_ext_%s' % cloud_str].attrs["Ice scattering database"] = scat_str

    print("Done! total processing time = %.2fs" % (time() - t0))

    return model


def _calc_sigma_d_tot_cl(tt, fits_ds, instrument, model, total_hydrometeor, p_diam, Vd_tot):
    hyd_type = "cl"
    sigma_d_numer = np.zeros((model.num_subcolumns, total_hydrometeor.shape[1]), dtype='float64')
    moment_denom = np.zeros((model.num_subcolumns, total_hydrometeor.shape[1]), dtype='float64')
    if tt % 50 == 0:
        print('Stratiform moment for class cl progress: %d/%d' % (tt, total_hydrometeor.shape[1]))
    num_diam = len(p_diam)
    Dims = Vd_tot.shape
    for k in range(Dims[2]):
        if total_hydrometeor[tt, k] == 0:
            continue
        N_0_tmp = fits_ds["N_0"].values[:, tt, k].astype('float64')
        N_0_tmp, d_diam_tmp = np.meshgrid(N_0_tmp, p_diam)
        lambda_tmp = fits_ds["lambda"].values[:, tt, k].astype('float64')
        lambda_tmp, d_diam_tmp = np.meshgrid(lambda_tmp, p_diam)
        mu_temp = fits_ds["mu"].values[:, tt, k] * np.ones_like(lambda_tmp)
        N_D = N_0_tmp * d_diam_tmp ** mu_temp * np.exp(-lambda_tmp * d_diam_tmp)
        Calc_tmp = np.tile(
            instrument.mie_table[hyd_type]["beta_p"].values, (model.num_subcolumns, 1)) * N_D.T
        moment_denom = np.trapz(Calc_tmp, x=p_diam, axis=1).astype('float64')
        v_tmp = model.vel_param_a[hyd_type] * p_diam ** model.vel_param_b[hyd_type]
        v_tmp = -v_tmp.magnitude.astype('float64')
        Calc_tmp2 = (v_tmp - np.tile(Vd_tot[:, tt, k], (num_diam, 1)).T) ** 2 * Calc_tmp.astype('float64')
        sigma_d_numer[:, k] = np.trapz(Calc_tmp2, x=p_diam, axis=1)

    return sigma_d_numer, moment_denom


def _calc_sigma_d_tot(tt, model, v_tmp, fits_ds, total_hydrometeor, vd_tot, sub_q_array, p_diam, beta_p):
    Dims = vd_tot.shape
    sigma_d_numer = np.zeros((model.num_subcolumns, total_hydrometeor.shape[1]), dtype='float64')
    moment_denom = np.zeros((model.num_subcolumns, total_hydrometeor.shape[1]), dtype='float64')
    num_diam = len(p_diam)
    mu = fits_ds["mu"].values.max()
    if tt % 50 == 0:
        print('Stratiform moment for class progress: %d/%d' % (tt, Dims[1]))
    for k in range(Dims[2]):
        if total_hydrometeor[tt, k] == 0:
            continue
        N_0_tmp = fits_ds["N_0"][:, tt, k].values
        lambda_tmp = fits_ds["lambda"][:, tt, k].values
        if np.all(np.isnan(N_0_tmp)):
            continue
        N_D = []
        for i in range(model.num_subcolumns):
            N_D.append(N_0_tmp[i] * p_diam ** mu * np.exp(-lambda_tmp[i] * p_diam))
        N_D = np.stack(N_D, axis=1).astype('float64')

        Calc_tmp = np.tile(beta_p, (model.num_subcolumns, 1)) * N_D.T
        moment_denom = np.trapz(Calc_tmp, x=p_diam, axis=1).astype('float64')
        Calc_tmp2 = (v_tmp - np.tile(vd_tot[:, tt, k], (num_diam, 1)).T) ** 2 * Calc_tmp.astype('float64')
        Calc_tmp2 = np.trapz(Calc_tmp2, x=p_diam, axis=1)
        sigma_d_numer[:, k] = np.where(sub_q_array[:, tt, k] == 0, 0, Calc_tmp2)

    return sigma_d_numer, moment_denom


def _calculate_observables_liquid(tt, total_hydrometeor, N_0, lambdas, mu,
                                  alpha_p, beta_p, v_tmp, num_subcolumns, instrument, p_diam):
    height_dims = N_0.shape[2]
    V_d_numer_tot = np.zeros((num_subcolumns, height_dims))
    V_d = np.zeros((num_subcolumns, height_dims))
    Ze = np.zeros_like(V_d)
    sigma_d = np.zeros_like(V_d)
    moment_denom_tot = np.zeros_like(V_d_numer_tot)
    hyd_ext = np.zeros_like(V_d_numer_tot)
    num_diam = len(p_diam)
    if tt % 50 == 0:
        print("Processing column %d" % tt)
    np.seterr(all="ignore")
    for k in range(height_dims):
        if total_hydrometeor[tt, k] == 0:
            continue
        if num_subcolumns > 1:
            N_0_tmp = np.squeeze(N_0[:, tt, k])
            lambda_tmp = np.squeeze(lambdas[:, tt, k])
            mu_temp = np.squeeze(mu[:, tt, k])
        else:
            N_0_tmp = N_0[:, tt, k]
            lambda_tmp = lambdas[:, tt, k]
            mu_temp = mu[:, tt, k]
        if all([np.isnan(x) for x in N_0_tmp]):
            continue

        N_D = []
        for i in range(num_subcolumns):
            N_D.append(N_0_tmp[i] * p_diam ** mu_temp[i] * np.exp(-lambda_tmp[i] * p_diam))
        N_D = np.stack(N_D, axis=0)

        Calc_tmp = beta_p * N_D
        tmp_od = np.trapz(alpha_p * N_D, x=p_diam, axis=1)
        moment_denom = np.trapz(Calc_tmp, x=p_diam, axis=1).astype('float64')
        Ze[:, k] = \
            (moment_denom * instrument.wavelength ** 4) / (instrument.K_w * np.pi ** 5) * 1e-6

        Calc_tmp2 = v_tmp * Calc_tmp.astype('float64')
        V_d_numer = np.trapz(Calc_tmp2, x=p_diam, axis=1)
        V_d[:, k] = V_d_numer / moment_denom
        Calc_tmp2 = (v_tmp - np.tile(V_d[:, k], (num_diam, 1)).T) ** 2 * Calc_tmp
        sigma_d_numer = np.trapz(Calc_tmp2, x=p_diam, axis=1)
        sigma_d[:, k] = np.sqrt(sigma_d_numer / moment_denom)
        V_d_numer_tot[:, k] += V_d_numer
        moment_denom_tot[:, k] += moment_denom
        hyd_ext[:, k] += tmp_od

    return V_d_numer_tot, moment_denom_tot, hyd_ext, Ze, V_d, sigma_d


def _calculate_other_observables(tt, total_hydrometeor, fits_ds, model, instrument, sub_q_array,
                                 hyd_type, p_diam, mie_for_ice):
    Dims = sub_q_array.shape
    if tt % 50 == 0:
        print('Stratiform moment for class %s progress: %d/%d' % (hyd_type, tt, Dims[1]))
    Ze = np.zeros((model.num_subcolumns, Dims[2]))
    V_d = np.zeros_like(Ze)
    sigma_d = np.zeros_like(Ze)
    V_d_numer_tot = np.zeros_like(Ze)
    moment_denom_tot = np.zeros_like(Ze)
    hyd_ext = np.zeros_like(Ze)
    for k in range(Dims[2]):
        if total_hydrometeor[tt, k] == 0:
            continue

        num_diam = len(p_diam)
        N_D = []
        for i in range(model.num_subcolumns):
            N_0_tmp = fits_ds["N_0"][i, tt, k].values
            lambda_tmp = fits_ds["lambda"][i, tt, k].values
            N_D.append(N_0_tmp * np.exp(-lambda_tmp * p_diam))
        N_D = np.stack(N_D, axis=0)
        if np.logical_and(np.isin(hyd_type, ["ci", "pi"]), not mie_for_ice):
            Calc_tmp = np.tile(instrument.c6_table["8col_agg"]["beta_p"].values,
                               (model.num_subcolumns, 1)) * N_D
            tmp_od = np.tile(
                instrument.c6_table["8col_agg"]["alpha_p"].values, (model.num_subcolumns, 1)) * N_D
        else:
            Calc_tmp = np.tile(instrument.mie_table[hyd_type]["beta_p"].values,
                               (model.num_subcolumns, 1)) * N_D
            tmp_od = np.tile(
                instrument.mie_table[hyd_type]["alpha_p"].values, (model.num_subcolumns, 1)) * N_D
        tmp_od = np.trapz(tmp_od, x=p_diam, axis=1)
        tmp_od = np.where(sub_q_array[:, tt, k] == 0, 0, tmp_od)
        moment_denom = np.trapz(Calc_tmp, x=p_diam, axis=1)
        moment_denom = np.where(sub_q_array[:, tt, k] == 0, 0, moment_denom)
        Ze[:, k] = \
            (moment_denom * instrument.wavelength ** 4) / (instrument.K_w * np.pi ** 5) * 1e-6
        v_tmp = model.vel_param_a[hyd_type] * p_diam ** model.vel_param_b[hyd_type]
        v_tmp = -v_tmp.magnitude
        Calc_tmp2 = Calc_tmp * v_tmp
        V_d_numer = np.trapz(Calc_tmp2, axis=1, x=p_diam)
        V_d_numer = np.where(sub_q_array[:, tt, k] == 0, 0, V_d_numer)
        V_d[:, k] = V_d_numer / moment_denom
        Calc_tmp2 = (v_tmp - np.tile(V_d[:, k], (num_diam, 1)).T) ** 2 * Calc_tmp
        Calc_tmp2 = np.trapz(Calc_tmp2, axis=1, x=p_diam)
        sigma_d_numer = np.where(sub_q_array[:, tt, k] == 0, 0, Calc_tmp2)
        sigma_d[:, k] = np.sqrt(sigma_d_numer / moment_denom)
        V_d_numer_tot[:, k] += V_d_numer
        moment_denom_tot[:, k] += moment_denom
        hyd_ext[:, k] += tmp_od

    return V_d_numer_tot, moment_denom_tot, hyd_ext, Ze, V_d, sigma_d
