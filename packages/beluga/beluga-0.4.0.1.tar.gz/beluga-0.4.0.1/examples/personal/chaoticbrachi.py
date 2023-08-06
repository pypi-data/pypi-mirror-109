"""Brachistochrone example."""
import beluga
import enum
import copy
import logging
from math import pi

from beluga.symbolic.data_classes import *
from beluga.numeric.data_classes.trajectory_mappers import *

ocp = beluga.Problem()

# Define independent variables
ocp.independent('t', 's')

# Define equations of motion
ocp.state('x', 'v*cos(theta)', 'm')
ocp.state('y', 'v*sin(theta)', 'm')
ocp.state('v', 'g*sin(theta)', 'm/s')

ocp.symmetry(['1', '0', '0'], 'm')
ocp.symmetry(['0', '1', '0'], 'm')

# Define controls
ocp.control('theta', 'rad')

# Define constants
ocp.constant('g', -9.81, 'm/s^2')
ocp.constant('x_f', 0, 'm')
ocp.constant('y_f', 0, 'm')

# Define costs
ocp.path_cost('1', '1')

# Define constraints
ocp.initial_constraint('x', 'm')
ocp.initial_constraint('y', 'm')
ocp.initial_constraint('v', 'm/s')
ocp.initial_constraint('t', 's')
ocp.terminal_constraint('x-x_f', 'm')
ocp.terminal_constraint('y-y_f', 'm')

ocp.scale(m='y', s='y/v', kg=1, rad=1, nd=1)

bvp_solver = beluga.bvp_algorithm('spbvp')

guess_maker = beluga.guess_generator(
    'auto',
    start=[0, 0, 0],          # Starting values for states in order
    costate_guess=-0.1,
    control_guess=[-pi/2],
    use_control_guess=True
)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection') \
                .num_cases(21) \
                .const('x_f', 10) \
                .const('y_f', -10)

continuation_steps.add_step('bisection') \
                .num_cases(40) \
                .const('dchaotic_theta_0', 15.0) \
                .const('chaotic_theta_speed', 60) \
                .const('chaos_parameter', 0.015)

continuation_steps.add_step('bisection') \
                .num_cases(40) \
                .const('dchaotic_theta_0', -15.0)

# 2 to -3 and 0.5 to 1.5 w/ param 0.01

# continuation_steps.add_step('productspace') \
#     .num_subdivisions(30) \
#     .const('chaotic_theta_0', 0.5) \
#     .const('dchaotic_theta_0', -3)

beluga.add_logger(logging_level=logging.DEBUG, display_level=logging.INFO)

# Make the original indirect method beluga uses by default
preprocessor = make_preprocessor()
indirect = make_indirect_method(ocp, analytical_jacobian=False, control_method='differential', method='traditional', reduction=False, do_momentum_shift=True, do_normalize_time=True)
postprocessor = make_postprocessor()

# Read this left to right as "post processor after indirect after preprocessor"
vanilla_indirect = postprocessor * indirect * preprocessor
# Alternatively: vanilla_indirect = preprocessor >> indirect >> postprocessor

class ChaoticOscillator(enum.Enum):
    SIN = enum.auto()

class ChaosMapper(SolMapper):
    def __init__(self, n_states0=0, n_controls0=0, chaos_order=2):
        self.n_states0 = n_states0
        self.n_controls0 = n_controls0
        self.chaos_order = chaos_order

    def map(self, sol: Solution) -> Solution:
        solout = copy.deepcopy(sol)
        
        # Add states for the chaotic shadow vehicle
        solout.y = np.column_stack((solout.y, solout.y))
        if solout.dual.size > 0:
            solout.dual = np.column_stack((solout.dual, solout.dual))

        solout.y = np.column_stack((solout.y, np.zeros((sol.t.size, solout.u.shape[1]*self.chaos_order))))
        if solout.dual.size > 0:
            solout.dual = np.column_stack((solout.dual, np.ones((sol.t.size, solout.u.shape[1]*self.chaos_order))))
        
        return solout

    def inv_map(self, sol: Solution) -> Solution:
        solout = copy.deepcopy(sol)

        solout.shadow = solout.y[:, self.n_states0:2*self.n_states0]
        solout.y = solout.y[:, :self.n_states0]
        solout.dual = solout.dual[:, :self.n_states0]

        return solout


