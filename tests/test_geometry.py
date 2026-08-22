import numpy as np
import pytest

from eddy_current_engine import Disk, GeometryParameters, analyze_geometry


def test_reference_geometry_regression():
    analysis = analyze_geometry(resolution=256)
    measured = analysis.measurements

    assert measured["triple"].area == pytest.approx(0.0026566298273148223, rel=1e-5)
    assert measured["disk_2_disk_3_only"].area == pytest.approx(6.62589063189413e-05, rel=1e-5)
    assert measured["disk_1_disk_2_only"].area == pytest.approx(0.0008429971011798002, rel=1e-5)
    assert measured["triple"].centroid == pytest.approx(
        (0.006890967853044326, -0.00824607030895322), abs=2e-7
    )


def test_regions_are_disjoint_and_inside_disks():
    analysis = analyze_geometry(resolution=64)
    regions = analysis.regions
    assert regions["triple"].intersection(regions["disk_1_disk_2_only"]).area < 1e-14
    assert all(np.isfinite(item.radial_width) and item.radial_width > 0 for item in analysis.measurements.values())


def test_invalid_parameters_are_rejected():
    with pytest.raises(ValueError):
        Disk((0.0, 0.0), 0.0)
    with pytest.raises(ValueError):
        GeometryParameters(origin_disk=4)
