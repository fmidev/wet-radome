import click

from wetrad.estimation import wet_radome_attn, open_xradar
from wetrad.correction import apply_correction_odim


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
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output ODIM H5 file",
)
@click.version_option()
def wetrad(file0, file1, ranges, output):
    """Wet radome attenuation correction.

    Compute wet radome attenuation for FILE1.
    FILE0 is the previous scan used for estimating the persistence of precipitation.
    """
    ds0 = open_xradar(file0)
    ds1 = open_xradar(file1)
    attn = wet_radome_attn(ds0, ds1, gates=list(ranges))
    if output:
        apply_correction_odim(file1, output, attn)
    else:
        print(f"{attn:.2f}")
