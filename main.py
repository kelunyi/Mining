from rbc import RBC
from scotia import Scotia

__author__ = 'Shengnuo'


file = open("storage", "w")
bank1 = Scotia("http://jobs.scotiabank.com/careers/it-jobs/job-list-1")
bank1.mining(file)

bank2 = RBC("https://jobs.rbc.com/go/Technology-Jobs/586000/")
#bank2.mining(file)
file.close()