from PIL import Image
from transformers import pipeline
from typing import Dict, List

vqa_pipeline = pipeline("visual-question-answering")

image =  Image.open("./Screenshot 2024-10-26 095954.png").convert(mode='RGB')
question = "What is the person doing?"


results: List[Dict[str, float]]
results = vqa_pipeline(image, question, top_k=4)
#[{'score': 0.9998154044151306, 'answer': 'yes'}]

for res in results:
    print(res.get('answer'),'\n')

