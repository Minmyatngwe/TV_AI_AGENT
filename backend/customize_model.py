
from langchain_core.prompts import ChatPromptTemplate
from prompts import customize
from langchain_ollama import ChatOllama
import json
from ai_model import replace_placeholder_text,convert_pptx_to_png
import ast 
cutomize_prompt=ChatPromptTemplate(
    [
        ("system",customize)
        
    ]
)
model=ChatOllama(model="qwen3.5:35b")
cutomize_chain=cutomize_prompt|model
def customize_template(web_text,prompt,placeholder,slide_path,file_path):
    global cutomize_chain
    
    ai_response=cutomize_chain.invoke(
        {"web_text":web_text,
         "input":placeholder,
         "prompt":prompt
        }
    )
    print("ai_response")
    print(ai_response.content)
    raw_content=ai_response.content
    try:
        ai_response = json.loads(raw_content)
    except json.JSONDecodeError:
        ai_response = ast.literal_eval(raw_content)
    
    powerpoint_path=replace_placeholder_text(slide_path,ai_response,file_path)
    
    png_full_path=convert_pptx_to_png(powerpoint_path[0])
    
    return powerpoint_path,png_full_path    
    
    
    
    
    
    
    
    
    
    


    
    
    
    
    