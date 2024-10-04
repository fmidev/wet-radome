"""wet radome attenuation estimation"""

import os

import matplotlib.pyplot as plt
import xarray as xr
import xradar as xd


def plot_ppi(da, ax=None, **kws):
    """plot PPI"""
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    da.plot(ax=ax, x="x", y="y", **kws)
    fig.tight_layout()
    return ax


def plot_dbz(dbz, minv=-10, **kws):
    """plot reflectivity"""
    dbz = dbz.where(dbz >= minv)
    ax = plot_ppi(dbz, vmin=-22, vmax=60, cmap="gist_ncar", **kws)
    return ax


def plot_rings(ds, gates=(10,), **kws):
    """plot rings at given range gates"""
    rings = ds.TH.copy()
    rings.data.fill(0)
    rings.data[:, gates] = 1.0
    ax = plot_ppi(rings.where(rings > 0), colors="k", levels=[0.5], add_colorbar=False, **kws)
    return ax


def percentile_at_range(da, ranges=[15], quantile=0.5):
    """percentile at given range gates"""
    return da.isel(range=ranges).quantile(quantile).values.item()


def linear_attn_adjust(dbz, dbz_min=30, dbz_max=45, adjust_max=6.5, **kws):
    """Linear wet radome attenuation adjustment"""
    percentile = percentile_at_range(dbz, **kws)
    if percentile < dbz_min:
        return 0.0
    elif percentile > dbz_max:
        return adjust_max
    return adjust_max * (percentile - dbz_min) / (dbz_max - dbz_min)
    

def open_xradar(filename, group="sweep_2", engine="odim"):
    """open_dataset xradar wrapper"""
    return xr.open_dataset(filename, group=group, engine=engine).xradar.georeference()


def wet_radome_attn(ds0, ds1, gates=[5]):
    """Wet radome attenuation in dB"""
    adj0 = linear_attn_adjust(ds0.TH, ranges=gates)
    adj1 = linear_attn_adjust(ds1.TH, ranges=gates)
    return min(adj0, adj1)


if __name__ == "__main__":
    plt.close("all")
    filename0 = os.path.expanduser("~/data/polar/fiuta/202208051330_radar.polar.fiuta.h5")
    filename1 = os.path.expanduser("~/data/polar/fiuta/202208051335_radar.polar.fiuta.h5")
    #xd.io.open_odim_datatree(filename1)
    ds0 = open_xradar(filename0)
    ds1 = open_xradar(filename1)
    ax = plot_dbz(ds1.TH)
    rangem = 50e3
    ax.set_xlim(-rangem, rangem)
    ax.set_ylim(-rangem, rangem)
    gates = [5]
    plot_rings(ds1, gates=gates, ax=ax)
    print(wet_radome_attn(ds0, ds1, gates=gates))