# Make the chaos functor
class ChaosFunctor(GenericFunctor):
    def __init__(self, oscillator: ChaoticOscillator):
        self.oscillator = oscillator

    def transformation(self, prob):
        n_states0 = len(prob.states)
        n_controls0 = len(prob.controls)

        # # Add states for the original vehicle
        # for ii in range(n_states0):
        #     xname = 'src_' + prob.states[ii].name
        #     prob.state(xname, prob.states[ii].eom, prob.states[ii].units)

        # Add states for the chaotic shadow vehicle
        for ii in range(n_states0):
            xname = 'chaotic_' + prob.states[ii].name
            prob.state(xname, prob.states[ii].eom, prob.states[ii].units)

        # Add chaotic oscillators
        for u in prob.controls:
            # Add states for the chaotic oscillator
            cname = 'chaotic_' + u.name
            dcname = 'dchaotic_' + u.name

            if self.oscillator is ChaoticOscillator.SIN:
                prob.state(cname, dcname, u.units)
                prob.state(dcname, '-' + cname + '_speed' + '*' + cname, u.units + '/' + prob.independent_variable.units)

            # Add constants for the initial conditions of the chaotic oscillators
            prob.constant(cname + '_0', 0, u.units)
            prob.constant(dcname + '_0', 0, u.units + '/' + prob.independent_variable.units)

            # Add constant for the speed of the oscillator
            prob.constant(cname + '_speed', 1, '1/' + prob.independent_variable.units)

            # Inject chaotic signal into shadow vehicle control variables
            for ii in range(n_states0):
                prob.states[ii + n_states0].eom = prob.states[ii + n_states0].eom.replace(u.name, '(' + u.name + ' + ' + cname + ')')
        
        # Set cost units for the chaotic cost penalty
        if prob.cost.path_units is not None:
            cparam_units = prob.cost.path_units
        elif prob.cost.units is not None:
            cparam_units = '(' + prob.cost.units + ')' + '/' + '(' + prob.independent_variable.units + ')'
        else:
            raise ValueError('No cost units defined.')
        
        # Create chaos_parameter constant
        prob.constant('chaos_parameter', 1e-12, cparam_units)

        # Build the chaotic cost penalty
        chaos_cost = ''
        for ii in range(n_states0):
            if ii > 0:
                chaos_cost += ' + '
            chaos_cost += 'chaos_parameter*(' + prob.states[ii].name + ' - ' + 'chaotic_' + prob.states[ii].name + ')**2'

        if prob.cost.path is None:
            prob.path_cost(chaos_cost, cparam_units)
        else:
            prob.cost.path += ' + ' + chaos_cost

        # Set initial conditions for the shadow vehicle
        for ii in range(n_states0):
            prob.initial_constraint(prob.states[ii].name + ' - ' + prob.states[ii + n_states0].name, prob.states[ii].units)
        
        # Set initial conditions for the chaotic oscillators
        for ii in range(n_controls0*2):
            prob.initial_constraint(prob.states[2*n_states0 + ii].name + ' - ' + prob.states[2*n_states0 + ii].name + '_0', prob.states[2*n_states0 + ii].units)
        
        prob.sol_map_chain.append(ChaosMapper(n_states0=n_states0, n_controls0=n_controls0))

        return prob

chaosfunctor = ChaosFunctor(ChaoticOscillator.SIN)

chaotic_indirect = postprocessor * indirect * preprocessor * chaosfunctor

vanilla_bvp = vanilla_indirect(copy.deepcopy(ocp))
chaotic_bvp = chaotic_indirect(copy.deepcopy(ocp))

bvp = chaotic_bvp

sol_set = beluga.solve(
    ocp=ocp,
    bvp=bvp,
    ocp_map=bvp.map_sol,
    ocp_map_inverse=bvp.inv_map_sol,
    method='traditional',
    optim_options={},
    bvp_algorithm=bvp_solver,
    steps=continuation_steps,
    guess_generator=guess_maker,
    autoscale=False,
    initial_helper=True,
    save_sols=False
)

# sol_set = beluga.utils.load('data.beluga')['solutions']

import matplotlib.pyplot as plt

orig = sol_set[0][-1]

for sol in sol_set[-1]:
    t1, = plt.plot(sol.shadow[:,0], sol.shadow[:,1], color='lightgray', label='Fully Chaotic Shadow Vehicles')

for sol in sol_set[-1]:
    t2, = plt.plot(sol.y[:,0], sol.y[:,1], color='gray')

t3, = plt.plot(orig.y[:,0], orig.y[:,1], color='b', linewidth=3)

plt.legend([t1, t2, t3], ['Fully Chaotic Shadow Vehicles', 'Flyable Chaotic Trajectories', 'Non-Chaotic Optimal Trajectory'])

plt.grid(True)
plt.show()
