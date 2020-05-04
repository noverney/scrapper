# 
# Author: Normand Overney
#    
import xlrd
from utils.parse_page import get_download_links
from utils.parse_page import download_from_link
import time

def read_spreadsheet(spreedsheet, col):
    workbook = xlrd.open_workbook(spreedsheet)
    worksheet = workbook.sheet_by_index(0)
    return worksheet.col(col)

def get_springer_books(spreedsheet, col):
    start = time.time()
    tags = ["pdf", "epub"]
    urls = read_spreadsheet(spreedsheet, col)[1:]
    number_urls = len(urls)
    for i,url in enumerate(urls):
        url = url.value
        links = get_download_links(url,tags)
        for link in links:
            download_from_link(link, "D:\\books")
            time.sleep(1)
        print(f"Done with: {i+1}/{number_urls}")
    print(f"Total Time: {time.time()-start}")
 
if __name__ == "__main__":
    spreedsheet = "Free+English+textbooks.xlsx"
    get_springer_books(spreedsheet, 18)