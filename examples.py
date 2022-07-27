from TCPHelper import TCPServer
from TCPHelper import TCPClient
from TCPHelper import resize
import threading
import cv2


# 图像发送方
def serverTest():
    # 服务器设置
    server = TCPServer(123)
    server.init()
    # 摄像头设置
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        _, frame = camera.read()
        # cv2.imshow('video', frame)
        if cv2.waitKey(10) == ord('q') or cv2.waitKey(10) == ord('Q'):
            break

        img = resize(frame)
        cv2.imshow('video', img)
        server.sendImage(img)


# 图像接收方
def clientTest():
    client = TCPClient('192.168.0.106', 123)
    thread_getMessage = threading.Thread(target=client.getAndInferImage)
    thread_getMessage.setDaemon(True)
    thread_getMessage.start()
    while True:
        continue

if __name__ == '__main__':
    serverTest()
    # clientTest()
