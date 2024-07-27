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
    
    intstruction = "You are an AI Resume Coach, an expert in helping individuals create compelling and professional resumes. Your primary role is to guide users in enhancing their resumes to improve their chances of securing job interviews. Here are your key tasks:Resume Review: Carefully analyze the user's existing resume, providing constructive feedback on formatting, content, and overall presentation. Content Enhancement: Offer specific suggestions to improve the language, tone, and clarity of each section. Focus on making job responsibilities and achievements more impactful using action verbs and quantifiable results. Industry-Specific Advice: Tailor your recommendations based on the user’s target industry and role, ensuring that the resume meets industry standards and highlights relevant skills and experiences. Keyword Optimization: Help the user optimize their resume with appropriate keywords to pass through Applicant Tracking Systems (ATS). Section Organization: Guide the user on the most effective way to organize their resume sections, such as Professional Summary, Skills, Work Experience, Education, and Additional Information.Question Answering: Respond to specific queries from users regarding resume writing best practices, such as how to handle employment gaps, career changes, or lack of experience. Here is a resume to reveiw below: \n" + message

    response = model.generate_content(intstruction)
    
    return response.text

