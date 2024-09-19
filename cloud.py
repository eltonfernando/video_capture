# -*- coding: utf-8 -*-
from logging import getLogger
from config import Data
import ftplib
import os
from threading import Thread
from glob import glob


class MyFTP(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.log = getLogger(__name__)
        self.log.info("criando th ftp")

    def run(self) -> None:
        list_videos = glob(os.path.join("upload", "*.mp4"))
        if len(list_videos) == 0:
            self.log.info("sem video para enviar")
            return
        for path_video in list_videos:
            self.log.info(f"enviando.. {path_video}")
            self.write_remote_file(path_video)
        self.ftp_server.close()

    def connect(self):
        conf_data = Data()
        HOSTNAME = conf_data.get_host_name()
        USERNAME = conf_data.get_user_name()
        PASSWORD = conf_data.get_password()
        try:
            self.ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            self.ftp_server.encoding = conf_data.get_encoding()
            self.ftp_server.cwd("dataset")
            return True
        except Exception as e:
            print(e)
            return False

    def write_remote_file(self, local_file):

        if not os.path.isfile(local_file):
            self.log.info(f"não encontrou arquivo {local_file}")
            return
        filename = os.path.basename(local_file)
        self.log.info(self.ftp_server.pwd())

        with open(local_file, "rb") as file:
            self.ftp_server.storbinary(f"STOR {filename}", file)
        self.log.info(f"uploud concluido")
        if Data().get_status_copia_local() == 0:
            os.remove(local_file)


if __name__ == "__main__":
    t = MyFTP()
    t.connect()
    t.start()
    print(t.is_alive())
    t.join()
