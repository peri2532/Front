"""
네이버 뉴스 크롤러 - 달별 수집 (감성분석용)
시간적 다양성 확보를 위한 월별 분할 수집
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime, timedelta
import os
import re

class NaverNewsMonthlycrawler:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--page-load-strategy=eager')
        
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(20)
        
        self.companies = [
            '삼성전자', '현대자동차', 'SK하이닉스', 'LG전자', '네이버',
            '카카오', '삼성SDI', '포스코', '현대중공업', 'KB금융'
        ]
        
        os.makedirs('naver_news_data', exist_ok=True)
    
    def get_date_ranges(self, months=3):
        """최근 N개월의 월별 날짜 범위 생성"""
        today = datetime.now()
        date_ranges = []
        
        for i in range(months):
            # i개월 전의 첫날과 마지막날
            if i == 0:
                # 이번 달: 1일 ~ 오늘
                end_date = today
                start_date = datetime(today.year, today.month, 1)
            else:
                # 이전 달들
                target_date = today - timedelta(days=30*i)
                year = target_date.year
                month = target_date.month
                
                # 해당 월의 첫날
                start_date = datetime(year, month, 1)
                
                # 해당 월의 마지막날
                if month == 12:
                    end_date = datetime(year, 12, 31)
                else:
                    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            
            date_ranges.append({
                'start': start_date.strftime('%Y.%m.%d'),
                'end': end_date.strftime('%Y.%m.%d'),
                'label': start_date.strftime('%Y년 %m월')
            })
        
        return date_ranges
    
    def search_company_news_by_date(self, company, start_date, end_date, period_label):
        """특정 기간의 기업 뉴스 검색"""
        try:
            print(f"  🗓️  {period_label} ({start_date} ~ {end_date})")
            
            # 날짜 범위가 포함된 URL
            search_url = f"https://search.naver.com/search.naver?where=news&query={company}&sm=tab_opt&sort=1&photo=0&field=0&pd=3&ds={start_date}&de={end_date}"
            
            self.driver.get(search_url)
            time.sleep(3)
            
            print(f"  ✅ 페이지 로드 완료")
            return True
            
        except Exception as e:
            print(f"  ❌ 검색 실패: {e}")
            return False
    
    def is_valid_news_link(self, url, text):
        """유효한 뉴스 링크인지 확인"""
        if not url:
            return False
        
        exclude_patterns = [
            'search.naver.com',
            'keep.naver.com',
            'media.naver.com/press',
            'javascript:',
            '#',
        ]
        
        for pattern in exclude_patterns:
            if pattern in url:
                return False
        
        if text and len(text.strip()) < 10:
            if '/article' in url or '/view' in url or '/news' in url:
                return True
            return False
        
        news_patterns = [
            'news.naver.com',
            'n.news.naver.com',
            '/article',
            '/news/',
            '/view',
            'articleView',
        ]
        
        for pattern in news_patterns:
            if pattern in url:
                return True
        
        if url.startswith('http') and any(domain in url for domain in ['.co.kr', '.com', '.kr']):
            if any(char.isdigit() for char in url):
                return True
        
        return False
    
    def extract_article_content(self, url, max_retries=2):
        """기사 페이지에서 본문 1-3줄 추출"""
        original_window = self.driver.current_window_handle
        
        for attempt in range(max_retries):
            try:
                self.driver.execute_script(f"window.open('{url}', '_blank');")
                WebDriverWait(self.driver, 5).until(lambda d: len(d.window_handles) > 1)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(2)
                
                content_selectors = [
                    'div#dic_area', 'div#articleBodyContents', 'div.article_body',
                    'div#articeBody', 'div.article_view', 'div.article-body',
                    'div.news_body', 'div.view_body', 'div#news-body-area',
                    'div.news-article-body', 'article', 'div[itemprop="articleBody"]',
                    'div.article-text', 'div.article', 'div.content', 'div.news_content',
                ]
                
                content_text = ""
                
                for selector in content_selectors:
                    try:
                        content_elem = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        text = content_elem.text.strip()
                        
                        if text and len(text) > 50:
                            content_text = text
                            break
                    except:
                        continue
                
                if content_text:
                    lines = []
                    for line in content_text.split('\n'):
                        line = line.strip()
                        
                        if len(line) < 10:
                            continue
                        if '기자' in line and len(line) < 30:
                            continue
                        if re.match(r'^\d{4}[-./]\d{1,2}[-./]\d{1,2}', line):
                            continue
                        if line.startswith('[') and line.endswith(']'):
                            continue
                        if '무단전재' in line or '재배포' in line:
                            continue
                        
                        lines.append(line)
                        
                        if len(lines) >= 3:
                            break
                    
                    result = ' '.join(lines[:3])
                    
                    if len(result) > 300:
                        result = result[:300] + '...'
                    
                    self.driver.close()
                    self.driver.switch_to.window(original_window)
                    return result
                
                self.driver.close()
                self.driver.switch_to.window(original_window)
                return ""
                
            except:
                try:
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                    self.driver.switch_to.window(original_window)
                except:
                    pass
                
                if attempt < max_retries - 1:
                    continue
                else:
                    return ""
        
        return ""
    
    def extract_articles_from_page(self):
        """현재 페이지에서 기사 URL과 제목 추출"""
        articles = []
        
        try:
            all_links = self.driver.find_elements(By.CSS_SELECTOR, 'ul.list_news a')
            
            if not all_links:
                return articles
            
            for link in all_links:
                try:
                    url = link.get_attribute('href')
                    text = link.text.strip()
                    title = link.get_attribute('title')
                    
                    if not self.is_valid_news_link(url, text):
                        continue
                    
                    if title and len(title) > 10:
                        final_title = title
                    elif text and len(text) > 10:
                        final_title = text
                    else:
                        continue
                    
                    articles.append({
                        'url': url,
                        'title': final_title
                    })
                    
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"    ❌ 추출 오류: {e}")
        
        return articles
    
    def scroll_and_collect(self, target_count=300):
        """무한 스크롤하며 기사 URL/제목 수집"""
        collected_urls = set()
        all_articles = []
        scroll_attempts = 0
        max_no_new_content = 5
        no_new_content_count = 0
        
        print(f"  📊 기사 수집 중 (목표: {target_count}개)")
        
        while len(all_articles) < target_count:
            articles = self.extract_articles_from_page()
            
            new_articles = []
            for article in articles:
                if article['url'] not in collected_urls:
                    collected_urls.add(article['url'])
                    new_articles.append(article)
            
            all_articles.extend(new_articles)
            
            if new_articles:
                print(f"    → {len(new_articles)}개 추가 (누적: {len(all_articles)}개)")
                no_new_content_count = 0
            else:
                no_new_content_count += 1
                
                if no_new_content_count >= max_no_new_content:
                    print(f"    ⚠️ 더 이상 기사 없음 ({len(all_articles)}개로 종료)")
                    break
            
            if len(all_articles) >= target_count:
                print(f"    ✅ 목표 달성!")
                break
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            try:
                more_btn = self.driver.find_element(By.CSS_SELECTOR, 'a.btn_more, button.btn_more')
                if more_btn.is_displayed():
                    more_btn.click()
                    time.sleep(2)
            except:
                pass
            
            scroll_attempts += 1
            
            if scroll_attempts > 100:
                print(f"    ⚠️ 최대 스크롤 도달 ({len(all_articles)}개로 종료)")
                break
        
        return all_articles[:target_count]
    
    def extract_content_for_articles(self, articles):
        """수집한 기사들의 본문 1-3줄 추출"""
        print(f"\n  📝 본문 추출 시작 ({len(articles)}개)")
        
        success_count = 0
        fail_count = 0
        
        for i, article in enumerate(articles, 1):
            try:
                content = self.extract_article_content(article['url'])
                
                if content:
                    article['content'] = content
                    success_count += 1
                else:
                    article['content'] = ""
                    fail_count += 1
                
                if i % 20 == 0:
                    print(f"    → {i}/{len(articles)} (성공: {success_count}, 실패: {fail_count})")
                
                time.sleep(0.5)
                
            except Exception as e:
                article['content'] = ""
                fail_count += 1
        
        print(f"  ✅ 완료! (성공: {success_count}, 실패: {fail_count})")
        
        return articles
    
    def crawl_company_news_monthly(self, company, articles_per_month=300, months=3):
        """특정 기업의 월별 뉴스 크롤링"""
        print(f"\n{'='*70}")
        print(f"🏢 {company}")
        print(f"{'='*70}")
        
        # 날짜 범위 생성
        date_ranges = self.get_date_ranges(months)
        
        print(f"\n📅 수집 기간:")
        for dr in date_ranges:
            print(f"   • {dr['label']}: {dr['start']} ~ {dr['end']}")
        print()
        
        all_articles = []
        
        try:
            for i, date_range in enumerate(date_ranges, 1):
                print(f"\n[{i}/{len(date_ranges)}] {date_range['label']}")
                print("-" * 70)
                
                # 해당 기간으로 검색
                if not self.search_company_news_by_date(
                    company, 
                    date_range['start'], 
                    date_range['end'],
                    date_range['label']
                ):
                    print(f"  ❌ {date_range['label']} 검색 실패")
                    continue
                
                # URL/제목 수집
                articles = self.scroll_and_collect(articles_per_month)
                
                if not articles:
                    print(f"  ⚠️ {date_range['label']} 기사 없음")
                    continue
                
                # 월별 표시 추가
                for article in articles:
                    article['period'] = date_range['label']
                
                all_articles.extend(articles)
                
                print(f"  ✓ {date_range['label']}: {len(articles)}개 수집")
            
            if not all_articles:
                print(f"\n❌ {company}: 전체 기간 기사 없음")
                return None
            
            print(f"\n{'='*70}")
            print(f"📊 {company} URL 수집 완료: 총 {len(all_articles)}개")
            print(f"{'='*70}")
            
            # 본문 추출
            all_articles = self.extract_content_for_articles(all_articles)
            
            # CSV 저장
            df = pd.DataFrame(all_articles)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"naver_news_data/{company}_monthly_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"\n✅ {company} 완료!")
            print(f"   📊 총 {len(all_articles)}개 기사")
            print(f"   💾 {filename}\n")
            
            # 월별 통계
            print(f"   📈 월별 분포:")
            for period in df['period'].value_counts().sort_index(ascending=False).items():
                print(f"      • {period[0]}: {period[1]}개")
            
            return df
                
        except Exception as e:
            print(f"\n❌ {company} 실패: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def crawl_all_companies(self, articles_per_month=300, months=3):
        """모든 기업의 월별 뉴스 크롤링"""
        print(f"\n🚀 네이버 뉴스 크롤러 - 월별 수집")
        print(f"📋 수집 대상: {len(self.companies)}개 기업")
        print(f"📅 수집 기간: 최근 {months}개월")
        print(f"🎯 월별 목표: {articles_per_month}개")
        print(f"📊 기업당 총: 약 {articles_per_month * months}개\n")
        
        results = {}
        start_time = time.time()
        
        for i, company in enumerate(self.companies, 1):
            print(f"\n{'#'*70}")
            print(f"# [{i}/{len(self.companies)}] {company} 시작")
            print(f"{'#'*70}")
            
            df = self.crawl_company_news_monthly(company, articles_per_month, months)
            results[company] = df
            
            if i < len(self.companies):
                print(f"\n⏳ 다음 기업까지 10초 대기...\n")
                time.sleep(10)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print(f"🎉 전체 크롤링 완료!")
        print(f"⏱️  소요 시간: {elapsed_time/60:.1f}분")
        print(f"{'='*70}\n")
        
        print("📊 최종 결과:")
        total = 0
        for company, df in results.items():
            if df is not None:
                count = len(df)
                total += count
                print(f"  ✓ {company}: {count}개")
            else:
                print(f"  ✗ {company}: 실패")
        
        print(f"\n💾 총 {total}개 기사")
        print(f"📁 저장: naver_news_data/")
        print(f"📅 시간적 다양성 확보! (월별 균등 분포)\n")
        
        return results
    
    def close(self):
        """브라우저 종료"""
        self.driver.quit()

if __name__ == "__main__":
    crawler = NaverNewsMonthlycrawler()
    
    try:
        # 최근 3개월, 월별 300개씩 수집
        # 총 900개 (시간적으로 균등 분포)
        results = crawler.crawl_all_companies(
            articles_per_month=300,  # 월별 개수
            months=3                 # 수집 개월 수
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        crawler.close()
        print("\n👋 크롤러 종료")