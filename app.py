from flask import Flask, request, render_template
from scrapegraphai.graphs import SmartScraperGraph
import google.generativeai as genai
from pymongo import MongoClient
import nest_asyncio
import datetime
import time

app = Flask(__name__, static_url_path='/static')

nest_asyncio.apply()

# Google API Key
GOOGLE_API_KEY = "AIzaSyCwoNY7QSGd4o4Y-vBdHmoG6t3zSpHIWlM"
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key = GOOGLE_API_KEY)

# Database Credentials
client = MongoClient("localhost", 27017)
db = client["News"]

# Web links of Data
links = {
    "1":["DST","https://dst.gov.in/call-for-proposals"],
    "2":["AmazonSpace","https://www.amazon.science/research-awards/call-for-proposals"],
    "3":["MNRE","https://mnre.gov.in/notice-category/current-notices/"],
    "4":["ICMR","https://main.icmr.nic.in/call%20for%20proposals"],
    "5":["NBHM","https://nbhm.dae.gov.in/news.html"],
    "6":["IGSTC","https://www.igstc.org/home/news_and_events"],
    "7":["USIEF","https://www.usief.org.in/MediaRoom.aspx"],
    "8":["SERI","https://research.swiss/category/funding-opportunities/"],
    "9":["Chanakya University","https://chanakyauniversity.edu.in/fellowship/admissions/"],
    "10":["DST","https://onlinedst.gov.in/Projectproposalformat.aspx?Id=2232"],
    "11":["INAE-SERB","https://www.inae.in/abdul-kalam-technology-innovation-national-fellowship/"],
    "12":["BIRAC","https://birac.nic.in/cfp.php"],
    "13":["CFC","https://www.common-fund.org/call-for-proposals"]
    }

# Define model
graph_config = {
    "llm": {
        "api_key": GOOGLE_API_KEY,
        "model": "gemini-pro",
    },
    "verbose":True
}

def fetch():
    for i in links.values():
        # Get today's date
        date = str(datetime.datetime.now()).split(' ')[0]
        date = date.split('-')
        # Create a new collection
        collection = db["collection"]
        requesting = []
        # Prompt to scrape data
        try:
            smart_scraper_graph = SmartScraperGraph(
                prompt="List me all the calls, fellowships, International bilateral and workshops along with their name, link, opening date and closing date. Seperate them by Calls, Fellowships, International bilateral and Workshops. If no link, give NA",
                source=i[1],
                config=graph_config
            )
            result = smart_scraper_graph.run()
            print(result)
        except:
            continue
        # Check if the data has expired
        for obj in result.values():
            for data in obj:
                try:
                    if data['closing_date'] != "null" and data['closing_date'] != None:
                        query = f"Convert {data['closing_date']} to 'DD-MM-YYYY' format. If date not given, take it as 1. If year not given take it as 2024. Just give the date I don't want any explaination, just dd-mm-yyyy,"
                        res = model.generate_content(query)
                        time.sleep(4.0) # To slow down requests
                        d = (res.text).strip().split('-')
                        print(d, date)
                        dd = (res.text).strip()
                        if "you" in dd:
                            dd = "NA"
                        else:
                            if d[2] < date[2]:
                                continue
                            if d[2] == date[2]:
                                if d[1] < date[1]:
                                    continue
                                if d[1] == date[1]:
                                    if d[0] < date[0]:
                                        continue
                    data['Organization'] = i[0]
                    data['closing_date'] = dd
                    db.collection.insert_one(data)
                except:
                    break
fetch()
@app.route('/')
def home():
    client = MongoClient("localhost", 27017)
    db = client["News"]
    col = db["collection"]
    data = col.find()
    store = []
    l = ["Event", "Organization", "Name", "Opening Date", "Closing Date", "Link"]
    store.append(l)
    for x in data:
        if "Call" in x['name'] or "call" in x['name']:
            eve = "Calls"
        elif "Fellow" in x['name'] or "fellow" in x['name']:
            eve = "Fellowship"
        elif "International" in x['name'] or "international" in x['name']:
            eve = "International Bilateral"
        elif "Workshop" in x['name'] or "workshop" in x['name']:
            eve = "Workshop"
        else:
            eve = "Event"
        lis = [eve, x['Organization'], x['name'], x['opening_date'], x['closing_date'], x['link']]
        x = []
        for i in lis:
            x.append(str(i))
        store.append(x)
    return render_template('index.html', datas=store)

if __name__ == '__main__':
    app.run()
