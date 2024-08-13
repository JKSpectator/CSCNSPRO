import random

'''
总时延=发送时延（传输时延）+传播时延+排队时延+处理时延
发送时延=数据长度/信道带宽      数据长度自设为1500B=12000b        信道带宽自设为100(Mbps)=1e+8(bps)       发送时延计算为1.2e-4(s)
传播时延=信道长度/传播速度      信道长度=正上方500km      电磁波在自由空间的传播速度是光速，3e+5(km/s)       传播时延计算为1.67e-3s
排队时延，没有排队情况，0
处理时延，没有处理，0
'''


class Communication:
    def __init__(self, configfile='communication_config.txt'):
        self.delay_normal = 0
        self.delay_no_noisy = 0
        self.delay_ideal = 0
        self.bandwidth = 0
        self.is_attacked = False
        self.attack_probability = 0
        self.velocity = 3e+8
        self.packet_size = 12000
        self.noisy = 0  # 0 没有噪声, 1 高斯噪声, 2 均匀噪声
        with open(configfile, 'r') as f:
            for line in f:
                words = line.split()
                if words[0] == 'bandwidth':
                    self.bandwidth = int(words[1])
                elif words[0] == 'velocity':
                    self.velocity = int(words[1])
                elif words[0] == 'packet_size':
                    self.packet_size = int(words[1])
                elif words[0] == 'noisy':
                    self.noisy = int(words[1])

    def communication_stt(self, distance=5e+5, packet_size=0, bandwidth=-1, is_attacked=False, add_delay=True):
        if packet_size == 0:
            packet_size = self.packet_size

        if bandwidth == -1:
            bandwidth = self.bandwidth

        if self.noisy != 0:
            random.seed(0)
            if self.noisy == 1:
                rm = random.gauss(0, 0.1)
                while rm + 1 == 0:
                    rm = random.gauss(0, 0.1)
                bandwidth *= rm
            elif self.noisy == 2:
                rm = random.random() * 2
                while rm == 0:
                    rm = random.random() * 2
                bandwidth *= rm

        delay = 0
        send_delay = packet_size / bandwidth
        propagation_delay = distance / self.velocity
        delay = delay + send_delay + propagation_delay

        if add_delay:
            self.delay_normal += delay

        return delay

    def communication_stt_no_noisy(self, distance=5e+5, packet_size=0, bandwidth=-1, add_delay=True):
        if packet_size == 0:
            packet_size = self.packet_size

        if bandwidth == -1:
            bandwidth = self.bandwidth

        delay = 0
        send_delay = packet_size / bandwidth
        propagation_delay = distance / self.velocity
        delay = delay + send_delay + propagation_delay

        if add_delay:
            self.delay_no_noisy += delay

        return delay


    def communication_stt_ideal(self, distance=5e+5, add_delay=True):
        delay = 0
        propagation_delay = distance / self.velocity
        delay = delay + propagation_delay

        if add_delay:
            self.delay_ideal += delay

        return delay


