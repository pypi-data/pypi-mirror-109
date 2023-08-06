import sys
import numpy as np
from math import pi
import beluga
import logging
import matplotlib.pyplot as plt

def rhoorig(x):
    return 1.23093524565514*np.exp(-x/7500)

def rhonew(x):
    return 1.23093524565514*np.exp(-0.0750885666941723*x + -0.00457449668124128*x**2 + 0.00010523812373774*x**3 + -9.3689305988181e-7*x**4 + 2.65316029433927e-9*x**5)

X = np.linspace(0,40000,20)

plt.plot(X, rhoorig(X), color='b')
plt.plot(X, rhonew(X), color='r')
plt.show()

heightVal   = 40000
velocityVal = 2000

# Rename this and/or move to optim package?
ocp = beluga.OCP()

# Define independent variables
ocp.independent('t', 's')

#rho = 'rho0*exp(a1*h+a2*h**2+a3*h**3+a4*h**4+a5*h**5)'
rho = 'rho0*exp(-h/H)'

Cl = '(1.5658*alpha + -0.0000)'   # lift coefficient
Cd = '(1.6537*alpha**2 + 0.0612)' # drag coefficient
D  = '(0.5*{}*v**2*{}*Aref)'.format(rho, Cd)
L  = '(0.5*{}*v**2*{}*Aref)'.format(rho, Cl)
r  = '(re+h)'

# Define equations of motion
ocp \
    .state('h',     'v*sin(gam)', 'm') \
    .state('theta', 'v*cos(gam)*cos(psi)/({}*cos(phi))'.format(r), 'rad') \
    .state('phi',   'v*cos(gam)*sin(psi)/{}'.format(r), 'rad') \
    .state('v',     '-{}/mass - mu*sin(gam)/{}**2'.format(D, r), 'm/s') \
    .state('gam',   '{}*cos(bank)/(mass*v) - mu/(v*{}**2)*cos(gam) + v/{}*cos(gam)'.format(L, r, r), 'rad') \
    .state('psi',   '{}*sin(bank)/(mass*cos(gam)*v) - v/{}*cos(gam)*cos(psi)*tan(phi)'.format(L, r), 'rad')

# Define controls
ocp.control('alpha', 'rad') \
   .control('bank', 'rad')

# Define costs (maximize impact velocity)
ocp.terminal_cost('-(v**2)', 'm**2/s**2')

