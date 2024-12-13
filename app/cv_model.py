from PIL import Image
from transformers import pipeline
from typing import Dict, List, Tuple
from transformers import ViltProcessor, ViltForQuestionAnswering


def model_computation(img: str, question: str) -> List[str]:

    vqa_pipeline = pipeline("visual-question-answering")

    image = Image.open(img).convert(mode="RGB")
    # image =  Image.open(img).convert(mode='RGB')
    query = question

    results: List[Dict[str, float]]
    results = vqa_pipeline(image, query, top_k=4)
    # [{'score': 0.9998154044151306, 'answer': 'yes'}]

    print(results)
    ans: List = []
    for res in results:
        ans.append(res.get("answer"))
        # print(res.get('answer'),'\n')

    return ans


if __name__ == "__main__":
    ans = model_computation(
        "C:/Users/rohit/Pictures/Screenshots/test_img.png",
        "What do you see in the image?",
    )
    # print(ans)
