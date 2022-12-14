def files():
        loc=filedialog.askopenfilenames(filetypes=(("Image files",("*.jpg","*.png","*.jpeg")),))
        file_size=0
        for i in loc:
                file_size+=os.path.getsize(i)
        if(file_size<2097152):
                encrypt(loc,32)
        elif(file_size<10485760):
                encrypt(loc,24)
        else:
                encrypt(loc,16)
def encrypt(loc,byte):
        count=1
        files=[]
        key = get_random_bytes(byte)
        for i in loc:
                with open (i,'rb') as f:
                        img=base64.b64encode(f.read())
                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(img)
                eloc=os.path.dirname(os.path.abspath(i))+"\Encrypted Image"+str(count)+".bin"
                files.append(eloc)
                with open(eloc, "wb") as f:
                        f.write(cipher.nonce)
                        f.write(tag)
                        f.write(ciphertext)
                count+=1
        en_successful(files,key)
def decrypt(key):
        loc=filedialog.askopenfilenames(filetypes=(("Bin files","*.bin"),))
        count=1
        files=[]
        for i in loc:
                try:  
                        with open(i, "rb") as f:
                                nonce=f.read(16)
                                tag=f.read(16)
                                ciphertext=f.read(-1)
                                cipher = AES.new(key, AES.MODE_EAX, nonce)
                                img=base64.b64decode(cipher.decrypt_and_verify(ciphertext, tag))
                        deloc=os.path.dirname(os.path.abspath(i))+"\Decrypted Image"+str(count)+".jpg"
                        files.append(deloc)
                        with open(deloc, "wb") as f:
                                f.write(img)
                except:
                        error()
                count+=1
        dec_successful(files)

def get_key():
        gk=CTk()
        gk.focus_force()
        gk.geometry('500x200')
        gk.title('PixCrypt')

        k=StringVar()

        def key():
                key=k.get()
                key=key.encode()
                key=key.decode('unicode-escape').encode('ISO-8859-1')
                decrypt(key)
                
        
        lab_1=CTkLabel(gk,text='Enter Key',fg_color=None,text_color="white",text_font=('bold',35)).place(relx=0.5,y=50,anchor='center')
        ent_1=CTkEntry(gk,textvar=k,fg_color='white',corner_radius=8,text_color='black',width=200).place(relx=0.5,y=100,anchor='center')
        but_1=CTkButton(gk,text='Decrypt',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[gk.destroy(),key()]).place(relx=0.5,y=150,anchor='center')
        gk.mainloop()

def email(loc):
                
        em=CTk()
        em.focus_force()
        em.geometry('600x400')
        em.title('PixCrypt')

        sen=StringVar()
        pas=StringVar()
        rec=StringVar()

        def send(loc):
                sender=sen.get()
                password=pas.get()
                receiver=rec.get()

                mail=MIMEMultipart()
                mail['From']=sender
                mail['To']=receiver
                mail['Subject']="File"

                for i in loc:
                        attatchment=MIMEBase('application','octet-stream')

                        with open(i ,"rb") as f:
                            attatchment.set_payload(f.read())

                        encoders.encode_base64(attatchment)
                        attatchment.add_header("Content-Disposition","attatchment;filename=File.bin")

                        mail.attach(attatchment)

                smtp=smtplib.SMTP('smtp.gmail.com',587)
                smtp.starttls()
                smtp.login(sender,password)
                s=mail.as_string()
                smtp.sendmail(sender,receiver,s)
                smtp.quit()

                em_successful()
        
        lab_1=CTkLabel(em,text='Send Email',fg_color=None,text_color="white",text_font=('bold',30)).place(relx=0.5,y=50,anchor='center')

        lab_2=CTkLabel(em,text='Your Email Address:',fg_color=None,text_color="white",text_font=('bold',20)).place(relx=0.3,y=150,anchor='center')
        ent_2=CTkEntry(em,textvar=sen,fg_color='white',corner_radius=8,text_color='black',width=200).place(relx=0.8,y=150,anchor='center')
        
        lab_3=CTkLabel(em,text='App Password:',fg_color=None,text_color="white",text_font=('bold',20)).place(relx=0.3,y=200,anchor='center')
        lab_3_1=CTkLabel(em,text='(Google Account-->App Passwords)',fg_color=None,text_color="red",text_font=('bold',10)).place(relx=0.3,y=230,anchor='center')
        ent_3=CTkEntry(em,textvar=pas,fg_color='white',corner_radius=8,text_color='black',width=200).place(relx=0.8,y=200,anchor='center')

        lab_4=CTkLabel(em,text='Receiver\'s Email Address:',fg_color=None,text_color="white",text_font=('bold',20)).place(relx=0.3,y=280,anchor='center')
        ent_4=CTkEntry(em,textvar=rec,fg_color='white',corner_radius=8,text_color='black',width=200).place(relx=0.8,y=280,anchor='center')

        but_1=CTkButton(em,text='Send',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[em.destroy(),send(loc)]).place(relx=0.25,y=350,anchor='center')
        but_2=CTkButton(em,text='Exit',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.75,y=350,anchor='center')


        em.mainloop()

