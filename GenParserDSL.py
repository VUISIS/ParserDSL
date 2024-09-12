import os
import sys
from datetime import datetime

from openai import OpenAI
from PyPDF2 import PdfReader

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
            max_tokens=4096,
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

def untar_code_extraction(text_3d_lang_specs, text_untar_latest):
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())

    question = "Summarize the c code untar_latest.c in pseudo code"
    question2 = "Understand the c code untar_latest.c and rewrite it in Prolog language"
    question3 = "Understand the c code untar_latest.c and rewrite it in FORMULA language"
    question4 = "Understand the c code untar_latest.c and rewrite it in state machine"

    result = call_openai_api(
        # System role
        # text_formula_documentation + 
        [
            # "Read and understand FORMULA documentation" + text_formula_simple_documentation,
            "Read and understand the following code in C language: " + text_untar_latest
        ], 
        # Assistant role
        [], 
        # User role
        [question4]
    )
    return result

def extract_dsl_into_3d(text_3d_lang_specs, text_untar_latest):
    extract_dsl_question = "Understand the 3D language specification and extract the C code into \
        The 3d Dependent Data Description language"

    # result = process_large_text("\n".join(texts), chunk_size=10000)
    result = call_openai_api(
        # System role
        ["Read and learn the following 3D language documentation: " + text_3d_lang_specs, 
         "Read and understand the following code in C language: " + text_untar_latest], 
        # Assistant role
        [], 
        # User role
        [extract_dsl_question]
    )
    return result
    

def fix_cve_2009_1270(text_3d_lang_specs, text_untar_latest):
    text_untar_negsize = read_file_into_text("./data/untar_negsize.c")
    text_untar_negsize_fixed = read_file_into_text("./data/untar_negsize_fixed.c")

    extract_dsl_question2 = "Understand the 3D language specification and extract the C code into \
        The 3d Dependent Data Description language for both untar_negsize.c and untar_negsize_fixed.c"
    
    result = call_openai_api(
        ["Read and learn the following 3D language documentation: " + text_3d_lang_specs, 
         "Read and understand the following code in untar_negsize.c: " + text_untar_negsize, 
         "Read and understand the following code in untar_negsize_fixed.c: " + text_untar_negsize_fixed],
        [],
        [
            # "Find the difference between the two files untar_negsize.c and untar_negsize_fixed.c"
            extract_dsl_question2
        ]
    )
    return result

def fix_cve_2017_12378(text_3d_lang_specs, text_untar_latest):
    text_untar_bb11946 = read_file_into_text("./data/untar_bb11946.c")
    text_untar_bb11946_fixed = read_file_into_text("./data/untar_bb11946_fixed.c")

    # There are several CVEs fixed in ClamAV 0.99.3
    # https://blog.clamav.net/2018/01/clamav-0993-has-been-released.html
    
    # extract_dsl_question3 = "Understand the 3D language specification and extract the C code into \
    #     The 3d Dependent Data Description language for both untar_bb11946.c and untar_bb11946_fixed.c"
    extract_dsl_question3 = "Understand the 3D language specification, \
        find the difference between untar_bb11946.c and untar_bb11946_fixed.c, \
        and extract the C code into The 3d Dependent Data Description language that fixes the bug."
    
    result = call_openai_api(
        ["Read and learn the following 3D language documentation: " + text_3d_lang_specs, 
         "Read and understand the following code in untar_bb11946.c: " + text_untar_bb11946, 
         "Read and understand the following code in untar_bb11946_fixed.c: " + text_untar_bb11946_fixed],
        [],
        [
            extract_dsl_question3
        ]
    )
    return result

def create_formula_parser_domain(text_3d_lang_specs, text_untar_latest):
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())

    question0 = "Summarize the FORMULA documentation with examples"
    
    question1 = "Understand the formula documentation and write a FORMULA domain for a generic data format parser"
    
    question2 = "Understand the formula documentation and write a FORMULA domain for a data format parser that has \
        two pointers moving forward when reading and transforming data"
    
    question3 = "Understand the formula documentation and 3D language specification, \
        Write a FORMULA domain to model 3D language"
 
    result = call_openai_api(
        # text_formula_documentation, 
        [text_formula_simple_documentation, text_3d_lang_specs],
        [], 
        [question3]
    )
    return result

if __name__ == "__main__":
    text_3d_lang_specs = read_file_into_text("./data/3d-lang.rst")
    text_untar_latest = read_file_into_text("./data/untar.c")

    result = untar_code_extraction(text_3d_lang_specs, text_untar_latest)
    # result = extract_dsl_into_3d(text_3d_lang_specs, text_untar_latest)
    # result = fix_cve_2009_1270(text_3d_lang_specs, text_untar_latest)
    # result = fix_cve_2017_12378(text_3d_lang_specs, text_untar_latest)
    # result = create_formula_parser_domain(text_3d_lang_specs, text_untar_latest)

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