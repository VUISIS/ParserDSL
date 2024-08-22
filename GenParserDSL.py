from openai import OpenAI
import os
from datetime import datetime

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_text_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


def read_file_into_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def call_openai_api(system_contents=[], assistant_contents=[], user_contents=[]):
    try:
        messages=[{ "role": "system", "content": system_content} for system_content in system_contents] + \
                [{"role": "assistant", "content": assistant_content} for assistant_content in assistant_contents] + \
                [{"role": "user", "content": user_content} for user_content in user_contents]
        # print(messages)

        response = client.chat.completions.create(
            model="gpt-4o", # GPT-4o has 30,000 TPM
            messages=messages,
            max_tokens=10000,
            stop=None,
            temperature=0.7
        )
        print(response.choices)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


def process_large_text(text, chunk_size=2000):
    chunks = split_text_into_chunks(text, chunk_size)
    responses = []

    # for chunk in chunks:
    #     response = call_openai_api(chunk)
    #     if response:
    #         responses.append(response)

    # return "\n".join(responses)

    response = call_openai_api(system_contents=chunks)
    return response


if __name__ == "__main__":
    text_3d_lang_specs = read_file_into_text("./3d-lang.rst")
    text_untar_code = read_file_into_text("./untar.c")

    extract_dsl_question = "Understand the 3D language specification and extract the C code into The 3d Dependent Data Description language"
    texts = [
        text_3d_lang_specs, 
        text_untar_code, 
        extract_dsl_question
    ]

    # result = process_large_text("\n".join(texts), chunk_size=10000)
    result = call_openai_api(
        # System role
        ["Read and learn the following 3D language documentation: " + text_3d_lang_specs, 
         "Read and understand the following code in C language: " + text_untar_code], 
        # Assistant role
        [], 
        # User role
        [extract_dsl_question])

    print(result)

    # Write the text to the file
    if result is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = f"example_{timestamp}.txt"
        folder_path = "./output"
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'w') as file:
            file.write(result)