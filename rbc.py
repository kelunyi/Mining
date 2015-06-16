from urlparse import urljoin
from mining_source import Source
from bs4 import BeautifulSoup
import requests

__author__ = 'Shengnuo'

class RBC(Source):
    url = None
    __page = None
    __r = None
    __soup = None
    __rows = None
    __current_num = None
    _last_page = None

    def __init__(self, url):
        self.url = url
        self.__current_num = 0
        self.__r = requests.get(url)
        self.__soup = BeautifulSoup(self.__r.content)
        self.__rows = self.__soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find_all("tr")
        self.__last_page = urljoin(self.url, self.__soup.find("a", {"class" : "paginationItemLast"}).get("href"))

    def mining(self, storage_file):
        current_url = str(self.url + `self.__current_num` + "/?q=&sortColumn=referencedate&sortDirection=desc")
        self.__r = requests.get(current_url)

        self.__soup = BeautifulSoup(self.__r.content)
        self.__rows = self.__soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find_all("tr")


        for job in self.__rows[3:]:
            title = job.find("td",{"class":"colTitle"}).find("span").find("a").text
            location = job.find("td",{"class":"colLocation hidden-phone"}).find("span").text
            date = job.find("td",{"class":"colDate hidden-phone"}).find("span").text
            job_url = urljoin(self.url,job.find("td",{"class":"colTitle"}).find("a",{"class":"jobTitle-link"}).get("href"))
            storage_file.write(str((title + " | " + location + " | " + date).encode("utf-8")) + '\n')
            storage_file.write(str(job_url.encode("utf-8")) + '\n')
            storage_file.write('\n')

            storage_file.write('\n')


        if current_url != self.__last_page:
            self.__current_num += 25
            self.mining(storage_file)


