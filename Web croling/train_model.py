import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import re
import warnings
warnings.filterwarnings('ignore')

# ✅ 1. 간단한 텍스트 전처리 (konlpy 없이)
def simple_preprocess(text):
    """한글, 영문, 숫자만 유지"""
    if pd.isna(text):
        return ""
    
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', str(text))
    
    # 특수문자 제거 (한글, 영문, 숫자, 공백만 유지)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    
    # 연속 공백 제거
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# ✅ 2. 감성 키워드 카운트
def count_sentiment_keywords(text):
    """긍정/부정 키워드 개수"""
    text_lower = str(text).lower()
    
    positive_keywords = [
        '상승', '증가', '성장', '호조', '개선', '확대', '신기록', '최고',
        '매출증가', '이익증가', '실적개선', '수주', '계약', '협력',
        '투자', '개발', '출시', '성공', '달성', '돌파', '호실적', '급등'
    ]
    
    negative_keywords = [
        '하락', '감소', '악화', '부진', '적자', '손실', '위기', '리스크',
        '지연', '철수', '중단', '실패', '부족', '우려', '하향', '감원',
        '소송', '제재', '규제', '조사', '적발', '급락', '폭락'
    ]
    
    pos_count = sum(1 for kw in positive_keywords if kw in text_lower)
    neg_count = sum(1 for kw in negative_keywords if kw in text_lower)
    
    return pos_count, neg_count

# ✅ 3. 감성 분석 모델 학습
def train_sentiment_model(train_file='train_dataset.csv'):
    """감성 분석 모델 학습"""
    
    print("="*60)
    print("📚 감성 분석 모델 학습 시작")
    print("="*60)
    
    # 데이터 로딩
    print("\n📥 학습 데이터 로딩...")
    df = pd.read_csv(train_file, encoding='utf-8-sig')
    
    print(f"✅ 데이터 크기: {len(df)}개")
    print(f"\n📊 레이블 분포:\n{df['감성레이블'].value_counts()}\n")
    
    # 텍스트 전처리
    print("🔧 텍스트 전처리 중...")
    df['제목'] = df['제목'].fillna('')
    df['본문요약'] = df['본문요약'].fillna('')
    
    # 제목 + 본문 결합
    df['combined_text'] = df['제목'] + ' ' + df['본문요약']
    df['cleaned_text'] = df['combined_text'].apply(simple_preprocess)
    
    # 감성 키워드 카운트
    print("📝 감성 키워드 분석 중...")
    df[['pos_count', 'neg_count']] = df['cleaned_text'].apply(
        lambda x: pd.Series(count_sentiment_keywords(x))
    )
    
    # TF-IDF 벡터화
    print("🔢 TF-IDF 벡터화...")
    vectorizer = TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    
    X_tfidf = vectorizer.fit_transform(df['cleaned_text'])
    
    # 추가 특징과 결합
    X_extra = df[['pos_count', 'neg_count', '3일수익률']].fillna(0).values
    X = np.hstack([X_tfidf.toarray(), X_extra])
    
    y = df['감성레이블']
    
    # 학습/검증 분리
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n🎯 모델 학습 시작...")
    print(f"   학습 데이터: {len(X_train)}개")
    print(f"   검증 데이터: {len(X_val)}개")
    
    # 랜덤 포레스트 학습
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # 평가
    train_score = model.score(X_train, y_train)
    val_score = model.score(X_val, y_val)
    
    print(f"\n{'='*60}")
    print(f"✅ 감성 분석 모델 학습 완료!")
    print(f"   학습 정확도: {train_score:.3f}")
    print(f"   검증 정확도: {val_score:.3f}")
    print(f"{'='*60}")
    
    # 상세 평가
    y_pred = model.predict(X_val)
    print("\n📊 검증 데이터 평가:")
    print(classification_report(y_val, y_pred))
    
    # 모델 저장
    joblib.dump(model, 'sentiment_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    
    print("\n💾 모델 저장 완료:")
    print("   - sentiment_model.pkl")
    print("   - tfidf_vectorizer.pkl")
    
    return model, vectorizer

# ✅ 4. 매매 신호 예측 모델
def train_trading_model(train_file='train_dataset.csv'):
    """매수/매도/관망 예측 모델"""
    
    print("\n" + "="*60)
    print("📈 매매 신호 예측 모델 학습 시작")
    print("="*60)
    
    df = pd.read_csv(train_file, encoding='utf-8-sig')
    
    # 텍스트 전처리
    df['제목'] = df['제목'].fillna('')
    df['본문요약'] = df['본문요약'].fillna('')
    df['combined_text'] = df['제목'] + ' ' + df['본문요약']
    df['cleaned_text'] = df['combined_text'].apply(simple_preprocess)
    
    df[['pos_count', 'neg_count']] = df['cleaned_text'].apply(
        lambda x: pd.Series(count_sentiment_keywords(x))
    )
    
    # 벡터화
    vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
    X_tfidf = vectorizer.fit_transform(df['cleaned_text'])
    
    # 추가 특징
    X_extra = df[['pos_count', 'neg_count', '3일수익률']].fillna(0).values
    X = np.hstack([X_tfidf.toarray(), X_extra])
    
    y = df['거래신호']
    
    # 학습
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # 평가
    train_score = model.score(X_train, y_train)
    val_score = model.score(X_val, y_val)
    
    print(f"\n✅ 매매 모델 학습 완료!")
    print(f"   학습 정확도: {train_score:.3f}")
    print(f"   검증 정확도: {val_score:.3f}")
    
    y_pred = model.predict(X_val)
    print("\n📊 검증 데이터 평가:")
    print(classification_report(y_val, y_pred))
    
    # 저장
    joblib.dump(model, 'trading_model.pkl')
    joblib.dump(vectorizer, 'trading_vectorizer.pkl')
    
    print("\n💾 매매 모델 저장 완료:")
    print("   - trading_model.pkl")
    print("   - trading_vectorizer.pkl")
    
    return model, vectorizer

# ✅ 5. 실행
if __name__ == "__main__":
    print("\n🤖 모델 학습 시작\n")
    
    # 감성 분석 모델
    sentiment_model, tfidf_vec = train_sentiment_model()
    
    # 매매 신호 모델
    trading_model, trading_vec = train_trading_model()
    
    print("\n" + "="*60)
    print("🎉 전체 학습 완료!")
    print("="*60)
    print("\n다음 단계: python realtime_analyzer.py")