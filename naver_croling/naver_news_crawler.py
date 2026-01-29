"""
네이버 뉴스 크롤러 - 병렬 처리 버전 (5개 동시 실행)
메모리: 16GB 이상 권장
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
from multiprocessing import Process, Queue
import traceback

class NaverNewsParallelCrawler:
    def __init__(self):
        self.companies = [
            '삼성전자', '현대자동차', 'SK하이닉스', 'LG전자', '네이버',
            '카카오', '삼성SDI', '포스코', '현대중공업', 'KB금융'
        ]
        
        os.makedirs('naver_news_data', exist_ok=True)
    
    @staticmethod
    def get_date_ranges(months=12):
        """최근 N개월의 월별 날짜 범위 생성"""
        today = datetime.now()
        date_ranges = []
        
        for i in range(months):
            if i == 0:
                end_date = today
                start_date = datetime(today.year, today.month, 1)
            else:
                target_date = today - timedelta(days=30*i)
                year = target_date.year
                month = target_date.month
                
                start_date = datetime(year, month, 1)
                
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
    
    @staticmethod
    def is_valid_news_link(url, text):
        """유효한 뉴스 링크인지 확인"""
        if not url:
            return False
        
        exclude_patterns = [
            'search.naver.com', 'keep.naver.com', 'media.naver.com/press',
            'javascript:', '#',
        ]
        
        for pattern in exclude_patterns:
            if pattern in url:
                return False
        
        if text and len(text.strip()) < 10:
            if '/article' in url or '/view' in url or '/news' in url:
                return True
            return False
        
        news_patterns = [
            'news.naver.com', 'n.news.naver.com', '/article',
            '/news/', '/view', 'articleView',
        ]
        
        for pattern in news_patterns:
            if pattern in url:
                return True
        
        if url.startswith('http') and any(domain in url for domain in ['.co.kr', '.com', '.kr']):
            if any(char.isdigit() for char in url):
                return True
        
        return False
    
    @staticmethod
    def crawl_single_company(company, articles_per_month=300, months=12, process_id=0):
        """단일 기업 크롤링 (프로세스에서 실행)"""
        try:
            print(f"\n[프로세스 {process_id}] 🏢 {company} 시작")
            print(f"[프로세스 {process_id}] {'='*70}")
            
            # Chrome 설정
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--page-load-strategy=eager')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(8)
            
            # 날짜 범위
            date_ranges = NaverNewsParallelCrawler.get_date_ranges(months)
            
            print(f"[프로세스 {process_id}] 📅 수집 기간: {len(date_ranges)}개월")
            
            all_articles = []
            
            # 월별 수집
            for i, date_range in enumerate(date_ranges, 1):
                try:
                    print(f"\n[프로세스 {process_id}] [{i}/{len(date_ranges)}] {date_range['label']}")
                    
                    # 검색
                    search_url = f"https://search.naver.com/search.naver?where=news&query={company}&sm=tab_opt&sort=1&photo=0&field=0&pd=3&ds={date_range['start']}&de={date_range['end']}"
                    driver.get(search_url)
                    time.sleep(3)
                    
                    # URL 수집
                    articles = NaverNewsParallelCrawler.collect_urls(driver, articles_per_month, process_id)
                    
                    if articles:
                        for article in articles:
                            article['period'] = date_range['label']
                        all_articles.extend(articles)
                        print(f"[프로세스 {process_id}]   ✓ {len(articles)}개 수집")
                    
                except Exception as e:
                    print(f"[프로세스 {process_id}]   ⚠️ {date_range['label']} 실패: {e}")
                    continue
            
            if not all_articles:
                print(f"[프로세스 {process_id}] ❌ {company}: 기사 없음")
                driver.quit()
                return
            
            print(f"\n[프로세스 {process_id}] 📝 본문 추출 시작 ({len(all_articles)}개)")
            
            # 본문 추출
            success = 0
            fail = 0
            
            for idx, article in enumerate(all_articles, 1):
                try:
                    content = NaverNewsParallelCrawler.extract_content(driver, article['url'])
                    article['content'] = content
                    
                    if content:
                        success += 1
                    else:
                        fail += 1
                    
                    if idx % 50 == 0:
                        print(f"[프로세스 {process_id}]   → {idx}/{len(all_articles)} (성공: {success}, 실패: {fail})")
                    
                    time.sleep(0.3)
                    
                except Exception as e:
                    article['content'] = ""
                    fail += 1
            
            # CSV 저장
            df = pd.DataFrame(all_articles)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"naver_news_data/{company}_monthly_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"\n[프로세스 {process_id}] ✅ {company} 완료!")
            print(f"[프로세스 {process_id}]    📊 {len(all_articles)}개")
            print(f"[프로세스 {process_id}]    ✓ 성공: {success}, ✗ 실패: {fail}")
            print(f"[프로세스 {process_id}]    💾 {filename}")
            
            # 월별 통계
            print(f"[프로세스 {process_id}]    📈 월별 분포:")
            for period, count in df['period'].value_counts().sort_index(ascending=False).head(5).items():
                print(f"[프로세스 {process_id}]       • {period}: {count}개")
            
            driver.quit()
            
        except Exception as e:
            print(f"\n[프로세스 {process_id}] ❌ {company} 전체 실패: {e}")
            traceback.print_exc()
            try:
                driver.quit()
            except:
                pass
    
    @staticmethod
    def collect_urls(driver, target_count, process_id):
        """URL 수집"""
        collected_urls = set()
        all_articles = []
        scroll_attempts = 0
        no_new_content = 0
        
        while len(all_articles) < target_count and scroll_attempts < 100:
            try:
                all_links = driver.find_elements(By.CSS_SELECTOR, 'ul.list_news a')
                
                new_articles = []
                for link in all_links:
                    try:
                        url = link.get_attribute('href')
                        text = link.text.strip()
                        title = link.get_attribute('title')
                        
                        if not NaverNewsParallelCrawler.is_valid_news_link(url, text):
                            continue
                        
                        if url in collected_urls:
                            continue
                        
                        if title and len(title) > 10:
                            final_title = title
                        elif text and len(text) > 10:
                            final_title = text
                        else:
                            continue
                        
                        collected_urls.add(url)
                        new_articles.append({'url': url, 'title': final_title})
                        
                    except:
                        continue
                
                all_articles.extend(new_articles)
                
                if new_articles:
                    no_new_content = 0
                else:
                    no_new_content += 1
                    if no_new_content >= 5:
                        break
                
                if len(all_articles) >= target_count:
                    break
                
                # 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # 더보기 버튼
                try:
                    more_btn = driver.find_element(By.CSS_SELECTOR, 'a.btn_more, button.btn_more')
                    if more_btn.is_displayed():
                        more_btn.click()
                        time.sleep(2)
                except:
                    pass
                
                scroll_attempts += 1
                
            except Exception as e:
                break
        
        return all_articles[:target_count]
    
    @staticmethod
    def extract_content(driver, url):
        """본문 추출"""
        original_window = driver.current_window_handle
        
        try:
            driver.execute_script(f"window.open('{url}', '_blank');")
            WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)
            
            content_selectors = [
                'div#dic_area', 'div#articleBodyContents', 'div.article_body',
                'div.article_view', 'div.article-body', 'div.news_body',
                'div.view_body', 'article', 'div[itemprop="articleBody"]',
                'div.article', 'div.content', 'div.news_content',
            ]
            
            content_text = ""
            
            for selector in content_selectors:
                try:
                    content_elem = WebDriverWait(driver, 2).until(
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
                
                driver.close()
                driver.switch_to.window(original_window)
                return result
            
            driver.close()
            driver.switch_to.window(original_window)
            return ""
            
        except:
            try:
                if len(driver.window_handles) > 1:
                    driver.close()
                driver.switch_to.window(original_window)
            except:
                pass
            return ""
    
    def crawl_all_companies_parallel(self, articles_per_month=300, months=12, parallel=5):
        """병렬로 모든 기업 크롤링"""
        print(f"\n{'='*70}")
        print(f"🚀 네이버 뉴스 크롤러 - 병렬 처리")
        print(f"{'='*70}")
        print(f"📋 수집 대상: {len(self.companies)}개 기업")
        print(f"📅 수집 기간: 최근 {months}개월")
        print(f"🎯 월별 목표: {articles_per_month}개")
        print(f"⚡ 병렬 처리: {parallel}개 동시 실행")
        print(f"📊 기업당 총: 약 {articles_per_month * months}개")
        print(f"💾 권장 메모리: 16GB 이상\n")
        
        start_time = time.time()
        
        # 기업을 그룹으로 나누기
        company_groups = []
        for i in range(0, len(self.companies), parallel):
            company_groups.append(self.companies[i:i+parallel])
        
        print(f"📦 {len(company_groups)}개 그룹으로 분할 (그룹당 {parallel}개씩)\n")
        
        # 그룹별로 병렬 실행
        for group_idx, company_group in enumerate(company_groups, 1):
            print(f"\n{'#'*70}")
            print(f"# 그룹 {group_idx}/{len(company_groups)}: {', '.join(company_group)}")
            print(f"{'#'*70}\n")
            
            processes = []
            
            # 프로세스 시작
            for idx, company in enumerate(company_group):
                p = Process(
                    target=self.crawl_single_company,
                    args=(company, articles_per_month, months, idx+1)
                )
                p.start()
                processes.append(p)
                time.sleep(2)  # 프로세스 시작 간격
            
            # 모든 프로세스 완료 대기
            for p in processes:
                p.join()
            
            print(f"\n✅ 그룹 {group_idx} 완료!\n")
            
            if group_idx < len(company_groups):
                print(f"⏳ 다음 그룹까지 10초 대기...\n")
                time.sleep(10)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print(f"🎉 전체 크롤링 완료!")
        print(f"⏱️  소요 시간: {elapsed_time/60:.1f}분 ({elapsed_time/3600:.1f}시간)")
        print(f"{'='*70}\n")
        
        # 결과 파일 확인
        print("📊 생성된 파일:")
        import glob
        files = glob.glob('naver_news_data/*_monthly_*.csv')
        for f in sorted(files):
            try:
                df = pd.read_csv(f)
                company_name = f.split('/')[-1].split('_monthly_')[0]
                print(f"  ✓ {company_name}: {len(df)}개 기사")
            except:
                pass
        
        print(f"\n📁 저장 위치: naver_news_data/")
        print(f"⚡ 병렬 처리로 시간 단축 완료!\n")

if __name__ == "__main__":
    print("="*70)
    print("⚠️  병렬 처리 크롤러 실행 전 확인사항:")
    print("="*70)
    print("1. RAM 16GB 이상 권장")
    print("2. Chrome 브라우저 5개가 동시에 실행됩니다")
    print("3. 작업 관리자에서 메모리 사용량 모니터링 권장")
    print("4. 실행 중 다른 프로그램 최소화 권장")
    print("="*70)
    
    response = input("\n계속 진행하시겠습니까? (y/n): ")
    
    if response.lower() != 'y':
        print("취소되었습니다.")
        exit()
    
    crawler = NaverNewsParallelCrawler()
    
    try:
        # 병렬 5개로 실행
        crawler.crawl_all_companies_parallel(
            articles_per_month=300,
            months=12,
            parallel=5  # 5개 동시 실행
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        traceback.print_exc()
    finally:
        print("\n👋 크롤러 종료")