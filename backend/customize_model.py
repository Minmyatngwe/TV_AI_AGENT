
from langchain_core.prompt import ChatPromptTemplate
from prompts import customize
from langchain_ollama import ChatOllama
import json
from ai_model import replace_placeholder_text,convert_pptx_to_png
cutomize_prompt=ChatPromptTemplate(
    [
        ("system",customize)
        
    ]
)
model=ChatOllama(model="qwen3.5:35b")
cutomize_chain=cutomize_prompt|model
def cutomize_template(web_text,prompt,placeholder,slide_path,file_path):
    global cutomize_chain
    
    ai_response=cutomize_chain.invoke(
        {"web_text":web_text,
         "input":placeholder,
         "prompt",prompt
        }
    )
    ai_response=json.load(ai_response.content)
    powerpoint_path=replace_placeholder_text(slide_path,ai_response,file_path)
    png_full_path=convert_pptx_to_png(powerpoint_path[0])
    
    return powerpoint_path,png_full_path
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    