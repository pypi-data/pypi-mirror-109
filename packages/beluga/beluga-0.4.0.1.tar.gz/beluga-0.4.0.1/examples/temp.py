
import copy
import pytest
import numpy as np

from sympy import Symbol

from beluga import Problem
from beluga.symbolic.data_classes.mapping_functions import *
from beluga.symbolic.differential_geometry import *
from beluga.numeric.data_classes import Trajectory

from beluga.numeric.data_classes import *

from beluga.numeric.bvp_solvers import SPBVP
import numpy as np
from scipy.special import erf

from sympy import Symbol

basis = [Symbol('x'), Symbol('y')]

f = basis[0]**2 + basis[1]**2
df = exterior_derivative(f, basis)

assert df[0] == 2*basis[0]
assert df[1] == 2*basis[1]

print(df)
print(type(df))

ddf = exterior_derivative(df, basis)

assert ddf[0, 0] == 0
assert ddf[0, 1] == 0
assert ddf[1, 0] == 0
assert ddf[1, 1] == 0

f = sympy.Array([basis[0]*basis[1], 0])
df = exterior_derivative(f, basis)

assert df[0, 0] == 0
assert df[0, 1] == -basis[0]
assert df[1, 0] == basis[0]
assert df[1, 1] == 0

