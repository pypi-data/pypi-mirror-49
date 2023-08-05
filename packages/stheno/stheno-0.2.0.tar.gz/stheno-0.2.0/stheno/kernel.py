# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
import operator

import numpy as np
import tensorflow as tf
from lab import B
from plum import Dispatcher, Self, Referentiable, convert

from stheno.function_field import (
    StretchedFunction,
    ShiftedFunction,
    SelectedFunction,
    InputTransformedFunction,
    DerivativeFunction,
    TensorProductFunction,
    stretch,
    transform,
    Function,
    ZeroFunction,
    OneFunction,
    ScaledFunction,
    ProductFunction,
    SumFunction,
    WrappedFunction,
    JoinFunction,
    shift,
    select,
    to_tensor,
    tuple_equal
)
from .field import add, mul, broadcast, get_field, Formatter, need_parens
from .input import Input, Unique
from .matrix import (
    Dense,
    LowRank,
    UniformlyDiagonal,
    Diagonal,
    One,
    Zero,
    dense,
    matrix
)
from .util import uprank

__all__ = ['Kernel',
           'OneKernel',
           'ZeroKernel',
           'ScaledKernel',
           'EQ',
           'RQ',
           'Matern12',
           'Exp',
           'Matern32',
           'Matern52',
           'Delta',
           'FixedDelta',
           'Linear',
           'DerivativeKernel',
           'DecayingKernel',
           'LogKernel']

log = logging.getLogger(__name__)

_dispatch = Dispatcher()


def expand(xs):
    """Expand a sequence to the same element repeated twice if there is only
    one element.

    Args:
        xs (sequence): Sequence to expand.

    Returns:
        object: `xs * 2` or `xs`.
    """
    return xs * 2 if len(xs) == 1 else xs


class Kernel(Function, Referentiable):
    """Kernel function.

    Kernels can be added and multiplied.
    """
    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    def __call__(self, x, y):
        """Construct the kernel matrix between all `x` and `y`.

        Args:
            x (input): First argument.
            y (input, optional): Second argument. Defaults to first
                argument.

        Returns:
            :class:`.matrix.Dense:: Kernel matrix.
        """
        raise RuntimeError('For kernel "{}", could not resolve '
                           'arguments "{}" and "{}".'.format(self, x, y))

    @_dispatch(object)
    def __call__(self, x):
        return self(x, x)

    @_dispatch(Input, Input)
    def __call__(self, x, y):
        # Both input types were not used. Unwrap.
        return self(x.get(), y.get())

    @_dispatch(Input, object)
    def __call__(self, x, y):
        # Left input type was not used. Unwrap.
        return self(x.get(), y)

    @_dispatch(object, Input)
    def __call__(self, x, y):
        # Right input type was not used. Unwrap.
        return self(x, y.get())

    @_dispatch(object, object)
    def elwise(self, x, y):
        """Construct the kernel vector `x` and `y` element-wise.

        Args:
            x (input): First argument.
            y (input, optional): Second argument. Defaults to first
                argument.

        Returns:
            tensor: Kernel vector as a rank 2 column vector.
        """
        # TODO: throw warning
        return B.expand_dims(B.diag(self(x, y)), axis=1)

    @_dispatch(object)
    def elwise(self, x):
        return self.elwise(x, x)

    @_dispatch(Input, Input)
    def elwise(self, x, y):
        # Both input types were not used. Unwrap.
        return self.elwise(x.get(), y.get())

    @_dispatch(Input, object)
    def elwise(self, x, y):
        # Left input type as not used. Unwrap.
        return self.elwise(x.get(), y)

    @_dispatch(object, Input)
    def elwise(self, x, y):
        # Right input type was not used. Unwrap.
        return self.elwise(x, y.get())

    def periodic(self, period=1):
        """Map to a periodic space.

        Args:
            period (tensor, optional): Period. Defaults to `1`.

        Returns:
            :class:`.kernel.Kernel`: Periodic version of the kernel.
        """
        return periodicise(self, period)

    def __reversed__(self):
        """Reverse the arguments of the kernel."""
        return reverse(self)

    @_dispatch(int)
    def __pow__(self, power, modulo=None):
        if power < 0:
            raise ValueError('Cannot raise to a negative power.')
        elif power == 0:
            return 1
        else:
            k = self
            for _ in range(power - 1):
                k *= self
        return k

    @property
    def stationary(self):
        """Stationarity of the kernel."""
        try:
            return self._stationary_cache
        except AttributeError:
            self._stationary_cache = self._stationary
            return self._stationary_cache

    @property
    def _stationary(self):
        return False

    @property
    def var(self):
        """Variance of the kernel."""
        raise RuntimeError('The variance of "{}" could not be determined.'
                           ''.format(self.__class__.__name__))

    @property
    def length_scale(self):
        """Approximation of the length scale of the kernel."""
        raise RuntimeError('The length scale of "{}" could not be determined.'
                           ''.format(self.__class__.__name__))

    @property
    def period(self):
        """Period of the kernel."""
        raise RuntimeError('The period of "{}" could not be determined.'
                           ''.format(self.__class__.__name__))


