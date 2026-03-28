from fastapi import FastAPI
from ai_model
from pydantic  import BaseModel
from typing import List
from ai_model import generate_template
app=FastAPI()

class Template(BaseModel):
    
    link:str
    template_paths:List


@app.post("/generate")
def generate(template:Template):
    file_path,powerpoint_paths,png_image_path=generate_template(template.link,template.template_paths)
    
        