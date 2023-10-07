# Autoencoder-based Anomaly Detection Project

## 프로젝트 소개

이 프로젝트는 **자동인코더(Autoencoder)**를 사용하여 금융 거래 데이터에서 이상치(Anomaly)를 탐지하는 딥러닝 모델을 구현한 프로젝트입니다. 

- **목적**: 일상적인 거래 패턴과 다른 비정상적인 거래를 자동으로 탐지
- **데이터**: 일별 거래 건수와 거래 금액 데이터 (2023년 1월~4월)
- **모델**: 자동인코더 (Autoencoder) - 비지도 학습 방식
- **프레임워크**: TensorFlow, Keras

---

## 데이터셋 구조

### 데이터 파일: `zezu.csv`
- **기간**: 2023년 1월 1일 ~ 4월 9일 (총 153일)
- **특성**:
  - `승인일자`: 거래 날짜
  - `이용건수_전체`: 전체 거래 건수
  - `이용금액_전체`: 전체 거래 금액
  - `이용건수_정상`: 정상 거래 건수
  - `이용금액_정상`: 정상 거래 금액
  - `이용건수_이상`: 이상 거래 건수
  - `이용금액_이상`: 이상 거래 금액

### 데이터 전처리 과정
1. **이상치 탐지**: IQR(Interquartile Range) 방법을 사용하여 이상치 식별
2. **레이블 생성**: 이상치로 판단된 데이터에 레이블 1, 정상 데이터에 레이블 0 부여
3. **데이터 정규화**: StandardScaler를 사용하여 특성 스케일링

---

## 모델 구조

### 자동인코더 아키텍처
```
입력층 (2차원) → 인코더 → 잠재층 (14차원) → 디코더 → 출력층 (2차원)
```

- **입력층**: 2개 특성 (이용건수_전체, 이용금액_전체)
- **인코더**: 
  - Dense(14, activation='tanh') + L1 정규화
  - Dense(7, activation='relu')
- **디코더**:
  - Dense(7, activation='tanh')
  - Dense(2, activation='relu')

### 학습 설정
- **옵티마이저**: Adam
- **손실 함수**: Mean Squared Error (MSE)
- **배치 크기**: 32
- **에포크**: 50
- **검증 데이터**: 20% 분할

---

## 실행 방법

### 1. 환경 설정
```bash
pip install tensorflow keras pandas numpy matplotlib seaborn scikit-learn
```

### 2. 데이터 준비
- `zezu.csv` 파일이 프로젝트 루트 디렉토리에 있어야 합니다.

### 3. 모델 학습
```bash
python model_train.py
```

### 4. Jupyter Notebook 실행 (권장)
```bash
jupyter notebook model_train.ipynb
```

---

## 주요 기능

### 1. 데이터 분석 및 시각화
- 거래 패턴 분석
- 이상치 탐지 및 시각화
- 정상/이상 데이터 분포 비교

### 2. 자동인코더 모델
- 비지도 학습을 통한 정상 패턴 학습
- 재구성 오차를 통한 이상치 탐지

### 3. 실시간 이상치 탐지
```python
# 예시 사용법
transaction_volume = 230.0  # 거래량
transaction_cost = 8200.0   # 거래금액

# 모델 예측
reconstruction_error = model.predict(scaled_data)
if reconstruction_error > threshold:
    print("이상치로 판단됨")
else:
    print("정상 거래")
```

---

## 결과 및 성능

### 학습 과정
- **모델 저장**: `model.h5` 파일로 최적 모델 저장
- **로그 기록**: TensorBoard를 통한 학습 과정 모니터링
- **손실 그래프**: 학습/검증 손실 시각화

### 이상치 탐지 결과
- 정상 거래 패턴을 학습하여 비정상적인 거래를 탐지
- 재구성 오차가 임계값을 초과하는 경우를 이상치로 판단

---

## 개선 가능한 부분

### 1. 데이터 품질 개선
- **인코딩 문제**: CSV 파일의 한글 인코딩 문제 해결 필요
- **데이터 검증**: 더 많은 데이터 검증 및 전처리 단계 추가
- **특성 엔지니어링**: 추가적인 특성 생성 고려

### 2. 모델 성능 향상
- **하이퍼파라미터 튜닝**: 더 체계적인 하이퍼파라미터 최적화
- **앙상블 방법**: 여러 모델의 조합을 통한 성능 향상
- **다양한 아키텍처**: LSTM, Transformer 등 다른 모델 구조 시도

### 3. 평가 지표 개선
- **정확한 평가**: 실제 이상치 레이블을 사용한 성능 평가
- **다양한 지표**: Precision, Recall, F1-Score 등 추가 지표
- **교차 검증**: K-fold 교차 검증을 통한 안정적인 성능 측정

### 4. 실용성 향상
- **실시간 처리**: 스트리밍 데이터 처리 기능 추가
- **웹 인터페이스**: 사용자 친화적인 웹 대시보드 구축
- **알림 시스템**: 이상치 탐지 시 자동 알림 기능

---

## 파일 구조

```
autoencoder/
├── README.md              # 프로젝트 설명서
├── model_train.py         # 메인 학습 스크립트
├── model_train.ipynb      # Jupyter 노트북
├── model.h5              # 학습된 모델 파일
├── zezu.csv              # 원본 데이터
└── logs/                 # TensorBoard 로그
    ├── train/
    └── validation/
```

---

## 사용된 라이브러리

- **TensorFlow/Keras**: 딥러닝 모델 구현
- **Pandas**: 데이터 처리 및 분석
- **NumPy**: 수치 계산
- **Matplotlib/Seaborn**: 데이터 시각화
- **Scikit-learn**: 데이터 전처리 및 분할