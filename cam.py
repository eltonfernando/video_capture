# -*- coding: utf-8 -*-
import cv2
from config import Data
from time import sleep


class CriateCamera(object):
    started_processo = False
    cap = cv2.VideoCapture()

    def __init__(self):
        self.statc_frame = None

    def read_frame(self):
        status: bool = True
        frame = None
        while not self.cap.isOpened():
            print(f"conectando...{Data().get_rstp()}")

            self.cap.open(Data().get_rstp())
            sleep(1)
        if self.cap.isOpened():
            status, frame = self.cap.read()
        if status or not frame is None:
            self.statc_frame = frame
            return frame
        else:
            print("frame static")
            self.cap.release()
            self.cap.open(Data().get_rstp())
            return self.statc_frame

    def set_started_processo(self, is_process: bool):
        if not is_process:
            self.cap.release()
        self.started_processo = is_process

    def is_startecd_processo(self):
        return self.started_processo