# Register the field.
@get_field.extend(Kernel)
def get_field(a): return Kernel


class OneKernel(Kernel, OneFunction, Referentiable):
    """Constant kernel of `1`."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y:
            return One(B.dtype(x), B.shape(uprank(x))[0])
        else:
            return One(B.dtype(x),
                       B.shape(uprank(x))[0],
                       B.shape(uprank(y))[0])

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return B.ones(B.dtype(x), B.shape(x)[0], 1)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 0

    @property
    def period(self):
        return 0


class ZeroKernel(Kernel, ZeroFunction, Referentiable):
    """Constant kernel of `0`."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y:
            return Zero(B.dtype(x), B.shape(uprank(x))[0])
        else:
            return Zero(B.dtype(x),
                        B.shape(uprank(x))[0],
                        B.shape(uprank(y))[0])

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return B.zeros(B.dtype(x), B.shape(x)[0], 1)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 0

    @property
    def length_scale(self):
        return 0

    @property
    def period(self):
        return 0


class ScaledKernel(Kernel, ScaledFunction, Referentiable):
    """Scaled kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return self._compute(self[0](x, y))

    @_dispatch(object, object)
    def elwise(self, x, y):
        return self._compute(self[0].elwise(x, y))

    def _compute(self, K):
        return B.multiply(self.scale, K)

    @property
    def _stationary(self):
        return self[0].stationary

    @property
    def var(self):
        return self.scale * self[0].var

    @property
    def length_scale(self):
        return self[0].length_scale

    @property
    def period(self):
        return self[0].period


class SumKernel(Kernel, SumFunction, Referentiable):
    """Sum of kernels."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.add(self[0](x, y), self[1](x, y))

    @_dispatch(object, object)
    def elwise(self, x, y):
        return B.add(self[0].elwise(x, y), self[1].elwise(x, y))

    @property
    def _stationary(self):
        return self[0].stationary and self[1].stationary

    @property
    def var(self):
        return self[0].var + self[1].var

    @property
    def length_scale(self):
        return (self[0].var * self[0].length_scale +
                self[1].var * self[1].length_scale) / self.var

    @property
    def period(self):
        return np.inf


