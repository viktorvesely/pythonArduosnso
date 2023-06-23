from __future__ import annotations

import serial
import time
import numpy as np
from typing import Callable
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("GTK4Agg")

from task import Task

UpdateData = tuple[np.ndarray, np.ndarray]
UpdateCallback = Callable[['Puncher', UpdateData], any]

class Puncher(Task):

    i_accx = 0
    i_accy = 1
    i_accz = 2

    i_gyx = 3
    i_gyy = 4
    i_gyz = 5
    

    def __init__(self, visual: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.visual = visual

        self.write_time = 30
        self.acc_path = "./data/acc.npy"
        self.gyr_path = "./data/gyr.npy"
        
        self.callbacks : list[UpdateCallback] = []
        self.connection = None

        self.fig, self.ax = None, None
        self.trajectory = None
        self.trajectory_length = 30
        self.t_acc, self.t_gyr = None, None
        
        if visual: 
            self.setup_visuals()    

    def setup_visuals(self):
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection = '3d')
        self.trajectory = self.ax.plot([], [], [], marker = 'o')[0]
        self.t_acc, self.t_gyr = [], []
        plt.show()

        self.on_update(self.update_visuals)

    def on_update(self, callback: UpdateCallback) -> Puncher:
        self.callbacks.append(callback)
        return self

    def process_data(self, acc: np.ndarray, gyr: np.ndarray) -> UpdateData: 

        return acc, gyr
        
    def update_visuals(self, _: Puncher, data: UpdateData):

        if not self.visual:
            return

        self.t_acc.append(data[0])
        self.t_gyr.append(data[1])

        self.t_acc = self.t_acc[-self.trajectory_length:]
        self.t_gyr = self.t_gyr[-self.trajectory_length:]

        accs = np.array(self.t_acc)
        gyrs = np.array(self.t_gyr)

        self.trajectory.set_data(accs[:, :2].T)
        self.trajectory.set_3d_properties(accs[:, 2].T)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        

    def read_data(self) -> UpdateData:
        line = self.connection.readline().decode("utf-8")
        nums = line.split(",")
        nums = np.array([float(num) for num in nums])

        acc = nums[self.i_accx:(self.i_accz + 1)]
        gyr = nums[self.i_gyx:(self.i_gyz + 1)]

        return self.process_data(acc, gyr)

    def trigger_update(self, data: UpdateData):
        
        for callback in self.callbacks:
            callback(self, data)

    def run(self):
        super().run()

        with serial.Serial("COM3",timeout=1, baudrate=115200) as connection:
            self.connection = connection
            while self.is_running():
                data = self.read_data()
                self.trigger_update(data)
                time.sleep(0.003)

        self.connection = None
    
