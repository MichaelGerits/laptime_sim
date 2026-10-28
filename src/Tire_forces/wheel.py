import numpy as np
from typing import TypedDict

class Wheel_parameters(TypedDict):
    """
    defines what the wheel parameter dictionary should look like and include
    """
    gamma_0: float
    del_0: float
    omega_c: float
    r_r: float
    p: float
    Iy: float 

class Wheel:
    def __init__(self, param:Wheel_parameters, ind=np.ones(2)):
        """
        object class for the wheel, houses the wheels dynamics and local in plane forces
        """
        self.pos = np.zeros(3) #vehicle body position coor
        self.vel = np.zeros(3) #global velocity coordinate
        self.ind = ind #position index (take 3/2 j index for single track)

        self.cam_0:float = param['gamma_0'] #wheel camber
        self.cam:float = self.cam_0
        self.delta = param['del_0'] #steering angle
        self.alpha:float = 0.0
        self.kappa:float = 0.0

        self.r_r = param['r_r']
        self.p = param['p'] #tire stiffness

        self.omega_c:float = 0.0
        self.Iy = param['Iy'] #inertia around rotational axis

    def __str__(self):
        return f"Wheel: {self.ind}"

    def calc_pos(self, a:np.typing.NDArray[np.float64], t:np.typing.NDArray[np.float64]):
    

        x:float = a[self.ind[0]-1] * (self.ind[0] * -2) + 3 #1 -> -2+3=1, 2 -> -4+3=-1
        y:float = t[self.ind[1]-1]/2 * (self.ind[1] * -2) + 3 #1 -> -2+3=1, 2 -> -4+3=-1

        self.pos = np.array([x,y,0]) #3dimensional for vector products

    def calc_vel(self, V_veh:np.typing.NDArray[np.float64], gamma_veh:np.typing.NDArray[np.float64]):
        
        if np.linalg.norm(self.pos - np.zeros(3)) <= 0.15:
            raise ValueError(f"Wheel {self.ind} relative position is too small for realistic velocity calculation")

        self.vel = np.cross(gamma_veh, self.pos) + V_veh #3dimensional for vector products
        #TODO: account for suspension dynamics (double track)

    def calc_slipangle(self):
        """calculates the slip angle of the tire"""

        self.alpha = -1*(self.delta - np.atan2(self.vel[1], self.vel[0])) #ISO standard

    def calc_slipratio(self):
        """calculates the tire slip without accounting for rotational offsets from guigianni"""

        self.kappa = (self.vel[0]- self.omega_c*self.r_r) / np.abs(self.vel[0])
    
    #TODO: add tire model fitting
    #TODO: calc longitudinal slip
    #TODO: calc lateral and longitudinal force and correcting moment
    #TODO: pu limit on total grip

    #TODO: add 3d plotting
