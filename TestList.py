# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
from bs4 import BeautifulSoup
# https://greeksharifa.github.io/references/2020/10/30/python-selenium-usage/#%ED%98%84%EC%9E%AC-url-%EC%96%BB%EA%B8%B0
from selenium import webdriver
from time import sleep

# https://www.w3schools.com/tags/ref_httpmethods.asp
from requests.adapters import HTTPAdapter 
# https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry
from requests.packages.urllib3.util.retry import Retry # to do sys
# https://docs.python.org/ko/3/howto/urllib2.html
from urllib.request import urlopen

# Module Imports
#import mariadb #$ pip3 install mariadb
import sys
import re
# https://brownbears.tistory.com/198
import requests
import json
import logging

# csv save Imports
import pandas as pd
import os.path as op
"""
Isuue
https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests

Why?
https://moondol-ai.tistory.com/238
https://realpython.com/python-requests/
https://velog.io/@hwang-eunji/python-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-feat.-selenium-2-%EC%8B%A4%EC%8A%B5
https://wikidocs.net/86334

What?
# DB Create Insert Query 작성
# Cloling_Data형식 수정
"""

class Word_Cloling():

    def __init__(self):
        super().__init__()

        # first VaVariables
        self._session       = None
        self._url           = 'http://www.psale.kr/?p=211'
        self._cur           = None
        self._set_title     = '#post-211 > div.post-content'
        self._set_listVal   = 'p'
        self._cloling_data  = {}

        # Move_Method
        self.Do_Logging_Move()
        self.seesion_setting()
        #self.cloling_try_example()
        self.cloling_try_example_Num1_100()
        self.csv_log_save()

    def Do_Logging_Move(self):
        # logger create
        logger = logging.getLogger()

        # logger pullOut List
        logger.setLevel(logging.INFO)
        logger.setLevel(logging.ERROR)
        logger.setLevel(logging.DEBUG)

        # logger putInfo
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # logger out
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    def seesion_setting(self):

        self.session = requests.Session()

        retry = Retry(connect=5, read=2, redirect=5)
        adapter = HTTPAdapter(max_retries=retry)
        logging.debug("adapter = %s" % adapter)
        logging.info("Variables Call")

        """
        # https://2.python-requests.org/en/master/api/#requests.Session.mount
        mount(prefix, adapter)[source]
        Registers a connection adapter to a prefix.

        Adapters are sorted in descending order by prefix length.
        """
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        logging.debug("seesion Property mount call")

    def cloling_try_example(self):

        # Max_ReCount Call error try example method
        try:
            response = requests.get(self._url)

        except requests.exceptions.ConnectionError:

            page = urlopen(self._url)
            logging.info("incode ...")
            sleep(2)
            # bytes to string
            logging.error("requests.exceptions.Connection = False")

            """
            doc = page.read().decode('utf-8') #Incoding
            print(doc)
            dic = json.loads(doc) #Dcoding
            """

        if response.status_code == 200:

            logging.debug("response.status_code = 200")
            html    = response.text
            soup    = BeautifulSoup(html, 'html.parser')
            title   = soup.select_one(self._set_title)
            listVal = title.select(self._set_listVal)
            logging.info("Variables Call")
            
            count = 1
            val = ""
            
            for _list in listVal:
                _list = str(_list)
                _list = re.sub("<p>|</p>|<br/>|\n[0-9]", "", _list)
                val = val + _list

                if (False if val.find(f'{count}.') == -1 else True):
                    list_cur = _list.find(f'{count}.')
                    #val = val + _list[:list_cur]
                    self._cloling_data.setdefault(f'{count}',val)
                    sleep(1)
                    logging.info(f"val{count}. : {val}")
                    count = count + 1
                    val = _list[list_cur:]
                
                else:
                    #logging.info(_list)
                    logging.error("Error : Missing")

            logging.info("self._cloling_data = %s" % self._cloling_data)

    def swap(self, x, i, j):
        x[i], x[j] = x[j], x[i]

    def bubbleSort(self, x):
        for size in reversed(range(len(x))):
            for i in range(size):
                if x[i] > x[i+1]:
                    self.swap(x, i, i+1)
                
        print("x : %s"% x)
        return x

    def list_map_ChangeType(self, _Init_list):
        """
        strType List Change Str or Int Method an Regular expression an Escape
        """

        listVal = str(_Init_list)
        # 정규표현식 응용
        listVal = re.sub("<p>|</p>|<br/>|[^0-9a-zㄱ-힣\.\[\] ]", "", listVal)

        #listVal = listVal.strip()
        _list = re.findall('\d+', listVal)
        #set = 튜플 변환 및 유일성을 추구하여 중복제거 sorted 정렬
        _list = sorted(set(_list))
        #_list = self.bubbleSort(_list)
        
        """
        list가 문자열일시 문자 비교를 1 10 100 2 21 22 이런식으로
        자릿수 우선 > 크기우선으로 변경된다.
        """
        # list_int형변환 list_a = [int (i) for i in list_a]
        _int_list = list(map(int, _list))
        _int_list = sorted(set(_int_list))

        return listVal, _int_list

    def cloling_try_example_Num1_100(self):

        # Max_ReCount Call error try example method
        try:
            response = requests.get(self._url)

        except requests.exceptions.ConnectionError:

            page = urlopen(self._url)
            logging.info("incode ...")
            sleep(2)
            # bytes to string
            logging.error("requests.exceptions.Connection = False")

            """
            doc = page.read().decode('utf-8') #Incoding
            print(doc)
            dic = json.loads(doc) #Dcoding
            """

        if response.status_code == 200:

            logging.debug("response.status_code = 200")
            html    = response.text
            soup    = BeautifulSoup(html, 'html.parser')
            title   = soup.select_one(self._set_title)
            listVal = title.select(self._set_listVal)
            logging.info("Variables Call Num1_100")
            
            count = 1
            val = ""
            listVal, _int_list = self.list_map_ChangeType(listVal)
            
            for _idx in _int_list:
                    
                if (False if listVal.find(f'{_idx}.') == -1 else True):
                        
                        # _list_cur = 현재 찾은 idx
                        _list_cur = listVal.find(f'{_idx}.')

                        valNone = listVal[:_list_cur]
                        valNone = re.sub("[0-9\.]", "", valNone)
                        self._cloling_data.setdefault(f'{count}',valNone)

                        sleep(0.3)
                        logging.info(f'{count} : 'f'{valNone}')
                        count = count + 1

                        listVal = listVal[_list_cur:]

            logging.info("self._cloling_data = %s" % self._cloling_data)

    def csv_log_save(self):

        """
        df = pd.DataFrame([['1위', '심재철'],
                ['2위', '서미경']])
        df.columns=['rank', 'keyword']
        df.to_csv('./TestList_CSV/TestDB.csv', index=False, encoding='cp949')
        """
        """
        
        """
        if op.exists('TestList_CSV/TestDB.csv'):
            csvFrame = pd.DataFrame(list(self._cloling_data))
            csvFrame.columns=['goodWord']
            csvFrame.to_csv('TestList_CSV/TestDB.csv', index=False, encoding='cp949')

        else:
            with open("TestList_CSV/TestDB.csv", 'w', newline='', encoding="utf8") as f:
                wf = csv.writer(f)
                wf.writerow(['goodWord'])
        

    def mariaDB_setting(self):
        """
        https://mariadb.com/ko/resources/blog/how-to-connect-python-programs-to-mariadb/

        # Retrieving Data
        cur.execute(
        "SELECT first_name,last_name FROM employees WHERE first_name=?", 
        (some_name,))

        # Print Result-set
        for (first_name, last_name) in cur:
            print(f"First Name: {first_name}, Last Name: {last_name}")

        # INSERT Data
        cursor.execute(
        "INSERT INTO employees (first_name,last_name) VALUES (?, ?)", 
        (first_name, last_name))

        # Disable Auto-Commit(자동커밋 비활성화)
        conn.autocommit = False

        # Catching Exceptions
        try:
            cursor.execute("some MariaDB query"))
        except mariadb.Error as e:
            print(f"Error: {e}")

        # Close Connection
        conn.close()
        """

        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user="db_user",
                password="db_user_passwd",
                host="192.0.2.1",
                port=3306,
                database="employees"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self._cur = conn.cursor()

        #self.mariadb_tableCreate(self._cur)

    def mariadb_tableCreate(self, createDB):
        """
        https://mariadb.com/docs/reference/conpy/api/cursor/
        https://docs.python.org/ko/3/library/sqlite3.html
        """

        # Create Table
        createDB().execute('''
            CREATE TABLE stocks
            (index, word, general)
        ''')

        # Insert a row of data
        lang_list = [("Fortran", 1957, 'A'), ("Python", 1991, 'B'), ("Go", 2009, 'C')]
        #createDB().execute("INSERT INTO stocks VALUES (%s, %s, %s)" % lang_list)
        for len_list in lang_list:
            createDB().execute("INSERT INTO stocks VALUES (%s, %s, %s)" % len_list)

        # DB output
        for row in createDB().execute('SELECT * FROM stocks ORDER BY price'):
            print(row)

        # Save (commit) the changes
        createDB().commit()

        #self._cur.


if __name__ == "__main__":
    Word_Cloling()
