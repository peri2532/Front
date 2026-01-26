import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse
from datetime import datetime
import re

# ✅ 크롤링할 기업 리스트
companies = [
    "삼성전자", "SK하이닉스", "LG에너지솔루션", "현대차", "기아",
    "삼성바이오로직스", "셀트리온", "카카오", "네이버", "POSCO홀딩스"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ✅ Google News RSS로 뉴스 수집
def collect_google_news(company, max_articles=1000):
    """Google News RSS로 뉴스 대량 수집"""
    
    print(f"\n{'='*60}")
    print(f"🔍 [{company}] 뉴스 수집 중... (목표: {max_articles}개)")
    print(f"{'='*60}")
    
    all_news = []
    seen_titles = set()  # 중복 제거용
    
    # 여러 검색어 조합으로 수집량 늘리기
    search_keywords = [
        f"{company}",
        f"{company} 주가",
        f"{company} 실적",
        f"{company} 영업이익",
        f"{company} 매출",
        f"{company} 투자",
    ]
    
    for keyword in search_keywords:
        if len(all_news) >= max_articles:
            break
        
        print(f"\n  🔎 검색어: '{keyword}'")
        
        encoded = urllib.parse.quote(keyword)
        rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        
        try:
            res = requests.get(rss_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.content, "xml")
            
            items = soup.find_all("item")
            print(f"     📰 {len(items)}개 발견")
            
            collected_this_search = 0
            
            for item in items:
                if len(all_news) >= max_articles:
                    break
                
                try:
                    title = item.title.get_text() if item.title else ""
                    pub_date = item.pubDate.get_text() if item.pubDate else ""
                    link = item.link.get_text() if item.link else ""
                    description = item.description.get_text() if item.description else ""
                    
                    # 중복 제목 제거
                    if title in seen_titles or len(title) < 10:
                        continue
                    
                    seen_titles.add(title)
                    
                    # description에서 본문 요약 추출
                    if description:
                        desc_soup = BeautifulSoup(description, 'html.parser')
                        desc_text = desc_soup.get_text(strip=True)
                        summary = desc_text[:300] if len(desc_text) > 30 else title
                    else:
                        summary = title
                    
                    all_news.append({
                        "기업": company,
                        "제목": title,
                        "날짜": pub_date,
                        "링크": link,
                        "본문요약": summary
                    })
                    
                    collected_this_search += 1
                    
                except Exception as e:
                    continue
            
            print(f"     ✅ {collected_this_search}개 수집 (누적: {len(all_news)}개)")
            time.sleep(2)  # 검색어 간 대기
            
        except Exception as e:
            print(f"     ❌ 에러: {str(e)[:50]}")
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ [{company}] 총 {len(all_news)}개 수집 완료")
    print(f"{'='*60}")
    
    return all_news

# ✅ 다음 뉴스 추가 수집 (부족할 경우)
def collect_daum_news(company, current_count, target=1000):
    """다음 뉴스로 부족분 채우기"""
    
    needed = target - current_count
    if needed <= 0:
        return []
    
    print(f"\n  ⚠️ 부족분 {needed}개 - 다음 뉴스 추가 수집...")
    
    all_news = []
    encoded = urllib.parse.quote(company)
    
    # 최대 10페이지까지 수집
    for page in range(1, 11):
        if len(all_news) >= needed:
            break
        
        url = f"https://search.daum.net/search?w=news&q={encoded}&sort=recency&p={page}"
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            news_items = soup.select('div.c-item-content')
            
            for item in news_items:
                if len(all_news) >= needed:
                    break
                
                try:
                    title_tag = item.select_one('a.f_link_b')
                    if not title_tag:
                        continue
                    
                    title = title_tag.get_text(strip=True)
                    link = title_tag.get('href', '')
                    
                    summary_tag = item.select_one('p.c-summary')
                    summary = summary_tag.get_text(strip=True)[:300] if summary_tag else title
                    
                    date_tag = item.select_one('span.c-datetime')
                    pub_date = date_tag.get_text(strip=True) if date_tag else ""
                    
                    all_news.append({
                        "기업": company,
                        "제목": title,
                        "날짜": pub_date,
                        "링크": link,
                        "본문요약": summary
                    })
                    
                except Exception:
                    continue
            
            time.sleep(1)
            
        except Exception:
            continue
    
    print(f"     ✅ 다음 뉴스 {len(all_news)}개 추가 수집")
    return all_news

# ✅ 전체 기업 수집
def collect_all_companies():
    """모든 기업 뉴스 1000개씩 수집"""
    
    print("🎯 대량 뉴스 수집 시작")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎲 목표: 기업당 1,000개 × 10개 기업 = 총 10,000개\n")
    
    all_data = []
    
    for i, company in enumerate(companies, 1):
        print(f"\n{'#'*60}")
        print(f"[{i}/{len(companies)}] {company} 수집 시작")
        print(f"{'#'*60}")
        
        # 1차: Google News 수집
        news = collect_google_news(company, max_articles=1000)
        
        # 2차: 부족하면 다음 뉴스 추가
        if len(news) < 1000:
            daum_news = collect_daum_news(company, len(news), target=1000)
            news.extend(daum_news)
        
        all_data.extend(news)
        
        print(f"\n📊 [{company}] 최종 수집: {len(news)}개")
        
        # 중간 저장 (만약을 위해)
        temp_df = pd.DataFrame(news)
        temp_file = f"{company}_news_temp.csv"
        temp_df.to_csv(temp_file, index=False, encoding='utf-8-sig')
        print(f"💾 임시 저장: {temp_file}")
        
        # 기업 간 대기
        if i < len(companies):
            print(f"\n⏸️ 다음 기업까지 5초 대기...\n")
            time.sleep(5)
    
    # ✅ 최종 통합 저장
    if all_data:
        df = pd.DataFrame(all_data)
        
        filename = f"all_news_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n{'='*60}")
        print(f"🎉 전체 수집 완료!")
        print(f"{'='*60}")
        print(f"📊 총 {len(df):,}개 뉴스 수집")
        print(f"💾 파일: {filename}")
        print(f"\n📋 기업별 수집 현황:")
        print(df['기업'].value_counts().sort_index())
        print(f"{'='*60}")
        
        # 통계
        print(f"\n📈 데이터 통계:")
        print(f"   - 평균 제목 길이: {df['제목'].str.len().mean():.1f}자")
        print(f"   - 평균 요약 길이: {df['본문요약'].str.len().mean():.1f}자")
        print(f"   - 중복 제거 후: {df.drop_duplicates(subset=['제목']).shape[0]:,}개")
        
        return df
    else:
        print("\n❌ 수집된 데이터가 없습니다!")
        return None

# ✅ 실행
if __name__ == "__main__":
    start_time = time.time()
    
    result_df = collect_all_companies()
    
    elapsed = time.time() - start_time
    print(f"\n⏱️ 총 소요 시간: {elapsed/60:.1f}분")