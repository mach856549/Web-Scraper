import requests
import re
import string
import os

from bs4 import BeautifulSoup


def main():
    global user_url, num_pages, article_type, cwd, new_dir
    cwd = os.getcwd()
    user_url = "https://www.nature.com"
    user_url_page = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page="
    num_pages = int(input())
    article_type = input()
    for i in range(1, num_pages + 1):
        response = get_response(user_url_page + str(i))
        new_dir = os.path.join(cwd, "Page_" + str(i))
        if os.access(new_dir, os.F_OK):
            pass
        else:
            os.mkdir(new_dir)
        response_handler1(response)
    print("Saved all articles.")


def get_response(url, params_=None):
    local_response = requests.get(url, params_)
    if local_response.status_code == 200:
        return local_response
    else:
        print(f"The URL returned {local_response.status_code}!")
        exit()


def write_file(data_, file_name):
    file = open(os.path.join(new_dir, file_name), 'wb')
    file.write(data_)
    file.close()


def response_handler1(response_local):
    if response_local.status_code == 200:
        soup = BeautifulSoup(response_local.content, "html.parser")
        articles_ = soup.find_all("article")
        # The item below is a filtered list of articles that have the meta__type = article_type
        articles_filtered = [article for article in articles_
                             if article.find('span', class_='c-meta__type').text == article_type]
        for article in articles_filtered:
            title = article.find("a").text
            url = article.find("a").get('href')
            response_article(user_url + url, title)
    else:
        error_handle()


def strip_title(title1):
    title = title1.strip()
    intab = string.punctuation + " "
    n = len(intab) - 1
    outtab = " " * n + "_"
    trantab = str.maketrans(intab, outtab)
    return title.translate(trantab).replace(" ", "")


def response_article(url, title):
    title_processed = strip_title(title)
    article_response = get_response(url)
    soup_article = BeautifulSoup(article_response.content, "html.parser")
    data = soup_article.find("div", class_=re.compile("body")).text
    data_bytes = bytes(data.strip(), encoding="utf-8")
    write_file(data_bytes, title_processed + ".txt")


def error_handle():
    print("Invalid movie page!")


main()
