import os
import sys
import gdal
import logging 

from snapista import Graph, Operator

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def calibrate(item):

    logging(f'Calibrate Sentinel-1 GRD acquisition {item.id}')

    g = Graph()

    g.add_node(
        operator=Operator(
            "Read", 
            formatName="SENTINEL-1", 
            file=item.get_assets()['manifest'].get_absolute_href().replace('file://', '')
        ), 
        node_id="read"
    )

    g.add_node(
        operator=Operator("Apply-Orbit-File", continueOnFail="true"),
        node_id="apply-orbit-file",
        source="read",
    )

    g.add_node(
        operator=Operator("Remove-GRD-Border-Noise", borderLimit="2000", trimThreshold="0.2"),
        node_id="noise-removal",
        source="apply-orbit-file",
    )

    g.add_node(
        operator=Operator("Calibration", selectedPolarisations="VV"),
        node_id="calibration",
        source="noise-removal",
    )

    g.add_node(
        operator=Operator("LinearToFromdB", sourceBandNames="Sigma0_VV"),
        node_id="linear",
        source="calibration",
    )

    g.add_node(
        operator=Operator(
            "Terrain-Correction", pixelSpacingInMeter="20.0", demName="SRTM 1Sec HGT"
        ),
        node_id="terrain-correction",
        source="linear",
    )

    g.add_node(
        operator=Operator("Write", file=f"{item.id}_SIGMA0_DB", formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="terrain-correction",
    )

    g.run()

    return g