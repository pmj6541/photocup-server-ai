import cv2
import numpy as np
import sys
import PhotoConverter
import Classify, Detect, PhotoConverter
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/ObjectDetect", method=['GET']
def ObjectDetect():
    #file read from args
    imgList = []
    imginput = request.json

    for i in range(10):
        filename = imginput['source']
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        imgList.append(img)

# 객체 검출 함수
    detectedInfos, imgShapeList = Detect.detect(imgList)

# Main Class 판별 함수
    mains = Classify.classify(imgShapeList,detectedInfos)

#main content 시각화
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(mains)) :
        main_label, main_x, main_y, main_w, main_h, color = mains[i]
        cv2.rectangle(imgList[i], (main_x, main_y), (main_x + main_w, main_y + main_h), color, 2)
        cv2.putText(imgList[i], "Main Class : "+main_label, (30,60), font, 3, color, 3)
        cv2.imwrite(f"res/res{i}.jpg", imgList[i])
        reponse = {
            'lable' : main_label
        }
    print("Every Process is Succesfully Done!")
    return jsonify(response), 200

if __name__ == '__main__':
    app.run()