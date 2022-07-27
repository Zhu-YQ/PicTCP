import socket
from .tools import log
import cv2
import numpy as np


class TCPClient:
    def __init__(self, server_ip, server_port):
        """
        默认构造方法
        :param server_ip: 服务器IP (str)
        :param server_port: 服务器程序端口 (int)
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))

    def getAndInferImage(self):
        while True:
            data, addr = self.client.recvfrom(90000)
            pic = np.fromstring(data, dtype='uint8')
            pic = cv2.imdecode(pic, cv2.IMREAD_COLOR)
            # 图像处理
            # TODO 传入神经网络，得到位置信息
            cv2.imshow('', pic)
            cv2.waitKey()
            cv2.destroyAllWindows()
            # 返回数据
            # TODO 返回位置信息
            self.sendMessage('12345')

    def sendMessage(self, message):
        self.client.send(message.encode(encoding='utf-8'))

    def sendMessages(self):
        flag = True
        while flag:
            message = input("Client>> ")
            self.sendMessage(message)
            if message == 'exit':
                self.close()
                flag = False

    def close(self):
        self.client.close()
        log('closed')