class ProductKernel(Kernel, ProductFunction, Referentiable):
    """Product of two kernels."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.multiply(self[0](x, y), self[1](x, y))

    @_dispatch(object, object)
    def elwise(self, x, y):
        return B.multiply(self[0].elwise(x, y), self[1].elwise(x, y))

    @property
    def _stationary(self):
        return self[0].stationary and self[1].stationary

    @property
    def var(self):
        return self[0].var * self[1].var

    @property
    def length_scale(self):
        return B.minimum(self[0].length_scale, self[1].length_scale)

    @property
    def period(self):
        return np.inf


class StretchedKernel(Kernel, StretchedFunction, Referentiable):
    """Stretched kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return self[0](*self._compute(x, y))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self[0].elwise(*self._compute(x, y))

    def _compute(self, x, y):
        stretches1, stretches2 = expand(self.stretches)
        return B.divide(x, stretches1), B.divide(y, stretches2)

    @property
    def _stationary(self):
        if len(self.stretches) == 1:
            return self[0].stationary
        else:
            # NOTE: Can do something more clever here.
            return False

    @property
    def var(self):
        return self[0].var

    @property
    def length_scale(self):
        if len(self.stretches) == 1:
            return self[0].length_scale * self.stretches[0]
        else:
            # NOTE: Can do something more clever here.
            return Kernel.length_scale.fget(self)

    @property
    def period(self):
        if len(self.stretches) == 1:
            return self[0].period * self.stretches[0]
        else:
            # NOTE: Can do something more clever here.
            return Kernel.period.fget(self)

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and \
               tuple_equal(expand(self.stretches), expand(other.stretches))


class ShiftedKernel(Kernel, ShiftedFunction, Referentiable):
    """Shifted kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return self[0](*self._compute(x, y))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self[0].elwise(*self._compute(x, y))

    def _compute(self, x, y):
        shifts1, shifts2 = expand(self.shifts)
        return B.subtract(x, shifts1), B.subtract(y, shifts2)

    @property
    def _stationary(self):
        if len(self.shifts) == 1:
            return self[0].stationary
        else:
            # NOTE: Can do something more clever here.
            return False

    @property
    def var(self):
        return self[0].var

    @property
    def length_scale(self):
        if len(self.shifts) == 1:
            return self[0].length_scale
        else:
            # NOTE: Can do something more clever here.
            return Kernel.length_scale.fget(self)

    @property
    def period(self):
        return self[0].period

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and \
               tuple_equal(expand(self.shifts), expand(other.shifts))


class SelectedKernel(Kernel, SelectedFunction, Referentiable):
    """Kernel with particular input dimensions selected."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return self[0](*self._compute(x, y))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self[0].elwise(*self._compute(x, y))

    def _compute(self, x, y):
        dims1, dims2 = expand(self.dims)
        x = x if dims1 is None else B.take(x, dims1, axis=1)
        y = y if dims2 is None else B.take(y, dims2, axis=1)
        return x, y

    @property
    def _stationary(self):
        if len(self.dims) == 1:
            return self[0].stationary
        else:
            # NOTE: Can do something more clever here.
            return False

    @property
    def var(self):
        return self[0].var

    @property
    def length_scale(self):
        length_scale = self[0].length_scale
        if B.isscalar(length_scale):
            return length_scale
        else:
            if len(self.dims) == 1:
                return B.take(length_scale, self.dims[0])
            else:
                # NOTE: Can do something more clever here.
                return Kernel.length_scale.fget(self)

    @property
    def period(self):
        period = self[0].period
        if B.isscalar(period):
            return period
        else:
            if len(self.dims) == 1:
                return B.take(period, self.dims[0])
            else:
                # NOTE: Can do something more clever here.
                return Kernel.period.fget(self)

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and \
               tuple_equal(expand(self.dims), expand(other.dims))


class InputTransformedKernel(Kernel, InputTransformedFunction, Referentiable):
    """Input-transformed kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    @uprank
    def __call__(self, x, y):
        return self[0](*self._compute(x, y))

    @_dispatch(object, object)
    @uprank
    def elwise(self, x, y):
        return self[0].elwise(*self._compute(x, y))

    def _compute(self, x, y):
        f1, f2 = expand(self.fs)
        x = x if f1 is None else uprank(f1(x))
        y = y if f2 is None else uprank(f2(y))
        return x, y

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and \
               tuple_equal(expand(self.fs), expand(other.fs))


class PeriodicKernel(Kernel, WrappedFunction, Referentiable):
    """Periodic kernel.

    Args:
        k (:class:`.kernel.Kernel`): Kernel to make periodic.
        scale (tensor): Period.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, k, period):
        WrappedFunction.__init__(self, k)
        self._period = to_tensor(period)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return self[0](*self._compute(x, y))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self[0].elwise(*self._compute(x, y))

    def _compute(self, x, y):
        def feat_map(z):
            z = B.divide(B.multiply(B.multiply(z, 2), B.pi), self.period)
            return B.concat(B.sin(z), B.cos(z), axis=1)

        return feat_map(x), feat_map(y)

    @property
    def _stationary(self):
        return self[0].stationary

    @property
    def var(self):
        return self[0].var

    @property
    def length_scale(self):
        return self[0].length_scale

    @property
    def period(self):
        return self._period

    @_dispatch(object, Formatter)
    def display(self, e, formatter):
        return '{} per {}'.format(e, formatter(self._period))

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and B.all(self.period == other.period)


