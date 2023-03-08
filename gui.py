# import tkinter as tk
# from pydantic import BaseModel, validator

# class LoginDetails(BaseModel):
#     email: str
#     password: str

#     @validator('email')
#     def email_validator(cls, v):
#         if not '@' in v:
#             raise ValueError('Invalid email')
#         return v

#     # @validator('password')
#     # def password_validator(cls, v):
#     #     if len(v) < 6:
#     #         raise ValueError('Password must be at least 6 characters')
#     #     return v

# class LoginGUI:
#     def __init__(self, filename):
#         self.filename = filename
    
#     def submit(self):
#         email = self.email_entry.get()
#         password = self.password_entry.get()

#         try:
#             login_details = LoginDetails(email=email, password=password)
#             with open(self.filename, 'a') as f:
#                 f.write(f"{email}:{password}\n")
#             self.email_entry.delete(0, tk.END)
#             self.password_entry.delete(0, tk.END)
#             self.error_label.pack_forget() # remove error message, if any
#             print("Login details saved successfully!")
#         except ValueError as e:
#             self.error_label = tk.Label(self.window, text=str(e), fg='red', font=("Arial", 8))
#             self.error_label.pack()

#     def clear_data(self):
#         with open(self.filename, 'w') as f:
#             f.write('')
#         print("All login details cleared successfully!")
    
#     def close(self):
#         self.window.destroy()
    
#     def create_window(self):
#         # create a new window
#         self.wi 

#         # set window title and dimensions
#         self.window.title("Login")
#         self.window.geometry("400x300")

#         # create a label widget for email
#         email_label = tk.Label(self.window, text="Email:", font=("Arial", 14))
#         email_label.pack()

#         # create an entry widget for email
#         self.email_entry = tk.Entry(self.window, font=("Arial", 14))
#         self.email_entry.pack()

#         # create a label widget for password
#         password_label = tk.Label(self.window, text="Password:", font=("Arial", 14))
#         password_label.pack()

#         # create an entry widget for password
#         self.password_entry = tk.Entry(self.window, show="*", font=("Arial", 14))
#         self.password_entry.pack()

#         # create a button widget to submit the form
#         submit_button = tk.Button(self.window, text="Submit", command=self.submit, font=("Arial", 14))
#         submit_button.pack()

#         # create a label widget for error message
#         self.error_label = tk.Label(self.window, text="", fg='red', font=("Arial", 14))

#         # create a button widget to clear all data
#         clear_button = tk.Button(self.window, text="Clear All Data", command=self.clear_data, font=("Arial", 14))
#         clear_button.pack()

#         # create a button widget to close the window
#         close_button = tk.Button(self.window, text="Close", command=self.close, font=("Arial", 14))
#         close_button.pack()

#         # run the main event loop
#         self.window.mainloop()

# login = LoginGUI("login_details.txt")
# login.create_window()
