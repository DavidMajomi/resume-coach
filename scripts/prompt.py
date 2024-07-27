import google.generativeai as genai
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def write_api_key_to_file(key, file):
    f = open(file, "w")
    f.write(key)
    f.close()


def read_api_key_from_file(path_to_file : str) -> str:
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            api_key = file.readline()
    else:
        raise Exception("File with api key does not exist")
    
    return api_key 




def prompt(message):
    genai.configure(api_key=read_api_key_from_file("../API keys/gemini_api_key.txt"))

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(message)
    
    return response.text