class EQ(Kernel, Referentiable):
    """Exponentiated quadratic kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return Dense(self._compute(B.pw_dists2(x, y)))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self._compute(B.ew_dists2(x, y))

    def _compute(self, dists2):
        return B.exp(-0.5 * dists2)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 1

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


class RQ(Kernel, Referentiable):
    """Rational quadratic kernel.

    Args:
        alpha (scalar): Shape of the prior over length scales. Determines the
            weight of the tails of the kernel. Must be positive.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, alpha):
        self.alpha = alpha

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return Dense(self._compute(B.pw_dists2(x, y)))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self._compute(B.ew_dists2(x, y))

    def _compute(self, dists2):
        return (1 + .5 * dists2 / self.alpha) ** (-self.alpha)

    @_dispatch(Formatter)
    def display(self, formatter):
        return 'RQ({})'.format(formatter(self.alpha))

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 1

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return B.all(self.alpha == other.alpha)


class Exp(Kernel, Referentiable):
    """Exponential kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return Dense(B.exp(-B.pw_dists(x, y)))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return B.exp(-B.ew_dists(x, y))

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 1

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


Matern12 = Exp  #: Alias for the exponential kernel.


class Matern32(Kernel, Referentiable):
    """Matern--3/2 kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return Dense(self._compute(B.pw_dists(x, y)))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self._compute(B.ew_dists(x, y))

    def _compute(self, dists):
        r = 3 ** .5 * dists
        return (1 + r) * B.exp(-r)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 1

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


class Matern52(Kernel, Referentiable):
    """Matern--5/2 kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return Dense(self._compute(B.pw_dists(x, y)))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return self._compute(B.ew_dists(x, y))

    def _compute(self, dists):
        r1 = 5 ** .5 * dists
        r2 = 5 * dists ** 2 / 3
        return (1 + r1 + r2) * B.exp(-r1)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 1

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


class Delta(Kernel, Referentiable):
    """Kronecker delta kernel.

    Args:
        epsilon (float, optional): Tolerance for equality in squared distance.
            Defaults to `1e-10`.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, epsilon=1e-10):
        self.epsilon = epsilon

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y:
            return self._eye(uprank(x))
        else:
            return Dense(self._compute(B.pw_dists2(uprank(x), uprank(y))))

    @_dispatch(Unique, Unique)
    def __call__(self, x, y):
        x, y = x.get(), y.get()
        if x is y:
            return self._eye(uprank(x))
        else:
            x, y = uprank(x), uprank(y)
            return Zero(B.dtype(x), B.shape(x)[0], B.shape(y)[0])

    @_dispatch(Unique, object)
    def __call__(self, x, y):
        x, y = uprank(x.get()), uprank(y)
        return Zero(B.dtype(x), B.shape(x)[0], B.shape(y)[0])

    @_dispatch(object, Unique)
    def __call__(self, x, y):
        x, y = uprank(x), uprank(y.get())
        return Zero(B.dtype(x), B.shape(x)[0], B.shape(y)[0])

    @_dispatch(Unique, Unique)
    def elwise(self, x, y):
        x, y = x.get(), y.get()
        if x is y:
            return One(B.dtype(x), B.shape(uprank(x))[0], 1)
        else:
            return Zero(B.dtype(x), B.shape(uprank(x))[0], 1)

    @_dispatch(Unique, object)
    def elwise(self, x, y):
        x = x.get()
        return Zero(B.dtype(x), B.shape(uprank(x))[0], 1)

    @_dispatch(object, Unique)
    def elwise(self, x, y):
        return Zero(B.dtype(x), B.shape(uprank(x))[0], 1)

    @_dispatch(B.Numeric, B.Numeric)
    def elwise(self, x, y):
        if x is y:
            return One(B.dtype(x), B.shape(uprank(x))[0], 1)
        else:
            return self._compute(B.ew_dists2(uprank(x), uprank(y)))

    def _eye(self, x):
        return UniformlyDiagonal(B.cast(B.dtype(x), 1), B.shape(x)[0])

    def _compute(self, dists2):
        dtype = B.dtype(dists2)
        return B.cast(dtype, B.lt(dists2, B.cast(dtype, self.epsilon)))

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 0

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return self.epsilon == other.epsilon


