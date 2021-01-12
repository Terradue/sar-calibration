import os
import sys
import logging
import click
from click2cwl import dump

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command(
    short_help="short help",
    help="help",
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
@click.option(
    "--aoi",
    "-a",
    "aoi",
    help="help for the area of interest",
    required=True,
)
@click.pass_context
def main(ctx, input_path, aoi):

    # dump the CWL and params (if requested)
    dump(ctx)

    print(input_path, aoi)

    sys.exit(0)

if __name__ == '__main__':
    main()
