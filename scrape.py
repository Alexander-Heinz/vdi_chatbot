from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
service = Service()  # ChromeDriver should be in PATH
driver = webdriver.Chrome(service=service, options=chrome_options)

BASE_URL = 'https://vdivde-it.de/de/faq/suche/'
START_PARAMS = '101+100+102+103+106+107+108+109+110+111+113+114+115+118+119+120+121+123+124+125+126+129+130+131+133+134+135'

def get_page(url):
    driver.get(url)
    time.sleep(2)  # Wait for JavaScript to load the content
    return driver.page_source

def click_and_get_full_answer(driver, answer_element):
    try:
        # Click on the answer element to expand it
        answer_element.click()
        # Wait for the full content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "block-vdivde-content"))
        )
        # Get the full answer HTML
        full_answer = driver.find_element(By.ID, "block-vdivde-content").get_attribute('innerHTML')
        # Navigate back
        driver.back()
        return full_answer
    except Exception as e:
        print(f"Error getting full answer: {e}")
        return None

def remove_unwanted_links(soup):
    # Find and remove links that contain "/de/faq"
    for a in soup.find_all('a', href=re.compile(r'/de/faq')):
        a.extract()
    return soup

def process_text_with_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    soup = remove_unwanted_links(soup)
    for a in soup.find_all('a', href=True):
        a.replace_with(f" {a.text} (siehe {a['href']}) ")

    # Get the text and normalize spaces
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(' .', '.').replace(' ,', ',')
    return text#soup.get_text(strip=False)

def parse_faq_page(html, category_name):
    soup = BeautifulSoup(html, 'html.parser')
    faqs = []

    # Find all question and answer elements based on the updated structure
    question_elements = soup.select('h3.card__title.publication__title span')
    answer_elements = soup.select('div.card__content > div')

    for question, answer in zip(question_elements, answer_elements):
        question_text = question.get_text(strip=True)
        answer_html = str(answer)
        
        if answer.get_text(strip=True).endswith('…'):
            # If the answer ends with '…', click to get the full answer
            full_answer = click_and_get_full_answer(driver, driver.find_element(By.XPATH, f"//span[contains(text(), '{question_text}')]"))
            if full_answer:
                answer_html = full_answer
        
        answer_text = process_text_with_links(answer_html)
        faqs.append((category_name, question_text, answer_text))
    
    return faqs

def get_category_name(html, field_faq_categories):
    soup = BeautifulSoup(html, 'html.parser')
    # Find the option tag where value matches the category number
    option_tag = soup.find('option', {'value': field_faq_categories})
    if option_tag:
        return option_tag.get_text(strip=True)
    return "Unknown Category"

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Category', 'Question', 'Answer'])
    df.to_csv(filename, index=False, encoding='utf-8')

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    all_faqs = []
    search_api_fulltext = "" 

    for field_faq_categories in range(102, 139):
        page_number = 0

        while True:
            url = f"{BASE_URL}{START_PARAMS}?field_faq_categories={field_faq_categories}&search_api_fulltext={search_api_fulltext}&page={page_number}"
            print(url)
            print(f"Scraping category {field_faq_categories}, page {page_number}...")
            html = get_page(url)
            # Get category name only on the first page of each category
            if page_number == 0:
                category_name = get_category_name(html, str(field_faq_categories))
                print(f"Category name: {category_name}")

            faqs = parse_faq_page(html, category_name)
            if not faqs:
                break
            all_faqs.extend(faqs)
            page_number += 1

    save_to_csv(all_faqs, 'faqs.csv')
    save_to_json(all_faqs, 'faqs.json')

    print("Scraping complete. FAQs saved to faqs.csv and faqs.json.")
    driver.quit()

if __name__ == '__main__':
    main()