import click

from wetrad import wet_radome_attn, open_xradar


@click.command()
@click.argument("file0", type=click.Path(exists=True))
@click.argument("file1", type=click.Path(exists=True))
@click.option(
    "--ranges",
    "-r",
    type=int,
    multiple=True,
    default=[5],
    help="Range gates to consider",
)
def wetrad(file0, file1, ranges):
    """The wetrad command line interface."""
    ds0 = open_xradar(file0)
    ds1 = open_xradar(file1)
    attn = wet_radome_attn(ds0, ds1, gates=ranges)
    print(f"Wet radome attenuation: {attn:.1f} dB")