# Knife Detection with Grounding DINO

## 프로젝트 소개

이 프로젝트는 Grounding DINO를 활용하여 실시간으로 칼(나이프)을 감지하는 딥러닝 기반 객체 탐지 시스템을 구현합니다. 웹캠을 통한 실시간 스트리밍과 이미지 기반 탐지 기능을 제공하며, FastAPI를 통한 웹 서비스도 지원합니다.

- **모델**: Grounding DINO (SwinT 기반)
- **탐지 대상**: 칼(나이프) 객체
- **기능**: 실시간 웹캠 스트리밍, 이미지 기반 탐지, 웹 API 서비스
- **프레임워크**: PyTorch, FastAPI, OpenCV

---

## 프로젝트 구조

```
knife_detection/
├── main.py                 # FastAPI 웹 서버 메인 파일
├── video.py               # 웹캠 스트리밍 처리 모듈
├── knife.ipynb            # Grounding DINO 모델 학습 및 추론 노트북
├── image_capture.ipynb    # 웹캠 이미지 캡처 노트북
└── README.md              # 프로젝트 문서
```

---

## 실행 방법

### 1. 필수 라이브러리 설치

```bash
pip install torch torchvision
pip install opencv-python
pip install fastapi uvicorn
pip install pillow numpy matplotlib
pip install groundingdino
pip install roboflow
```

### 2. Grounding DINO 설치

```bash
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO
pip install -e .
```

### 3. 모델 가중치 다운로드

```bash
mkdir weights
cd weights
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```

### 4. 웹 서버 실행

```bash
uvicorn main:app --reload
```

서버가 실행되면 `http://localhost:8000/video`에서 실시간 웹캠 스트리밍을 확인할 수 있습니다.

### 5. 노트북 실행

- `knife.ipynb`: Grounding DINO 모델을 사용한 칼 탐지 실험
- `image_capture.ipynb`: 웹캠을 통한 이미지 캡처 및 저장

---

## 주요 기능

### 실시간 웹캠 스트리밍
- OpenCV를 활용한 실시간 웹캠 스트리밍
- FastAPI를 통한 웹 브라우저에서 접근 가능
- MJPEG 스트리밍 형식 지원

### 객체 탐지
- Grounding DINO 모델을 사용한 정확한 칼 탐지
- 텍스트 프롬프트 기반 탐지 ("knife" 키워드)
- 바운딩 박스 및 신뢰도 점수 표시

### 이미지 처리
- 웹캠을 통한 이미지 캡처
- 배치 이미지 처리 지원
- 다양한 이미지 형식 지원

---

## API 엔드포인트

### GET /video
실시간 웹캠 스트리밍을 제공합니다.

**응답**: MJPEG 스트리밍 비디오

**사용 예시**:
```bash
curl http://localhost:8000/video
```

---

## 모델 설정

### Grounding DINO 설정
- **백본**: SwinT (Swin Transformer)
- **설정 파일**: `GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py`
- **가중치**: `weights/groundingdino_swint_ogc.pth`

### 추론 파라미터
- **box_threshold**: 0.35 (바운딩 박스 임계값)
- **text_threshold**: 0.25 (텍스트 매칭 임계값)
- **탐지 프롬프트**: "knife"

---

## 사용 예시

### Python에서 직접 사용

```python
import cv2
from groundingdino.util.inference import load_model, predict, annotate

# 모델 로드
model = load_model(CONFIG_PATH, WEIGHTS_PATH)

# 이미지 로드
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 추론 실행
boxes, logits, phrases = predict(
    model=model,
    image=image,
    caption="knife",
    box_threshold=0.35,
    text_threshold=0.25
)

# 결과 시각화
annotated_image = annotate(image_source=image, boxes=boxes, logits=logits, phrases=phrases)
```

### 웹 브라우저에서 접근

1. 서버 실행: `uvicorn main:app --reload`
2. 브라우저에서 `http://localhost:8000/video` 접속
3. 실시간 웹캠 스트리밍 확인

---

## 성능 및 정확도

- **탐지 정확도**: Grounding DINO의 높은 정확도 활용
- **실시간 처리**: GPU 가속 지원으로 빠른 추론 속도
- **다양한 환경**: 다양한 조명 조건과 각도에서 탐지 가능

---

## 참고/응용

- **보안 시스템**: 건물 출입구, 공공장소 보안 모니터링
- **산업 안전**: 제조업체에서 위험 도구 탐지
- **교육**: 컴퓨터 비전 및 객체 탐지 학습
- **연구**: Grounding DINO 모델 성능 분석 및 개선

---

## 라이선스

이 프로젝트는 Grounding DINO의 라이선스를 따릅니다. 자세한 내용은 [Grounding DINO GitHub](https://github.com/IDEA-Research/GroundingDINO)를 참조하세요.