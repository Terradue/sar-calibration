import os
import sys
import logging
import click
from click2cwl import dump
from pystac import Catalog, CatalogType
from .stachelp import get_item
from .calibrator import Calibrator


logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command(
    short_help="short help",
    help="help!!",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    )
)
@click.option(
    "--input_path",
    "-i",
    "input_path",
    help="help for input reference",
    type=click.Path(),
    required=True,
)
@click.pass_context
def main(ctx, input_path):

    # dump the CWL and params (if requested)
    dump(ctx)

    if 'TMPDIR' in os.environ:
        os.chdir(os.environ['TMPDIR'])

    logging.info(os.path.join(input_path, 'catalog.json'))

    item = get_item(os.path.join(input_path, 'catalog.json'))

    output_dir = f'{item.id}'

    calibrator = Calibrator()

    item_out = calibrator.calibrate(item)

    logging.info('STAC')

    cat = Catalog(id='catalog',
                  description="Calibrated sar product")

    cat.add_items([item_out])

    cat.normalize_and_save(root_href='./',
                           catalog_type=CatalogType.SELF_CONTAINED)

    logging.info('Done!')


    #os.mkdir(output_dir)

    sys.exit(0)

if __name__ == '__main__':
    main()
