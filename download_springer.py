# 
# Author: Normand Overney
#    
import xlrd
from utils.parse_page import get_download_links
from utils.parse_page import download_from_link
import time
import os
import sys

def read_spreadsheet(spreedsheet, col):
    workbook = xlrd.open_workbook(spreedsheet)
    worksheet = workbook.sheet_by_index(0)
    return worksheet.col(col)

# it took: 14827.792130231857
def get_springer_books(download_dir, spreedsheet, col):
    start = time.time()
    tags = ["pdf", "epub"]
    urls = read_spreadsheet(spreedsheet, col)[1:]
    number_urls = len(urls)
    for i,url in enumerate(urls):
        url = url.value
        links = get_download_links(url,tags)
        for link in links:
            download_from_link(link, download_dir)
            time.sleep(1)
        print(f"Done with: {i+1}/{number_urls}")
    print(f"Total Time: {time.time()-start}")


def count_springer_books(spreedsheet, col):
    tags = ["pdf", "epub"]
    urls = read_spreadsheet(spreedsheet, col)[1:]
    number_urls = len(urls)
    num_books = 0
    cant_download = 0
    for i,url in enumerate(urls):
        url = url.value
        links = len(get_download_links(url,tags))
        num_books += links
        if links == 0:
            cant_download += 1
    print(f"Total Number of Books can't download: {cant_download}/{num_books}")

def get_names(spreedsheet, col, col2):
    titles = [x.value.rstrip().replace(" ", "_").replace(",","").replace(":","").replace("/", "") for x in read_spreadsheet(spreedsheet,col)]
    dois = [x.value.split("/")[-1] for x in read_spreadsheet(spreedsheet,col2)]
    # need to create valid filenames 
    assert len(titles) == len(dois)

    # if same title need to make them unique  
    uniq_titles = {}
    for index,title in enumerate(titles):
        if title not in uniq_titles:
            uniq_titles[title] = 1
        else:
            uniq_titles[title] += 1
            titles[index] = title + f"_{uniq_titles[title]}"

    assert len(set(titles)) == len(titles)
    assert len(set(dois)) == len(dois)
    return dict(zip(dois, titles))

def rename_titles(folder_path, dois_to_titles):
    filenames = os.listdir(folder_path)
    for filename in filenames:
        #print(filename)
        end = ".pdf"
        if ".pdf" not in filename:
            end = ".epub"
        key = filename.rstrip(end).split("%2F")[-1]
        if key in dois_to_titles:
            new_name = dois_to_titles[key]+end
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))

# the folder is 10.9 GB so have enough storage
# I could parallize this operation
if __name__ == "__main__":
    download_dir = sys.argv[1]
    spreedsheet = "Free+English+textbooks.xlsx"
    count_springer_books(spreedsheet, 18)
    # here is the download command and you need a specific filepath to download to
    get_springer_books(download_dir, spreedsheet, col)
    dois_to_titles = get_names(spreedsheet,0,17)
    rename_titles(download_dir, dois_to_titles)