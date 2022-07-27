import threading
import socket
from .tools import log
import cv2
import numpy as np


class TCPServer:
    def __init__(self, port):
        """
        默认构造方法
        :param port: 通讯程序端口 (int)
        """
        # 获取本机IP
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.port = port
        # 设定服务器
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        # 客户端信息
        self.connection = None
        self.connection_status = False
        self.client_address = None

    def _getMessage(self):
        """接收报文"""
        # 检查连接状态
        while True:
            if self.connection_status is True:
                break
        # 客户端已连接
        while True:
            try:
                message = str(self.connection.recv(1024), encoding="utf-8")
                # 收到断开TCP连接指令
                if message == 'quit':
                    self.connection.close()
                    self.connection_status = False
                    self.init()  # 重新开始监听等待状态
                    return None
                # 收到关闭服务器指令
                elif message == 'shut down':
                    self.shutDown()
                    return None
                # 收到其他信息
                else:
                    # 异常信息
                    if message == '':
                        raise ConnectionResetError
                    log('Received message: ' + message)
                    # TODO 将信息通过串口传输给STM32进行决策

            # 连接异常断开
            except ConnectionResetError:
                log(self.client_address[0] + ' disconnected!')
                print("--------------------------------------")
                self.connection.close()
                self.connection_status = False
                self.init()
                return None

    def sendImage(self, img):
        """
        发送报文
        :param img: 待发送图片 (ndarray)
        :return: None
        """
        if self.connection_status is False:
            return None

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, img_encode = cv2.imencode('.jpg', img, encode_param)
        data = np.array(img_encode)
        message = data.tostring()

        self.connection.send(message)
        log('Image sent')

    def init(self):
        """初始化服务器，进入监听状态，等待连接"""
        print("--------------------------------------")
        log('IP: ' + self.ip + ', Port: ' + str(self.port))
        self.server.listen(3)
        log('Start listening...')
        self.connection, self.client_address = self.server.accept()
        self.connection_status = True
        log(self.client_address[0] + ' connected!')
        # 新建线程获取信息
        thrd = threading.Thread(target=self._getMessage)
        thrd.setDaemon(False)
        thrd.start()

    def shutDown(self):
        """断开TCP连接，关闭服务器"""
        self.connection.close()
        self.server.close()
        log('Shut down')