class FixedDelta(Kernel, Referentiable):
    """Kronecker delta kernel that produces a diagonal matrix with given
    noises if and only if the inputs are identical and of the right shape.

    Args:
        noises (vector): Noises.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, noises):
        self.noises = noises

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y and B.shape(uprank(x))[0] == B.shape(self.noises)[0]:
            return Diagonal(self.noises)
        else:
            x, y = uprank(x), uprank(y)
            return Zero(B.dtype(x), B.shape(x)[0], B.shape(y)[0])

    @_dispatch(B.Numeric, B.Numeric)
    def elwise(self, x, y):
        if x is y and B.shape(B.uprank(x))[0] == B.shape(self.noises)[0]:
            return B.uprank(self.noises)
        else:
            x = B.uprank(x)
            return Zero(B.dtype(x), B.shape(x)[0], 1)

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return 0

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return B.all(self.noises == other.noises)


class Linear(Kernel, Referentiable):
    """Linear kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        if x is y:
            return LowRank(uprank(x))
        else:
            return LowRank(left=uprank(x),
                           right=uprank(y))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return B.expand_dims(B.sum(B.multiply(x, y), axis=1), axis=1)

    @property
    def _stationary(self):
        return False

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


class DecayingKernel(Kernel, Referentiable):
    """Decaying kernel.

    Args:
        alpha (tensor): Shape of the gamma distribution governing the
            distribution of decaying exponentials.
        beta (tensor): Rate of the gamma distribution governing the
            distribution of decaying exponentials.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        return B.divide(self._compute_beta_raised(),
                        B.power(B.pw_sums(B.add(x, self.beta), y), self.alpha))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        return B.divide(self._compute_beta_raised(),
                        B.power(B.ew_sums(B.add(x, self.beta), y), self.alpha))

    def _compute_beta_raised(self):
        beta_norm = B.sqrt(B.maximum(B.sum(B.power(self.beta, 2)),
                                     B.cast(B.dtype(self.beta), 1e-30)))
        return B.power(beta_norm, self.alpha)

    @_dispatch(Formatter)
    def display(self, formatter):
        return 'DecayingKernel({}, {})'.format(formatter(self.alpha),
                                               formatter(self.beta))

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return B.all(self.alpha == other.alpha) and \
               B.all(self.beta == other.beta)


class LogKernel(Kernel, Referentiable):
    """Logarithm kernel."""

    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        dists = B.maximum(B.pw_dists(x, y), 1e-10)
        return B.divide(B.log(dists + 1), dists)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        dists = B.maximum(B.ew_dists(x, y), 1e-10)
        return B.divide(B.log(dists + 1), dists)

    @_dispatch(Formatter)
    def display(self, formatter):
        return 'LogKernel()'

    @property
    def _stationary(self):
        return True

    @property
    def var(self):
        return 1

    @property
    def length_scale(self):
        return np.inf

    @property
    def period(self):
        return np.inf

    @_dispatch(Self)
    def __eq__(self, other):
        return True


class PosteriorKernel(Kernel, Referentiable):
    """Posterior kernel.

    Args:
        k_ij (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the left input and the right input respectively.
        k_zi (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the data and the left input respectively.
        k_zj (:class:`.kernel.Kernel`): Kernel between processes
            corresponding to the data and the right input respectively.
        z (input): Locations of data.
        K_z (:class:`.matrix.Dense`): Kernel matrix of data.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, k_ij, k_zi, k_zj, z, K_z):
        self.k_ij = k_ij
        self.k_zi = k_zi
        self.k_zj = k_zj
        self.z = z
        self.K_z = matrix(K_z)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.schur(self.k_ij(x, y),
                       self.k_zi(self.z, x),
                       self.K_z,
                       self.k_zj(self.z, y))

    @_dispatch(object, object)
    def elwise(self, x, y):
        qf_diag = B.qf_diag(self.K_z,
                            self.k_zi(self.z, x),
                            self.k_zj(self.z, y))
        return B.subtract(self.k_ij.elwise(x, y),
                          B.expand_dims(qf_diag, axis=1))


class CorrectiveKernel(Kernel, Referentiable):
    """Kernel that adds the corrective variance in sparse conditioning.

    Args:
        k_zi (:class:`.kernel.Kernel`): Kernel between the processes
            corresponding to the left input and the inducing points
            respectively.
        k_zj (:class:`.kernel.Kernel`): Kernel between the processes
            corresponding to the right input and the inducing points
            respectively.
        z (input): Locations of the inducing points.
        A (tensor): Corrective matrix.
        L (tensor): Kernel matrix of the inducing points.
    """
    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, k_zi, k_zj, z, A, K_z):
        self.k_zi = k_zi
        self.k_zj = k_zj
        self.z = z
        self.A = A
        self.L = B.cholesky(matrix(K_z))

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.qf(self.A,
                    B.trisolve(self.L, self.k_zi(self.z, x)),
                    B.trisolve(self.L, self.k_zj(self.z, y)))

    @_dispatch(object, object)
    def elwise(self, x, y):
        return B.qf_diag(self.A,
                         B.trisolve(self.L, self.k_zi(self.z, x)),
                         B.trisolve(self.L, self.k_zj(self.z, y)))[:, None]


