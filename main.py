# -*- coding: utf-8 -*-
import cv2
import shutil
from logging import getLogger
from collections import deque
from cloud import MyFTP
import numpy as np
import datetime
from config import Data
from salve_video import Video
from cam import CriateCamera
from utils import default_log
import os

__version__ = "0.0.3"
os.environ["__VERSION__"] = __version__
default_log()
log = getLogger(__name__)
if not os.path.isdir("videos"):
    os.mkdir("videos")
os.makedirs("videos", exist_ok=True)
os.makedirs("upload", exist_ok=True)
config_data = Data()


def nothing(x):
    pass


name_janela = f"videCapture {__version__}"
cv2.namedWindow(name_janela, cv2.WINDOW_NORMAL)
bg = cv2.createBackgroundSubtractorMOG2(history=100, detectShadows=False)
cv2.createTrackbar("Sensibilidade", "janela", 1, 25, nothing)

FPS = config_data.get_fps()
TIME_SPLIT_VIDEO_MINU = config_data.get_time_split_video()


def new_name_video():
    name_video = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return config_data.get_id_cam() + "_" + name_video


list_movi = deque(maxlen=40)


def movimento(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, None, 0.4, 0.4)
    fundo = bg.apply(gray)
    fundo = cv2.medianBlur(fundo, 7)
    list_movi.append(int(np.sum(fundo)))
    total = int(np.mean(list_movi)) + 2
    return total


salve_video = Video(fps=FPS, format="mp4", out_name=os.path.join("videos", new_name_video()))


cam = CriateCamera()
cam.set_started_processo(True)
serve_cloud = MyFTP()
if serve_cloud.connect():
    serve_cloud.start()
counter_frame = 0
while True:
    img = cam.read_frame()
    if img is None:
        continue

    valor = cv2.getTrackbarPos("Sensibilidade", "janela")
    valor_bar = int(np.exp(valor))

    total = movimento(img)
    if total > valor_bar:
        salve_video.write_frame(img)
        cv2.putText(img, "gravando", (180, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)

    if valor_bar < 2:
        cv2.putText(img, "continuo", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(img, "stop", (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow(name_janela, cv2.resize(img, None, None, 0.4, 0.4))  # img = cv2.flip(img)

    if TIME_SPLIT_VIDEO_MINU * 10 < counter_frame // FPS:
        log.info("novo video")
        salve_video.close()
        path = salve_video.get_path_out()
        out = os.path.join("upload", os.path.basename(path))
        try:
            shutil.move(path, out)
        except Exception as error:
            log.error(error, exc_info=error)

        salve_video.set_name_out(os.path.join("videos", new_name_video()))

        if not serve_cloud.is_alive():
            serve_cloud = MyFTP()
            if serve_cloud.connect():
                serve_cloud.start()

        counter_frame = 0
    counter_frame += 1

    k = cv2.waitKey(FPS)
    if k == ord("q"):
        salve_video.close()
        cv2.destroyAllWindows()
        break
