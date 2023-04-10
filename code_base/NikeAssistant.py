from AI import AI
from scrapper import scrapper
import webbrowser
from ChatWindow import ChatWindow
import tkinter as tk
from tkinter import messagebox
import threading
import time

class NikeAssistant:
    def __init__(self, chat_window):
        self.trigger_word="hello nike"
        self.s = scrapper('')
        self.ai=AI()
        self.time=time
        
        #check for internet connection
        if self.s.check_internet_connection() == True:
            self.chat_window = chat_window
            threading.Thread(target=self.main, daemon=True).start()
        else:
            messagebox.showerror('No Internet', 'Please check your internet connection.')
            self.chat_window.destroy()
            self.chat_window.master.destroy()

    #greets the user when running the program
    def main(self):
        self.chat_window.add_chat_bubble("Hello I am Nike voice assistant.", from_system=True)
        self.ai.speak("Hello I am Nike voice assistant.")
        self.chat_window.add_chat_bubble("Enter ""Hello Nike"" to activate or help to view the instructions.",from_system=True)
        self.ai.speak("Enter hello nike to activate or help to view the instructions.")
        self.run()

    #check for the trigger word or help
    def run(self):
       while True:
            command = self.chat_window.send_message()
            if command is not None and self.trigger_word in command.lower():
                self.listen_for_commands()
            elif command is not None and "help" in command.lower():
                self.display_file('code_base/Help.txt')
                self.listen_for_commands()
            elif None:
                pass
            else:
                self.chat_window.input_field.insert('end', 'Invalid command.')

    #displays the help.txt into a message box
    def display_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
                messagebox.showinfo(title='Help', message=content)
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='File not found')

    #Waits for command from user
    def listen_for_commands(self):
        self.chat_window.add_chat_bubble("What can I help you with?", from_system=True)
        self.ai.speak("What can I help you with?")
        v_command = self.chat_window.send_message()
        if v_command is not None:
            self.self_command(v_command)

    #Asks user to continue using or not
    def command_again(self):
        self.chat_window.add_chat_bubble("Is there something else you need help with?", from_system=True)
        self.ai.speak("Is there something else you need help with?")
        answer = self.chat_window.send_message()
        while True:
            if answer is not None:
                if 'yes' in answer:
                    self.listen_for_commands()
                if 'no' in answer:
                    self.chat_window.add_chat_bubble('Shutting off!', from_system=True)
                    self.ai.speak('Shutting off')
                    self.chat_window.destroy()
                    self.chat_window.master.destroy()
                else:
                    self.chat_window.add_chat_bubble("Wrong command!")
                    self.ai.speak("Wrong command!")
            else:
                self.chat_window.input_field.insert('end', 'Invalid command.')
    
    #Conditions for possible commands
    def self_command(self, command):
        while True:
            if 'search' in command.lower():
                query = self.extract_query(command)
                self.search(query)
                self.command_again()
                self.time.sleep(10)
            if 'website' in command.lower():
                webbrowser.open('https://www.nike.com/ph/')
                self.command_again()
                self.time.sleep(10)
            if 'cart' in command.lower():
                webbrowser.open('https://www.nike.com/ph/cart')
                self.command_again()
                self.time.sleep(10)
            if 'favorites' in command.lower():
                webbrowser.open('https://www.nike.com/ph/favorites')
                self.command_again()
                self.time.sleep(10)
            if 'log in' in command or 'login' in command.lower():
                webbrowser.open('https://www.nike.com/ph/member/profile/login')
                self.command_again()
                self.time.sleep(10)
            if 'sale' in command or 'sales' in command.lower():
                webbrowser.open('https://www.nike.com/ph/w/sale-3yaep')
                self.command_again()
                self.time.sleep(10)
            if 'new' in command.lower():
                webbrowser.open('https://www.nike.com/ph/w/new-3n82y')
                self.command_again()
                self.time.sleep(10)
            if 'best' in command.lower():
                webbrowser.open('https://www.nike.com/ph/w/best-76m50')
                self.command_again()
                self.time.sleep(10)
            if 'custom' in command.lower():
                webbrowser.open('https://www.nike.com/ph/w/nike-by-you-shoes-6ealhzy7ok')
                self.command_again()
                self.time.sleep(10)
            if 'close' in command or 'terminate' in command or 'shut down' in command.lower():
                self.chat_window.add_chat_bubble('Shutting off!', from_system=True)
                self.ai.speak('Shutting off')
                self.chat_window.destroy()
                self.chat_window.master.destroy()
            if 'help' in command.lower():
                self.display_file('code_base/Help.txt')
                self.command_again()
            else:
                self.chat_window.input_field.insert('end', 'Invalid command.')
                command=self.chat_window.send_message()

    #Extracts the item that the user wants to search for
    def extract_query(self, command):
        # Remove the 'search' keyword from the command
        query = command.replace('search for', '')
        # Remove leading and trailing whitespaces
        query = query.strip()
        return query
    
    #shows the search results
    def search(self, query):
        self.chat_window.add_chat_bubble(f"Searching for {query}...", from_system=True)
        self.ai.speak(f"Searching for {query}.")
        self.scrapper = scrapper(query)
        search_result = self.scrapper.search_result()
        self.chat_window.add_chat_bubble(search_result, from_system=True)
        self.ai.speak(f'These are the results I found for {query}')
        while True:
            if not search_result.startswith("Error"):
                self.chat_window.add_chat_bubble("Do you want to open an item?", from_system=True)
                self.ai.speak("Do you want to open an item?")
                open = self.chat_window.send_message()
                if 'yes' in open:
                    self.chat_window.add_chat_bubble("Pick an item.", from_system=True)
                    self.ai.speak("Pick an item")
                    choice = self.chat_window.send_message()
                    if '1' in choice or 'one' in choice:
                        self.s.pick_result(1)
                        self.command_again()
                    if '2' in choice or 'two' in choice:
                        self.s.pick_result(2)
                        self.command_again()
                    if '3' in choice or 'three' in choice:
                        self.s.pick_result(3)
                        self.command_again()
                    if '4' in choice or 'four' in choice:
                        self.s.pick_result(4)
                        self.command_again()
                    if '5' in choice or 'five' in choice:
                        self.s.pick_result(5)
                        self.command_again()
                if 'no' in open:
                    self.command_again()
                else:
                    self.chat_window.add_chat_bubble("Wrong command!")
                    self.ai.speak("Wrong command!")

# create an instance of the NikeAssistant class 
root = tk.Tk()
#root.geometry('420x500')
chat_window = ChatWindow(root)
root.title("Nike Bot")
root.wm_attributes("-topmost", 1)
img = tk.PhotoImage(file='code_base/nike_logo.png')
root.iconphoto(False,img)

#instance of nike assistant
nike_assistant = NikeAssistant(chat_window)

# Set the window dimensions
width = chat_window.width
height = chat_window.height

# Get the screen dimensions
screen_width = root.winfo_screenwidth() -10
screen_height = root.winfo_screenheight()-30

root.update()

# Calculate the x and y coordinates for the bottom-right corner
x = screen_width - width
y = screen_height - height

# Set the window location and dimensions
root.geometry("{}x{}+{}+{}".format(width, height, x, y))
root.mainloop()
