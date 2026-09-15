"""Strict real/finite interface to the preserved parity reference implementation.

This module changes input validation, not the estimator. Import the maintained
API here; research/parity_frames/core.py is an immutable historical fixture.
Zero-imaginary complex arrays are also rejected. No implicit normalization or
projection of invalid inputs is performed. Dense routines remain diagnostics.
"""
from __future__ import annotations
import hashlib
import importlib.util
import math
from numbers import Integral, Real
from pathlib import Path
import numpy as np

_SOURCE = Path(__file__).resolve().parents[1] / 'research/parity_frames/core.py'
_SHA = '168d7022dde985ae9373c08cc4dcbce9c2445c24f4fffd875d8366567b86f1f7'
if hashlib.sha256(_SOURCE.read_bytes()).hexdigest() != _SHA:
    raise RuntimeError('Immutable parity reference hash mismatch')
_spec = importlib.util.spec_from_file_location('_qbp_parity_reference', _SOURCE)
_ref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ref)


def _integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise ValueError(f'{name} must be an integer, not a coerced value')
    if value < minimum:
        raise ValueError(f'{name} must be >= {minimum}')
    return int(value)


def _scalar(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f'{name} must be real')
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f'{name} must be finite')
    return value


def _real(value, name, ndim=None):
    try:
        raw = np.asarray(value)
        if raw.dtype.kind not in 'iuf' or np.iscomplexobj(raw):
            raise ValueError(f'{name} must contain real numeric values')
        if ndim is not None and raw.ndim != ndim:
            raise ValueError(f'{name} must have {ndim} dimensions')
        if not np.all(np.isfinite(raw)):
            raise ValueError(f'{name} must be finite')
        with np.errstate(over='raise', invalid='raise'):
            out = np.array(raw, dtype=np.float64, copy=True)
        if not np.all(np.isfinite(out)):
            raise ValueError(f'{name} is outside float64 range')
        return out
    except (TypeError, OverflowError, FloatingPointError) as exc:
        raise ValueError(f'Invalid {name}') from exc


def _power_two(length, minimum=2):
    if length < minimum or length & (length - 1):
        raise ValueError(f'Power-of-two length >= {minimum} required')


def _tangents(T):
    T = _real(T, 'T', 2)
    _power_two(T.shape[0])
    if T.shape[1] == 0:
        raise ValueError('At least one tangent column required')
    if math.hypot(*T[0]) > 1e-10:
        raise ValueError('Reference-orthogonal tangents required')
    return T


def validate_inputs(T, q):
    T = _tangents(T)
    q = _real(q, 'q', 1)
    if q.shape != (T.shape[0],):
        raise ValueError('Response shape mismatch')
    if abs(math.hypot(*q) - 1.0) > 1e-10:
        raise ValueError('Unit response required; normalization is not automatic')
    return T, q


def _checked(function, *args):
    try:
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            result = function(*args)
        values = result if isinstance(result, tuple) else (result,)
        if any(not np.all(np.isfinite(x)) for x in values):
            raise ValueError('Nonfinite numerical output')
        return result
    except (FloatingPointError, OverflowError) as exc:
        raise ValueError('Input exceeds safe numerical range') from exc


def fwht(array):
    array = _real(array, 'array')
    if array.ndim == 0:
        raise ValueError('An array axis is required')
    _power_two(array.shape[-1], 1)
    return _checked(_ref.fwht, array)


def measurement_moments(T, q, phase=None):
    T, q = validate_inputs(T, q)
    if phase is not None:
        phase = _real(phase, 'phase', 1)
        if (phase.shape != q.shape or phase[0] != 1 or
                not np.all((phase == 1) | (phase == -1))):
            raise ValueError('Exact +/-1 phase vector fixing address zero required')
    return _checked(_ref.measurement_moments, T, q, phase)


def full_quadratic_covariance(T, q):
    T, q = validate_inputs(T, q)
    return _checked(_ref.full_quadratic_covariance, T, q)


def interpolated_covariance(T, q, rounds):
    T, q = validate_inputs(T, q)
    rounds = _integer(rounds, 'rounds')
    return _checked(_ref.interpolated_covariance, T, q, rounds)


def covariance_risk_matrix(T, rounds):
    return _checked(_ref.covariance_risk_matrix, _tangents(T), _integer(rounds, 'rounds'))


def imbalance(T):
    return _checked(_ref.imbalance, _tangents(T))


def risk_bound(T, rounds):
    return _checked(_ref.risk_bound, _tangents(T), _integer(rounds, 'rounds'))


def rounds_for_relative_bound(beta, eta):
    beta, eta = _scalar(beta, 'beta'), _scalar(eta, 'eta')
    if beta < 1 or eta <= 0:
        raise ValueError('beta >= 1 and eta > 0 required')
    if beta == 1:
        return 0
    # Use logarithms to avoid overflow in (beta-1)/(2*eta).
    return max(0, math.ceil((math.log(beta - 1) - math.log(2) - math.log(eta))/math.log(4)))


def _pairs(n, pairs):
    n = _integer(n, 'n', 1)
    out = []
    try:
        for item in pairs:
            if len(item) != 2:
                raise ValueError('Each parity pair needs two masks')
            a, b = (_integer(v, 'mask') for v in item)
            if max(a, b) >= 1 << n:
                raise ValueError('Mask outside register')
            out.append((a, b))
    except TypeError as exc:
        raise ValueError('Invalid parity-pair sequence') from exc
    return n, out


def parity_phase(n, pairs):
    n, pairs = _pairs(n, pairs)
    return _checked(_ref.parity_phase, n, pairs)


def quadratic_phase(n, mask):
    n, mask = _integer(n, 'n', 1), _integer(mask, 'mask')
    if mask >= 1 << (n*(n-1)//2):
        raise ValueError('Quadratic mask outside register')
    return _checked(_ref.quadratic_phase, n, mask)


def local_shift_score(table, y, pairs):
    table = _real(table, 'table', 1)
    _power_two(len(table))
    n, pairs = _pairs((len(table)-1).bit_length(), pairs)
    y = _integer(y, 'y')
    if y >= len(table):
        raise ValueError('Outcome outside local register')
    return _checked(_ref.local_shift_score, table, y, pairs)


def local_direct_score(tau, y, pairs):
    tau = _real(tau, 'tau', 1)
    _power_two(len(tau))
    n, pairs = _pairs((len(tau)-1).bit_length(), pairs)
    y = _integer(y, 'y')
    if y >= len(tau):
        raise ValueError('Outcome outside local register')
    return _checked(_ref.local_direct_score, tau, y, pairs)


__all__ = ['validate_inputs', 'fwht', 'measurement_moments',
           'full_quadratic_covariance', 'interpolated_covariance',
           'covariance_risk_matrix', 'imbalance', 'risk_bound',
           'rounds_for_relative_bound', 'parity_phase', 'quadratic_phase',
           'local_shift_score', 'local_direct_score']
