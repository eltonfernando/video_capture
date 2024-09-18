# -*- coding: utf-8 -*-

"""
Autor: Elton fernandes dos Santos

ob = Video()
ob.write_frame(frame)
# novo video
ob.set_name_out("novo")
"""
import cv2


class Video:
    def __init__(self, format="avi", fps=15, out_name="saida"):
        self.format = format
        self.fps = fps
        self.out_name = out_name
        self.fourcc = None
        self.ob_write = None
        self.set_fourcc()

    def get_path_out(self):
        return self.out_name

    def set_name_out(self, name_out):
        self.ob_write = None
        self.out_name = name_out
        self.set_fourcc()

    def set_fourcc(self):
        self.out_name += "." + self.format
        if self.format == "avi":
            self.fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
        if self.format == "mp4":
            self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    def write_frame(self, frame):
        if self.ob_write is None:
            self.ob_write = cv2.VideoWriter(self.out_name, self.fourcc, self.fps, (frame.shape[1], frame.shape[0]), True)
        else:
            self.ob_write.write(frame)

    def close(self):
        self.ob_write.release()


if __name__ == "__main__":
    "teste"
    cap = cv2.VideoCapture(0)

    vs = Video()
    while cap.isOpened():

        _, frame = cap.read()
        cv2.imshow("janela", frame)
        vs.write_frame(frame)
        k = cv2.waitKey(30)
        if k == ord("q"):
            vs.close()
            break
