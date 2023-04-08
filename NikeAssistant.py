import secrets
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
        if self.s.check_internet_connection() == True:
            self.chat_window = chat_window
            threading.Thread(target=self.main, daemon=True).start()
        else:
            messagebox.showerror('No Internet', 'Please check your internet connection.')
            self.chat_window.destroy()
            self.chat_window.master.destroy()

    def main(self):
        self.chat_window.add_chat_bubble("Hello I am Nike voice assistant.", from_system=True)
        self.ai.speak("Hello I am Nike voice assistant.")
        self.chat_window.add_chat_bubble("Enter ""Hello Nike"" to activate or help to view the instructions.",from_system=True)
        self.ai.speak("Enter hello nike to activate or help to view the instructions.")
        self.run()

    def run(self):
       while True:
            command = self.chat_window.send_message()
            if command is not None and self.trigger_word in command.lower():
                self.listen_for_commands()

    def listen_for_commands(self):
        self.chat_window.add_chat_bubble("What can I help you with?", from_system=True)
        self.ai.speak("What can I help you with?")
        v_command = self.chat_window.send_message()
        if v_command is not None:
            self.self_command(v_command)

    def command_again(self):
        self.chat_window.add_chat_bubble("Is there something else you need help with?", from_system=True)
        self.ai.speak("Is there something else you need help with?")
        answer = self.chat_window.send_message()
        if answer is not None:
            if 'yes' in answer:
                self.listen_for_commands()
            if 'no' in answer:
                self.chat_window.add_chat_bubble('Shutting off!', from_system=True)
                self.ai.speak('Shutting off')
                self.chat_window.destroy()
                self.chat_window.master.destroy()
    
    def self_command(self, command):
        if 'search' in command:
            query = self.extract_query(command)
            self.search(query)
            self.command_again()
            self.time.sleep(10)
        if 'website' in command:
            webbrowser.open('https://www.nike.com/ph/')
            self.command_again()
            self.time.sleep(10)
        if 'cart' in command:
            webbrowser.open('https://www.nike.com/ph/cart')
            self.command_again()
            self.time.sleep(10)
        if 'favorites' in command:
            webbrowser.open('https://www.nike.com/ph/favorites')
            self.command_again()
            self.time.sleep(10)
        if 'login' in command:
            webbrowser.open('https://www.nike.com/ph/member/profile/login')
            self.command_again()
            self.time.sleep(10)
        if 'sale' in command or 'sales' in command:
            webbrowser.open('https://www.nike.com/ph/w/sale-3yaep')
            self.command_again()
            self.time.sleep(10)
        if 'new' in command:
            webbrowser.open('https://www.nike.com/ph/w/new-3n82y')
            self.command_again()
            self.time.sleep(10)
        if 'best' in command:
            webbrowser.open('https://www.nike.com/ph/w/best-76m50')
            self.command_again()
            self.time.sleep(10)
        if 'custom' in command:
            webbrowser.open('https://www.nike.com/ph/w/nike-by-you-shoes-6ealhzy7ok')
            self.command_again()
            self.time.sleep(10)
        if 'close' in command or 'terminate' in command or 'shut down' in command:
            self.chat_window.add_chat_bubble('Shutting off!', from_system=True)
            self.ai.speak('Shutting off')
            self.chat_window.destroy()
            self.chat_window.master.destroy()
        if 'help' in command:
            pass

    def extract_query(self, command):
        # Remove the 'search' keyword from the command
        query = command.replace('search for', '')
        # Remove leading and trailing whitespaces
        query = query.strip()
        return query
        
    def search(self, query):
        self.chat_window.add_chat_bubble(f"Searching for {query}...", from_system=True)
        self.ai.speak(f"Searching for {query}.")
        self.s(query)
        self.chat_window.add_chat_bubble(self.s.search_result(), from_system=True)

        if 'Error' not in self.s.search_result():
            self.ai.speak(f'These are the results I found for {query}')
            choice = self.chat_window.send_message()
            if '1' in choice or 'one' in choice:
                self.s.pick_result(1)
            if '2' in choice or 'two' in choice:
                self.s.pick_result(2)
            if '3' in choice or 'three' in choice:
                self.s.pick_result(3)
            if '4' in choice or 'four' in choice:
                self.s.pick_result(4)
            if '5' in choice or 'five' in choice:
                self.s.pick_result(5)

# create an instance of the NikeAssistant class 
root = tk.Tk()
#root.geometry('420x500')
chat_window = ChatWindow(root)
root.title("Nike Bot")
root.wm_attributes("-topmost", 1)
img = tk.PhotoImage(file='nike logo.png')
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
