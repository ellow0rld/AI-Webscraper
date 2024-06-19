import streamlit as st
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import os
import google.generativeai as genai

client = MongoClient("localhost", 27017)
database = client['Call Proposals']
collection = database['reviews']

st.title("Proposal Calls")

os.environ['GOOGLE_API_KEY'] = "AIzaSyCwoNY7QSGd4o4Y-vBdHmoG6t3zSpHIWlM"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

def read_input():
   links = {
       "1":["DST","https://dst.gov.in/call-for-proposals", "https://dst.gov.in"],
       "2":["MEITY","https://www.meity.gov.in/whatsnew", "https://www.meity.gov.in"],
       "3":["BIRAC","https://birac.nic.in/cfp.php","https://birac.nic.in"],
       "4":["Amazon Space","https://www.amazon.science/research-awards/call-for-proposals", "https://www.amazon.science/research-awards/call-for-proposals"],
       "5":["MNRE","https://mnre.gov.in/notice-category/current-notices/", "https://mnre.gov.in"]
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
       query = data + "name of organization is"+links[str(i)][0]+ "Jumbled links of calls for proposals:"+l+"\n Prepare a table with the following data: Call for proposals or joint call for proposals along with respective link, opening date, closing date and the name of the organization."
       #response = model.generate_content(query)
       #query2 = "Today's date is 8th June 2024. Remove all the data points from above whose closing data is before today and print it here."
       llm_function(query)

def llm_function(query):
    response = model.generate_content(query)
    if "no information" not in response:
        st.markdown(response.text)

read_input()
#response = model.generate_content("Merge all the above tables into a single table with four columns: Organization Name, Call for Proposal Name, Starting Date and Ending Date")
# streamlit run app.py
