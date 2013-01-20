import requests
from flask import Flask
from flask import jsonify
from BeautifulSoup import *
from models.link import Link

import json
import re


app = Flask(__name__)
body = None
link = Link()

def is_valid_link(link):
    match = re.match(r'.*\.html',str(link))
    if match:
        return True
    return False


def fetch_news():
    r = requests.get("http://javascriptweekly.com/archive/")
    body = r.content
    soup = BeautifulSoup(body)
    links = soup.findAll("a")
    res = []
    for link in links:
        if is_valid_link(link):
            res.append(link)
    return sorted_links(links)

## append links to link.objects
def inject_links(links):
    for l in links:
        tmp  =  re.split(r'<a\shref=',str(l))
        number =  re.sub(r'\.*html','',tmp[1]).split(">")[0]
        if not re.match(r'"\/"',str(number)):
            link.objects.append(
                    {"number": int(number.strip('"')),
                        "body": l}
                    )

## set link.objects order by newest.
def sorted_links(links):
    inject_links(links)
    link.objects = sorted(link.objects,key = lambda link_obj:link_obj["number"])
    return link.objects

def latest_link():
    latest = link.objects.pop()
    return latest


    

@app.route("/")
def hello():
    return "hellooo"

@app.route("/news")
def news():
    # set link.objects by fetch_news
    fetch_news()
    print link.objects



    return jsonify(data=["apple","orange","banana"])



if __name__ == "__main__":
    app.debug = True
    app.run()
