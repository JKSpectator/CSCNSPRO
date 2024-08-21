import mmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use("TkAgg")
# 设置显示中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 准备数据
t = []  # X轴数据点
delay = []
delay_no_noisy = []  # Y轴数据点
delay_ideal = []

# 共享内存名称
file_name = 'global_share_memory'
# 内存区域
shmem = mmap.mmap(0, 100, file_name, mmap.ACCESS_READ)

# 定义图表和轴
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Communication Delay", color='r')
line2, = ax.plot([], [], label="Noise-Free Communication Delay", color='b')
line3, = ax.plot([], [], label="Ideal Communication Delay", color='g')

# 初始化图表，设置空的数据集
def init():
    ax.set_xlim(1, 100)  # 这里设置一个初始范围，可以根据需要调整
    ax.set_ylim(0, 0.004)  # 这里设置一个初始范围，可以根据需要调整
    ax.legend()
    return line1, line2, line3

# 更新函数，每次调用时添加新的数据点
def update(frame):
    data = np.frombuffer(shmem, dtype=np.double, count=3)
    if frame > 100:
        frame %= 100
    t.pop(0)
    t.append(frame)
    delay.pop(0)
    delay.append(data[0])
    delay_no_noisy.pop(0)
    delay_no_noisy.append(data[1])
    delay_ideal.pop(0)
    delay_ideal.append(data[2])

    line1.set_data(t, delay)
    line2.set_data(t, delay_no_noisy)
    line3.set_data(t, delay_ideal)

    return line1, line2, line3

# 创建动画
ani = FuncAnimation(fig, update, frames=range(1, 101), init_func=init, blit=True)
plt.title("Communication Delay Variation Over Test Rounds")
plt.xlabel("Sample Slot")
plt.ylabel("Delay(s)")
plt.grid(True)

plt.show()