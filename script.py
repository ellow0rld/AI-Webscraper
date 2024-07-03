import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import datetime
import google.generativeai as genai

st.title("Proposal Calls")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCwoNY7QSGd4o4Y-vBdHmoG6t3zSpHIWlM"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
instruction = """
You are an expert in structuring data by identifying patterns from unstructured data. 
You will be given unstructured data regarding research proposal calls.
You are supposed to structure the data and return only the data asked by user in the mentioned format.
Always the closing dates must be later than today.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# "3":["BIRAC","https://birac.nic.in/cfp.php","https://birac.nic.in"],
def read_input():
    date = str(datetime.datetime.now()).split(' ')[0]
    links = {
       "1":["DST","https://dst.gov.in/call-for-proposals", "https://dst.gov.in"],
       "2":["MEITY","https://www.meity.gov.in/whatsnew", "https://www.meity.gov.in"],
       "3":["Amazon Space","https://www.amazon.science/research-awards/call-for-proposals", "https://www.amazon.science/research-awards/call-for-proposals"],
       "4":["MNRE","https://mnre.gov.in/notice-category/current-notices/", "https://mnre.gov.in"]
    }
    for i in range(1,6):
        url = links[str(i)][1]
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        data = soup.text
        link = soup.find_all('a', href=True)
        l = ""
        for a in link:
            li = a['href'][1:]
            if "www" not in a['href']:
                li = links[str(i)][2] + a['href']
            l = l +"\n"+ li
        print(links[str(i)][0])
        print(l)
        print(data)
        query = f"""
        Unstructured Data: {data} 
        Name of organization is {links[str(i)][0]} 
        Jumbled links of calls for proposals: {l}
        Today's Date: {date}
        Create a tabular form with the following:
        1. Call for proposals or joint call for proposals 
        2. along with respective link
        3. opening date with year
        4. closing date with year
        If the link is missing or the opening date or closing date is not given, output NA and proceed.
        """
        #response = model.generate_content(query)
        llm_function(query)


def llm_function(query):
    response = model.generate_content(query)
    if "no information" not in response:
        st.markdown(response.text)

read_input()
#response = model.generate_content("Merge all the above tables into a single table with four columns: Organization Name, Call for Proposal Name, Starting Date and Ending Date")
# streamlit run app.py
