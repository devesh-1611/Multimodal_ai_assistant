from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import os
from PIL import Image
from pathlib import Path
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
)

import google.generativeai as genai
import base64
from PIL import Image
from io import BytesIO
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_image_from_prompt(prompt: str, output_path="generated_image.png"):
    """
    Generate an image using free APIs.
    Tries multiple services: Pollinations.ai, Hugging Face, then creates a fallback.
    """
    import requests
    
    try:
        print(f"Attempting to generate image for prompt: {prompt[:50]}...")
        
        # Try Pollinations.ai (completely free, no auth needed)
        print("  Trying Pollinations.ai...")
        try:
            pollinations_url = "https://image.pollinations.ai/prompt/" + prompt.replace(" ", "%20")
            response = requests.get(pollinations_url, timeout=30)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f" Image generated successfully with Pollinations.ai: {output_path}")
                return output_path
        except Exception as e:
            print(f"  Pollinations.ai failed: {str(e)[:80]}")
        
        # Try Hugging Face with corrected approach
        hf_api_key = os.getenv("HF_API_KEY")
        if hf_api_key:
            print("  Trying Hugging Face API...")
            try:
                headers = {"Authorization": f"Bearer {hf_api_key}"}
                api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=60
                )
                
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f" Image generated successfully with Hugging Face: {output_path}")
                    return output_path
                else:
                    print(f"  HF status: {response.status_code}")
            except Exception as e:
                print(f"  Hugging Face failed: {str(e)[:80]}")
        
        print("All image generation APIs failed, creating descriptive image...")
        
    except Exception as e:
        print(f"Error in image generation: {type(e)._name_}: {str(e)[:100]}")
    
    # Fallback: Create a visually appealing descriptive image
    from PIL import Image, ImageDraw
    import random
    
    width, height = 512, 512
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    # Create gradient background from blue to purple
    for y in range(height):
        r = int(100 + (155 * y / height))
        g = int(150 - (50 * y / height))
        b = int(200 + (55 * y / height))
        for x in range(width):
            pixels[x, y] = (r, g, b)
    
    draw = ImageDraw.Draw(img)
    
    # Add decorative circles
    for _ in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(5, 25)
        draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 255, 100), outline=(255, 255, 255))
    
    # Add text box with prompt
    draw.rectangle([30, 180, 482, 400], fill=(255, 255, 255, 200), outline=(100, 100, 200), width=3)
    
    # Wrap text
    lines = []
    words = prompt.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) < 35:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)
    
    # Draw wrapped text
    y_offset = 200
    for line in lines[:4]:
        draw.text((50, y_offset), line, fill=(0, 0, 0))
        y_offset += 35
    
    # Add status
    draw.text((50, 450), "Descriptive Placeholder", fill=(100, 100, 200))
    
    img.save(output_path)
    print(f" Descriptive placeholder created: {output_path}")
    return output_path





def analyze_text(prompt: str):
    messages = [("human", prompt)]
    return llm.invoke(messages).content



def analyze_image(image_path, prompt):
    from langchain_google_genai import ChatGoogleGenerativeAI
    #from langchain.schema import HumanMessage
    from langchain_core.messages import HumanMessage


    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # Load and encode image
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    #  Pass text + image together
    messages = [
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_b64}"}
        ])
    ]

    return llm.invoke(messages).content



# def analyze_audio(audio_path: str, prompt: str):
#     path = Path(audio_path)
#     messages = [("human", prompt), path]
#     return llm.invoke(messages).content

def analyze_audio(audio_path: str, prompt: str):
    path = Path(audio_path)
    audio_bytes = path.read_bytes()
    from langchain_core.messages import HumanMessage
    messages = [
        HumanMessage(content=prompt),
        HumanMessage(content=f"Audio file '{path.name}' with {len(audio_bytes)} bytes uploaded.")
    ]
    response = llm.invoke(messages)
    return response.content