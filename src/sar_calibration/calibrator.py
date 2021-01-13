import pystac
from . import sentinel 
from . import kompsat 
from . import iceye


class Calibrator(object):

    def calibrate(self, item, **kwargs):
    
        calibrator = get_calibrator(item)
    
        return calibrator(item, **kwargs)


def get_calibrator(item):

    mission = item.properties['mission']

    calibrators = dict()

    calibrators['sentinel-1'] = _calibrate_sentinel
    calibrators['kompsat5'] = _calibrate_kompsat
    calibrators['iceye'] = _calibrate_iceye

    calibrator = calibrators.get(mission)

    if calibrator is not None:

        return calibrator

    else:

        raise ValueError(mission)


def _calibrate_sentinel(item, **kwargs):

    return sentinel.calibrate(item, **kwargs)

def _calibrate_kompsat(item, **kwargs):

    return kompsat.calibrate(item, **kwargs)

def _calibrate_iceye(item, **kwargs):

    return iceye.calibrate(item, **kwargs)