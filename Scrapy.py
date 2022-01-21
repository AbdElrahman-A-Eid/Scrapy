import csv, time, os
from datetime import datetime, timedelta
import dateutil.relativedelta as rd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from __init__ import dirname, config, get_driver

# Initialize path to data folder variable
scrapped_data_path = f"{dirname}/Wuzzuf Scraped Data/"

# Check if the scrapped data folder exists, if not create it
if not os.path.exists(scrapped_data_path):
    os.mkdir(scrapped_data_path)

# Defining a function to convert time posting to actual date and time
def convert_datetime(str_time):
    """Returns the date and time converted from the relative str format
    
    Args:
        (str): the time in the format of '3 days ago' for example
        
    Returns:
        (str): the date time representation in the format of 'dd/mm/YYYY HH:MM'"""
    str_time = str_time.split(' ')
    digit = int(str_time[0])
    category = str_time[1]
    time_now = datetime.now()
    if category.find('day') != -1:
        new_time = time_now - timedelta(days=digit)
    elif category.find('hour') != -1:
        new_time = time_now - timedelta(hours=digit)
    elif category.find('minute') != -1:
        new_time = time_now - timedelta(minutes=digit)
    elif category.find('month') != -1:
        new_time = time_now - rd.relativedelta(months=digit)
    elif category.find('year') != -1:
        new_time = time_now - rd.relativedelta(years=digit)
    elif category.find('second') != -1:
        new_time = time_now - timedelta(seconds=digit)

    return datetime.strftime(new_time, config['datetime_format'])

# Initiate an zero counter to keep track of jobs
jobs_count = 0

# Initiate an zero counter to keep track of search pages
pages_count = 0

# Getting User Input for seach query
search_query = input('Please specify the search query for the jobs you would like to scrape: ')
while not search_query.replace(' ', '').isalnum():
    search_query = input('Please specify the search query for the jobs you would like to scrape (Letters and numbers only): ')
search_query = search_query.strip()

# Getting User Input for required pages count
required_pages = input('Please specify how many result pages you would like to scrape: ')
while not required_pages.isnumeric():
    required_pages = input('Please specify how many result pages you would like to scrape (valid positive integer): ')
required_pages = int(required_pages)

# The link to the webpage to be scrapped:
LINK = f"https://wuzzuf.net/search/jobs/?q={'+'.join(search_query.split(' '))}&a=hpb"

# Record the starting time to calculate duration
start_time = time.time()

# Initiate a Context Manager for the CSV file
with open(f"{scrapped_data_path}{datetime.strftime(datetime.now(), '%Y%m%d%H%M')}_{'-'.join(search_query.split(' '))}.csv", 'w', encoding='utf-8', newline='') as csvfile:

    # Initiating CSV file header row and delimiter
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(
        ['Job Title', 'Company', 'Company Address', 'Posting Time', 'Job Type(s)', 'Career Level',
         'Years of Experience', 'Industries', 'Skill(s)', 'Link'])

    # Initializing a Context Manager for the ChromeDriver for better environment managment
    with get_driver() as driver:

        # Maximize Browser Window
        driver.maximize_window()

        # Initialize a flag 
        content_available = 1

        # Open the required link in browser
        driver.get(LINK)

        while pages_count < required_pages and content_available:
            # Increasing pages count
            pages_count += 1

            # Initializing a generator for the jobs data (A job at a time) to ensure
            # better memory management. Using WebDriverWait to allow the WebElements to be
            # loaded before accessing them.
            try:
                jobs_postings = [item for item in WebDriverWait(driver, 50).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="css-pkv5jc"]')))
                ]
            except Exception as e:
                print(f"{type(e)}: {e}")
                content_available = 0
                break

            # Iterating over the job details generator
            for job in jobs_postings:

                # Accessing the job title and Link
                job_title = job.find_element(
                    By.XPATH, './*/h2/a[@class="css-o171kl"]')
                job_title_text = job_title.text
                job_link = job_title.get_attribute('href')

                # Accessing the company name and trimming extra characters
                company_name = job.find_element(
                    By.XPATH, './*/div[@class="css-d7j1kk"]/a').text[:-2]

                # Accessing the company address
                company_address = job.find_element(
                    By.XPATH, './*/div[@class="css-d7j1kk"]/span').text

                # Accessing the job posing time
                job_time = convert_datetime(job.find_element(
                    By.XPATH, './div[@class="css-laomuu"]/div/div').text)

                # Accessing the job type
                job_types = job.find_elements(
                    By.XPATH, './div[@class="css-y4udm8"]/div[@class="css-1lh32fc"]/a/span')
                job_types = [type.text for type in job_types]

                # Accessing the job career level
                career_level = job.find_element(
                    By.XPATH, './div[@class="css-y4udm8"]/div[2]/a[1]').text

                # Accessing the job years of experience and trimming extra characters
                try:
                    exp_years = job.find_element(
                        By.XPATH, './div[@class="css-y4udm8"]/div[2]/span[1]').text[2:]
                except Exception:
                    exp_years = ''

                # Accessing the industries involved for this job and trimming extra characters
                try:
                    industries = job.find_elements(
                        By.XPATH, './div[@class="css-y4udm8"]/div[2]/a[@class="css-o171kl"][position() > 1]')
                    industries = [industry.text[2:].strip() for industry in industries]
                except Exception:
                    industries = ['']

                # Accessing the job required skills and trim extra characters in case they exist
                try:
                    job_skills = job.find_elements(
                        By.XPATH, './div[@class="css-y4udm8"]/div[2]/a[@class="css-5x9pm1"]')
                    job_skills = [skill.text[2:].strip() if skill.text[:2] == '· ' else skill.text.strip() for skill in job_skills]
                except Exception:
                    job_skills = ['']

                # Organize job data in a list in preparation to append to the CSV file
                # Company industry list and job skills list are joined as a string
                job_l = [job_title_text, company_name, company_address, job_time, ' | '.join(job_types), career_level,
                        exp_years, ' | '.join(industries), ' | '.join(job_skills), job_link]

                # Increment the jobs counter
                jobs_count += 1

                # Append book details row to the CSV file
                csvwriter.writerow(job_l)


            # Chcking if there is a next page button and clicking it
            try:
                if pages_count < required_pages:
                    driver.find_element(By.XPATH, '//li[position()>2]/button[@class="css-zye1os ezfki8j0"]').click()
                    print(f"Navigating to page no. {pages_count + 1}...")
                    # Wait untill the old page become stale to allow the page to load when clicking next
                    WebDriverWait(driver, 10).until(
                        EC.staleness_of(job_title)
                    )
            except Exception:
                if pages_count < required_pages:
                    content_available = 0
                    print('No more pages available!')


# Record end time to calculate duration
end_time = time.time()

# Print the operation summary along with the duration taken
print(f"{jobs_count} Job Postings over {pages_count} pages have been scraped successfully as a csv file!\nOperation took {round(end_time-start_time, 2)} seconds!")

# Created by AbdElrahman Eid as part of ITI AI-Pro Course | Yinshe | Piain
