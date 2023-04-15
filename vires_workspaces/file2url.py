#!/usr/bin/python3
# -*- coding: utf8 -*-
# 
# Usage: ./file2url.py *.json
# 
# Find out how to replace with this:
# cat wkspc_AEJ_LPL.json | gzip | base64 -w0 | awk '{print "https://vires.services?ws=data:application/json+gzip;base64,"$1}'
# (currently missing the dumps, encode/decode ascii and quote)

from base64 import standard_b64encode
from gzip import GzipFile
from io import BytesIO
import json
import sys
from urllib.parse import quote


def load_workspace(file):
    with open(file) as f:
        data = json.load(f)
    return json.dumps(data).encode("ascii")


def gzip_data(data):
    buffer_ = BytesIO()
    with GzipFile(fileobj=buffer_, mode="wb", compresslevel=9) as file_gzip:
        file_gzip.write(data)
        file_gzip.close()
    buffer_.seek(0)
    return buffer_.read()


def gzip_base64(data):
    return standard_b64encode(gzip_data(data)).decode("ascii")


def url_from_file(file):
    request_string = gzip_base64(load_workspace(file))
    base_url = "https://vires.services?ws="
    quoted_data_url = quote(f"data:application/json+gzip;base64,{request_string}")
    return base_url+quoted_data_url


if __name__ == "__main__":
    files = sys.argv[1:]
    files = [file for file in files if ".json" in file]
    urls = [url_from_file(file) for file in files]
    for file, url in zip(files, urls):
        print(f"{file}:\n{url}\n")
