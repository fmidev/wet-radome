"""Apply wet radome attenuation correction to ODIM data using xradar."""

import h5py
import xradar as xd


def get_source(odimfile):
    """Get source parameter of ODIM file."""
    with h5py.File(odimfile, "r") as f:
        src = f['/what'].attrs['source'].decode()
    # drop fields with non-ascii characters
    lst = src.split(',')
    src = ','.join([s for s in lst if all(ord(c) < 128 for c in s)])
    return src


def apply_correction_sweep(swp, attenuation, field='DBZH'):
    """Apply wet radome attenuation correction to DBZ field in xarray dataset.
    """
    out = swp.copy()
    try:
        out[field] += attenuation
    except KeyError:
        return swp.copy()
    return out


def apply_correction_odim(file_in, file_out, attenuation, **kws):
    """Apply wet radome attenuation correction to DBZH field in ODIM HDF5 file.
    """
    radar = xd.io.open_odim_datatree(file_in)
    radar = radar.map_over_subtree(
        apply_correction_sweep, attenuation, **kws
    )
    src = get_source(file_in)
    xd.io.to_odim(radar, file_out, source=src)


if __name__ == '__main__':
    import os
    filename1 = os.path.expanduser("~/data/polar/fiuta/202208051335_radar.polar.fiuta.h5")
    ds1 = xd.io.open_odim_datatree(filename1)
    attn = 0.5
    apply_correction_odim(filename1, filename1.replace(".h5", ".wetrad.h5"), attn)
    print(f"Attenuation: {attn:.2f} dB")
