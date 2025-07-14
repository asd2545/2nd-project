import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scraping():
    base_url = "https://th.jobsdb.com"
    current_url = "https://th.jobsdb.com/th/Data-jobs"
    all_job_data = []
    
    page_count = 0

    while current_url and page_count < 5:
        print(f"Attempting to fetch: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()
            print(f"Successfully connected to {current_url}")
        except requests.exceptions.RequestException as e:
            print(f'Failed to fetch page {current_url}: {e}')
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.select('article[data-automation="normalJob"]')

        if not job_listings:
            print("No job listings found on this page. Check selectors.")
            current_url = None 
            break
            
        for job_card in job_listings:
            job_title_element = job_card.select_one('a[data-automation="jobTitle"]')
            company_title_element = job_card.select_one('a[data-automation="jobCompany"]')
            location_element = job_card.select_one('a[data-automation="jobLocation"]')

            job_title_text = job_title_element.get_text(strip=True) if job_title_element else 'N/A'
            company_title_text = company_title_element.get_text(strip=True) if company_title_element else 'N/A'
            location_text = location_element.get_text(strip=True) if location_element else 'N/A'
            
            all_job_data.append([job_title_text, company_title_text, location_text])
        
        next_page_span = soup.find('span', string='ถัดไป')
        next_page_link_element = None

        if next_page_span:
            parent_a = next_page_span.find_parent('a')
            if parent_a and 'href' in parent_a.attrs:
                next_page_link_element = parent_a
        
        if next_page_link_element:
            relative_url = next_page_link_element['href']
            current_url = base_url + relative_url
            page_count += 1
        else:
            current_url = None
            print("No more pages to scrape.")
        
    if all_job_data:
        df = pd.DataFrame(all_job_data, columns=['Job Title', 'Company Title', 'Company Location'])
        current_time = datetime.now()
        timestamp_str = current_time.strftime("%d-%m-%Y")
        file_name = f"raw_data_scraped_at {timestamp_str}.csv"       
        try:
            df.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"Successfully created: {file_name}")
        except Exception as e:
            print(f"Error saving CSV file locally: {e}")
    else:
        print("No data was scraped.")

if __name__ == "__main__":
    scraping()
