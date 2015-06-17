from urlparse import urljoin
import datetime
from mining_source import Source
import mysql.connector

__author__ = 'Shengnuo'
from bs4 import BeautifulSoup
import requests

class Scotia(Source):
    url = None
    def __init__(self, url):
        self.url = url


    def mining(self, db_cursor):
        current_url = self.url

        while 1:
            soup = BeautifulSoup(requests.get(current_url).content)
            rows = soup.find("table", {"class" : "info-table"}).find_all("tr")

            for job in rows[4:-1]:
                title = job.find("td",{"class":"jobTitle"}).find('a').text
                location = job.find("td",{"class":"location"}).text
                date = datetime.datetime.strptime(job.find("td",{"class":"custom1"}).text, '%m/%d/%Y').strftime('%Y-%m-%d')
                job_url = urljoin(self.url, job.find("td",{"class":"jobTitle"}).find('a').get("href"))
                id = int("10" + job.find("td", {"class":"companyName"}).text)
                try:
                    db_cursor.execute("INSERT INTO scotia VALUES (%s, %s, %s, %s, %s)", (id, title, location, date, job_url))
                except mysql.connector.errors.IntegrityError:
                    db_cursor.execute("UPDATE scotia SET title=%s, location=%s, date_posted=%s, url=%s WHERE id=%s", (title, location, date, job_url, id))

            next_page = soup.find("td", {"class":"pagination"}).find("a",{"class":"pagination-more"})
            if next_page != None:
                current_url = urljoin(self.url, next_page.get("href"))
            else: break






