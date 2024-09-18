# -*- coding: utf-8 -*-
import json
from os.path import isfile


class Data:
    def __init__(self):
        if not isfile("./setup.json"):
            raise Exception(" não encontrei setup.josn")
        with open("./setup.json") as json_file:
            self.data = json.load(json_file)

    def get_id_cam(self):
        return self.data["ID_CAM"]

    def get_time_split_video(self):
        tempo = self.data["TIME_SPLIT_VIDEO_MINU"]
        if isinstance(tempo, int):
            return tempo
        else:
            print("TIME_SPLIT_VIDEO_SEGUND precisa ser um inteiro")
            return 15

    def get_fps(self):
        return self.data["FPS"]

    def get_host_name(self):
        return self.data["FTP_HOSTNAME"]

    def get_user_name(self):
        return self.data["FTP_USERNAME"]

    def get_password(self):
        return self.data["FTP_PASSWORD"]

    def get_rstp(self):
        return self.data["RSTP"]

    def get_encoding(self):
        return self.data["encoding"]

    def get_status_copia_local(self):
        status = self.data["manter_copia_local"]
        if status == 1:
            return True
        else:
            return False
