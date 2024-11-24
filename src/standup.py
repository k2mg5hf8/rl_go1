import time
from freedogs2py_bridge import RealGo1

import config
import positions
import utils


config.ENABLE_SIMULATION = True

real = False
conn = None

if not real:
    import simulation

    conn = simulation.Simulation(config)
    conn.set_keyframe(0)
else:
    conn = RealGo1()


conn.start()
time.sleep(0.2)

cycles = 0
phase = 0
phase_cycles = 0

stand_command = positions.stand_command_2()


while real or conn.viewer.is_running():
    cur_state = conn.get_latest_state()
    if cur_state is not None:
        state = cur_state

    if phase == 0:
        if phase_cycles >= 100:
            phase = 1
            phase_cycles = 0
    elif phase == 1:
        if phase_cycles >= 100:
            phase = 2
            phase_cycles = 0
            init_q = utils.q_vec(state)
        conn.send(positions.laydown_command().robot_cmd())
    elif phase == 2:
        q_step = utils.interpolate(init_q, stand_command.q, phase_cycles, 500)
        conn.send(stand_command.copy(q = q_step).robot_cmd())

    phase_cycles += 1
    time.sleep(0.01)
