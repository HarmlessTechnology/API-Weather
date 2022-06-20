# API Weather V0.5
import os
import sys
import tkinter as tk
import webbrowser
import requests
from PIL import Image, ImageTk

# -Specific problem fixes are here-

# remove terminal window fix COMMENT THIS OUT IF DEBUGGING
import win32gui, win32con

#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide , win32con.SW_HIDE)


# cacert error fix by https://stackoverflow.com/questions/46119901/python-requests-cant-find-a-folder-with-a-
# certificate-when-converted-to-exe
def override_where():
    return os.path.abspath("supporting\cacert.pem")


if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    import requests.utils
    import requests.adapters

    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()
# -end fixes-

version_number = 0.5
version_status = "ALPHA"

main = tk.Tk()
main.geometry('1280x720')
main.title("API Weather - Version " + str(version_number) + " " + version_status)
main.iconbitmap("app_icon.ico")

user_font = "Sans Serif MS"
window_color = "black"
border_color = "grey"
text_color = "white"


def format_response(weather_json):
    try:
        location = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temperature = weather_json['main']['temp']
        feels_like = weather_json['main']['feels_like']
        humidity = weather_json['main']['humidity']
        wind = weather_json['wind']['speed']
        result = 'Location: %s \nConditions: %s \nTemperature: %s °F \nFeels like: %s °F \nPercent humidity: %s' \
                 '\nWind Speed: %s MPH' % (location, conditions, temperature, feels_like, humidity, wind)
    except:
        result = 'Error retrieving API data. \nThe location you entered is invalid \nor you have not provided an API ' \
                 'key.'

    return result


def open_weather(location):
    api_file = open('api_key.txt', 'r')
    api_key = api_file.read()
    api_file.close()
    link = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {'APPID': api_key, 'q': location, 'units': 'imperial'}
    response = requests.get(link, params=parameters)
    weather_json = response.json()
    # print(weather_json) # DEBUG - Shows all available information gathered from API
    display['text'] = format_response(response.json())
    image_id = weather_json['weather'][0]['icon']
    open_image(image_id)


def open_image(icon):
    size = int(bottom_frame.winfo_height() * .85)
    image = ImageTk.PhotoImage(Image.open('./image/' + icon + '.png').resize((size, size)))
    weather_image.delete("all")
    weather_image.create_image(0, 0, anchor='nw', image=image)
    weather_image.image = image


def open_api(_clonk):
    def remember_api():
        new_api = api_input.get()
        with open('api_key.txt', 'w') as write_file:
            write_file.write(new_api)
        api_window.destroy()

    api_window = tk.Toplevel(main)
    api_window.geometry("800x100")
    api_window.title("API Weather - Change API key")

    api_background_label = tk.Label(api_window, bg=window_color)
    api_background_label.place(relwidth=1, relheight=1)

    api_frame = tk.Frame(api_window, bg=border_color, bd=5)
    api_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    api_input = tk.Entry(api_frame, font=(user_font, 18), bg="white")
    api_input.place(relx=.1, rely=.1, relwidth=.5, relheight=.8)

    api_button = tk.Button(api_frame, text="Change API Key", font=(user_font, 18), bg=window_color, fg=text_color,
                           command=remember_api)
    api_button.place(relx=.6, rely=.1, relwidth=.3, relheight=.8)


def open_about(_click):
    webbrowser.open("about.txt")


def open_options(_clack):
    options_window = tk.Toplevel(main)
    options_window.geometry("400x400")
    options_window.title("API Weather - options")

    options_background_label = tk.Label(options_window, bg=window_color)
    options_background_label.place(relwidth=1, relheight=1)

    options_frame = tk.Frame(options_window, bg=border_color, bd=5)
    options_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    # open program that will edit api_key variable
    api_button = tk.Button(options_frame, text="Change API key", font=(user_font, 18), bg=window_color,
                           fg=text_color, command=lambda: open_api(True))
    api_button.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.1)

    # display instruction manual
    instruction_button = tk.Button(options_frame, text="Instruction Manual", font=(user_font, 18), bg=window_color,
                                   fg=text_color, command=lambda: webbrowser.open("instructions.txt"))
    instruction_button.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.1)

    # display license information
    license_button = tk.Button(options_frame, text="License Information", font=(user_font, 18), bg=window_color,
                               fg=text_color, command=lambda: webbrowser.open("mylicense.txt"))
    license_button.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.1)


# display background on window
background_image = tk.PhotoImage(file='background.png')
background_label = tk.Label(main, bg=window_color, image=background_image)
background_label.place(relwidth=1, relheight=1)

# provide a frame for the text entry box and button
top_frame = tk.Frame(main, bg=border_color, bd=5)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# make a text entry box
user_input = tk.Entry(top_frame, font=(user_font, 17), bg='white')
user_input.place(relwidth=0.687, relheight=1)

# make a search button
search_button = tk.Button(top_frame, text="Get Current Weather", font=(user_font, 18), bg=window_color, fg=text_color,
                          command=lambda: open_weather(user_input.get()))
search_button.place(relx=0.7, relheight=1, relwidth=0.3)

# provide a border/frame
bottom_frame = tk.Frame(main, bg=border_color, bd=10)
bottom_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

# make a spot for the weather report
display = tk.Label(bottom_frame, font=(user_font, 35), bg=window_color, fg=text_color, justify='left', anchor='nw')
display.place(relwidth=1, relheight=1)

# make a spot for the weather image
weather_image = tk.Canvas(display, bg=window_color, bd=0, highlightthickness=0)
weather_image.place(relx=.6, rely=-.1, relwidth=1, relheight=1)

# make a frame for menu buttons
top_menu = tk.Frame(main, bg=border_color, bd=0)
top_menu.place(relx=0, rely=0, relwidth=0.1, relheight=0.03, anchor='nw')

# make an about button
_click = True
about_button = tk.Button(top_menu, text="About", font=(user_font, 10), bg=window_color, fg=text_color,
                         command=lambda: open_about(_click))
about_button.place(relx=0, rely=0, relwidth=.5, relheight=1, anchor='nw')

# make an options button
_clack = True
options_button = tk.Button(top_menu, text="Options", font=(user_font, 10), bg=window_color, fg=text_color,
                           command=lambda: open_options(_clack))
options_button.place(relx=.5, rely=0, relwidth=.5, relheight=1, anchor='nw')

main.mainloop()
