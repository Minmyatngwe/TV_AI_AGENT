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
import qrcode
import time
import json
import playwright 
from playwright.sync_api import sync_playwright
import ollama 
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE 
import ast 


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

import os
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def extract_from_shapes(shapes, placeholder_list):
    """
    Recursive function to find text and image placeholders 
    in a collection of shapes (handles nested groups).
    """
    
    for shape in shapes:
        if "image" in shape.name.lower():
            placeholder_list.append(shape.name)

        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            extract_from_shapes(shape.shapes, placeholder_list)

        elif shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                clean_text = paragraph.text.strip()
                if clean_text.startswith("{{") and clean_text.endswith("}}"):
                    full_placeholder = "".join(run.text for run in paragraph.runs)
                    placeholder_list.append(full_placeholder)

def get_placeholder_name(slides_path):
    print("Processing slides...")
    slide_placeholder = {}
    
    for path in slides_path:
        slide_file_name = os.path.basename(path)
        # Initialize the list for this file
        slide_placeholder[slide_file_name] = []
        
        print(f"Reading: {slide_file_name}")
        presentation = Presentation(path)
        
        for slide in presentation.slides:
            extract_from_shapes(slide.shapes, slide_placeholder[slide_file_name])
            
    for key in slide_placeholder:
        slide_placeholder[key] = list(set(slide_placeholder[key]))
            
    print(slide_placeholder)
    return slide_placeholder

def summarize(link,slides_path):
        global summarize_chain
        response=requests.get(link)
        soup=BeautifulSoup(response.content,'html.parser')
        text=soup.text
        text_clean=re.sub(r"\n+","\n",text)
        
        images=soup.find_all('img',class_="fl-photo-img")
        
        
        slide_placeholders=get_placeholder_name(slides_path)
        summarization=summarize_chain.invoke({"input":text_clean,"slide_placeholder":slide_placeholders})
        
        return summarization.content
    

    
        
print(summarize("https://www.roboai.fi/en/news-en/apply-to-study-at-the-roboai-academy-2026/",["./template/testing_.pptx","./template/second_testing_template.pptx"]))
