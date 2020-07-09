import cv2
from absl import flags, app
from face_detection import predict as face_detection
from hat_classifier import predict as hat_classifier
from gender_reco import predict as gender_reco
from model_hair_loss_level import predict as hair_loss_reco
# import urllib
import numpy as np
from skimage import io

def main(image_url):
    img = io.imread(image_url)
    print(img)
    # req = urllib.urlopen(image_url)
    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # img = cv2.imdecode(arr, -1) # 'Load it as it is'
    cv2.imshow('profile picture', img)
    cv2.waitKey(1000)
    follow=False
    faces = face_detector(img)
    for face in faces:
        cv2.imshow('face detected', face)
        cv2.waitKey(1000)
        is_hat = hat_detector(face)
        if is_hat:
            is_man = gender_detector(face)
            if is_man:
                is_bald = bald_detector(face)
                if is_bald:
                    follow=True
    return follow

def face_detector(image):
    faces = face_detection.predict(image)
    return faces

def hat_detector(image):
    res = hat_classifier.predict(image)
    print(res)
    if res[0][0]<0.8:
        return True
    else:
        print('the user is wearing a hat')
        return False

def gender_detector(image):
    res = gender_reco.predict(image)
    print(res)
    if res[0][0]>0.2:
        return True
    else:
        print('this user is a women')
        return False

def bald_detector(image):
    res = hair_loss_reco.predict(image)
    print(res)
    if res[0][0]<0.95:
        return True
    else:
        print('this user isn\'t bald enough')
        return False

if __name__ == "__main__":
    FLAGS=flags.FLAGS
    flags.DEFINE_string('weights','./face_detection/checkpoints/yolov3_train_8.tf','path to weights')
    flags.DEFINE_string('image_url','https://instagram.fcdg2-1.fna.fbcdn.net/v/t51.2885-19/s150x150/105955417_740153806820758_1293447938380088868_n.jpg?_nc_ht=instagram.fcdg2-1.fna.fbcdn.net&_nc_ohc=VyIHFmKNs2YAX8hURgS&oh=645b18e8b61d00245cbcf1abe4e852a9&oe=5F1F6CCA','')
    app.run(main)
