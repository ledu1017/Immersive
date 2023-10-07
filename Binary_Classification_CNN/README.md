# Pneumonia Detection with Convolutional Neural Networks

## 프로젝트 소개

이 프로젝트는 흉부 X-ray 이미지를 분석하여 폐렴(pneumonia)과 정상(normal) 상태를 분류하는 딥러닝 기반의 의료 영상 진단 모델을 구현합니다. CNN(Convolutional Neural Network)을 활용하여 의료진의 진단을 보조하는 AI 시스템을 구축하는 것이 목적입니다.

- **데이터셋**: 흉부 X-ray 이미지 (정상/폐렴 이진 분류)
- **모델**: 커스텀 CNN 아키텍처
- **프레임워크**: TensorFlow, Keras
- **배포**: TensorFlow.js를 활용한 웹 기반 추론 시스템

---

## 데이터셋 구조

```
dataset/
├── train/
│   ├── normal/
│   └── pneumonia/
├── test/
│   ├── normal/
│   └── pneumonia/
└── val/
    ├── normal/
    └── pneumonia/
```

- 각 폴더에는 해당 클래스의 X-ray 이미지가 포함되어 있습니다.
- 정상(normal)과 폐렴(pneumonia) 두 가지 클래스로 구성됩니다.

---

## 실행 방법

1. **필수 라이브러리 설치**
   ```bash
   pip install tensorflow keras opencv-python pillow numpy matplotlib scikit-learn
   ```

2. **모델 학습**
   - `model/pneumonia_model.ipynb` 파일을 Jupyter Notebook에서 실행하세요.
   - 데이터 전처리, 모델 학습, 평가 과정이 순차적으로 진행됩니다.

3. **웹 애플리케이션 실행**
   - `index.html` 파일을 웹 브라우저에서 열어주세요.
   - TensorFlow.js를 통해 학습된 모델을 로드하고 실시간 추론을 수행할 수 있습니다.

---

## 지원하는 분류 클래스

- **Normal**: 정상 흉부 X-ray
- **Pneumonia**: 폐렴이 의심되는 흉부 X-ray

---

## 주요 코드/구조

- **데이터 전처리**: 이미지 리사이징, 정규화, 데이터 증강
- **모델 구조**: 커스텀 CNN 아키텍처 (Conv2D, MaxPooling2D, Dense 레이어)
- **학습 및 평가**: 조기 종료(Early Stopping), 모델 체크포인트, 성능 지표 측정
- **웹 배포**: TensorFlow.js를 활용한 브라우저 기반 추론

---

## 파일 구조

```
├── README.md
├── index.html              # 웹 애플리케이션 메인 페이지
├── predict.js              # TensorFlow.js 추론 로직
├── model.json              # 모델 아키텍처 정보
├── model/
│   ├── pneumonia_model.ipynb  # 모델 학습 노트북
│   ├── pneumonia_model.h5     # 학습된 모델 가중치
│   └── model_json/           # TensorFlow.js 모델 파일들
└── dataset/                # 데이터셋 디렉토리
    ├── train/
    ├── test/
    └── val/
```

---

## 웹 애플리케이션 사용법

1. 웹 브라우저에서 `index.html` 파일을 엽니다.
2. "Choose File" 버튼을 클릭하여 X-ray 이미지를 업로드합니다.
3. "Predict" 버튼을 클릭하여 분석을 시작합니다.
4. 결과가 화면에 표시됩니다:
   - **정상**: "이 이미지는 정상(normal)일 가능성이 있습니다."
   - **폐렴**: "이 이미지는 폐렴(pneumonia)일 가능성이 있습니다."

---

## 모델 성능

- **처리 속도**: 실시간 추론 가능
- **배포**: 웹 브라우저에서 즉시 사용 가능

---

## 참고/응용

- CNN을 활용한 이미지 분류 모델 설계 실습
- TensorFlow.js를 통한 웹 기반 AI 모델 배포 학습
- 의료 AI 시스템의 실제 구현 사례