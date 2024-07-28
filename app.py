from flask import Flask, request, abort
import os
import multiprocessing
from scripts.prompt import prompt
from read_pdf import extract_text_from_pdf

import smtplib 


import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

LOCK = multiprocessing.Lock()

LIST_Of_FILES = []
TOTAL_NUM_USERS = 0

def output_line_to_file(key, file):
    f = open(file, "w")
    f.write(key)
    f.close()
    


def read_file_line(path_to_file : str) -> str:
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            val = file.readline()
    else:
        raise Exception("File does not exist")
    
    return val 

def read_all_emails():
    f = open("../emails.txt", "r")
    lines = f.readlines()
    
    f.close()
    
    f = open("../emails.txt", "w")
    f.write("")
    f.close()
    
    return lines


def get_num_users():
    return int(read_file_line("../num_users.txt"))


def increment_num_users():
    # TOTAL_NUM_USERS += 1
    number_of_users = int(read_file_line("../num_users.txt"))
    print(number_of_users)
    output_line_to_file(str(number_of_users + 1), "../num_users.txt")
    
    
def append_email_to_file(val):
    val = val + "\n"
    f = open("../emails.txt", "a")
    f.write(val)
    f.close()







def mail_response(response, email):
    

    your_google_email = read_file_line("../gmail.txt")  # The email you setup to send the email using app password
    your_google_email_app_password = read_file_line("../gmail_password.txt")  # The app password you generated
    
    
    print(email)
    print(your_google_email)
    print(your_google_email_app_password)

    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(your_google_email, your_google_email_app_password)

    
    sent_from = your_google_email
    sent_to = email  
    sent_subject = "You Resume Insights"
    
    email_text = f"""\
    From: {sent_from}
    To: {sent_to}
    Subject: {sent_subject}

    {response}
    """
    
    smtpserver.sendmail(sent_from, sent_to, email_text)

    # Close the connection
    smtpserver.close()



@app.route('/num_users', methods=['GET','POST'])
def num_users():
    return f"{get_num_users()}"


@app.route('/process_uploads', methods=['GET','POST'])
def process_uploads():
    list_of_files = read_all_emails()
    print(list_of_files)
    if len(list_of_files) > 0:
        count = 15
        while (count > 0):
            if len(list_of_files) > 0:
                email = list_of_files[0]
                email = email.replace('\n', '')
                file_name = email + ".pdf"
                
                message_to_send = extract_text_from_pdf("../uploads/" + file_name)
                response = prompt(message_to_send)
                mail_response(response, email)
                
                os.remove("../uploads/" + file_name)
                
                
                list_of_files.pop(0)
                
            count += -1
            
    
        return "Done processing"
    
    else:
        return "Nothing to process"
    

@app.route('/upload_pdf', methods=['GET','POST'])
def upload_pdf():
    # message = prompt("")
    # print(message)
    
    if 'file' not in request.files:
        abort(400, "No file part")
    
    file = request.files['file']
    name = request.form.get('email')
    
    if file.filename == '':
        abort(400, "No selected file")
    
    if not name:
        abort(400, "No name provided")
    
    if file and file.filename.endswith('.pdf'):
        filename = f"{name}.pdf"
        
        
        
        LOCK.acquire()
        append_email_to_file(name)
        # print(LIST_Of_FILES[0])
        increment_num_users()
        LOCK.release()
        
        file_path = os.path.join('../uploads', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        return f"Your resume was uploaded successfully.", 200
    
    
    return "Completed"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
