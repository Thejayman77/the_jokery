##########################################
# The Jokery
# A little Python program demonstrating some
# cool components of Python.  Just having a
# little fun.
# - Jason Hegedus
# - v. 1.0.0
##########################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import json, sys
import urllib.request
from urllib.request import URLError, HTTPError, ContentTooShortError


##################
# Setup GUI object
##################
gui = tk.Tk()
gui.title("The jokery")
gui.geometry("640x480")
gui.resizable(width=False, height=False)

#################
# Classes
#################
class joke(object):
    def __init__(self):
        self.joke = ""
        self.auth = ""
        self.cat = ""
        self.explicit = False
    


#################
# Functions
#################
def down_url(url, user_agent="wswp@thejayman77@gmail.com", headers=[], num_retries=2):
    request = urllib.request.Request(url)

    # Add the headers into the request
    request.add_header("User-agent", user_agent)
    for h,v in headers:
        request.add_header(h, v)
    
    # Now request the actual website
    try:
        html = urllib.request.urlopen(request).read()
    except (HTTPError, URLError, ContentTooShortError) as e:
        print("Error:", e)
        html = None

        if num_retries > 0:
            if hasattr(e, "code") and 500 <= e.code < 600:

                # Return download function until retries deplted
                return down_url(url, headers = headers, num_retries = num_retries-1)
    return html.decode("utf-8")

def get_a_joke():
    global joke_box

    # Clear the current joke, if any
    joke_box.delete("1.0", tk.END)

    ## Get a joke (From one site for now)
    ## Using classes for later expansion (Possibly DB storage and whatnot)
    new_joke = joke()
    
    # Setup request headers
    header_list = []
    header_list.append(("Accept", "application/json"))

    # Get the joke
    joke_return = json.loads(down_url("https://icanhazdadjoke.com", headers=header_list))
    new_joke.joke = joke_return["joke"]

    joke_box.insert("1.0", new_joke.joke)

def quit_app():
    gui.destroy()
    sys.exit()


#################
# Whip up a quick GUI
#################
joke_label = tk.Label(gui, text="The joke:", font=("",12,"bold"), anchor=tk.SW, height=5)
joke_box = tk.scrolledtext.ScrolledText(gui, wrap="word", font=("Georgio", 14), fg="blue")
joke_button = tk.Button(gui, text="Get Joke", width=12, command=get_a_joke)
quit_button = tk.Button(gui, text="Quit", width=12, command=quit_app)

# Grids
gui.rowconfigure(0, weight=1)
gui.rowconfigure(1, weight=2)
gui.columnconfigure(0, weight=1)
joke_label.grid(column=0, row=0, sticky=tk.EW, pady=(0,6))
joke_box.grid(column=0, row=1, sticky=tk.NSEW, padx=(6,0), pady=(0,6))
joke_button.grid(column=1, row=0, padx=(0,6))
quit_button.grid(column=1, row=1, padx=(0,6))

#################
# Prep
#################


#################
# GUI mainloop()
#################
gui.mainloop()