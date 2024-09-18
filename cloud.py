# -*- coding: utf-8 -*-
from config import Data
import ftplib
import os
from threading import Thread
from glob import glob


class MyFTP(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("criando th ftp")

    def run(self) -> None:
        list_videos = glob(os.path.join("upload", "*.mp4"))
        if len(list_videos) == 0:
            print("sem video para enviar")
            return
        for path_video in list_videos:
            print(f"enviando.. {path_video}")
            self.write_remote_file(path_video)
        self.ftp_server.close()

    def connect(self):
        conf_data = Data()
        HOSTNAME = conf_data.get_host_name()
        USERNAME = conf_data.get_user_name()
        PASSWORD = conf_data.get_password()
        self.ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
        self.ftp_server.encoding = conf_data.get_encoding()
        self.ftp_server.cwd("dataset")
        return True

    def write_remote_file(self, local_file):

        if not os.path.isfile(local_file):
            print(f"não encontrou arquivo {local_file}")
            return
        filename = os.path.basename(local_file)
        print(self.ftp_server.pwd())

        with open(local_file, "rb") as file:
            self.ftp_server.storbinary(f"STOR {filename}", file)
        print(f"uploud concluido")
        if Data().get_status_copia_local() == 0:
            os.remove(local_file)


if __name__ == "__main__":
    t = MyFTP()
    t.connect()
    t.start()
    print(t.is_alive())
    t.join()
