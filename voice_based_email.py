from tkinter import *
import os
import smtplib
from tkinter import *
import imaplib
import pyttsx3
import speech_recognition as sr
from email.message import EmailMessage
import tkinter as tk
import email
from email.header import decode_header
import webbrowser
import os



# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()






# Create the main window


########################compose########################
def get_info():
 try:
        
   with sr.Microphone() as source:
            listener = sr.Recognizer()
            print('listening...')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            
            return info.lower()
            text_box.insert(end,info)
 except:
     pass
        
    


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('jkarunakarreddy78@gmail.com', 'oclmvbpztfikfbgx')
    email = EmailMessage()
    email['From'] = 'jkarunakarreddy78@gmail.com'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)


email_list = {
    'sara':'sk8451287@gmail.com',
    'sai vivek':'saivivek1809@gmail.com',
    'nitin':'nithinbhimavarapu1234@gmail.com',
    'rafi':'khajarafiuddin17@gmail.com'



}


def get_email_info():
    engine = pyttsx3.init()
    engine.say('Hi Sir I am your assistant for today, To Whom you want to send email')
    engine.runAndWait()
    name = get_info()
    receiver = email_list[name]
    print(receiver)
    engine.say('What is the subject of your email?')
    engine.runAndWait()
    subject = get_info()
    engine.say('Tell me the text in your email')
    engine.runAndWait()
    message = get_info()
    send_email(receiver, subject, message)
    engine.say('Thankyou sir for using me. Your email has been send')
    engine.runAndWait()


################################sentmail################################

def sent_mail():
    username = "jkarunakarreddy78@gmail.com"
    password = "oclmvbpztfikfbgx"
    imap_server = "imap.gmail.com"



    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)


    status, messages = imap.select('"[Gmail]/Sent Mail"')
    engine=pyttsx3.init()
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                To, encoding = decode_header(msg.get("To"))[0]
                if isinstance(To, bytes):
                    To = To.decode(encoding)    
                print("Subject:", subject)
                print("From:", From)
                print("To:", To)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                            engine.say(body)
                            engine.runAndWait()
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                        
            
            engine.say("it is from"+From)
            engine.runAndWait()
            engine.say("the subject is" + subject)
            engine.runAndWait()
            engine.say("the body is"+body)
            engine.runAndWait()
            # close the connection and logout
    imap.close()
    imap.logout()
#########################read mails########################################
#account credentials
def read_mails():
    username = "jkarunakarreddy78@gmail.com"
    password = "oclmvbpztfikfbgx"
    imap_server = "imap.gmail.com"



    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)


    status, messages = imap.select("Inbox")
    engine=pyttsx3.init()
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                To, encoding = decode_header(msg.get("To"))[0]
                if isinstance(To, bytes):
                    To = To.decode(encoding)    
                print("Subject:", subject)
                print("From:", From)
                

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                            engine.say(body)
                            engine.runAndWait()
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                        
            
                engine.say("it is from"+From)
                engine.runAndWait()
            #   engine.say("it is sent to" + To)
            #   engine.runAndWait()
                engine.say("the subject is" + subject)
                engine.runAndWait()
                engine.say("the body is"+body)
                engine.runAndWait()
            # close the connection and logout
    imap.close()
    imap.logout()





          






			# printing the details		
	
    ####################bin mails###############
    
def bin_mails():
    username = "jkarunakarreddy78@gmail.com"
    password = "oclmvbpztfikfbgx"
    imap_server = "imap.gmail.com"



    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)


    status, messages = imap.select('"[Gmail]/Trash"')
    engine=pyttsx3.init()
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                To, encoding = decode_header(msg.get("To"))[0]
                if isinstance(From, bytes):
                    To = To.decode(encoding)

                print("Subject:", subject)
                print("From:", From)
                print("To:", To)

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                            engine.say(body)
                            engine.runAndWait()
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                        
            
            engine.say("it is from"+From)
            engine.runAndWait()
            engine.say("the subject is" + subject)
            engine.runAndWait()
            engine.say("the body is"+body)
            engine.runAndWait()
            engine.say("it is sent to"+To)
            engine.runAndWait()
            # close the connection and logout
    imap.close()
    imap.logout()




         


    
       

def newpage():
    # Import the require
            global main_screen
            main_screen = Tk()

             
            def leftclick(event):
                        print("left")
                        print("compose mail")
                        get_email_info()

            def rightclick(event):
                        print("right")
                        print("reading sent mails")
                        sent_mail()

            def doubleclickleft(event):
                        print("doubleclickleft")
                        print("reading mails from inbox")
                        read_mails()

            def doubleclickright(event):
                        print("doubleclickright")
                        print("logout")
                        destroy()
            def mouse_wheel(event):
                     bin_mails()
                     print("scrollingdown")
                     print("reading trash mails")        
                        

                                        
            frame = Frame(main_screen, width=300, height=250)

            frame.bind("<Button-1>",leftclick)

            frame.bind("<Button-3>", rightclick)

            frame.bind("<Double-Button-1>", doubleclickleft)

            frame.bind("<Double-Button-3>", doubleclickright)
            frame.bind("<MouseWheel>", mouse_wheel)

            

            frame.pack()

                    
            

            

            
            
           

                    
    # Import the require
        
            
            
            B1 = Button(main_screen, text="Compose Mail",command=get_email_info)
            B1.pack()
            B2 = Button(main_screen, text="Read Mails",command=read_mails)
            B2.pack()
            
            B3 = Button(main_screen, text="Sent Mails",command=sent_mail)
            B3.pack()
        
            B4 = Button(main_screen, text="Bin Mails",command=bin_mails)
            B4.pack()
            btn1 = Button(main_screen, text ="logout",command=main_screen.destroy)
            btn1.bind("<Return>", lambda eff: main_screen.destroy())
            btn1.pack()

            main_screen.mainloop()


    
            
           
            



            
# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()


# Designing popup for login success

def login_sucess():
    global login_success_screen
    # login_success_screen = Toplevel(login_screen)
    # login_success_screen.title("Success")
    # login_success_screen.geometry("150x100")
    # Label(login_success_screen, text="Login Success").pack()
    # Button(login_success_screen, text="OK", command=delete_login_success).pack()
    newpage()



# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window
def destroy():
     main_screen.destroy()

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()
    








    
main_account_screen()

