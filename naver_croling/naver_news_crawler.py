"""
기존 CSV 파일 본문 보완 크롤러
본문이 없는 기사만 다시 크롤링하여 업데이트
실패 사유별 통계 포함
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import re
import glob

class ContentUpdater:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--page-load-strategy=eager')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(8)

    def extract_article_content(self, url, max_retries=2):
        """기사 페이지에서 본문 1~3줄 추출"""
        original_window = self.driver.current_window_handle

        for attempt in range(max_retries):
            try:
                self.driver.execute_script(f"window.open('{url}', '_blank');")
                WebDriverWait(self.driver, 3).until(lambda d: len(d.window_handles) > 1)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(1)

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
                        content_elem = WebDriverWait(self.driver, 2).until(
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

    def update_csv_file(self, csv_path):
        """CSV 파일의 본문 없는 기사만 크롤링하여 업데이트"""

        print(f"\n{'='*70}")
        print(f"📄 파일: {os.path.basename(csv_path)}")
        print(f"{'='*70}")

        try:
            df = pd.read_csv(csv_path)

            if 'content' not in df.columns:
                df['content'] = ''

            missing_content = df['content'].isna() | (df['content'] == '') | (df['content'].astype(str).str.strip() == '')
            missing_count = missing_content.sum()
            total_count = len(df)

            print(f"📊 전체: {total_count}개")
            print(f"✅ 본문 있음: {total_count - missing_count}개")
            print(f"❌ 본문 없음: {missing_count}개")

            if missing_count == 0:
                print(f"✓ 모든 기사에 본문 있음. 스킵!")
                return df

            print(f"\n📝 본문 크롤링 시작 ({missing_count}개)")

            success = 0
            fail = 0

            fail_reasons = {
                'url_missing': 0,
                'no_selector_found': 0,
                'load_error': 0,
                'other': 0,
            }

            for idx in df[missing_content].index:
                try:
                    url = str(df.at[idx, 'url']).strip()

                    if not url or url.lower() == 'nan':
                        fail_reasons['url_missing'] += 1
                        fail += 1
                        continue

                    print(f"  [{success + fail + 1}/{missing_count}] 크롤링 중...", end='\r')

                    content = self.extract_article_content(url)

                    if content:
                        df.at[idx, 'content'] = content
                        success += 1
                    else:
                        fail += 1
                        fail_reasons['no_selector_found'] += 1

                except Exception as e:
                    fail += 1
                    error_msg = str(e).lower()
                    if 'timeout' in error_msg or 'chrome' in error_msg or 'load' in error_msg:
                        fail_reasons['load_error'] += 1
                    else:
                        fail_reasons['other'] += 1

                if (success + fail) % 20 == 0:
                    print(f"  [{success + fail}/{missing_count}] 성공: {success}, 실패: {fail}")

                time.sleep(0.3)

            print(f"\n✅ 크롤링 완료!")
            print(f"   성공: {success}개")
            print(f"   실패: {fail}개")

            print(f"\n📉 실패 사유 통계:")
            for reason, count in fail_reasons.items():
                label = {
                    'url_missing': "🔗 링크 없음",
                    'no_selector_found': "🧱 본문 태그 없음",
                    'load_error': "⏳ 페이지 로딩 실패",
                    'other': "❗ 기타 예외"
                }.get(reason, reason)
                print(f"   {label:<20}: {count}건")

            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"💾 저장 완료: {csv_path}")

            return df

        except Exception as e:
            print(f"❌ 파일 처리 실패: {e}")
            import traceback
            traceback.print_exc()
            return None

    def update_all_files(self, folder_path='naver_news_data', exclude_patterns=None):
        """폴더 내 모든 CSV 파일 업데이트"""

        if exclude_patterns is None:
            exclude_patterns = ['SK하이닉스', '삼성전자_news', '현대자동차_news']

        print(f"\n🚀 CSV 파일 본문 보완 시작")
        print(f"📁 폴더: {folder_path}")
        print(f"🚫 제외 패턴: {', '.join(exclude_patterns)}")
        print(f"{'='*70}\n")

        csv_files = glob.glob(f"{folder_path}/*.csv")

        filtered_files = []
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            should_exclude = any(filename.startswith(pattern) for pattern in exclude_patterns)
            if should_exclude:
                print(f"⏭️  제외: {filename}")
            else:
                filtered_files.append(csv_file)

        print(f"\n📋 처리 대상: {len(filtered_files)}개 파일")
        for f in filtered_files:
            print(f"   • {os.path.basename(f)}")

        if not filtered_files:
            print("\n⚠️ 처리할 파일이 없습니다.")
            return

        print()

        results = {}
        start_time = time.time()

        for i, csv_file in enumerate(filtered_files, 1):
            print(f"\n[{i}/{len(filtered_files)}]")
            df = self.update_csv_file(csv_file)
            results[csv_file] = df

            if i < len(filtered_files):
                print(f"\n⏳ 다음 파일까지 3초 대기...")
                time.sleep(3)

        elapsed_time = time.time() - start_time

        print(f"\n{'='*70}")
        print(f"🎉 전체 작업 완료!")
        print(f"⏱️  소요 시간: {elapsed_time/60:.1f}분")
        print(f"{'='*70}\n")

        print("📊 최종 결과:")
        for csv_file, df in results.items():
            if df is not None:
                filename = os.path.basename(csv_file)
                total = len(df)
                with_content = df['content'].notna().sum()
                print(f"  ✓ {filename}: {with_content}/{total}개 본문 있음")
            else:
                print(f"  ✗ {os.path.basename(csv_file)}: 실패")

        print(f"\n💾 저장 위치: {folder_path}/")

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    print("="*70)
    print("📝 기존 CSV 파일 본문 보완 크롤러")
    print("="*70)
    print("✅ 본문 있는 기사: 유지")
    print("❌ 본문 없는 기사: 다시 크롤링")
    print("🚫 제외: SK하이닉스, 삼성전자_news, 현대자동차_news로 시작하는 파일")
    print("="*70)

    folder = input("\nCSV 파일이 있는 폴더 경로 (엔터=naver_news_data): ").strip()
    if not folder:
        folder = "naver_news_data"

    response = input(f"\n'{folder}' 폴더의 파일들을 처리하시겠습니까? (y/n): ")

    if response.lower() != 'y':
        print("취소되었습니다.")
        exit()

    updater = ContentUpdater()

    try:
        exclude_patterns = ['SK하이닉스', '삼성전자_news', '현대자동차_news']
        updater.update_all_files(
            folder_path=folder,
            exclude_patterns=exclude_patterns
        )
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        updater.close()
        print("\n👋 크롤러 종료")
