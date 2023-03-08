import random
import time
from tkinter import *
from pydantic import BaseModel, validator
from typing import Optional

from Insta.insta import InstaBot


class Credentials(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_validator(cls, v):
        if not '@' in v:
            raise ValueError('Invalid email')
        return v

    # @validator('password')
    # def password_validator(cls, v):
    #     if len(v) < 6:
    #         raise ValueError('Password must be at least 6 characters')
    #     return v

class App:
    def __init__(self, master):
        self.master = master
        master.title("Instagram Bot")
        master.geometry("400x300")
        self.email_label = Label(master, text="Email", font=("Arial", 14))
        self.email_label.pack()
        self.email_entry = Entry(master)
        self.email_entry.pack()

        self.password_label = Label(master, text="Password", font=("Arial", 14))
        self.password_label.pack()
        self.password_entry = Entry(master, show="*")
        self.password_entry.pack()

        self.error_label = Label(master, text="", font=("Arial", 8))
        self.error_label.pack()

        self.submit_button = Button(master, text="Submit", command=self.save_credentials)
        self.submit_button.pack()

        self.run_button = Button(master, text="Run Bot", command=self.run_instabot)
        self.run_button.pack()

        self.delete_button = Button(master, text="Delete Data", command=self.delete_data)
        self.delete_button.pack()

    def save_credentials(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            credentials = Credentials(email=email, password=password)
        except ValueError as e:
            self.error_label.config(text=str(e), fg='red', font=("Arial", 8))
        else:
            with open("credentials.txt", "a+") as f:
                f.write(f"{email},{password}\n")
            self.error_label.config(text="")
            # self.run_button.config(state=NORMAL)

    def run_instabot(self):
        with InstaBot("chrome", "credentials.txt") as bot:
            bot.get_url()

            with open(bot.credentials_file, "r") as f:
                for credentials in bot.read_credentials():
                    # credentials=Credentials(bot.read_credentials())
                    # brea
                    # Login to the account
                    bot.login(credentials)

                    # Do something with the account
                    bot.do_something()

                    # Wait for some time before doing anything else
                    time.sleep(random.randint(10, 60))

    def delete_data(self):
        try:
            with open("credentials.txt", "w"):
                pass
        except FileNotFoundError:
            pass
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.error_label.config(text="")
        self.run_button.config(state=DISABLED)


root = Tk()
app = App(root)
root.mainloop()
