# photocup-server-ai
### 22-2 photocup ai 정리
## Object Detect & Classify Process
Mobile 로부터 전송받은 사진의 Class를 판단하는 과정에는 사진 속 다양한 객체를 검출하는 Detect 과정과 검출된 객체 중 어떠한 객체를 Class로 판단할지 선택하는
Classify 과정으로 나뉜다.
## Detect 과정
사진 내의 객체를 검출히가 위한 과정이다. 현재 선정한 Object Detection Model 은 OpenCV에서 활용할 수 있는 YoloV3 Model 이다. 위 모델을 선정한 이유는, OpenCV와
미리 학습된 YOLO weight 파일을 이용해 gpu가 갖춰지지 않은 서버 상에서도 Object Detection을 진행할 수 있다는 강점이 있었고, 검출해내는 객체의 종류가 80여가지가 
되어 본 서비스가 분류할 수 있는 객체의 가짓수가 매우 다양해 질 수 있다는 점에서 적합하다고 판단하였다.

![image](https://user-images.githubusercontent.com/39343594/231322329-6ff6f5c8-b55b-4f70-97fe-61501300f3de.png)

다음 표는 YOLO 에서 검출할 수 있는 객체들과 그 객체들을 굵직한 카테고리로 묶은 표이다. input으로 들어간 사진에서 표 내의 객체들을 검출하여 총 16개의 Class로 분류한다.

## Classify 과정
사진 내의 Object 들을 검출 한 후, 다양한 객체가 검출된 경우, 해당 사진의 Class가 어떤 객체에 해당하는지 판단해줄 필요가 있다.

![image](https://user-images.githubusercontent.com/39343594/231322542-2c6a0559-794e-4a73-a486-86c1d631d6da.png)

다음 사진에서는 Dog와 Person 이라는 객체가 검출되었다. 해당 사진을 Classify 하고자 할 때, Main Class를 Dog로 할지, Person으로 할지 판단해주는 알고리즘이 필요하다.
이에 사용되는 핵심기술은 FCOS[1] Object Detection Model 에서 기술한 Centerness Weight이다.

### Centerness Weight
FCOS MODEL 에서 사용한 Center-ness의 직관은 사진의 중심부로부터 거리가 멀 경우, 해당 사진이 주로 표현하는 객체와는 연관성이 떨어진다는 점에서 시작하였다.
이를 Object Detection에 적용하기 위해, 각 픽셀별 classification score에 앞서 설명한 가중치 center-ness 값을 곱하여 중심부와 더 가까운 객체를 주로 인식하게 하였다.

![image](https://user-images.githubusercontent.com/39343594/231323130-ab535377-d27f-4b70-b357-ec027c74c08c.png)
![image](https://user-images.githubusercontent.com/39343594/231323285-1b5977e8-4393-48cd-af68-b3a6787f01c2.png)

FCOS에서 사용한 centerness 계산식은 다음과 같다. 위 식을 통해 centerness의 값은 0~1 값을 갖고, 기준점이 객체의 정중앙으로부터 멀어질수록 centerness 값은 0으로
수렴하게 된다.
이를 우리의 프로젝트에 적용시키면 사진의 정중앙으로부터 거리가 먼 객체일수록 해당 사진의 Main Class와는 거리가 멀다 라는 직관이 된다. 따라서 우리는 검출된 객체의 
정중앙을 기준점으로 잡고,
    왼쪽테두리 - 기준점 = l
    오른쪽테두리 - 기준점 = r 
    상단테두리 - 기준점 = t
    하단테두리 - 기준점 = b
로 변수를 지정하여 centerness를 계산한다.
그 뒤, 검출된 객체들의 centerness를 비교하여 가장 높은 값의 centerness를 지닌 객체를 Main Class로 선정한다.
해당 기능은 Object Detection Process 중, Object Detection Model을 통해 객체 검출을 한 뒤, Main Class를 판단하기 위한 Process로 추가된다.


참고문헌:

[1] Tian, Zhi, et al. "Fcos: Fully convolutional one-stage object detection." Proceedings of the IEEE/CVF international conference on computer vision. 2019.
