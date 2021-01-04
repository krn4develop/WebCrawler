from urllib.parse import urlparse
import requests
from bs4 import *
from urllib import parse
from collections import Counter
import re


# Requesting user for input to crawl
url = input("Enter the URL you want to crawl: ")
depth = int(input("Enter the jumps you want to make for extracting links: "))

# parsing URL address for accessing domain name only
domain = urlparse(url).netloc

# requesting the target url for its content and get a response back
response = requests.get(url)

# using BeautifulSoup to convert the text
soup = BeautifulSoup(response.content, 'html.parser')

# Creating empty list to save all the links
every_links = set()


# Extract the links from the site and append to the list for storing the links
def link_extractor():
    page = 0
    while page <= depth:
        for i in soup.find_all('a'):
            href = i.get('href')
            full_url = parse.urljoin(url, href)
            split_url = urlparse(full_url).netloc
            if split_url == domain:
                every_links.update([full_url])
        page += 1
    print("The links in the page are: ", every_links)


# function to extract email address, phone number, comments, and most common words
def automatic_extract():
    # Extract email address from the site using regular expression
    email_extract = re.findall(r'[\w.-]+@[\w.-]+', soup.text)
    if email_extract:
        print("The email address in the page are: ", email_extract)
    else:
        print("There are no email address in this page.")

    # Extract phone numbers from the site using regular expression
    phone_extract = re.findall(r'[+(]?[1-9][0-9 .\-()]{8,}[0-9]', soup.text)
    if phone_extract:
        print("The phone numbers in the page are: ", phone_extract)
    else:
        print("There are no phone numbers in this page.")

    # Extract comments from the site using regular expression
    comment_box = []
    comment_extract = re.findall(r'<!--(.*?)-->', str(soup))
    for line in enumerate(comment_extract):
        comment_box.append(line)
    if comment_box:
        print("The line number and comment of the web page in the format of (Line number, comment): ", comment_box)
    else:
        print("There are no comments in the source code of this page.")

    # Find out the most common word found in the web page
    all_words = soup.text.split()
    counter = Counter(all_words)
    most_common_word = counter.most_common(10)
    print("The most common word in this web page in the format of (word, count) is: ", most_common_word)


# function to identify special words through regular expression defined by the users
def match_data():
    special_data = str(input("Enter regular expression you want to match: "))
    match = re.findall(special_data, soup.text)
    if match:
        print("The matched data are: ", match)
    else:
        print("There is no matching data in this page as per your entry.")


# Calling function
link_extractor()
match_data()
automatic_extract()
