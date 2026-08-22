"""Geometric analysis of the three overlapping disks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from shapely.geometry import GeometryCollection, LineString, MultiLineString, Point

from .parameters import Disk, GeometryParameters


@dataclass(frozen=True)
class RegionMeasurement:
    name: str
    area: float
    centroid: tuple[float, float]
    radial_width: float
    edge_points: tuple[tuple[float, float], tuple[float, float]]


@dataclass(frozen=True)
class GeometryAnalysis:
    disks: tuple[object, object, object]
    regions: dict[str, object]
    measurements: dict[str, RegionMeasurement]


def make_disk(disk: Disk, resolution: int = 256):
    """Return a polygonal approximation to a disk."""

    if resolution < 16:
        raise ValueError("resolution must be at least 16")
    return Point(*disk.center).buffer(disk.radius, quad_segs=resolution)


def overlap_regions(disks: tuple[object, object, object]) -> dict[str, object]:
    """Return the triple overlap and the two pair-only regions used in the model."""

    disk_1, disk_2, disk_3 = disks
    triple = disk_1.intersection(disk_2).intersection(disk_3)
    return {
        "triple": triple,
        "disk_2_disk_3_only": disk_2.intersection(disk_3).difference(triple),
        "disk_1_disk_2_only": disk_1.intersection(disk_2).difference(triple),
    }


def _line_segments(geometry: object) -> list[LineString]:
    if isinstance(geometry, LineString):
        return [geometry]
    if isinstance(geometry, MultiLineString):
        return list(geometry.geoms)
    if isinstance(geometry, GeometryCollection):
        return [item for item in geometry.geoms if isinstance(item, LineString)]
    return []


def radial_width(
    region: object,
    origin: tuple[float, float],
    centroid: tuple[float, float],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """Measure the edge-to-edge width on the line through origin and centroid."""

    origin_array = np.asarray(origin, dtype=float)
    centroid_array = np.asarray(centroid, dtype=float)
    direction = centroid_array - origin_array
    norm = np.linalg.norm(direction)
    if region.is_empty or norm <= 1e-14:
        return np.nan, ((np.nan, np.nan), (np.nan, np.nan))

    unit = direction / norm
    min_x, min_y, max_x, max_y = region.bounds
    span = max(np.hypot(max_x - min_x, max_y - min_y), 1.0) * 4.0
    line = LineString([origin_array - span * unit, origin_array + span * unit])
    segments = _line_segments(region.intersection(line))
    if not segments:
        return np.nan, ((np.nan, np.nan), (np.nan, np.nan))

    centroid_point = Point(*centroid)
    segment = min(segments, key=lambda item: item.distance(centroid_point))
    first = tuple(map(float, segment.coords[0]))
    last = tuple(map(float, segment.coords[-1]))
    return float(Point(first).distance(Point(last))), (first, last)


def analyze_geometry(
    parameters: GeometryParameters | None = None,
    resolution: int = 256,
) -> GeometryAnalysis:
    """Compute areas, centroids, and radial widths for the reference geometry."""

    parameters = parameters or GeometryParameters()
    disk_parameters = parameters.disks()
    disks = tuple(make_disk(item, resolution=resolution) for item in disk_parameters)
    regions = overlap_regions(disks)
    origin = disk_parameters[parameters.origin_disk - 1].center

    measurements: dict[str, RegionMeasurement] = {}
    for name, region in regions.items():
        if region.is_empty:
            centroid = (np.nan, np.nan)
            area = np.nan
            width = np.nan
            edges = ((np.nan, np.nan), (np.nan, np.nan))
        else:
            area = float(region.area)
            centroid = (float(region.centroid.x), float(region.centroid.y))
            width, edges = radial_width(region, origin, centroid)
        measurements[name] = RegionMeasurement(name, area, centroid, width, edges)

    return GeometryAnalysis(disks, regions, measurements)
