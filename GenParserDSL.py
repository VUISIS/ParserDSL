import os
import sys
from pprint import pprint
from datetime import datetime

from openai import OpenAI
from PyPDF2 import PdfReader

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_text_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def process_large_text(text, chunk_size=2000):
    chunks = split_text_into_chunks(text, chunk_size)
    responses = []

    # for chunk in chunks:
    #     response = call_openai_api(chunk)
    #     if response:
    #         responses.append(response)

    # return "\n".join(responses)

    response = ask_chatgpt(system_contents=chunks)
    return response


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


def ask_chatgpt(system_contents=[], assistant_contents=[], user_contents=[]):
    try:
        messages=[{ "role": "system", "content": system_content} for system_content in system_contents] + \
                [{"role": "assistant", "content": assistant_content} for assistant_content in assistant_contents] + \
                [{"role": "user", "content": user_content} for user_content in user_contents]

        response = client.chat.completions.create(
            model="gpt-4o", # GPT-4o has 30,000 TPM
            messages=messages,
            max_tokens=4096,
            stop=None,
            temperature=0.2 # Default is 0.7 and smaller number means less creative
        )
        # pprint(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
    
def ask_chatgpt_interactively(init_system_contents=[], init_assistant_contents=[], init_user_contents=[]):
    system_contents = init_system_contents
    assistant_contents = init_assistant_contents
    user_contents = init_user_contents

    chat_history = "*" * 64 + "\n" + \
                   "Context: \n" +   "\n++++++++++++++++++++++++++++++++\n".join(system_contents) + \
                   "\n" + "*" * 64 + "\n" + \
                   "Questions: \n" + "\n++++++++++++++++++++++++++++++++\n".join(user_contents) + \
                   "\n" + "*" * 64 + "\n"
 
    while True:
        response = ask_chatgpt(
            system_contents=system_contents,
            assistant_contents=assistant_contents,
            user_contents=user_contents
        )

        if response is not None:
            chat_history += "Response: \n" + response + "\n"
            print(response)

        print("Type 'exit' or 'quit' to end the interactive prompt.")

        user_prompt = input("Enter more question: ")
        
        if user_prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        user_contents.append(user_prompt)
        chat_history += "*" * 64 + "\n" + \
                        "Additional question: \n" + user_prompt + "\n" + \
                        "*" * 64 + "\n"

        if response is not None:
            # Add the response to the assistant contents
            assistant_contents.append(response)
    
    return chat_history

def test_gpt_interactively():
    user_prompt = input("Enter your first question: ")
    chat_history = ask_chatgpt_interactively(
        init_system_contents=[],
        init_assistant_contents=[],
        init_user_contents=[user_prompt]
    )
    return chat_history

def tar_in_prolog_to_formula():
    text_prolog_code = read_file_into_text("./prolog/tar.pl")
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    question = "Convert the Prolog code into FORMULA language"
    result = ask_chatgpt(
        [text_prolog_code, text_formula_simple_documentation],
        [],
        [question]
    )
    return result

def generate_formula_core_parser_domain():
    text_parser_abstract = """
    Parser Abstraction
    1. The current read and offset keep getting updated while moving forward until the end of the file in a while loop.
    2. There are variables for storing the current read and intermediate results such as a counter.
    3. Intermediate results are derived from the current read and other intermediate results by transforming and updating them.
    4. Intermediate results decide how the pointers move forward.
    """
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())

    question = "Understand the FORMULA documentation and model a generic data format parser with dependent data type based on the parser abstraction"
    result = ask_chatgpt_interactively(
        [text_parser_abstract] + text_formula_documentation,
        [],
        [question]
    )
    return result

def extend_formula_core_parser_domain(question):
    text_untar_wrong = read_file_into_text("./data/untar_bb11946.c")
    # text_untar_wrong = read_file_into_text("./data/untar_negsize.c")
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    text_formula_parser_core_dsl = read_file_into_text("./formula/ParserDSL.4ml")
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())
    
    # FORMULA is a DSL for high-level modeling and may not be able to catch all details in C code.
    # Suppose we have a working FORMULA DSL for Tar. How to prove that the DSL in FORMULA is equal to the C code? 
    # Maybe we don't care but just want to close the loop and find bugs in the C code.

    # Why don't we just use symbolic execution such as KLEE to find bugs in the C code?
    # Translate from code to code, from C to a low-level language such as prolog.  

    # Write specs in 3D or similar languages that generate a verified parser in F* language.
    # 3D language may not be able to deal with checksums and is also not supposed to do it in parsing anyway.

    result = ask_chatgpt_interactively(
        text_formula_documentation + [text_formula_parser_core_dsl] + [text_untar_wrong],
        [],
        [question]
    )
    return result

