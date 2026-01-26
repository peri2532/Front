import pandas as pd
import numpy as np
import joblib
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import yfinance as yf
import re
import os

# =========================================================
# 경로 설정 (모델 파일 안정적 로드용)
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = BASE_DIR   # 모델 파일들이 현재 폴더(Web croling)에 있음


# =========================================================
# 1. 텍스트 전처리 함수 (train_model.py와 동일)
# =========================================================
def simple_preprocess(text):
    """한글, 영문, 숫자만 유지"""
    if pd.isna(text):
        return ""
    
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

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

# =========================================================
# 2. 모델 로드 및 분석 클래스
# =========================================================
class NewsAnalyzer:
    def __init__(self):
        """학습된 모델 로드"""
        print("🔧 모델 로딩 중...")
        
        try:
            self.sentiment_model = joblib.load(os.path.join(MODEL_DIR, 'sentiment_model.pkl'))
            self.trading_model = joblib.load(os.path.join(MODEL_DIR, 'trading_model.pkl'))
            self.tfidf_vectorizer = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))
            self.trading_vectorizer = joblib.load(os.path.join(MODEL_DIR, 'trading_vectorizer.pkl'))
            
            print("✅ 모델 로딩 완료")
        except FileNotFoundError as e:
            print(f"❌ 모델 파일이 없습니다: {e}")
            print("   먼저 train_model.py를 실행하여 모델을 생성하세요.")
            raise
        
        # 티커 매핑
        self.ticker_map = {
            "삼성전자": "005930.KS",
            "SK하이닉스": "000660.KS",
            "LG에너지솔루션": "373220.KS",
            "현대차": "005380.KS",
            "기아": "000270.KS",
            "삼성바이오로직스": "207940.KS",
            "셀트리온": "068270.KS",
            "카카오": "035720.KS",
            "네이버": "035420.KS",
            "POSCO홀딩스": "005490.KS"
        }
    
    # -----------------------------------------------------
    # 뉴스 단건 분석
    # -----------------------------------------------------
    def analyze_news(self, title, content):
        """뉴스 기사 분석"""
        combined_text = f"{title} {content}"
        cleaned = simple_preprocess(combined_text)
        pos_count, neg_count = count_sentiment_keywords(cleaned)
        
        # ================= 감성 분석 =================
        X_tfidf = self.tfidf_vectorizer.transform([cleaned])
        X_extra = np.array([[pos_count, neg_count, 0]])  # 수익률은 0
        X_sentiment = np.hstack([X_tfidf.toarray(), X_extra])
        
        sentiment_raw = self.sentiment_model.predict(X_sentiment)[0]
        sentiment_proba = self.sentiment_model.predict_proba(X_sentiment)[0]
        sentiment_confidence = max(sentiment_proba)
        
        # 라벨 매핑 (모델 학습 기준에 맞게 조정 가능)
        sentiment_map = {0: "부정", 1: "중립", 2: "긍정"}
        sentiment = sentiment_map.get(sentiment_raw, sentiment_raw)
        
        # ================= 거래 신호 =================
        X_trading_tfidf = self.trading_vectorizer.transform([cleaned])
        X_trading_extra = np.array([[pos_count, neg_count, 0]])
        X_trading = np.hstack([X_trading_tfidf.toarray(), X_trading_extra])
        
        trade_raw = self.trading_model.predict(X_trading)[0]
        trade_proba = self.trading_model.predict_proba(X_trading)[0]
        trade_confidence = max(trade_proba)
        
        signal_map = {0: "매도", 1: "관망", 2: "매수"}
        trade_signal = signal_map.get(trade_raw, trade_raw)
        
        return {
            '감성': sentiment,
            '감성_신뢰도': f"{sentiment_confidence:.1%}",
            '긍정키워드': pos_count,
            '부정키워드': neg_count,
            '거래신호': trade_signal,
            '신호_신뢰도': f"{trade_confidence:.1%}",
            '분석시각': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # -----------------------------------------------------
    # 현재 주가 조회
    # -----------------------------------------------------
    def get_current_price(self, company):
        ticker = self.ticker_map.get(company)
        if not ticker:
            return None
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            prev_close = info.get('previousClose', 0)
            
            if prev_close:
                change_pct = ((current_price - prev_close) / prev_close) * 100
            else:
                change_pct = 0
            
            return {
                '현재가': f"{current_price:,.0f}원",
                '전일대비': f"{change_pct:+.2f}%"
            }
        except:
            return None

# =========================================================
# 3. 실시간 뉴스 수집 & 분석
# =========================================================
def collect_and_analyze_latest_news(company, max_news=5):
    """특정 기업의 최신 뉴스 수집 및 분석"""
    
    print(f"\n{'='*70}")
    print(f"🔍 [{company}] 최신 뉴스 분석")
    print(f"{'='*70}")
    
    analyzer = NewsAnalyzer()
    
    # 현재 주가
    price_info = analyzer.get_current_price(company)
    if price_info:
        print(f"\n📊 현재 주가: {price_info['현재가']} ({price_info['전일대비']})")
    
    # Google News RSS
    encoded = urllib.parse.quote(company)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(rss_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, "xml")
        items = soup.find_all("item")[:max_news]
        
        if not items:
            print("⚠️ 최신 뉴스를 찾을 수 없습니다.")
            return
        
        results = []
        
        for i, item in enumerate(items, 1):
            title = item.title.get_text()
            link = item.link.get_text()
            pub_date = item.pubDate.get_text()
            
            # description (제목 + 첫 문장 전략 유지)
            description = ""
            if item.description:
                desc_soup = BeautifulSoup(item.description.get_text(), 'html.parser')
                description = desc_soup.get_text(strip=True)[:200]
            
            print(f"\n📰 [{i}] {title}")
            print(f"    🕐 {pub_date}")
            
            analysis = analyzer.analyze_news(title, description)
            
            print(f"\n    🤖 AI 분석 결과:")
            print(f"       감성: {analysis['감성']} (신뢰도: {analysis['감성_신뢰도']})")
            print(f"       긍정 키워드: {analysis['긍정키워드']}개 | 부정 키워드: {analysis['부정키워드']}개")
            print(f"       💡 추천: {analysis['거래신호']} (신뢰도: {analysis['신호_신뢰도']})")
            
            results.append({
                '순번': i,
                '기업': company,
                '제목': title,
                '날짜': pub_date,
                '링크': link,
                **analysis
            })
        
        # ================= 종합 판단 =================
        print(f"\n{'='*70}")
        print("📊 종합 분석 결과")
        print(f"{'='*70}")
        
        df = pd.DataFrame(results)
        
        sentiment_counts = df['감성'].value_counts()
        signal_counts = df['거래신호'].value_counts()
        
        print(f"\n감성 분포: {dict(sentiment_counts)}")
        print(f"신호 분포: {dict(signal_counts)}")
        
        positive_ratio = sentiment_counts.get('긍정', 0) / len(df)
        negative_ratio = sentiment_counts.get('부정', 0) / len(df)
        
        if positive_ratio >= 0.6:
            final_recommendation = "📈 매수 검토 권장"
        elif negative_ratio >= 0.6:
            final_recommendation = "📉 매도 또는 관망 권장"
        else:
            final_recommendation = "⚖️ 신중한 관망 권장"
        
        print(f"\n🎯 최종 추천: {final_recommendation}")
        print(f"{'='*70}")
        
        # ================= 결과 저장 =================
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        csv_file = f"{company}_analysis_{timestamp}.csv"
        json_file = f"{company}_analysis_{timestamp}.json"
        
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        df.to_json(json_file, orient="records", force_ascii=False, indent=2)
        
        print(f"\n💾 CSV 저장:  {csv_file}")
        print(f"💾 JSON 저장: {json_file}")
        
        return df
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

# =========================================================
# 4. 멀티 기업 동시 분석
# =========================================================
def analyze_multiple_companies(companies, max_news=3):
    print("🎯 멀티 기업 분석 시작\n")
    
    all_results = {}
    
    for company in companies:
        result = collect_and_analyze_latest_news(company, max_news)
        if result is not None:
            all_results[company] = result
    
    print(f"\n{'='*70}")
    print("📊 기업별 비교 리포트")
    print(f"{'='*70}\n")
    
    for company, df in all_results.items():
        positive = len(df[df['감성'] == '긍정'])
        buy_signals = len(df[df['거래신호'] == '매수'])
        
        print(f"{company:15s} | 긍정뉴스: {positive}/{len(df)} | 매수신호: {buy_signals}/{len(df)}")
    
    print(f"{'='*70}")

# =========================================================
# 5. 실행
# =========================================================
if __name__ == "__main__":
    # 단일 기업
    collect_and_analyze_latest_news("삼성전자", max_news=5)
    
    # 여러 기업 비교 예시
    # analyze_multiple_companies(["삼성전자", "SK하이닉스", "네이버"], max_news=3)