def dkx(k_elwise, i):
    """Construct the derivative of a kernel with respect to its first
    argument.

    Args:
        k_elwise (function): Function that performs element-wise computation
            of the kernel.
        i (int): Dimension with respect to which to compute the derivative.

    Returns:
        function: Derivative of the kernel with respect to its first argument.
    """

    def _dkx(x, y):
        with tf.GradientTape() as t:
            # Get the numbers of inputs.
            nx = B.shape(x)[0]
            ny = B.shape(y)[0]

            # Copy the input `ny` times to efficiently compute many derivatives.
            xis = tf.identity_n([x[:, i:i + 1]] * ny)
            t.watch(xis)

            # Tile inputs for batched computation.
            x = B.tile(x, ny, 1)
            y = B.reshape(B.tile(y, 1, nx), ny * nx, -1)

            # Insert tracked dimension, which is different for every tile.
            xi = B.concat(*xis, axis=0)
            x = B.concat(x[:, :i], xi, x[:, i + 1:], axis=1)

            # Perform the derivative computation.
            out = dense(k_elwise(x, y))
            grads = t.gradient(out, xis, unconnected_gradients='zero')
            return B.concat(*grads, axis=1)

    return _dkx


def dkx_elwise(k_elwise, i):
    """Construct the element-wise derivative of a kernel with respect to
    its first argument.

    Args:
        k_elwise (function): Function that performs element-wise computation
            of the kernel.
        i (int): Dimension with respect to which to compute the derivative.

    Returns:
        function: Element-wise derivative of the kernel with respect to its
            first argument.
    """

    def _dkx_elwise(x, y):
        with tf.GradientTape() as t:
            xi = x[:, i:i + 1]
            t.watch(xi)
            x = B.concat(x[:, :i], xi, x[:, i + 1:], axis=1)
            out = dense(k_elwise(x, y))
            return t.gradient(out, xi, unconnected_gradients='zero')

    return _dkx_elwise


