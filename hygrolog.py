#!/usr/bin/python2

import sqlite3
import requests
import re
from datetime import datetime as dt
import argparse

DB_FILENAME = "./hygrolog.db"
HYGROMETER_URL = "http://192.168.1.52"

def setup_db(database):
  conn = sqlite3.connect(database)
  c = conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS hygrodata (
		date text,
		temperature real,
		relative_humidity real
		)""")
  conn.commit()
  return conn, c

def fetch_temp_rh(url):
  r = requests.get(url)
  m = re.search('[0-9]{2}\.[0-9]{2}C', r.text)
  temp = m.group(0)[:-1]
  m = re.search('[0-9]{2}\.[0-9]{2}%', r.text)
  rh = m.group(0)[:-1]
  return temp, rh
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Fetch hygrometer values from webserver and save to sqlite DB")
  parser.add_argument('--dbfile', dest='dbfile', default=DB_FILENAME, help='Sqlite DB file to use')
  parser.add_argument('--url', dest='url', default=HYGROMETER_URL, help='Url to fetch values from')
  args = parser.parse_args()

  conn, c = setup_db(args.dbfile)
  temp, rh = fetch_temp_rh(args.url)
  c.execute('''INSERT INTO hygrodata VALUES (?, ?, ?)''', (str(dt.now())[:-7], temp, rh))
  conn.commit()
  conn.close()