def untar_code_extraction_interactively():
    text_untar_wrong = read_file_into_text("./data/untar_negsize.c")
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    # Feeding the whole FORMULA PDF to GPT may exceed token limit but gives better results
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())

    question = "Understand the c code for tar parser and FORMULA documentation."
    question2 = "Understand the parsing logic of c code in untar_negsize.c and model it in NuSMV language"
    
    chat_history = ask_chatgpt_interactively(
        init_system_contents=[text_untar_wrong] + text_formula_documentation,
        init_assistant_contents=[],
        init_user_contents=[question2]
    )
    return chat_history

def untar_code_extraction(text_3d_lang_specs, text_untar_latest):
    text_formula_simple_documentation = read_file_into_text("./data/formula.txt")
    text_formula_documentation = []
    reader = PdfReader("./data/formula.pdf")
    for page in reader.pages:
        text_formula_documentation.append(page.extract_text())

    # Try to ask GPT interactively and let GPT tell you what information it needs
    question = "Summarize the c code untar.c in pseudo code"
    question2 = "Understand the c code untar.c and rewrite it in Prolog language"
    question3 = "Understand the c code untar.c and rewrite it in FORMULA language"
    question4 = "Understand the c code untar.c and rewrite it in state machine"
    question5 = "Understand the c code untar.c and represent it in state machine"
    question6 = "Understand parsing logic in untar.c and represent it in state machine, then convert it to FORMULA language"

    result = ask_chatgpt(
        # System role
        # text_formula_documentation + 
        [
            "Read and understand FORMULA documentation" + text_formula_simple_documentation,
            "Read and understand the following code in C language: " + text_untar_latest
        ], 
        # Assistant role
        [], 
        # User role
        [question6]
    )
    return result

def extract_dsl_into_3d(text_3d_lang_specs, text_untar_latest):
    extract_dsl_question = "Understand the 3D language specification and extract the C code into \
        The 3d Dependent Data Description language"

    # result = process_large_text("\n".join(texts), chunk_size=10000)
    result = ask_chatgpt(
        # System role
        ["Read and learn the following 3D language documentation: " + text_3d_lang_specs, 
         "Read and understand the following code in C language: " + text_untar_latest], 
        # Assistant role
        [], 
        # User role
        [extract_dsl_question]
    )
    return result


def convert_c_to_prolog(text_3d_lang_specs, text_untar_latest):
    question = "Convert the C code untar.c into Prolog language" 
    question2 = "Convert the C code untar.c into FORMULA language"
    result = ask_chatgpt(
        ["Read and understand the following code in untar.c: " + text_untar_latest],
        [],
        [question]
    )
    return result
    

def fix_cve_2009_1270(text_3d_lang_specs, text_untar_latest):
    text_untar_negsize = read_file_into_text("./data/untar_negsize.c")
    text_untar_negsize_fixed = read_file_into_text("./data/untar_negsize_fixed.c")

    extract_dsl_question2 = "Understand the 3D language specification and extract the C code into \
        The 3d Dependent Data Description language for both untar_negsize.c and untar_negsize_fixed.c"
    
    result = ask_chatgpt(
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
    
    result = ask_chatgpt(
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
 
    result = ask_chatgpt(
        # text_formula_documentation, 
        [text_formula_simple_documentation, text_3d_lang_specs],
        [], 
        [question3]
    )
    return result

if __name__ == "__main__":
    text_3d_lang_specs = read_file_into_text("./data/3d-lang.rst")
    text_untar_latest = read_file_into_text("./data/untar.c")
    question = read_file_into_text("./data/question1.txt")

    # result = test_gpt_interactively()

    # result = extract_dsl_into_3d(text_3d_lang_specs, text_untar_latest)
    # result = fix_cve_2009_1270(text_3d_lang_specs, text_untar_latest)
    # result = fix_cve_2017_12378(text_3d_lang_specs, text_untar_latest)
    # result = create_formula_parser_domain(text_3d_lang_specs, text_untar_latest)
    # result = convert_c_to_prolog(text_3d_lang_specs, text_untar_latest)
    # result = tar_in_prolog_to_formula()
    # result = untar_code_extraction(text_3d_lang_specs, text_untar_latest)
    # result = untar_code_extraction_interactively()
    # result = generate_formula_core_parser_domain()

    result = extend_formula_core_parser_domain(question)

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