from __future__ import annotations

from math import sin, cos, asin, acos, hypot
from numpy import asarray

from typing import Sequence
from typing_extensions import Annotated
from nptyping import NDArray

Vec = Annotated[Sequence[float], 3]
NpVec = NDArray[(3,), float]


__all__ = [
    'arc_sin',
    'arc_cos',
    'euclidean_distance',
    'planar_rotation',
    'is_isotropic',
    'transform_stress',
    'transform_stress_angle',
    'stress_vec_to_tensor',
    'stress_tensor_to_vec'
]


s, c = sin, cos


def s2(angle: float) -> float:
    """Calculate sine squared of angle in radians."""
    return s(angle) ** 2


def c2(angle: float) -> float:
    """Calculate cosine squared of angle in radians."""
    return c(angle) ** 2


def arc_sin(num: float) -> float:
    """Calculate inverse sine. Input values are bounded
    between -.9999 and .9999 for numerical stability."""
    return asin(max(min(num, .9999), -.9999))


def arc_cos(num: float) -> float:
    """Calculate inverse cosine. Input values are bounded
    between -.9999 and .9999 for numerical stability."""
    return acos(max(min(num, .9999), -.9999))


def euclidean_distance(pt_a: Vec, pt_b: Vec) -> float:
    """Calculate distance between two 3D points using the hypotenuse."""
    return hypot(pt_a[0] - pt_b[0], pt_a[1] - pt_b[1], pt_a[2] - pt_b[2])


def planar_rotation(angle: float) -> NDArray[(2, 2), float]:
    """Get the planar rotation matrix from an angle in radians."""
    return asarray([[c(angle),  -s(angle)],
                    [s(angle),   c(angle)]])


def is_isotropic(vec: NpVec) -> bool:
    """Check whether a planar stress pseudo-vector is isotropic."""
    return (vec[0] == vec[1]) and (vec[2] == 0)


def transform_stress(stress: NpVec, rotation: NDArray[(2, 2), float],
                     invert: bool = False) -> NpVec:
    """Transform a planar stress pseudo-vector by a 2x2 rotation matrix.
    Internally, the stress pseudo-vector is converted to a 2x2 tensor."""
    s = stress_vec_to_tensor(stress)
    R = rotation
    r = (R.dot(s).dot(R.T) if invert
         else R.T.dot(s).dot(R))
    return stress_tensor_to_vec(r)


def transform_stress_angle(stress: NpVec, angle: float, invert: bool = False) -> NpVec:
    """Transform a planar stress pseudo-vector by an angle in radians."""
    a = -angle if invert else angle
    s2a = s2(a)
    c2a = c2(a)
    sca = s(a) * c(a)
    T = [[c2a,    s2a,     2 * sca],
         [s2a,    c2a,    -2 * sca],
         [-sca,   sca,   c2a - s2a]]
    return asarray(T).dot(stress)


def stress_vec_to_tensor(vec: NpVec) -> NDArray[(2, 2), float]:
    """Convert planar stresses from pseudo-vector to tensor form."""
    return asarray([[vec[0], vec[2]],
                    [vec[2], vec[1]]])


def stress_tensor_to_vec(tens: NDArray[(2, 2), float]) -> NpVec:
    """Convert planar stresses from tensor to pseudo-vector form."""
    return asarray([tens[0, 0], tens[1, 1], tens[0, 1]])