from urlparse import urljoin
import datetime
from os.path import isfile, join
from mining_source import Source
import mysql.connector
from bs4 import BeautifulSoup
import requests
import os
import time

import re

__author__ = 'Shengnuo'


class Scotia(Source):
    url = None
    __conn = None

    def __init__(self):
        self.url = "http://jobs.scotiabank.com/careers/it-jobs/job-list-8"
        self.__conn = mysql.connector.connect(user='root', password = 'genghiskhan', host = 'localhost', database='job_database')


    def mine_to_file(self):
        current_url = "http://jobs.scotiabank.com/careers/it-jobs/job-list-1"
        dir = os.path.dirname(__file__) + "\scotia\\"
        if not os.path.exists("scotia"): os.mkdir("scotia")


        delete_dic = {f : f for f in os.listdir(dir) if isfile(join(dir, f))}

        while 1:
            soup = BeautifulSoup(requests.get(current_url).content)
            rows = soup.find("table", {"class" : "info-table"}).find_all("tr")

            for job in rows[4:-1]:
                title = job.find("td",{"class":"jobTitle"}).find('a').text
                location = job.find("td",{"class":"location"}).text
                date = datetime.datetime.strptime(job.find("td",{"class":"custom1"}).text, '%m/%d/%Y').strftime('%Y-%m-%d')
                job_url = urljoin(self.url, job.find("td",{"class":"jobTitle"}).find('a').get("href"))
                desc_name = job_url.split("/")[-1] + ".txt"
                desc_path = dir + desc_name
                desc = self.get_desc(job_url)

                if desc_name in delete_dic:     # delete the file in the delete_dic if the job still exists
                    del delete_dic[desc_name]


                if not os.path.isfile(desc_path):       #create the file is the file DNE
                    f = open(desc_path,'w')
                    f.close()
                f = open(desc_path,'w')

                try:
                    f.write(desc)
                except IndexError:
                    print desc_path
                f.close()
                if desc_name in delete_dic:
                    del delete_dic[desc_name]

                print("minded " + desc_name.encode('utf-8'))

            #break
            next_page = soup.find("td", {"class":"pagination"}).find("a",{"class":"pagination-more"})
            if next_page != None:
                current_url = urljoin(self.url, next_page.get("href"))
            else: break
        # clean up obsolete jobs
        print("-----------------------------------------------")
        print ("jobs to delete ")
        print (delete_dic)
        time.sleep(5)
        for f in delete_dic:
            if os.path.isfile(dir + f):
                os.remove(dir + f)
                print("cleaned " + f)

    def mine_to_database(self):
        current_url = "http://jobs.scotiabank.com/careers/it-jobs/job-list-1"
        db_cursor = self.__conn.cursor()
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS job_table (
        Title VARCHAR (200),
        Company VARCHAR (45),
        Date_Posted DATE ,
        Location VARCHAR (45),
        URL VARCHAR (200),
        Description VARCHAR (10000))""")
        db_cursor.execute("SELECT * FROM job_table")
        delete_dic = {item[4]:item[4] for item in db_cursor.fetchall() if item[1] == "Scotia Bank"}

        while 1:
            soup = BeautifulSoup(requests.get(current_url).content)
            rows = soup.find("table", {"class" : "info-table"}).find_all("tr")


            for job in rows[4:-1]:
                title = job.find("td",{"class":"jobTitle"}).find('a').text
                location = job.find("td",{"class":"location"}).text
                date = datetime.datetime.strptime(job.find("td",{"class":"custom1"}).text, '%m/%d/%Y').strftime('%Y-%m-%d')
                job_url = urljoin(self.url, job.find("td",{"class":"jobTitle"}).find('a').get("href"))
                desc = self.get_desc(job_url)
                if job_url in delete_dic:     # delete the file in the delete_dic if the job still exists
                    del delete_dic[job_url]

                try:
                    db_cursor.execute("INSERT INTO job_table VALUES (%s, %s, %s, %s, %s, %s)", (title, "Scotia Bank", date, location,  job_url, desc))
                except mysql.connector.errors.IntegrityError:
                    db_cursor.execute("UPDATE job_table SET Title=%s, Company=%s, Date_Posted=%s, Location=%s, Description=%s WHERE URL=%s", (title, "Scotia Bank",  date, location, desc, job_url))

            #break
            next_page = soup.find("td", {"class":"pagination"}).find("a",{"class":"pagination-more"})
            if next_page != None:
                current_url = urljoin(self.url, next_page.get("href"))
            else: break

        for f in delete_dic:
            db_cursor.execute("DELETE FROM job_table WHERE URL = '%s'", f)

        self.__conn.commit()
        db_cursor.close()


    def get_desc(self,url):
        desc = ""
        keyword_list = ["description", "key accountabilities", "key accountability" , "purpose",  "responsibility", "responsibilities", "duty", "duties", "qualification","education", "requirement", "degree"]

        desc_block = BeautifulSoup(requests.get(url).content).find("div", {"id" : "jobDesc"}).find_all(text = True)
        #print (desc_block)
        for elem in desc_block:
            desc = desc + elem + "\n"

        desc = desc.lower()
        for keyword in keyword_list:
            if keyword in desc:
                desc = desc.split(keyword)[1]
                break

        return desc


    def get_scotia(self):
        db_cursor = self.__conn.cursor()
        db_cursor.execute("""SELECT * FROM job_table """)
        list = [item for item in db_cursor.fetchall() if item[1] == 'Scotia Bank']

        return list








