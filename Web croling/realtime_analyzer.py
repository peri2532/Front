import pandas as pd
import numpy as np
import joblib
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import yfinance as yf

# ✅ 1. 모델 로드
class NewsAnalyzer:
    def __init__(self):
        """학습된 모델 및 전처리기 로드"""
        print("🔧 모델 로딩 중...")
        
        try:
            self.sentiment_model = joblib.load('sentiment_model.pkl')
            self.trading_model = joblib.load('trading_model.pkl')
            self.tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
            self.trading_vectorizer = joblib.load('trading_vectorizer.pkl')
            self.preprocessor = joblib.load('text_preprocessor.pkl')
            
            print("✅ 모델 로딩 완료")
        except FileNotFoundError:
            print("❌ 모델 파일이 없습니다! 먼저 학습을 진행하세요.")
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
    
    def analyze_news(self, title, content):
        """
        뉴스 기사 분석
        
        Returns:
            dict: 감성, 신뢰도, 거래신호 등
        """
        # 텍스트 전처리
        combined_text = title + ' ' + content
        cleaned = self.preprocessor.clean_text(combined_text)
        keywords = self.preprocessor.extract_keywords(cleaned)
        pos_count, neg_count = self.preprocessor.add_sentiment_features(cleaned)
        
        # 감성 분석
        X_tfidf = self.tfidf_vectorizer.transform([keywords])
        X_extra = np.array([[pos_count, neg_count]])
        X_sentiment = np.hstack([X_tfidf.toarray(), X_extra])
        
        sentiment = self.sentiment_model.predict(X_sentiment)[0]
        sentiment_proba = self.sentiment_model.predict_proba(X_sentiment)[0]
        sentiment_confidence = max(sentiment_proba)
        
        # 거래 신호 예측
        X_trading_tfidf = self.trading_vectorizer.transform([keywords])
        # 임시 수익률 (실제론 과거 데이터 사용)
        X_trading_extra = np.array([[pos_count, neg_count, 0, 0]])
        X_trading = np.hstack([X_trading_tfidf.toarray(), X_trading_extra])
        
        trade_signal = self.trading_model.predict(X_trading)[0]
        trade_proba = self.trading_model.predict_proba(X_trading)[0]
        trade_confidence = max(trade_proba)
        
        return {
            '감성': sentiment,
            '감성_신뢰도': f"{sentiment_confidence:.1%}",
            '긍정키워드': pos_count,
            '부정키워드': neg_count,
            '거래신호': trade_signal,
            '신호_신뢰도': f"{trade_confidence:.1%}",
            '분석시각': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_current_price(self, company):
        """현재 주가 조회"""
        ticker = self.ticker_map.get(company)
        if not ticker:
            return None
        
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.info.get('currentPrice', 
                            stock.info.get('regularMarketPrice', 0))
            prev_close = stock.info.get('previousClose', 0)
            
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

# ✅ 2. 실시간 뉴스 수집 & 분석
def collect_and_analyze_latest_news(company, max_news=5):
    """특정 기업의 최신 뉴스 수집 및 분석"""
    
    print(f"\n{'='*70}")
    print(f"🔍 [{company}] 최신 뉴스 분석")
    print(f"{'='*70}")
    
    analyzer = NewsAnalyzer()
    
    # 현재 주가 정보
    price_info = analyzer.get_current_price(company)
    if price_info:
        print(f"\n📊 현재 주가: {price_info['현재가']} ({price_info['전일대비']})")
    
    # 최신 뉴스 검색
    search_keyword = f"{company} 최신"
    encoded = urllib.parse.quote(search_keyword)
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
            
            print(f"\n📰 [{i}] {title}")
            print(f"    🕐 {pub_date}")
            print(f"    🔗 {link[:80]}...")
            
            # 본문 수집 (간단 버전)
            try:
                article_res = requests.get(link, headers=headers, timeout=5)
                article_soup = BeautifulSoup(article_res.text, 'html.parser')
                
                # 본문 추출 시도
                content = ""
                for selector in ['#dic_area', '.article_body', 'article']:
                    element = article_soup.select_one(selector)
                    if element:
                        content = element.get_text(strip=True)[:1000]
                        break
                
                if not content:
                    content = title  # 본문 없으면 제목만 사용
                
            except:
                content = title
            
            # AI 분석
            analysis = analyzer.analyze_news(title, content)
            
            print(f"\n    🤖 AI 분석 결과:")
            print(f"       감성: {analysis['감성']} (신뢰도: {analysis['감성_신뢰도']})")
            print(f"       긍정 키워드: {analysis['긍정키워드']}개 | 부정 키워드: {analysis['부정키워드']}개")
            print(f"       💡 추천: {analysis['거래신호']} (신뢰도: {analysis['신호_신뢰도']})")
            
            results.append({
                '순번': i,
                '제목': title,
                '날짜': pub_date,
                '링크': link,
                **analysis
            })
        
        # 종합 판단
        print(f"\n{'='*70}")
        print("📊 종합 분석 결과")
        print(f"{'='*70}")
        
        df = pd.DataFrame(results)
        
        sentiment_counts = df['감성'].value_counts()
        signal_counts = df['거래신호'].value_counts()
        
        print(f"\n감성 분포: {dict(sentiment_counts)}")
        print(f"신호 분포: {dict(signal_counts)}")
        
        # 최종 추천
        if '긍정' in sentiment_counts and sentiment_counts['긍정'] >= max_news * 0.6:
            final_recommendation = "📈 매수 검토 권장"
        elif '부정' in sentiment_counts and sentiment_counts['부정'] >= max_news * 0.6:
            final_recommendation = "📉 매도 또는 관망 권장"
        else:
            final_recommendation = "⚖️ 신중한 관망 권장"
        
        print(f"\n🎯 최종 추천: {final_recommendation}")
        print(f"{'='*70}")
        
        # 결과 저장
        output_file = f"{company}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 분석 결과 저장: {output_file}")
        
        return df
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

# ✅ 3. 멀티 기업 동시 분석
def analyze_multiple_companies(companies, max_news=3):
    """여러 기업 동시 분석 및 비교"""
    
    print("🎯 멀티 기업 분석 시작\n")
    
    all_results = {}
    
    for company in companies:
        result = collect_and_analyze_latest_news(company, max_news)
        if result is not None:
            all_results[company] = result
    
    # 비교 리포트
    print(f"\n{'='*70}")
    print("📊 기업별 비교 리포트")
    print(f"{'='*70}\n")
    
    for company, df in all_results.items():
        positive = len(df[df['감성'] == '긍정'])
        buy_signals = len(df[df['거래신호'] == '매수'])
        
        print(f"{company:15s} | 긍정뉴스: {positive}/{len(df)} | 매수신호: {buy_signals}/{len(df)}")
    
    print(f"{'='*70}")

# ✅ 4. 실행 예시
if __name__ == "__main__":
    # 단일 기업 분석
    collect_and_analyze_latest_news("삼성전자", max_news=5)
    
    # 또는 여러 기업 동시 분석
    # analyze_multiple_companies(["삼성전자", "SK하이닉스", "네이버"], max_news=3)