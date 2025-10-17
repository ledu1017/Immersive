# 스마트폰 센서 데이터 기반 모션 분류

## 프로젝트 소개

이 프로젝트는 스마트폰의 가속도계(Accelerometer)와 자이로스코프(Gyroscope) 센서 데이터를 활용하여 사용자의 모션을 분류하는 머신러닝 모델입니다. 다양한 센서 특성값을 추출하고 여러 알고리즘을 비교하여 최적의 모션 분류 성능을 달성합니다.

- **데이터셋**: 스마트폰 센서 데이터 (가속도계, 자이로스코프)
- **모델**: RandomForest, Neural Network 등 다양한 분류 모델
- **프레임워크**: scikit-learn, TensorFlow/Keras
- **특성**: 561개의 센서 특성값 (시간 도메인, 주파수 도메인)

---

## 프로젝트 구조

```
smartphone_sensor_sata_based_motion _classification/
├── README.md
├── README_sample.md
├── data_analysis.ipynb           # 데이터 탐색 및 분석
├── modeling.ipynb                # 통합 모델링
└── modeling_by_step.ipynb        # 단계별 모델링
```

---

## 데이터셋 구조

### 센서 데이터 특성
- **가속도계 데이터**: 3축 가속도 센서 데이터 (X, Y, Z)
- **자이로스코프 데이터**: 3축 각속도 센서 데이터 (X, Y, Z)
- **특성 개수**: 561개 (시간 도메인 + 주파수 도메인 특성)
- **주요 특성 그룹**:
  - `tBodyAcc-*`: 신체 가속도 (시간 도메인)
  - `tGravityAcc-*`: 중력 가속도 (시간 도메인)
  - `tBodyGyro-*`: 신체 자이로스코프 (시간 도메인)
  - `fBodyAcc-*`: 신체 가속도 (주파수 도메인)
  - `fBodyGyro-*`: 신체 자이로스코프 (주파수 도메인)

### 모션 클래스
사용자의 다양한 활동을 분류하는 목표 변수:
- **WALKING**: 걷기
- **WALKING_UPSTAIRS**: 계단 오르기
- **WALKING_DOWNSTAIRS**: 계단 내려가기
- **SITTING**: 앉기
- **STANDING**: 서기
- **LAYING**: 누워있기

---

## 실행 방법

### 1. 필수 라이브러리 설치
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
pip install tensorflow keras joblib tqdm
```

### 2. 데이터 준비
- Google Colab 환경에서 실행 (Google Drive 연동)
- 센서 데이터 파일이 올바른 경로에 위치하는지 확인

### 3. 데이터 분석
```bash
# 데이터 탐색 및 분석
jupyter notebook data_analysis.ipynb
```

### 4. 모델 학습 및 평가
```bash
# 통합 모델링
jupyter notebook modeling.ipynb

# 단계별 모델링
jupyter notebook modeling_by_step.ipynb
```

---

## 주요 분석 과정

### 1. 데이터 탐색 (data_analysis.ipynb)
- **기본 정보 확인**: 데이터 형태, 결측치 확인
- **목표 변수 분석**: 모션 클래스별 분포 확인
- **센서 특성 분석**: 561개 특성의 분포 및 상관관계 분석
- **특성 그룹화**: 센서 타입별, 집계 방식별 특성 분류

### 2. 모델링 (modeling.ipynb, modeling_by_step.ipynb)
- **특성 선택**: 중요도 기반 특성 선택
- **데이터 전처리**: 
  - Label Encoding (목표 변수)
  - Train/Validation 분할 (8:2 비율)
  - MinMax Scaling
- **모델 학습**: 다양한 알고리즘 비교
- **성능 평가**: 정확도, 분류 리포트 등

---

## 사용된 알고리즘

### 1. Random Forest
- 앙상블 기반 분류 알고리즘
- 특성 중요도 분석 가능
- 과적합 방지 효과

### 2. Neural Network (TensorFlow/Keras)
```python
Sequential([
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(6, activation='softmax')  # 6개 모션 클래스
])
```

---

## 특성 중요도 분석

프로젝트에서는 특성 중요도를 분석하여 모델 성능에 기여하는 주요 센서 특성을 식별합니다:

```python
def plot_feature_importance(importance, names, result_only=False, topn='all'):
    # 특성 중요도 시각화 및 분석
```

### 주요 특성들
- `tGravityAcc-min()-X`, `tGravityAcc-min()-Y`: 중력 가속도 최솟값
- `tGravityAcc-energy()-X`: 중력 가속도 에너지
- `angle(X,gravityMean)`, `angle(Y,gravityMean)`: 중력 벡터와의 각도
- `tBodyAcc-max()-X`: 신체 가속도 최댓값

---

## 모델 성능

### 평가 지표
- **정확도 (Accuracy)**: 전체 분류 정확도
- **분류 리포트**: 클래스별 정밀도, 재현율, F1-score
- **혼동 행렬**: 클래스별 분류 결과 시각화

### 예상 성능
- Random Forest: 높은 정확도와 안정성
- Neural Network: 복잡한 패턴 학습 가능
- 특성 선택을 통한 성능 최적화