
from langchain_core.prompt import ChatPromptTemplate
from prompts import customize
from langchain_ollama import ChatOllama


cutomize_prompt=ChatPromptTemplate(
    [
        ("system",customize)
        
    ]
)
model=ChatOllama(model="qwen3.5:35b")
cutomize_chain=cutomize_prompt|model
def customize(web_text,prompt,placeholder,slide_path,file_path):
    global cutomize_chain
    
    cutomize_chain.invoke(
        {"web_text":web_text,
         "input":placeholder,
         "prompt",prompt
        }
    )
    
    
    
    
    
    


    
    
    
    
    