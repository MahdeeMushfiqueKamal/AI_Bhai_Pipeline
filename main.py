from dotenv import load_dotenv
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import sys
import cv2
import textwrap

load_from_file = True


def generate_content(title: str):
    load_dotenv()
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        print("OPENAI_API_KEY found in environment variables")
    except:
        print("Error while getting OPENAI_API_KEY from environment variables")
        sys.exit(1)

    llm = OpenAI(temperature=0.7, max_tokens=500, openai_api_key=openai_api_key)

    prompt_template = PromptTemplate(
        input_variables=["title", "number_of_facts", "max_characters"],
        template="""
    Imagine you making a facebook post that describes features of a technology. 
    Write {number_of_facts} interesting facts about {title}. 
    The fact doesn't need to be a full sentence. 
    Each fact should be on a new line.
    Each fact can have at max {max_characters} characters. 
    """,
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    llm_output = chain.run(
        {"title": title, "number_of_facts": 10, "max_characters": 45}
    )

    llm_output = llm_output.strip()

    f = open("output.txt", "w")
    f.write(llm_output)
    f.close()

    return llm_output


def add_text_to_image(img, text, output_path):
    font = cv2.FONT_HERSHEY_SIMPLEX
    wrapped_text = textwrap.wrap(text, width=24)
    x, y = 0, 0  # Starting coordinates set to 0
    font_size = 1.5
    font_thickness = 2

    y_offset = (len(wrapped_text)-1) * 40

    for i, line in enumerate(wrapped_text):
        text_size = cv2.getTextSize(line, font, font_size, font_thickness)[0]

        # Center horizontally
        x = int((img.shape[1] - text_size[0]) / 2) 

        gap = text_size[1] + 40

        y = int((img.shape[0] + text_size[1]) / 2) + i * gap - y_offset

        cv2.putText(img, line, (x, y), font,
                    font_size,
                    (0,0,0),
                    font_thickness,
                    lineType=cv2.LINE_AA)
        
    cv2.imwrite(output_path, img)


if __name__ == "__main__":
    title = sys.argv[1]
    print(f"Generating content for {title}")
    if load_from_file:
        with open("output.txt", "r") as f:
            llm_output = f.read()
    else:
        llm_output = generate_content(title)

    print("llm_output:")
    print(llm_output)

    sentences = llm_output.split("\n")

    if llm_output.startswith("1."):
        sentences = [sentence[3:] for sentence in sentences]

    print("sentences:")
    print(sentences)

    for index, sentence in enumerate(sentences):
        add_text_to_image(img = cv2.imread("background.png"), text = sentence, output_path = f"images/{index+1}.png")

    add_text_to_image(img = cv2.imread("background.png"), text = f"10 interesting facts about {title}", output_path = f"images/0.png")
