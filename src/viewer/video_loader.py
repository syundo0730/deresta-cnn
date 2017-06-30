import cv2


class VideoLoader:
    def __init__(self, video_file_name):
        self.video_file_name = video_file_name
        self.capture = None
        self.width = 0
        self.height = 0
        self.frame_num = 0
        self.init()

    def get_size(self):
        return self.width, self.height

    def init(self):
        if self.capture is not None and self.capture.isOpened():
            self.capture.release()
        self.capture = cv2.VideoCapture(self.video_file_name)
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_num = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)

    # def read(self):
    #     if self.capture is not None and self.capture.isOpened():
    #         ret, frame = self.capture.read()
    #         if not ret:
    #             return None, 0
    #         time = self.capture.get(cv2.CAP_PROP_POS_MSEC)
    #         return frame, time
    #     else:
    #         return None, 0
