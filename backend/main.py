from fastapi import FastAPI
from pydantic  import BaseModel
from typing import List
from ai_model import generate_template
from customize_model import customize_template
import os
import subprocess
from pdf2image import convert_from_path

app=FastAPI()

class Template(BaseModel):
    
    link:str
    template_paths:List


class PATH(BaseModel):
    path:str

@app.post("/generate")
def generate(template:Template):
    file_path,powerpoint_paths,png_image_paths,web_text,placeholders=generate_template(template.link,template.template_paths)


def convert_pptx_to_png(pptx_path):
    output_path=os.path.dirname(pptx_path)
    pdf_path = os.path.join(output_path, "pdf_files")
    os.makedirs(pdf_path, exist_ok=True)    
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]   
    try:
        subprocess.run([
            "libreoffice", 
            "--headless", 
            "--convert-to", "pdf", 
            "--outdir", pdf_path, 
            pptx_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error rendering PDF: {e}")
        return []    
    pdf_file_path=os.path.join(pdf_path,f"{base_name}.pdf")
    try:
        images = convert_from_path(pdf_file_path, dpi=300)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []
    
    image_path = os.path.join(output_path, "image")
    os.makedirs(image_path, exist_ok=True)    
    for i, image in enumerate(images):
        png_filename = f"{base_name}.png"
        png_full_path = os.path.join(image_path, png_filename)
        
        image.save(png_full_path, "PNG")
        print(f"Saved: {png_filename}")
            
    return png_full_path

@app.post("/convert_pptx")
def convert(path:PATH):
    convert_pptx_to_png(path.path)
    


class CUTOMIZE(BaseModel):
    
    web_text:str
    prompt:str
    placeholder:list[dict]
    slide_path:str
    file_path:str
    
@app.post("/cutomize")
def cutomize_pptx(cutomize:CUTOMIZE):
    cutomize_template(
        web_text=cutomize.web_text,
        prompt=cutomize.prompt,
        placeholder=cutomize.placeholder,
        slide_path=cutomize.slide_path,
        file_path=cutomize.file_path
    )