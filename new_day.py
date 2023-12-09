#!/usr/bin/env python3

import sys
import os
import http.client


year = '2023'
day = sys.argv[1]
print(f"Making directory for day {day}")

directory = f"day{day}"
os.makedirs(directory, exist_ok=True)

def touch(fname):
    open(os.path.join(directory, fname),"a").close()

touch("test.txt")
touch("main.py")
touch("input.txt")

print("Fetching puzzle input")
# TODO: error handling
token = open("./token.txt").read()
host = "adventofcode.com"
path = f"/{year}/day/{day}/input"
conn = http.client.HTTPSConnection(host)
conn.request("GET", path, headers={"Host": host, "Cookie": f"session={token.strip()}"})
response = conn.getresponse()
print(response.status, response.reason)

response_text = response.read().decode('utf-8')

with open(os.path.join(directory, "input.txt"), "w") as fh:
    fh.write(response_text)



