from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup, Tag

import pandas as pd
import time


# create an empty list of said length --> used for creating the data frame
def dummyList(length: int) -> list[None]:
    return [None] * length


def buildNamedEmptyDataFrame(length: int, columns: list[str]) -> pd.DataFrame:
    dataframe = pd.DataFrame()
    for column in columns:
        dataframe[column] = dummyList(length)
    return dataframe


def calculateNumPeople(web_driver: webdriver.Chrome) -> int:
    element = web_driver.find_element(By.XPATH, '//*[@id="people-search"]/span')
    value = element.text.split(")")[0].split("(")[1]
    return int(value)


CONTACT_CATEGORIES = [
    'ZoomInfo Contact ID', 'Last Name', 'First Name', 'Middle Name',
    'Salutation', 'Suffix', 'Job Title', 'Job Function', 'Management Level',
    'Company Division Name', 'Direct Phone Number', 'Email Address',
    'Email Domain', 'Department', 'Contact Accuracy Score',
    'Contact Accuracy Grade', 'ZoomInfo Contact Profile URL',
    'LinkedIn Contact Profile URL', 'Notice Provided Date',
    'Person Street', 'Person City', 'Person State',
    'Person Zip Code', 'Country', 'ZoomInfo Company ID',
    'Company Name', 'Website', 'Founded Year', 'Company HQ Phone',
    'Fax', 'Ticker', 'Revenue (in 000s USD)', 'Revenue Range (in USD)',
    'Employees', 'Employee Range', 'SIC Code 1', 'SIC Code 2', 'SIC Codes',
    'NAICS Code 1', 'NAICS Code 2', 'NAICS Codes', 'Primary Industry',
    'Primary Sub-Industry', 'All Industries', 'All Sub-Industries',
    'Industry Hierarchical Category', 'Secondary Industry Hierarchical Category',
    'Alexa Rank', 'ZoomInfo Company Profile URL', 'LinkedIn Company Profile URL',
    'Facebook Company Profile URL', 'Twitter Company Profile URL',
    'Ownership Type', 'Business Model', 'Certified Active Company',
    'Certification Date', 'Total Funding Amount (in 000s USD)',
    'Recent Funding Amount (in 000s USD)', 'Recent Funding Round',
    'Recent Funding Date', 'Recent Investors', 'All Investors',
    'Company Street Address', 'Company City', 'Company State',
    'Company Zip Code', 'Company Country', 'Full Address',
    'Number of Locations', 'Query Name'
]

theUsername = ...
thePassword = ...
searchPrompt = "Elon Musk"

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://login.zoominfo.com')

# find and put in the username
elem = driver.find_element(By.XPATH, '//*[@id="okta-signin-username"]')
elem.click()
elem.send_keys(theUsername)
elem.send_keys(Keys.RETURN)

# find and put in the password
elem = driver.find_element(By.XPATH, '//*[@id="okta-signin-password"]')
elem.click()
elem.send_keys(thePassword)
elem.send_keys(Keys.RETURN)

# wait for verification code entry
while "login" in driver.current_url:
    time.sleep(1)

driver.get("https://app.zoominfo.com/#/apps/search/v2/saved")
time.sleep(5)
elem = driver.find_element(By.XPATH, '//*[@id="app-wrapper"]/div[2]/dozi-root/zi-pages/div/div/div/div/zi-search-core'
                                     '-container-v2/div/div/div[1]/zi-filters-ng/div/div/div['
                                     '2]/zi-shared-filters-container-ng/div[1]/div[2]/div/span')
elem.click()
time.sleep(5)
elem = driver.find_element(By.XPATH, '//*[@id="contact-name-filter-header"]/div/span')
elem.click()
time.sleep(5)
elem = driver.find_element(By.XPATH, '//*[@id="full-name-freetext-filter"]')
elem.send_keys(searchPrompt)
elem.send_keys(Keys.RETURN)
time.sleep(5)

tableDiv = driver.find_element(By.XPATH, '//*[@id="pr_id_1"]/div[1]')

numPeople = calculateNumPeople(driver)
print(numPeople)
df = buildNamedEmptyDataFrame(numPeople, CONTACT_CATEGORIES)

soup = BeautifulSoup(driver.page_source, features='lxml')
linkElems: list[Tag] = soup.findAll(name='a', href=True)

for i in range(0, min(2000, len(linkElems))):
    pass
