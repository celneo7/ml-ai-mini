import time
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# base code referenced from https://www.geeksforgeeks.org/youtube-data-scraping-preprocessing-and-analysis-using-python/

urls = [ 
    'https://www.youtube.com/c/GeeksforGeeksVideos/videos',
    'https://www.youtube.com/@gmmtv/videos',
    'https://www.youtube.com/@TXT_bighit/videos',
    'https://www.youtube.com/@redvelvet/videos'
]

times = 0
rows = 0
t = v = d = []


options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for url in urls:
    driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url)) 
    for i in range(10):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')
    
    titles = [t.text for t in soup.findAll('yt-formatted-string', id = 'video-title')]
    views = [v.text for v in driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[1]')]
    durations = [d.text for d in soup.findAll('div', class_ = 'badge-shape-wiz__text')]

    workbook = xlsxwriter.Workbook(f'output_{url.split('/')[-2]}.xlsx')
    worksheet = workbook.add_worksheet()

    for col_index, item in enumerate(['title','views','duration']):
        worksheet.write(0, col_index, item)

    for index, (title, view, duration) in enumerate(zip(titles, views, durations), start=1):
        worksheet.write(index, 0, title)
        worksheet.write(index, 1, view.split(' ')[0])
        worksheet.write(index, 2, duration)

    workbook.close()