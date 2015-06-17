from urlparse import urljoin
from mining_source import Source
from bs4 import BeautifulSoup
import requests
import mysql.connector


__author__ = 'Shengnuo'

class RBC(Source):
    url = None

    def __init__(self, url):
        self.url = url
        self.__current_num = 0
        self.__r = requests.get(url)
        self.__soup = BeautifulSoup(self.__r.content)
        self.__rows = self.__soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find_all("tr")
        self.__last_page = urljoin(self.url, self.__soup.find("a", {"class" : "paginationItemLast"}).get("href"))

    def mining(self, db_cursor):
        current_num = 0
        id = 200000

        while 1:
            current_url = str(self.url + `current_num` + "/?q=&sortColumn=referencedate&sortDirection=desc")
            soup = BeautifulSoup(requests.get(current_url).content)
            rows = soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find("tbody").find_all("tr")

            total_job_num = soup.find("span", {"class" : "paginationLabel"}).find_all("b")[1].text
            for job in rows[3:]:
                id += 1
                title = job.find("td",{"class":"colTitle"}).find("span").find("a").text
                location = job.find("td",{"class":"colLocation hidden-phone"}).find("span").text
                date = job.find("td",{"class":"colDate hidden-phone"}).find("span").text
                job_url = urljoin(self.url,job.find("td",{"class":"colTitle"}).find("a",{"class":"jobTitle-link"}).get("href"))
                '''
                try:
                    db_cursor.execute("INSERT INTO rbc VALUES (%s, %s, %s, %s, %s)", (id, title, location, date, job_url))
                except mysql.connector.errors.IntegrityError:
                    db_cursor.execute("UPDATE rbc SET title=%s, location=%s, date_posted=%s, url=%s WHERE id=%s", (title, location, date, job_url, id))
                '''
                db_cursor.execute("INSERT INTO rbc VALUES (%s, %s, %s, %s, %s)", (id, title, location, date, job_url))
                #print (id, title, location, date, job_url)

            '''
            current_num += 25
            if current_num + 25 > total_job_num:
                break
            '''
            break


