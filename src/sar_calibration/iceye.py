import os
from .output import rescale
from snapista import Graph, Operator


def calibrate(item):

    temp_calibrated_product = f"temp_{item.id}_SIGMA0_DB"
    calibrated_product = f"{item.id}_SIGMA0_DB"

    g = Graph()

    g.add_node(
        operator=Operator(
            "Read", 
            formatName="IceyeProduct", 
            file=item.get_assets()['metadata'].get_absolute_href()
        ), 
        node_id="read"
    )

    g.add_node(
        operator=Operator("Calibration", selectedPolarisations="VV", outputImageScaleInDb='true', outputSigmaBand='true'),
        node_id="calibration",
        source="read",
    )

    g.add_node(
        operator=Operator(
            "Terrain-Correction", 
            pixelSpacingInMeter="2.5", 
            demName="SRTM 1Sec HGT"
        ),
        node_id="terrain-correction",
        source="calibration",
    )

    g.add_node(
        operator=Operator("Write", file=temp_calibrated_product, formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="terrain-correction",
    )

    g.run()

    rescale(temp_calibrated_product, calibrated_product)

    return calibrated_product