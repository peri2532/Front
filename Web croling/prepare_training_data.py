import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import glob

# ✅ 1. 수집한 CSV 파일들 통합
def merge_news_csvs():
    """모든 기업 뉴스 CSV를 하나로 통합"""
    all_files = glob.glob("*_news_*.csv")
    
    if not all_files:
        print("❌ CSV 파일이 없습니다!")
        return None
    
    df_list = []
    for file in all_files:
        df = pd.read_csv(file, encoding='utf-8-sig')
        df_list.append(df)
    
    merged_df = pd.concat(df_list, ignore_index=True)
    print(f"✅ 총 {len(merged_df)}개 뉴스 통합 완료")
    
    return merged_df

# ✅ 2. 주가 데이터 수집
def get_stock_data(ticker_symbol, start_date, end_date):
    """한국 주식 데이터 수집"""
    try:
        stock = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)
        return stock
    except Exception as e:
        print(f"❌ 주가 데이터 수집 실패: {e}")
        return None

# ✅ 3. 뉴스-주가 레이블링 (완전 수정)
def create_labeled_dataset(news_df):
    """뉴스 발표 후 주가 변동을 기준으로 레이블 생성"""
    
    ticker_map = {
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
    
    labeled_data = []
    
    for company in news_df['기업'].unique():
        print(f"\n🔍 [{company}] 레이블링 시작...")
        
        company_news = news_df[news_df['기업'] == company].copy()
        ticker = ticker_map.get(company)
        
        if not ticker:
            print(f"  ⚠️ 티커 심볼 없음")
            continue
        
        # 주가 데이터 수집
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        stock_data = get_stock_data(ticker, start_date, end_date)
        
        if stock_data is None or stock_data.empty:
            print(f"  ⚠️ 주가 데이터 없음")
            continue
        
        success_count = 0
        
        # 각 뉴스별 레이블링
        for idx, row in company_news.iterrows():
            try:
                # 뉴스 날짜 파싱 (여러 형식 시도)
                date_str = row['날짜']
                
                try:
                    # RFC 2822 형식 (Google News RSS)
                    news_date = pd.to_datetime(date_str, format='%a, %d %b %Y %H:%M:%S %Z', errors='coerce')
                    if pd.isna(news_date):
                        # ISO 형식
                        news_date = pd.to_datetime(date_str, errors='coerce')
                except:
                    news_date = pd.to_datetime(date_str, errors='coerce')
                
                if pd.isna(news_date):
                    continue
                
                # 시간대 제거
                if news_date.tzinfo is not None:
                    news_date = news_date.tz_localize(None)
                
                # 날짜만 추출 (시간 제거)
                news_date_only = news_date.date()
                
                # 주가 데이터에서 뉴스 날짜 이후 데이터 필터링
                future_mask = stock_data.index.date >= news_date_only
                future_data = stock_data[future_mask]
                
                if len(future_data) < 4:  # 최소 4거래일 필요
                    continue
                
                # 기준가와 3거래일 후 가격
                base_price = float(future_data.iloc[0]['Close'])
                future_price = float(future_data.iloc[3]['Close'])
                
                # 수익률 계산
                return_3d = ((future_price - base_price) / base_price) * 100
                
                # 레이블 생성
                if return_3d > 2:
                    sentiment_label = "긍정"
                    trade_signal = "매수"
                elif return_3d < -2:
                    sentiment_label = "부정"
                    trade_signal = "매도"
                else:
                    sentiment_label = "중립"
                    trade_signal = "관망"
                
                labeled_data.append({
                    '기업': company,
                    '티커': ticker,
                    '제목': row['제목'],
                    '본문요약': row['본문요약'],
                    '날짜': news_date,
                    '3일수익률': round(return_3d, 2),
                    '감성레이블': sentiment_label,
                    '거래신호': trade_signal
                })
                
                success_count += 1
                
            except Exception as e:
                # 에러 메시지 출력 생략 (너무 많음)
                continue
        
        print(f"  ✅ {success_count}개 레이블 완료")
    
    result_df = pd.DataFrame(labeled_data)
    
    if result_df.empty:
        print("\n❌ 레이블된 데이터가 없습니다!")
        print("   원인: 뉴스 날짜가 최근이라 주가 데이터 부족")
        return None
    
    print(f"\n{'='*60}")
    print(f"✅ 전체 레이블링 완료: {len(result_df)}개")
    print(f"\n📊 감성 레이블 분포:")
    print(result_df['감성레이블'].value_counts())
    print(f"\n📊 거래 신호 분포:")
    print(result_df['거래신호'].value_counts())
    print(f"{'='*60}")
    
    return result_df

# ✅ 4. 실행
if __name__ == "__main__":
    print("🎯 학습 데이터 준비 시작\n")
    
    # 1단계: 뉴스 CSV 통합
    news_df = merge_news_csvs()
    
    if news_df is not None:
        # 2단계: 주가 데이터와 결합하여 레이블 생성
        labeled_df = create_labeled_dataset(news_df)
        
        # 3단계: 저장
        if labeled_df is not None and not labeled_df.empty:
            output_file = f"labeled_news_dataset_{datetime.now().strftime('%Y%m%d')}.csv"
            labeled_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n💾 저장 완료: {output_file}")
            
            # 4단계: 학습용/테스트용 분리
            train_size = int(len(labeled_df) * 0.8)
            train_df = labeled_df.iloc[:train_size]
            test_df = labeled_df.iloc[train_size:]
            
            train_df.to_csv('train_dataset.csv', index=False, encoding='utf-8-sig')
            test_df.to_csv('test_dataset.csv', index=False, encoding='utf-8-sig')
            
            print(f"📚 학습 데이터: {len(train_df)}개 → train_dataset.csv")
            print(f"🧪 테스트 데이터: {len(test_df)}개 → test_dataset.csv")
        else:
            print("\n❌ 레이블 데이터 생성 실패!")
            print("   뉴스가 너무 최근이라 주가 변동 데이터가 부족할 수 있습니다.")