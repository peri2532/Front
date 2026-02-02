"""
실패한 기사 본문 재수집 크롤러
본문이 없거나 짧은 기사만 다시 추출
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import os
import re
import glob

class ContentRetryExtractor:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--page-load-strategy=eager')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(10)
    
    def extract_content_smart(self, url, max_retries=2):
        """향상된 본문 추출 - 100개 이상의 선택자 시도"""
        original_window = self.driver.current_window_handle
        
        for attempt in range(max_retries):
            try:
                # 새 탭에서 열기
                self.driver.execute_script(f"window.open('{url}', '_blank');")
                WebDriverWait(self.driver, 5).until(lambda d: len(d.window_handles) > 1)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(2)
                
                content_text = ""
                
                # ========================================
                # 전략 1: ID 선택자 (가장 정확함)
                # ========================================
                id_selectors = [
                    'dic_area', 'articleBodyContents', 'articeBody', 'articleBody',
                    'article-body', 'article_body', 'news-body-area', 'newsBody',
                    'content', 'article-content', 'news_content', 'story_body',
                    'main-content', 'article_content', 'post-content', 'entry-content',
                ]
                
                for selector_id in id_selectors:
                    try:
                        elem = self.driver.find_element(By.ID, selector_id)
                        text = elem.text.strip()
                        if text and len(text) > 50:
                            content_text = text
                            break
                    except:
                        continue
                
                # ========================================
                # 전략 2: Class 선택자 (일반적)
                # ========================================
                if not content_text:
                    class_selectors = [
                        'article_view', 'article-view', 'article_body', 'article-body',
                        'article-text', 'article-content', 'news_body', 'news-body',
                        'news_view', 'news-view', 'view_body', 'view-body',
                        'news-article-body', 'news_article_body', 'detail_body',
                        'detail-body', 'content_view', 'content-view', 'txt_article',
                        'read_body', 'read-body', 'article_txt', 'article-txt',
                        'post_article', 'post-article', 'entry_content', 'entry-content',
                        'story_body', 'story-body', 'main_article', 'main-article',
                        'news_article', 'news-article', 'art_body', 'art-body',
                    ]
                    
                    for class_name in class_selectors:
                        try:
                            elem = self.driver.find_element(By.CLASS_NAME, class_name)
                            text = elem.text.strip()
                            if text and len(text) > 50:
                                content_text = text
                                break
                        except:
                            continue
                
                # ========================================
                # 전략 3: CSS 복합 선택자
                # ========================================
                if not content_text:
                    css_selectors = [
                        'div#dic_area', 'div#articleBodyContents', 'div.article_body',
                        'div.article_view', 'div.article-body', 'div.news_body',
                        'div.view_body', 'div.news-article-body', 'div.detail_body',
                        'section.article_view', 'section.article-view', 'section.news_body',
                        'article', 'article.article', 'article.post', 'article.news',
                        'div[itemprop="articleBody"]', 'div[id*="article"]', 'div[id*="content"]',
                        'div[class*="article"]', 'div[class*="content"]', 'div[class*="body"]',
                        '.article_body .article_view', '.news_body .news_view',
                        'main article', 'main .article', 'main .content',
                        '#content article', '#content .article', '#main article',
                        '.post-content', '.entry-content', '.story-body',
                    ]
                    
                    for selector in css_selectors:
                        try:
                            elem = WebDriverWait(self.driver, 2).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            text = elem.text.strip()
                            if text and len(text) > 50:
                                content_text = text
                                break
                        except:
                            continue
                
                # ========================================
                # 전략 4: XPath (강력함)
                # ========================================
                if not content_text:
                    xpath_selectors = [
                        '//div[contains(@id, "article")]',
                        '//div[contains(@id, "content")]',
                        '//div[contains(@class, "article")]',
                        '//div[contains(@class, "content")]',
                        '//div[contains(@class, "body")]',
                        '//article',
                        '//section[contains(@class, "article")]',
                        '//*[@itemprop="articleBody"]',
                        '//div[@id="newsBody"]',
                        '//div[@class="news_body"]',
                    ]
                    
                    for xpath in xpath_selectors:
                        try:
                            elem = self.driver.find_element(By.XPATH, xpath)
                            text = elem.text.strip()
                            if text and len(text) > 50:
                                content_text = text
                                break
                        except:
                            continue
                
                # ========================================
                # 전략 5: 태그명으로 찾기 (마지막 수단)
                # ========================================
                if not content_text:
                    try:
                        # article 태그 찾기
                        articles = self.driver.find_elements(By.TAG_NAME, 'article')
                        for article in articles:
                            text = article.text.strip()
                            if text and len(text) > 100:  # 더 긴 텍스트만
                                content_text = text
                                break
                    except:
                        pass
                
                # ========================================
                # 전략 6: 본문 추정 (모든 p 태그 수집)
                # ========================================
                if not content_text:
                    try:
                        # 모든 p 태그 찾기
                        paragraphs = self.driver.find_elements(By.TAG_NAME, 'p')
                        long_paragraphs = []
                        
                        for p in paragraphs:
                            text = p.text.strip()
                            # 긴 문단만 (광고/링크 제외)
                            if len(text) > 30 and '©' not in text and 'http' not in text:
                                long_paragraphs.append(text)
                        
                        if len(long_paragraphs) >= 2:
                            content_text = ' '.join(long_paragraphs[:5])
                    except:
                        pass
                
                # ========================================
                # 본문 정리 및 1-3줄 추출
                # ========================================
                if content_text:
                    lines = []
                    for line in content_text.split('\n'):
                        line = line.strip()
                        
                        # 필터링
                        if len(line) < 10:
                            continue
                        if '기자' in line and len(line) < 30:
                            continue
                        if re.match(r'^\d{4}[-./]\d{1,2}[-./]\d{1,2}', line):
                            continue
                        if line.startswith('[') and line.endswith(']'):
                            continue
                        if '무단전재' in line or '재배포' in line or '저작권' in line:
                            continue
                        if '©' in line or 'copyright' in line.lower():
                            continue
                        if line.startswith('▶') or line.startswith('◆'):
                            continue
                        
                        lines.append(line)
                        
                        if len(lines) >= 3:
                            break
                    
                    result = ' '.join(lines[:3])
                    
                    if len(result) > 300:
                        result = result[:300] + '...'
                    
                    # 최소 길이 체크
                    if len(result) >= 20:
                        self.driver.close()
                        self.driver.switch_to.window(original_window)
                        return result
                
                # 실패
                self.driver.close()
                self.driver.switch_to.window(original_window)
                
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    return ""
                
            except Exception as e:
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
    
    def retry_failed_articles(self, csv_file, min_content_length=20):
        """본문이 없거나 짧은 기사만 재추출"""
        print(f"\n{'='*70}")
        print(f"📝 실패 기사 재추출: {csv_file}")
        print(f"{'='*70}\n")
        
        # CSV 읽기
        df = pd.read_csv(csv_file)
        
        # 실패한 기사 찾기 (본문 없거나 짧음)
        failed_mask = df['content'].isna() | (df['content'].str.len() < min_content_length)
        failed_df = df[failed_mask].copy()
        
        total = len(df)
        failed_count = len(failed_df)
        success_count = total - failed_count
        
        print(f"📊 통계:")
        print(f"  전체 기사: {total}개")
        print(f"  성공: {success_count}개 ({success_count/total*100:.1f}%)")
        print(f"  실패: {failed_count}개 ({failed_count/total*100:.1f}%)")
        
        if failed_count == 0:
            print(f"\n✅ 모든 기사에 본문이 있습니다!")
            self.driver.quit()
            return df
        
        print(f"\n🔄 {failed_count}개 기사 재시도 중...\n")
        
        # 재시도
        retry_success = 0
        retry_fail = 0
        
        for idx, row_idx in enumerate(failed_df.index, 1):
            try:
                url = df.at[row_idx, 'url']
                content = self.extract_content_smart(url)
                
                if content and len(content) >= min_content_length:
                    df.at[row_idx, 'content'] = content
                    retry_success += 1
                else:
                    retry_fail += 1
                
                if idx % 20 == 0:
                    print(f"  → {idx}/{failed_count} (성공: {retry_success}, 실패: {retry_fail})")
                
                time.sleep(0.5)
                
            except Exception as e:
                retry_fail += 1
        
        print(f"\n✅ 재시도 완료!")
        print(f"  추가 성공: {retry_success}개")
        print(f"  여전히 실패: {retry_fail}개")
        
        # 최종 통계
        final_success = success_count + retry_success
        final_fail = retry_fail
        
        print(f"\n📊 최종 결과:")
        print(f"  성공: {final_success}개 ({final_success/total*100:.1f}%)")
        print(f"  실패: {final_fail}개 ({final_fail/total*100:.1f}%)")
        
        # 저장
        output_file = csv_file.replace('.csv', '_retry.csv')
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 저장: {output_file}")
        
        self.driver.quit()
        return df
    
    def retry_all_files(self, folder='naver_news_data'):
        """폴더 내 모든 CSV 파일 재시도"""
        print(f"\n{'='*70}")
        print(f"📁 폴더 내 모든 파일 재처리: {folder}")
        print(f"{'='*70}\n")
        
        # CSV 파일 찾기
        csv_files = glob.glob(f'{folder}/*_monthly_*.csv')
        
        if not csv_files:
            print("❌ CSV 파일을 찾을 수 없습니다!")
            return
        
        print(f"✓ {len(csv_files)}개 파일 발견\n")
        
        for i, csv_file in enumerate(csv_files, 1):
            company_name = csv_file.split('/')[-1].split('_monthly_')[0]
            
            # retry 파일은 건너뛰기
            if '_retry' in csv_file:
                continue
            
            print(f"\n[{i}/{len(csv_files)}] {company_name}")
            print("-" * 70)
            
            try:
                self.retry_failed_articles(csv_file)
            except Exception as e:
                print(f"❌ {company_name} 실패: {e}")
                continue
            
            print()
        
        print(f"\n{'='*70}")
        print(f"🎉 전체 재처리 완료!")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    print("="*70)
    print("📝 네이버 뉴스 본문 재추출 크롤러")
    print("="*70)
    print("실패한 기사(본문 없음/짧음)만 다시 추출합니다.")
    print("100개 이상의 선택자로 최대한 많이 추출합니다.")
    print("="*70)
    
    print("\n옵션을 선택하세요:")
    print("1. 특정 파일만 재시도")
    print("2. naver_news_data 폴더 전체 재시도")
    
    choice = input("\n선택 (1 or 2): ")
    
    extractor = ContentRetryExtractor()
    
    try:
        if choice == '1':
            # 파일 목록 보여주기
            csv_files = glob.glob('naver_news_data/*_monthly_*.csv')
            
            print("\n파일 목록:")
            for i, f in enumerate(csv_files, 1):
                if '_retry' not in f:
                    company = f.split('/')[-1].split('_monthly_')[0]
                    print(f"{i}. {company}")
            
            file_num = int(input("\n파일 번호: ")) - 1
            extractor.retry_failed_articles(csv_files[file_num])
            
        elif choice == '2':
            extractor.retry_all_files()
        
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            extractor.driver.quit()
        except:
            pass
        print("\n👋 종료")