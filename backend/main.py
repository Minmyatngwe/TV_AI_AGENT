from fastapi import FastAPI
from pydantic  import BaseModel
from typing import List
from ai_model import generate_template,convert_pptx_to_png,replace_placeholder_text
from customize_model import customize_template
import os
import subprocess
from pdf2image import convert_from_path
import shutil
app=FastAPI()

class Template(BaseModel):
    
    link:str
    template_paths:List


class PATH(BaseModel):
    path:str

@app.post("/generate")
def generate(template:Template):
    print("path")
    print(template.template_paths)

    file_path,powerpoint_paths,png_image_paths,web_text,placeholders=generate_template(template.link,template.template_paths)
    print("generate ai response")
    print(placeholders)
    return {
        "file_path":file_path,
        "powerpoint_paths":powerpoint_paths,
        "png_image_paths":png_image_paths,
        "web_text":web_text,
        "placeholders":placeholders
    }

def convert_pptx_to_png_for_template(pptx_path):
    abs_pptx_path=os.path.abspath(pptx_path)
    parent_path=os.path.dirname(abs_pptx_path)
    pdf_path = os.path.join(parent_path, "pdf_files")
    os.makedirs(pdf_path, exist_ok=True)    
    base_name = os.path.splitext(os.path.basename(abs_pptx_path))[0] 
    image_path=os.path.join(parent_path,"image")
    os.makedirs(image_path,exist_ok=True)
    tempo_path=r"/tmp/pdf_tempo"  
    os.makedirs(tempo_path,exist_ok=True) 
    try:
        # 2. Add the temporary profile argument back in!
        profile_arg = f"-env:UserInstallation=file://{tempo_path}/profile"
        
        subprocess.run([
            "libreoffice", 
            profile_arg, 
            "--headless", 
            "--convert-to", "pdf", 
            "--outdir", tempo_path, 
            abs_pptx_path
        ], check=True)
        

    except subprocess.CalledProcessError as e:
        print(f"Error rendering PDF: {e}")
        return []    
    temp_pdf_file = os.path.join(tempo_path, f"{base_name}.pdf")
    
    pdf_file_path=os.path.join(pdf_path,f"{base_name}.pdf")
    shutil.move(temp_pdf_file,pdf_file_path)
    try:
        images = convert_from_path(pdf_file_path, dpi=300)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []
    
    for i, image in enumerate(images):
        png_filename = f"{base_name}.png"
        png_full_path = os.path.join(image_path, png_filename)
        
        image.save(png_full_path, "PNG")
        print(f"Saved: {png_filename}")
            
    return png_full_path

@app.post("/convert_pptx")
def convert(path:PATH):
    print("covert is called")
    convert_pptx_to_png_for_template(path.path)
    


class CUTOMIZE(BaseModel):
    
    web_text:str
    prompt:str
    placeholder:list[dict]
    slide_path:list
    file_path:str
    
@app.post("/cutomize")
def cutomize_pptx(cutomize:CUTOMIZE):
    print("citomize is called")
    ai_response,powerpoint_path,image_path= customize_template(
        web_text=cutomize.web_text,
        prompt=cutomize.prompt,
        placeholder=cutomize.placeholder,
        slide_path=cutomize.slide_path,
        file_path=cutomize.file_path
    )
    print("cutomize_ai_response")
    print(ai_response)
    return {
        "powerpoint_paths":powerpoint_path,
        "png_image_paths":image_path,
        "ai_response":ai_response
    }
    
class IMAGE(BaseModel):
    slide_path:list
    number:int
    ai_response:list[dict]
    file_path:str

@app.post("/change_image")
def chnage_image(image:IMAGE):
    increment=False 
    path=image.slide_path
    number=image.number
    ai_response=image.ai_response
    file_path=image.file_path
    base_name=os.path.basename(path[0])
    parent_path=os.path.dirname(os.path.dirname(path[0]))
    
    files=os.listdir(parent_path)
    images=[]
    for i in files:
        if i.endswith(".png") and not i.startswith("qr"):
            images.append(i)
    print("counter")
    print(number)
    if number>=len(images):
        number=0
        increment=True
        

    selected_image=images[number]
    
    # image_full_path=os.path.join(file_path,selected_image)
    
    for tempo_dict in ai_response:
        for slide_name in tempo_dict:
            if slide_name==base_name:
                
                for key in tempo_dict[slide_name]:
                    print(key)
                    if "image" in key:
                        tempo_dict[slide_name][key]=selected_image
    print("images",selected_image)
    
    print("\n\n ai response")
    print(ai_response)
    template_full_path=os.path.join("./template",base_name)

    powerpoint_path=replace_placeholder_text([template_full_path],ai_response,file_path)[0]
    convert_pptx_to_png(powerpoint_path)
    if not increment:
        number+=1
    return{
        "image_counter":number
    }
    
    
    
    
    
    
    
            
            
    
    
    
    
    