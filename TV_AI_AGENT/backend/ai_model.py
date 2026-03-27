from prompts import summarize_prompt,selecting_image_prompt,defining_layout_prompt,layout_variant_prompt,slide_critique_prompt,html_fix_prompt
import requests 
from bs4 import BeautifulSoup
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
import os 
from langchain_core.messages import AIMessage,HumanMessage
import base64
from google import genai
from dotenv import load_dotenv
import qrcode
load_dotenv()
import time
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import playwright 
from playwright.sync_api import sync_playwright
import ollama 



summarize_template=ChatPromptTemplate(
    [
        ("system",summarize_prompt),
        ("human","{input}")
    ]
)

ollama_model_text="qwen3.5:9b"
ollama_model_vl="qwen3-vl:30b"
deepseek_r1="hengwen/DeepSeek-R1-Distill-Qwen-32B:q4_k_m"

qwen_35="qwen3.5:35b"

summarize_model=ChatOllama(model=qwen_35)
summarize_chain=summarize_template|summarize_model

def summarize(link):
        global summarize_chain
        response=requests.get(link)
        soup=BeautifulSoup(response.content,'html.parser')
        text=soup.text
        text_clean=re.sub(r"\n+","\n",text)
        
        images=soup.find_all('img',class_="fl-photo-img")
        summarization=summarize_chain.invoke({"input":text_clean})
        ai_response=json.loads(summarization.content)    


print(summarize("https://www.roboai.fi/en/news-en/apply-to-study-at-the-roboai-academy-2026/"))
