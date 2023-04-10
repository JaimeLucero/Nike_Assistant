import tkinter as tk
from PIL import Image, ImageTk
from ChatBubble import ChatBubble
from AI import AI
from scrapper import scrapper


class ChatWindow(tk.Frame):
    def __init__(self, master=None, width=420, height=500):
        super().__init__(master, width=width, height=height)

        self.width=width
        self.height=height
        self.scrapper=scrapper('')
        self.ai=AI()
        self.send_button_clicked = False

        self.pack(expand=True, fill='both')

        # Create a frame to hold the scrollable area
        self.chat_frame = tk.Frame(self, bg='#181818')
        self.chat_frame.pack(side='top', fill='both', expand=True)

        # Create a scrollable area to hold the chat bubbles
        self.canvas = tk.Canvas(self.chat_frame, bg='#181818', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Create a frame to hold the text field and buttons
        self.input_frame = tk.Frame(self, bg='darkgray')
        self.input_frame.pack(side='bottom', fill='x')

        # Create a text field for input
        self.input_field = tk.Text(self.input_frame, bd=0, bg='white', font=('Arial', 11), width=40, height=4)
        self.input_field.pack(side='left')

        #disable the input field if there is no internet
        if self.scrapper.check_internet_connection() == True:
            self.input_field.config(state='normal')
        else:
            self.input_field.config(state='disabled')

        # Load the send icon
        send_image = Image.open('code_base/send.png')
        send_image = send_image.resize((40, 40), Image.ANTIALIAS)
        send_icon = ImageTk.PhotoImage(send_image)

        # Create the send button
        self.send_button = tk.Button(self.input_frame, image=send_icon, bg='darkgray', bd=0, command=self.send_button) 
        self.send_button.image = send_icon  # keep a reference to the image to prevent garbage collection
        self.send_button.pack(side='right', padx=10, pady=10)

        # Load the mic icon
        mic_image = Image.open('code_base/mic.png')
        mic_image = mic_image.resize((40, 40), Image.ANTIALIAS)
        mic_icon = ImageTk.PhotoImage(mic_image)

        # Create the mic button
        self.mic_button = tk.Button(self.input_frame, image=mic_icon, bg='white', bd=0, command=self.start_listening)
        self.mic_button.image = mic_icon  # keep a reference to the image to prevent garbage collection
        self.mic_button.pack(side='right', expand=True, fill='both')

    
    def add_chat_bubble(self, text='', from_system=True):
        # Add a new chat bubble to the scrollable frame
        if from_system:
            system_bubble = ChatBubble(self.scrollable_frame, text=text, from_system=from_system)
            system_bubble.pack(side='top', anchor='w')
        else:
            user_bubble = ChatBubble(self.scrollable_frame, text=text, from_system=False)
            user_bubble.pack(side='top', anchor='e')
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def send_button(self):
        self.send_button_clicked = True

    def send_message(self):
        self.input_field.focus_set()  # give focus to the input field
        message = None
        while not self.send_button_clicked:  # wait for the send button to be clicked
            self.update()  # update the GUI to handle events
        message = self.input_field.get('1.0', 'end-1c').strip()  # get the text from the input field
        if message:  # check if the user entered any text
            self.add_chat_bubble(text=message, from_system=False)  # display the text as a chat bubble
        self.input_field.delete('1.0', 'end')  # clear the input field after sending the message
        self.send_button_clicked = False  # reset the variable to False
        return message  # return the text from the input field

    def start_listening(self):
        self.input_field.delete('1.0', 'end')  # clear the input field
        self.input_field.insert('end', 'Listening...')  # display a message indicating that the assistant is listening
        self.input_field.update()  # update the input field to display the message
        command = self.ai.listen()
        self.input_field.delete('1.0', 'end')  # clear the input field again
        self.input_field.insert('end', command)  # display the recognized speech in the input field


