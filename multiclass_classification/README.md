# YouTube 댓글 감정 분석 모델

## 프로젝트 소개

이 프로젝트는 YouTube 댓글을 크롤링하고, 딥러닝을 활용하여 댓글의 감정을 분석하는 텍스트 분류 모델입니다. 한국어 정치 관련 키워드에 대한 댓글을 수집하고, 긍정/부정/중립으로 감정을 분류합니다.

- **데이터셋**: 한국어 정치 관련 단어 사전 (긍정/부정/중립)
- **모델**: LSTM 기반 감정 분석 모델
- **프레임워크**: TensorFlow, Keras
- **크롤링**: Selenium을 활용한 YouTube 댓글 수집

---

## 프로젝트 구조

```
multiclass_classification/
├── README.md
└── model/
    ├── youtube_crawling.py          # YouTube 댓글 크롤링 스크립트
    ├── model_train.ipynb            # 모델 학습 노트북
    ├── model_test.ipynb             # 모델 테스트 노트북
    ├── emotion_model.h5             # 학습된 모델 파일
    ├── test5.xlsx                   # 테스트 데이터 (Excel)
    ├── pos_pol_word.txt             # 긍정 정치 단어 사전
    ├── neg_pol_word.txt             # 부정 정치 단어 사전
    └── obj_unknown_pol_word.txt     # 중립 정치 단어 사전
```

---

## 데이터셋 구조

### 단어 사전 파일
- **pos_pol_word.txt**: 긍정적 정치 관련 단어들 (감정 레이블: 2)
- **neg_pol_word.txt**: 부정적 정치 관련 단어들 (감정 레이블: 0)  
- **obj_unknown_pol_word.txt**: 중립적 정치 관련 단어들 (감정 레이블: 1)

### 테스트 데이터
- **test5.xlsx**: YouTube에서 크롤링한 댓글 데이터
- 시트명: "한국 저출산" (검색 키워드)
- E열: 댓글 내용

---

## 실행 방법

### 1. 필수 라이브러리 설치
```bash
pip install tensorflow keras openpyxl selenium pandas numpy
pip install beautifulsoup4 webdriver-manager
```

### 2. Chrome WebDriver 설정
```bash
# Chrome WebDriver 자동 설치
pip install webdriver-manager
```

### 3. 데이터 준비
- `model/` 폴더에 단어 사전 파일들이 있는지 확인
- `test5.xlsx` 파일이 올바른 형식으로 준비되어 있는지 확인

### 4. 모델 학습
```bash
# Jupyter Notebook 실행
jupyter notebook model/model_train.ipynb
```

### 5. 모델 테스트
```bash
# 테스트 노트북 실행
jupyter notebook model/model_test.ipynb
```

### 6. YouTube 크롤링 (선택사항)
```bash
cd model
python youtube_crawling.py
```

---

## 감정 분류 클래스

- **0**: 부정 (Negative)
- **1**: 중립 (Neutral)  
- **2**: 긍정 (Positive)

---

## 주요 코드/구조

### 데이터 전처리
- **토크나이저**: `Tokenizer(num_words=10000, oov_token='<OOV>')`
- **시퀀스 변환**: `texts_to_sequences()`
- **패딩**: `pad_sequences(maxlen=10, padding='post', truncating='post')`

### 모델 아키텍처
```python
Sequential([
    Embedding(10000, 16, input_length=10),
    LSTM(32),
    Dense(16, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')  # 3개 클래스 분류
])
```

### 크롤링 기능
- **Selenium WebDriver**: YouTube 댓글 자동 수집
- **BeautifulSoup**: HTML 파싱
- **Excel 저장**: 수집된 데이터를 Excel 파일로 저장

---

### 발견된 문제점

1. **데이터 불균형**
   - 긍정/부정/중립 단어 수의 불균형
   - 실제 댓글과 학습 데이터의 분포 차이

2. **모델 성능**
   - 단순한 LSTM 구조로 인한 성능 한계
   - 과적합 가능성 (Dropout만으로는 부족)

3. **전처리 개선 필요**
   - 한국어 특화 전처리 부족
   - 이모지, 특수문자 처리 미흡

4. **평가 지표 부족**
   - 정확도 외의 세밀한 평가 지표 없음
   - 교차 검증 미실행

## 참고/응용

- **정치 댓글 분석**: 특정 정치 이슈에 대한 여론 분석
- **브랜드 모니터링**: 제품/서비스에 대한 고객 반응 분석
- **소셜 미디어 분석**: 트위터, 인스타그램 등 다양한 플랫폼 확장 가능
- **실시간 감정 분석**: 스트리밍 데이터에 대한 실시간 분석 시스템 구축