def dky(k_elwise, i):
    """Construct the derivative of a kernel with respect to its second
    argument.

    Args:
        k_elwise (function): Function that performs element-wise computation
            of the kernel.
        i (int): Dimension with respect to which to compute the derivative.

    Returns:
        function: Derivative of the kernel with respect to its second argument.
    """

    def _dky(x, y):
        with tf.GradientTape() as t:
            # Get the numbers of inputs.
            nx = B.shape(x)[0]
            ny = B.shape(y)[0]

            # Copy the input `nx` times to efficiently compute many derivatives.
            yis = tf.identity_n([y[:, i:i + 1]] * nx)
            t.watch(yis)

            # Tile inputs for batched computation.
            x = B.reshape(B.tile(x, 1, ny), nx * ny, -1)
            y = B.tile(y, nx, 1)

            # Insert tracked dimension, which is different for every tile.
            yi = B.concat(*yis, axis=0)
            y = B.concat(y[:, :i], yi, y[:, i + 1:], axis=1)

            # Perform the derivative computation.
            out = dense(k_elwise(x, y))
            grads = t.gradient(out, yis, unconnected_gradients='zero')
            return B.transpose(B.concat(*grads, axis=1))

    return _dky


def dky_elwise(k_elwise, i):
    """Construct the element-wise derivative of a kernel with respect to
    its second argument.

    Args:
        k_elwise (function): Function that performs element-wise computation
            of the kernel.
        i (int): Dimension with respect to which to compute the derivative.

    Returns:
        function: Element-wise derivative of the kernel with respect to its
            second argument.
    """

    def _dky_elwise(x, y):
        with tf.GradientTape() as t:
            yi = y[:, i:i + 1]
            t.watch(yi)
            y = B.concat(y[:, :i], yi, y[:, i + 1:], axis=1)
            out = dense(k_elwise(x, y))
            return t.gradient(out, yi, unconnected_gradients='zero')

    return _dky_elwise


def perturb(x):
    """Slightly perturb a tensor.

    Args:
        x (tensor): Tensor to perturb.

    Returns:
        tensor: `x`, but perturbed.
    """
    dtype = convert(B.dtype(x), B.NPDType)
    if dtype == np.float64:
        return 1e-20 + x * (1 + 1e-14)
    elif dtype == np.float32:
        return 1e-20 + x * (1 + 1e-7)
    else:
        raise ValueError('Cannot perturb a tensor of data type {}.'
                         ''.format(B.dtype(x)))


class DerivativeKernel(Kernel, DerivativeFunction, Referentiable):
    """Derivative of kernel."""
    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def __call__(self, x, y):
        i, j = expand(self.derivs)
        k = self[0]

        # Prevent that `x` equals `y` to stabilise nested gradients.
        y = perturb(y)

        if i is not None and j is not None:
            # Derivative with respect to both `x` and `y`.
            return Dense(dky(dkx_elwise(k.elwise, i), j)(x, y))

        elif i is not None and j is None:
            # Derivative with respect to `x`.
            return Dense(dkx(k.elwise, i)(x, y))

        elif i is None and j is not None:
            # Derivative with respect to `y`.
            return Dense(dky(k.elwise, j)(x, y))

        else:
            raise RuntimeError('No derivative specified.')

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        i, j = expand(self.derivs)
        k = self[0]

        # Prevent that `x` equals `y` to stabilise nested gradients.
        y = perturb(y)

        if i is not None and j is not None:
            # Derivative with respect to both `x` and `y`.
            return dky_elwise(dkx_elwise(k.elwise, i), j)(x, y)

        elif i is not None and j is None:
            # Derivative with respect to `x`.
            return dkx_elwise(k.elwise, i)(x, y)

        elif i is None and j is not None:
            # Derivative with respect to `y`.
            return dky_elwise(k.elwise, j)(x, y)

        else:
            raise RuntimeError('No derivative specified.')

    @property
    def _stationary(self):
        # NOTE: In the one-dimensional case, if derivatives with respect to both
        #     arguments are taken, then the result is in fact stationary.
        return False

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0] and \
               tuple_equal(expand(self.derivs), expand(other.derivs))


