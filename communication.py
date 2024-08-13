import simpy
import random
'''
总时延=发送时延（传输时延）+传播时延+排队时延+处理时延
发送时延=数据长度/信道带宽      数据长度自设为1500B=12000b        信道带宽自设为100(Mbps)=1e+8(bps)       发送时延计算为1.2e-4(s)
传播时延=信道长度/传播速度      信道长度=正上方500km      电磁波在自由空间的传播速度是光速，3e+5(km/s)       传播时延计算为1.67e-3s
排队时延，没有排队情况，0
处理时延，没有处理，0
'''
# 定义仿真环境
env = simpy.Environment()
SpeedOfLight = 3e+8 # (m/s)
# 定义地面站和卫星站
class GroundStation:
    def __init__(self, id):
        self.id = id
        self.inbox = simpy.Store(env)
        self.outbox = simpy.Store(env)

    def send_packet(self, packet):
        print(f"Ground{self.id} sends packet of size {packet} at {env.now}")
        yield self.outbox.put(packet)

    def receive_packet(self):
        packet = yield self.inbox.get()
        print(f"Ground{self.id} receives packet at {env.now}")

class SatelliteStation:
    def __init__(self, id):
        self.id = id
        self.inbox = simpy.Store(env)
        self.outbox = simpy.Store(env)

    def send_packet(self, packet):
        print(f"Satellite{self.id} sends packet of size {packet} at {env.now}")
        yield self.outbox.put(packet)

    def receive_packet(self):
        packet = yield self.inbox.get()
        print(f"Satellite{self.id} receives packet at {env.now}")

    def relay_packet(self):
        packet = yield self.inbox.get()
        print(f"Satellite{self.id} relay packet of size {packet} at {env.now}")
        self.outbox.put(packet)

# 定义通信链路的延迟和带宽
def communication_sourceTtarget(source, target, delay, bandwidth):
    # 模拟带宽限制，传输时延
    packet_size = yield source.outbox.get()  # 这里需要使用 yield 获取数据包大小
    yield simpy.Timeout(env, packet_size / bandwidth)  # 使用 yield 等待带宽限制

    # 模拟传播时延
    yield simpy.Timeout(env, delay)  # 使用 yield 等待时延

    # 将包传递给卫星站
    target.inbox.put(packet_size)

# 定义通信链路的延迟和带宽
def communication_gts(ground_station, satellite_station, delay, bandwidth):
    # 模拟带宽限制，传输时延
    packet_size = yield ground_station.outbox.get()  # 这里需要使用 yield 获取数据包大小
    yield simpy.Timeout(env, packet_size / bandwidth)  # 使用 yield 等待带宽限制

    # 模拟传播时延
    yield simpy.Timeout(env, delay)  # 使用 yield 等待时延
    print(f"Ground{ground_station.id}'s packet has sent to Satellite{satellite_station.id} at {env.now}")
    # 将包传递给卫星站
    satellite_station.inbox.put(packet_size)

# 定义通信链路的延迟和带宽
def communication_sts(satellite_station_source, satellite_station_target, delay, bandwidth):
    # 模拟带宽限制，传输时延
    packet_size = yield satellite_station_source.outbox.get()  # 这里需要使用 yield 获取数据包大小
    yield simpy.Timeout(env, packet_size / bandwidth)  # 使用 yield 等待带宽限制

    # 模拟传播时延
    yield simpy.Timeout(env, delay)  # 使用 yield 等待时延
    print(f"Satellite{satellite_station_source.id}'s packet has sent to Satellite{satellite_station_target.id} at {env.now}")
    # 将包传递给卫星站
    satellite_station_target.inbox.put(packet_size)

# 定义通信链路的延迟和带宽
def communication_stg(satellite_station, ground_station, delay, bandwidth):
    # 模拟带宽限制，传输时延
    packet_size = yield satellite_station.outbox.get()  # 这里需要使用 yield 获取数据包大小
    yield simpy.Timeout(env, packet_size / bandwidth)  # 使用 yield 等待带宽限制

    # 模拟传播时延
    yield simpy.Timeout(env, delay)  # 使用 yield 等待时延
    print(f"Satellite{satellite_station.id}'s packet has sent to Ground{ground_station.id} at {env.now}")
    # 将包传递给卫星站
    ground_station.inbox.put(packet_size)


# 初始化地面站和卫星站
ground1 = GroundStation(-1)
ground2 = GroundStation(-2)
satellite0 = SatelliteStation(0)
satellite1 = SatelliteStation(1)
satellite2 = SatelliteStation(2)

# 定义传输参数
delay = 1.67e-3  # 传播时延，单位：秒
bandwidth = 1e+8  # 带宽，单位：bps

# 启动仿真传输过程
env.process(ground1.send_packet(12000))
env.process(satellite0.relay_packet())
env.process(satellite1.relay_packet())
env.process(satellite2.relay_packet())
env.process(ground2.receive_packet())
# 连接地面站和卫星站
env.process(communication_gts(ground1, satellite0, delay, bandwidth))
env.process(communication_sts(satellite0, satellite1, delay, bandwidth))
env.process(communication_sts(satellite1, satellite2, delay, bandwidth))
env.process(communication_stg(satellite2, ground2, delay, bandwidth))

# 运行仿真
env.run()