import numpy as np
import sys

sys.path.append("./submodules/free-dog-sdk/")
from ucl.lowCmd import lowCmd
from ucl.complex import motorCmd, motorCmdArray
from ucl.enums import MotorModeLow

sys.path.append('./submodules/unitree_legged_sdk/lib/python/amd64')
import robot_interface_aliengo as sdk

import constants


class Command:
    def __init__(self, q=[0.]*12, dq=[0.]*12, Kp=[0.]*12, Kd=[0.]*12, tau=[0.]*12):
        self.q = np.array(q, dtype=np.float32)
        self.dq = np.array(dq, dtype=np.float32)
        self.Kp = np.array(Kp, dtype=np.float32)
        self.Kd = np.array(Kd, dtype=np.float32)
        self.tau = np.array(tau, dtype=np.float32)

    def robot_cmd(self) -> lowCmd:
        lcmd = lowCmd()
        mCmdArr = motorCmdArray()
        for i in range(12):
            mCmdArr.setMotorCmd(
                constants.motors_names[i],
                motorCmd(mode=MotorModeLow.Servo,
                         q=self.q[i].item(),
                         dq=self.dq[i].item(),
                         Kp=self.Kp[i].item(),
                         Kd=self.Kd[i].item(),
                         tau=self.tau[i].item())
            )
        lcmd.motorCmd = mCmdArr
        return lcmd
    

    def aliengo_cmd(self, lcmd, p = False):
        # lcmd = sdk.LowCmd() 

        # LOWLEVEL  = 0xff  # TEMP!!!!
        # lcmd.levelFlag = LOWLEVEL   

        print(lcmd)             
        # print( type(lcmd) )          

        for i in range(12):
            lcmd.motorCmd[i].q = self.q[i].item()
            lcmd.motorCmd[i].dq = self.dq[i].item()
            lcmd.motorCmd[i].Kp = self.Kp[i].item()
            lcmd.motorCmd[i].Kd = self.Kd[i].item()
            lcmd.motorCmd[i].tau = self.tau[i].item()
        
        return lcmd

    def get_command(self, num):
        return (
                self.q[num].item(),
                self.dq[num].item(),
                self.Kp[num].item(),
                self.Kd[num].item(),
                self.tau[num].item(),
            )

    def clamp_q(self):
        self.q = np.clip(self.q, constants.q_mujoco_min, constants.q_mujoco_max)

    def copy(self, q=None, dq=None, Kp=None, Kd=None, tau=None):
        return Command(
            q = self.q.copy() if q is None else q,
            dq = self.dq.copy() if dq is None else dq,
            Kp = self.Kp.copy() if Kp is None else Kp,
            Kd = self.Kd.copy() if Kd is None else Kd,
            tau = self.tau.copy() if tau is None else tau,
        )


def CommandFromArray5(arr: list[tuple[float]]) -> Command:
    '''
    arr - 12 elements list of 4-tuples [q, dq, Kp, Kd, tau] for
    (FR_0, FR_1, FR2, FL_0, FL_1, FL_2, RR_0, RR_1, RR_2, RL_0, RL_1, RL_2)
    '''
    return Command(
        q=[e[0] for e in arr],
        dq=[e[1] for e in arr],
        Kp=[e[2] for e in arr],
        Kd=[e[3] for e in arr],
        tau=[e[4] for e in arr]
    )


def CommandFromArray3(arr: list[tuple[float]], dq=0, tau=0) -> Command:
    '''
    arr - 12 elements list of 4-tuples [q, Kp, Kd] for
    (FR_0, FR_1, FR2, FL_0, FL_1, FL_2, RR_0, RR_1, RR_2, RL_0, RL_1, RL_2)
    '''
    return Command(
        q=[e[0] for e in arr],
        dq=[dq]*12,
        Kp=[e[1] for e in arr],
        Kd=[e[2] for e in arr],
        tau=[tau]*12
    )