class TensorProductKernel(Kernel, TensorProductFunction, Referentiable):
    """Tensor product kernel."""
    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(B.Numeric, B.Numeric)
    def __call__(self, x, y):
        f1, f2 = expand(self.fs)
        if x is y and f1 is f2:
            return LowRank(uprank(f1(uprank(x))))
        else:
            return LowRank(left=uprank(f1(uprank(x))),
                           right=uprank(f2(uprank(y))))

    @_dispatch(B.Numeric, B.Numeric)
    @uprank
    def elwise(self, x, y):
        f1, f2 = expand(self.fs)
        return B.multiply(uprank(f1(x)), uprank(f2(y)))

    @_dispatch(Self)
    def __eq__(self, other):
        return tuple_equal(expand(self.fs), expand(other.fs))


class ReversedKernel(Kernel, WrappedFunction, Referentiable):
    """Reversed kernel.

    Evaluates with its arguments reversed.
    """
    _dispatch = Dispatcher(in_class=Self)

    @_dispatch(object, object)
    def __call__(self, x, y):
        return B.transpose(self[0](y, x))

    @_dispatch(object, object)
    def elwise(self, x, y):
        return self[0].elwise(y, x)

    @property
    def _stationary(self):
        return self[0].stationary

    @property
    def var(self):
        return self[0].var

    @property
    def length_scale(self):
        return self[0].length_scale

    @property
    def period(self):
        return self[0].period

    @_dispatch(object, Formatter)
    def display(self, e, formatter):
        return 'Reversed({})'.format(e)

    @_dispatch(Self)
    def __eq__(self, other):
        return self[0] == other[0]


@need_parens.extend_multi((Function, ReversedKernel),
                          ({WrappedFunction, JoinFunction}, ReversedKernel))
def need_parens(el, parent): return False


@need_parens.extend(ReversedKernel, ProductFunction)
def need_parens(el, parent): return False


# Periodicise kernels.

@_dispatch(Kernel, object)
def periodicise(a, b): return PeriodicKernel(a, b)


@_dispatch(ZeroKernel, object)
def periodicise(a, b): return a


# Reverse kernels.

@_dispatch(Kernel)
def reverse(a): return a if a.stationary else ReversedKernel(a)


@_dispatch(ReversedKernel)
def reverse(a): return a[0]


@_dispatch.multi((ZeroKernel,), (OneKernel,))
def reverse(a): return a


@_dispatch(ShiftedKernel)
def reverse(a): return shift(reversed(a[0]), *reversed(a.shifts))


@_dispatch(StretchedKernel)
def reverse(a): return stretch(reversed(a[0]), *reversed(a.stretches))


@_dispatch(InputTransformedKernel)
def reverse(a): return transform(reversed(a[0]), *reversed(a.fs))


@_dispatch(SelectedKernel)
def reverse(a): return select(reversed(a[0]), *reversed(a.dims))


# Propagate reversal.

@_dispatch(SumKernel)
def reverse(a): return add(reverse(a[0]), reverse(a[1]))


@_dispatch(ProductKernel)
def reverse(a): return mul(reverse(a[0]), reverse(a[1]))


@_dispatch(ScaledKernel)
def reverse(a): return mul(a.scale, reversed(a[0]))


# Make shifting synergise with reversal.

@shift.extend(Kernel, [object])
def shift(a, *shifts):
    if a.stationary and len(shifts) == 1:
        return a
    else:
        return ShiftedKernel(a, *shifts)


@shift.extend(ZeroKernel, [object])
def shift(a, *shifts): return a


@shift.extend(ShiftedKernel, [object])
def shift(a, *shifts):
    return shift(a[0], *broadcast(operator.add, a.shifts, shifts))
