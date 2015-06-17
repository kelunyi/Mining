from rbc import RBC
from scotia import Scotia
import mysql.connector

__author__ = 'Shengnuo'

conn = mysql.connector.connect(user='root', password = 'genghiskhan', host = 'localhost', database='job_database')
mycursor = conn.cursor()


'''
bank1 = Scotia("http://jobs.scotiabank.com/careers/it-jobs/job-list-8")
bank1.mining(mycursor)
'''

bank2 = RBC("https://jobs.rbc.com/go/Technology-Jobs/586000/")
bank2.mining(mycursor)

conn.commit()
