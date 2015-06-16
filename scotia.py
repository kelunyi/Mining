from urlparse import urljoin
from mining_source import Source

__author__ = 'Shengnuo'
from bs4 import BeautifulSoup
import requests

class Scotia(Source):
    url = None
    __current_url = None
    __page = None
    __r = None
    __soup = None
    __rows = None

    def __init__(self, url):
        self.url = url
        self.__current_url = self.url
        self.__r = requests.get(url)
        self.__soup = BeautifulSoup(self.__r.content)
        self.__rows = self.__soup.find("table", {"class" : "info-table"}).find_all("tr")


    def mining(self, storage_file):
        self.__r = requests.get(self.__current_url)
        self.__soup = BeautifulSoup(self.__r.content)
        self.__rows = self.__soup.find("table", {"class" : "info-table"}).find_all("tr")

        for job in self.__rows[4:-1]:
            title = job.find("td",{"class":"jobTitle"}).find('a').text
            location = job.find("td",{"class":"location"}).text
            date = job.find("td",{"class":"custom1"}).text
            job_url = job.find("td",{"class":"jobTitle"}).find('a').get("href")
            storage_file.write((title + " | " + location + " | " + date).encode("utf-8"))
            storage_file.write(job_url.encode("utf-8"))

        #next_page = urljoin(self.url, self.__soup.find("td", {"class":"pagination"}).find("a",{"class":"pagination-more"}))
        next_page = self.__soup.find("td", {"class":"pagination"}).find("a",{"class":"pagination-more"})

        if next_page != None:
            next_link = urljoin(self.url, next_page.get("href"))
            self.__current_url = next_link
            self.mining(storage_file)



