import os
from urlparse import urljoin
import datetime
from os.path import isfile, join
from mining_source import Source
from bs4 import BeautifulSoup
import requests
import mysql.connector


__author__ = 'Shengnuo'

class RBC(Source):
    url = None
    __conn = None

    def __init__(self):
        self.url = "https://jobs.rbc.com/go/Technology-Jobs/586000/"
        self.__conn = mysql.connector.connect(user='root', password = 'genghiskhan', host = 'localhost', database='job_database')

    def mine_to_file(self):
        #db_cursor = self.__conn.cursor()
        current_num = 0
        id = 200000
        '''
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS job_table (
        Title VARCHAR (200),
        Company VARCHAR (45),
        Date_Posted DATE ,
        Location VARCHAR (45),
        URL VARCHAR (200))""")
        '''
        dir = os.path.dirname(__file__) + "\\rbc\\"
        if not os.path.exists("rbc"): os.mkdir("rbc")

        delete_dic = {f : f for f in os.listdir(dir) if isfile(join(dir ,f))}

        while 1:
            current_url = str(self.url + `current_num` + "/?q=&sortColumn=referencedate&sortDirection=desc")
            soup = BeautifulSoup(requests.get(current_url).content)
            total_job_num = int(soup.find("span", {"class" : "paginationLabel"}).find_all("b")[1].text)
            rows = soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find("tbody").find_all("tr")
            if current_num  > total_job_num:
                break
            for job in rows:
                id += 1
                title = job.find("td",{"class":"colTitle"}).find("span").find("a").text
                location = job.find("td",{"class":"colLocation hidden-phone"}).find("span").text
                raw_date = job.find("td",{"class":"colDate hidden-phone"}).find("span").text.replace("\n","").replace("\t","")
                date = datetime.datetime.strptime(raw_date,"%b %d, %Y").strftime("%Y-%m-%d")
                job_url = urljoin(self.url,job.find("td",{"class":"colTitle"}).find("a",{"class":"jobTitle-link"}).get("href"))
                desc_name = job_url.split("/")[-3] + ".txt"
                desc_path = dir + desc_name
                desc = self.get_desc(job_url)
                if desc_name in delete_dic:
                    del delete_dic[desc_name]

                if not os.path.isfile(desc_path):
                    f = open(desc_path,'w')
                    f.close()
                f = open(desc_path, 'w')

                f.write("Title:" + title + "\n")
                f.write("Location:" + location + "\n")
                f.write("Date Posted:" + date + "\n")
                f.write("URL:" + job_url + "\n")
                f.write("-------------------------------------------\n")
                try:
                    f.write(desc)
                except IndexError:
                    print desc_path
                f.close()

                if desc_name in delete_dic:
                    del delete_dic[desc_name]

                print("minded " + desc_name.encode('utf-8'))
                '''
                try:
                    db_cursor.execute("INSERT INTO job_table VALUES (%s, %s, %s, %s, %s)", (title, "RBC", date, location,  job_url))
                except mysql.connector.errors.IntegrityError:
                    db_cursor.execute("UPDATE job_table SET Title=%s, Company=%s, Date_Posted=%s, Location=%s WHERE URL=%s", (title, "RBC",  date, location, job_url))

        self.__conn.commit()
        db_cursor.close()
        '''
            current_num += 25


        print("------------------------------------")
        print("jobs to delete ")
        print (delete_dic)

        for f in delete_dic:
            if os.path.isfile(dir + f):
                os.remove(dir + f)
                print ("cleaned " + f)

    def mine_to_database(self):
        db_cursor = self.__conn.cursor()
        current_num = 0
        id = 200000

        db_cursor.execute("""CREATE TABLE IF NOT EXISTS job_table (
        Title VARCHAR (200),
        Company VARCHAR (45),
        Date_Posted DATE ,
        Location VARCHAR (45),
        URL VARCHAR (200),
        Description VARCHAR (10000))""")

        db_cursor.execute("SELECT * FROM job_table")
        delete_dic = {item[4]:item[4] for item in db_cursor.fetchall() if item[1] == "RBC"}

        while 1:
            current_url = str(self.url + `current_num` + "/?q=&sortColumn=referencedate&sortDirection=desc")
            soup = BeautifulSoup(requests.get(current_url).content)
            total_job_num = int(soup.find("span", {"class" : "paginationLabel"}).find_all("b")[1].text)
            rows = soup.find("table", {"class" : "searchResults full table table-striped table-hover"}).find("tbody").find_all("tr")
            if current_num  > total_job_num:
                break
            for job in rows:
                id += 1
                title = job.find("td",{"class":"colTitle"}).find("span").find("a").text
                location = job.find("td",{"class":"colLocation hidden-phone"}).find("span").text
                raw_date = job.find("td",{"class":"colDate hidden-phone"}).find("span").text.replace("\n","").replace("\t","")
                date = datetime.datetime.strptime(raw_date,"%b %d, %Y").strftime("%Y-%m-%d")
                job_url = urljoin(self.url,job.find("td",{"class":"colTitle"}).find("a",{"class":"jobTitle-link"}).get("href"))
                desc = self.get_desc(job_url)
                if job_url in delete_dic:
                    del delete_dic[job_url]


                try:
                    db_cursor.execute("INSERT INTO job_table VALUES (%s, %s, %s, %s, %s, %s)", (title, "RBC", date, location,  job_url, desc))
                except mysql.connector.errors.IntegrityError:
                    db_cursor.execute("UPDATE job_table SET Title=%s, Company=%s, Date_Posted=%s, Location=%s, Description=%s WHERE URL=%s", (title, "RBC",  date, location, desc, job_url))
                except mysql.connector.errors.DataError: pass
            current_num += 25


        for f in delete_dic:
            db_cursor.execute("DELETE FROM job_table WHERE URL = '%s'", f)
        self.__conn.commit()
        db_cursor.close()




    def get_desc(self, url):
        desc = ""
        keyword_list = ["description", "key accountabilities", "key accountability" , "purpose",  "knowledge", "responsibility", "responsibilities", "duty", "duties", "qualification","education", "requirement", "degree"]

        desc_block = BeautifulSoup(requests.get(url).content).find("span", {"itemprop" : "description"}).find_all(text = True)
        for elem in desc_block:
            desc = desc + elem + "\n"
        desc = desc.lower()

        for keyword in keyword_list:
            if keyword in desc:
                desc = keyword + " ".join(desc.split(keyword)[1:])
                break
        return desc