# Define constraints
ocp.initial_constraint('h-h_0', 'm')
ocp.initial_constraint('theta-theta_0', 'rad')
ocp.initial_constraint('phi', 'rad')
ocp.initial_constraint('v-v_0', 'm/s')
ocp.initial_constraint('gam-gam_0', 'rad')
ocp.initial_constraint('psi-psi_0', 'rad')
ocp.initial_constraint('t', 's')
ocp.terminal_constraint('h-h_f', 'm')
ocp.terminal_constraint('theta-theta_f', 'rad')
ocp.terminal_constraint('phi-phi_f', 'rad')
ocp.terminal_constraint('gam', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')
ocp.terminal_constraint('psi', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')

# Define constants
ocp.constant('mu',   3.986e5*1e9,  'm**3/s**2')  # Gravitational parameter, m**3/s**2
ocp.constant('rho0', 1.23093524565514, 'kg/m**3')# Sea-level atmospheric density, kg/m**3
ocp.constant('H',    7500,         'm')          # Scale height for atmosphere of Earth, m
ocp.constant('mass', 750/2.2046226,'kg')         # Mass of vehicle, kg
ocp.constant('re',   6378000,      'm')          # Radius of planet, m
ocp.constant('Aref', pi*(24*.0254/2)**2, 'm**2') # Reference area of vehicle, m**2
ocp.constant('rn',   1/12*0.3048, 'm')           # Nose radius, m
ocp.constant('h_0',     heightVal,         'm')
ocp.constant('theta_0', 0,             'rad')
ocp.constant('v_0',     velocityVal,   'm/s')
ocp.constant('gam_0', -(90-10)*pi/180, 'rad')
ocp.constant('psi_0',   0,             'rad')
ocp.constant('h_f',     0,             'm')
ocp.constant('theta_f', 0,             'rad')
ocp.constant('phi_f',   0,             'rad')
ocp.constant('a1',-0.0750885666941723, 'm**(-1)')
ocp.constant('a2',-0.00457449668124128,'m**(-2)')
ocp.constant('a3',0.00010523812373774, 'm**(-3)')
ocp.constant('a4',-9.3689305988181e-7, 'm**(-4)')
ocp.constant('a5',2.65316029433927e-9, 'm**(-5)')
ocp.constant('eps', 0, '1')
ocp.constant('half_ang', 5*pi/2, 'rad')
ocp.constant('eps_ang', 1e-2, '1')
ocp.constant('H2', 7100, 'm')

ocp.scale(m='h', s='h/v', kg='mass', rad=1)

bvp_solver = beluga.bvp_algorithm('spbvp')

guess_maker = beluga.guess_generator(
    'auto',
    start=[heightVal, 0, 0, velocityVal, -(90-10)*pi/180, 0],
    direction='forward',
    costate_guess=-0.1,
    control_guess=[0.0, 0.0],
    use_control_guess=True,
    time_integrate=0.5,
)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection').num_cases(21) \
    .const('h_f',     0) \
    .const('theta_f', 6945.9/6378000)

continuation_steps.add_step('bisection').num_cases(21) \
    .const('theta_f', 0.5*pi/180)

continuation_steps.add_step('bisection').num_cases(41) \
    .const('gam_0', 0) \
    .const('theta_f', 3*pi/180)

continuation_steps.add_step('bisection').num_cases(41) \
    .const('phi_f', 2*pi/180)

beluga.add_logger(logging_level=logging.DEBUG, display_level=logging.DEBUG)

bvp, gamma_map, gamma_map_inverse = beluga.ocp2bvp(ocp)

sol_set = beluga.solve(
    ocp=ocp,
    bvp=bvp,
    ocp_map=gamma_map,
    ocp_map_inverse=gamma_map_inverse,
    method='indirect',
    bvp_algorithm=bvp_solver,
    steps=continuation_steps,
    guess_generator=guess_maker,
    initial_helper=True
)

traj0 = sol_set[-1][-1]

heightVal   = 40000
velocityVal = 2000

# Rename this and/or move to optim package?
ocp = beluga.OCP()

# Define independent variables
ocp.independent('t', 's')

rho_0 = 'rho0*exp(a1*h+a2*h**2+a3*h**3+a4*h**4+a5*h**5)'
rho_0 = 'rho0*exp(-h/H2)'
rho_1 = 'rho0*exp(-h/H)'
rho = '((eps)*({}) + (1 - eps)*({}))'.format(rho_0, rho_1)

# rho = 'rho0*exp(-h/H)'

Cl = '(1.5658*alpha + -0.0000)'   # lift coefficient
Cd = '(1.6537*alpha**2 + 0.0612)' # drag coefficient
D  = '(0.5*{}*v**2*{}*Aref)'.format(rho, Cd)
L  = '(0.5*{}*v**2*{}*Aref)'.format(rho, Cl)
r  = '(re+h)'

# Define equations of motion
ocp \
    .state('h',     'v*sin(gam)', 'm') \
    .state('theta', 'v*cos(gam)*cos(psi)/({}*cos(phi))'.format(r), 'rad') \
    .state('phi',   'v*cos(gam)*sin(psi)/{}'.format(r), 'rad') \
    .state('v',     '-{}/mass - mu*sin(gam)/{}**2'.format(D, r), 'm/s') \
    .state('gam',   '{}*cos(bank)/(mass*v) - mu/(v*{}**2)*cos(gam) + v/{}*cos(gam)'.format(L, r, r), 'rad') \
    .state('psi',   '{}*sin(bank)/(mass*cos(gam)*v) - v/{}*cos(gam)*cos(psi)*tan(phi)'.format(L, r), 'rad')

# Define controls
ocp.control('alpha', 'rad') \
   .control('bank', 'rad')

# Define costs (maximize impact velocity)
ocp.terminal_cost('-(v**2)', 'm**2/s**2')

# Define constraints
ocp.initial_constraint('h-h_0', 'm')
ocp.initial_constraint('theta-theta_0', 'rad')
ocp.initial_constraint('phi', 'rad')
ocp.initial_constraint('v-v_0', 'm/s')
ocp.initial_constraint('gam-gam_0', 'rad')
ocp.initial_constraint('psi-psi_0', 'rad')
ocp.initial_constraint('t', 's')
ocp.terminal_constraint('h-h_f', 'm')
ocp.terminal_constraint('theta-theta_f', 'rad')
ocp.terminal_constraint('phi-phi_f', 'rad')
ocp.terminal_constraint('gam', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')
ocp.terminal_constraint('psi', 'rad', lower='-half_ang', upper='half_ang', activator='eps_ang', method='utm')

# Define constants
ocp.constant('mu',   3.986e5*1e9,  'm**3/s**2')  # Gravitational parameter, m**3/s**2
ocp.constant('rho0', 1.23093524565514, 'kg/m**3')# Sea-level atmospheric density, kg/m**3
ocp.constant('H',    7500,         'm')          # Scale height for atmosphere of Earth, m
ocp.constant('mass', 750/2.2046226,'kg')         # Mass of vehicle, kg
ocp.constant('re',   6378000,      'm')          # Radius of planet, m
ocp.constant('Aref', pi*(24*.0254/2)**2, 'm**2') # Reference area of vehicle, m**2
ocp.constant('rn',   1/12*0.3048, 'm')           # Nose radius, m
ocp.constant('h_0',     heightVal,         'm')
ocp.constant('theta_0', traj0.y[0][1],             'rad')
ocp.constant('v_0',     traj0.y[0][3],   'm/s')
ocp.constant('gam_0', traj0.y[0][4], 'rad')
ocp.constant('psi_0',   traj0.y[0][5],             'rad')
ocp.constant('h_f',     traj0.y[-1][0],             'm')
ocp.constant('theta_f', traj0.y[-1][1],             'rad')
ocp.constant('phi_f',   traj0.y[-1][2],             'rad')
ocp.constant('a1',-0.0750885666941723, 'm**(-1)')
ocp.constant('a2',-0.00457449668124128,'m**(-2)')
ocp.constant('a3',0.00010523812373774, 'm**(-3)')
ocp.constant('a4',-9.3689305988181e-7, 'm**(-4)')
ocp.constant('a5',2.65316029433927e-9, 'm**(-5)')
ocp.constant('eps', 0, '1')
ocp.constant('half_ang', 5*pi/2, 'rad')
ocp.constant('eps_ang', 1e-2, '1')
ocp.constant('H2', 7100, 'm')

ocp.scale(m='h', s='h/v', kg='mass', rad=1)

bvp_solver = beluga.bvp_algorithm('spbvp')

guess_maker = beluga.guess_generator('static', solinit=traj0)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection').num_cases(50) \
    .const('eps', 1.0)

bvp, gamma_map, gamma_map_inverse = beluga.ocp2bvp(ocp)

sol_set = beluga.solve(
    ocp=ocp,
    bvp=bvp,
    ocp_map=gamma_map,
    ocp_map_inverse=gamma_map_inverse,
    method='indirect',
    optim_options={'control_method':'pmp'},
    bvp_algorithm=bvp_solver,
    steps=continuation_steps,
    guess_generator=guess_maker,
    initial_helper=True,
)

traj1 = sol_set[-1][-1]

plt.plot(traj0.y[:,3], traj0.y[:,0], color='r', label='atmosphere 1')
plt.plot(traj1.y[:,3], traj1.y[:,0], color='b', label='atmosphere 2')
plt.legend()
plt.grid()
plt.show()
