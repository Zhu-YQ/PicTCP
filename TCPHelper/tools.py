import cv2


def log(info):
    print('LOG: ' + info)

def resize(img):
    height, width = img.shape[0:2]
    target_height = 400
    target_width = int(width * (target_height / height))
    img = cv2.resize(img, (target_width, target_height))
    return img