#step1: setup groq api key
import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#step:convert image to required format 

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def describe_image(image_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description


#Step3: Setup Multimodal LLM

from groq import Groq

query="make my dietplan i have a low blood pressure?"
model="deepseek-r1-distill-llama-70b"

def analyze_text_with_query(query, model,):

 client=Groq()
 messages=[
    {
       "role": "user",
       "content": [
           {
                "type": "text",
                "text": query
           },
       ],
    }]

 chat_completion=client.chat.completions.create(
     messages=messages,
     model=model
)

 return chat_completion.choices[0].message.content

