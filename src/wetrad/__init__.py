import os

import matplotlib.pyplot as plt
import xarray as xr
import xradar as xd


def plot_ppi(da, ax=None, **kws):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    da.plot(ax=ax, x="x", y="y", **kws)
    fig.tight_layout()
    return ax


def plot_dbz(ds, minv=-10, **kws):
    dbz = ds.DBZH.where(ds.DBZH >= minv)
    ax = plot_ppi(dbz, vmin=-22, vmax=60, cmap="gist_ncar", **kws)
    return ax


def plot_rings(ds, gates=(10,), **kws):
    rings = ds.TH.copy()
    rings.data.fill(0)
    rings.data[:, gates] = 1.0
    ax = plot_ppi(rings.where(rings > 0), colors="k", levels=[0.5], add_colorbar=False, **kws)
    return ax


def intense_precip_over_radar(swp, gates=(10,), dbz_thr=45, fraction=0.9):
    """Check if the radar is in intense precipitation."""
    dbz_at_gates = swp.DBZH.isel(range=gates)
    return (dbz_at_gates >= dbz_thr).sum() / len(gates) >= fraction


if __name__ == "__main__":
    filename = os.path.expanduser("~/data/polar/filuo/202208170030_radar.polar.filuo.h5")
    ds = xr.open_dataset(filename, group="sweep_0", engine="odim").xradar.georeference()
    ax = plot_dbz(ds)
    rangem = 50e3
    ax.set_xlim(-rangem, rangem)
    ax.set_ylim(-rangem, rangem)
    gates = (15,)
    plot_rings(ds, gates=gates, ax=ax)