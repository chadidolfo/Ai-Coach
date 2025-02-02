import urllib
import cv2
import time
import Pose as pm
import numpy as np
import sys
import subprocess

class lateralRaise:
    def __init__(self, video_path, user_name):
        self.detector = pm.poseDetector()
        self.pTime = 0
        self.count = 0
        self.dir = 0
        self.form_good = False
        self.percentage = 0
        self.video_path = video_path
        self.user_name = user_name

    def check_form(self, lmList):
        shoulder_angle_threshold = 160
        elbow_angle_threshold = 170

        shoulder_angle = self.calculate_angle(lmList[12], lmList[14], lmList[16])
        elbow_angle = self.calculate_angle(lmList[14], lmList[16], lmList[18])

        shoulder_percentage = min(max((shoulder_angle - 90) / (shoulder_angle_threshold - 90) * 100, 0), 100)
        elbow_percentage = min(max((elbow_angle - 90) / (elbow_angle_threshold - 90) * 100, 0), 100)

        self.percentage = (shoulder_percentage + elbow_percentage) / 2
        self.form_good = (self.percentage >= 75)

        return self.form_good

    def calculate_angle(self, a, b, c):
        a = np.array(a[1:])
        b = np.array(b[1:])
        c = np.array(c[1:])

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360.0 - angle

        return angle

    def draw_text_with_background(self, img, text, pos, font, scale, color, thickness):
        (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
        x, y = pos

        y1, y2 = max(0, y - h - 10), min(img.shape[0], y + 10)
        x1, x2 = max(0, x), min(img.shape[1], x + w + 20)

        if y2 > y1 and x2 > x1:
            sub_img = img[y1:y2, x1:x2]
            black_rect = np.zeros(sub_img.shape, dtype=np.uint8)
            res = cv2.addWeighted(sub_img, 0.7, black_rect, 0.3, 0)
            img[y1:y2, x1:x2] = res

        cv2.putText(img, text, (x + 10, y), font, scale, color, thickness)

    def draw_progress_bar(self, img, percentage):
        height, width = img.shape[:2]
        bar_height = height // 4
        bar_width = width // 50
        start_point = (width - bar_width - 50, height // 10)
        end_point = (start_point[0] + bar_width, start_point[1] + bar_height)

        cv2.rectangle(img, start_point, end_point, (255, 255, 255), 3)
        cv2.rectangle(img, start_point,
                      (start_point[0] + bar_width, start_point[1] + int((bar_height * percentage) / 100)),
                      (255, 255, 255), cv2.FILLED)

        self.draw_text_with_background(img, f'{int(percentage)}%',
                                       (start_point[0] - 50, start_point[1] + bar_height + 30),
                                       cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    def draw_landmarks(self, img, lmList, color):
        keypoints = [12, 14, 16, 11, 13, 15]
        for id in keypoints:
            cx, cy = lmList[id][1], lmList[id][2]
            cv2.circle(img, (cx, cy), 5, color, cv2.FILLED)

    def run(self):
        while True:
            try:
                img_arr = np.array(bytearray(urllib.request.urlopen(self.video_path).read()), dtype=np.uint8)
                img_url = cv2.imdecode(img_arr, -1)
                img_url = cv2.resize(img_url, (1000, 800))

                img = self.detector.findPose(img_url)
                lmList = self.detector.findPosition(img, draw=False)
                if len(lmList) != 0:
                    if self.check_form(lmList):
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    self.draw_landmarks(img, lmList, color)

                    if lmList[14][2] < lmList[12][2]:
                        if self.dir == 0:
                            self.count += 1
                            self.dir = 1
                    elif lmList[14][2] > lmList[12][2]:
                        self.dir = 0

                    self.draw_progress_bar(img, self.percentage)
                    self.draw_text_with_background(img, f"Count: {self.count}", (50, img.shape[0] - 50),
                                                   cv2.FONT_HERSHEY_PLAIN, 2,
                                                   (255, 255, 255), 2)
                    self.draw_text_with_background(img, "Status: UP" if self.dir == 1 else "Status: DOWN",
                                                   (img.shape[1] - 300, img.shape[0] // 2),
                                                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    h, w, _ = img.shape
                    form_status_text = "Form: Good" if self.form_good else "Form: Bad"
                    self.draw_text_with_background(img, form_status_text, (w - 260, h - 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                                   (255, 255, 255), 2)

                cTime = time.time()
                fps = 1 / (cTime - self.pTime)
                self.pTime = cTime
                # Draw Fps
                self.draw_text_with_background(img, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                               (255, 255, 255), 2)
                # Draw Nickname
                self.draw_text_with_background(img, f"Welcome {self.user_name}", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                               (255, 255, 255), 2)
                cv2.imshow("Image", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print(f"Error: {e}")
                break

        cv2.destroyAllWindows()
        subprocess.run(["python", "gui.py"])  # Relaunch the GUI when the window is closed


if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = 'http://192.168.1.29:8080/shot.jpg'
    user_name = sys.argv[2]

    lr = lateralRaise(video_path, user_name)
    lr.run()