def display(loc):
        for i in loc:
                img=Image.open(i)
                img.show()
        os._exit(0)

def en_successful(loc,key):
        suc=CTk()
        suc.focus_force()
        suc.geometry('600x300')
        suc.title('PixCrypt')
        key=str(key)
        key=key.lstrip("'b")
        key=key.rstrip("'")
        keyvar=StringVar()
        keyvar.set(key)
        lab_1=CTkLabel(suc,text='Encryption Successful',fg_color=None,text_color="white",text_font=('bold',35)).place(relx=0.5,y=75,anchor='center')
        lab_2=CTkLabel(suc,text='Cipher Key:-',fg_color=None,text_color="white",text_font=('bold',25)).place(relx=0.5,y=150,anchor='center')
        ent_1=CTkEntry(suc,textvar=keyvar,text_font=('bold',10),relief='flat',width=300,state='readonly',readonlybackground='black',fg_color='black',bg_color='white').place(relx=0.5,y=200,anchor='center')
        but_1=CTkButton(suc,text='Exit',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.75,y=250,anchor='center')
        but_2=CTkButton(suc,text='Send as Email',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[suc.destroy(),email(loc)]).place(relx=0.25,y=250,anchor='center')
        suc.mainloop()
        
def dec_successful(loc):
        suc=CTk()
        suc.focus_force()
        suc.geometry('500x200')
        suc.title('PixCrypt')
        lab_1=CTkLabel(suc,text='Decryption Successful',fg_color=None,text_color="white",text_font=('bold',35)).place(relx=0.5,y=75,anchor='center')
        but_1=CTkButton(suc,text='Exit',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.75,y=150,anchor='center')
        but_2=CTkButton(suc,text='View Images',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[suc.destroy(),display(loc)]).place(relx=0.25,y=150,anchor='center')
        suc.mainloop()

def em_successful():
        suc=CTk()
        suc.focus_force()
        suc.geometry('500x200')
        suc.title('PixCrypt')
        lab_1=CTkLabel(suc,text='Successful',fg_color=None,text_color="white",text_font=('bold',35)).place(relx=0.5,y=75,anchor='center')
        but_1=CTkButton(suc,text='Exit',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.5,y=150,anchor='center')
        suc.mainloop()

def error():
        err=CTk()
        err.focus_force()
        err.geometry('500x250')
        err.title('PixCrypt')
        lab_1=CTkLabel(err,text='Error',fg_color=None,text_color="white",text_font=('bold',40)).place(relx=0.5,y=50,anchor='center')
        lab_2=CTkLabel(err,text='Invalid key',fg_color=None,text_color="red",text_font=('bold',20)).place(relx=0.5,y=125,anchor='center')
        but_1=CTkButton(err,text='Home',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[err.destroy(),main()]).place(relx=0.25,y=200,anchor='center')
        but_2=CTkButton(err,text='Exit',fg_color='black',text_color="white",text_font=('bold',20),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.75,y=200,anchor='center')
        err.mainloop()
def main():
    main=CTk()
    main.geometry('500x400')
    main.title('PixCrypt')
    lab_1=CTkLabel(main,text='PixCrypt\nImage Encrypter',fg_color=None,text_color="white",text_font=('bold',45)).place(relx=0.5,y=80,anchor='center')
    but_1=CTkButton(main,text='Encrypt',fg_color='black',text_color="white",text_font=('bold',30),corner_radius=8,hover_color="#545352",command=lambda:[main.destroy(),files()]).place(relx=0.25,y=220,anchor='center')
    but_2=CTkButton(main,text='Decrypt',fg_color='black',text_color="white",text_font=('bold',30),corner_radius=8,hover_color="#545352",command=lambda:[main.destroy(),get_key()]).place(relx=0.75,y=220,anchor='center')
    but_3=CTkButton(main,text='Exit',fg_color='black',text_color="white",text_font=('bold',30),corner_radius=8,hover_color="#545352",command=lambda:[os._exit(0)]).place(relx=0.5,y=320,anchor='center')
    main.mainloop()

from tkinter import*
from customtkinter import *
set_appearance_mode("dark")
from tkinter import filedialog

import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from PIL import Image
main()
