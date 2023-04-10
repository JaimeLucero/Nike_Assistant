import tkinter as tk
from tkinter import font
import textwrap

class ChatBubble(tk.Canvas):
    def __init__(self, master=None, text='', from_system=True, bg='white', fg='black', padding=5, width=400, canvas_width=None, canvas_height=None, bubble_width=500):
        super().__init__(master, bg=bg, highlightthickness=0, relief='flat', width=bubble_width, height=1)

        self.configure(background='#181818')
        text = text.strip()
        self.bubble_width = bubble_width
        self.padding=padding

        # set font and color based on whether the bubble is from the system or the user
        if from_system:
            font = ('Arial', 10, 'bold')
            text_color = 'black'
            bg_color = '#FFFFFF'
            anchor_pos = 'w'
        else:
            font = ('Arial', 10, 'bold')
            text_color = 'white'
            bg_color = 'blue'
            anchor_pos = 'e'

        # get font object and calculate text dimensions
        font_obj = tk.font.Font(font=font)
        text_lines = self.wrap_text(text, font_obj, width - 2 * padding)
        text_width = max(font_obj.measure(line) for line in text_lines)
        text_height = font_obj.metrics('linespace') * len(text_lines)

        # calculate the size and position of the bubble
        rect_width = text_width + 2 * padding
        rect_height = text_height + 2 * padding

        # calculate the total height of the chat bubble
        num_newlines = text.count('\n')
        if num_newlines > 0 and text[-1] == '\n':
            num_newlines -= 1
        linespace = font_obj.metrics('linespace')
        total_lines = len(text_lines) + num_newlines
        if total_lines == 1:
            total_height = rect_height + padding * 2
        else:
            total_height = rect_height + (linespace * (total_lines-padding)) + padding *2

        # set the canvas height to the total height of the chat bubble
        self.configure(height=total_height)

        # create chat bubble shape using a rectangle with rounded corners
        if from_system:
            x = padding
            y = padding
        else:
            x = width - rect_width - padding
            y = self.winfo_height()
        self.create_rounded_rectangle(x, y, x + rect_width, total_height - padding,  fill=bg_color, outline=bg_color)

        #anchor the text based on if it is from user or the system
        text_anchor = 'nw' if from_system else 'nw'
        text_width = min(font_obj.measure(text), width - 2 * padding)
        text_x = padding + 5 if from_system else rect_width - padding - 5 - text_width + padding + (width - rect_width + 2 * self.bubble_width) / 2
        if not from_system:
            text_x = width - 2 * padding - text_width
        text_y = padding + 5

        # Split the text into lines using splitlines() method
        text_lines = text.splitlines()
        for line in text_lines:
            justify = 'right' if from_system else 'left'
            words = line.split()
            new_line = words[0]
            for word in words[1:]:
                if font_obj.measure(new_line + ' ' + word) < (width - 2 * padding):
                    new_line += ' ' + word
                else:
                    truncated_line = font_obj.measure(new_line) > text_width and new_line[:4] + "..." or new_line
                    self.create_text(text_x, text_y, anchor=text_anchor, font=font, text=truncated_line, fill=text_color, width=width - 2 * padding, justify=justify)
                    new_line = word
                    text_y += font_obj.metrics('linespace')  # update text_y here
            truncated_line = font_obj.measure(new_line) > text_width and new_line[:4] + "..." or new_line
            self.create_text(text_x, text_y, anchor=text_anchor, font=font, text=truncated_line, fill=text_color, width=width - 2 * padding, justify=justify)
            text_y += font_obj.metrics('linespace')

    #function that will wrap the text to a specific width
    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.measure(current_line + ' ' + word) <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    #function that will create the rounded rectangle
    def create_rounded_rectangle(self, x1, y1, width, height, radius = 20,  **kwargs):
        points = [x1+radius, y1,
                x1+radius, y1,
                width-radius, y1,
                width-radius, y1,
                width, y1,
                width, y1+radius,
                width, y1+radius,
                width, height-radius,
                width, height-radius,
                width, height,
                width-radius, height,
                width-radius, height,
                x1+radius, height,
                x1+radius, height,
                x1, height,
                x1, height-radius,
                x1, height-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
