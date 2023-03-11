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
        master.geometry("600x300")
        
        self.usernames_frame = Frame(master)
        self.usernames_frame.pack(side=LEFT, padx=10, pady=10)

        # Create a label widget for usernames
        self.usernames_label = Label(self.usernames_frame, text="Usernames", font=("Arial", 14, "bold"))
        self.usernames_label.pack(side=TOP)

        # Create a listbox widget to display the usernames
        self.usernames_listbox = Listbox(self.usernames_frame, width=20, font=("Arial", 12))
        self.usernames_listbox.pack(side=TOP, fill=Y)

        # Load the usernames from the credentials.txt file
        with open("credentials.txt", "r") as f:
            for line in f:
                username, _ = line.strip().split(",")
                self.usernames_listbox.insert(END, username)
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
        
        self.story_link_label = Label(master, text="Story link", font=("Arial", 14))
        self.story_link_label.pack()
        
        # self.story_link_var = StringVar()
        # self.story_link_var.trace("w", self.check_entry)
        
        self.story_link_entry = Entry(master, width=50)
        self.story_link_entry.pack()
        
        self.run_button = Button(master, text="Run Bot", command=self.run_instabot, state="disabled")
        self.run_button.pack()
        
        self.story_link_entry.bind("<KeyRelease>", lambda e: self.check_entry())
        self.check_entry()

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
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.update_usernames_listbox()
    
    def update_usernames_listbox(self):
        # Clear the existing items in the listbox
        self.usernames_listbox.delete(0, END)
        
        # Read the contents of the file and add them to the listbox
        with open('credentials.txt', 'r') as f:
            for line in f:
                # Extract the username from the line and add it to the listbox
                username = line.split(',')[0]
                self.usernames_listbox.insert(END, username)

    def run_instabot(self):
        with InstaBot("chrome", "credentials.txt") as bot:
            bot.get_url()

            with open(bot.credentials_file, "r") as f:
                for credentials in bot.read_credentials():
                    # credentials=Credentials(bot.read_credentials())
                    # brea
                    # Login to the account
                    credentials_check = bot.login(credentials)
                    
                    if credentials_check:
                        # Do something with the account
                        bot.story_view(self.story_link_entry.get(),credentials.email[:credentials.email.index("@")])
                    else:
                        continue

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
        
    def check_entry(self):
        if not self.story_link_entry.get():
            self.run_button.config(state=DISABLED)
        else:
            self.run_button.config(state=NORMAL)


root = Tk()
app = App(root)
root.mainloop()
