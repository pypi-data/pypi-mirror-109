"""
References
----------
.. [1] Vinh, Nguyen X., Adolf Busemann, and Robert D. Culp. "Hypersonic and planetary entry flight mechanics."
    NASA STI/Recon Technical Report A 81 (1980).
"""

from math import pi
import beluga
from beluga.utils import save
import logging

X0 = [80000., 0., 0., 4000., -75*pi/180, 0., 0., 0.]
ocp = beluga.Problem()

# Define independent variables
ocp.independent('t', 's')

# Define equations of motion
ocp.state('h', 'v*sin(gam)', 'm')
ocp.state('theta', 'v*cos(gam)*cos(psi)/(r*cos(phi))', 'rad')
ocp.state('phi', 'v*cos(gam)*sin(psi)/r', 'rad')
ocp.state('v', '-D/mass - mu*sin(gam)/r**2', 'm/s')
ocp.state('gam', 'L*cos(bank)/(mass*v) - mu/(v*r**2)*cos(gam) + v/r*cos(gam)', 'rad')
ocp.state('psi', 'L*sin(bank)/(mass*cos(gam)*v) - v/r*cos(gam)*cos(psi)*tan(phi)', 'rad')
ocp.state('alpha', 'u1', 'rad')
ocp.state('bank', 'u2', 'rad')


# Define quantities used in the problem
ocp.quantity('rho', 'rho0*exp(-h/H)')
ocp.quantity('Cl', '1.5658*alpha')
ocp.quantity('Cd', '1.6537*alpha**2 + 0.0612')
ocp.quantity('D', '0.5*rho*v**2*Cd*Aref')
ocp.quantity('L', '0.5*rho*v**2*Cl*Aref')
ocp.quantity('r', 're + h')

# Define controls
ocp.control('u1', 'rad/s')
ocp.constant('epsilon1', 200, 'm**2/s**3')
ocp.constant('u1_max', 20*pi/180, 'rad/s')
ocp.path_constraint('u1', 'rad/s', lower='-u1_max', upper='u1_max', activator='epsilon1', method='epstrig+', regulator='erf')

ocp.control('u2', 'rad/s')
ocp.constant('epsilon2', 200, 'm**2/s**3')
ocp.constant('u2_max', 360*pi/180, 'rad/s')
ocp.path_constraint('u2', 'rad/s', lower='-u2_max', upper='u2_max', activator='epsilon2', method='epstrig+', regulator='erf')

# Define constants
ocp.constant('mu', 3.986e5*1e9, 'm**3/s**2')  # Gravitational parameter, m**3/s**2
ocp.constant('rho0', 1.2, 'kg/m**3')  # Sea-level atmospheric density, kg/m**3
ocp.constant('H', 7500, 'm')  # Scale height for atmosphere of Earth, m
ocp.constant('mass', 750/2.2046226, 'kg')  # Mass of vehicle, kg
ocp.constant('re', 6378000, 'm')  # Radius of planet, m
ocp.constant('Aref', pi*(24*.0254/2)**2, 'm**2')  # Reference area of vehicle, m**2
ocp.constant('h_0', X0[0], 'm')
ocp.constant('theta_0', X0[1], 'rad')
ocp.constant('phi_0', X0[2], 'rad')
ocp.constant('v_0', X0[3], 'm/s')
ocp.constant('gam_0', X0[4], 'rad')
ocp.constant('psi_0', X0[5], 'rad')
ocp.constant('alpha_0', X0[6], 'rad')
ocp.constant('bank_0', X0[7], 'rad')
ocp.constant('h_f', 0., 'm')
ocp.constant('theta_f', 0., 'rad')
ocp.constant('phi_f', 0., 'rad')

ocp.constant('half_ang', 5*pi/2, 'rad')
ocp.constant('eps_ang', 1e-2, '1')

# Define costs
ocp.terminal_cost('-(v**2)', 'm**2/s**2')

# Define constraints
ocp.initial_constraint('h - h_0', 'm')
ocp.initial_constraint('theta - theta_0', 'rad')
ocp.initial_constraint('phi - phi_0', 'rad')
ocp.initial_constraint('v - v_0', 'm/s')
ocp.initial_constraint('gam - gam_0', 'rad')
ocp.initial_constraint('psi - psi_0', 'rad')
ocp.terminal_constraint('alpha', 'rad')
ocp.terminal_constraint('bank', 'rad')
ocp.initial_constraint('t', 's')
ocp.terminal_constraint('h - h_f', 'm')
ocp.terminal_constraint('theta - theta_f', 'rad')
ocp.terminal_constraint('phi - phi_f', 'rad')

ocp.terminal_constraint('gam', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')
ocp.terminal_constraint('psi', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')

ocp.scale(m='h', s='h/v', kg='mass', rad=1)
# ocp.scale(m=1, s=1, kg=1, rad=1)

bvp_solver = beluga.bvp_algorithm('spbvp')

guess_maker = beluga.guess_generator(
    'auto',
    start=X0,
    direction='forward',
    costate_guess=-0.1,
    control_guess=[0., 0.],
    use_control_guess=True,
    time_integrate=0.5
)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection').num_cases(10) \
    .const('theta_f', 0.01*pi/180) \
    .const('h_f', 0)

continuation_steps.add_step('bisection').num_cases(11) \
    .const('gam_0', -80*pi/180) \
    .const('theta_f', 0.5*pi/180)

# shallower entry
continuation_steps.add_step('bisection').num_cases(31) \
    .const('gam_0', -1.5*pi/180) \
    .const('theta_f', 2.82*pi/180)

# crossrange
continuation_steps.add_step('bisection').num_cases(9) \
    .const('phi_f', 0.5*pi/180)

# epstrig+ epsilon
continuation_steps.add_step('bisection', raise_exception=False).num_cases(30) \
    .const('epsilon1', 1e-3) \
    .const('epsilon2', 1e-3)

beluga.add_logger(logging_level=logging.DEBUG, display_level=logging.INFO)

sol_set = beluga.solve(
    ocp=ocp,
    method='indirect',
    optim_options={'control_method':'pmp'},
    bvp_algorithm=bvp_solver,
    steps=continuation_steps,
    guess_generator=guess_maker,
    initial_helper=True,
    save=False
)

import matplotlib.pyplot as plt

sol = sol_set[-1][-1]

plt.plot(sol.t, sol.u[:,0], color='b')
plt.plot(sol.t, sol.u[:,1], color='r')
plt.show()

# save(ocp=ocp, bvp=None, bvp_solver=None, sol_set=sol_set, filename='data.beluga')
