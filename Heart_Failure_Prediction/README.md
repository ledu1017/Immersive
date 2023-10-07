# Heart Disease Prediction with Machine Learning

## 프로젝트 소개

이 프로젝트는 심장병 진단 데이터를 활용하여 다양한 머신러닝 분류 알고리즘의 성능을 비교하고, 최적의 예측 모델을 찾는 것을 목적으로 합니다. 5가지 주요 분류 알고리즘을 사용하여 심장병 위험도를 예측하고, 특성 중요도 분석을 통해 핵심 변수를 도출합니다.

- **데이터셋**: 심장병 진단 데이터, 총 920개 레코드, 12개 특성
- **모델**: SVM, Decision Tree, KNN, Logistic Regression, Random Forest
- **프레임워크**: Scikit-learn, Pandas, NumPy

---

## 데이터셋 구조

```
Heart_Failure_Prediction/
├── heart.csv                    # 심장병 진단 데이터셋
├── HeartDisease.py             # Python 스크립트 버전
├── HeartDisease.ipynb          # Jupyter Notebook 버전
├── README.md                   # 프로젝트 설명서
└── .ipynb_checkpoints/         # Jupyter 체크포인트 파일들
```

### 데이터 특성 설명

| 특성명 | 설명 | 값 |
|--------|------|-----|
| Age | 나이 | 연령 |
| Sex | 성별 | M(남성), F(여성) |
| ChestPainType | 흉통 유형 | ATA, NAP, ASY, TA |
| RestingBP | 안정 시 혈압 | mmHg |
| Cholesterol | 콜레스테롤 | mg/dl |
| FastingBS | 공복 혈당 | 0(≤120), 1(>120) |
| RestingECG | 안정 시 심전도 | Normal, ST, LVH |
| MaxHR | 최대 심박수 | bpm |
| ExerciseAngina | 운동성 협심증 | N(No), Y(Yes) |
| Oldpeak | ST 분절 하강 | mm |
| ST_Slope | ST 분절 기울기 | Up, Flat, Down |
| HeartDisease | 심장병 여부 | 0(No), 1(Yes) |

---

## 실행 방법

1. **필수 라이브러리 설치**
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn
   ```

2. **데이터 준비**
   - `heart.csv` 파일이 프로젝트 루트 디렉토리에 있는지 확인하세요.

3. **코드 실행**
   - **Python 스크립트**: `python HeartDisease.py`
   - **Jupyter Notebook**: `jupyter notebook HeartDisease.ipynb`
   - 각 셀을 순서대로 실행하면 데이터 전처리, 모델 학습, 성능 비교, 결과 시각화가 진행됩니다.

---

## 지원하는 머신러닝 모델

- Support Vector Machine (SVM)
- Decision Tree Classifier
- K-Nearest Neighbors (KNN)
- Logistic Regression
- Random Forest Classifier

---

## 주요 코드/구조

- **데이터 전처리**: 범주형 변수 인코딩, 데이터 분할 (훈련:테스트 = 8:2)
- **모델 훈련 및 평가**: 개별 모델 성능 측정, 교차 검증(5-fold)을 통한 안정적인 성능 평가
- **특성 분석**: Random Forest를 통한 특성 중요도 계산, 상위 5개 특성 도출
- **데이터 정규화**: MinMaxScaler를 사용한 특성 정규화, 정규화 전후 성능 비교

---

## 결과 예시

### 모델 성능 비교 (5-fold 교차 검증)
```
SVM: 85.43%
DecisionTreeClassifier: 82.61%
KNeighborsClassifier: 84.78%
LogisticRegression: 86.96%
RandomForestClassifier: 88.04%
```

### 특성 중요도 (상위 5개)
1. MaxHR (최대 심박수) - 0.284
2. Oldpeak (ST 분절 하강) - 0.198
3. Age (나이) - 0.167
4. RestingBP (안정 시 혈압) - 0.145
5. Cholesterol (콜레스테롤) - 0.134

### 데이터 분포
- **심장병 없음**: 508명 (55.2%)
- **심장병 있음**: 412명 (44.8%)

### 주요 발견사항
- Random Forest가 가장 높은 정확도(88.04%)를 보임
- 최대 심박수(MaxHR)가 심장병 예측에 가장 중요한 특성
- 상위 5개 특성만으로도 충분한 예측 성능 달성 가능

---

## 참고/응용

- 다양한 분류 알고리즘의 성능 비교 및 벤치마킹 실습에 적합
- 의료 데이터 분석, 특성 선택, 모델 최적화 등 연구/실습에 활용 가능
- **주의**: 이 프로젝트는 교육 목적으로 제작되었으며, 실제 의료 진단에는 사용하지 마세요. 