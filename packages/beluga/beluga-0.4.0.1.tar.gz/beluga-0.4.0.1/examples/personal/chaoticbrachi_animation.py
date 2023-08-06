import beluga
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from celluloid import Camera

sol_set = beluga.utils.load('shiftspeed.beluga')['solutions']

orig = sol_set[0][-1]
speeds = set()

for sol in sol_set[-1]:
    speeds.add(sol.const[-2])

speeds = sorted(speeds)


fig = plt.figure()
camera = Camera(fig)

for speed in speeds:
    for sol in sol_set[-1]:
        if sol.const[-2] == speed:
            t = plt.plot(sol.y[:,0], sol.y[:,1], color='gray')

    plt.plot(orig.y[:,0], orig.y[:,1], color='b', linewidth=3)
    plt.legend(t, ['Oscillator speed: {0:0.2f}'.format(speed)])
    camera.snap()

animation = camera.animate()
animation.save('trajs_speed.gif', writer = 'imagemagick')

sol_set = beluga.utils.load('shiftphase.beluga')['solutions']

orig = sol_set[0][-1]
phases = set()

for sol in sol_set[-1]:
    phases.add(sol.const[-4])

phases = sorted(phases)


fig = plt.figure()
camera = Camera(fig)

for phase in phases:
    for sol in sol_set[-1]:
        if sol.const[-4] == phase:
            t = plt.plot(sol.y[:,0], sol.y[:,1], color='gray')

    plt.plot(orig.y[:,0], orig.y[:,1], color='b', linewidth=3)
    plt.legend(t, ['Oscillator phase: {0:0.2f}'.format(phase)])
    camera.snap()

animation = camera.animate()
animation.save('trajs_phase.gif', writer = 'imagemagick')