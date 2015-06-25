from mining_source import Source
import mechanize

__author__ = 'Shengnuo'

class CIBC(Source):
    url = None

    def __init__(self):
        self.url = "https://cibc.taleo.net/careersection/1/jobsearch.ftl?lang=en"

    def mining(self):
        br = mechanize.Browser()
        br.open(self.url)

        br.select_form("ftlform")
        br.form['keyword'] = 'IT'
        br.select_form("ftlform")
        response = br.submit(id = "basicSearchFooterInterface.searchAction")

        print response.geturl() # URL of the page we just opened
        print response.info()   # headers
        print response.read()
