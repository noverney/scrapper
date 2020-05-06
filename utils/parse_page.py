#
# Author: Normand Overney 
#


# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import os
import time

def get_download_links(url, tags, add_attr="title"):
    # Connect to the URL
    response = requests.get(url)
    base_url = "https://"+urlparse(url, scheme="http").netloc
    # Parse HTML and save to BeautifulSoup object¶
    soup = BeautifulSoup(response.text, "html.parser")
    download_links = []
    # To download the whole data set, let's do a for loop through all a tags
    for one_a_tag in soup.findAll('a'):  #'a' tags are for links
        link = one_a_tag['href']
        if any([True if x in link else False for x in tags]) and add_attr in str(one_a_tag):
            download_links.append(urljoin(base_url,link))
    # page extraction goes here
    soup.decompose()
    return list(set(download_links))

def download_from_link(url, path, chunk_size=2000):
    start = time.time()
    r = requests.get(url, stream=True)
    name = url.split("/")[-1]
    with open(os.path.join(path,name), 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(f"Time: {time.time()-start}")