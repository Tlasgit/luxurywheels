import tkinter as tk  # Provides a Python interface to the Tk GUI toolkit.
from tkinter import *  # Imports all classes, functions, and constants from tkinter module.
from tkinter import ttk, font  # Additional widgets and font handling utilities for Tkinter.
from tkinter import filedialog  # Dialogs for file and directory selection.
from flask import Flask  # Web framework for creating web applications in Python.
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy integration for Flask web applications.
from sqlalchemy import create_engine, extract, desc  # SQL toolkit and Object-Relational Mapper (ORM) for Python.
from sqlalchemy.exc import OperationalError  # Exceptions related to database operations in SQLAlchemy.
from flask_bcrypt import Bcrypt  # Password hashing utilities for Flask web applications.
from PIL import ImageTk, Image  # Python Imaging Library for image manipulation.
import os  # Provides functions to interact with the operating system.
import pandas as pd  # Data manipulation and analysis library.
import tkinter.font as tkFont  # Additional font utilities for Tkinter.
from datetime import datetime, timedelta, timezone  # Date and time utilities.
import re  # Regular expression operations.
import numpy as np  # Numerical computing library for arrays, matrices, and mathematical functions.
from tkcalendar import *  # Calendar widget for Tkinter.
import sys 

print("Python Version: 3.12.0")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = Flask(__name__) # Create the Flask application instance

basedir = os.path.abspath(os.path.dirname(__file__)) # Get the absolute path of the current directory

db_path = os.path.join(basedir, resource_path('luxury.db')) # Construct the path to the database file

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}' # Configure the SQLAlchemy database URI to connect to the SQLite database file

bcrypt = Bcrypt(app) # Initialize Bcrypt extension with the Flask application instance
db = SQLAlchemy(app) # Initialize SQLAlchemy extension with the Flask application instance

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_up_date = db.Column(db.String(50), nullable=False)
    drop_off_date = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(50), nullable=False)
    rental_duration = db.Column(db.Integer, nullable=False)
    cost_per_day = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    id_passport_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_number = db.Column(db.String(20), nullable=False)
    billing_address = db.Column(db.String(200), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    photos = db.Column(db.String(300), nullable=False)
    reservation_state = db.Column(db.String(15), default="In progress")
    date_confirm_completed_renting = db.Column(db.String(15), default="Not Completed")
    code_confirm_completed_renting = db.Column(db.String(20), default="Employee Code")
    date_cancel_reservation = db.Column(db.String(15), default="Not Cancelled")
    code_cancel_reservation = db.Column(db.String(20), default="Employee Code")
    last_update = db.Column(db.String(15), default="No previous update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, pick_up_date, drop_off_date, vehicle_id, rental_duration, cost_per_day, total_cost, full_name, phone_number, 
                email, id_passport_number, date_of_birth, nationality, emergency_contact_name, emergency_contact_number,
                 billing_address, payment_method, photos,  **kwargs):
        self.pick_up_date = pick_up_date
        self.drop_off_date = drop_off_date
        self.vehicle_id = vehicle_id
        self.rental_duration = rental_duration
        self.cost_per_day = cost_per_day
        self.total_cost = total_cost
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.id_passport_number = id_passport_number
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_number = emergency_contact_number
        self.billing_address = billing_address
        self.payment_method = payment_method
        self.photos = photos
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Reservation(id={self.id}, Full Name={self.full_name}, Vehicle={self.vehicle_id})"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_pay = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    f_name = db.Column(db.String(100), nullable=False)
    p_number = db.Column(db.String(50),  nullable=False)
    id_number = db.Column(db.String(50), nullable=False)
    bill_address = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(20), nullable=False)
    photos = db.Column(db.String(300), nullable=False)
    last_update = db.Column(db.String(15), default="No previous update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, total_pay, payment_method, f_name, p_number, id_number, bill_address, vehicle_id, photos, **kwargs):
        self.total_pay = total_pay
        self.payment_method = payment_method
        self.f_name = f_name
        self.p_number = p_number
        self.id_number = id_number
        self.bill_address = bill_address
        self.vehicle_id = vehicle_id
        self.photos = photos
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Payment(id={self.id}, Full Name={self.f_name}, Vehicle={self.vehicle_id})"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(15), nullable=False)
    p_n_indicative = db.Column(db.String(15), nullable=False)
    p_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    id_type = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(50), unique=True, nullable=False)
    credit_number = db.Column(db.String(50), unique=True, nullable=False)
    bill_address = db.Column(db.String(50), nullable=False)
    p_car = db.Column(db.String(50), nullable=False)
    p_moto = db.Column(db.String(50), nullable=False)
    em_name = db.Column(db.String(100), nullable=False)
    m_license = db.Column(db.String(50), nullable=False)
    p_em_indicative = db.Column(db.String(15), nullable=False)
    em_number = db.Column(db.String(50), unique=True, nullable=False)
    photos = db.Column(db.String(300), nullable=False)
    renting = db.Column(db.String(20), default="No")
    code_renting = db.Column(db.String(20), default="Employee Code")
    last_update = db.Column(db.String(15), default="No previous update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, f_name, dob, p_n_indicative, p_number, email, address, nationality, id_type, id_number, 
                credit_number, bill_address, p_car, p_moto, m_license, em_name, p_em_indicative, em_number, photos, **kwargs):
        self.f_name = f_name
        self.dob = dob
        self.p_n_indicative = p_n_indicative
        self.p_number = p_number
        self.email = email
        self.address = address
        self.nationality = nationality
        self.id_type = id_type
        self.id_number = id_number
        self.credit_number = credit_number
        self.bill_address = bill_address
        self.p_car = p_car
        self.p_moto = p_moto
        self.m_license = m_license
        self.em_name = em_name
        self.p_em_indicative = p_em_indicative
        self.em_number = em_number
        self.photos = photos
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Client(id={self.id}, Full Name={self.f_name}, Email={self.email})"

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    segment = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(15), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    wheels = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    fuel = db.Column(db.String(20), nullable=False)
    doors = db.Column(db.Integer, nullable=False, default=0)
    gearbox = db.Column(db.String(20), nullable=False)
    photos = db.Column(db.String(300), nullable=False)
    cc = db.Column(db.String(20), default="Not Relevant")
    availability = db.Column(db.String(20), default="Available")
    rented = db.Column(db.String(20), default="No")
    code_rented = db.Column(db.String(20), default="Employee Code")
    for_inspection = db.Column(db.String(20), default="No")
    code_inspection = db.Column(db.String(20), default="Employee Code")
    for_legalization = db.Column(db.String(20), default="No")
    code_legalization = db.Column(db.String(20), default="Employee Code")
    last_update = db.Column(db.String(15), default="No previous update")
    code_last_update = db.Column(db.String(20), default="Employee Code")
    next_inspection = db.Column(db.String(15), nullable=False)
    next_legalization = db.Column(db.String(15), nullable=False)
    insertion_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    code_insertion = db.Column(db.String(20), default="Employee Code")

    def __init__(self, vehicle_type, category, segment, brand, model, year, license_plate, seats, wheels, doors, 
                color, fuel, gearbox, photos, **kwargs):
        self.vehicle_type = vehicle_type
        self.category = category
        self.segment = segment
        self.brand = brand
        self.model = model
        self.year = year
        self.license_plate = license_plate
        self.seats = seats
        self.wheels = wheels
        self.doors = doors
        self.color = color
        self.fuel = fuel
        self.gearbox = gearbox
        self.photos = photos
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Vehicle(id={self.id}, brand={self.brand}, model={self.model})"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    employee_code = db.Column(db.String(30), unique=True, nullable=False)
    employee_type = db.Column(db.String(30), nullable=False)

    def __init__(self, full_name, username, password, employee_code, employee_type,  **kwargs):
        self.full_name = full_name
        self.username = username
        self.password = password
        self.employee_code = employee_code
        self.employee_type = employee_type
        super().__init__(**kwargs)

    def __repr__(self):
        return f"Employee(id={self.id}, Full Name={self.full_name}, Employee Type={self.employee_type})"

class Lw:
    # Constants for window dimensions and logo path
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 620
    LOGO_PATH = resource_path('resources/lwheels.png')


    def __init__(self, root, flask_app):
        # Initialize the class with root window and Flask application instance
        self.root = root
        self.flask_app = flask_app

        # Activate Flask application context
        self.app_context = flask_app.app_context()
        self.app_context.push()

        # Hide window decorations
        self.root.overrideredirect(True)

        # Load logo image
        self.logo_image = PhotoImage(file=self.LOGO_PATH)

        # Create canvas for displaying logo
        self.canvas = tk.Canvas(self.root, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2, image=self.logo_image,
                                 anchor=tk.CENTER)

        # Configure window background color
        self.root.configure(bg='black')

        # Calculate window position to center it on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_main = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_main = (screen_height - self.WINDOW_HEIGHT) // 2

        # Set window geometry
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{center_x_main}+{center_y_main}")

        # Schedule showing the main window after 3 seconds
        self.root.after(3000, self.show_main_window)


    # Method to bind hover effects to a button
    def bind_hover_effects(self, button):
        button.bind("<Enter>", self.on_button_enter)
        button.bind("<Leave>", self.on_button_leave)

    # Method to handle mouse enter event for buttons
    @staticmethod
    def on_button_enter(event):
        event.widget.config(bg="#205a3d")

    # Method to handle mouse leave event for buttons
    @staticmethod
    def on_button_leave(event):
        event.widget.config(bg="#000000")

    def green_bind_hover_effects(self, button):
        button.bind("<Enter>", self.green_on_button_enter)
        button.bind("<Leave>", self.green_on_button_leave)

    @staticmethod
    def green_on_button_enter(event):
        event.widget.config(bg="#205a3d")

    @staticmethod
    def green_on_button_leave(event):
        event.widget.config(bg="#004d00")

    def red_bind_hover_effects(self, button):
        button.bind("<Enter>", self.red_on_button_enter)
        button.bind("<Leave>", self.red_on_button_leave)

    @staticmethod
    def red_on_button_enter(event):
        event.widget.config(bg="#ff6666")

    @staticmethod
    def red_on_button_leave(event):
        event.widget.config(bg="#800000")

    def orange_bind_hover_effects(self, button):
        button.bind("<Enter>", self.orange_on_button_enter)
        button.bind("<Leave>", self.orange_on_button_leave)

    @staticmethod
    def orange_on_button_enter(event):
        event.widget.config(bg="#FF8C00")

    @staticmethod
    def orange_on_button_leave(event):
        event.widget.config(bg="#C56C00")

    def load_data(self, new_window): # Open a file dialog to select a data file
        data_path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")],
            parent=new_window 
        )
        if data_path:
            print("Selected file:", data_path)
            self.data_path = data_path

            _, file_extension = os.path.splitext(self.data_path) # Get the file extension

            # Read the data file based on its extension
            if file_extension.lower() == '.csv':
                self.df = pd.read_csv(self.data_path)


            elif file_extension.lower() in ('.xlsx', '.xls'):
                self.df = pd.read_excel(self.data_path)

    def load_image(self, new_window): # Open a file dialog to select picture files
        file_paths = filedialog.askopenfilenames(
            title="Select pictures",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
            parent=new_window  
        )
        if file_paths:
            print("Selected files:", file_paths)

            text = file_paths
            cleaned_text = [s.replace("'", "").strip() for s in text] # cleans up the file paths, removes any single quotes

            formatted_text = ", ".join(cleaned_text) # formats them into a comma-separated string
            self.photo_paths = formatted_text

    def create_section_window(self, section):
        new_window = tk.Toplevel(self.root)
        new_window.title(section)
        new_window.iconphoto(True, PhotoImage(file=resource_path('resources/lw.png')))

        # Set the geometry of the new window
        new_window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        # Center the new window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_new_window = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_new_window = (screen_height - self.WINDOW_HEIGHT) // 2
        new_window.geometry(f"+{center_x_new_window}+{center_y_new_window}")

        new_window.resizable(True, True)

        new_window.configure(bg='black')

        self.root.attributes('-disabled', True) # Disable the root window while the new window is open

        # Depending on the section, call the corresponding method to populate the new window
        if section == "Insert Vehicles":
            self.insert_vehicle_section(new_window)
        elif section == "Insert Clients":
            self.insert_clients_section(new_window)
        elif section == "Make Reservations":
            self.make_reservations_section(new_window)
        elif section == "Manage Vehicles":
            self.manage_vehicles_section(new_window)
        elif section == "Manage Clients":
            self.manage_clients_section(new_window)
        elif section == "Manage Reservations":
            self.manage_reservations_section(new_window)
        elif section == "Payment Records":
            self.payments_section(new_window)
        elif section == "Employees Information":
            self.employees_section(new_window)

        def close_new_window():
            self.root.attributes('-disabled', False) # Enable the root window
            new_window.destroy() # Destroy the new window

        # Call the close_new_window function when the user tries to close the new window
        new_window.protocol("WM_DELETE_WINDOW", close_new_window)

    def photo_viewer(self, window, photos, view_mode=None, result_callback=None, updated_photos=None):  # Method that creates a window to view and/or delete photos
        # Check if 'photos' is a string and split it into a list of file paths
        if isinstance(photos, str):
                paths = photos
                print(paths)
                photos = paths.split(', ')

        changed_photos = photos # This variable is used later to track changes made to the list

        # Define a function to load and resize an image
        def load_image(file_path):
            try:
                original_image = Image.open(file_path)
                width, height = original_image.size
                aspect_ratio = width / height
                target_width = 350
                target_height = int(target_width / aspect_ratio)
                resized_image = original_image.resize((target_width, target_height))
                return ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                return None

        # Define a function to update the displayed photo
        def update_photo(image_number):
            nonlocal photo_label, status, next_photo_button, previous_photo_button, delete_photo_button

            photo_label.grid_forget()
            delete_number = image_number - 1

            self.my_img = load_image(photos[image_number - 1])
            if self.my_img:
                photo_label = Label(photo_view_window, image=self.my_img)
                photo_label.grid(row=0, column=0, columnspan=4)
            next_photo_button.config(command=lambda: update_photo(image_number + 1))
            previous_photo_button.config(command=lambda: update_photo(image_number - 1))

            if view_mode != "Edit Mode": # If the view mode is "Edit Mode", the button to delete photos is disabled 
                delete_photo_button.config(state=DISABLED)

            delete_photo_button.config(command=lambda: delete_photo(image_number - 1))

            status.config(text="Image {} of {}".format(image_number, len(photos)))

            if len(photos) == 1 or image_number == 1:
                previous_photo_button.config(state=tk.DISABLED)
            elif image_number > 1:
                previous_photo_button.config(state=tk.NORMAL)
            
            if image_number == len(photos):

                next_photo_button.config(state=tk.DISABLED)
            else:
                next_photo_button.config(state=tk.NORMAL)

        # Define a function to delete a photo
        def delete_photo(delete_number):
            nonlocal photos

            try:
                del photos[delete_number]
                if not photos:
                    on_close(result_callback)
                else:
                    update_photo(1)
            except Exception as e:
                print(f"Error deleting photo: {e}")

        # Define a function to handle the window closure
        def on_close(result_callback):
            print(f"Original: {original_photos}")
            print(f"Changed: {changed_photos}")
            if len(original_photos) != len(', '.join(changed_photos)): # Check if there are any changes in the photos
                def handle_choice(option):
                    if option == "confirm":
                        if len(changed_photos) == 0:
                            updated_photos = "nan"
                            result_callback("confirm", updated_photos)
                            photo_view_window.destroy()
                            print("Confirm changes")
                        else:
                            updated_photos = ', '.join(changed_photos)
                            result_callback("confirm", updated_photos)
                            photo_view_window.destroy()
                            print("Confirm changes")
                    elif option == "cancel":
                        updated_photos = original_photos
                        result_callback("cancel", updated_photos)
                        photo_view_window.destroy()
                        print("Cancel changes")

                changes_warning = "Apply changes to photos?"
                self.pop_warning(photo_view_window, changes_warning, "photochanges", lambda option: handle_choice(option))
                print("There were some changes on photos")

            else:
                updated_photos = original_photos
                result_callback("cancel", updated_photos)
                photo_view_window.destroy()


        photo_view_window = tk.Toplevel(window)
        if view_mode != None:
            photo_view_window.title(f"Photo Viewer ({view_mode})")
        else:
            photo_view_window.title("Photo Viewer")
        photo_view_window.iconphoto(True, PhotoImage(file=resource_path('resources/lw.png')))
        photo_view_window.configure(bg='black')
        photo_view_window.resizable(False, False)
        photo_view_window.grab_set()

        # Create widgets for navigating and displaying photos
        photo_label = Label(photo_view_window)
        status = Label(photo_view_window, text="Image 1 of {}".format(len(photos)), fg="white", bg="black")

        previous_photo_button = tk.Button(photo_view_window, text="Previous Photo", width=15, borderwidth=2,
                                          fg="white", bg="black", state=tk.DISABLED)
        next_photo_button = tk.Button(photo_view_window, text="Next Photo", width=15, borderwidth=2,
                                      fg="white", bg="black")
        delete_photo_button = tk.Button(photo_view_window, text="Delete Photo", width=10, borderwidth=2,
                                        fg="white", bg="#800000")


        previous_photo_button.grid(row=1, column=0, sticky="we")
        self.bind_hover_effects(previous_photo_button)

        next_photo_button.grid(row=1, column=1, sticky="ew")
        self.bind_hover_effects(next_photo_button)

        status.grid(row=1, column=2, sticky="ew")

        delete_photo_button.grid(row=1, column=3, sticky="ew")
        self.red_bind_hover_effects(delete_photo_button)

        update_photo(1)

        original_photos = ', '.join(photos) # Store the original photo paths

        # If the view mode is "Edit Mode" when the user tries to close the window the program will check for any changes in the photos list
        if view_mode == "Edit Mode": 
            photo_view_window.protocol("WM_DELETE_WINDOW", lambda: on_close(result_callback))

            photo_view_window.wait_window(photo_view_window)

    def change_row_color(self, tree, row_index, color):
        item_id = tree.get_children()[row_index]
        tag_name = f"row_{row_index}_tag"
        tree.item(item_id, tags=(tag_name,))
        tree.tag_configure(tag_name, background=color) # Method to change row color of treeview widget

    def toggle_combo_text(self, result, combobox): # Method to change the text color of the combobox widget 
        if result == 0:
            combobox["foreground"] = "darkred"
        else:
            combobox["foreground"] = "white"

    def toggle_entry_colors(self, result, entry): # Method to change the color of the entry boxes
        if result == 0:
            entry.configure(bg="darkred")
        else:
            entry.configure(bg="#313131")

    def toggle_entry_colors_ifnan(self, result, entry): # Method to change the of the entry boxes if the value is 'nan'
        if result == 0:
            entry.configure(bg="darkred")
        else:
            entry.configure(bg="#313131")

    def toggle_button_colors(self, result, button):  # Method to change the buttons color
        if result == 0:
            button.configure(bg='darkred')
        else:
            button.configure(bg="black")

    # Method that creates a window used to display warnings/information or confirm actions
    def pop_warning(self, window, variable, warning, choice_callback=None, photos_callback=None):
        warning_pop = tk.Toplevel(window)
        warning_pop.title("Warning")
        warning_pop.iconphoto(True, tk.PhotoImage(file=resource_path('resources/lw.png')))
        warning_pop.resizable(0,0)
        warning_pop.configure(bg="black")
        warning_pop.grab_set()



        def choice(option):
            warning_pop.destroy()
            if choice_callback:
                choice_callback(option)



        if isinstance(variable, list):

            if warning == "invalidformat":
                invalid_format = f"There was/were {len(variable)} file(s) with Invalid Format or Extension"
                label_invalid_format = tk.Label(warning_pop, text=invalid_format, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_invalid_format.pack(pady=5)


                for index, invalid in enumerate(variable, start=1):
                    invalid_label = tk.Label(warning_pop, text=f"{invalid}\n______", font=("Helvetica", 10),
                                               fg="white", bg="black")
                    invalid_label.pack()

            elif warning == "missingheading":
                missing_heading = f"There was/were {len(variable)} column heading missing"
                label_missing_heading = tk.Label(warning_pop, text=missing_heading, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_missing_heading.pack(pady=5)


                for index, missing in enumerate(variable, start=1):
                    missing_label = tk.Label(warning_pop, text=f"{missing}", font=("Helvetica", 10),
                                               fg="white", bg="black")
                    missing_label.pack()

            elif warning == "unmatchedheading":
                unmatched_heading = f"There was/were {len(variable)} column heading unmatched"
                label_unmatched_heading = tk.Label(warning_pop, text=unmatched_heading, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_unmatched_heading.pack(pady=5)


                for index, unmatched in enumerate(variable, start=1):
                    unmatched_label = tk.Label(warning_pop, text=f"{unmatched}", font=("Helvetica", 10),
                                               fg="white", bg="black")
                    unmatched_label.pack()

            elif warning == "addrecvalidation":
                for error_list in variable:
                    error_text = f"There was/were {len(error_list)-1} error(s) of type: {error_list[0]}"
                    label_info_error = tk.Label(warning_pop, text=error_text, font=("Helvetica", 12),
                                                   fg="white", bg="darkred")
                    label_info_error.pack(pady=5, padx=10)

                    for error in error_list[1:]:
                        error_label = tk.Label(warning_pop, text=error, font=("Helvetica", 10),
                                                   fg="white", bg="black")
                        error_label.pack()

            elif warning == "filenotfound":
                file_not_found_warning = f"There was/were {len(variable)} file(s) not found"
                label_file_not_found = tk.Label(warning_pop, text=file_not_found_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_file_not_found.pack(pady=5)


                for notfound in variable:
                    notfound_label = tk.Label(warning_pop, text=f"{notfound}", font=("Helvetica", 10),
                                               fg="white", bg="black")
                    notfound_label.pack()

            elif warning == "databinvalidadd":
                db_invalid_warning = f"There was/were {len(variable)} record(s) with invalid data"
                label_invalid_record = tk.Label(warning_pop, text=db_invalid_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_invalid_record.pack(pady=5)

                for error_list in variable:
                    for error in error_list:
                        if len(error) > 1:
                            error_index = tk.Label(warning_pop, text=f"----------{error_list[0]}----------", font=("Helvetica", 10),
                                               fg="darkred", bg="black")
                            error_index.pack()

                            error_label = tk.Label(warning_pop, text=f"{error[0]} : {error[1:]}", font=("Helvetica", 10),
                                               fg="white", bg="black")
                            error_label.pack(padx=20)

            elif warning == "databvalidadd":

                def grab_photo_path(e):
                    global photos
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        verify_photo_button.config(state=NORMAL)
                        x = treeview.index(selected_items[0])
                        paths = treeview.item(x, "values")[-1]
                        photos = paths.split(',')
                        print(photos)


                warning_pop.maxsize(600,500)
                db_valid_warning = f"Please confirm the information of the following {len(variable)} record(s) to add to the Database"
                label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_valid_record.pack(pady=10)

                treeview_confirm_frame = tk.Frame(warning_pop)
                treeview_confirm_frame.pack()
                treeview_confirm_frame.configure(bg="black")

                treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                treeScrolly.pack(side="right", fill="y")

                treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                treeScrollx.pack(side="bottom", fill="x")

                treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                        yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                treeScrolly.config(command=treeview.yview)
                treeScrollx.config(command=treeview.xview)

                if 'vehicle type' in [column.lower() for column in self.df.columns]:
                    vehicle_headings = ['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate',
                                        'Seats', 'Doors', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Wheels',
                                         'Vehicle Photos']
                    treeview["column"] = vehicle_headings

                elif 'full name' in [column.lower() for column in self.df.columns]:
                    client_headings = ['Full Name', 'Date of Birth', 'Phone Number Indicative', 'Phone Number', 'Email', 'Address', 'Nationality', 'Identification Type', 'ID/Passport Number',
                                    'Credit Card Number', 'Billing Address', 'Preferred Car Type', 'Preferred Motorcycle Type', 'Motorcycle License', 'Emergency Contact Name', 'Emergency Contact Indicative', 'Emergency Contact Number',
                                     'Client ID Photos']
                    treeview["column"] = client_headings

                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")

                treeview.pack(expand=True, fill="both")

                cnt = 0
                for index in variable:
                    if 'vehicle type' in [column.lower() for column in self.df.columns]:
                        vehicle = [self.df.at[index, head] for head in vehicle_headings]
                        treeview.insert(parent='', index='end', iid=cnt, text="", values=(vehicle))
                        cnt += 1
                    elif 'full name' in [column.lower() for column in self.df.columns]:
                        client = [self.df.at[index, head] for head in client_headings]
                        treeview.insert(parent='', index='end', iid=cnt, text="", values=(client))
                        cnt += 1

                for col in treeview["columns"][:-1]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                    
                    max_width = max(
                        tkFont.Font().measure(str(treeview.set(item, col)))
                        for item in treeview.get_children("")
                    )
                    
                    column_width = max(heading_width, max_width) + 20 
                    
                    treeview.column(col, width=column_width, minwidth=heading_width)

                last_col = treeview["columns"][-1]
                treeview.column(last_col, width=100)

                verify_photo_frame = tk.Frame(warning_pop)
                verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                verify_photo_frame.configure(bg="black")

                verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="white",
                                               bg="black", width=20, state=DISABLED, command=lambda: self.photo_viewer(warning_pop, photos, "View Mode"))
                verify_photo_button.pack(side="right", padx=5)
                self.bind_hover_effects(verify_photo_button) 

                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=(5,15))
                confirm_cancel_frame.configure(bg="black")

                confirm_record_validation_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=10, command=lambda: choice("confirm"))
                confirm_record_validation_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_record_validation_button) 

                cancel_record_validation_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=10, command=lambda: choice("cancel"))
                cancel_record_validation_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_record_validation_button)

                treeview.bind("<ButtonRelease-1>", grab_photo_path)

            elif warning == "platealreadyindb":
                plate_already_in_db_warning = f"There was/were {len(variable)} record(s) with a\nlicense plate that already exists in the Database"
                label_plate_already_in_db = tk.Label(warning_pop, text=plate_already_in_db_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_plate_already_in_db.pack(ipadx=10)

                for plate in variable:
                    plate_label = tk.Label(warning_pop, text=re.sub(r'[^\w\s]', '', plate), font=("Helvetica", 10),
                                               fg="white", bg="black")
                    plate_label.pack(pady=(15,5))

            elif warning == "treerepeatedvalues":
                repeated_tree_values_warning = f"There was/were {len(variable)} column(s)\nwith repeated values that must be unique"
                label_repeated_tree_values = tk.Label(warning_pop, text=repeated_tree_values_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_repeated_tree_values.pack(ipadx=10)

                for warning in variable:
                    print(warning)
                    warning_column_label = tk.Label(warning_pop, text=re.sub(r'[^\w\s]', '', warning[2]), font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_column_label.pack(pady=(15,5))

            elif warning == "valuealreadyindb":
                repeated_db_values_warning = f"There was/were {len(variable)} item(s) with values that\nalready exist on the Database and must be unique"
                label_repeated_db_values = tk.Label(warning_pop, text=repeated_db_values_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_repeated_db_values.pack(ipadx=10)

                warning_exist_list = []
                for warning in variable:
                    for value in warning:
                        if value in warning_exist_list:
                            pass
                        else:
                            warning_exist_list.append(value)

                for warning in warning_exist_list:
                    warning_column_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_column_label.pack(pady=(10,5))

            elif warning == "multipledataalreadyindb":
                repeated_multiple_warning = f"There was/were {len(variable)} column(s) with values that\nalready exist on the Database and must be unique"
                label_repeated_multiple_values = tk.Label(warning_pop, text=repeated_multiple_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_multiple_values.pack(ipadx=10)

                for warning in variable:
                    warning_column_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_column_label.pack(pady=(15,5))

            elif warning == "wrongdatetextformat":
                wrong_format_warning = f"There was/were {len(variable)} date(s) with wrong date format\nExpected format: yyyy-mm-dd"
                label_wrong_format = tk.Label(warning_pop, text=wrong_format_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_wrong_format.pack(ipadx=10)

                for warning in variable:
                    warning_column_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_column_label.pack(pady=(15,5))

            elif warning == "manyclientorvehiclenotindb":
                not_in_db_warning = f"There was/were {variable[0]} record(s) with items not found in the Database"
                label_not_in_db_warning = tk.Label(warning_pop, text=not_in_db_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_not_in_db_warning.pack(ipadx=10)


                warning_label = tk.Label(warning_pop, text="Client and/or Vehicle not found in the Database", font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(15,5))

            elif warning == "dbtotree":
                database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']

                engine = create_engine(database_uri)

                df = pd.read_sql_table(variable[0], con=engine)

                engine.dispose()

                print(df)

                if df.empty:
                    warning = "The selected Database Table is empty."

                    empty_table_warning = f"Error while trying to fetch information from the Database"
                    label_empty_table_warning = tk.Label(warning_pop, text=empty_table_warning, font=("Helvetica", 12),
                                                   fg="white", bg="darkred")
                    label_empty_table_warning.pack(ipadx=10)
                    
                    empty_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),

                                                fg="white", bg="black")
                    empty_label.pack(padx=10)
                else:

                    def confirm_selected():
                        selected_items = treeview.selection()
                        x = treeview.index(selected_items[0])
                        variable[1].delete(0, tk.END)
                        if variable[0] == "client":
                            variable[1].insert(0, str(df.at[x, 'id_number']))
                        elif variable[0] == "vehicle":
                            variable[1].insert(0, str(df.at[x, 'license_plate']))
                        variable[2]()
                        warning_pop.destroy()

                    def cancel_selected():
                        warning_pop.destroy()

                    warning_pop.maxsize(600,500)

                    db_valid_warning = f"Please select the {variable[0]}"
                    label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                                   fg="white", bg="darkgreen")
                    label_valid_record.pack(pady=10)

                    treeview_confirm_frame = tk.Frame(warning_pop)
                    treeview_confirm_frame.pack()
                    treeview_confirm_frame.configure(bg="black")

                    treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    column_list = df.columns.tolist()

                    if 'vehicle_type' in column_list:
                        df['year'] = df['year'].apply(convert_to_datetime)
                        df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)
                        columns_to_int = ['doors', 'wheels', 'seats']
                        photo_col = "photos"
                    if 'f_name' in column_list:
                        df['dob'] = df['dob'].apply(convert_to_datetime)
                        df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)
                        columns_to_int = []
                        photo_col = "photos"

                    def grab_photo_path(e):
                        global photos
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            verify_photo_button.config(state=NORMAL)
                            paths = df.at[x, photo_col]
                            photos = paths.split(',')

                            if 'vehicle_type' in column_list:
                                if str(df.at[x, 'availability']) == 'Available':
                                    confirm_record_selection_button.config(state=NORMAL)
                                else:
                                    confirm_record_selection_button.config(state=DISABLED)
                            else:
                                confirm_record_selection_button.config(state=NORMAL)

                    treeview["column"] = column_list
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")

                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass               
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                        
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                        
                        column_width = max(heading_width, max_width) + 20 
                        
                        treeview.column(col, width=column_width, minwidth=heading_width)


                    treeview.column(photo_col, width=120, minwidth=120)

                    treeview.pack(expand=True, fill="both")

                    verify_photo_frame = tk.Frame(warning_pop)
                    verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                    verify_photo_frame.configure(bg="black")

                    verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="white",
                                                   bg="black", width=20, state=DISABLED, command=lambda: self.photo_viewer(warning_pop, photos, "View Mode"))
                    verify_photo_button.pack(side="right", padx=5)
                    self.bind_hover_effects(verify_photo_button) 

                    confirm_cancel_frame = tk.Frame(warning_pop)
                    confirm_cancel_frame.pack(pady=(5,15))
                    confirm_cancel_frame.configure(bg="black")

                    confirm_record_selection_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                                   bg="darkgreen", width=10, state=DISABLED, command=confirm_selected)
                    confirm_record_selection_button.grid(row=0, column=0, padx=10)
                    self.green_bind_hover_effects(confirm_record_selection_button) 

                    cancel_record_selection_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                                   bg="darkred", width=10, command=lambda: choice("cancel"))
                    cancel_record_selection_button.grid(row=0, column=1, padx=10)
                    self.red_bind_hover_effects(cancel_record_selection_button)

                    treeview.bind("<ButtonRelease-1>", grab_photo_path)

            elif warning == "somevehiclenotavailable":
                unavailable_warning = f"{len(variable)} record(s) failed to add to the Database due to:"
                label_unavailable_warning = tk.Label(warning_pop, text=unavailable_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_unavailable_warning.pack(ipadx=10)


                warning_label = tk.Label(warning_pop, text="Vehicle Unavailable", font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(10,5))

            elif warning == "vehicledateexceeded":
                exceeded_warning = f"There was/were {len(variable)} warning(s) of exceeded Legalization/Inspection date"
                label_exceeded_warning = tk.Label(warning_pop, text=exceeded_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_exceeded_warning.pack(ipadx=10)

                for warning in variable:
                    warning_column_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_column_label.pack(pady=(10,5))

            elif warning == "cannotdelete":
                can_not_delete_warning = f"There is/are {len(variable)} vehicle(s) that can't be deleted due to being currently rented"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_label.pack(pady=(10,5))

            elif warning == "dropdateexceeds":
                date_exceeded_warning = f"{len(variable)} record(s) failed to add to the Database due to:"
                label_date_exceeded_warning = tk.Label(warning_pop, text=date_exceeded_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_date_exceeded_warning.pack(ipadx=10)


                warning_label = tk.Label(warning_pop, text="Drop-off date exceeds Vehicle next inspection and/or next_legalization date", font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(10,5))

            elif warning == "showdbiteminfo":
                if variable[0] == "vehicle":
                    if variable[3] == "current":
                        reservation = Reservation.query.filter_by(vehicle_id=variable[2], reservation_state="In progress").first()
                        if variable[1] == "client":
                            
                            client = Client.query.filter_by(id_number=reservation.id_passport_number).first()

                            data = {'Full Name':client.f_name,'Date of Birth':client.dob, "Phone Number Indicative": str(client.p_n_indicative),'Phone Number':str(client.p_number),'Email':client.email,
                            'Address':client.address,'Nationality':client.nationality, 'Identification Type':client.id_type,'Identification Number':str(client.id_number),'Credit Number':str(client.credit_number),
                            'Billing Address':client.bill_address,'Preferred Car Type':client.p_car,'Preferred Motorcycle Type':client.p_moto, 'Motorcycle License': client.m_license, 'Emergency Contact Name':client.em_name, 
                            'Contact Number Indicative':str(client.p_em_indicative), 'Emergency Contact Number':str(client.em_number),'Currently Renting':client.renting,'Client ID Photos':client.photos }

                        elif variable[1] == "reservation":
                            data = {'Pick-up Date':reservation.pick_up_date,'Drop-off Date':reservation.drop_off_date,'Vehicle License Plate':reservation.vehicle_id,
                            'Rental Duration':reservation.rental_duration,'Cost Per Day':reservation.cost_per_day,'Total Cost':reservation.total_cost,'Full Name':reservation.full_name,
                            'Phone Number':reservation.phone_number,'Email':reservation.email,'ID/Passport Number':reservation.id_passport_number,'Date of Birth':reservation.date_of_birth,
                            'Nationality':reservation.nationality,'Emergency Contact Name':reservation.emergency_contact_name,'Emergency Contact Number':reservation.emergency_contact_number,
                            'Billing Address':reservation.billing_address,'Payment-Method':reservation.payment_method,'Reservation State':reservation.reservation_state,'Receipt Photos':reservation.photos}

                        df = pd.DataFrame([data])

                    else:
                        reservations = Reservation.query.filter_by(vehicle_id=variable[2]).all()

                        if variable[1] == "client":
                            df = pd.DataFrame(columns=['Full Name','Date of Birth', 'Phone Number Indicative','Phone Number','Email','Address','Nationality', 'Identification Type','Identification Number','Credit Number',
                            'Billing Address','Preferred Car Type','Preferred Motorcycle Type', 'Motorcycle License', 'Emergency Contact Name','Contact Number Indicative', 'Emergency Contact Number','Currently Renting','Client ID Photos'])

                            for reservation in reservations:
                                client = Client.query.filter_by(id_number=reservation.id_passport_number).first()

                                new_df_record = {
                                    'Full Name':client.f_name,
                                    'Date of Birth':client.dob,
                                    'Phone Number Indicative': str(client.p_n_indicative),
                                    'Phone Number':str(client.p_number),
                                    'Email':client.email,
                                    'Address':client.address,
                                    'Nationality':client.nationality,
                                    'Identification Type':client.id_type,
                                    'Identification Number':str(client.id_number),
                                    'Credit Number':str(client.credit_number),
                                    'Billing Address':client.bill_address,
                                    'Preferred Car Type':client.p_car,
                                    'Preferred Motorcycle Type':client.p_moto,
                                    'Motorcycle License': client.m_license,
                                    'Emergency Contact Name':client.em_name, 
                                    'Contact Number Indicative':str(client.p_em_indicative),
                                    'Emergency Contact Number':str(client.em_number),
                                    'Currently Renting':client.renting,
                                    'Client ID Photos':client.photos
                                }

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)

                        elif variable[1] == "reservation":
                            df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle License Plate', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                          'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                          'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Reservation State','Receipt Photos'])

                            for reservation in reservations:                                                                    
                                    new_df_record = {
                                        'Pick-up Date': reservation.pick_up_date,
                                        'Drop-off Date': reservation.drop_off_date,
                                        'Vehicle License Plate': reservation.vehicle_id, 
                                        'Rental Duration': reservation.rental_duration, 
                                        'Cost Per Day': reservation.cost_per_day, 
                                        'Total Cost': reservation.total_cost,
                                        'Full Name': reservation.full_name, 
                                        'Phone Number': reservation.phone_number, 
                                        'Email': reservation.email, 
                                        'ID/Passport Number': reservation.id_passport_number,
                                        'Date of Birth': reservation.date_of_birth, 
                                        'Nationality': reservation.nationality, 
                                        'Emergency Contact Name': reservation.emergency_contact_name,
                                        'Emergency Contact Number': reservation.emergency_contact_number, 
                                        'Billing Address': reservation.billing_address, 
                                        'Payment-Method': reservation.payment_method,
                                        'Reservation State':reservation.reservation_state,
                                        'Receipt Photos': reservation.photos
                                    }

                                    new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                    df = pd.concat([df, new_df_record], ignore_index=True)

                elif variable[0] == "client":

                    if variable[3] == "current":
                        reservations = Reservation.query.filter_by(id_passport_number=variable[2], reservation_state="In progress").all()
                        if variable[1] == "vehicle":

                            df = pd.DataFrame(columns=['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate', 'Number of Seats',
                                'Number of Wheels', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Doors', 'Vehicle Photos'])

                            for reservation in reservations:

                                vehicle = Vehicle.query.filter_by(license_plate=reservation.vehicle_id).first()

                                new_df_record = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                                'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                                'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)


                        elif variable[1] == "reservation":
                            print("got to reservation")

                            df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle License Plate', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                          'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                          'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Reservation State','Receipt Photos'])

                            for reservation in reservations:                                                                    
                                    new_df_record = {
                                        'Pick-up Date': reservation.pick_up_date,
                                        'Drop-off Date': reservation.drop_off_date,
                                        'Vehicle License Plate': reservation.vehicle_id, 
                                        'Rental Duration': reservation.rental_duration, 
                                        'Cost Per Day': reservation.cost_per_day, 
                                        'Total Cost': reservation.total_cost,
                                        'Full Name': reservation.full_name, 
                                        'Phone Number': reservation.phone_number, 
                                        'Email': reservation.email, 
                                        'ID/Passport Number': reservation.id_passport_number,
                                        'Date of Birth': reservation.date_of_birth, 
                                        'Nationality': reservation.nationality, 
                                        'Emergency Contact Name': reservation.emergency_contact_name,
                                        'Emergency Contact Number': reservation.emergency_contact_number, 
                                        'Billing Address': reservation.billing_address, 
                                        'Payment-Method': reservation.payment_method,
                                        'Reservation State':reservation.reservation_state,
                                        'Receipt Photos': reservation.photos
                                    }

                                    new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                    df = pd.concat([df, new_df_record], ignore_index=True)

                    else:
                        reservations = Reservation.query.filter_by(id_passport_number=variable[2]).all()
                        if variable[1] == "vehicle":

                            df = pd.DataFrame(columns=['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate', 'Number of Seats',
                                'Number of Wheels', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Doors', 'Vehicle Photos'])

                            for reservation in reservations:

                                vehicle = Vehicle.query.filter_by(license_plate=reservation.vehicle_id).first()

                                new_df_record = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                                'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                                'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                                new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                df = pd.concat([df, new_df_record], ignore_index=True)


                        elif variable[1] == "reservation":

                            df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle License Plate', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                          'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                          'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Reservation State','Receipt Photos'])

                            for reservation in reservations:                                                                    
                                    new_df_record = {
                                        'Pick-up Date': reservation.pick_up_date,
                                        'Drop-off Date': reservation.drop_off_date,
                                        'Vehicle License Plate': reservation.vehicle_id, 
                                        'Rental Duration': reservation.rental_duration, 
                                        'Cost Per Day': reservation.cost_per_day, 
                                        'Total Cost': reservation.total_cost,
                                        'Full Name': reservation.full_name, 
                                        'Phone Number': reservation.phone_number, 
                                        'Email': reservation.email, 
                                        'ID/Passport Number': reservation.id_passport_number,
                                        'Date of Birth': reservation.date_of_birth, 
                                        'Nationality': reservation.nationality, 
                                        'Emergency Contact Name': reservation.emergency_contact_name,
                                        'Emergency Contact Number': reservation.emergency_contact_number, 
                                        'Billing Address': reservation.billing_address, 
                                        'Payment-Method': reservation.payment_method,
                                        'Reservation State':reservation.reservation_state,
                                        'Receipt Photos': reservation.photos
                                    }

                                    new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                    df = pd.concat([df, new_df_record], ignore_index=True)

                elif variable[0] == "reservation":

                    if variable[1] == "vehicle":

                        reservation = Reservation.query.filter_by(vehicle_id=variable[2]).first()
                        vehicle = Vehicle.query.filter_by(license_plate=reservation.vehicle_id).first()


                        data = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                        'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                        'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                        df = pd.DataFrame([data])
                        
        
                    elif variable[1] == "client":

                        reservation = Reservation.query.filter_by(id_passport_number=variable[2]).first()
                        
                        client = Client.query.filter_by(id_number=reservation.id_passport_number).first()

                        data = {'Full Name':client.f_name,'Date of Birth':client.dob, "Phone Number Indicative": str(client.p_n_indicative),'Phone Number':str(client.p_number),'Email':client.email,
                        'Address':client.address,'Nationality':client.nationality, 'Identification Type':client.id_type,'Identification Number':str(client.id_number),'Credit Number':str(client.credit_number),
                        'Billing Address':client.bill_address,'Preferred Car Type':client.p_car,'Preferred Motorcycle Type':client.p_moto, 'Motorcycle License': client.m_license, 'Emergency Contact Name':client.em_name, 
                        'Contact Number Indicative':str(client.p_em_indicative), 'Emergency Contact Number':str(client.em_number),'Currently Renting':client.renting,'Client ID Photos':client.photos }

                        df = pd.DataFrame([data])

                elif variable[0] == "showcancelcompletedinprogress":

                    reservations = Reservation.query.filter_by(reservation_state=variable[1]).all()

                    df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle License Plate', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                  'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                  'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Receipt Photos'])

                    for reservation in reservations:                                                                    
                            new_df_record = {
                                'Pick-up Date': reservation.pick_up_date,
                                'Drop-off Date': reservation.drop_off_date,
                                'Vehicle License Plate': reservation.vehicle_id, 
                                'Rental Duration': reservation.rental_duration, 
                                'Cost Per Day': reservation.cost_per_day, 
                                'Total Cost': reservation.total_cost,
                                'Full Name': reservation.full_name, 
                                'Phone Number': reservation.phone_number, 
                                'Email': reservation.email, 
                                'ID/Passport Number': reservation.id_passport_number,
                                'Date of Birth': reservation.date_of_birth, 
                                'Nationality': reservation.nationality, 
                                'Emergency Contact Name': reservation.emergency_contact_name,
                                'Emergency Contact Number': reservation.emergency_contact_number, 
                                'Billing Address': reservation.billing_address, 
                                'Payment-Method': reservation.payment_method,
                                'Receipt Photos': reservation.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif variable[0] == "reservationinfo":

                    if variable[1] == "reservation":

                        reservation = Reservation.query.filter_by(id = variable[2]).first()

                        data = {'Pick-up Date':reservation.pick_up_date,'Drop-off Date':reservation.drop_off_date,'Vehicle License Plate':reservation.vehicle_id,
                        'Rental Duration':reservation.rental_duration,'Cost Per Day':reservation.cost_per_day,'Total Cost':reservation.total_cost,'Full Name':reservation.full_name,
                        'Phone Number':reservation.phone_number,'Email':reservation.email,'ID/Passport Number':reservation.id_passport_number,'Date of Birth':reservation.date_of_birth,
                        'Nationality':reservation.nationality,'Emergency Contact Name':reservation.emergency_contact_name,'Emergency Contact Number':reservation.emergency_contact_number,
                        'Billing Address':reservation.billing_address,'Payment-Method':reservation.payment_method,'Reservation State':reservation.reservation_state,'Receipt Photos':reservation.photos}

                        df = pd.DataFrame([data])

                    elif variable[1] == "client":
                        
                        client = Client.query.filter_by(id_number=variable[2]).first()

                        data = {'Full Name':client.f_name,'Date of Birth':client.dob, "Phone Number Indicative": str(client.p_n_indicative),'Phone Number':str(client.p_number),'Email':client.email,
                        'Address':client.address,'Nationality':client.nationality, 'Identification Type':client.id_type,'Identification Number':str(client.id_number),'Credit Number':str(client.credit_number),
                        'Billing Address':client.bill_address,'Preferred Car Type':client.p_car,'Preferred Motorcycle Type':client.p_moto, 'Motorcycle License': client.m_license, 'Emergency Contact Name':client.em_name, 
                        'Contact Number Indicative':str(client.p_em_indicative), 'Emergency Contact Number':str(client.em_number),'Currently Renting':client.renting,'Client ID Photos':client.photos }

                        df = pd.DataFrame([data])


                    elif variable[1] == "vehicle":

                        vehicle = Vehicle.query.filter_by(license_plate=variable[2]).first()


                        data = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                        'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                        'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                        df = pd.DataFrame([data])





                print(df)

                warning_pop.maxsize(600,500)

                db_valid_warning = "Information Table"
                label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_valid_record.pack(pady=10)

                treeview_confirm_frame = tk.Frame(warning_pop)
                treeview_confirm_frame.pack()
                treeview_confirm_frame.configure(bg="black")


                # Create vertical scrollbar
                treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                treeScrolly.pack(side="right", fill="y")

                # Create horizontal scrollbar
                treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                treeScrollx.pack(side="bottom", fill="x")

                treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                        yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)


                treeScrolly.config(command=treeview.yview)
                treeScrollx.config(command=treeview.xview)

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                column_list = df.columns.tolist()

                if 'Vehicle Type' in column_list:
                    df['Year'] = df['Year'].apply(convert_to_datetime)
                    columns_to_int = ['Number of Doors', 'Number of Wheels', 'Number of Seats']
                    photo_col = "Vehicle Photos"
                elif 'Client ID Photos' in column_list:
                    df['Date of Birth'] = df['Date of Birth'].apply(convert_to_datetime)
                    columns_to_int = []
                    photo_col = "Client ID Photos"
                elif 'Pick-up Date' in column_list:
                    df['Pick-up Date'] = df['Pick-up Date'].apply(convert_to_datetime)
                    columns_to_int = ['Rental Duration', 'Cost Per Day', 'Total Cost']
                    photo_col = "Receipt Photos"


                def grab_photo_path(e):
                    global photos
                    selected_items = treeview.selection()
                    if len(selected_items) > 0:
                        x = treeview.index(selected_items[0])
                        verify_photo_button.config(state=NORMAL)
                        paths = df.at[x, photo_col]
                        photos = paths.split(',')



                treeview["column"] = column_list
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")

                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass             
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                    
                    max_width = max(
                        tkFont.Font().measure(str(treeview.set(item, col)))
                        for item in treeview.get_children("")
                    )
                    
                    column_width = max(heading_width, max_width) + 20

                    treeview.column(col, width=column_width, minwidth=heading_width)

                treeview.column(photo_col, width=120, minwidth=120)

                treeview.pack(expand=True, fill="both")

                verify_photo_frame = tk.Frame(warning_pop)
                verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                verify_photo_frame.configure(bg="black")

                verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="white",
                                               bg="black", width=20, state=DISABLED, command=lambda: self.photo_viewer(warning_pop, photos, "View Mode"))
                verify_photo_button.pack(side="right", padx=5)
                self.bind_hover_effects(verify_photo_button) 

                treeview.bind("<ButtonRelease-1>", grab_photo_path)

            elif warning == "notvalidlicenseclass":
                can_not_delete_warning = f"There was/were {len(variable)} reservations that failed due to\nthe client motorcyle license not being compatible with the vehicle."
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_label.pack(pady=(10,5))

            elif warning == "cannotdeleteclient":
                can_not_delete_warning = f"There is/are {len(variable)} client(s) that can't be deleted due to being currently renting"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_label.pack(pady=(10,5))

            elif warning == "updateexistingclientinfo":
                exists_warning = f"Error while trying to update record the following\nvalues already exists in the Database and must be unique"
                label_exists_warning = tk.Label(warning_pop, text=exists_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_exists_warning.pack(ipadx=10)

                for exists in variable:
                    exists_label = tk.Label(warning_pop, text=exists, font=("Helvetica", 10),
                        fg="white", bg="black")
                    exists_label.pack(pady=5)

            elif warning == "cannotdeletereservation":
                can_not_delete_warning = f"There is/are {len(variable)} reservation(s) that can't be deleted due to being currently in progress"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_label.pack(pady=(10,5))

            elif warning == "managerexpirewarning":
                can_not_delete_warning = f"There is/are {len(variable)} vehicle(s) with legalization and/or inspection expiring within 5 or less days"
                label_can_not_delete_warning = tk.Label(warning_pop, text=can_not_delete_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_can_not_delete_warning.pack(ipadx=10)

                for warning in variable:
                    warning_label = tk.Label(warning_pop, text=warning, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    warning_label.pack(pady=(10,5))
            
        elif isinstance(variable, tuple):
            if warning == "missingheadunmatched":
                missing_heading = f"There was/were {len(variable[0])} column heading missing"
                label_missing_heading = tk.Label(warning_pop, text=missing_heading, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_missing_heading.pack(ipadx=10)
                

                for index, missing in enumerate(variable[0], start=1):
                    missing_head_label = tk.Label(warning_pop, text=missing, font=("Helvetica", 10),
                                               fg="white", bg="black")
                    missing_head_label.pack()

                unmatched_heading = f"There was/were {len(variable[1])} column heading unmatched"
                label_unmatched_heading = tk.Label(warning_pop, text=unmatched_heading, font=("Helvetica", 12),
                    fg="white", bg="darkred")
                label_unmatched_heading.pack(pady=(20,5), padx=10)

                for index, unmatched in enumerate(variable[1], start=1):
                    unmatched_head_label = tk.Label(warning_pop, text=unmatched, font=("Helvetica", 10),
                        fg="white", bg="black")
                    unmatched_head_label.pack()

            elif warning == "not_unique_license_plate":
                license_plate_warning = f"There was/were {len(variable[0])} vehicles with repeated license plate"
                label_license_plate_warning = tk.Label(warning_pop, text=license_plate_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_license_plate_warning.pack(ipadx=10)

                for repeated in variable[1]:
                    repeated_license_label = tk.Label(warning_pop, text=repeated, font=("Helvetica", 10),
                        fg="white", bg="black")
                    repeated_license_label.pack(pady=5)

        elif isinstance(variable, str):
            if warning == "nanselectedphoto":
                nan_selected_photo_warning = "The photos column of the selected item is empty"
                label_nan_selected_photo_warning = tk.Label(warning_pop, text=nan_selected_photo_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_nan_selected_photo_warning.pack(pady=5, padx=10)
                
                empty_selected_photos_label = tk.Label(warning_pop, text=f"Index: {variable}", font=("Helvetica", 10),
                                            fg="white", bg="black")
                empty_selected_photos_label.pack()

            elif warning == "noselectedtoupdate":
                no_selected_update_warning = "Error while trying to update record"
                label_no_selected_update_warning = tk.Label(warning_pop, text=no_selected_update_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_update_warning.pack(pady=5, padx=10)
                
                no_selected_update_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                            fg="white", bg="black")
                no_selected_update_label.pack()

            elif warning == "noselectedtoseephotos":
                no_selected_viewphotos_warning = "Error while trying to see record photos"
                label_no_selected_viewphotos_warning = tk.Label(warning_pop, text=no_selected_viewphotos_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_viewphotos_warning.pack(pady=5, padx=10)
                
                no_selected_viewphotos_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                            fg="white", bg="black")
                no_selected_viewphotos_label.pack()

            elif warning == "noselectedtoremove":
                no_selected_remove_warning = "Error while trying to remove record"
                label_no_selected_remove_warning = tk.Label(warning_pop, text=no_selected_remove_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_remove_warning.pack(pady=5, padx=10)
                
                no_selected_remove_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                no_selected_remove_label.pack()

            elif warning == "noselectedtoadddatabase":
                no_selected_add_database_warning = "Error while trying to add record(s) to the Database"
                label_no_selected_add_database_warning = tk.Label(warning_pop, text=no_selected_remove_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_no_selected_add_database_warning.pack(pady=5, padx=10)
                
                no_selected_add_database_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                no_selected_add_database_label.pack()

            elif warning == "platealreadyindatab":
                plate_already_in_db_warning = "Error while trying to add record to the Database\nthe following license plate already exists in the Database"
                label_plate_already_in_db_warning = tk.Label(warning_pop, text=plate_already_in_db_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_plate_already_in_db_warning.pack(ipadx=10)
                
                plate_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                plate_label.pack(padx=10)
 
            elif warning == "photochanges":
                label_photo_changes_warning = tk.Label(warning_pop, text=variable, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_photo_changes_warning.pack(ipadx=30, ipady=5)
                
                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=15)
                confirm_cancel_frame.configure(bg="black")

                confirm_photo_changes_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=6, command=lambda: choice("confirm"))
                confirm_photo_changes_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_photo_changes_button) 

                cancel_photo_changes_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=6, command=lambda: choice("cancel"))
                cancel_photo_changes_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_photo_changes_button)

            elif warning == "wrongdatetextformat":
                date_wrong_format_warning = "Date with wrong text format\nexpected: 'yyyy mm dd'"
                label_date_wrong_format_warning = tk.Label(warning_pop, text=date_wrong_format_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_date_wrong_format_warning.pack(ipadx=10)
                
                date_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                date_label.pack(padx=10)

            elif warning == "vehiclenotavailable":
                not_available_warning = "Error while trying to add record"
                label_not_available_warning = tk.Label(warning_pop, text=not_available_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_not_available_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "wrongemployeecode":
                wrong_code_warning = "Error while validating employee code"
                label_wrong_code_warning = tk.Label(warning_pop, text=wrong_code_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_wrong_code_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "cannotdeletealldb":
                delete_warning = "Error while trying to delete record(s)"
                label_delete_warning = tk.Label(warning_pop, text=delete_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_delete_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "cantupdaterented":
                update_warning = "Error while trying to update record"
                label_update_warning = tk.Label(warning_pop, text=update_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_update_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "updateexistingplate":
                plate_already_in_db_warning = "Error while trying to update record\nthe following license plate already exists in the Database"
                label_plate_already_in_db_warning = tk.Label(warning_pop, text=plate_already_in_db_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_plate_already_in_db_warning.pack(ipadx=10)
                
                plate_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                plate_label.pack(padx=10)

            elif warning == "dropdateexceeds":
                drop_exceeds_warning = "Error while trying to add record to the Database"
                label_drop_exceeds_warning = tk.Label(warning_pop, text=drop_exceeds_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_drop_exceeds_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "ccnotvalidlicense":
                cc_warning = "Error while trying to add reservation\nThe client doesn't have a motorcycle license or the vehicle CC it's above license class"
                label_cc_warning = tk.Label(warning_pop, text=cc_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cc_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "cantupdateinprogress":
                cant_update_warning = "Error while trying to update record"
                label_cant_update_warning = tk.Label(warning_pop, text=cant_update_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_update_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "erroraddemploye":
                cant_add_warning = "Error while trying to add new employee"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "employeecodeexists":
                cant_add_warning = "Error while trying to add new employee"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "databaselocked":
                cant_add_warning = "Error due to Database being locked"
                label_cant_add_warning = tk.Label(warning_pop, text=cant_add_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkred")
                label_cant_add_warning.pack(ipadx=10)
                
                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),

                                            fg="white", bg="black")
                warning_label.pack(padx=10)

            elif warning == "clientorvehiclenotindb":
                not_in_db_warning = "Error while trying to add record to the Database"
                label_not_in_db_warning = tk.Label(warning_pop, text=not_in_db_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_not_in_db_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(15,5))

            elif warning == "cantlegalizationinspection":
                rented_warning = "The selected vehicle can't be sent to Legalization/Inspection due to:"
                label_rented_warning = tk.Label(warning_pop, text=rented_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_rented_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(15,5))

            elif warning == "employeesdata":
                section_warning = "Error while trying to access employees data"
                label_warning = tk.Label(warning_pop, text=section_warning, font=("Helvetica", 12),   
                                               fg="white", bg="darkred")
                label_warning.pack(ipadx=10)

                warning_label = tk.Label(warning_pop, text=variable, font=("Helvetica", 10),
                                           fg="white", bg="black")
                warning_label.pack(pady=(15,5))

        elif isinstance(variable, dict):
            if warning == "validateaddrecord":
                validate_add_record_warning = f"Please confirm to add record"
                label_validate_add_record_warning = tk.Label(warning_pop, text=f"{validate_add_record_warning}", font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_validate_add_record_warning.pack(pady=5, padx=20)

                if 'Pick-up Date' in variable:
                    if 'Total Cost' in variable:
                        limit = 16
                    else:
                        limit = 5
                elif 'Model' in variable:
                    limit = 14
                else:
                    limit = 17

                for index, (key, value) in enumerate(variable.items()):
                    if index < limit:
                        validate_add_record_label = tk.Label(warning_pop, text=f"{key} : {value[0]}", font=("Helvetica", 10),
                                                    fg="white", bg="black")
                        validate_add_record_label.pack(pady=3)
                    else:
                        break

                photos_validate_label_button_frame = tk.Frame(warning_pop)
                photos_validate_label_button_frame.pack()
                photos_validate_label_button_frame.configure(bg="black")
                
                photos_to_validate_label = tk.Label(photos_validate_label_button_frame, font=("Helvetica", 10),
                                                    fg="white", bg="black")
                photos_to_validate_label.grid(row=0, column=0)

                if next(iter(variable)) == 'Vehicle Type':
                    paths = variable['Vehicle Photos'].strip("()")
                    photos_to_validate_label.config(text="Vehicle Photos :")
                elif next(iter(variable)) == 'Full Name':
                    paths = variable['Client ID Photos'].strip("()")
                    photos_to_validate_label.config(text="Client ID Photos :")
                elif next(iter(variable)) == 'Pick-up Date':
                    paths = variable['Receipt Photos'].strip("()")
                    photos_to_validate_label.config(text="Receipt Photos :")

                split_paths = paths.split(', ')

                photos_to_validate_button = Button(photos_validate_label_button_frame, text="Verify Photos", fg="white",
                                               bg="black", width=10, command=lambda: self.photo_viewer(warning_pop, split_paths, "View Mode"))
                photos_to_validate_button.grid(row=0, column=1)
                
                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=15)
                confirm_cancel_frame.configure(bg="black")

                confirm_record_validation_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=10, command=lambda: choice("confirm"))
                confirm_record_validation_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_record_validation_button) 

                cancel_record_validation_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=10, command=lambda: choice("cancel"))
                cancel_record_validation_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_record_validation_button)

        elif isinstance(variable, pd.core.frame.DataFrame):
            print("Is instance of Dataframe")
            if warning == "dfdatabvalidadd":

                def grab_photo_path(e):
                    global photos
                    selected_items = treeview.selection()

                    if selected_items:
                        verify_photo_button.config(state=NORMAL)
                        item_id = selected_items[0]
                        if treeview.exists(item_id):
                            values = treeview.item(item_id, "values")
                            if values:
                                paths = values[-1]
                                photos = paths.split(',')
                                print(photos)
                            else:
                                print("No values found for the selected item")
                        else:
                            print("Selected item does not exist in the treeview")
                    else:
                        print("No item selected")

                warning_pop.maxsize(600,500)

                db_valid_warning = f"Please confirm the information of the following {len(variable)} record(s) to add to the Database"
                label_valid_record = tk.Label(warning_pop, text=db_valid_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_valid_record.pack(pady=10)

                treeview_confirm_frame = tk.Frame(warning_pop)
                treeview_confirm_frame.pack()
                treeview_confirm_frame.configure(bg="black")

                treeScrolly = ttk.Scrollbar(treeview_confirm_frame, orient="vertical")
                treeScrolly.pack(side="right", fill="y")

                treeScrollx = ttk.Scrollbar(treeview_confirm_frame, orient="horizontal")
                treeScrollx.pack(side="bottom", fill="x")

                treeview = ttk.Treeview(treeview_confirm_frame, show="headings",
                                        yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)


                treeScrolly.config(command=treeview.yview)
                treeScrollx.config(command=treeview.xview)

                column_list = variable.columns.tolist()

                if 'Payment-Method' in column_list:
                    reservation_headings = ['Pick-up Date', 'Drop-off Date', 'Vehicle ID', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                      'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                      'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Receipt Photos']

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    variable['Pick-up Date'] = variable['Pick-up Date'].apply(convert_to_datetime)
                    variable['Drop-off Date'] = variable['Drop-off Date'].apply(convert_to_datetime)                  

                    treeview["column"] = reservation_headings
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")

                    columns_to_int = ['Rental Duration', 'Cost Per Day', 'Total Cost']

                    for column in columns_to_int:
                        try:
                            # Convert the column to integers, filling NaN values with 0
                            variable[column] = variable[column].fillna(0).astype('int64')
                            # Replace 0 with 'nan'
                            variable[column] = variable[column].replace(0, 'nan')
                        except ValueError:
                            pass              
                       
                    df_rows = variable.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"][:-1]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                        
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                        
                        column_width = max(heading_width, max_width) + 20 

                        treeview.column(col, width=column_width, minwidth=heading_width)

                    last_col = treeview["columns"][-1]
                    treeview.column(last_col, width=120, minwidth=120)

                treeview.pack(expand=True, fill="both")

                verify_photo_frame = tk.Frame(warning_pop)
                verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                verify_photo_frame.configure(bg="black")

                verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="white",
                                               bg="black", width=20, state=DISABLED, command=lambda: self.photo_viewer(warning_pop, photos, "View Mode"))
                verify_photo_button.pack(side="right", padx=5)
                self.bind_hover_effects(verify_photo_button) 

                confirm_cancel_frame = tk.Frame(warning_pop)
                confirm_cancel_frame.pack(pady=(5,15))
                confirm_cancel_frame.configure(bg="black")

                confirm_record_validation_button = Button(confirm_cancel_frame, text="Confirm", fg="white",
                                               bg="darkgreen", width=10, command=lambda: choice("confirm"))
                confirm_record_validation_button.grid(row=0, column=0, padx=10)
                self.green_bind_hover_effects(confirm_record_validation_button) 

                cancel_record_validation_button = Button(confirm_cancel_frame, text="Cancel", fg="white",
                                               bg="darkred", width=10, command=lambda: choice("cancel"))
                cancel_record_validation_button.grid(row=0, column=1, padx=10)
                self.red_bind_hover_effects(cancel_record_validation_button)

                treeview.bind("<ButtonRelease-1>", grab_photo_path)

            elif warning == "export":

                export_warning = f"Please select the desired Export Format"
                label_export_warning = tk.Label(warning_pop, text=export_warning, font=("Helvetica", 12),
                                               fg="white", bg="darkgreen")
                label_export_warning.pack(pady=10)

                format_frame = tk.Frame(warning_pop)
                format_frame.pack(pady=(5,15))
                format_frame.configure(bg="black")

                column_list = variable.columns.tolist()

                current_date = str(datetime.now(timezone.utc))[:19].replace(":", "-")

                def export_excel(file_name):
                    file_name += "-Excel"
                    variable.to_excel(f"{file_name}.xlsx", index=False)
                    warning_pop.destroy()

                def export_csv(file_name):
                    file_name += "-CSV"
                    variable.to_csv(f"{file_name}.csv", index=False)
                    warning_pop.destroy()


                if "pick_up_date" in column_list:
                    single_item = f"Reservation-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Reservations {current_date}"
                elif "dob" in column_list:
                    single_item = f"Client-ID-Passport {variable.at[0, 'id_number']} - {current_date}"
                    multiple_items = f"Clients {current_date}"
                elif "vehicle_type" in column_list:
                    single_item = f"Vehicle-License Plate {variable.at[0, 'license_plate']} - {current_date}"
                    multiple_items = f"Vehicles {current_date}"
                elif "employee_type" in column_list:
                    single_item = f"Employee-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Employees {current_date}"
                else:
                    single_item = f"Payment-ID {variable.at[0, 'id']} - {current_date}"
                    multiple_items = f"Payments {current_date}"

                if len(variable) == 1:
                    file_name = single_item
                    print(file_name)
                else:
                    file_name = multiple_items
                    print(file_name)


                csv_button = Button(format_frame, text="CSV Format", fg="white",
                                               bg="black", width=10, command=lambda: export_csv(file_name))
                csv_button.grid(row=0, column=0, padx=10)
                self.bind_hover_effects(csv_button) 

                excel_button = Button(format_frame, text="Excel Format", fg="white",
                                               bg="black", width=10, command=lambda: export_excel(file_name))
                excel_button.grid(row=0, column=1, padx=10)
                self.bind_hover_effects(excel_button)

    # Method to validate the values of the inputs or selection boxes, to make sure no data is missing or the type of data is wrong
    def validate_data(self, type_of_data, num, alpha, defined, empty):
        global not_num, not_alpha, not_defined, is_empty, errors_found
              
        if type_of_data == "entries":
            not_num = ["Invalid input, must only contain numbers"]
            for column_num, value_num in num.items():
                first_value = value_num[0]
                try:
                    int(first_value)
                except ValueError:
                    not_num.append(column_num)
                    
            not_alpha = ["Invalid input, must only contain letters"]
            for column_word, value_word in alpha.items():
                first_value = value_word[0]
                clean_first_value = re.sub(r'[^\w\s]', '', first_value).replace(' ','')
                if all(char.isalpha() for char in clean_first_value):
                    pass
                else:
                    not_alpha.append(column_word)

            not_defined = ["Must select one of the options"]
            for column_defined, value_defined in defined.items():
                first_value = value_defined[0]
                if first_value == "Not Defined":
                    not_defined.append(column_defined)
                else:
                    pass

            is_empty = ["Entry is empty"]
            for column_all, value_all in empty.items():
                first_value = value_all[0]
                if len(first_value) == 0 or str(first_value).lower() == "empty" or str(first_value).lower() == "0":
                    is_empty.append(column_all)
                else:
                    pass

        elif type_of_data == "data_add_database":
            not_num = ["Invalid input, must only contain numbers"]
            for column_num, value_num in num.items():
                try:
                    int(value_num)
                except ValueError:
                    not_num.append(column_num)
                    
            not_alpha = ["Invalid input, must only contain letters"]
            for column_word, value_word in alpha.items():
                clean_first_value = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                if all(char.isalpha() for char in clean_first_value):
                    pass
                else:
                    not_alpha.append(column_word)

            not_defined = ["Must select one of the options"]
            for column_defined, value_defined in defined.items():
                first_value = value_defined[0]
                second_value = value_defined[1]
                if first_value.lower() not in [val.lower() for val in second_value] or first_value.lower() == 'not defined':
                    not_defined.append(column_defined)
                else:
                    pass

            is_empty = ["Entry is empty"]
            for column_all, value_all in empty.items():
                if len(value_all) == 0 or value_all.lower() == "nan" or value_all.lower() == "0":
                    is_empty.append(column_all)
                else:
                    pass

        errors_found = is_empty, not_defined, not_alpha, not_num

    # Method to verify the photo path and format of each photo in the list of photos
    def verify_photo_path(self, possible_photo_paths):
        global invalid_photo_paths, valid_photo_paths, valid_photo_type, invalid_photo_type

        paths_list = possible_photo_paths.split(',')

        paths_list = [path.strip() for path in paths_list]

        allowed_extensions = ['.png', '.jpg', '.jpeg']

        invalid_photo_type = []
        valid_photo_type = []
        for path in paths_list:
            if any(path.lower().endswith(ext) for ext in allowed_extensions):
                valid_photo_type.append(path)
            else:
                invalid_photo_type.append(path)

        invalid_photo_paths = []
        valid_photo_paths = []
        for path in valid_photo_type:
            try:
                print(f"Image open: {Image.open(path)}")
                Image.open(path)
                valid_photo_paths.append(path)
            except FileNotFoundError:
                invalid_photo_paths.append(path)

    # Method to verify if there is any repeated element inside a list of data that must only contain unique elements
    def check_if_repeated(self, valid, column):
        check_repeated = [re.sub(r'[^\w\s]', '', str(self.df.at[record, column]).lower()) for record in valid]

        repeated_value = []
        single_value = []
        for record in check_repeated:
            if record in single_value:
                repeated_value.append(record)                                    
            else:
                single_value.append(record)

        not_unique = []
        for record in valid:
            if re.sub(r'[^\w\s]', '', str(self.df.at[record, column]).lower()) in repeated_value:
                not_unique.append(record)
        
        column_repeated = []       
        if len(not_unique) > 0:
            column_repeated.append(column)

        warning_repeated = not_unique, repeated_value, column

        return valid, warning_repeated

    # Method that creates a window where the user can select a date
    def datepicker(self, window, entry, date_type, button=None, pick_date=None, costs=None):
        picker_calendar = tk.Toplevel(window)
        picker_calendar.title("Select a date")
        picker_calendar.iconphoto(True, tk.PhotoImage(file=resource_path('resources/lw.png')))
        picker_calendar.resizable(0,0)
        picker_calendar.configure(bg="black")
        picker_calendar.grab_set()

        def select_date():
            selected_date = cal.get_date()
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)
            entry.config(state="readonly")
            if button is not None:
                if pick_date is not None:
                    button.config(state=DISABLED)
                    costs()
                else:
                    button.config(state=NORMAL)

            picker_calendar.destroy()


        current_date = datetime.now().date()
        five_days_later = current_date + timedelta(days=5)

        cal = Calendar(picker_calendar, selectmode='day', date_pattern='yyyy-mm-dd', date=current_date)
        cal.pack()

        if date_type == "reservation":
            if hasattr(self, 'df'):
                if pick_date is not None:
                    date = datetime.strptime(pick_date, '%Y-%m-%d').date()
                    cal.config(mindate=date)
                else:
                    pass
            elif not hasattr(self, 'df'):
                if pick_date is not None:
                    date = datetime.strptime(pick_date, '%Y-%m-%d').date()
                    cal.config(mindate=date)
                else:
                    cal.config(mindate=current_date, maxdate=five_days_later)
        elif date_type == "vehicle_date":
            cal.config(maxdate=current_date)
        elif date_type == "dob":
            must_be_adult = datetime.now() - timedelta(days=18*365)
            current_date = must_be_adult.date()
            cal.config(maxdate=current_date)

        get_date_button = tk.Button(picker_calendar, text="Select Date", command=select_date)
        get_date_button.pack(pady=5)

    # Method to verify the employee code that the user tries to use when confirming certain actions
    def check_employee_code(self, code, must_be_manager=False):

        if code == "":
            code_result = "Must enter employee code to confirm this action"
        else:
            employee = None
            employee = Employee.query.filter(Employee.employee_code.ilike(code)).first()
            if employee is not None:
                if must_be_manager is True:
                    if employee.employee_type == "Manager":
                        code_result = "valid"
                    else:
                        code_result = "The employee with the given code is not allowed to perform this action\nMust be a Manager"
                else: code_result = "valid" 
            else:
                code_result = "The given employee code doesn't match any registered employee code" 

        return code_result

    # Method that calculates date based on the current date (e.g. next inspection date)
    def calculate_date(self, date, add_one=False):
        date_object = datetime.strptime(date, "%Y-%m-%d")
        given_day = date_object.day
        given_month = date_object.month
        given_year = date_object.year

        current_day = datetime.now().day
        current_month = datetime.now().month
        current_year = datetime.now().year

        # When add_one is False we let the program decide if its necessary to add one year to the current date, based on the current date
        if add_one is False:
            if given_month == current_month:
                if given_day >= current_day:
                    new_date = datetime(current_year, given_month, given_day)
                elif given_day < current_day:
                    if given_month == 2:
                        if given_day == 29:
                            new_date = datetime(current_year + 1, given_month, given_day-1)
                            print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
                        else:
                            new_date = datetime(current_year + 1, given_month, given_day)
                            print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
                    else:
                        new_date = datetime(current_year + 1, given_month, given_day)
                        print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
            elif given_month > current_month:
                new_date = datetime(current_year, given_month, given_day)
                print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
            elif given_month < current_month:
                if given_month == 2:
                    if given_day == 29:
                        new_date = datetime(current_year + 1, given_month, given_day-1)
                        print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
                    else:
                        new_date = datetime(current_year + 1, given_month, given_day)
                        print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
                else:
                    new_date = datetime(current_year + 1, given_month, given_day)
                    print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))

        # Add one is True for example when we confirm the vehicle inspection/legalization and we need to update the next inspection/legalization date to be the same but on the next year
        elif add_one is True:
            if given_month == 2:
                if given_day == 29:
                    new_date = datetime(current_year + 1, given_month, given_day-1)
                    print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
                else:
                    # Next inspection is in the next year at the given month and day
                    new_date = datetime(current_year + 1, given_month, given_day)
                    print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))
            else:
                new_date = datetime(current_year + 1, given_month, given_day)
                print("The next date is scheduled for:", new_date.strftime("%Y-%m-%d"))

        new_date = str(new_date.date())

        return new_date

    # Method to create a window where the user can create new users/employees
    def new_employee(self):
        new_employee_window = tk.Toplevel(self.root)
        new_employee_window.title("New User")
        new_employee_window.iconphoto(True, tk.PhotoImage(file=resource_path('resources/lw.png')))
        new_employee_window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x_new_employee = (screen_width - self.WINDOW_WIDTH) // 2
        center_y_new_employee = (screen_height - self.WINDOW_HEIGHT) // 2

        new_employee_window.geometry(f"+{center_x_new_employee}+{center_y_new_employee}")
        new_employee_window.resizable(False, False)
        new_employee_window.configure(bg='black')

        def confirm_register():
            try:
                must_be_number = {}

                must_not_have_number = {
                        'Full Name': (new_fullname_entry.get(), new_fullname_entry)
                    }

                must_be_defined = {
                        'Employee Type': (selected_type.get(), type_combobox)
                }

                must_not_be_empty = {
                     
                        'Full Name': (new_fullname_entry.get(), new_fullname_entry),
                        'Username': (new_username_entry.get(), new_username_entry),
                        'Password': (new_password_entry.get(), new_password_entry),
                        'Confirm Password': (confirm_password_entry.get(), confirm_password_entry),                               
                        'Employee Code': (employee_code_entry.get(), employee_code_entry)
                    }

                self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                if any(len(error_list) > 1 for error_list in errors_found):
                    result_of_validation = "Error Found" 
                    print("Error Found")
                else:
                    result_of_validation = "No Error Found"
                    print("No Error Found")

                if result_of_validation == "No Error Found":
                    try:
                        with self.flask_app.app_context():
                            db.create_all()
                            code =  re.sub(r'[^\w\s]', '', str(employee_code_entry.get()).lower())
                            existing_code = Employee.query.filter(Employee.employee_code.ilike(code)).first()
                            if existing_code is not None:
                                self.toggle_entry_colors(0, employee_code_entry)
                                warning = f"The following employee code {code} already exists in the Database\nPlease choose a different employee code"
                                self.pop_warning(new_employee_window, warning, "employeecodeexists")
                            else:
                                self.toggle_entry_colors(1, employee_code_entry)
                                if new_password_entry.get() == confirm_password_entry.get():
                                    self.toggle_entry_colors(1, new_password_entry)
                                    self.toggle_entry_colors(1, confirm_password_entry)
                                    if len(new_password_entry.get()) < 10:
                                        warning="Password is too short\nPlease use at least 10 characters"
                                        self.pop_warning(new_employee_window, warning, "erroraddemploye")
                                        return
                                    existing_user = Employee.query.filter(Employee.username.ilike(new_username_entry.get())).first()
                                    if existing_user:
                                        warning="Username already exists\nChoose a different username"
                                        self.pop_warning(new_employee_window, warning, "erroraddemploye")
                                        return

                                    password_hash = bcrypt.generate_password_hash(new_password_entry.get()).decode('utf-8')

                                    new_employee = Employee(full_name=new_fullname_entry.get(), 
                                        username=new_username_entry.get(), 
                                        password=password_hash,
                                        employee_code=employee_code_entry.get(),
                                        employee_type=selected_type.get())

                                    db.session.add(new_employee)

                                    db.session.commit()
                                    new_employee_window.destroy()
                                else:
                                    self.toggle_entry_colors(0, new_password_entry)
                                    self.toggle_entry_colors(0, confirm_password_entry)
                                    warning="Passwords do not match"
                                    self.pop_warning(new_employee_window, warning, "erroraddemploye")
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_employee_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    for key in must_not_be_empty:
                        if key in is_empty:
                            entry_value = must_not_be_empty[key][1]
                            self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                            if key == "Year":
                                year_entry.config(readonlybackground="darkred")
                        else:
                            self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                    for key in must_be_defined:
                        if key in not_defined:
                            combobox_value = must_be_defined[key][1]
                            self.toggle_combo_text(0, must_be_defined[key][1])
                        else:
                            self.toggle_combo_text(1, must_be_defined[key][1])

                    for key in must_not_have_number:
                        if key in not_alpha or key in is_empty:
                            entry_value = must_not_have_number[key][1]
                            self.toggle_entry_colors(0, must_not_have_number[key][1])
                        else:
                            self.toggle_entry_colors(1, must_not_have_number[key][1])

                    for key in must_be_number:
                        if key in not_num or key in is_empty:
                            entry_value = must_be_number[key][1]
                            self.toggle_entry_colors(0, must_be_number[key][1])
                        else:
                            self.toggle_entry_colors(1, must_be_number[key][1])

                    errors_adding = []
                    for error_list in errors_found:
                        if len(error_list) > 1:
                            errors_adding.append(error_list)

                    if len(errors_adding) > 0:
                        self.pop_warning(new_employee_window, errors_adding, "addrecvalidation")
            except Exception as e:
                print(e)

        label_font = ("Helvetica", 20)
        new_employee_label = tk.Label(new_employee_window, text="Register new User", font=label_font, fg="white", bg="black")
        new_employee_label.pack(pady=(50, 20))

        new_fullname_label = tk.Label(new_employee_window, text="Full Name:", fg="white", bg="black")
        new_fullname_label.pack(side=tk.TOP, padx=10, pady=2)
        new_fullname_entry = Entry(new_employee_window, width=35, borderwidth=5)
        new_fullname_entry.pack(side=tk.TOP, pady=2)

        new_username_label = tk.Label(new_employee_window, text="Choose a Username:", fg="white", bg="black")
        new_username_label.pack(side=tk.TOP, padx=10, pady=2)
        new_username_entry = Entry(new_employee_window, width=35, borderwidth=5)
        new_username_entry.pack(side=tk.TOP, pady=2)

        new_password_label = tk.Label(new_employee_window, text="Password:", fg="white", bg="black")
        new_password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        new_password_entry = Entry(new_employee_window, show="*", width=35, borderwidth=5)
        new_password_entry.pack(side=tk.TOP, pady=2)

        confirm_password_label = tk.Label(new_employee_window, text="Confirm Password:", fg="white", bg="black")
        confirm_password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        confirm_password_entry = Entry(new_employee_window, show="*", width=35, borderwidth=5)
        confirm_password_entry.pack(side=tk.TOP, pady=2)

        employee_code_label = tk.Label(new_employee_window, text="Employee code:", fg="white", bg="black")
        employee_code_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        employee_code_entry = Entry(new_employee_window, width=35, borderwidth=5)
        employee_code_entry.pack(side=tk.TOP, pady=2)

        type_employee_label = tk.Label(new_employee_window, text="Employee type:",
                         font=("Helvetica", 10), fg="white", bg="black")
        type_employee_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        employee_types = ['Not Defined', 'Regular', 'Manager']
        selected_type = tk.StringVar()
        type_combobox = ttk.Combobox(new_employee_window,
                                        textvariable=selected_type,
                                        values=employee_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        type_combobox.pack(side=tk.TOP, pady=2)
        type_combobox.set(employee_types[0]) 

        new_register_button = tk.Button(new_employee_window, text="Register", command=confirm_register, fg="white", bg="#004d00")
        new_register_button.pack(side=tk.TOP, pady=(20, 80))
        self.green_bind_hover_effects(new_register_button)

        new_employee_window.grab_set()

    # Section to insert vehicles into the database
    def insert_vehicle_section(self, new_window):
        if hasattr(self, 'df'):
            del self.df
        else:
            pass

        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        file_section_info = "Upload a Excel/CSV file by pressing the 'Upload Vehicle File' button"
        file_section_info_label = tk.Label(treeFrame, text=file_section_info, font=("Helvetica", 10),
                                           fg="white", bg="black")
        file_section_info_label.pack(pady=(140, 0))

        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)

        edit_treeview_frame.configure(bg="black")

        # Function to check if the selected file is the intended for this section
        def check_data(): 
            if self.df is not None and not self.df.empty:
                vehicle_file_headings = []
                for column in self.df.columns:
                    vehicle_file_headings.append(column.lower())

                vehicle_headings = ['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate',
                                    'Seats', 'Doors', 'Color', 'Fuel', 'Type of Gearbox', 'Vehicle CC', 'Number of Wheels',
                                     'Vehicle Photos']

                vehicle_headings_lowercase = [head.lower() for head in vehicle_headings]

                vehicle_file_headings_check = all(
                    head in vehicle_file_headings for head in vehicle_headings_lowercase)

                if vehicle_file_headings_check and len(vehicle_file_headings) == len(vehicle_headings):
                    add_vehicle_button.grid_forget()

                    for widget in treeFrame.winfo_children():
                        widget.destroy()

                    treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeFrame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    # Function to analyze the data in each row and column, if an error occurs (e.g., empty cells or wrong input type), the row containing the error is highlighted in red
                    def verify_data(): 
                        for index, row in self.df.iterrows():
                            not_num = []
                            must_be_number = {
                                'Seats': row['Seats'],
                                'Number of Wheels': row['Number of Wheels'],
                                'Doors': row['Doors']
                            }

                            if str(row['Vehicle Type']).lower() == "motorcycles":
                                del must_be_number['Doors']

                            for column_num, value_num in must_be_number.items():
                                try:
                                    int(value_num)
                                except ValueError:
                                    not_num.append(value_num)

                            not_alpha = []
                            must_not_have_number = {
                                'Vehicle Type': str(row['Vehicle Type']),
                                'Segment': str(row['Segment']),
                                'Category': str(row['Category']),
                                'Fuel': str(row['Fuel']),
                                'Type of Gearbox': str(row['Type of Gearbox']),
                                'Brand': str(row['Brand']),
                                'Color': str(row['Color'])
                            }

                            for column_word, value_word in must_not_have_number.items():
                                clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                                if all(char.isalpha() for char in clean_value_word):
                                    pass
                                else:
                                    not_alpha.append(value_word)

                            is_empty = []
                            all_data = {
                                'Year': str(row['Year']),
                                'Seats': str(row['Seats']),
                                'Number of Wheels': str(row['Number of Wheels']),
                                'Doors': str(row['Doors']),
                                'Model': str(row['Model']),
                                'Vehicle Type': str(row['Vehicle Type']),
                                'Segment': str(row['Segment']),
                                'Category': str(row['Category']),
                                'Fuel': str(row['Fuel']),
                                'Color': str(row['Color']),
                                'Type of Gearbox': str(row['Type of Gearbox']),
                                'Brand': str(row['Brand']),
                                'Vehicle Photos': str(row['Vehicle Photos']),
                                'License Plate': str(row['License Plate']),
                                'Vehicle CC': str(row['Vehicle CC'])
                            }

                            if str(row['Vehicle Type']).lower() == "motorcycles":
                                del all_data['Doors']

                            for column_all, value_all in all_data.items():
                                if value_all == 'nan':
                                    is_empty.append(value_all)
                                else:
                                    pass

                            not_defined = []
                            must_be_defined = {
                                'Vehicle Type': (str(row['Vehicle Type']), vehicle_types),
                                'Category': (str(row['Category']), categories),
                                'Fuel': (str(row['Fuel']), fuels),
                                'Type of Gearbox': (str(row['Type of Gearbox']), gearbox_types)
                            }

                            for column_defined, value_defined in must_be_defined.items():
                                if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                                    not_defined.append(value_defined)
                                else:
                                    pass

                            if str(row['Vehicle Type']).lower() == 'cars':
                                if str(row['Segment']).lower() not in [seg.lower() for seg in segments_cars] or str(row['Segment']).lower() == 'not defined':
                                    not_defined.append(str(row['Segment']))
                                if str(row['Vehicle CC']).lower() not in [c.lower() for c in cc_not_relevant] or str(row['Vehicle CC']).lower() == 'not defined':
                                    not_defined.append(str(row['Vehicle CC']))
                            elif str(row['Vehicle Type']).lower() == 'motorcycles':
                                if str(row['Segment']).lower() not in [seg.lower() for seg in segments_motorcycles] or str(row['Segment']).lower() == 'not defined':
                                    not_defined.append(str(row['Segment']))
                                if str(row['Vehicle CC']).lower() not in [c.lower() for c in cc_list] or str(row['Vehicle CC']).lower() == 'not defined':
                                    not_defined.append(str(row['Vehicle CC']))

                            errors_found = not_num, not_alpha, is_empty, not_defined

                            possible_photo_path_list = str(row['Vehicle Photos'])

                            self.verify_photo_path(possible_photo_path_list)
                            if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                                pass
                            if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                is_empty.append("Photos")

                            date_to_check = str(row['Year'])
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            if any(len(error_list) > 0 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False:
                                result_of_validation = "Error Found"
                                self.change_row_color(treeview, index, "darkred")
                            else:
                                self.change_row_color(treeview, index, "#313131")
                                result_of_validation = "No Error Found"


                    # Function to refresh the data of the treeview widget after any change to the data of the dataframe
                    def refresh_tree():
                        treeview.delete(*treeview.get_children())

                        def convert_to_datetime(date_string):
                            try:
                                return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                            except ValueError:
                                return date_string

                        self.df['Year'] = self.df['Year'].apply(convert_to_datetime)

                        treeview["column"] = list(self.df)
                        treeview["show"] = "headings"

                        for column in treeview["column"]:
                            treeview.heading(column, text=column)
                            treeview.column(column, anchor="center")

                        columns_to_int = ['Doors', 'Number of Wheels', 'Seats', 'License Plate', 'Vehicle CC']

                        for column in columns_to_int:
                            try:
                                self.df[column] = self.df[column].fillna(0).astype('int64')
                                self.df[column] = self.df[column].replace(0, 'nan')
                            except ValueError:
                                pass             
                           
                        df_rows = self.df.to_numpy().tolist()
                        for row in df_rows:
                            treeview.insert("", "end", values=row)

                        for col in treeview["columns"][:-1]:
                            heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                            
                            max_width = max(
                                tkFont.Font().measure(str(treeview.set(item, col)))
                                for item in treeview.get_children("")
                            )
                            
                            column_width = max(heading_width, max_width) + 30  
                            
                            treeview.column(col, width=column_width, minwidth=column_width)

                        photo_col = "Vehicle Photos"
                        treeview.column(photo_col, width=120, minwidth=120)
                        year_entry.config(readonlybackground="#313131")

                        treeview.update_idletasks()

                        verify_data()

                    # Function to clear the text entries/selection option
                    # Restores the original color of the text/text entries/buttons (in case any errors occurred previously)
                    def clear_entries():
                        entries = [license_plate_entry, employee_code_entry, brand_entry, model_entry, seats_entry, doors_entry, color_entry, wheels_entry]
                        for entry in entries:
                            entry.delete(0, END)
                            self.toggle_entry_colors(1, entry)

                        read_only_entries = [year_entry, doors_entry]
                        for entry in read_only_entries:
                            entry.config(state=tk.NORMAL)
                            entry.delete(0, tk.END)
                            entry.config(state="readonly", readonlybackground="#313131")


                        combos = [[gearbox_combobox, gearbox_types],[fuel_combobox, fuels], [segment_combobox, segments_cars], [category_combobox, categories], [vehicle_type_combobox, vehicle_types], [cc_combobox, cc_list]]
                        for combo in combos:
                            self.toggle_combo_text(1, combo[0])
                            combo[0].set(combo[1][0])

                        if hasattr(self, 'photo_paths'):
                            del self.photo_paths
                        see_photos_button.configure(state=tk.DISABLED)
                        reload_show_photos_button.configure(image=self.update_photos_button_image)

                    # Function to select elements from the table, automatically performs some actions (e.g., fills the text entries/options with the respective information)
                    def select_record(e):
                        clear_entries()

                        selected_items = treeview.selection()

                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])

                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                            vehicle_type = str(self.df.at[x, "Vehicle Type"]).lower()

                            if vehicle_type == "cars":
                                vehicle_type_combobox.set(vehicle_types[1])
                                self.toggle_combo_text(1, vehicle_type_combobox)
                                doors_entry.config(state=NORMAL)
                                doors_entry.insert(0, self.df.at[x, "Doors"])
                            elif vehicle_type == "motorcycles":
                                vehicle_type_combobox.set(vehicle_types[2])
                                self.toggle_combo_text(1, vehicle_type_combobox)
                                doors_entry.config(state=NORMAL)
                                doors_entry.insert(0, 0)
                                doors_entry.config(state="readonly", readonlybackground="#313131")
                            else:
                                vehicle_type_combobox.set(vehicle_types[0])
                                self.toggle_combo_text(0, vehicle_type_combobox)

                            category = str(self.df.at[x, "Category"]).lower()
                            if category == "gold":
                                category_combobox.set(categories[1])
                                self.toggle_combo_text(1, category_combobox)
                            elif category == "silver":
                                category_combobox.set(categories[2])
                                self.toggle_combo_text(1, category_combobox)
                            elif category == "economic":
                                category_combobox.set(categories[3])
                                self.toggle_combo_text(1, category_combobox)
                            else:
                                category_combobox.set(categories[0])
                                self.toggle_combo_text(0, category_combobox)

                            segment = str(self.df.at[x, "Segment"]).lower()
                            cc = str(self.df.at[x, 'Vehicle CC']).lower()

                            if vehicle_type == "cars":
                                segment_options = segments_cars
                                mapping = {seg.lower(): segments_cars[i] for i, seg in enumerate(segments_cars)}
                                cc_options = cc_not_relevant
                                mapping_cc = {c.lower(): cc_not_relevant[i] for i, c in enumerate(cc_not_relevant)}
                            else:
                                segment_options = segments_motorcycles
                                mapping = {seg.lower(): segments_motorcycles[i] for i, seg in enumerate(segments_motorcycles)}
                                cc_options = cc_list
                                mapping_cc = {c.lower(): cc_list[i] for i, c in enumerate(cc_list)}

                            segment_combobox['values'] = segment_options
                            segment_combobox.set(segment_options[0])
                            segment_combobox.set(mapping.get(segment.lower(), "Not Defined"))

                            if segment_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, segment_combobox)
                            else:
                                self.toggle_combo_text(1, segment_combobox)

                            cc_combobox['values'] = cc_options
                            cc_combobox.set(cc_options[0])
                            cc_combobox.set(mapping_cc.get(cc.lower(), "Not Defined"))

                            if cc_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, cc_combobox)
                            else:
                                self.toggle_combo_text(1, cc_combobox)

                            fuel = str(self.df.at[x, "Fuel"]).lower()

                            fuel_combobox.set(fuels[0]) 
                            mapping = {f.lower(): fuels[i] for i, f in enumerate(fuels)}
                            fuel_combobox.set(mapping.get(fuel, mapping["not defined"]))

                            if fuel_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, fuel_combobox)
                            else:
                                self.toggle_combo_text(1, fuel_combobox)

                            gearbox = str(self.df.at[x, "Type of Gearbox"]).lower()

                            gearbox_combobox.set(gearbox_types[0]) 
                            mapping = {gear.lower(): gearbox_types[i] for i, gear in enumerate(gearbox_types)}
                            gearbox_combobox.set(mapping.get(gearbox, mapping["not defined"]))
                            if gearbox_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, gearbox_combobox)
                            else:
                                self.toggle_combo_text(1, gearbox_combobox)


                            brand_entry.insert(0, self.df.at[x, "Brand"])
                            model_entry.insert(0, self.df.at[x, "Model"])
                            license_plate_entry.insert(0, self.df.at[x, "License Plate"])
                            seats_entry.insert(0, self.df.at[x, "Seats"])
                            color_entry.insert(0, self.df.at[x, "Color"])
                            wheels_entry.insert(0, self.df.at[x, "Number of Wheels"])

                            year_entry.config(state=tk.NORMAL)
                            year_entry.insert(0, self.df.at[x, "Year"])
                            year_entry.config(state="readonly")

                            date_to_check = str(self.df.at[x, "Year"])
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                            if bool(re.match(pattern, date_to_check)) == False:
                                year_entry.config(readonlybackground="darkred")
                            else:
                                year_entry.config(readonlybackground="#313131")

                            must_not_empty_entries = {
                                seats_entry: seats_entry.get(),
                                wheels_entry: wheels_entry.get(),
                                doors_entry: doors_entry.get(),
                                brand_entry: brand_entry.get(),
                                color_entry: color_entry.get(),
                                license_plate_entry: license_plate_entry.get(),
                                model_entry: model_entry.get()
                            }
                            for column_entry_check, value_check in must_not_empty_entries.items():
                                if str(value_check).lower() == 'nan' or str(value_check).lower() == '0' or str(value_check).lower() == '':
                                    self.toggle_entry_colors_ifnan(0, column_entry_check)
                                    column_entry_check.delete(0, "end")
                                    column_entry_check.insert(0, "EMPTY")
                                else:
                                    self.toggle_entry_colors_ifnan(1, column_entry_check)

                            must_be_number_entries = {
                                seats_entry: seats_entry.get(),
                                wheels_entry: wheels_entry.get(),
                                doors_entry: doors_entry.get()
                            }
                            for value_key, value in must_be_number_entries.items():
                                try:
                                    int(value)
                                    self.toggle_entry_colors(1, value_key)
                                except ValueError:
                                    self.toggle_entry_colors(0, value_key)

                            must_not_have_number_entries = {
                                brand_entry: brand_entry.get(),
                                color_entry: color_entry.get()
                            }
                            for word_key, word in must_not_have_number_entries.items():
                                if any(not char.isalpha() for char in word) or str(word).lower() == "empty":
                                    self.toggle_entry_colors(0, word_key)
                                else:
                                    self.toggle_entry_colors(1, word_key)

                            self.verify_photo_path(str(self.df.at[x, "Vehicle Photos"]))
                            if str(self.df.at[x, "Vehicle Photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                self.toggle_button_colors(0, selected_vehicle_photos_button)
                                self.red_bind_hover_effects(selected_vehicle_photos_button)
                            else:
                                self.toggle_button_colors(1, selected_vehicle_photos_button)
                                self.bind_hover_effects(selected_vehicle_photos_button)
                                print(self.df.at[x, "Vehicle Photos"])
                        else:
                            pass

                    # Allows updating the data of the selected element in the table, so the user can update or correct any incorrect data without having to make that change in the file
                    def update_record():
                        must_be_number = {
                                'Seats': (seats_entry.get(), seats_entry),
                                'Number of Wheels': (wheels_entry.get(), wheels_entry),
                                'Doors': (doors_entry.get(), doors_entry)
                            }

                        must_not_have_number = {
                                'Brand': (brand_entry.get(), brand_entry),
                                'Color': (color_entry.get(), color_entry)
                            }

                        must_be_defined = {
                                'Vehicle Type': (selected_vehicle_type.get(), vehicle_type_combobox),
                                'Segment': (selected_segment.get(), segment_combobox),
                                'Category': (selected_category.get(), category_combobox),
                                'Fuel': (selected_fuel.get(), fuel_combobox),
                                'Type of Gearbox': (selected_gearbox.get(), gearbox_combobox),
                                'Vehicle CC': (selected_cc.get(), cc_combobox)
                        }

                        must_not_be_empty = {

                                'Seats': (seats_entry.get(), seats_entry),
                                'Number of Wheels': (wheels_entry.get(), wheels_entry),
                                'Doors': (doors_entry.get(), doors_entry),
                                'Model': (model_entry.get(), model_entry),                               
                                'Color': (color_entry.get(), color_entry),
                                'Brand': (brand_entry.get(), brand_entry),
                                'License Plate': (license_plate_entry.get(), license_plate_entry)
                            }

                        if selected_vehicle_type.get() == "Motorcycles":
                            del must_not_be_empty['Doors']

                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])

                            self.verify_photo_path(str(self.df.at[x, 'Vehicle Photos']))

                            if str(self.df.at[x, 'Vehicle Photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                if hasattr(self, 'photo_paths'):
                                    pass
                                else:
                                    is_empty.append("Photos")

                            date_to_check = str(year_entry.get())
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                                result_of_validation = "Error Found"
                            else:
                                result_of_validation = "No Error Found"

                            if result_of_validation == "No Error Found":
                                self.df.at[x, "Vehicle Type"] = selected_vehicle_type.get()
                                self.df.at[x, "Category"] = selected_category.get()
                                self.df.at[x, "Segment"] = selected_segment.get()
                                self.df.at[x, "Brand"] = brand_entry.get()
                                self.df.at[x, "Model"] = model_entry.get()
                                self.df.at[x, "Year"] = year_entry.get()
                                self.df.at[x, "License Plate"] = license_plate_entry.get()
                                self.df.at[x, "Seats"] = int(seats_entry.get())
                                self.df.at[x, "Doors"] = int(doors_entry.get())
                                self.df.at[x, "Color"] = color_entry.get()
                                self.df.at[x, "Fuel"] = selected_fuel.get()
                                self.df.at[x, "Vehicle CC"] = selected_cc.get()
                                self.df.at[x, "Type of Gearbox"] = selected_gearbox.get()
                                self.df.at[x, "Number of Wheels"] = (int(wheels_entry.get()))

                                if hasattr(self, 'photo_paths'):
                                    self.df.at[x, 'Vehicle Photos'] = self.photo_paths
                                else:
                                    pass

                                self.toggle_button_colors(1, selected_vehicle_photos_button)
                                clear_entries()

                                refresh_tree()
                            else:

                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format = str(self.df.at[x,'Year'])
                                    self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                                for key in must_not_be_empty:
                                    if key in is_empty:
                                        entry_value = must_not_be_empty[key][1]
                                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    else:
                                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                                for key in must_be_defined:
                                    if key in not_defined:
                                        combobox_value = must_be_defined[key][1]
                                        self.toggle_combo_text(0, must_be_defined[key][1])
                                    else:
                                        self.toggle_combo_text(1, must_be_defined[key][1])

                                for key in must_not_have_number:
                                    if key in not_alpha or key in is_empty:
                                        entry_value = must_not_have_number[key][1]
                                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_not_have_number[key][1])

                                if "Photos" in is_empty:
                                    self.toggle_button_colors(0, select_photos_button)
                                    self.red_bind_hover_effects(select_photos_button)
                                else:
                                    self.toggle_button_colors(1, select_photos_button)
                                    self.bind_hover_effects(select_photos_button)

                                for key in must_be_number:
                                    if key in not_num or key in is_empty:
                                        entry_value = must_be_number[key][1]
                                        self.toggle_entry_colors(0, must_be_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_be_number[key][1])

                                errors_adding = []
                                for error_list in errors_found:
                                    if len(error_list) > 1:
                                        errors_adding.append(error_list)

                                if len(errors_adding) > 0:
                                    self.pop_warning(new_window, errors_adding, "addrecvalidation")
                        else:
                            warning = "Must select an item to Update"
                            self.pop_warning(new_window, warning, "noselectedtoupdate" )

                        refresh_tree()

                    # Used to delete one or more elements from the table
                    def remove_selected():
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            for record in selected_items:
                                x = treeview.index(record)
                                treeview.delete(record)
                                self.df.drop(index=x, inplace=True)
                                print(self.df)

                                self.df.reset_index(drop=True, inplace=True)
                            verify_data()
                        else:
                            warning = "Must select at least one record to remove"
                            self.pop_warning(new_window, warning, "noselectedtoremove")

                    # Used to add one or more elements from the table to the database
                    def add_selected_to_database():
                        global errors_found
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            invalid_records = []
                            valid_records = []
                            for record in selected_items:
                                x = treeview.index(record)

                                must_be_number = {
                                        'Seats': (str(self.df.at[x, "Seats"])),
                                        'Number of Wheels': (str(self.df.at[x, "Number of Wheels"])),
                                        'Doors': (str(self.df.at[x, "Doors"]))
                                    }


                                must_not_have_number = {
                                        'Brand': (str(self.df.at[x, "Brand"])),
                                        'Color': (str(self.df.at[x, "Color"]))
                                    }

                                must_be_defined = {
                                        'Vehicle Type': (str(self.df.at[x, "Vehicle Type"]), vehicle_types),
                                        'Category': (str(self.df.at[x, "Category"]), categories),
                                        'Fuel': (str(self.df.at[x, "Fuel"]), fuels),
                                        'Type of Gearbox': (str(self.df.at[x, "Type of Gearbox"]), gearbox_types),
                                }


                                must_not_be_empty = {
                                        'Seats': (str(self.df.at[x, "Seats"])),
                                        'Number of Wheels': (str(self.df.at[x, "Number of Wheels"])),
                                        'Doors': (str(self.df.at[x, "Doors"])),
                                        'Model': (str(self.df.at[x, "Model"])),                               
                                        'Color': (str(self.df.at[x, "Color"])),
                                        'Brand': (str(self.df.at[x, "Brand"])),
                                        'License Plate': (str(self.df.at[x, "License Plate"]))
                                    }

                                if str(self.df.at[x, "Vehicle Type"]).lower() == "motorcycles":
                                    del must_be_number['Doors']
                                    del must_not_be_empty['Doors']

                                self.validate_data("data_add_database", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)


                                if str(self.df.at[x, "Vehicle Type"]).lower() == 'cars':
                                    if str(self.df.at[x, "Segment"]).lower() not in [seg.lower() for seg in segments_cars] or str(self.df.at[x, "Segment"]).lower() == 'not defined':
                                        not_defined.append("Segment")
                                    if str(self.df.at[x, "Vehicle CC"]).lower() not in [c.lower() for c in cc_not_relevant] or str(self.df.at[x, "Vehicle CC"]).lower() == 'not defined':
                                        not_defined.append("Vehicle CC")
                                elif str(self.df.at[x, "Vehicle Type"]).lower() == 'motorcycles':
                                    if str(self.df.at[x, "Segment"]).lower() not in [seg.lower() for seg in segments_motorcycles] or str(self.df.at[x, "Segment"]).lower() == 'not defined':
                                        not_defined.append("Segment")
                                    if str(self.df.at[x, "Vehicle CC"]).lower() not in [c.lower() for c in cc_list] or str(self.df.at[x, "Vehicle CC"]).lower() == 'not defined':
                                        not_defined.append("Vehicle CC")

                                print(f"Errors at index {x}: \n {errors_found}, {not_alpha}, {not_num}, {is_empty}, {not_defined}")
                                photos_of_selected = str(self.df.at[x, "Vehicle Photos"])

                                if photos_of_selected.lower() != "nan":

                                    self.verify_photo_path(photos_of_selected)

                                    if len(valid_photo_type) > 0:
                                        if len(valid_photo_paths) > 0:
                                            pass
                                        if len(invalid_photo_paths) > 0:
                                            invalid_photo_paths.insert(0, "Invalid Photo Paths")
                                            errors_found = errors_found + (invalid_photo_paths,)

                                    if len(invalid_photo_type) > 0:
                                        invalid_photo_type.insert(0, "Invalid Photo Type")
                                        errors_found = errors_found + (invalid_photo_type,)
                                else:
                                    is_empty.append("Photos")

                                if any(len(error_list) > 1 for error_list in errors_found):
                                    errors_found = tuple(str(x)) + errors_found
                                    invalid_records.append(errors_found)
                                else:
                                    valid_records.append(x)
                                    result_of_validation = "No Error Found"

                            check_plate = [re.sub(r'[^\w\s]', '', str(self.df.at[record, 'License Plate']).lower()) for record in valid_records]

                            repeated_plate = []
                            single_plate = []
                            for record in check_plate:
                                if record in single_plate:
                                    repeated_plate.append(record)                                    
                                else:
                                    single_plate.append(record)

                            not_unique_plate = []
                            for record in valid_records:
                                if re.sub(r'[^\w\s]', '', str(self.df.at[record, 'License Plate']).lower()) in repeated_plate:
                                    not_unique_plate.append(record)

                            if len(not_unique_plate) > 0:
                                for record in not_unique_plate:
                                    valid_records.remove(record)

                                warning_license_plate = not_unique_plate, repeated_plate

                                self.pop_warning(new_window, warning_license_plate, "not_unique_license_plate")

                            wrong_format_record = []
                            wrong_text_format = []
                            for record in valid_records:
                                date_to_check = str(self.df.at[record, "Year"])
                                pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format.append(date_to_check)
                                    wrong_format_record.append(record)

                            if len(wrong_text_format) > 0:
                                self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")
                                for record in wrong_format_record:
                                    valid_records.remove(record)

                            if len(valid_records) > 0:
                                result = self.check_employee_code(str(employee_code_entry.get()), False)
                                print(result)
                                if result == "valid":
                                    self.toggle_entry_colors(1, employee_code_entry)

                                    def handle_choice(option, valid_records):
                                        if option == "confirm":
                                            try:
                                                with self.flask_app.app_context():
                                                    db.create_all()
                                                    plate_already_in_db = []
                                                    for x in valid_records:
                                                        cleaned_license_plate = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'License Plate']).lower())
                                                        existing_license_plate = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_license_plate)).first()
                                                        if existing_license_plate:
                                                            plate_already_in_db.append(self.df.at[x, 'License Plate'])
                                                        else:
                                                            next_inspection_date=self.calculate_date(str(self.df.at[x, 'Year']))

                                                            current_day = datetime.now().day
                                                            current_month = datetime.now().month
                                                            current_year = datetime.now().year

                                                            if current_month == 2:
                                                                if current_day == 29:
                                                                    next_legalization = datetime(current_year + 1, current_month, current_day-1)
                                                                    print("The next legalization is scheduled for:", next_inspection.strftime("%Y-%m-%d"))
                                                                else:
                                                                    next_legalization = datetime(current_year + 1, current_month, current_day)
                                                                    print("The next legalization is scheduled for:", next_legalization.strftime("%Y-%m-%d"))
                                                            else:
                                                                next_legalization = datetime(current_year + 1, current_month, current_day)
                                                                print("The next legalization is scheduled for:", next_legalization.strftime("%Y-%m-%d"))

                                                            next_legalization_date = next_legalization.date()

                                                            if self.df.at[x, "Vehicle Type"].lower() == "cars":
                                                                car_instance = Vehicle(
                                                                    doors=int(self.df.at[x, "Doors"]),
                                                                    vehicle_type="cars",
                                                                    category=self.df.at[x, 'Category'].lower(),
                                                                    segment=self.df.at[x, 'Segment'].lower(),
                                                                    brand=self.df.at[x, 'Brand'].lower(),
                                                                    model=self.df.at[x, 'Model'],
                                                                    year=self.df.at[x, 'Year'],
                                                                    license_plate=cleaned_license_plate,
                                                                    seats=int(self.df.at[x, 'Seats']),
                                                                    wheels=int(self.df.at[x, "Number of Wheels"]),
                                                                    color=self.df.at[x, 'Color'].lower(),
                                                                    fuel=self.df.at[x, 'Fuel'].lower(),
                                                                    gearbox=self.df.at[x, 'Type of Gearbox'].lower(),
                                                                    photos=self.df.at[x, 'Vehicle Photos'],
                                                                    next_inspection=next_inspection_date,
                                                                    next_legalization=next_legalization_date,
                                                                    code_insertion=str(employee_code_entry.get())
                                                                )
                                                                db.session.add(car_instance)
                                                            else:
                                                                motorcycle_instance = Vehicle(
                                                                    doors=0,
                                                                    vehicle_type="motorcycles",
                                                                    category=self.df.at[x, 'Category'].lower(),
                                                                    segment=self.df.at[x, 'Segment'].lower(),
                                                                    brand=self.df.at[x, 'Brand'].lower(),
                                                                    model=self.df.at[x, 'Model'],
                                                                    year=self.df.at[x, 'Year'],
                                                                    license_plate=cleaned_license_plate,
                                                                    seats=int(self.df.at[x, 'Seats']),
                                                                    wheels=int(self.df.at[x, "Number of Wheels"]),
                                                                    color=self.df.at[x, 'Color'].lower(),
                                                                    fuel=self.df.at[x, 'Fuel'].lower(),
                                                                    gearbox=self.df.at[x, 'Type of Gearbox'].lower(),
                                                                    cc=self.df.at[x, 'Vehicle CC'],
                                                                    photos=self.df.at[x, 'Vehicle Photos'],
                                                                    next_inspection=next_inspection_date,
                                                                    next_legalization=next_legalization_date,
                                                                    code_insertion=str(employee_code_entry.get())
                                                                )
                                                                db.session.add(motorcycle_instance)

                                                    db.session.commit()
                                                    clear_entries()

                                                    if len(plate_already_in_db) > 0:
                                                        self.pop_warning(new_window, plate_already_in_db, "platealreadyindb")

                                            except OperationalError as e:
                                                warning = "Database is locked. Please close the Database and try again."
                                                self.pop_warning(new_window, warning, "databaselocked")
                                                db.session.rollback()
                                                print("Database is locked. Please try again later.")

                                        elif option == "cancel":
                                            print("User canceled")

                                    self.pop_warning(new_window, valid_records, "databvalidadd", lambda option: handle_choice(option, valid_records))
                                else:
                                    self.toggle_entry_colors(0, employee_code_entry)
                                    self.pop_warning(new_window, result, "wrongemployeecode")

                            if len(invalid_records) > 0:
                                self.pop_warning(new_window, invalid_records, "databinvalidadd")

                    # Allows adding new elements to the table
                    def add_record():
                        must_be_number = {
                                'Seats': (seats_entry.get(), seats_entry),
                                'Number of Wheels': (wheels_entry.get(), wheels_entry),
                                'Doors': (doors_entry.get(), doors_entry)
                            }

                        must_not_have_number = {
                                'Brand': (brand_entry.get(), brand_entry),
                                'Color': (color_entry.get(), color_entry)
                            }

                        must_be_defined = {
                                'Vehicle Type': (selected_vehicle_type.get(), vehicle_type_combobox),
                                'Segment': (selected_segment.get(), segment_combobox),
                                'Category': (selected_category.get(), category_combobox),
                                'Fuel': (selected_fuel.get(), fuel_combobox),
                                'Type of Gearbox': (selected_gearbox.get(), gearbox_combobox),
                                'Vehicle CC': (selected_cc.get(), cc_combobox)
                        }

                        must_not_be_empty = {
                             
                                'Seats': (seats_entry.get(), seats_entry),
                                'Number of Wheels': (wheels_entry.get(), wheels_entry),
                                'Doors': (doors_entry.get(), doors_entry),
                                'Model': (model_entry.get(), model_entry),                               
                                'Color': (color_entry.get(), color_entry),
                                'Brand': (brand_entry.get(), brand_entry),
                                'License Plate': (license_plate_entry.get(), license_plate_entry),
                                'Year': (year_entry.get(), year_entry)
                            }


                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        if hasattr(self, 'photo_paths'):
                            self.toggle_button_colors(1, select_photos_button)
                        else:
                            is_empty.append("Photos")

                        date_to_check = str(year_entry.get())
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                        if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                            result_of_validation = "Error Found"
                        else:
                            result_of_validation = "No Error Found"

                        if result_of_validation == "No Error Found":

                            def handle_choice(option, possible_new_record):
                                if option == "confirm":
                                    new_record = pd.DataFrame(possible_new_record)
                                    self.df = pd.concat([self.df, new_record], ignore_index=True)
                                    clear_entries()
                                    self.df.reset_index(drop=True, inplace=True)

                                    refresh_tree()
                                elif option == "cancel":
                                    print("User canceled")

                            possible_new_record = {
                            'Vehicle Type': [selected_vehicle_type.get()],
                            'Category': [selected_category.get()],
                            'Segment': [selected_segment.get()],
                            'Fuel': [selected_fuel.get()],
                            'Type of Gearbox': [selected_gearbox.get()],
                            'Brand': [brand_entry.get()],
                            'Model': [model_entry.get()],
                            'License Plate': [license_plate_entry.get()],
                            'Color': [color_entry.get()],
                            'Year': [year_entry.get()],
                            'Seats': [int(seats_entry.get())],
                            'Doors': [int(doors_entry.get())],
                            'Vehicle CC': [selected_cc.get()],
                            'Number of Wheels': [int(wheels_entry.get())],
                            'Vehicle Photos': self.photo_paths
                            }

                            self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                        else:
                            if str(year_entry.get()) != "":
                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format = str(year_entry.get())
                                    self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                            for key in must_not_be_empty:
                                if key in is_empty:
                                    entry_value = must_not_be_empty[key][1]
                                    self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    if key == "Year":
                                        year_entry.config(readonlybackground="darkred")
                                else:
                                    self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                            for key in must_be_defined:
                                if key in not_defined:
                                    combobox_value = must_be_defined[key][1]
                                    self.toggle_combo_text(0, must_be_defined[key][1])
                                else:
                                    self.toggle_combo_text(1, must_be_defined[key][1])

                            for key in must_not_have_number:
                                if key in not_alpha or key in is_empty:
                                    entry_value = must_not_have_number[key][1]
                                    self.toggle_entry_colors(0, must_not_have_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_not_have_number[key][1])

                            if "Photos" in is_empty:
                                self.toggle_button_colors(0, select_photos_button)
                                self.red_bind_hover_effects(select_photos_button)
                            else:
                                self.toggle_button_colors(1, select_photos_button)
                                self.bind_hover_effects(select_photos_button)

                            for key in must_be_number:
                                if key in not_num or key in is_empty:
                                    entry_value = must_be_number[key][1]
                                    self.toggle_entry_colors(0, must_be_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_be_number[key][1])

                            errors_adding = []
                            for error_list in errors_found:
                                if len(error_list) > 1:
                                    errors_adding.append(error_list)

                            if len(errors_adding) > 0:
                                self.pop_warning(new_window, errors_adding, "addrecvalidation")                        

                    # Removes all elements from the table
                    def remove_all():
                        for record in treeview.get_children():
                            x = treeview.index(record)
                            treeview.delete(record)
                            print(x)
                            self.df.drop(index=x, inplace=True)
                            print(self.df)
                            self.df.reset_index(drop=True, inplace=True)

                    # Opens the photo viewing window of the selected element
                    def selected_vehicle_photos():
                        selected_items = treeview.selection()
                        print(selected_items)
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            print(f"This is X: {type(x)}")
                            photos_of_selected = str(self.df.at[x, "Vehicle Photos"])

                            if photos_of_selected.lower() != "nan":
                                self.verify_photo_path(photos_of_selected)

                                if len(valid_photo_type) > 0:
                                    print(valid_photo_type)
                                    if len(valid_photo_paths) > 0:
                                        def handle_photo_viewer_result(result, updated_photos):
                                            if result == "confirm":
                                                print("Updated photos:", updated_photos)
                                                self.df.at[x, 'Vehicle Photos'] = updated_photos
                                            elif result == "cancel":
                                                print("User cancelled changes")
                                        updated_photos = []
                                        self.photo_viewer(new_window, valid_photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos)
                                        print(f"Photos after view: {self.df.at[x, 'Vehicle Photos']}")
                                    if len(invalid_photo_paths) > 0:
                                        self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                        self.toggle_button_colors(0, selected_vehicle_photos_button)
                                print(invalid_photo_type)
                                for path in invalid_photo_type:
                                    if path == "":
                                        invalid_photo_type.remove(path)
                                if len(invalid_photo_type) > 0:
                                    self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                                    self.toggle_button_colors(0, selected_vehicle_photos_button)
                            else:
                                x += 1
                                self.pop_warning(new_window, str(x), "nanselectedphoto")
                                self.toggle_button_colors(0, selected_vehicle_photos_button)
                        else:
                            warning = "Must select a record to see photos"
                            self.pop_warning(new_window, warning, "noselectedtoseephotos")

                    refresh_tree()

                    treeview.pack(expand=True, fill="both")

                    add_record_button = Button(edit_treeview_frame, text="Add Record to Data Frame", fg="white",
                                               bg="black",
                                               command=add_record)
                    add_record_button.grid(row=0, column=0, padx=5, pady=3)
                    self.bind_hover_effects(add_record_button)

                    add_record_database = Button(edit_treeview_frame, text="Add Selected Record(s) to Database", fg="white",
                                               bg="darkgreen",
                                               command=add_selected_to_database)
                    add_record_database.grid(row=1, column=0, columnspan=7, padx=10, pady=5)
                    self.green_bind_hover_effects(add_record_database)

                    update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                           command=update_record)
                    update_button.grid(row=0, column=1, padx=5, pady=3)
                    self.bind_hover_effects(update_button)

                    clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                                  command=clear_entries)
                    clear_entries_button.grid(row=0, column=2, padx=5, pady=3)
                    self.bind_hover_effects(clear_entries_button)

                    selected_vehicle_photos_button = Button(edit_treeview_frame, text="See Selected Vehicle Photos",
                                                            fg="white",
                                                            bg="black", command=selected_vehicle_photos)
                    selected_vehicle_photos_button.grid(row=0, column=3, padx=5, pady=3)
                    self.bind_hover_effects(selected_vehicle_photos_button)

                    remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                                    bg="black", command=remove_selected)
                    remove_selected_button.grid(row=0, column=4, padx=5, pady=3)
                    self.bind_hover_effects(remove_selected_button)

                    remove_all_button = Button(edit_treeview_frame, text="Remove All Records", fg="white",
                                               bg="black", command=remove_all)
                    remove_all_button.grid(row=0, column=5, padx=5, pady=3)
                    self.bind_hover_effects(remove_all_button)

                    refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                               bg="black", command=refresh_tree)
                    refresh_tree_button.grid(row=0, column=6, padx=5, pady=3)
                    self.bind_hover_effects(refresh_tree_button)

                    treeview.bind("<ButtonRelease-1>", select_record)

                else:
                    missing_heading = [head for head in vehicle_headings_lowercase if head not in vehicle_file_headings]
                    unmatched_heading = [head for head in vehicle_file_headings if head not in vehicle_headings_lowercase]
                    missing_unmatched_head = missing_heading, unmatched_heading

                    if len(missing_heading) > 0 and len(unmatched_heading) > 0:
                        print(f"Missing Heading: {missing_heading} \nUnmatched Heading: {unmatched_heading}")
                        self.pop_warning(new_window, missing_unmatched_head, "missingheadunmatched" )
                    elif len(missing_heading) > 0 and len(unmatched_heading) == 0:
                        print(f"Missing Heading: {missing_heading}")
                        self.pop_warning(new_window, missing_heading, "missingheading")
                    elif len(missing_heading) == 0 and len(unmatched_heading) > 0:
                        print(f"Unmatched Heading: {unmatched_heading}")
                        self.pop_warning(new_window, unmatched_heading, "unmatchedheading")

            else:
                print("No file path selected")

        # Function to check if a file has been uploaded
        def check_if_df():
            if hasattr(self, 'df'):
                check_vehicle_file_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_files_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_check_button.configure(image=self.check_files_image)
            else:
                print("No file selected")

        # Function to check if a photo has been uploaded
        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))

                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                print("No file selected")
                see_photos_button.configure(state=tk.DISABLED)
                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))
                reload_show_photos_button.configure(image=self.update_photos_button_image)

        # Function to add vehicles to the database table without using a data file
        def add_vehicle_db():
            must_be_number = {
                    'Seats': (seats_entry.get(), seats_entry),
                    'Number of Wheels': (wheels_entry.get(), wheels_entry),
                    'Doors': (doors_entry.get(), doors_entry)
                }

            must_not_have_number = {
                    'Brand': (brand_entry.get(), brand_entry),
                    'Color': (color_entry.get(), color_entry)
                }

            must_be_defined = {
                    'Vehicle Type': (selected_vehicle_type.get(), vehicle_type_combobox),
                    'Segment': (selected_segment.get(), segment_combobox),
                    'Category': (selected_category.get(), category_combobox),
                    'Fuel': (selected_fuel.get(), fuel_combobox),
                    'Type of Gearbox': (selected_gearbox.get(), gearbox_combobox),
                    'Vehicle CC': (selected_cc.get(), cc_combobox)
            }

            must_not_be_empty = {
                 
                    'Seats': (seats_entry.get(), seats_entry),
                    'Number of Wheels': (wheels_entry.get(), wheels_entry),
                    'Doors': (doors_entry.get(), doors_entry),
                    'Model': (model_entry.get(), model_entry),                               
                    'Color': (color_entry.get(), color_entry),
                    'Brand': (brand_entry.get(), brand_entry),
                    'License Plate': (license_plate_entry.get(), license_plate_entry),
                    'Year': (year_entry.get(), year_entry)
                }

            if selected_vehicle_type.get() == "Motorcycles":
                del must_not_be_empty['Doors']

            self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

            if hasattr(self, 'photo_paths'):
                self.toggle_button_colors(1, select_photos_button)
            else:
                is_empty.append("Photos")

            date_to_check = str(year_entry.get())
            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

            if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False:  
                result_of_validation = "Error Found"
            else:
                result_of_validation = "No Error Found"

            if result_of_validation == "No Error Found":

                result = self.check_employee_code(str(employee_code_entry.get()), False)
                if result == "valid":
                    self.toggle_entry_colors(1, employee_code_entry)

                    combo = [vehicle_type_combobox, category_combobox, segment_combobox, fuel_combobox, gearbox_combobox]
                    for box in combo:
                        self.toggle_combo_text(1, box)

                    entries = [brand_entry, model_entry, color_entry, license_plate_entry, wheels_entry, seats_entry, doors_entry]
                    for entry in entries:
                        self.toggle_entry_colors(1, entry)

                    year_entry.config(readonlybackground="#313131")

                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    def handle_choice(option, possible_new_record):
                        if option == "confirm":
                            try:
                                with self.flask_app.app_context():
                                    db.create_all()
                                    
                                    cleaned_license_plate = re.sub(r'[^\w\s]', '', str(license_plate_entry.get()).lower())
                                    existing_license_plate = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_license_plate)).first()

                                    if existing_license_plate:
                                        self.pop_warning(new_window, cleaned_license_plate, "platealreadyindatab")
                                    else:
                                        next_inspection_date=self.calculate_date(year_entry.get())

                                        current_day = datetime.now().day
                                        current_month = datetime.now().month
                                        current_year = datetime.now().year

                                        if current_month == 2:
                                            if current_day == 29:
                                                next_legalization = datetime(current_year + 1, current_month, current_day-1)
                                                print("The next legalization is scheduled for:", next_inspection.strftime("%Y-%m-%d"))
                                            else:
                                                next_legalization = datetime(current_year + 1, current_month, current_day)
                                                print("The next legalization is scheduled for:", next_legalization.strftime("%Y-%m-%d"))

                                        else:
                                            next_legalization = datetime(current_year + 1, current_month, current_day)
                                            print("The next legalization is scheduled for:", next_legalization.strftime("%Y-%m-%d"))

                                        next_legalization_date = next_legalization.date()

                                        if selected_vehicle_type.get().lower() == "cars":
                                            car_instance = Vehicle(
                                                doors=int(doors_entry.get()),
                                                vehicle_type="cars",
                                                category=str(selected_category.get()).lower(),
                                                segment=str(selected_segment.get()).lower(),
                                                brand=str(brand_entry.get()).lower(),
                                                model=str(model_entry.get()).lower(),
                                                year=year_entry.get(),
                                                license_plate=cleaned_license_plate,
                                                seats=int(seats_entry.get()),
                                                wheels=int(wheels_entry.get()),
                                                color=str(color_entry.get()).lower(),
                                                fuel=str(selected_fuel.get()).lower(),
                                                gearbox=str(selected_gearbox.get()).lower(),
                                                photos=self.photo_paths,
                                                next_inspection=next_inspection_date,
                                                next_legalization=next_legalization_date,
                                                code_insertion=str(employee_code_entry.get())
                                            )
                                            db.session.add(car_instance)
                                        else:
                                            motorcycle_instance = Vehicle(
                                                doors=0,
                                                vehicle_type="motorcycles",
                                                category=str(selected_category.get()).lower(),
                                                segment=str(selected_segment.get()).lower(),
                                                brand=str(brand_entry.get()).lower(),
                                                model=str(model_entry.get()).lower(),
                                                year=year_entry.get(),
                                                license_plate=cleaned_license_plate,
                                                seats=int(seats_entry.get()),
                                                wheels=int(wheels_entry.get()),
                                                color=str(color_entry.get()).lower(),
                                                fuel=str(selected_fuel.get()).lower(),
                                                gearbox=str(selected_gearbox.get()).lower(),
                                                cc=str(selected_cc.get()),
                                                photos=self.photo_paths,
                                                next_inspection=next_inspection_date,
                                                next_legalization=next_legalization_date,
                                                code_insertion=str(employee_code_entry.get())
                                            )
                                            db.session.add(motorcycle_instance)

                                        db.session.commit()

                                        entries = [license_plate_entry, employee_code_entry, brand_entry, model_entry, seats_entry, doors_entry, color_entry, wheels_entry]
                                        for entry in entries:
                                            entry.delete(0, END)
                                            self.toggle_entry_colors(1, entry)

                                        read_only_entries = [year_entry, doors_entry]
                                        for entry in read_only_entries:
                                            entry.config(state=tk.NORMAL)
                                            entry.delete(0, tk.END)
                                            entry.config(state="readonly", readonlybackground="#313131")


                                        combos = [[gearbox_combobox, gearbox_types],[fuel_combobox, fuels], [segment_combobox, segments_cars], [category_combobox, categories],
                                                [vehicle_type_combobox, vehicle_types], [cc_combobox, cc_list]]
                                        for combo in combos:
                                            self.toggle_combo_text(1, combo[0])
                                            combo[0].set(combo[1][0])

                                        del self.photo_paths

                                        check_if_photos()
                            except OperationalError as e:
                                warning = "Database is locked. Please close the Database and try again."
                                self.pop_warning(new_window, warning, "databaselocked")
                                db.session.rollback()
                                print("Database is locked. Please try again later.")

                        elif option == "cancel":
                            print("User canceled")

                    possible_new_record = {
                    'Vehicle Type': [selected_vehicle_type.get()],
                    'Category': [selected_category.get()],
                    'Segment': [selected_segment.get()],
                    'Fuel': [selected_fuel.get()],
                    'Type of Gearbox': [selected_gearbox.get()],
                    'Brand': [brand_entry.get()],
                    'Model': [model_entry.get()],
                    'License Plate': [license_plate_entry.get()],
                    'Color': [color_entry.get()],
                    'Year': [year_entry.get()],
                    'Seats': [int(seats_entry.get())],
                    'Doors': [int(doors_entry.get())],
                    'Vehicle CC': [selected_cc.get()],
                    'Number of Wheels': [int(wheels_entry.get())],
                    'Vehicle Photos': self.photo_paths
                    }

                    self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                else:
                    self.toggle_entry_colors(0, employee_code_entry)
                    self.pop_warning(new_window, result, "wrongemployeecode")
            else:
                if str(year_entry.get()) != "":
                    if bool(re.match(pattern, date_to_check)) == False:
                        wrong_text_format = str(year_entry.get())
                        self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                for key in must_not_be_empty:
                    if key in is_empty:
                        entry_value = must_not_be_empty[key][1]
                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                        if key == "Year":
                            year_entry.config(readonlybackground="darkred")
                    else:
                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                for key in must_be_defined:
                    if key in not_defined:
                        combobox_value = must_be_defined[key][1]
                        self.toggle_combo_text(0, must_be_defined[key][1])
                    else:
                        self.toggle_combo_text(1, must_be_defined[key][1])

                for key in must_not_have_number:
                    if key in not_alpha or key in is_empty:
                        entry_value = must_not_have_number[key][1]
                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_not_have_number[key][1])

                if "Photos" in is_empty:
                    self.toggle_button_colors(0, select_photos_button)
                    self.red_bind_hover_effects(select_photos_button)
                else:
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                for key in must_be_number:
                    if key in not_num or key in is_empty:
                        entry_value = must_be_number[key][1]
                        self.toggle_entry_colors(0, must_be_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_be_number[key][1])

                errors_adding = []
                for error_list in errors_found:
                    if len(error_list) > 1:
                        errors_adding.append(error_list)

                if len(errors_adding) > 0:
                    self.pop_warning(new_window, errors_adding, "addrecvalidation")

        insert_vehicle_frame = tk.Frame(new_window)
        insert_vehicle_frame.configure(bg="black")
        insert_vehicle_frame.pack(pady=(0,10))

        upload_vehicle_file_button = tk.Button(insert_vehicle_frame, text="Upload Vehicle File", width=15,
                                               borderwidth=2,
                                               fg="white", bg="black", command=lambda: self.load_data(new_window))
        upload_vehicle_file_button.grid(row=0, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(upload_vehicle_file_button)

        check_vehicle_file_button = tk.Button(insert_vehicle_frame, text="Check Data", width=15, borderwidth=2,
                                              fg="white", bg="black", state=tk.DISABLED, command=check_data)
        check_vehicle_file_button.grid(row=0, column=4, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_vehicle_file_button)

        update_files_button_image_path = resource_path('resources/update.png')
        self.update_files_button_image = ImageTk.PhotoImage(Image.open(update_files_button_image_path))
        reload_check_button = tk.Button(insert_vehicle_frame, image=self.update_files_button_image, command=check_if_df,
                                        borderwidth=0, highlightthickness=0)
        reload_check_button.grid(row=0, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_check_button)

        vehicle_type_label = tk.Label(insert_vehicle_frame, text="Vehicle Type:",
                                      font=("Helvetica", 10), fg="white", bg="black")
        vehicle_type_label.grid(row=0, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        vehicle_types = ["Not Defined", "Cars", "Motorcycles"]
        selected_vehicle_type = tk.StringVar()
        vehicle_type_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_vehicle_type,
                                             values=vehicle_types, state="readonly", justify="center", height=4,
                                             width=20)
        vehicle_type_combobox.grid(row=0, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        vehicle_type_combobox.set(vehicle_types[0]) 

        category_label = tk.Label(insert_vehicle_frame, text="Category:",
                                  font=("Helvetica", 10), fg="white", bg="black")
        category_label.grid(row=1, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        categories = ["Not Defined", "Gold", "Silver", "Economic"]
        selected_category = tk.StringVar()
        category_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_category,
                                         values=categories, state="readonly", justify="center", height=4, width=20)
        category_combobox.grid(row=1, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        category_combobox.set(categories[0]) 

        segment_label = tk.Label(insert_vehicle_frame, text="Segment:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        segment_label.grid(row=2, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        segments_cars = ["Not Defined", "Microcar", "Subcompact", "Compact", "Midsize", "Full-size", "SUV",
                         "Crossover", "Multi-Purpose Vehicle", "Convertible/Cabriolet", "Coupe",
                         "Roadster", "Hot Hatch", "Sports Car"]

        segments_motorcycles = ["Not Defined", "Sport Bikes", "Cruisers", "Touring Bikes", "Naked Bikes",
                                "Adventure Bikes", "Dirt Bikes", "Scooters",
                                "Electric Motorcycles", "Cafe Racers", "Choppers",
                                "Bobbers", "Trikes"]

        selected_segment = tk.StringVar()

        segment_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_segment,
                                        values=segments_cars, state="readonly", justify="center", height=4, width=20)
        segment_combobox.grid(row=2, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        segment_combobox.set(segments_cars[0])  

        doors_label = tk.Label(insert_vehicle_frame, text="Doors:",
                               font=("Helvetica", 10), fg="white", bg="black")
        doors_label.grid(row=3, column=4, pady=5, padx=(40, 5), sticky=tk.E)

        doors_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        doors_entry.grid(row=3, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        employee_code_label = tk.Label(insert_vehicle_frame, text="Employee Code:",
                          font=("Helvetica", 10), fg="white", bg="black")
        employee_code_label.grid(row=4, column=4, pady=5, padx=(40, 5), sticky=tk.E)

        employee_code_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        employee_code_entry.grid(row=4, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        # Updates the segment list based on the selected vehicle type
        def update_segment_options(event):
            selected_type = selected_vehicle_type.get()
            if selected_type == "Cars":
                segment_combobox['values'] = segments_cars
                cc_combobox['values'] = cc_not_relevant
                selected_segment.set(segments_cars[0])
                selected_cc.set(cc_not_relevant[1])
                cc_combobox.config(state="disabled")
                doors_entry.config(state=tk.NORMAL)
                doors_entry.delete(0, tk.END)
            elif selected_type == "Motorcycles":
                segment_combobox['values'] = segments_motorcycles
                cc_combobox['values'] = cc_list
                selected_segment.set(segments_motorcycles[0])
                cc_combobox.config(state="readonly")
                selected_cc.set(cc_list[0])
                doors_entry.delete(0, tk.END)
                doors_entry.insert(0, 0)
                doors_entry.config(state="readonly", readonlybackground="#313131")

        vehicle_type_combobox.bind("<<ComboboxSelected>>", update_segment_options)

        fuel_label = tk.Label(insert_vehicle_frame, text="Fuel:",
                              font=("Helvetica", 10), fg="white", bg="black")
        fuel_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        fuels = ["Not Defined", "Gasoline(Petrol)", "Diesel", "Electricity", "Hybrid", "Plug-in Hybrid (PHEV)",
                 "Compressed Natural Gas (CNG)", "Liquefied Petroleum Gas (LPG)",
                 "Hydrogen Fuel Cell", "Biodiesel", "Flex-Fuel"]
        selected_fuel = tk.StringVar()
        fuel_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_fuel,
                                     values=fuels, state="readonly", justify="center", height=4, width=20)
        fuel_combobox.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        fuel_combobox.set(fuels[0])

        gearbox_label = tk.Label(insert_vehicle_frame, text="Type of Gearbox:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        gearbox_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        gearbox_types = ["Not Defined", "Manual", "Semi-Automatic", "Automatic"]
        selected_gearbox = tk.StringVar()
        gearbox_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_gearbox,
                                        values=gearbox_types, state="readonly", justify="center", height=4, width=20)
        gearbox_combobox.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        gearbox_combobox.set(gearbox_types[0]) 

        cc_label = tk.Label(insert_vehicle_frame, text="Vehicle CC:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        cc_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        cc_not_relevant = ["Not Defined", "Not Relevant"]
        cc_list = ["Not Defined", "<= 50", "<= 50 (11kw)", "<= 50 (35kw)", "51 - 125", "51 - 125 (11kw)", "51 - 125 (35kw)", "126 - 500", "126 - 500 (35kw)", "501 - 1000", "501 - 1000 (35kw)", ">= 1000", ">= 1000 (35kw)"]
        selected_cc = tk.StringVar()
        cc_combobox = ttk.Combobox(insert_vehicle_frame, textvariable=selected_cc,
                                        values=cc_list, state="readonly", justify="center", height=4, width=20)
        cc_combobox.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        cc_combobox.set(cc_list[0]) 

        year_button = tk.Button(insert_vehicle_frame, text="Select Vehicle Date:", width=20, borderwidth=2,
            fg="white", bg="black", command=lambda: self.datepicker(new_window, year_entry, "vehicle_date"))

        year_button.grid(row=6, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        year_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        year_entry.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        brand_label = tk.Label(insert_vehicle_frame, text="Brand:",
                               font=("Helvetica", 10), fg="white", bg="black")
        brand_label.grid(row=1, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        brand_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        brand_entry.grid(row=1, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        model_label = tk.Label(insert_vehicle_frame, text="Model:",
                               font=("Helvetica", 10), fg="white", bg="black")
        model_label.grid(row=2, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        model_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        model_entry.grid(row=2, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        color_label = tk.Label(insert_vehicle_frame, text="Color:",
                               font=("Helvetica", 10), fg="white", bg="black")
        color_label.grid(row=3, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        color_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        color_entry.grid(row=3, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        license_plate_label = tk.Label(insert_vehicle_frame, text="License Plate:",
                                       font=("Helvetica", 10), fg="white", bg="black")
        license_plate_label.grid(row=4, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        license_plate_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        license_plate_entry.grid(row=4, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        wheels_label = tk.Label(insert_vehicle_frame, text="Number of Wheels:",
                                font=("Helvetica", 10), fg="white", bg="black")
        wheels_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        wheels_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        wheels_entry.grid(row=1, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        seats_label = tk.Label(insert_vehicle_frame, text="Seats:",
                               font=("Helvetica", 10), fg="white", bg="black")
        seats_label.grid(row=2, column=4, pady=5, padx=(40, 5), sticky=tk.E)

        seats_entry = tk.Entry(insert_vehicle_frame, bd=2, width=10)
        seats_entry.grid(row=2, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        select_photos_button = tk.Button(insert_vehicle_frame, text="Select Vehicle Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=5, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(select_photos_button)

        # If the user deletes any photo from the list of photos uploaded, this function updates the list  
        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                print("User confirmed changes")
                print("Updated photos:", updated_photos)
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(insert_vehicle_frame, text="See Vehicle Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=5, column=4, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(insert_vehicle_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=5, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)

        add_vehicle_button = tk.Button(insert_vehicle_frame, text="Add Vehicle", width=15, borderwidth=2,
                                           fg="white", bg="#004d00", command=add_vehicle_db)
        add_vehicle_button.grid(row=6, column=4, columnspan=2, pady=5, padx=5, sticky="w")
        self.green_bind_hover_effects(add_vehicle_button)

    # Section to insert clients into the database
    def insert_clients_section(self, new_window):
        if hasattr(self, 'df'):
            del self.df
        else:
            pass

        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        file_section_info = "Upload a Excel/CSV file by pressing the 'Upload Client File' button"
        file_section_info_label = tk.Label(treeFrame, text=file_section_info, font=("Helvetica", 10),
                                           fg="white", bg="black")
        file_section_info_label.pack(pady=(140, 0))

        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)

        edit_treeview_frame.configure(bg="black")

        def check_data():

            if self.df is not None and not self.df.empty:
                client_file_headings = []
                for column in self.df.columns:
                    client_file_headings.append(column.lower())

                client_headings = ['Full Name', 'Date of Birth', 'Phone Number Indicative', 'Phone Number', 'Email', 'Address', 'Nationality', 'Identification Type', 'ID/Passport Number',
                                    'Credit Card Number', 'Billing Address', 'Preferred Car Type', 'Preferred Motorcycle Type', 'Motorcycle License', 'Emergency Contact Name',
                                    'Emergency Contact Indicative', 'Emergency Contact Number', 'Client ID Photos']

                client_headings_lowercase = [head.lower() for head in client_headings]

                client_file_headings_check = all(
                    head in client_file_headings for head in client_headings_lowercase)

                if client_file_headings_check and len(client_file_headings) == len(client_headings):
                    add_client_button.grid_forget()

                    for widget in treeFrame.winfo_children():
                        widget.destroy()

                    treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeFrame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    def verify_data():
                        for index, row in self.df.iterrows():
                            not_num = []
                            must_be_number = {
                                'Phone Number': row['Phone Number'],
                                'Credit Card Number': row['Credit Card Number'],
                                'Emergency Contact Number': row['Emergency Contact Number']                           
                            }

                            for column_num, value_num in must_be_number.items():
                                try:
                                    int(value_num)
                                except ValueError:
                                    not_num.append(value_num)

                            not_alpha = []
                            must_not_have_number = {
                                'Full Name': str(row['Full Name']),
                                'Identification Type': str(row['Identification Type']),
                                'Preferred Car Type': str(row['Preferred Car Type']),
                                'Preferred Motorcycle Type': str(row['Preferred Motorcycle Type']),
                                'Emergency Contact Name': str(row['Emergency Contact Name'])
                            }

                            for column_word, value_word in must_not_have_number.items():
                                clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                                if all(char.isalpha() for char in clean_value_word):
                                    pass
                                else:
                                    not_alpha.append(value_word)

                            is_empty = []
                            all_data = {
                                'Date of Birth': str(row['Date of Birth']),
                                'Phone Number Indicative': str(row['Phone Number Indicative']),
                                'Phone Number': str(row['Phone Number']),
                                'ID/Passport Number': str(row['ID/Passport Number']),
                                'Credit Card Number': str(row['Credit Card Number']),
                                'Emergency Contact Indicative': str(row['Emergency Contact Indicative']),
                                'Emergency Contact Number': str(row['Emergency Contact Number']),
                                'Full Name': str(row['Full Name']),
                                'Identification Type': str(row['Identification Type']),
                                'Preferred Car Type': str(row['Preferred Car Type']),
                                'Preferred Motorcycle Type': str(row['Preferred Motorcycle Type']),
                                'Emergency Contact Name': str(row['Emergency Contact Name']),
                                'Email': str(row['Email']),
                                'Address': str(row['Address']),
                                'Billing Address': str(row['Billing Address']),
                                'Motorcycle License': str(row['Motorcycle License']),
                                'Client ID Photos': str(row['Client ID Photos'])
                            }

                            for column_all, value_all in all_data.items():
                                if value_all == 'nan':
                                    is_empty.append(value_all)
                                else:
                                    pass

                            not_defined = []
                            must_be_defined = {
                                'Identification Type': (str(row['Identification Type']), id_types),
                                'Preferred Car Type': (str(row['Preferred Car Type']), car_types),
                                'Preferred Motorcycle Type': (str(row['Preferred Motorcycle Type']), moto_types),
                                'Motorcycle License': (str(row['Motorcycle License']), license_class),
                                'Nationality': (str(row['Nationality']), nationalities)
                            }

                            for column_defined, value_defined in must_be_defined.items():
                                if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                                    not_defined.append(value_defined)
                                else:
                                    pass

                            errors_found = not_num, not_alpha, is_empty, not_defined

                            possible_photo_path_list = str(row['Client ID Photos'])
                        
                            self.verify_photo_path(possible_photo_path_list)
                            if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                                pass

                            if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                is_empty.append("Photos")

                            date_to_check = str(row['Date of Birth'])
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            if any(len(error_list) > 0 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False:
                                result_of_validation = "Error Found"
                                self.change_row_color(treeview, index, "darkred")
                            else:
                                self.change_row_color(treeview, index, "#313131")
                                result_of_validation = "No Error Found"

                    def refresh_tree():
                        treeview.delete(*treeview.get_children())

                        def convert_to_datetime(date_string):
                            try:
                                return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                            except ValueError:
                                return date_string

                        self.df['Date of Birth'] = self.df['Date of Birth'].apply(convert_to_datetime)

                        treeview["column"] = list(self.df)
                        treeview["show"] = "headings"

                        for column in treeview["column"]:
                            treeview.heading(column, text=column)
                            treeview.column(column, anchor="center")


                        columns_to_int = ['Phone Number', 'Credit Card Number', 'Emergency Contact Number', 'Phone Number Indicative', 'Emergency Contact Indicative' ]

                        for column in columns_to_int:
                            try:
                                self.df[column] = self.df[column].fillna(0).astype('int64')
                                self.df[column] = self.df[column].replace(0, 'nan')
                            except ValueError:
                                pass              
                           
                        df_rows = self.df.to_numpy().tolist()
                        for row in df_rows:
                            treeview.insert("", "end", values=row)

                        for col in treeview["columns"]:
                            heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                            
                            max_width = max(
                                tkFont.Font().measure(str(treeview.set(item, col)))
                                for item in treeview.get_children("")
                            )
                            
                            column_width = max(heading_width, max_width) + 20 
                            
                            treeview.column(col, width=column_width, minwidth=column_width)

                        treeview.column("Client ID Photos", width=120, minwidth=120)

                        treeview.update_idletasks()

                        verify_data()

                    def clear_entries():
                        entries = [p_n_indicative_entry, employee_code_entry, p_em_indicative_entry, full_name_entry, phone_entry, email_entry, address_entry, id_number_entry, credit_card_entry, billing_address_entry,
                                    emergency_name_entry, emergency_phone_entry]
                        for entry in entries:
                            entry.delete(0, END)
                            self.toggle_entry_colors(1, entry)

                        read_only_entries = [dob_entry]
                        for entry in read_only_entries:
                            entry.config(state=tk.NORMAL)
                            entry.delete(0, tk.END)
                            entry.config(state="readonly", readonlybackground="#313131")

                        combos = [[id_type_combobox, id_types],[car_type_combobox, car_types], [moto_type_combobox, moto_types], [license_class_combobox, license_class], [nation_combobox, nationalities]]
                        for combo in combos:
                            self.toggle_combo_text(1, combo[0])
                            combo[0].set(combo[1][0])

                        if hasattr(self, 'photo_paths'):
                            del self.photo_paths
                        see_photos_button.configure(state=tk.DISABLED)

                        reload_show_photos_button.configure(image=self.update_photos_button_image)

                    def select_record(e):
                        clear_entries()

                        selected_items = treeview.selection()

                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])

                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                            type_id = str(self.df.at[x, "Identification Type"]).lower()

                            id_type_combobox.set(id_types[0])  
                            mapping = {t.lower(): id_types[i] for i, t in enumerate(id_types)}
                            id_type_combobox.set(mapping.get(type_id, mapping["not defined"]))

                            if id_type_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, id_type_combobox)
                            else:
                                self.toggle_combo_text(1, id_type_combobox)

                            p_car = str(self.df.at[x, "Preferred Car Type"]).lower()

                            car_type_combobox.set(car_types[0])  
                            mapping = {c.lower(): car_types[i] for i, c in enumerate(car_types)}
                            car_type_combobox.set(mapping.get(p_car, mapping["not defined"]))

                            if car_type_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, car_type_combobox)
                            else:
                                self.toggle_combo_text(1, car_type_combobox)

                            p_moto = str(self.df.at[x, "Preferred Motorcycle Type"]).lower()

                            moto_type_combobox.set(moto_types[0])
                            mapping = {m.lower(): moto_types[i] for i, m in enumerate(moto_types)}
                            moto_type_combobox.set(mapping.get(p_moto, mapping["not defined"]))

                            if moto_type_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, moto_type_combobox)
                            else:
                                self.toggle_combo_text(1, moto_type_combobox)

                            license = str(self.df.at[x, "Motorcycle License"]).lower()

                            license_class_combobox.set(license_class[0]) 
                            mapping = {c.lower(): license_class[i] for i, c in enumerate(license_class)}
                            license_class_combobox.set(mapping.get(license, mapping["not defined"]))

                            if license_class_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, license_class_combobox)
                            else:
                                self.toggle_combo_text(1, license_class_combobox)

                            nation = str(self.df.at[x, 'Nationality']).lower()

                            nation_combobox.set(nationalities[0]) 
                            mapping = {n.lower(): nationalities[i] for i, n in enumerate(nationalities)}
                            nation_combobox.set(mapping.get(nation, mapping["not defined"]))

                            if nation_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, nation_combobox)
                            else:
                                self.toggle_combo_text(1, nation_combobox)

                            full_name_entry.insert(0, self.df.at[x, "Full Name"])
                            phone_entry.insert(0, self.df.at[x, "Phone Number"])
                            email_entry.insert(0, self.df.at[x, "Email"])
                            address_entry.insert(0, self.df.at[x, "Address"])
                            id_number_entry.insert(0, self.df.at[x, "ID/Passport Number"])
                            credit_card_entry.insert(0, self.df.at[x, "Credit Card Number"])
                            billing_address_entry.insert(0, self.df.at[x, "Billing Address"])
                            emergency_name_entry.insert(0, self.df.at[x, "Emergency Contact Name"])
                            emergency_phone_entry.insert(0, self.df.at[x, "Emergency Contact Number"])
                            p_n_indicative_entry.insert(0, self.df.at[x, "Phone Number Indicative"])
                            p_em_indicative_entry.insert(0, self.df.at[x, "Emergency Contact Indicative"])

                            dob_entry.config(state=tk.NORMAL)
                            dob_entry.insert(0, self.df.at[x, "Date of Birth"])
                            dob_entry.config(state="readonly")

                            date_to_check = str(self.df.at[x, "Date of Birth"])
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                            if bool(re.match(pattern, date_to_check)) == False:
                                dob_entry.config(readonlybackground="darkred")
                            else:
                                dob_entry.config(readonlybackground="#313131")

                            must_not_empty_entries = {
                                full_name_entry: full_name_entry.get(),
                                p_n_indicative_entry: p_n_indicative_entry.get(),
                                p_em_indicative_entry: p_em_indicative_entry.get(),
                                dob_entry: dob_entry.get(),
                                phone_entry: phone_entry.get(),
                                email_entry: email_entry.get(),
                                address_entry: address_entry.get(),
                                id_number_entry: id_number_entry.get(),
                                credit_card_entry: credit_card_entry.get(),
                                billing_address_entry: billing_address_entry.get(),
                                emergency_name_entry: emergency_name_entry.get(),
                                emergency_phone_entry: emergency_phone_entry.get()
                            }
                            for column_entry_check, value_check in must_not_empty_entries.items():
                                if str(value_check).lower() == 'nan':
                                    self.toggle_entry_colors_ifnan(0, column_entry_check)
                                    column_entry_check.delete(0, "end")
                                    column_entry_check.insert(0, "EMPTY")
                                else:
                                    self.toggle_entry_colors_ifnan(1, column_entry_check)

                            must_be_number_entries = {
                                phone_entry: phone_entry.get(),
                                credit_card_entry: credit_card_entry.get(),
                                emergency_phone_entry: emergency_phone_entry.get()
                            }
                            for value_key, value in must_be_number_entries.items():
                                try:
                                    int(value)
                                    self.toggle_entry_colors(1, value_key)
                                except ValueError:
                                    self.toggle_entry_colors(0, value_key)

                            must_not_have_number_entries = {
                                full_name_entry: full_name_entry.get(),
                                emergency_name_entry: emergency_name_entry.get()
                            }
                            for word_key, word in must_not_have_number_entries.items():
                                if any(not char.isalpha() for char in word) or str(word).lower() == "empty":
                                    self.toggle_entry_colors(0, word_key)
                                else:
                                    self.toggle_entry_colors(1, word_key)

                            self.verify_photo_path(str(self.df.at[x, "Client ID Photos"]))
                            if str(self.df.at[x, "Client ID Photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                self.toggle_button_colors(0, selected_client_photos_button)
                                self.red_bind_hover_effects(selected_client_photos_button)
                            else:
                                self.toggle_button_colors(1, selected_client_photos_button)
                                self.bind_hover_effects(selected_client_photos_button)
                        else:
                            pass

                    def update_record():
                        must_be_number = {
                                'Phone Number': (phone_entry.get(), phone_entry),
                                'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                                'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry)
                            }

                        must_not_have_number = {
                                'Full Name': (full_name_entry.get(), full_name_entry),
                                'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry)
                            }

                        must_be_defined = {
                                'Identification Type': (selected_id_type.get(), id_type_combobox),
                                'Preferred Car Type': (selected_car_type.get(), car_type_combobox),
                                'Preferred Motorcycle Type': (selected_moto_type.get(), moto_type_combobox),
                                'Nationality' : (selected_nation.get(), nation_combobox),
                                'Motorcycle License': (selected_license_class.get(), license_class_combobox)
                        }

                        must_not_be_empty = {
                                'Date of Birth': (dob_entry.get(), dob_entry),
                                'Phone Number': (phone_entry.get(), phone_entry),
                                'Phone Number Indicative': (p_n_indicative_entry.get(), p_n_indicative_entry),
                                'Emergency Contact Indicative': (p_em_indicative_entry.get(), p_em_indicative_entry),
                                'ID/Passport Number': (id_number_entry.get(), id_number_entry),
                                'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                                'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry),
                                'Full Name': (full_name_entry.get(), full_name_entry),
                                'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry),
                                'Email': (email_entry.get(), email_entry),
                                'Address': (address_entry.get(), address_entry),
                                'Billing Address': (billing_address_entry.get(), billing_address_entry)
                            }


                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            self.verify_photo_path(str(self.df.at[x, 'Client ID Photos']))

                            if str(self.df.at[x, 'Client ID Photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                if hasattr(self, 'photo_paths'):
                                    pass
                                else:
                                    is_empty.append("Photos")

                            date_to_check = str(dob_entry.get())
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                                result_of_validation = "Error Found"
                            else:
                                result_of_validation = "No Error Found"

                            if result_of_validation == "No Error Found":
                                self.df.at[x, "Date of Birth"] = dob_entry.get()
                                self.df.at[x, "Phone Number Indicative"] = str(p_n_indicative_entry.get())
                                self.df.at[x, "Emergency Contact Indicative"] = str(p_em_indicative_entry.get())
                                self.df.at[x, "Phone Number"] = int(phone_entry.get())
                                self.df.at[x, "Nationality"] = selected_nation.get()
                                self.df.at[x, "ID/Passport Number"] = str(id_number_entry.get())
                                self.df.at[x, "Credit Card Number"] = int(credit_card_entry.get())
                                self.df.at[x, "Emergency Contact Number"] = int(emergency_phone_entry.get())
                                self.df.at[x, "Full Name"] = full_name_entry.get()
                                self.df.at[x, "Emergency Contact Name"] = emergency_name_entry.get()
                                self.df.at[x, "Email"] = email_entry.get()
                                self.df.at[x, "Address"] = address_entry.get()
                                self.df.at[x, "Billing Address"] = billing_address_entry.get()
                                self.df.at[x, "Identification Type"] = selected_id_type.get()
                                self.df.at[x, "Preferred Car Type"] = selected_car_type.get()
                                self.df.at[x, "Preferred Motorcycle Type"] = selected_moto_type.get()
                                self.df.at[x, "Motorcycle License"] = selected_license_class.get()

                                if hasattr(self, 'photo_paths'):
                                    self.df.at[x, 'Client ID Photos'] = self.photo_paths
                                else:
                                    pass

                                self.toggle_button_colors(1, selected_client_photos_button)
                                clear_entries()

                                refresh_tree()
                            else:

                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format = str(self.df.at[x,'Date of Birth'])
                                    self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                                for key in must_not_be_empty:
                                    if key in is_empty:
                                        entry_value = must_not_be_empty[key][1]
                                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    else:
                                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                                for key in must_be_defined:
                                    if key in not_defined:
                                        combobox_value = must_be_defined[key][1]
                                        self.toggle_combo_text(0, must_be_defined[key][1])
                                    else:
                                        self.toggle_combo_text(1, must_be_defined[key][1])

                                for key in must_not_have_number:
                                    if key in not_alpha or key in is_empty:
                                        entry_value = must_not_have_number[key][1]
                                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_not_have_number[key][1])



                                if "Photos" in is_empty:
                                    self.toggle_button_colors(0, select_photos_button)
                                    self.red_bind_hover_effects(select_photos_button)
                                else:
                                    self.toggle_button_colors(1, select_photos_button)
                                    self.bind_hover_effects(select_photos_button)


                                for key in must_be_number:
                                    if key in not_num or key in is_empty:
                                        entry_value = must_be_number[key][1]
                                        self.toggle_entry_colors(0, must_be_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_be_number[key][1])

                                errors_adding = []
                                for error_list in errors_found:
                                    if len(error_list) > 1:
                                        errors_adding.append(error_list)

                                if len(errors_adding) > 0:
                                    self.pop_warning(new_window, errors_adding, "addrecvalidation")
                        else:
                            warning = "Must select an item to Update"
                            self.pop_warning(new_window, warning, "noselectedtoupdate" )

                        refresh_tree()

                    def remove_selected():
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            print(selected_items)
                            for record in selected_items:
                                x = treeview.index(record)
                                treeview.delete(record)
                                self.df.drop(index=x, inplace=True)
                                self.df.reset_index(drop=True, inplace=True)
                            verify_data()
                        else:
                            warning = "Must select at least one record to remove"
                            self.pop_warning(new_window, warning, "noselectedtoremove")

                    def add_selected_to_database():
                        global errors_found
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            invalid_records = []
                            valid_records = []
                            for record in selected_items:
                                x = treeview.index(record)
                                must_be_number = {
                                        'Phone Number': (str(self.df.at[x, "Phone Number"])),
                                        'Credit Card Number': (str(self.df.at[x, "Credit Card Number"])), 
                                        'Emergency Contact Number': (str(self.df.at[x, "Emergency Contact Number"]))
                                    }

                                must_not_have_number = {
                                        'Full Name': (str(self.df.at[x, "Full Name"])),
                                        'Emergency Contact Name': (str(self.df.at[x, "Emergency Contact Name"]))
                                    }

                                must_be_defined = {
                                        'Identification Type': (str(self.df.at[x, "Identification Type"]), id_types),
                                        'Nationality' : (str(self.df.at[x, "Nationality"]), nationalities),
                                        'Preferred Car Type': (str(self.df.at[x, "Preferred Car Type"]), car_types),
                                        'Preferred Motorcycle Type': (str(self.df.at[x, "Preferred Motorcycle Type"]), moto_types),
                                        'Motorcycle License': (str(self.df.at[x, "Motorcycle License"]), license_class)
                                }

                                must_not_be_empty = {
                                        'Date of Birth': (str(self.df.at[x, "Date of Birth"])),
                                        'Phone Number Indicative': (str(self.df.at[x, "Phone Number Indicative"])),
                                        'Phone Number': (str(self.df.at[x, "Phone Number"])), 
                                        'ID/Passport Number': (str(self.df.at[x, "ID/Passport Number"])),
                                        'Credit Card Number': (str(self.df.at[x, "Credit Card Number"])),
                                        'Emergency Contact Indicative': (str(self.df.at[x, "Emergency Contact Indicative"])), 
                                        'Emergency Contact Number': (str(self.df.at[x, "Emergency Contact Number"])),
                                        'Full Name': (str(self.df.at[x, "Full Name"])),
                                        'Emergency Contact Name': (str(self.df.at[x, "Emergency Contact Name"])),
                                        'Email': (str(self.df.at[x, "Email"])),
                                        'Address': (str(self.df.at[x, "Address"])),
                                        'Billing Address': (str(self.df.at[x, "Billing Address"]))
                                    }

                                self.validate_data("data_add_database", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                                print(f"Errors at index {x}: \n {errors_found}, {not_alpha}, {not_num}, {is_empty}, {not_defined}")
                                photos_of_selected = str(self.df.at[x, "Client ID Photos"])

                                if photos_of_selected.lower() != "nan":
                                    self.verify_photo_path(photos_of_selected)

                                    if len(valid_photo_type) > 0:
                                        if len(valid_photo_paths) > 0:
                                            pass
                                        if len(invalid_photo_paths) > 0:
                                            invalid_photo_paths.insert(0, "Invalid Photo Paths")
                                            errors_found = errors_found + (invalid_photo_paths,)
                                    if len(invalid_photo_type) > 0:
                                        invalid_photo_type.insert(0, "Invalid Photo Type")
                                        errors_found = errors_found + (invalid_photo_type,)
                                else:
                                    is_empty.append("Photos")

                                if any(len(error_list) > 1 for error_list in errors_found):
                                    errors_found = tuple(str(x)) + errors_found
                                    invalid_records.append(errors_found)
                                else:
                                    valid_records.append(x)
                                    result_of_validation = "No Error Found"

                            must_not_repeat = ['Phone Number', 'ID/Passport Number', 'Credit Card Number', 'Emergency Contact Number', 'Email']

                            all_that_repeated = []
                            for must_not in must_not_repeat:
                                if len(valid_records) > 0:
                                    valid_records, warning_repeated = self.check_if_repeated(valid_records, must_not)
                                    if len(warning_repeated[0]) > 0:
                                        all_that_repeated.append(warning_repeated)
                                else:
                                    print("Valid records is empty")

                            for warning in all_that_repeated:
                                for index in warning[0]:
                                    try:
                                        valid_records.remove(index)
                                    except ValueError:
                                        pass

                            if len(all_that_repeated) > 0:
                                self.pop_warning(new_window, all_that_repeated, "treerepeatedvalues")

                            wrong_format_record = []
                            wrong_text_format = []
                            for record in valid_records:
                                date_to_check = str(self.df.at[record, "Date of Birth"])
                                pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format.append(date_to_check)
                                    wrong_format_record.append(record)

                            if len(wrong_text_format) > 0:
                                self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")
                                for record in wrong_format_record:
                                    valid_records.remove(record)

                            if len(valid_records) > 0:
                                result = self.check_employee_code(str(employee_code_entry.get()), False)
                                print(result)
                                if result == "valid":
                                    self.toggle_entry_colors(1, employee_code_entry)

                                    def handle_choice(option, valid_records):
                                        if option == "confirm":
                                            try:
                                                with self.flask_app.app_context():
                                                    db.create_all()
                                                    all_exists_in_db = []
                                                    for x in valid_records:

                                                        cleaned_em_num = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'Emergency Contact Number']).lower())
                                                        cleaned_cred_num = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'Credit Card Number']).lower())
                                                        cleaned_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'ID/Passport Number']).lower())
                                                        cleaned_phone = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'Phone Number']).lower())
                                                        cleaned_email = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'Email']).lower())

                                                        existing_em_num = Client.query.filter(Client.em_number.ilike(cleaned_em_num)).first() 
                                                        existing_cred_num = Client.query.filter(Client.credit_number.ilike(cleaned_cred_num)).first()
                                                        existing_id_num = Client.query.filter(Client.id_number.ilike(cleaned_id_num)).first()
                                                        existing_phone = Client.query.filter(Client.p_number.ilike(cleaned_phone)).first()
                                                        existing_email = Client.query.filter(Client.email.ilike(cleaned_email)).first()

                                                        check_existence = [[existing_email, 'Email'], [existing_phone, 'Phone Number'], [existing_em_num, 'Emergency Contact Number'], [existing_id_num, 'ID/Passport Number'], [existing_cred_num, 'Credit Card Number']]

                                                        exists_in_db = []
                                                        for value in check_existence:
                                                            if value[0] != None:
                                                                exists_in_db.append(value[1])

                                                        if len(exists_in_db) > 0:
                                                            all_exists_in_db.append(exists_in_db)
                                                        else:
                                                            client_instance = Client(
                                                                f_name=self.df.at[x, 'Full Name'].lower(),
                                                                dob=self.df.at[x, 'Date of Birth'],
                                                                p_n_indicative=str(self.df.at[x, 'Phone Number Indicative']),
                                                                p_number=int(cleaned_phone),
                                                                email=cleaned_email,
                                                                address=self.df.at[x, 'Address'],
                                                                nationality=self.df.at[x, 'Nationality'],
                                                                id_type=self.df.at[x, 'Identification Type'],
                                                                id_number=str(cleaned_id_num),
                                                                credit_number=int(cleaned_cred_num),
                                                                bill_address=self.df.at[x, 'Billing Address'],
                                                                p_car=self.df.at[x, 'Preferred Car Type'],
                                                                m_license=str(self.df.at[x, 'Motorcycle License']),
                                                                p_moto=self.df.at[x, 'Preferred Motorcycle Type'],
                                                                p_em_indicative=str(self.df.at[x, 'Emergency Contact Indicative']),
                                                                em_name=self.df.at[x, 'Emergency Contact Name'].lower(),
                                                                em_number=int(cleaned_em_num),
                                                                photos=self.df.at[x, 'Client ID Photos'],
                                                                code_insertion=str(employee_code_entry.get())
                                                            )
                                                            db.session.add(client_instance)

                                                    db.session.commit()
                                                    clear_entries()

                                                    if len(all_exists_in_db) > 0:
                                                        self.pop_warning(new_window, all_exists_in_db, "valuealreadyindb")

                                            except OperationalError as e:
                                                warning = "Database is locked. Please close the Database and try again."
                                                self.pop_warning(new_window, warning, "databaselocked")
                                                db.session.rollback()
                                                print("Database is locked. Please try again later.")
                                                

                                        elif option == "cancel":
                                            print("User canceled")

                                    self.pop_warning(new_window, valid_records, "databvalidadd", lambda option: handle_choice(option, valid_records))

                                else:
                                    self.toggle_entry_colors(0, employee_code_entry)
                                    self.pop_warning(new_window, result, "wrongemployeecode")

                            if len(invalid_records) > 0:
                                self.pop_warning(new_window, invalid_records, "databinvalidadd")

                    def add_record():
                        must_be_number = {
                                'Phone Number': (phone_entry.get(), phone_entry),
                                'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                                'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry)
                                }

                        must_not_have_number = {
                                'Full Name': (full_name_entry.get(), full_name_entry),
                                'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry)
                                }

                        must_be_defined = {
                                'Identification Type': (selected_id_type.get(), id_type_combobox),
                                'Preferred Car Type': (selected_car_type.get(), car_type_combobox),
                                'Preferred Motorcycle Type': (selected_moto_type.get(), moto_type_combobox),
                                'Motorcycle License': (selected_license_class.get(), license_class_combobox),
                                'Nationality': (selected_nation.get(), nation_combobox)
                                }

                        must_not_be_empty = {
                                'Date of Birth': (dob_entry.get(), dob_entry),
                                'Phone Number': (phone_entry.get(), phone_entry),
                                'Phone Number Indicative': (p_n_indicative_entry.get(), p_n_indicative_entry),
                                'Emergency Contact Indicative': (p_em_indicative_entry.get(), p_em_indicative_entry),
                                'ID/Passport Number': (id_number_entry.get(), id_number_entry),
                                'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                                'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry),
                                'Full Name': (full_name_entry.get(), full_name_entry),
                                'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry),
                                'Email': (email_entry.get(), email_entry),
                                'Adress': (address_entry.get(), address_entry),
                                'Billing Address': (billing_address_entry.get(), billing_address_entry),
                                'Date of Birth': (dob_entry.get(), dob_entry)
                                }

                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        if hasattr(self, 'photo_paths'):
                            self.toggle_button_colors(1, select_photos_button)
                        else:
                            is_empty.append("Photos")

                        date_to_check = str(dob_entry.get())
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                        if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                            result_of_validation = "Error Found"
                        else:
                            result_of_validation = "No Error Found"

                        if result_of_validation == "No Error Found":

                            def handle_choice(option, possible_new_record):
                                if option == "confirm":
                                    new_record = pd.DataFrame(possible_new_record)
                                    self.df = pd.concat([self.df, new_record], ignore_index=True)
                                    clear_entries()
                                    self.df.reset_index(drop=True, inplace=True)

                                    refresh_tree()
                                elif option == "cancel":
                                    print("User canceled")

                            possible_new_record = {
                            'Full Name': [full_name_entry.get()],
                            'Date of Birth': [dob_entry.get()],
                            'Phone Number Indicative': [str(p_n_indicative_entry.get())],
                            'Phone Number': [int(phone_entry.get())],
                            'Email': [email_entry.get()],
                            'Address': [address_entry.get()],
                            'Nationality': [selected_nation.get()],
                            'Identification Type': [selected_id_type.get()],
                            'ID/Passport Number': [str(id_number_entry.get())],
                            'Credit Card Number': [int(credit_card_entry.get())],
                            'Billing Address': [billing_address_entry.get()],
                            'Preferred Car Type': [selected_car_type.get()],
                            'Preferred Motorcycle Type': [selected_moto_type.get()],
                            'Motorcycle License': [selected_license_class.get()],
                            'Emergency Contact Name': [emergency_name_entry.get()],
                            'Emergency Contact Indicative': [str(p_em_indicative_entry.get())],
                            'Emergency Contact Number': [int(emergency_phone_entry.get())],
                            'Client ID Photos': self.photo_paths
                            }

                            print(f"Type of possible new record: {type(possible_new_record)}")
                            print(f"Possible new record: {possible_new_record}")

                            self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                        else:
                            if str(dob_entry.get()) != "":
                                if bool(re.match(pattern, date_to_check)) == False:
                                    wrong_text_format = str(dob_entry.get())
                                    self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                            for key in must_not_be_empty:
                                if key in is_empty:
                                    entry_value = must_not_be_empty[key][1]
                                    self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    if key == "Date of Birth":
                                        dob_entry.config(readonlybackground="darkred")
                                else:
                                    self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                            for key in must_be_defined:
                                if key in not_defined:
                                    combobox_value = must_be_defined[key][1]
                                    self.toggle_combo_text(0, must_be_defined[key][1])
                                else:
                                    self.toggle_combo_text(1, must_be_defined[key][1])

                            for key in must_not_have_number:
                                if key in not_alpha or key in is_empty:
                                    entry_value = must_not_have_number[key][1]
                                    self.toggle_entry_colors(0, must_not_have_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_not_have_number[key][1])

                            if "Photos" in is_empty:
                                self.toggle_button_colors(0, select_photos_button)
                                self.red_bind_hover_effects(select_photos_button)
                            else:
                                self.toggle_button_colors(1, select_photos_button)
                                self.bind_hover_effects(select_photos_button)

                            for key in must_be_number:
                                if key in not_num or key in is_empty:
                                    entry_value = must_be_number[key][1]
                                    self.toggle_entry_colors(0, must_be_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_be_number[key][1])

                            errors_adding = []
                            for error_list in errors_found:
                                if len(error_list) > 1:
                                    errors_adding.append(error_list)

                            if len(errors_adding) > 0:
                                self.pop_warning(new_window, errors_adding, "addrecvalidation")                        

                    def remove_all():
                        for record in treeview.get_children():
                            x = treeview.index(record)
                            treeview.delete(record)
                            self.df.drop(index=x, inplace=True)
                            self.df.reset_index(drop=True, inplace=True)

                    def selected_client_photos():
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            photos_of_selected = str(self.df.at[x, "Client ID Photos"])

                            if photos_of_selected.lower() != "nan":
                                self.verify_photo_path(photos_of_selected)

                                if len(valid_photo_type) > 0:
                                    if len(valid_photo_paths) > 0:
                                        def handle_photo_viewer_result(result, updated_photos):
                                            if result == "confirm":
                                                self.df.at[x, 'Client ID Photos'] = updated_photos
                                            elif result == "cancel":
                                                print("User cancelled changes")

                                        updated_photos = []
                                        self.photo_viewer(new_window, valid_photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos)
                                    if len(invalid_photo_paths) > 0:
                                        self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                        self.toggle_button_colors(0, selected_client_photos_button)
                                print(invalid_photo_type)
                                for path in invalid_photo_type:
                                    if path == "":
                                        invalid_photo_type.remove(path)
                                if len(invalid_photo_type) > 0:
                                    self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                                    self.toggle_button_colors(0, selected_client_photos_button)
                            else:
                                x += 1
                                self.pop_warning(new_window, str(x), "nanselectedphoto")
                                self.toggle_button_colors(0, selected_client_photos_button)
                        else:
                            warning = "Must select a record to see photos"
                            self.pop_warning(new_window, warning, "noselectedtoseephotos")

                    refresh_tree()
                    treeview.pack(expand=True, fill="both")

                    add_record_button = Button(edit_treeview_frame, text="Add Record to Data Frame", fg="white",
                                               bg="black",
                                               command=add_record)
                    add_record_button.grid(row=0, column=0, padx=5, pady=3)
                    self.bind_hover_effects(add_record_button)

           
                    add_record_database = Button(edit_treeview_frame, text="Add Selected Record(s) to Database", fg="white",
                                               bg="darkgreen",
                                               command=add_selected_to_database)
                    add_record_database.grid(row=1, column=0, columnspan=7, padx=10, pady=5)
                    self.green_bind_hover_effects(add_record_database)

                    update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                           command=update_record)
                    update_button.grid(row=0, column=1, padx=5, pady=3)
                    self.bind_hover_effects(update_button)

                    clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                                  command=clear_entries)
                    clear_entries_button.grid(row=0, column=2, padx=5, pady=3)
                    self.bind_hover_effects(clear_entries_button)


                    selected_client_photos_button = Button(edit_treeview_frame, text="See Selected Client ID Photos",
                                                            fg="white",
                                                            bg="black", command=selected_client_photos)
                    selected_client_photos_button.grid(row=0, column=3, padx=5, pady=3)
                    self.bind_hover_effects(selected_client_photos_button)

                    remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                                    bg="black", command=remove_selected)
                    remove_selected_button.grid(row=0, column=4, padx=5, pady=3)
                    self.bind_hover_effects(remove_selected_button)

                    remove_all_button = Button(edit_treeview_frame, text="Remove All Records", fg="white",
                                               bg="black", command=remove_all)
                    remove_all_button.grid(row=0, column=5, padx=5, pady=3)
                    self.bind_hover_effects(remove_all_button)

                    refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                               bg="black", command=refresh_tree)
                    refresh_tree_button.grid(row=0, column=6, padx=5, pady=3)
                    self.bind_hover_effects(refresh_tree_button)

                    treeview.bind("<ButtonRelease-1>", select_record)

                else:
                    missing_heading = [head for head in client_headings_lowercase if head not in client_file_headings]
                    unmatched_heading = [head for head in client_file_headings if head not in client_headings_lowercase]
                    missing_unmatched_head = missing_heading, unmatched_heading

                    if len(missing_heading) > 0 and len(unmatched_heading) > 0:
                        self.pop_warning(new_window, missing_unmatched_head, "missingheadunmatched" )
                    elif len(missing_heading) > 0 and len(unmatched_heading) == 0:
                        self.pop_warning(new_window, missing_heading, "missingheading")
                    elif len(missing_heading) == 0 and len(unmatched_heading) > 0:
                        self.pop_warning(new_window, unmatched_heading, "unmatchedheading")
            else:
                print("No file path selected")

        def check_if_df():
            if hasattr(self, 'df'):
                check_client_file_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_files_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_check_button.configure(image=self.check_files_image)
            else:
                print("No file selected")

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)
                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))
                reload_show_photos_button.configure(image=self.update_photos_button_image)

        def add_client_db():
            must_be_number = {
                    'Phone Number': (phone_entry.get(), phone_entry),
                    'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                    'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry)
                    }

            must_not_have_number = {
                    'Full Name': (full_name_entry.get(), full_name_entry),
                    'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry)
                    }

            must_be_defined = {
                    'Identification Type': (selected_id_type.get(), id_type_combobox),
                    'Preferred Car Type': (selected_car_type.get(), car_type_combobox),
                    'Preferred Motorcycle Type': (selected_moto_type.get(), moto_type_combobox),
                    'Motorcycle License': (selected_license_class.get(), license_class_combobox),
                    'Nationality' : (selected_nation.get(), nation_combobox)
                    }

            must_not_be_empty = {
                    'Date of Birth': (dob_entry.get(), dob_entry),
                    'Phone Number Indicative': (p_n_indicative_entry.get(), p_n_indicative_entry),
                    'Phone Number': (phone_entry.get(), phone_entry),
                    'ID/Passport Number': (id_number_entry.get(), id_number_entry),
                    'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                    'Emergency Contact Indicative': (p_em_indicative_entry.get(), p_em_indicative_entry),
                    'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry),
                    'Full Name': (full_name_entry.get(), full_name_entry),
                    'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry),
                    'Email': (email_entry.get(), email_entry),
                    'Address': (address_entry.get(), address_entry),
                    'Billing Address': (billing_address_entry.get(), billing_address_entry),
                    'Date of Birth': (dob_entry.get(), dob_entry)
                    }


            self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

            if hasattr(self, 'photo_paths'):
                self.toggle_button_colors(1, select_photos_button)
            else:
                is_empty.append("Photos")

            date_to_check = str(dob_entry.get())
            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

            if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                result_of_validation = "Error Found"
            else:
                result_of_validation = "No Error Found"

            if result_of_validation == "No Error Found":
                result = self.check_employee_code(str(employee_code_entry.get()), False)
                if result == "valid":
                    self.toggle_entry_colors(1, employee_code_entry)

                    combo = [id_type_combobox, car_type_combobox, moto_type_combobox, nation_combobox]
                    for box in combo:
                        self.toggle_combo_text(1, box)

                    entries = [full_name_entry, phone_entry, dob_entry, id_number_entry, credit_card_entry, emergency_phone_entry, 
                                emergency_name_entry, email_entry, address_entry, billing_address_entry]
                    for entry in entries:
                        self.toggle_entry_colors(1, entry)

                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    def handle_choice(option, possible_new_record):
                        if option == "confirm":
                            try:
                                with self.flask_app.app_context():
                                    db.create_all()
                                    
                                    cleaned_em_num = re.sub(r'[^\w\s]', '', str(emergency_phone_entry.get()).lower())
                                    cleaned_cred_num = re.sub(r'[^\w\s]', '', str(credit_card_entry.get()).lower())
                                    cleaned_id_num = re.sub(r'[^\w\s]', '', str(id_number_entry.get()).lower())
                                    cleaned_phone = re.sub(r'[^\w\s]', '', str(phone_entry.get()).lower())
                                    cleaned_email = re.sub(r'[^\w\s]', '', str(email_entry.get()).lower())

                                    existing_em_num = Client.query.filter(Client.em_number.ilike(cleaned_em_num)).first() 
                                    existing_cred_num = Client.query.filter(Client.credit_number.ilike(cleaned_cred_num)).first()
                                    existing_id_num = Client.query.filter(Client.id_number.ilike(cleaned_id_num)).first()
                                    existing_phone = Client.query.filter(Client.p_number.ilike(cleaned_phone)).first()
                                    existing_email = Client.query.filter(Client.email.ilike(cleaned_email)).first()

                                    check_existence = [[existing_email, 'Email'], [existing_phone, 'Phone Number'], [existing_em_num, 'Emergency Contact Number'], [existing_id_num, 'ID/Passport Number'], [existing_cred_num, 'Credit Card Number']]

                                    exists_in_db = []
                                    for value in check_existence:
                                        if value[0] != None:
                                            exists_in_db.append(value[1])

                                    if len(exists_in_db) > 0:
                                        self.pop_warning(new_window, exists_in_db, "clientdataalreadyindb")
                                        
                                    else:
                                        client_instance = Client(
                                            f_name=full_name_entry.get().lower(),
                                            dob=dob_entry.get(),
                                            p_n_indicative=str(p_n_indicative_entry.get()),
                                            p_number=int(cleaned_phone),
                                            email=cleaned_email,
                                            address=address_entry.get(),
                                            nationality=selected_nation.get(),
                                            id_type=selected_id_type.get(),
                                            id_number=str(cleaned_id_num),
                                            credit_number=int(cleaned_cred_num),
                                            bill_address=billing_address_entry.get(),
                                            p_car=selected_car_type.get(),
                                            p_moto=selected_moto_type.get(),
                                            m_license=str(selected_license_class.get()),
                                            em_name=emergency_name_entry.get().lower(),
                                            p_em_indicative=str(p_em_indicative_entry.get()),
                                            em_number=int(cleaned_em_num),
                                            photos=self.photo_paths,
                                            code_insertion=str(employee_code_entry.get())
                                        )
                                        db.session.add(client_instance)
                                        db.session.commit()

                                        entries = [p_n_indicative_entry, employee_code_entry, p_em_indicative_entry, full_name_entry, phone_entry, email_entry, 
                                                    address_entry, id_number_entry, credit_card_entry, billing_address_entry, emergency_name_entry, emergency_phone_entry]
                                        for entry in entries:
                                            entry.delete(0, END)
                                            self.toggle_entry_colors(1, entry)

                                        read_only_entries = [dob_entry]
                                        for entry in read_only_entries:
                                            entry.config(state=tk.NORMAL)
                                            entry.delete(0, tk.END)
                                            entry.config(state="readonly", readonlybackground="#313131")

                                        combos = [[id_type_combobox, id_types],[car_type_combobox, car_types], [moto_type_combobox, moto_types], 
                                                [license_class_combobox, license_class], [nation_combobox, nationalities]]
                                        for combo in combos:
                                            self.toggle_combo_text(1, combo[0])
                                            combo[0].set(combo[1][0])

                                        del self.photo_paths
                                        check_if_photos()
                            except OperationalError as e:
                                warning = "Database is locked. Please close the Database and try again."
                                self.pop_warning(new_window, warning, "databaselocked")
                                db.session.rollback()
                                print("Database is locked. Please try again later.")

                        elif option == "cancel":
                            print("User canceled")

                    possible_new_record = {
                    'Full Name': [full_name_entry.get()],
                    'Date of Birth': [dob_entry.get()],
                    'Phone Number Indicative': [str(p_n_indicative_entry.get())],
                    'Phone Number': [int(phone_entry.get())],
                    'Email': [email_entry.get()],
                    'Address': [address_entry.get()], 
                    'Nationality': [selected_nation.get()], 
                    'Identification Type': [selected_id_type.get()],
                    'ID/Passport Number': [str(id_number_entry.get())],
                    'Credit Card Number': [int(credit_card_entry.get())],
                    'Billing Address': [billing_address_entry.get()],
                    'Preferred Car Type': [selected_car_type.get()],
                    'Motorcycle License': [selected_license_class.get()],
                    'Preferred Motorcycle Type': [selected_moto_type.get()],
                    'Emergency Contact Name': [emergency_name_entry.get()],
                    'Emergency Contact Indicative': [str(p_em_indicative_entry.get())],
                    'Emergency Contact Number': [int(emergency_phone_entry.get())],
                    'Client ID Photos': self.photo_paths
                    }
                        
                    self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                else:
                    self.toggle_entry_colors(0, employee_code_entry)
                    self.pop_warning(new_window, result, "wrongemployeecode")
            else:
                if str(dob_entry.get()) != "":
                    if bool(re.match(pattern, date_to_check)) == False:
                        wrong_text_format = str(dob_entry.get())
                        self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                for key in must_not_be_empty:
                    if key in is_empty:
                        entry_value = must_not_be_empty[key][1]
                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                        if key == "Date of Birth":
                            dob_entry.config(readonlybackground="darkred")
                    else:
                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                for key in must_be_defined:
                    if key in not_defined:
                        combobox_value = must_be_defined[key][1]
                        self.toggle_combo_text(0, must_be_defined[key][1])
                    else:
                        self.toggle_combo_text(1, must_be_defined[key][1])

                for key in must_not_have_number:
                    if key in not_alpha or key in is_empty:
                        entry_value = must_not_have_number[key][1]
                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_not_have_number[key][1])

                if "Photos" in is_empty:
                    self.toggle_button_colors(0, select_photos_button)
                    self.red_bind_hover_effects(select_photos_button)
                else:
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                for key in must_be_number:
                    if key in not_num or key in is_empty:
                        entry_value = must_be_number[key][1]
                        self.toggle_entry_colors(0, must_be_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_be_number[key][1])

                errors_adding = []
                for error_list in errors_found:
                    if len(error_list) > 1:
                        errors_adding.append(error_list)

                if len(errors_adding) > 0:
                    self.pop_warning(new_window, errors_adding, "addrecvalidation")

        insert_client_frame = tk.Frame(new_window)
        insert_client_frame.configure(bg="black")
        insert_client_frame.pack(pady=(0,10))

        upload_client_file_button = tk.Button(insert_client_frame, text="Upload Client File", width=15,
                                               borderwidth=2,
                                               fg="white", bg="black", command=lambda: self.load_data(new_window))
        upload_client_file_button.grid(row=0, column=3, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(upload_client_file_button)

        check_client_file_button = tk.Button(insert_client_frame, text="Check Data", width=15, borderwidth=2,
                                              fg="white", bg="black", state=tk.DISABLED, command=check_data)
        check_client_file_button.grid(row=0, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(check_client_file_button)

        update_files_button_image_path = resource_path('resources/update.png')
        self.update_files_button_image = ImageTk.PhotoImage(Image.open(update_files_button_image_path))
        reload_check_button = tk.Button(insert_client_frame, image=self.update_files_button_image, command=check_if_df,
                                        borderwidth=0, highlightthickness=0)
        reload_check_button.grid(row=0, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_check_button)

        employee_code_label = tk.Label(insert_client_frame, text="Employee Code:",
                          font=("Helvetica", 10), fg="white", bg="black")
        employee_code_label.grid(row=0, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        employee_code_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        employee_code_entry.grid(row=0, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        full_name_label = tk.Label(insert_client_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        full_name_label.grid(row=1, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        full_name_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        dob_button = tk.Button(insert_client_frame, text="Select Date of Birth", width=15, borderwidth=2,
                                              fg="white", bg="black", command=lambda: self.datepicker(new_window, dob_entry, "dob"))

        dob_button.grid(row=2, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        dob_entry = tk.Entry(insert_client_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        dob_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        phone_indicative_label = tk.Label(insert_client_frame, text="Phone Indicative:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_indicative_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        p_n_indicative_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        p_n_indicative_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(insert_client_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        phone_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(insert_client_frame, text="Email:",
                               font=("Helvetica", 10), fg="white", bg="black")
        email_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        email_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        address_label = tk.Label(insert_client_frame, text="Address:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        address_label.grid(row=6, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        address_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        address_entry.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)


        nation_label = tk.Label(insert_client_frame, text="Nationality:",
                         font=("Helvetica", 10), fg="white", bg="black")
        nation_label.grid(row=7, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        nationalities = [
            "Not Defined","Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean", "Armenian", "Australian", "Austrian", "Azerbaijani",
            "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Barbudans", "Batswana", "Belarusian", "Belgian", "Belizean", "Beninese", "Bhutanese", "Bolivian",
            "Bosnian", "Brazilian", "British", "Bruneian", "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean",
            "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese", "Costa Rican", "Croatian", "Cuban", "Cypriot", "Czech",
            "Danish", "Djibouti", "Dominican", "Dutch", "East Timorese", "Ecuadorean", "Egyptian", "Emirian", "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian",
            "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Greek", "Grenadian", "Guatemalan", "Guinea-Bissauan",
            "Guinean", "Guyanese", "Haitian", "Herzegovinian", "Honduran", "Hungarian", "I-Kiribati", "Icelander", "Indian", "Indonesian", "Iranian", "Iraqi",
            "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakhstani", "Kenyan", "Kittian and Nevisian", "Kuwaiti", "Kyrgyz",
            "Laotian", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian", "Luxembourger", "Macedonian", "Malagasy", "Malawian", "Malaysian",
            "Maldivan", "Malian", "Maltese", "Marshallese", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monacan", "Mongolian", "Moroccan",
            "Mosotho", "Motswana", "Mozambican", "Namibian", "Nauruan", "Nepalese", "New Zealander", "Ni-Vanuatu", "Nicaraguan", "Nigerian", "Nigerien", "North Korean",
            "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Panamanian", "Papua New Guinean", "Paraguayan", "Peruvian", "Polish", "Portuguese", "Qatari",
            "Romanian", "Russian", "Rwandan", "Saint Lucian", "Salvadoran", "Samoan", "San Marinese", "Sao Tomean", "Saudi", "Scottish", "Senegalese", "Serbian",
            "Seychellois", "Sierra Leonean", "Singaporean", "Slovakian", "Slovenian", "Solomon Islander", "Somali", "South African", "South Korean", "Spanish", "Sri Lankan",
            "Sudanese", "Surinamer", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian or Tobagonian",
            "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani", "Venezuelan", "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"
        ]
        selected_nation = tk.StringVar()
        nation_combobox = ttk.Combobox(insert_client_frame,
                                        textvariable=selected_nation,
                                        values=nationalities, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        nation_combobox.grid(row=7, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        nation_combobox.set(nationalities[0])  # Set the default selection        

        id_type_label = tk.Label(insert_client_frame, text="Identification Type:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        id_type_label.grid(row=1, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        id_types = ["Not Defined", "National ID", "Passport"]
        selected_id_type = tk.StringVar()
        id_type_combobox = ttk.Combobox(insert_client_frame,
                                        textvariable=selected_id_type,
                                        values=id_types, state="readonly", justify="center", height=4,
                                        style="TCombobox")
        id_type_combobox.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        id_type_combobox.set(id_types[0])  # Set the default selection

        id_number_label = tk.Label(insert_client_frame, text="ID/Passport Number:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        id_number_label.grid(row=2, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        id_number_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        id_number_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        credit_card_label = tk.Label(insert_client_frame, text="Credit Card Number:",
                                     font=("Helvetica", 10), fg="white", bg="black")
        credit_card_label.grid(row=3, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        credit_card_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        credit_card_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        billing_address_label = tk.Label(insert_client_frame, text="Billing Address:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        billing_address_label.grid(row=4, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        billing_address_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        billing_address_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)


        moto_license_label = tk.Label(insert_client_frame, text="Motorcycle License:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        moto_license_label.grid(row=5, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        license_class = ["Not Defined", "Not Applicable", "A1(125cc|11kw|0.1kw/kg)", "A2(max-35kw|0.2kw/kg)", "A"]
        selected_license_class = tk.StringVar()
        license_class_combobox = ttk.Combobox(insert_client_frame,
                                        textvariable=selected_license_class,
                                        values=license_class, state="readonly", justify="center", height=4,
                                        style="TCombobox")
        license_class_combobox.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        license_class_combobox.set(id_types[0])  # Set the default selection

        car_type_label = tk.Label(insert_client_frame, text="Preferred Car Type:",
                                  font=("Helvetica", 10), fg="white", bg="black")
        car_type_label.grid(row=1, column=4, pady=5, padx=(30, 5), sticky=tk.E)
        car_types = ["Not Defined", "None", "Microcar", "Subcompact", "Compact", "Midsize", "Full-size", "SUV", "Crossover",
                     "Multi-Purpose Vehicle", "Convertible/Cabriolet", "Coupe", "Roadster", "Hot Hatch", "Sports Car"]
        selected_car_type = tk.StringVar()
        car_type_combobox = ttk.Combobox(insert_client_frame, textvariable=selected_car_type,
                                         values=car_types, state="readonly", justify="center", height=4)
        car_type_combobox.grid(row=1, column=5, pady=5, padx=(5, 20), sticky=tk.W)
        car_type_combobox.set(car_types[0])  # Set the default selection

        moto_type_label = tk.Label(insert_client_frame,
                                   text="Preferred Motorcycle Type:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        moto_type_label.grid(row=2, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        moto_types = ["Not Defined", "None", "Sport Bikes", "Cruisers", "Touring Bikes", "Naked Bikes",
                      "Adventure Bikes", "Dirt Bikes", "Scooters",
                      "Electric Motorcycles", "Cafe Racers", "Choppers",
                      "Bobbers", "Trikes"]
        selected_moto_type = tk.StringVar()
        moto_type_combobox = ttk.Combobox(insert_client_frame,
                                          textvariable=selected_moto_type,
                                          values=moto_types, state="readonly", justify="center", height=4)
        moto_type_combobox.grid(row=2, column=5, pady=5, padx=(5, 20), sticky=tk.W)
        moto_type_combobox.set(moto_types[0])  # Set the default selection

        emergency_name_label = tk.Label(insert_client_frame, text="Emergency Contact Name:",
                                        font=("Helvetica", 10), fg="white", bg="black")
        emergency_name_label.grid(row=3, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        emergency_name_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        emergency_name_entry.grid(row=3, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        emergency_phone_indicative_label = tk.Label(insert_client_frame, text="Emergency Contact Indicative:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        emergency_phone_indicative_label.grid(row=4, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        p_em_indicative_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        p_em_indicative_entry.grid(row=4, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        emergency_phone_label = tk.Label(insert_client_frame, text="Emergency Contact Number:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        emergency_phone_label.grid(row=5, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        emergency_phone_entry = tk.Entry(insert_client_frame, bd=2, width=10)
        emergency_phone_entry.grid(row=5, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        select_photos_button = tk.Button(insert_client_frame, text="Select Client ID Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=6, column=3, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)

        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(insert_client_frame, text="See Client ID Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=6, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(insert_client_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=6, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)
        
        add_client_button = tk.Button(insert_client_frame, text="Add Client", width=20, borderwidth=2,
                                          fg="white", bg="#004d00",
                                          command=add_client_db)
        add_client_button.grid(row=7, column=4, padx=5, pady=5, sticky="e")
        self.green_bind_hover_effects(add_client_button)

    # Section to insert/make reservation into the database
    def make_reservations_section(self, new_window):
        if hasattr(self, 'df'):
            del self.df
        else:
            pass

        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        file_section_info = "Upload a Excel/CSV file by pressing the 'Upload Reservation File' button"
        file_section_info_label = tk.Label(treeFrame, text=file_section_info, font=("Helvetica", 10),
                                           fg="white", bg="black")
        file_section_info_label.pack(pady=(140, 0))

        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)
        edit_treeview_frame.configure(bg="black")

        def check_data():
            if self.df is not None and not self.df.empty:
                reservations_file_headings = []
                for column in self.df.columns:
                    reservations_file_headings.append(column.lower())

                reservations_headings = ['Pick-up Date', 'Drop-off Date', 'Vehicle ID', 'ID/Passport Number',
                                    'Payment-Method', 'Receipt Photos']
                reservations_headings_lowercase = [head.lower() for head in reservations_headings]

                reservations_file_headings_check = all(
                    head in reservations_file_headings for head in reservations_headings_lowercase)

                if reservations_file_headings_check and len(reservations_file_headings) == len(reservations_headings):
                    confirm_reservation_button.grid_forget()

                    for widget in treeFrame.winfo_children():
                        widget.destroy()

                    treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeFrame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    def verify_data():
                        for index, row in self.df.iterrows():
                            not_num = []
                            must_be_number = {                        
                            }

                            for column_num, value_num in must_be_number.items():
                                try:
                                    int(value_num)
                                except ValueError:
                                    not_num.append(value_num)

                            not_alpha = []

                            is_empty = []
                            all_data = {
                                'Pick-up Date': str(row['Pick-up Date']),
                                'ID/Passport Number': str(row['ID/Passport Number']),
                                'Drop-off Date': str(row['Drop-off Date']),
                                'Receipt Photos': str(row['Receipt Photos']),
                                'Vehicle ID': str(row['Vehicle ID'])
                            }

                            for column_all, value_all in all_data.items():
                                if value_all == 'nan':
                                    is_empty.append(value_all)
                                else:
                                    pass

                            not_defined = []
                            must_be_defined = {
                                'Payment-Method': (str(row['Payment-Method']), pay_types)
                            }

                            for column_defined, value_defined in must_be_defined.items():
                                if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                                    not_defined.append(value_defined)
                                else:
                                    pass

                            errors_found = not_num, not_alpha, is_empty, not_defined

                            possible_photo_path_list = str(row['Receipt Photos'])

                            self.verify_photo_path(possible_photo_path_list)
                            if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                                pass
                            if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                is_empty.append("Photos")

                            date_pick_check = str(row['Pick-up Date'])
                            date_drop_check = str(row['Drop-off Date'])

                            dates_to_check = [date_pick_check, date_drop_check]
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            existing_client = None
                            existing_vehicle = None

                            cleaned_id_number = re.sub(r'[^\w\s]', '', str(row['ID/Passport Number']).lower())
                            existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(row['Vehicle ID']).lower())
                            existing_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()                                
                            

                            if any(len(error_list) > 0 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or existing_client == None or existing_vehicle == None: 
                                result_of_validation = "Error Found"
                                self.change_row_color(treeview, index, "darkred")
                            else:
                                self.change_row_color(treeview, index, "#313131")
                                result_of_validation = "No Error Found"

                    def refresh_tree():
                        treeview.delete(*treeview.get_children())

                        def convert_to_datetime(date_string):
                            try:
                                return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                            except ValueError:
                                return date_string

                        self.df['Pick-up Date'] = self.df['Pick-up Date'].apply(convert_to_datetime)
                        self.df['Drop-off Date'] = self.df['Drop-off Date'].apply(convert_to_datetime)          

                        treeview["column"] = list(self.df)
                        treeview["show"] = "headings"

                        for column in treeview["column"]:
                            treeview.heading(column, text=column)
                            treeview.column(column, anchor="center")

                        columns_to_int = ['Vehicle ID', 'ID/Passport Number']

                        for column in columns_to_int:
                            try:
                                self.df[column] = self.df[column].fillna(0).astype('int64')
                                self.df[column] = self.df[column].replace(0, 'nan')
                            except ValueError:
                                pass             
                           
                        df_rows = self.df.to_numpy().tolist()
                        for row in df_rows:
                            treeview.insert("", "end", values=row)

                        for col in treeview["columns"][:-1]:
                            heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                            
                            max_width = max(
                                tkFont.Font().measure(str(treeview.set(item, col)))
                                for item in treeview.get_children("")
                            )
                            
                            column_width = max(heading_width, max_width) + 20  
                            
                            treeview.column(col, width=column_width, minwidth=heading_width)

                        last_col = treeview["columns"][-1]
                        treeview.column(last_col, width=120, minwidth=120)

                        treeview.update_idletasks()

                        verify_data()

                    def clear_entries():
                        entries = [id_num_entry, vehicle_id_entry, employee_code_entry]
                        for entry in entries:
                            entry.delete(0, END)
                            self.toggle_entry_colors(1, entry)

                        read_only_entries = [pick_entry, drop_entry, rent_duration_entry, cost_day_entry, cost_total_entry, 
                        full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                        for entry in read_only_entries:
                            entry.config(state=tk.NORMAL)
                            entry.delete(0, tk.END)
                            entry.config(state="readonly", readonlybackground="#313131")

                        combos = [[pay_type_combobox, pay_types]]
                        for combo in combos:
                            self.toggle_combo_text(1, combo[0])
                            combo[0].set(combo[1][0])

                        if hasattr(self, 'photo_paths'):
                            del self.photo_paths
                        see_photos_button.configure(state=tk.DISABLED)
                        reload_show_photos_button.configure(image=self.update_photos_button_image)

                    def select_record(e):
                        clear_entries()

                        selected_items = treeview.selection()

                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            self.toggle_entry_colors(1, employee_code_entry)
                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                            cleaned_id_number = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'ID/Passport Number']).lower())
                            existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[x, 'Vehicle ID']).lower())
                            existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                            must_exist = [[existing_client, "client"], [existing_cleaned_vehicle, "vehicle"]]
                            none_foundlist = []
                            for must in must_exist:
                                if must[0] == None:
                                    none_foundlist.append(must[1])

                            type_pay = str(self.df.at[x, "Payment-Method"]).lower()

                            pay_type_combobox.set(pay_types[0])  # Set the default selection
                            mapping = {p.lower(): pay_types[i] for i, p in enumerate(pay_types)}
                            pay_type_combobox.set(mapping.get(type_pay, mapping["not defined"]))

                            if pay_type_combobox.get() == 'Not Defined':
                                self.toggle_combo_text(0, pay_type_combobox)
                            else:
                                self.toggle_combo_text(1, pay_type_combobox)

                            read_only_entries = [pick_entry, drop_entry, rent_duration_entry, 
                            cost_day_entry, cost_total_entry, full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                            client_read_only_entries = [full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                            for entry in read_only_entries:
                                entry.config(state=tk.NORMAL)

                            if "client" in none_foundlist:
                                self.toggle_entry_colors(0, id_num_entry)
                                id_num_entry.insert(0, "Not found")
                                for entry in client_read_only_entries:
                                    entry.insert(0, "Not found")
                                    entry.config(readonlybackground="darkred")
                                    
                            elif "client" not in none_foundlist:
                                self.toggle_entry_colors(1, id_num_entry)
                                for entry in client_read_only_entries:
                                    entry.config(readonlybackground="#313131")
                                full_name_entry.insert(0, str(existing_client.f_name))
                                phone_entry.insert(0, int(existing_client.p_number))
                                email_entry.insert(0, str(existing_client.email))
                                dob_entry.insert(0, str(existing_client.dob))
                                em_name_entry.insert(0, str(existing_client.em_name))
                                em_num_entry.insert(0, int(existing_client.em_number))
                                bill_address_entry.insert(0, str(existing_client.bill_address))
                                id_num_entry.insert(0, int(existing_client.id_number))
                                nationality_entry.insert(0, str(existing_client.nationality))

                            if "vehicle" in none_foundlist:
                                vehicle_id_entry.insert(0, "Not found")
                                self.toggle_entry_colors(0, vehicle_id_entry)
                            else:
                                vehicle_id_entry.insert(0, str(existing_cleaned_vehicle.license_plate))
                                self.toggle_entry_colors(1, vehicle_id_entry)

                            date_pick_check = str(self.df.at[x, 'Pick-up Date'])
                            date_drop_check = str(self.df.at[x, 'Drop-off Date'])

                            dates_to_check = [[date_pick_check, pick_entry], [date_drop_check, drop_entry]]
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"                                
                            inval_date = []
                            for date in dates_to_check:
                                if bool(re.match(pattern, date[0])) == False:
                                    date[1].insert(0, str(date[0]))
                                    date[1].config(readonlybackground="darkred")
                                    inval_date.append(date)
                                else:
                                    date[1].insert(0, str(date[0]))
                                    date[1].config(readonlybackground="#313131")


                            if len(inval_date) > 0:
                                rent_duration_entry.insert(0, "Failed")
                                rent_duration_entry.config(readonlybackground="darkred")
                                cost_day_entry.insert(0, "Failed")
                                cost_day_entry.config(readonlybackground="darkred")
                                cost_total_entry.insert(0, "Failed")
                                cost_total_entry.config(readonlybackground="darkred")
                            else:
                                date_format = "%Y-%m-%d"
                                date_pick = datetime.strptime(date_pick_check, date_format)
                                date_drop = datetime.strptime(date_drop_check, date_format)

                                rent_duration_entry.config(readonlybackground="#313131")
                                cost_day_entry.config(readonlybackground="#313131")
                                cost_total_entry.config(readonlybackground="#313131")

                                difference = date_drop - date_pick
                                difference = difference.days + 1
                                rent_duration_entry.insert(0, difference)

                                try:
                                    if existing_cleaned_vehicle.category.lower() == 'gold':
                                        cost_day_entry.insert(0, 120)
                                        total = int(difference) * 120
                                        cost_total_entry.insert(0, int(total))
                                    elif existing_cleaned_vehicle.category.lower() == 'silver':
                                        cost_day_entry.insert(0, 80)
                                        total = int(difference) * 80
                                        cost_total_entry.insert(0, int(total))
                                    elif existing_cleaned_vehicle.category.lower() == 'economic':
                                        cost_day_entry.insert(0, 40)
                                        total = int(difference) * 40
                                        cost_total_entry.insert(0, int(total))
                                except AttributeError:
                                    pass

                            for entry in read_only_entries:
                                entry.config(state="readonly")

                            self.verify_photo_path(str(self.df.at[x, "Receipt Photos"]))
                            if str(self.df.at[x, "Receipt Photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                                self.red_bind_hover_effects(selected_receipt_photos_button)
                            else:
                                self.toggle_button_colors(1, selected_receipt_photos_button)
                                self.bind_hover_effects(selected_receipt_photos_button)
                                print(self.df.at[x, "Receipt Photos"])
                        else:
                            pass

                    def update_record():
                        must_be_number = {
                            }

                        must_not_have_number = {}

                        must_be_defined = {
                                'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
                        }

                        must_not_be_empty = {
                                'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                                'ID/Passport Number': (id_num_entry.get(), id_num_entry)
                            }


                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])

                            self.verify_photo_path(str(self.df.at[x, 'Receipt Photos']))

                            if str(self.df.at[x, 'Receipt Photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                                if hasattr(self, 'photo_paths'):
                                    pass
                                else:
                                    is_empty.append("Photos")

                            date_pick_check = str(pick_entry.get())
                            date_drop_check = str(drop_entry.get())

                            dates_to_check = [date_pick_check, date_drop_check]
                            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                            cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                            existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                            existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                            must_exist = [[existing_client, "client"], [existing_cleaned_vehicle, "vehicle"]]
                            none_foundlist = []
                            for must in must_exist:
                                if must[0] == None:
                                    none_foundlist.append(must[1])                              
                            
                            if any(len(error_list) > 1 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or len(none_foundlist) > 0: 
                                result_of_validation = "Error Found"
                            else:
                                result_of_validation = "No Error Found"

                            if result_of_validation == "No Error Found":
                                self.df.at[x, "Pick-up Date"] = pick_entry.get()
                                self.df.at[x, "Drop-off Date"] = drop_entry.get()
                                self.df.at[x, "ID/Passport Number"] = id_num_entry.get()
                                self.df.at[x, "Vehicle ID"] = str(vehicle_id_entry.get())
                                self.df.at[x, "Payment-Method"] = selected_pay_type.get()

                                if hasattr(self, 'photo_paths'):
                                    self.df.at[x, 'Receipt Photos'] = self.photo_paths
                                else:
                                    pass

                                self.toggle_button_colors(1, selected_receipt_photos_button)
                                clear_entries()

                                refresh_tree()
                            else:
                                if len(none_foundlist) > 0:
                                    warning = "Client and/or Vehicle not found in the Database"
                                    self.pop_warning(new_window, warning, "clientorvehiclenotindb")  

                                wrong_date_format = []
                                for date in dates_to_check:
                                    if bool(re.match(pattern, date)) == False:
                                        wrong_date_format.append(date)
                                        self.pop_warning(new_window, wrong_date_format, "wrongdatetextformat")
                               

                                for key in must_not_be_empty:
                                    if key in is_empty:
                                        entry_value = must_not_be_empty[key][1]
                                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    else:
                                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                                for key in must_be_defined:
                                    if key in not_defined:
                                        combobox_value = must_be_defined[key][1]
                                        self.toggle_combo_text(0, must_be_defined[key][1])
                                    else:
                                        self.toggle_combo_text(1, must_be_defined[key][1])

                                for key in must_not_have_number:
                                    if key in not_alpha or key in is_empty:
                                        entry_value = must_not_have_number[key][1]
                                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_not_have_number[key][1])



                                if "Photos" in is_empty:
                                    self.toggle_button_colors(0, select_photos_button)
                                    self.red_bind_hover_effects(select_photos_button)
                                else:
                                    self.toggle_button_colors(1, select_photos_button)
                                    self.bind_hover_effects(select_photos_button)


                                for key in must_be_number:
                                    if key in not_num or key in is_empty:
                                        entry_value = must_be_number[key][1]
                                        self.toggle_entry_colors(0, must_be_number[key][1])
                                    else:
                                        self.toggle_entry_colors(1, must_be_number[key][1])

                                errors_adding = []
                                for error_list in errors_found:
                                    if len(error_list) > 1:
                                        errors_adding.append(error_list)
                                if len(errors_adding) > 0:
                                    self.pop_warning(new_window, errors_adding, "addrecvalidation")
                        else:
                            warning = "Must select an item to Update"
                            self.pop_warning(new_window, warning, "noselectedtoupdate" )

                        refresh_tree()

                    def remove_selected():
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            print(selected_items)
                            for record in selected_items:
                                x = treeview.index(record)
                                treeview.delete(record)
                                self.df.drop(index=x, inplace=True)
                                self.df.reset_index(drop=True, inplace=True)
                            verify_data()
                        else:
                            warning = "Must select at least one record to remove"
                            self.pop_warning(new_window, warning, "noselectedtoremove")

                    def add_selected_to_database():
                        global errors_found
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            invalid_records = []
                            valid_records = []
                            for record in selected_items:
                                x = treeview.index(record)

                                must_be_number = {
                                        'ID/Passport Number': (str(self.df.at[x, "ID/Passport Number"]))
                                    }

                                must_not_have_number = {}

                                must_be_defined = {
                                        'Payment-Method' : (str(self.df.at[x, "Payment-Method"]), pay_types)
                                    }

                                must_not_be_empty = {
                                        'Vehicle ID': (str(self.df.at[x, "Vehicle ID"])),
                                        'ID/Passport Number': (str(self.df.at[x, "ID/Passport Number"]))
                                    }


                                self.validate_data("data_add_database", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                                photos_of_selected = str(self.df.at[x, "Receipt Photos"])

                                if photos_of_selected.lower() != "nan":

                                    self.verify_photo_path(photos_of_selected)

                                    if len(valid_photo_type) > 0:
                                        if len(valid_photo_paths) > 0:
                                            pass
                                        if len(invalid_photo_paths) > 0:
                                            invalid_photo_paths.insert(0, "Invalid Photo Paths")
                                            errors_found = errors_found + (invalid_photo_paths,)

                                    if len(invalid_photo_type) > 0:
                                        invalid_photo_type.insert(0, "Invalid Photo Type")
                                        errors_found = errors_found + (invalid_photo_type,)
                                else:
                                    is_empty.append("Photos")

                                if any(len(error_list) > 1 for error_list in errors_found):
                                    errors_found = tuple(str(x)) + errors_found
                                    invalid_records.append(errors_found)
                                else:
                                    valid_records.append(x)
                                    result_of_validation = "No Error Found"

                            must_not_repeat = ['Vehicle ID']

                            all_that_repeated = []
                            for must_not in must_not_repeat:
                                if len(valid_records) > 0:
                                    valid_records, warning_repeated = self.check_if_repeated(valid_records, must_not)
                                    if len(warning_repeated[0]) > 0:
                                        all_that_repeated.append(warning_repeated)
                                else:
                                    print("Valid records is empty")

                            for warning in all_that_repeated:
                                for index in warning[0]:
                                    try:
                                        valid_records.remove(index)
                                    except ValueError:
                                        pass

                            if len(all_that_repeated) > 0:
                                self.pop_warning(new_window, all_that_repeated, "treerepeatedvalues")

                            record_wrong_format = []
                            wrong_text_format = []
                            for record in valid_records:
                                date_pick_check = str(self.df.at[record, "Pick-up Date"])
                                date_drop_check = str(self.df.at[record, "Drop-off Date"])

                                dates_to_check = [date_pick_check, date_drop_check]
                                pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                                if any(bool(re.match(pattern, date)) == False for date in dates_to_check):
                                    wrong_text_format.append(date_to_check)
                                    record_wrong_format.append(record)

                            if len(wrong_text_format) > 0:
                                self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")
                                for record in record_wrong_format:
                                    valid_records.remove(record)

                            record_none_found = []
                            none_foundcount = 0
                            none_foundlist = []
                            for record in valid_records:
                                cleaned_id_number = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'ID/Passport Number']).lower())
                                existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first()

                                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'Vehicle ID']).lower())
                                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                                must_exist = [[existing_client, "client", cleaned_id_number], [existing_cleaned_vehicle, "vehicle", cleaned_vehicle_plate_id_num]]
                                error = False
                                for must in must_exist:
                                    if must[0] == None:
                                        if must[2] not in none_foundlist:
                                            none_foundlist.append(must[2])
                                            error = True
                                        
                                if error == True:
                                    none_foundcount += 1
                                    record_none_found.append(record)
                            result_found = [none_foundcount, none_foundlist]

                            if len(none_foundlist) > 0:
                                self.pop_warning(new_window, result_found, "manyclientorvehiclenotindb")
                                for record in record_none_found:
                                    valid_records.remove(record)

                            not_available = []
                            for record in valid_records:
                                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'Vehicle ID']).lower())
                                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()
                                if existing_cleaned_vehicle.availability == "Unavailable":
                                    drop_off_date = datetime.strptime(str(self.df.at[record, "Drop-off Date"]), "%Y-%m-%d").date()
                                    current_date = datetime.now().date()
                                    if drop_off_date < current_date:
                                        print("drop is before current")
                                    else:
                                        not_available.append(record)

                            if len(not_available) > 0:
                                self.pop_warning(new_window, not_available, "somevehiclenotavailable")
                                for record in not_available:
                                    valid_records.remove(record)

                            date_has_exceeded = []
                            for record in valid_records:
                                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'Vehicle ID']).lower())
                                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()
                                date_next_inspection = datetime.strptime(existing_cleaned_vehicle.next_inspection, "%Y-%m-%d")
                                date_next_legalization = datetime.strptime(existing_cleaned_vehicle.next_legalization, "%Y-%m-%d")
                                drop = datetime.strptime(str(self.df.at[record, "Drop-off Date"]), "%Y-%m-%d")

                                if drop >= date_next_inspection or drop >= date_next_legalization:
                                    date_has_exceeded.append(record)

                            if len(date_has_exceeded) > 0:
                                self.pop_warning(new_window, date_has_exceeded, "dropdateexceeds")
                                for record in date_has_exceeded:
                                    valid_records.remove(record)

                            not_valid_license_record = []
                            not_valid_license = []
                            for record in valid_records:
                                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'Vehicle ID']).lower())
                                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()
                                cleaned_id_number = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'ID/Passport Number']).lower())
                                existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first()

                                vehicle_cc = existing_cleaned_vehicle.cc
                                client_motorcycle_license = existing_client.m_license
                                vehicle_type = existing_cleaned_vehicle.vehicle_type

                                not_valid = False

                                if client_motorcycle_license == "A1(125cc|11kw|0.1kw/kg)":
                                    cc_list_class = ["<= 50 (11kw)", "51 - 125 (11kw)"]
                                    if vehicle_cc not in cc_list_class:
                                        not_valid = True
                                elif client_motorcycle_license == "A2(max-35kw|0.2kw/kg)":
                                    cc_list_class = ["<= 50 (35kw)", "51 - 125 (35kw)", "126 - 500 (35kw)", "501 - 1000 (35kw)", ">= 1000 (35kw)"]
                                    if vehicle_cc not in cc_list_class:
                                        not_valid = True
                                elif client_motorcycle_license == "Not Applicable":
                                    if vehicle_type.lower() == "motorcycles":
                                        not_valid = True

                                if not_valid == True:
                                    not_valid_info = f"Client id number: {cleaned_id_number}, motorcyle license class is: {client_motorcycle_license}"
                                    not_valid_license.append(not_valid_info)
                                    not_valid_license_record.append(record)


                            if len(not_valid_license) > 0:
                                self.pop_warning(new_window, not_valid_license, 'notvalidlicenseclass')
                                for record in not_valid_license_record:
                                    valid_records.remove(record)

                            if len(valid_records) > 0:
                                code_check=self.check_employee_code(str(employee_code_entry.get()), False)
                                if code_check == "valid":
                                    self.toggle_entry_colors(1, employee_code_entry)

                                    valid_df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle ID', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                                      'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                                      'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Receipt Photos'])

                                    for record in valid_records:
                                        cleaned_id_number = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'ID/Passport Number']).lower())
                                        existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                                        cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(self.df.at[record, 'Vehicle ID']).lower())
                                        existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                                        date_pick_check = str(self.df.at[record, 'Pick-up Date'])
                                        date_drop_check = str(self.df.at[record, 'Drop-off Date'])

                                        date_format = "%Y-%m-%d"
                                        date_pick = datetime.strptime(date_pick_check, date_format)
                                        date_drop = datetime.strptime(date_drop_check, date_format)

                                        duration = date_drop - date_pick

                                        duration = duration.days

                                        if existing_cleaned_vehicle.category.lower() == 'gold':
                                            cost_day = 120
                                        elif existing_cleaned_vehicle.category.lower() == 'silver':
                                            cost_day = 80
                                        else:
                                            cost_day = 40

                                        duration += 1

                                        total = duration * cost_day
                                                      
                                        new_df_record = {
                                            'Pick-up Date': self.df.at[record, 'Pick-up Date'],
                                            'Drop-off Date': self.df.at[record, 'Drop-off Date'],
                                            'Vehicle ID': existing_cleaned_vehicle.license_plate, 
                                            'Rental Duration': int(duration), 
                                            'Cost Per Day': int(cost_day), 
                                            'Total Cost': int(total),
                                            'Full Name': existing_client.f_name, 
                                            'Phone Number': existing_client.p_number, 
                                            'Email': existing_client.email, 
                                            'ID/Passport Number': existing_client.id_number,
                                            'Date of Birth': existing_client.dob, 
                                            'Nationality': existing_client.nationality, 
                                            'Emergency Contact Name': existing_client.em_name,
                                            'Emergency Contact Number': existing_client.em_number, 
                                            'Billing Address': existing_client.bill_address, 
                                            'Payment-Method': self.df.at[record, 'Payment-Method'],
                                            'Receipt Photos': self.df.at[record, 'Receipt Photos']
                                        }

                                        new_df_record = pd.DataFrame([new_df_record])  # Convert to DataFrame with a single row

                                        valid_df = pd.concat([valid_df, new_df_record], ignore_index=True)

                                    def handle_choice(option, valid_df):
                                        if option == "confirm":
                                            try:
                                                for index, row in valid_df.iterrows():
                                                    def create_payment_record():
                                                        payment_record = Payment(
                                                            total_pay = int(row['Total Cost']),
                                                            payment_method = row['Payment-Method'], 
                                                            f_name = row['Full Name'],
                                                            p_number = int(row['Phone Number']),
                                                            id_number = int(row['ID/Passport Number']),
                                                            bill_address = row['Billing Address'], 
                                                            vehicle_id = row['Vehicle ID'], 
                                                            photos = row['Receipt Photos'],
                                                            code_insertion = str(employee_code_entry.get())
                                                            )

                                                        db.session.add(payment_record)

                                                        db.session.commit()

                                                    def update_vehicle_state():
                                                        vehicle = Vehicle.query.filter_by(license_plate=row['Vehicle ID']).first()
                                                        vehicle.availability = "Unavailable"
                                                        vehicle.rented = "Yes"
                                                        vehicle.code_rented = str(employee_code_entry.get())
                                                        db.session.commit()

                                                    def update_client_state():
                                                        client = Client.query.filter_by(id_number=row['ID/Passport Number']).first()
                                                        client.renting = "Yes"
                                                        client.code_renting = str(employee_code_entry.get())
                                                        db.session.commit()

                                                    with self.flask_app.app_context():
                                                        db.create_all()

                                                        drop_off_date = datetime.strptime(str(row['Drop-off Date']), "%Y-%m-%d").date()
                                                        current_date = datetime.now().date()

                                                        if drop_off_date < current_date:
                                                            reservation = Reservation(
                                                                pick_up_date = str(row['Pick-up Date']),
                                                                drop_off_date = str(row['Drop-off Date']),
                                                                vehicle_id = row['Vehicle ID'],
                                                                rental_duration = int(row['Rental Duration']),
                                                                cost_per_day = int(row['Cost Per Day']),
                                                                total_cost = int(row['Total Cost']),
                                                                full_name = row['Full Name'],
                                                                phone_number = int(row['Phone Number']),
                                                                email = row['Email'],
                                                                id_passport_number = int(row['ID/Passport Number']),
                                                                date_of_birth = str(row['Date of Birth']),
                                                                nationality = row['Nationality'],
                                                                emergency_contact_name = row['Emergency Contact Name'],
                                                                emergency_contact_number = int(row['Emergency Contact Number']),
                                                                billing_address = row['Billing Address'],
                                                                payment_method = row['Payment-Method'],
                                                                photos = row['Receipt Photos'],
                                                                code_insertion = str(employee_code_entry.get()),
                                                                reservation_state = "Completed",
                                                                date_confirm_completed_renting = str(row['Drop-off Date']),
                                                                code_confirm_completed_renting = str(employee_code_entry.get())
                                                            )
                                                        else:
                                                            reservation = Reservation(
                                                                pick_up_date = str(row['Pick-up Date']),
                                                                drop_off_date = str(row['Drop-off Date']),
                                                                vehicle_id = row['Vehicle ID'],
                                                                rental_duration = int(row['Rental Duration']),
                                                                cost_per_day = int(row['Cost Per Day']),
                                                                total_cost = int(row['Total Cost']),
                                                                full_name = row['Full Name'],
                                                                phone_number = int(row['Phone Number']),
                                                                email = row['Email'],
                                                                id_passport_number = int(row['ID/Passport Number']),
                                                                date_of_birth = str(row['Date of Birth']),
                                                                nationality = row['Nationality'],
                                                                emergency_contact_name = row['Emergency Contact Name'],
                                                                emergency_contact_number = int(row['Emergency Contact Number']),
                                                                billing_address = row['Billing Address'],
                                                                payment_method = row['Payment-Method'],
                                                                photos = row['Receipt Photos'],
                                                                code_insertion = str(employee_code_entry.get())
                                                            )
                                                        
                                                        db.session.add(reservation)

                                                        db.session.commit()


                                                        if drop_off_date < current_date:
                                                            print("drop is before current")
                                                        else:
                                                            update_vehicle_state()
                                                            update_client_state()


                                                        create_payment_record()

                                                clear_entries()
                                            except OperationalError as e:
                                                warning = "Database is locked. Please close the Database and try again."
                                                self.pop_warning(new_window, warning, "databaselocked")
                                                db.session.rollback()
                                                print("Database is locked. Please try again later.")
                                        
                                        elif option == "cancel":
                                            print("User canceled")

                                    self.pop_warning(new_window, valid_df, "dfdatabvalidadd", lambda option: handle_choice(option, valid_df))
                                else:
                                    self.pop_warning(new_window, code_check, "wrongemployeecode")
                                    self.toggle_entry_colors(0, employee_code_entry)
                            if len(invalid_records) > 0:
                                if len(wrong_text_format) > 0:
                                    self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                                self.pop_warning(new_window, invalid_records, "databinvalidadd")

                    def add_record():
                        must_be_number = {
                                'ID/Passport Number': (id_num_entry.get(), id_num_entry)
                            }

                        must_not_have_number = {}

                        must_be_defined = {
                                'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
                        }

                        must_not_be_empty = {
                                'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                                'ID/Passport Number': (id_num_entry.get(), id_num_entry),
                                'Pick-up Date': (pick_entry.get(), pick_entry),
                                'Drop-off Date': (drop_entry.get(), drop_entry)
                            }

                        self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                        if hasattr(self, 'photo_paths'):
                            self.toggle_button_colors(1, select_photos_button)
                        else:
                            is_empty.append("Photos")

                        date_pick_check = str(pick_entry.get())
                        date_drop_check = str(drop_entry.get())

                        dates_to_check = [date_pick_check, date_drop_check]
                        pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                        cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                        existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                        cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                        existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                        must_exist = [[existing_client, "client"], [existing_cleaned_vehicle, "vehicle"]]
                        none_foundlist = []
                        for must in must_exist:
                            if must[0] == None:
                                none_foundlist.append(must[1]) 

                        if any(len(error_list) > 1 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or len(none_foundlist) > 0: 
                            result_of_validation = "Error Found"
                        else:
                            result_of_validation = "No Error Found"

                        if result_of_validation == "No Error Found":

                            def handle_choice(option, possible_new_record):
                                if option == "confirm":
                                    new_record = pd.DataFrame(possible_new_record)
                                    self.df = pd.concat([self.df, new_record], ignore_index=True)

                                    clear_entries()

                                    self.df.reset_index(drop=True, inplace=True)

                                    refresh_tree()
                                elif option == "cancel":
                                    print("User canceled")

                            possible_new_record = {
                            'Pick-up Date': [pick_entry.get()],
                            'Drop-off Date': [drop_entry.get()],
                            'ID/Passport Number': [int(id_num_entry.get())],
                            'Vehicle ID': [vehicle_id_entry.get()],
                            'Payment-Method': [selected_pay_type.get()],
                            'Receipt Photos': self.photo_paths
                            }

                            self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                        else:
                            if len(none_foundlist) > 0:
                                self.pop_warning(new_window, none_foundlist, "clientorvehiclenotindb")  

                            wrong_date_format = []
                            for date in dates_to_check:
                                if date != "":
                                    if bool(re.match(pattern, date)) == False:
                                        wrong_date_format.append(date)
                                        self.pop_warning(new_window, wrong_date_format, "wrongdatetextformat")

                            for key in must_not_be_empty:
                                if key in is_empty:
                                    entry_value = must_not_be_empty[key][1]
                                    self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                                    if key == "Pick-up Date":
                                        pick_entry.config(readonlybackground="darkred")
                                    if key == "Drop-off Date":
                                        drop_entry.config(readonlybackground="darkred")
                                else:
                                    self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                            for key in must_be_defined:
                                if key in not_defined:
                                    combobox_value = must_be_defined[key][1]
                                    self.toggle_combo_text(0, must_be_defined[key][1])
                                else:
                                    self.toggle_combo_text(1, must_be_defined[key][1])

                            for key in must_not_have_number:
                                if key in not_alpha or key in is_empty:
                                    entry_value = must_not_have_number[key][1]
                                    self.toggle_entry_colors(0, must_not_have_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_not_have_number[key][1])

                            if "Photos" in is_empty:
                                self.toggle_button_colors(0, select_photos_button)
                                self.red_bind_hover_effects(select_photos_button)
                            else:
                                self.toggle_button_colors(1, select_photos_button)
                                self.bind_hover_effects(select_photos_button)

                            for key in must_be_number:
                                if key in not_num or key in is_empty:
                                    entry_value = must_be_number[key][1]
                                    self.toggle_entry_colors(0, must_be_number[key][1])
                                else:
                                    self.toggle_entry_colors(1, must_be_number[key][1])

                            errors_adding = []
                            for error_list in errors_found:
                                if len(error_list) > 1:
                                    errors_adding.append(error_list)

                            if len(errors_adding) > 0:
                                self.pop_warning(new_window, errors_adding, "addrecvalidation")                        

                    def remove_all():
                        for record in treeview.get_children():
                            x = treeview.index(record)
                            treeview.delete(record)
                            self.df.drop(index=x, inplace=True)
                            self.df.reset_index(drop=True, inplace=True)

                    def selected_receipt_photos():
                        selected_items = treeview.selection()
                        print(selected_items)
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            photos_of_selected = str(self.df.at[x, "Receipt Photos"])

                            if photos_of_selected.lower() != "nan":

                                self.verify_photo_path(photos_of_selected)

                                if len(valid_photo_type) > 0:
                                    print(valid_photo_type)
                                    if len(valid_photo_paths) > 0:
                                        def handle_photo_viewer_result(result, updated_photos):
                                            if result == "confirm":
                                                self.df.at[x, 'Receipt Photos'] = updated_photos
                                            elif result == "cancel":
                                                print("User cancelled changes")

                                        updated_photos = []
                                        self.photo_viewer(new_window, valid_photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos)
                                    if len(invalid_photo_paths) > 0:
                                        self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                        self.toggle_button_colors(0, selected_receipt_photos_button)
                                print(invalid_photo_type)
                                for path in invalid_photo_type:
                                    if path == "":
                                        invalid_photo_type.remove(path)
                                if len(invalid_photo_type) > 0:
                                    self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                                    self.toggle_button_colors(0, selected_receipt_photos_button)
                            else:
                                x += 1
                                self.pop_warning(new_window, str(x), "nanselectedphoto")
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                        else:
                            warning = "Must select a record to see photos"
                            self.pop_warning(new_window, warning, "noselectedtoseephotos")

                    refresh_tree()

                    treeview.pack(expand=True, fill="both")

                    add_record_button = Button(edit_treeview_frame, text="Add Record to Data Frame", fg="white",
                                               bg="black",
                                               command=add_record)
                    add_record_button.grid(row=0, column=0, padx=5, pady=3)
                    self.bind_hover_effects(add_record_button)

                    add_record_database = Button(edit_treeview_frame, text="Add Selected Record(s) to Database", fg="white",
                                               bg="darkgreen",
                                               command=add_selected_to_database)
                    add_record_database.grid(row=1, column=0, columnspan=7, padx=10, pady=5)
                    self.green_bind_hover_effects(add_record_database)

                    update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                           command=update_record)
                    update_button.grid(row=0, column=1, padx=5, pady=3)
                    self.bind_hover_effects(update_button)

                    clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                                  command=clear_entries)
                    clear_entries_button.grid(row=0, column=2, padx=5, pady=3)
                    self.bind_hover_effects(clear_entries_button)

                    selected_receipt_photos_button = Button(edit_treeview_frame, text="See Selected Receipt Photos",
                                                            fg="white",
                                                            bg="black", command=selected_receipt_photos)
                    selected_receipt_photos_button.grid(row=0, column=3, padx=5, pady=3)
                    self.bind_hover_effects(selected_receipt_photos_button)

                    remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                                    bg="black", command=remove_selected)
                    remove_selected_button.grid(row=0, column=4, padx=5, pady=3)
                    self.bind_hover_effects(remove_selected_button)

                    remove_all_button = Button(edit_treeview_frame, text="Remove All Records", fg="white",
                                               bg="black", command=remove_all)
                    remove_all_button.grid(row=0, column=5, padx=5, pady=3)
                    self.bind_hover_effects(remove_all_button)

                    refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                               bg="black", command=refresh_tree)
                    refresh_tree_button.grid(row=0, column=6, padx=5, pady=3)
                    self.bind_hover_effects(refresh_tree_button)

                    treeview.bind("<ButtonRelease-1>", select_record)

                else:
                    missing_heading = [head for head in reservations_headings_lowercase if head not in reservations_file_headings]
                    unmatched_heading = [head for head in reservations_file_headings if head not in reservations_headings_lowercase]
                    missing_unmatched_head = missing_heading, unmatched_heading

                    if len(missing_heading) > 0 and len(unmatched_heading) > 0:
                        self.pop_warning(new_window, missing_unmatched_head, "missingheadunmatched" )
                    elif len(missing_heading) > 0 and len(unmatched_heading) == 0:
                        self.pop_warning(new_window, missing_heading, "missingheading")
                    elif len(missing_heading) == 0 and len(unmatched_heading) > 0:
                        self.pop_warning(new_window, unmatched_heading, "unmatchedheading")

            else:
                print("No file path selected")

        def check_if_df():
            if hasattr(self, 'df'):
                check_reservation_file_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_files_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_check_button.configure(image=self.check_files_image)
            else:
                print("No file selected")

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)

                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)

                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))

                reload_show_photos_button.configure(image=self.update_photos_button_image)

        def add_reservations_db():
            must_be_number = {
                    'ID/Passport Number': (id_num_entry.get(), id_num_entry)
                }

            must_not_have_number = {}

            must_be_defined = {
                    'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
            }

            must_not_be_empty = {
                    'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                    'ID/Passport Number': (id_num_entry.get(), id_num_entry),
                    'Pick-up Date': (pick_entry.get(), pick_entry),
                    'Drop-off Date': (drop_entry.get(), drop_entry)
                }

            self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

            if hasattr(self, 'photo_paths'):
                self.toggle_button_colors(1, select_photos_button)
            else:
                is_empty.append("Photos")

            date_pick_check = str(pick_entry.get())
            date_drop_check = str(drop_entry.get())

            dates_to_check = [date_pick_check, date_drop_check]
            pattern = r"\b\d{4}-\d{2}-\d{2}\b"

            cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
            existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
            existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

            must_exist = [[existing_client, "client"], [existing_cleaned_vehicle, "vehicle"]]
            none_foundlist = []
            for must in must_exist:
                if must[0] == None:
                    none_foundlist.append(must[1]) 

            if any(len(error_list) > 1 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or len(none_foundlist) > 0 or existing_cleaned_vehicle.availability == "Unavailable":
                result_of_validation = "Error Found"
            else:
                result_of_validation = "No Error Found"

            if result_of_validation == "No Error Found":
                code_check=self.check_employee_code(str(employee_code_entry.get()), False)
                if code_check == "valid":

                    date_next_inspection = datetime.strptime(existing_cleaned_vehicle.next_inspection, "%Y-%m-%d")
                    date_next_legalization = datetime.strptime(existing_cleaned_vehicle.next_legalization, "%Y-%m-%d")
                    drop = datetime.strptime(drop_entry.get(), "%Y-%m-%d")

                    if drop >= date_next_inspection or drop >= date_next_legalization:
                        warning = "Drop-off date exceeds the inspection or legalization date"
                        self.pop_warning(new_window, warning, "dropdateexceeds")
                    else:
                        vehicle_cc = existing_cleaned_vehicle.cc
                        client_motorcycle_license = existing_client.m_license
                        vehicle_type = existing_cleaned_vehicle.vehicle_type

                        not_valid = False

                        if client_motorcycle_license == "A1(125cc|11kw|0.1kw/kg)":
                            cc_list_class = ["<= 50 (11kw)", "51 - 125 (11kw)"]
                            if vehicle_cc not in cc_list_class:
                                not_valid = True
                        elif client_motorcycle_license == "A2(max-35kw|0.2kw/kg)":
                            cc_list_class = ["<= 50 (35kw)", "51 - 125 (35kw)", "126 - 500 (35kw)", "501 - 1000 (35kw)", ">= 1000 (35kw)"]
                            if vehicle_cc not in cc_list_class:
                                not_valid = True
                        elif client_motorcycle_license == "Not Applicable":
                            if vehicle_type.lower() == "motorcycles":
                                not_valid = True
                        if not_valid == True:
                            client_license = f"Client license class: {client_motorcycle_license}"
                            self.pop_warning(new_window, client_license, "ccnotvalidlicense")
                        else:
                            self.toggle_entry_colors(1, employee_code_entry)
                            self.toggle_combo_text(1, pay_type_combobox)

                            read_only_entries = [pick_entry, drop_entry, rent_duration_entry, cost_day_entry, cost_total_entry, 
                            full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]
                            
                            for entry in read_only_entries:
                                entry.config(readonlybackground="#313131")

                            self.toggle_entry_colors(1, vehicle_id_entry)
                            self.toggle_entry_colors(1, id_num_entry)

                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                            def handle_choice(option, possible_new_record):
                                if option == "confirm":
                                    try:
                                        def create_payment_record():
                                            payment_record = Payment(
                                                total_pay = int(total),
                                                payment_method = selected_pay_type.get(),
                                                f_name = existing_client.f_name,
                                                p_number = existing_client.p_number,
                                                id_number = existing_client.id_number,
                                                bill_address = existing_client.bill_address, 
                                                vehicle_id = cleaned_vehicle_plate_id_num,
                                                photos = self.photo_paths,
                                                code_insertion = str(employee_code_entry.get())
                                                )

                                            db.session.add(payment_record)
                                            db.session.commit()

                                        def update_vehicle_state():
                                            vehicle = Vehicle.query.filter_by(license_plate=cleaned_vehicle_plate_id_num).first()
                                            vehicle.availability = "Unavailable"
                                            vehicle.rented = "Yes"
                                            vehicle.code_rented = str(employee_code_entry.get())
                                            db.session.commit()

                                        def update_client_state():
                                            client = Client.query.filter_by(id_number=existing_client.id_number).first()
                                            client.renting = "Yes"
                                            client.code_renting = str(employee_code_entry.get())
                                            db.session.commit()

                                        with self.flask_app.app_context():
                                            db.create_all()

                                            reservation = Reservation(
                                                pick_up_date = str(pick_entry.get()),
                                                drop_off_date = str(drop_entry.get()),
                                                vehicle_id = cleaned_vehicle_plate_id_num,
                                                rental_duration = int(duration),
                                                cost_per_day = int(cost_day),
                                                total_cost = int(total),
                                                full_name = existing_client.f_name,
                                                phone_number = existing_client.p_number,
                                                email = existing_client.email,
                                                id_passport_number = existing_client.id_number,
                                                date_of_birth = existing_client.dob,
                                                nationality = existing_client.nationality,
                                                emergency_contact_name = existing_client.em_name,
                                                emergency_contact_number = existing_client.em_number,
                                                billing_address = existing_client.bill_address,
                                                payment_method = selected_pay_type.get(),
                                                photos = self.photo_paths,
                                                code_insertion = str(employee_code_entry.get())
                                            )

                                            db.session.add(reservation)
                                            db.session.commit()

                                            update_vehicle_state()
                                            update_client_state()
                                            create_payment_record()

                                            entries = [id_num_entry, vehicle_id_entry, employee_code_entry]
                                            for entry in entries:
                                                entry.delete(0, END)
                                                self.toggle_entry_colors(1, entry)

                                            read_only_entries = [pick_entry, drop_entry, rent_duration_entry, cost_day_entry, cost_total_entry, 
                                            full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                                            for entry in read_only_entries:
                                                entry.config(state=tk.NORMAL)
                                                entry.delete(0, tk.END)
                                                entry.config(state="readonly", readonlybackground="#313131")

                                            combos = [[pay_type_combobox, pay_types]]
                                            for combo in combos:
                                                self.toggle_combo_text(1, combo[0])
                                                combo[0].set(combo[1][0])

                                            del self.photo_paths

                                            check_if_photos()
                                    except OperationalError as e:
                                        warning = "Database is locked. Please close the Database and try again."
                                        self.pop_warning(new_window, warning, "databaselocked")
                                        db.session.rollback()
                                        print("Database is locked. Please try again later.")

                                elif option == "cancel":
                                    print("User canceled")

                            cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                            existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                            existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                            date_pick_check = str(pick_entry.get())
                            date_drop_check = str(drop_entry.get())

                            date_format = "%Y-%m-%d"
                            date_pick = datetime.strptime(date_pick_check, date_format)
                            date_drop = datetime.strptime(date_drop_check, date_format)

                            duration = date_drop - date_pick

                            duration = duration.days

                            if existing_cleaned_vehicle.category.lower() == 'gold':
                                cost_day = 120
                            elif existing_cleaned_vehicle.category.lower() == 'silver':
                                cost_day = 80
                            else:
                                cost_day = 40

                            duration += 1
                            total = duration * cost_day

                            possible_new_record = {
                            'Pick-up Date': [pick_entry.get()],
                            'Drop-off Date': [drop_entry.get()],
                            'Vehicle ID': [vehicle_id_entry.get()], 
                            'Rental Duration': [duration], 
                            'Cost Per Day': [cost_day], 
                            'Total Cost': [total],
                            'Full Name': [existing_client.f_name], 
                            'Phone Number': [existing_client.p_number], 
                            'Email': [existing_client.email], 
                            'ID/Passport Number': [int(id_num_entry.get())],
                            'Date of Birth': [existing_client.dob], 
                            'Nationality': [existing_client.nationality], 
                            'Emergency Contact Name': [existing_client.em_name],
                            'Emergency Contact Number': [existing_client.em_number], 
                            'Billing Address': [existing_client.bill_address], 
                            'Payment-Method': [selected_pay_type.get()],
                            'Receipt Photos': self.photo_paths,
                            }

                            self.pop_warning(new_window, possible_new_record, "validateaddrecord", lambda option: handle_choice(option, possible_new_record))
                else:
                    self.pop_warning(new_window, code_check, "wrongemployeecode")
                    self.toggle_entry_colors(0, employee_code_entry)
            else:
                if existing_cleaned_vehicle is not None:
                    if existing_cleaned_vehicle.availability == "Unavailable":
                        warning = "The desired vehicle is currently Unavailable"
                        self.pop_warning(new_window, warning, "vehiclenotavailable")

                if len(none_foundlist) > 0:
                    warning = "Client and/or Vehicle not found in the Database"
                    self.pop_warning(new_window, warning, "clientorvehiclenotindb")  

                wrong_date_format = []
                for date in dates_to_check:
                    if date != "":
                        if bool(re.match(pattern, date)) == False:
                            wrong_date_format.append(date)
                            self.pop_warning(new_window, wrong_date_format, "wrongdatetextformat")

                for key in must_not_be_empty:
                    if key in is_empty:
                        entry_value = must_not_be_empty[key][1]
                        self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                        if key == "Pick-up Date":
                            pick_entry.config(readonlybackground="darkred")
                        if key == "Drop-off Date":
                            drop_entry.config(readonlybackground="darkred")
                    else:
                        self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                for key in must_be_defined:
                    if key in not_defined:
                        combobox_value = must_be_defined[key][1]
                        self.toggle_combo_text(0, must_be_defined[key][1])
                    else:
                        self.toggle_combo_text(1, must_be_defined[key][1])

                for key in must_not_have_number:
                    if key in not_alpha or key in is_empty:
                        entry_value = must_not_have_number[key][1]
                        self.toggle_entry_colors(0, must_not_have_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_not_have_number[key][1])

                if "Photos" in is_empty:
                    self.toggle_button_colors(0, select_photos_button)
                    self.red_bind_hover_effects(select_photos_button)
                else:
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                for key in must_be_number:
                    if key in not_num or key in is_empty:
                        entry_value = must_be_number[key][1]
                        self.toggle_entry_colors(0, must_be_number[key][1])
                    else:
                        self.toggle_entry_colors(1, must_be_number[key][1])

                errors_adding = []
                for error_list in errors_found:
                    if len(error_list) > 1:
                        errors_adding.append(error_list)

                if len(errors_adding) > 0:
                    self.pop_warning(new_window, errors_adding, "addrecvalidation")

        insert_reservation_frame = tk.Frame(new_window)
        insert_reservation_frame.configure(bg="black")
        insert_reservation_frame.pack(pady=(0,10))


        # Function to calculate the cost of the reservation, based on the duration and category of the vehicle and then fills the entry boxes with the respective
        def costs_of_rent(*args):
            try:
                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()
                cost_entries = [rent_duration_entry, cost_day_entry, cost_total_entry]
          
                if existing_cleaned_vehicle:
                    vehicle_id_entry.config(bg="#313131")
                    cost_entries = [rent_duration_entry, cost_day_entry, cost_total_entry]
          
                    for entry in cost_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)

                    date_pick_check = pick_entry.get()
                    date_drop_check = drop_entry.get()

                    date_format = "%Y-%m-%d"
                    date_pick = datetime.strptime(date_pick_check, date_format)
                    date_drop = datetime.strptime(date_drop_check, date_format)

                    rent_duration_entry.config(readonlybackground="#313131")
                    cost_day_entry.config(readonlybackground="#313131")
                    cost_total_entry.config(readonlybackground="#313131")

                    difference = date_drop - date_pick

                    difference = int(difference.days) + 1
                    rent_duration_entry.insert(0, difference)
                    
                    if existing_cleaned_vehicle.category.lower() == 'gold':
                        cost_day_entry.insert(0, 120)
                        total = int(difference) * 120
                        cost_total_entry.insert(0, int(total))
                    elif existing_cleaned_vehicle.category.lower() == 'silver':
                        cost_day_entry.insert(0, 80)
                        total = int(difference) * 80
                        cost_total_entry.insert(0, int(total))
                    elif existing_cleaned_vehicle.category.lower() == 'economic':
                        cost_day_entry.insert(0, 40)
                        total = int(difference) * 40
                        cost_total_entry.insert(0, int(total))

                    for entry in cost_entries:
                        entry.config(state="readonly")
                else:
                    for entry in cost_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)
                        entry.config(readonlybackground="darkred")
                    for entry in cost_entries:
                        entry.config(state="readonly")
                    vehicle_id_entry.config(bg="darkred")
            except ValueError:
                pass

        # Function to retrieve the data of the selected client and then fills the entry boxes with the respective information
        def client_info(*args):
            try:
                cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 
                client_entries = [full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                if existing_client:
                    id_num_entry.config(bg="#313131")

                    for entry in client_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)

                    full_name_entry.insert(0, str(existing_client.f_name))
                    phone_entry.insert(0, int(existing_client.p_number))
                    email_entry.insert(0, str(existing_client.email))
                    dob_entry.insert(0, str(existing_client.dob))
                    em_name_entry.insert(0, str(existing_client.em_name))
                    em_num_entry.insert(0, int(existing_client.em_number))
                    bill_address_entry.insert(0, str(existing_client.bill_address))
                    nationality_entry.insert(0, str(existing_client.nationality))

                    for entry in client_entries:
                        entry.config(state="readonly")
                        entry.config(readonlybackground="#313131")
                else:
                    for entry in client_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)
                    for entry in client_entries:
                        entry.config(state="readonly")
                        entry.config(readonlybackground="darkred")

                    id_num_entry.config(bg="darkred")
            except ValueError:
                pass

        employee_code_label = tk.Label(insert_reservation_frame, text="Employee Code:",
                          font=("Helvetica", 10), fg="white", bg="black")
        employee_code_label.grid(row=0, column=5, pady=(0,5), padx=5, sticky=tk.E)

        employee_code_entry = tk.Entry(insert_reservation_frame, bd=2, width=10)
        employee_code_entry.grid(row=0, column=6, padx=5, pady=(0,3))

        upload_reservation_file_button = tk.Button(insert_reservation_frame, text="Upload Reservation File", width=20,
                                               borderwidth=2,
                                               fg="white", bg="black", command=lambda: self.load_data(new_window))
        upload_reservation_file_button.grid(row=1, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(upload_reservation_file_button)

        check_reservation_file_button = tk.Button(insert_reservation_frame, text="Check Data", width=15, borderwidth=2,
                                              fg="white", bg="black", state=tk.DISABLED, command=check_data)
        check_reservation_file_button.grid(row=1, column=5, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(check_reservation_file_button)

        # Load the update button image
        update_files_button_image_path = resource_path('resources/update.png')
        self.update_files_button_image = ImageTk.PhotoImage(Image.open(update_files_button_image_path))
        reload_check_button = tk.Button(insert_reservation_frame, image=self.update_files_button_image, command=check_if_df,
                                        borderwidth=0, highlightthickness=0)
        reload_check_button.grid(row=1, column=6, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_check_button)

        select_vehicle_button = tk.Button(insert_reservation_frame, text="Select Vehicle", width=20, borderwidth=2,
                                              fg="white", bg="black")

        select_vehicle_button.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_vehicle_button)

                        # Date of Birth Entry
        select_client_button = tk.Button(insert_reservation_frame, text="Select Client", width=15, borderwidth=2,
                                              fg="white", bg="black")

        select_client_button.grid(row=1, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_client_button)

        pick_button = tk.Button(insert_reservation_frame, text="Select the Pick-up Date", width=20, borderwidth=2,
                                              fg="white", bg="black", command=lambda: self.datepicker(new_window, pick_entry, "reservation", drop_button))

        pick_button.grid(row=2, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(pick_button)
        pick_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        pick_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        pick_entry.bind("<KeyRelease>", costs_of_rent)

        drop_button = tk.Button(insert_reservation_frame, text="Select the Drop-off Date", width=20, borderwidth=2,
                                              fg="white", bg="black", state=DISABLED, command=lambda: self.datepicker(new_window, drop_entry, "reservation", drop_button, pick_entry.get(), costs_of_rent))

        drop_button.grid(row=3, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(drop_button)
        drop_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        drop_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        drop_entry.bind("<KeyRelease>", costs_of_rent)

        vehicle_id_label = tk.Label(insert_reservation_frame, text="Vehicle ID:",
                               font=("Helvetica", 10), fg="white", bg="black")
        vehicle_id_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        vehicle_id_entry = tk.Entry(insert_reservation_frame, bd=2, width=10)
        vehicle_id_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        vehicle_id_entry.bind("<KeyRelease>", costs_of_rent)

        rent_duration_label = tk.Label(insert_reservation_frame, text="Rental duration:",
                               font=("Helvetica", 10), fg="white", bg="black")
        rent_duration_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        rent_duration_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        rent_duration_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        cost_day_label = tk.Label(insert_reservation_frame, text="Cost per day:",
                               font=("Helvetica", 10), fg="white", bg="black")
        cost_day_label.grid(row=6, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        cost_day_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        cost_day_entry.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        cost_total_label = tk.Label(insert_reservation_frame, text="Total cost:",
                               font=("Helvetica", 10), fg="white", bg="black")
        cost_total_label.grid(row=7, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        cost_total_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        cost_total_entry.grid(row=7, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        full_name_label = tk.Label(insert_reservation_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        full_name_label.grid(row=2, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        full_name_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(insert_reservation_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_label.grid(row=3, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        phone_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(insert_reservation_frame, text="Email:",
                               font=("Helvetica", 10), fg="white", bg="black")
        email_label.grid(row=4, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        email_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)


        id_num_label = tk.Label(insert_reservation_frame, text="ID/Passport Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        id_num_label.grid(row=5, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        id_num_entry = tk.Entry(insert_reservation_frame, bd=2, width=10)
        id_num_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        id_num_entry.bind("<KeyRelease>", client_info)

        dob_label = tk.Label(insert_reservation_frame, text="Date of Birth:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        dob_label.grid(row=6, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        dob_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        dob_entry.grid(row=6, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        nationality_label = tk.Label(insert_reservation_frame, text="Nationality:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        nationality_label.grid(row=2, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        nationality_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        nationality_entry.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        em_name_label = tk.Label(insert_reservation_frame, text="Emergency Contact Name:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        em_name_label.grid(row=3, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        em_name_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        em_name_entry.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        em_num_label = tk.Label(insert_reservation_frame, text="Emergency Contact Number:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        em_num_label.grid(row=4, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        em_num_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        em_num_entry.grid(row=4, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        bill_address_label = tk.Label(insert_reservation_frame, text="Billing Address:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        bill_address_label.grid(row=5, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        bill_address_entry = tk.Entry(insert_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        bill_address_entry.grid(row=5, column=5, pady=5, padx=(5, 10), sticky=tk.W)     

        pay_method_label = tk.Label(insert_reservation_frame, text="Payment-Method:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        pay_method_label.grid(row=6, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        pay_types = ["Not Defined", "Cash", "Credit Card", "Paypal", "Bank Transfer", "Google Pay", "Apple Pay"]
        selected_pay_type = tk.StringVar()
        pay_type_combobox = ttk.Combobox(insert_reservation_frame,
                                        textvariable=selected_pay_type,
                                        values=pay_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        pay_type_combobox.grid(row=6, column=5, pady=5, padx=(5, 10), sticky=tk.W)
        pay_type_combobox.set(pay_types[0]) 

        select_photos_button = tk.Button(insert_reservation_frame, text="Select Receipt Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=7, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)

        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(insert_reservation_frame, text="See Receipt Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=7, column=5, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(insert_reservation_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=7, column=6, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)

        confirm_reservation_button = tk.Button(insert_reservation_frame, text="Add reservations", width=20, borderwidth=2,
                                          fg="white", bg="#004d00",
                                          command=add_reservations_db)
        confirm_reservation_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)
        self.green_bind_hover_effects(confirm_reservation_button)

        get_vehicle_table = ["vehicle", vehicle_id_entry, costs_of_rent]
        select_vehicle_button.config(command=lambda: self.pop_warning(new_window, get_vehicle_table, "dbtotree"))

        get_client_table = ["client", id_num_entry, client_info]
        select_client_button.config(command=lambda: self.pop_warning(new_window, get_client_table, "dbtotree"))

    # Section to manage vehicles
    def manage_vehicles_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(pady=(140, 0))
        
        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)

        edit_treeview_frame.configure(bg="black")

        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']

            engine = create_engine(database_uri)

            df = pd.read_sql_table("vehicle", con=engine)

            engine.dispose()

        except ValueError:
            print("ValueError")


        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            # Function to export data from the database table as CSV/Excel
            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'vehicle_type', 'category', 'segment', 'brand', 'model', 'year', 
                                                      'license_plate', 'seats', 'wheels', 'color', 'fuel', 'gearbox', 'photos', 
                                                      'cc', 'availability', 'rented', 'code_rented', 'for_inspection', 'code_inspection', 'for_legalization',
                                                       'code_legalization', 'last_update', 'code_last_update', 'next_inspection', 'next_legalization', 'insertion_date', 'code_insertion', 'doors'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'vehicle_type': df.at[x, 'vehicle_type'],
                            'category': df.at[x, 'category'],
                            'segment': df.at[x, 'segment'], 
                            'brand': df.at[x, 'brand'], 
                            'model': df.at[x, 'model'], 
                            'year': df.at[x, 'year'],
                            'license_plate': df.at[x, 'license_plate'], 
                            'seats': df.at[x, 'seats'], 
                            'wheels': df.at[x, 'wheels'], 
                            'color': df.at[x, 'color'],
                            'fuel': df.at[x, 'fuel'], 
                            'gearbox': df.at[x, 'gearbox'], 
                            'photos': df.at[x, 'photos'],
                            'cc': df.at[x, 'cc'], 
                            'availability': df.at[x, 'availability'], 
                            'rented': df.at[x, 'rented'],
                            'code_rented': df.at[x, 'code_rented'], 
                            'for_inspection': df.at[x, 'for_inspection'], 
                            'code_inspection': df.at[x, 'code_inspection'],
                            'for_legalization': df.at[x, 'for_legalization'], 
                            'code_legalization': df.at[x, 'code_legalization'], 
                            'last_update': df.at[x, 'last_update'],
                            'code_last_update': df.at[x, 'code_last_update'],
                            'next_inspection': df.at[x, 'next_inspection'],
                            'next_legalization': df.at[x, 'next_legalization'],
                            'insertion_date': df.at[x, 'insertion_date'],
                            'code_insertion': df.at[x, 'code_insertion'],
                            'doors': df.at[x, 'doors']
                        }

                        new_df_record = pd.DataFrame([new_df_record]) 

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")

            # Function to send the selected vehicle for inspection
            def send_for_inspection():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    result = self.check_employee_code(str(employee_code_entry.get()), True)
                    if result == "valid":
                        try:
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'license_plate']).lower())).first()
                            if vehicle.rented == "Yes":
                                warning = "Being currently rented"
                                self.pop_warning(new_window, warning, "cantlegalizationinspection")
                            else:
                                vehicle.for_inspection = "Yes"
                                vehicle.availability = "Unavailable"
                                vehicle.code_inspection = str(employee_code_entry.get())
                                db.session.commit()
                                df.at[x, 'availability'] = "Unavailable"
                                df.at[x, 'for_inspection'] = "Yes"
                                df.at[x, 'code_inspection'] = str(employee_code_entry.get())
                                refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")

            # Function to send the selected vehicle for legalization
            def send_for_legalization():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    result = self.check_employee_code(str(employee_code_entry.get()), True)
                    if result == "valid":
                        try:
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'license_plate']).lower())).first()
                            if vehicle.rented == "Yes":
                                warning = "Being currently rented"
                                self.pop_warning(new_window, warning, "cantlegalizationinspection")
                            else:
                                vehicle.for_legalization = "Yes"
                                vehicle.availability = "Unavailable"
                                vehicle.code_legalization = str(employee_code_entry.get())
                                db.session.commit()
                                df.at[x, 'availability'] = "Unavailable"
                                df.at[x, 'for_legalization'] = "Yes"
                                df.at[x, 'code_legalization'] = str(employee_code_entry.get())
                                refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")

            # Function to confirm that selected vehicle inspection
            def confirm_inspection():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    result = self.check_employee_code(str(employee_code_entry.get()), True)
                    if result == "valid":
                        try:
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'license_plate']).lower())).first()
                            next_inspection_date=self.calculate_date(str(df.at[x, 'next_inspection']), True)

                            vehicle.next_inspection = next_inspection_date
                            vehicle.for_inspection = "No"
                            vehicle.code_inspection = str(employee_code_entry.get())

                            legalization_date = datetime.strptime(vehicle.next_legalization, "%Y-%m-%d").date()
                            current_date = datetime.now().date()

                            if vehicle.rented == "Yes" or vehicle.for_legalization == "Yes" or legalization_date <= current_date:
                                vehicle.availability = "Unavailable"
                            else:
                                vehicle.availability = "Available"                       

                            db.session.commit()

                            if vehicle.rented == "Yes" or vehicle.for_legalization == "Yes" or legalization_date <= current_date:
                                df.at[x, 'availability'] = "Unavailable"
                            else:
                                df.at[x, 'availability'] = "Available" 

                            df.at[x, 'for_inspection'] = "No"
                            df.at[x, 'code_inspection'] = str(employee_code_entry.get())
                            df.at[x, 'next_inspection'] = next_inspection_date
                            refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")

            # Function to confirm the selected vehicle legalization
            def confirm_legalization():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    result = self.check_employee_code(str(employee_code_entry.get()), True)
                    
                    if result == "valid":
                        try:
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'license_plate']).lower())).first()
                            next_legalization_date=self.calculate_date(str(df.at[x, 'next_legalization']), True)
                            vehicle.next_legalization = next_legalization_date
                            vehicle.for_legalization = "No"
                            vehicle.code_legalization = str(employee_code_entry.get())

                            inspection_date = datetime.strptime(vehicle.next_inspection, "%Y-%m-%d").date()
                            current_date = datetime.now().date()

                            if vehicle.rented == "Yes" or vehicle.for_inspection == "Yes" or inspection_date <= current_date:
                                vehicle.availability = "Unavailable"
                            else:
                                vehicle.availability = "Available"

                            db.session.commit()

                            if vehicle.rented == "Yes" or vehicle.for_inspection == "Yes" or inspection_date <= current_date:
                                df.at[x, 'availability'] = "Unavailable"
                            else:
                                df.at[x, 'availability'] = "Available"
                            
                            df.at[x, 'for_legalization'] = "No"
                            df.at[x, 'code_legalization'] = str(employee_code_entry.get())
                            df.at[x, 'next_legalization'] = next_legalization_date
                            refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")

            # Function to see the information about the current reservation of the selected vehicle
            def check_vehicle_reservation():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["vehicle", "reservation", str(df.at[x, 'license_plate']), "current"]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            # Function to see the information about the current client of the selected vehicle
            def check_client_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_client = ["vehicle", "client", str(df.at[x, 'license_plate']), "current"]
                    self.pop_warning(new_window, get_client, "showdbiteminfo")                    

            # Function to see the client history of the selected vehicle
            def check_client_history():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_client = ["vehicle", "client", str(df.at[x, 'license_plate']), "history"]
                    self.pop_warning(new_window, get_client, "showdbiteminfo")  

            # Function to see the reservation history of the selected vehicle
            def check_reservation_history():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["vehicle", "reservation", str(df.at[x, 'license_plate']), "history"]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")
                
            def verify_data():
                date_exceeded = []
                for index, row in df.iterrows():

                    not_num = []
                    must_be_number = {
                        'Seats': row['seats'],
                        'Number of Wheels': row['wheels'],
                        'Doors': row['doors']
                    }

                    if str(row['vehicle_type']).lower() == "motorcycles":
                        del must_be_number['Doors']

                    for column_num, value_num in must_be_number.items():
                        try:
                            int(value_num)
                        except ValueError:
                            not_num.append(value_num)

                    not_alpha = []
                    must_not_have_number = {
                        'Vehicle Type': str(row['vehicle_type']),
                        'Segment': str(row['segment']),
                        'Category': str(row['category']),
                        'Fuel': str(row['fuel']),
                        'Type of Gearbox': str(row['gearbox']),
                        'Brand': str(row['brand']),
                        'Color': str(row['color'])
                    }

                    for column_word, value_word in must_not_have_number.items():
                        clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                        if all(char.isalpha() for char in clean_value_word):
                            pass
                        else:
                            not_alpha.append(value_word)

                    is_empty = []
                    all_data = {
                        'Year': str(row['year']),
                        'Seats': str(row['seats']),
                        'Number of Wheels': str(row['wheels']),
                        'Doors': str(row['doors']),
                        'Model': str(row['model']),
                        'Vehicle Type': str(row['vehicle_type']),
                        'Segment': str(row['segment']),
                        'Category': str(row['category']),
                        'Fuel': str(row['fuel']),
                        'Color': str(row['color']),
                        'Type of Gearbox': str(row['gearbox']),
                        'Brand': str(row['brand']),
                        'Vehicle Photos': str(row['photos']),
                        'License Plate': str(row['license_plate']),
                        'Vehicle CC': str(row['cc'])
                    }

                    if str(row['vehicle_type']).lower() == "motorcycles":
                        del all_data['Doors']

                    for column_all, value_all in all_data.items():
                        if value_all == 'nan':
                            is_empty.append(value_all)
                        else:
                            pass

                    not_defined = []
                    must_be_defined = {
                        'Vehicle Type': (str(row['vehicle_type']), vehicle_types),
                        'Category': (str(row['category']), categories),
                        'Fuel': (str(row['fuel']), fuels),
                        'Type of Gearbox': (str(row['gearbox']), gearbox_types)
                    }

                    for column_defined, value_defined in must_be_defined.items():
                        if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                            not_defined.append(value_defined)
                        else:
                            pass

                    if str(row['vehicle_type']).lower() == 'cars':
                        if str(row['segment']).lower() not in [seg.lower() for seg in segments_cars] or str(row['segment']).lower() == 'not defined':
                            not_defined.append(str(row['segment']))
                        if str(row['cc']).lower() not in [c.lower() for c in cc_not_relevant] or str(row['cc']).lower() == 'not defined':
                            not_defined.append(str(row['cc']))
                    elif str(row['vehicle_type']).lower() == 'motorcycles':
                        if str(row['segment']).lower() not in [seg.lower() for seg in segments_motorcycles] or str(row['segment']).lower() == 'not defined':
                            not_defined.append(str(row['segment']))
                        if str(row['cc']).lower() not in [c.lower() for c in cc_list] or str(row['cc']).lower() == 'not defined':
                            not_defined.append(str(row['cc']))

                    errors_found = not_num, not_alpha, is_empty, not_defined

                    possible_photo_path_list = str(row['photos'])

                    self.verify_photo_path(possible_photo_path_list)
                    if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                        pass
                    if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        is_empty.append("Photos")

                    date_to_check = str(row['year'])
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    if any(len(error_list) > 0 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False:
                        result_of_validation = "Error Found"
                        self.change_row_color(treeview, index, "darkred")
                    else:
                        self.change_row_color(treeview, index, "#313131")
                        result_of_validation = "No Error Found"

                    date_next_inspection = datetime.strptime(str(row['next_inspection']), "%Y-%m-%d")
                    
                    current_date = datetime.now()
                    days_left_to_inspection = (date_next_inspection - current_date).days
                    days_left_to_inspection +=1

                    date_next_legalization = datetime.strptime(str(row['next_legalization']), "%Y-%m-%d")
                    days_left_to_legalization = (date_next_legalization - current_date).days

                    days_left_to_legalization += 1

                    if str(row['availability']) == "Unavailable":
                        self.change_row_color(treeview, index, "#000000")
                        if days_left_to_legalization <= 15 and str(row['for_legalization']) == "No":
                            self.change_row_color(treeview, index, "#C56C00")
                            if days_left_to_legalization <= 0:
                                date_exceeded.append(str(row['license_plate']))
                                self.change_row_color(treeview, index, "darkred")
                        if days_left_to_inspection <= 15 and str(row['for_inspection']) == "No":
                            self.change_row_color(treeview, index, "#C56C00")
                            if days_left_to_inspection <= 0:
                                date_exceeded.append(str(row['license_plate']))
                                self.change_row_color(treeview, index, "darkred")
                    elif str(row['availability']) == "Available":
                        self.change_row_color(treeview, index, "#313131")
                        if days_left_to_legalization <= 15 or days_left_to_inspection <= 15:
                            self.change_row_color(treeview, index, "#C56C00")
                        if days_left_to_legalization <= 0 or days_left_to_inspection <= 0:
                            date_exceeded.append(str(row['license_plate']))
                            self.change_row_color(treeview, index, "darkred")
                if len(date_exceeded) > 0:
                    self.pop_warning(new_window, date_exceeded, 'vehicledateexceeded')

            def refresh_tree(df):
                treeview.delete(*treeview.get_children())

                send_for_inspection_button.configure(bg="black")
                send_for_inspection_button.configure(state=DISABLED)
                self.bind_hover_effects(send_for_inspection_button)

                send_for_legalization_button.configure(bg="black")
                send_for_legalization_button.configure(state=DISABLED)
                self.bind_hover_effects(send_for_legalization_button)

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                df['next_legalization'] = df['next_legalization'].apply(convert_to_datetime)
                df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)   
                df['year'] = df['year'].apply(convert_to_datetime)

                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")

                columns_to_int = ['doors', 'wheels', 'seats', 'license_plate', 'cc']

                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0 
                    
                    column_width = max(heading_width, max_width) + 20 

                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.column("photos", width=120, minwidth=120)

                treeview.update_idletasks()

                verify_data()

            def clear_entries():

                entries = [license_plate_entry, employee_code_entry, brand_entry, model_entry, seats_entry, doors_entry, color_entry, wheels_entry]
                for entry in entries:
                    entry.delete(0, END)
                    self.toggle_entry_colors(1, entry)

                read_only_entries = [legalization_date_entry, year_entry, doors_entry]
                for entry in read_only_entries:
                    entry.config(state=tk.NORMAL)
                    entry.delete(0, tk.END)
                    entry.config(state="readonly", readonlybackground="#313131")


                combos = [[gearbox_combobox, gearbox_types],[fuel_combobox, fuels], [segment_combobox, segments_cars], [category_combobox, categories], [vehicle_type_combobox, vehicle_types], [cc_combobox, cc_list]]
                for combo in combos:
                    self.toggle_combo_text(1, combo[0])
                    combo[0].set(combo[1][0])

                if hasattr(self, 'photo_paths'):
                    del self.photo_paths
                see_photos_button.configure(state=tk.DISABLED)
                reload_show_photos_button.configure(image=self.update_photos_button_image)

            def select_record(e):
                clear_entries()

                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    print(df.at[x, 'seats'])
                    export_selected_button.configure(state=NORMAL)
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    vehicle_type = str(df.at[x, "vehicle_type"]).lower()

                    if vehicle_type == "cars":
                        vehicle_type_combobox.set(vehicle_types[1])
                        self.toggle_combo_text(1, vehicle_type_combobox)
                        doors_entry.config(state=NORMAL)
                        doors_entry.insert(0, df.at[x, "doors"])
                    elif vehicle_type == "motorcycles":
                        vehicle_type_combobox.set(vehicle_types[2])
                        self.toggle_combo_text(1, vehicle_type_combobox)
                        doors_entry.config(state=NORMAL)
                        doors_entry.insert(0, 0)
                        doors_entry.config(state="readonly")
                    else:
                        vehicle_type_combobox.set(vehicle_types[0])
                        self.toggle_combo_text(0, vehicle_type_combobox)

                    category = str(df.at[x, "category"]).lower()
                    if category == "gold":
                        category_combobox.set(categories[1])
                        self.toggle_combo_text(1, category_combobox)
                    elif category == "silver":
                        category_combobox.set(categories[2])
                        self.toggle_combo_text(1, category_combobox)
                    elif category == "economic":
                        category_combobox.set(categories[3])
                        self.toggle_combo_text(1, category_combobox)
                    else:
                        category_combobox.set(categories[0])
                        self.toggle_combo_text(0, category_combobox)

                    segment = str(df.at[x, "segment"]).lower()
                    cc = str(df.at[x, 'cc']).lower()

                    if vehicle_type == "cars":
                        segment_options = segments_cars
                        mapping = {seg.lower(): segments_cars[i] for i, seg in enumerate(segments_cars)}
                        cc_options = cc_not_relevant
                        mapping_cc = {c.lower(): cc_not_relevant[i] for i, c in enumerate(cc_not_relevant)}
                    else:
                        segment_options = segments_motorcycles
                        mapping = {seg.lower(): segments_motorcycles[i] for i, seg in enumerate(segments_motorcycles)}
                        cc_options = cc_list
                        mapping_cc = {c.lower(): cc_list[i] for i, c in enumerate(cc_list)}

                    segment_combobox['values'] = segment_options

                    segment_combobox.set(segment_options[0])

                    segment_combobox.set(mapping.get(segment.lower(), "Not Defined"))

                    if segment_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, segment_combobox)
                    else:
                        self.toggle_combo_text(1, segment_combobox)

                    cc_combobox['values'] = cc_options
                    cc_combobox.set(cc_options[0])
                    cc_combobox.set(mapping_cc.get(cc.lower(), "Not Defined"))

                    if cc_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, cc_combobox)
                    else:
                        self.toggle_combo_text(1, cc_combobox)

                    fuel = str(df.at[x, "fuel"]).lower()

                    fuel_combobox.set(fuels[0]) 
                    mapping = {f.lower(): fuels[i] for i, f in enumerate(fuels)}
                    fuel_combobox.set(mapping.get(fuel, mapping["not defined"]))

                    if fuel_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, fuel_combobox)
                    else:
                        self.toggle_combo_text(1, fuel_combobox)

                    gearbox = str(df.at[x, "gearbox"]).lower()

                    gearbox_combobox.set(gearbox_types[0])  # Set the default selection
                    mapping = {gear.lower(): gearbox_types[i] for i, gear in enumerate(gearbox_types)}
                    gearbox_combobox.set(mapping.get(gearbox, mapping["not defined"]))
                    if gearbox_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, gearbox_combobox)
                    else:
                        self.toggle_combo_text(1, gearbox_combobox)

                    date_next_inspection = datetime.strptime(df.at[x, "next_inspection"], "%Y-%m-%d")

                    current_date = datetime.now()
                    days_left_to_inspection = (date_next_inspection - current_date).days
                    days_left_to_inspection +=1
                    if days_left_to_inspection <= 15:
                        if str(df.at[x, 'for_inspection']) == "No":
                            send_for_inspection_button.configure(bg="#C56C00")
                            send_for_inspection_button.configure(state=NORMAL)
                            self.orange_bind_hover_effects(send_for_inspection_button)
                        else:
                            send_for_inspection_button.configure(bg="black")
                            send_for_inspection_button.configure(state=DISABLED)
                            self.bind_hover_effects(send_for_inspection_button)
                    else:
                        send_for_inspection_button.configure(bg="black")
                        send_for_inspection_button.configure(state=DISABLED)
                        self.bind_hover_effects(send_for_inspection_button)

                    date_next_legalization = datetime.strptime(str(df.at[x, 'next_legalization']), "%Y-%m-%d")
                    days_left_to_legalization = (date_next_legalization - current_date).days

                    days_left_to_legalization += 1

                    if days_left_to_legalization <= 15:
                        if str(df.at[x, 'for_legalization']) == "No":
                            send_for_legalization_button.configure(bg="#C56C00")
                            send_for_legalization_button.configure(state=NORMAL)
                            self.orange_bind_hover_effects(send_for_legalization_button)
                        else:
                            send_for_legalization_button.configure(bg="black")
                            send_for_legalization_button.configure(state=DISABLED)
                            self.bind_hover_effects(send_for_legalization_button)
                    else:
                        send_for_legalization_button.configure(bg="black")
                        send_for_legalization_button.configure(state=DISABLED)
                        self.bind_hover_effects(send_for_legalization_button)

                    if str(df.at[x, 'for_legalization']) == "Yes":
                        confirm_legalization_button.configure(state=NORMAL)
                    else:
                        confirm_legalization_button.configure(state=DISABLED)

                    if str(df.at[x, 'for_inspection']) == "Yes":
                        confirm_inspection_button.configure(state=NORMAL)
                    else:
                        confirm_inspection_button.configure(state=DISABLED)

                    plate_reservations = Reservation.query.filter_by(vehicle_id=str(df.at[x, 'license_plate'])).all()
                    plate_reservations_in_progress = Reservation.query.filter_by(vehicle_id=str(df.at[x, 'license_plate']), reservation_state="In progress").first()

                    if len(plate_reservations) > 0:
                        check_reservation_history_button.configure(state=NORMAL)
                        check_client_history_button.configure(state=NORMAL)
                        if plate_reservations_in_progress is not None:
                            check_reservation_button.configure(state=NORMAL)
                            check_client_button.configure(state=NORMAL)
                        else:
                            check_reservation_button.configure(state=DISABLED)
                            check_client_button.configure(state=DISABLED)     
                    else:
                        check_reservation_history_button.configure(state=DISABLED)
                        check_client_history_button.configure(state=DISABLED)
                        check_reservation_button.configure(state=DISABLED)
                        check_client_button.configure(state=DISABLED)

                    legalization_date_entry.config(state=tk.NORMAL)
                    legalization_date_entry.insert(0, df.at[x, "next_legalization"])
                    legalization_date_entry.config(state="readonly")

                    brand_entry.insert(0, df.at[x, "brand"])
                    model_entry.insert(0, df.at[x, "model"])
                    license_plate_entry.insert(0, df.at[x, "license_plate"])
                    seats_entry.insert(0, df.at[x, "seats"])
                    color_entry.insert(0, df.at[x, "color"])
                    wheels_entry.insert(0, df.at[x, "wheels"])

                    year_entry.config(state=tk.NORMAL)
                    year_entry.insert(0, df.at[x, "year"])
                    year_entry.config(state="readonly")

                    date_to_check = str(df.at[x, "year"])
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                    if bool(re.match(pattern, date_to_check)) == False:
                        year_entry.config(readonlybackground="darkred")
                    else:
                        year_entry.config(readonlybackground="#313131")

                    must_not_empty_entries = {
                        seats_entry: seats_entry.get(),
                        wheels_entry: wheels_entry.get(),
                        doors_entry: doors_entry.get(),
                        brand_entry: brand_entry.get(),
                        color_entry: color_entry.get(),
                        license_plate_entry: license_plate_entry.get(),
                        model_entry: model_entry.get()
                    }
                    for column_entry_check, value_check in must_not_empty_entries.items():
                        if str(value_check).lower() == 'nan':
                            self.toggle_entry_colors_ifnan(0, column_entry_check)
                            column_entry_check.delete(0, "end")
                            column_entry_check.insert(0, "EMPTY")
                        else:
                            self.toggle_entry_colors_ifnan(1, column_entry_check)

                    must_be_number_entries = {
                        seats_entry: seats_entry.get(),
                        wheels_entry: wheels_entry.get(),
                        doors_entry: doors_entry.get()
                    }
                    for value_key, value in must_be_number_entries.items():
                        try:
                            int(value)
                            self.toggle_entry_colors(1, value_key)
                        except ValueError:
                            self.toggle_entry_colors(0, value_key)

                    must_not_have_number_entries = {
                        brand_entry: brand_entry.get(),
                        color_entry: color_entry.get()
                    }
                    for word_key, word in must_not_have_number_entries.items():
                        if any(not char.isalpha() for char in word) or str(word).lower() == "empty":
                            self.toggle_entry_colors(0, word_key)
                        else:
                            self.toggle_entry_colors(1, word_key)

                    self.verify_photo_path(str(df.at[x, "photos"]))
                    if str(df.at[x, "photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        self.toggle_button_colors(0, selected_vehicle_photos_button)
                        self.red_bind_hover_effects(selected_vehicle_photos_button)
                    else:
                        self.toggle_button_colors(1, selected_vehicle_photos_button)
                        self.bind_hover_effects(selected_vehicle_photos_button)
                else:
                    pass

            def update_record():
                must_be_number = {
                        'Seats': (seats_entry.get(), seats_entry),
                        'Number of Wheels': (wheels_entry.get(), wheels_entry),
                        'Doors': (doors_entry.get(), doors_entry)
                    }

                must_not_have_number = {
                        'Brand': (brand_entry.get(), brand_entry),
                        'Color': (color_entry.get(), color_entry)
                    }

                must_be_defined = {
                        'Vehicle Type': (selected_vehicle_type.get(), vehicle_type_combobox),
                        'Segment': (selected_segment.get(), segment_combobox),
                        'Category': (selected_category.get(), category_combobox),
                        'Fuel': (selected_fuel.get(), fuel_combobox),
                        'Type of Gearbox': (selected_gearbox.get(), gearbox_combobox),
                        'Vehicle CC': (selected_cc.get(), cc_combobox)
                }

                must_not_be_empty = {
                     
                        'Seats': (seats_entry.get(), seats_entry),
                        'Number of Wheels': (wheels_entry.get(), wheels_entry),
                        'Doors': (doors_entry.get(), doors_entry),
                        'Model': (model_entry.get(), model_entry),                               
                        'Color': (color_entry.get(), color_entry),
                        'Brand': (brand_entry.get(), brand_entry),
                        'License Plate': (license_plate_entry.get(), license_plate_entry)
                    }

                if selected_vehicle_type.get() == "Motorcycles":
                    del must_not_be_empty['Doors']

                self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    self.verify_photo_path(str(df.at[x, 'photos']))

                    if str(df.at[x, 'photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        if hasattr(self, 'photo_paths'):
                            pass
                        else:
                            is_empty.append("Photos")

                    date_to_check = str(year_entry.get())
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                        result_of_validation = "Error Found"
                    else:
                        result_of_validation = "No Error Found"

                    if result_of_validation == "No Error Found":
                        result = self.check_employee_code(str(employee_code_entry.get()), False)

                        if result == "valid":
                            self.toggle_entry_colors(1, employee_code_entry)
                            cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(df.at[x, 'license_plate']).lower())
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()
                            if vehicle.rented == "Yes":
                                warning = "The selected record can't be updated now due to being currently rented"
                                self.pop_warning(new_window, warning, "cantupdaterented")
                            else:

                                new_plate = re.sub(r'[^\w\s]', '', str(license_plate_entry.get()).lower())

                                existing_license_plate = None

                                if new_plate == vehicle.license_plate:
                                    pass
                                else: 
                                    existing_license_plate = Vehicle.query.filter(Vehicle.license_plate.ilike(new_plate)).first()

                                if existing_license_plate:
                                    warning = str(license_plate_entry.get())
                                    self.pop_warning(new_window, warning, "updateexistingplate")
                                else:
                                    try:
                                        date_update = str(datetime.now(timezone.utc).date())

                                        if year_entry.get() != vehicle.year:
                                            print(year_entry.get())
                                            next_inspection_date = self.calculate_date(year_entry.get())
                                            print(next_inspection_date)
                                            vehicle.next_inspection = next_inspection_date

                                        vehicle.category = selected_category.get()
                                        vehicle.segment = selected_segment.get()
                                        vehicle.brand = brand_entry.get()
                                        vehicle.model = str(model_entry.get())
                                        vehicle.year = str(year_entry.get())
                                        vehicle.cc = selected_cc.get()
                                        vehicle.license_plate = new_plate
                                        vehicle.seats = int(seats_entry.get())
                                        vehicle.doors = int(doors_entry.get())
                                        vehicle.color = color_entry.get()
                                        vehicle.fuel = selected_fuel.get()
                                        vehicle.gearbox = selected_gearbox.get()
                                        vehicle.wheels = (int(wheels_entry.get()))
                                        vehicle.next_legalization = str(legalization_date_entry.get())
                                        vehicle.code_last_update = str(employee_code_entry.get())
                                        vehicle.last_update = str(date_update)

                                        if hasattr(self, 'photo_paths'):
                                            vehicle.photos = self.photo_paths
                                        else:
                                            pass

                                        db.session.commit()
                                        self.toggle_button_colors(1, selected_vehicle_photos_button)

                                        if year_entry.get() != vehicle.year:
                                            next_inspection_date = self.calculate_date(year_entry.get())
                                            df.at[x, 'next_inspection'] = next_inspection_date

                                        df.at[x, "segment"] = vehicle.segment
                                        df.at[x, "category"] = selected_category.get()
                                        df.at[x, "brand"] = brand_entry.get()
                                        df.at[x, "model"] = str(model_entry.get())
                                        df.at[x, "year"] = str(year_entry.get())
                                        df.at[x, "license_plate"] = new_plate
                                        df.at[x, "cc"] = selected_cc.get()
                                        df.at[x, "seats"] = int(seats_entry.get())
                                        df.at[x, "doors"] = int(doors_entry.get())
                                        df.at[x, "color"] = color_entry.get()
                                        df.at[x, "fuel"] = selected_fuel.get()
                                        df.at[x, "gearbox"] = selected_gearbox.get()
                                        df.at[x, "wheels"] = (int(wheels_entry.get()))
                                        df.at[x, "next_legalization"] = str(legalization_date_entry.get())
                                        df.at[x, "code_last_update"] = str(employee_code_entry.get())
                                        df.at[x, "last_update"] = str(date_update)

                                        if hasattr(self, 'photo_paths'):
                                            df.at[x, 'photos'] = self.photo_paths
                                        else:
                                            pass

                                        clear_entries()
                                        refresh_tree(df)

                                    except OperationalError as e:
                                        warning = "Database is locked. Please close the Database and try again."
                                        self.pop_warning(new_window, warning, "databaselocked")
                                        db.session.rollback()
                                        print("Database is locked. Please try again later.")
                        else:
                            self.toggle_entry_colors(0, employee_code_entry)
                            self.pop_warning(new_window, result, "wrongemployeecode")
                    else:
                        if bool(re.match(pattern, date_to_check)) == False:
                            wrong_text_format = str(df.at[x,'year'])
                            self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                        for key in must_not_be_empty:
                            if key in is_empty:
                                entry_value = must_not_be_empty[key][1]
                                self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                            else:
                                self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                        for key in must_be_defined:
                            if key in not_defined:
                                combobox_value = must_be_defined[key][1]
                                self.toggle_combo_text(0, must_be_defined[key][1])
                            else:
                                self.toggle_combo_text(1, must_be_defined[key][1])

                        for key in must_not_have_number:
                            if key in not_alpha or key in is_empty:
                                entry_value = must_not_have_number[key][1]
                                self.toggle_entry_colors(0, must_not_have_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_not_have_number[key][1])

                        if "Photos" in is_empty:
                            self.toggle_button_colors(0, select_photos_button)
                            self.red_bind_hover_effects(select_photos_button)
                        else:
                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                        for key in must_be_number:
                            if key in not_num or key in is_empty:
                                entry_value = must_be_number[key][1]
                                self.toggle_entry_colors(0, must_be_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_be_number[key][1])

                        errors_adding = []
                        for error_list in errors_found:
                            if len(error_list) > 1:
                                errors_adding.append(error_list)

                        if len(errors_adding) > 0:
                            self.pop_warning(new_window, errors_adding, "addrecvalidation")
                else:
                    warning = "Must select an item to Update"
                    self.pop_warning(new_window, warning, "noselectedtoupdate" )

            def remove_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    try:
                        if len(selected_items) == Vehicle.query.count():
                            warning = "Can not delete all the data from the Vehicle Database"
                            self.pop_warning(new_window, warning, "cannotdeletealldb" )
                        else:
                            code_check=self.check_employee_code(str(employee_code_entry.get()), True)
                            if code_check == "valid":
                                self.toggle_entry_colors(1, employee_code_entry)
                                can_not_delete = []
                                for record in selected_items:
                                    x = treeview.index(record)
                                    vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'license_plate']).lower())).first()
                                    if vehicle.rented == "Yes":
                                        can_not_delete.append(vehicle.license_plate)
                                    else:
                                        db.session.delete(vehicle)
                                        db.session.commit()     
                                        treeview.delete(record)
                                        df.drop(index=x, inplace=True)
                                        df.reset_index(drop=True, inplace=True)
                                        clear_entries()
                                verify_data()
                                if len(can_not_delete) > 0:
                                    self.pop_warning(new_window, can_not_delete, "cannotdelete")
                            else:
                                self.toggle_entry_colors(0, employee_code_entry)
                                self.pop_warning(new_window, code_check, "wrongemployeecode")
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    warning = "Must select at least one record to remove"
                    self.pop_warning(new_window, warning, "noselectedtoremove")

            def selected_vehicle_photos():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    photos_of_selected = str(df.at[x, "photos"])

                    if photos_of_selected.lower() != "nan":
                        self.verify_photo_path(photos_of_selected)

                        if len(valid_photo_type) > 0:
                            print(valid_photo_type)
                            if len(valid_photo_paths) > 0:
                                def handle_photo_viewer_result(result, updated_photos):
                                    if result == "confirm":
                                        try:
                                            plate = re.sub(r'[^\w\s]', '', str(df.at[x, 'license_plate']).lower())
                                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(plate)).first()
                                            vehicle.photos = updated_photos
                                            db.session.commit()
                                            df.at[x, 'photos'] = updated_photos
                                        except OperationalError as e:
                                            warning = "Database is locked. Please close the Database and try again."
                                            self.pop_warning(new_window, warning, "databaselocked")
                                            db.session.rollback()
                                            print("Database is locked. Please try again later.")
                                    elif result == "cancel":
                                        print("User cancelled changes")

                                if str(df.at[x, "rented"]) == "Yes":
                                    mode = "View Mode"
                                else:
                                    mode = "Edit Mode"

                                updated_photos = []
                                self.photo_viewer(new_window, valid_photo_paths, mode, handle_photo_viewer_result, updated_photos)
                            if len(invalid_photo_paths) > 0:
                                self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                self.toggle_button_colors(0, selected_vehicle_photos_button)
                        print(invalid_photo_type)
                        for path in invalid_photo_type:
                            if path == "":
                                invalid_photo_type.remove(path)
                        if len(invalid_photo_type) > 0:
                            self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                            self.toggle_button_colors(0, selected_vehicle_photos_button)
                    else:
                        x += 1
                        self.pop_warning(new_window, str(x), "nanselectedphoto")
                        self.toggle_button_colors(0, selected_vehicle_photos_button)
                else:
                    warning = "Must select a record to see photos"
                    self.pop_warning(new_window, warning, "noselectedtoseephotos")

            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                   command=update_record)
            update_button.grid(row=0, column=0, padx=5, pady=3)
            self.bind_hover_effects(update_button)

            clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                          command=clear_entries)
            clear_entries_button.grid(row=0, column=1, padx=5, pady=3)
            self.bind_hover_effects(clear_entries_button)

            selected_vehicle_photos_button = Button(edit_treeview_frame, text="See Selected Vehicle Photos",
                                                    fg="white",
                                                    bg="black", command=selected_vehicle_photos)
            selected_vehicle_photos_button.grid(row=0, column=2, padx=5, pady=3)
            self.bind_hover_effects(selected_vehicle_photos_button)

            remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                            bg="black", command=remove_selected)
            remove_selected_button.grid(row=0, column=3, padx=5, pady=3)
            self.bind_hover_effects(remove_selected_button)

            refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                       bg="black", command=lambda: refresh_tree(df))
            refresh_tree_button.grid(row=0, column=4, padx=5, pady=3)
            self.bind_hover_effects(refresh_tree_button)

            employee_code_label = tk.Label(edit_treeview_frame, text="Employee Code:",
                              font=("Helvetica", 10), fg="white", bg="black")
            employee_code_label.grid(row=0, column=5, pady=5, padx=(20, 5), sticky=tk.E)

            employee_code_entry = tk.Entry(edit_treeview_frame, bd=2, width=10)
            employee_code_entry.grid(row=0, column=6, padx=5, pady=3)

            treeview.bind("<ButtonRelease-1>", select_record)

            send_for_inspection_button.config(command=send_for_inspection)
            send_for_legalization_button.config(command=send_for_legalization)
            confirm_inspection_button.config(command=confirm_inspection)
            confirm_legalization_button.config(command=confirm_legalization)
            check_reservation_history_button.config(command=check_reservation_history)
            check_client_history_button.config(command=check_client_history)
            check_reservation_button.config(command=check_vehicle_reservation)
            check_client_button.config(command=check_client_info)
            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)

                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))

                reload_show_photos_button.configure(image=self.update_photos_button_image)

        edit_vehicle_frame = tk.Frame(new_window)
        edit_vehicle_frame.configure(bg="black")
        edit_vehicle_frame.pack(pady=(0,10))

        select_photos_button = tk.Button(edit_vehicle_frame, text="Select Vehicle Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=0, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(select_photos_button)

        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(edit_vehicle_frame, text="See Vehicle Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=0, column=4, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = 'resources/update.png'
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(edit_vehicle_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=0, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)

        vehicle_type_label = tk.Label(edit_vehicle_frame, text="Vehicle Type:",
                                      font=("Helvetica", 10), fg="white", bg="black")
        vehicle_type_label.grid(row=0, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        vehicle_types = ["Not Defined", "Cars", "Motorcycles"]
        selected_vehicle_type = tk.StringVar()
        vehicle_type_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_vehicle_type,
                                             values=vehicle_types, state="readonly", justify="center", height=4,
                                             width=20)
        vehicle_type_combobox.grid(row=0, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        vehicle_type_combobox.set(vehicle_types[0])
        vehicle_type_combobox.state(['disabled'])

        category_label = tk.Label(edit_vehicle_frame, text="Category:",
                                  font=("Helvetica", 10), fg="white", bg="black")
        category_label.grid(row=1, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        categories = ["Not Defined", "Gold", "Silver", "Economic"]
        selected_category = tk.StringVar()
        category_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_category,
                                         values=categories, state="readonly", justify="center", height=4, width=20)
        category_combobox.grid(row=1, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        category_combobox.set(categories[0]) 

        segment_label = tk.Label(edit_vehicle_frame, text="Segment:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        segment_label.grid(row=2, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        segments_cars = ["Not Defined", "Microcar", "Subcompact", "Compact", "Midsize", "Full-size", "SUV",
                         "Crossover", "Multi-Purpose Vehicle", "Convertible/Cabriolet", "Coupe",
                         "Roadster", "Hot Hatch", "Sports Car"]

        segments_motorcycles = ["Not Defined", "Sport Bikes", "Cruisers", "Touring Bikes", "Naked Bikes",
                                "Adventure Bikes", "Dirt Bikes", "Scooters",
                                "Electric Motorcycles", "Cafe Racers", "Choppers",
                                "Bobbers", "Trikes"]

        selected_segment = tk.StringVar()
        segment_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_segment,
                                        values=segments_cars, state="readonly", justify="center", height=4, width=20)
        segment_combobox.grid(row=2, column=1, pady=5, padx=(5, 20), sticky=tk.W)
        segment_combobox.set(segments_cars[0])

        doors_label = tk.Label(edit_vehicle_frame, text="Doors:",
                               font=("Helvetica", 10), fg="white", bg="black")
        doors_label.grid(row=3, column=4, pady=5, padx=(40, 5), sticky=tk.E)

        doors_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        doors_entry.grid(row=3, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        def update_segment_options(event):
            selected_type = selected_vehicle_type.get()
            if selected_type == "Cars":
                segment_combobox['values'] = segments_cars
                selected_segment.set(segments_cars[0])
                doors_entry.config(state=tk.NORMAL)
                doors_entry.delete(0, tk.END)
            elif selected_type == "Motorcycles":
                segment_combobox['values'] = segments_motorcycles
                selected_segment.set(segments_motorcycles[0])
                doors_entry.delete(0, tk.END)
                doors_entry.insert(0, 0)
                doors_entry.config(state="readonly", readonlybackground="#313131")

        vehicle_type_combobox.bind("<<ComboboxSelected>>", update_segment_options)

        fuel_label = tk.Label(edit_vehicle_frame, text="Fuel:",
                              font=("Helvetica", 10), fg="white", bg="black")
        fuel_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        fuels = ["Not Defined", "Gasoline(Petrol)", "Diesel", "Electricity", "Hybrid", "Plug-in Hybrid (PHEV)",
                 "Compressed Natural Gas (CNG)", "Liquefied Petroleum Gas (LPG)",
                 "Hydrogen Fuel Cell", "Biodiesel", "Flex-Fuel"]
        selected_fuel = tk.StringVar()
        fuel_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_fuel,
                                     values=fuels, state="readonly", justify="center", height=4, width=20)
        fuel_combobox.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        fuel_combobox.set(fuels[0])

        gearbox_label = tk.Label(edit_vehicle_frame, text="Type of Gearbox:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        gearbox_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        gearbox_types = ["Not Defined", "Manual", "Semi-Automatic", "Automatic"]
        selected_gearbox = tk.StringVar()
        gearbox_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_gearbox,
                                        values=gearbox_types, state="readonly", justify="center", height=4, width=20)
        gearbox_combobox.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        gearbox_combobox.set(gearbox_types[0]) 

        cc_label = tk.Label(edit_vehicle_frame, text="Vehicle CC:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        cc_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)

        cc_not_relevant = ["Not Defined", "Not Relevant"]
        cc_list = ["Not Defined", "<= 50", "<= 50 (11kw)", "<= 50 (35kw)", "51 - 125", "51 - 125 (11kw)", "51 - 125 (35kw)", "126 - 500", "126 - 500 (35kw)", "501 - 1000", "501 - 1000 (35kw)", ">= 1000", ">= 1000 (35kw)"]
        selected_cc = tk.StringVar()
        cc_combobox = ttk.Combobox(edit_vehicle_frame, textvariable=selected_cc,
                                        values=cc_list, state="readonly", justify="center", height=4, width=20)
        cc_combobox.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        cc_combobox.set(cc_list[0]) 

        year_button = tk.Button(edit_vehicle_frame, text="Select Vehicle Date:", width=20, borderwidth=2,
                                              fg="white", bg="black", command=lambda: self.datepicker(new_window, year_entry, "vehicle_date"))

        year_button.grid(row=6, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        year_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        year_entry.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        legalization_date_button = tk.Button(edit_vehicle_frame, text="Next Legalization Date:", width=20, borderwidth=2,
                                      fg="white", bg="black", command=lambda: self.datepicker(new_window, legalization_date_entry, "legalization"))

        legalization_date_button.grid(row=7, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        legalization_date_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        legalization_date_entry.grid(row=7, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        export_selected_button = tk.Button(edit_vehicle_frame, text="Export Selected Data", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_selected_button.grid(row=8, column=0, pady=5, padx=5)
        self.bind_hover_effects(export_selected_button)

        export_all_button = tk.Button(edit_vehicle_frame, text="Export All Data", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_all_button.grid(row=8, column=1, pady=5, padx=5)
        self.bind_hover_effects(export_all_button)

        brand_label = tk.Label(edit_vehicle_frame, text="Brand:",
                               font=("Helvetica", 10), fg="white", bg="black")
        brand_label.grid(row=1, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        brand_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        brand_entry.grid(row=1, column=3, pady=5, padx=(5, 20), sticky=tk.W)
        
        model_label = tk.Label(edit_vehicle_frame, text="Model:",
                               font=("Helvetica", 10), fg="white", bg="black")
        model_label.grid(row=2, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        model_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        model_entry.grid(row=2, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        color_label = tk.Label(edit_vehicle_frame, text="Color:",
                               font=("Helvetica", 10), fg="white", bg="black")
        color_label.grid(row=3, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        color_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        color_entry.grid(row=3, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        license_plate_label = tk.Label(edit_vehicle_frame, text="License Plate:",
                                       font=("Helvetica", 10), fg="white", bg="black")
        license_plate_label.grid(row=4, column=2, pady=5, padx=(30, 5), sticky=tk.E)

        license_plate_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        license_plate_entry.grid(row=4, column=3, pady=5, padx=(5, 20), sticky=tk.W)

        wheels_label = tk.Label(edit_vehicle_frame, text="Number of Wheels:",
                                font=("Helvetica", 10), fg="white", bg="black")
        wheels_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)

        wheels_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        wheels_entry.grid(row=1, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        seats_label = tk.Label(edit_vehicle_frame, text="Seats:",
                               font=("Helvetica", 10), fg="white", bg="black")
        seats_label.grid(row=2, column=4, pady=5, padx=(40, 5), sticky=tk.E)

        seats_entry = tk.Entry(edit_vehicle_frame, bd=2, width=10)
        seats_entry.grid(row=2, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        send_for_inspection_button = tk.Button(edit_vehicle_frame, text="Send Vehicle for Inspection", width=22, borderwidth=2,
                                         fg="white", bg="black", state=DISABLED)
        send_for_inspection_button.grid(row=5, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(send_for_inspection_button)

        send_for_legalization_button = tk.Button(edit_vehicle_frame, text="Send Vehicle for Legalization", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        send_for_legalization_button.grid(row=5, column=4, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(send_for_legalization_button)

        confirm_inspection_button = tk.Button(edit_vehicle_frame, text="Confirm Vehicle Inspection", width=22, borderwidth=2,
                                         fg="white", bg="black", state=DISABLED)
        confirm_inspection_button.grid(row=6, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(confirm_inspection_button)

        confirm_legalization_button = tk.Button(edit_vehicle_frame, text="Confirm Vehicle Legalization", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        confirm_legalization_button.grid(row=6, column=4, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(confirm_legalization_button)

        check_client_button = tk.Button(edit_vehicle_frame, text="Check Current Client", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_client_button.grid(row=7, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(check_client_button)

        check_reservation_button = tk.Button(edit_vehicle_frame, text="Check Current Reservation", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_reservation_button.grid(row=7, column=4, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_reservation_button)

        check_client_history_button = tk.Button(edit_vehicle_frame, text="Check Client History", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_client_history_button.grid(row=8, column=2, columnspan=2, pady=5, padx=(50, 20), sticky="w")
        self.bind_hover_effects(check_client_history_button)

        check_reservation_history_button = tk.Button(edit_vehicle_frame, text="Check Reservation History", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_reservation_history_button.grid(row=8, column=4, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_reservation_history_button)

        if df is not None and not df.empty:
            print("df is not none")
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to manage clients
    def manage_clients_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(pady=(140, 0))

        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)

        edit_treeview_frame.configure(bg="black")

        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("client", con=engine)

            engine.dispose()
        except ValueError:
            print("ValueError")


        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")
            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'f_name', 'dob', 'p_n_indicative', 'p_number', 'email', 'nationality', 
                                                      'address', 'id_type', 'id_number', 'credit_number', 'bill_address', 'p_car', 'p_moto', 
                                                      'm_license', 'em_name', 'p_em_indicative', 'em_number', 'photos', 'renting', 'code_renting',
                                                       'last_update', 'code_last_update', 'insertion_date', 'code_insertion'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'f_name': df.at[x, 'f_name'],
                            'dob': df.at[x, 'dob'],
                            'p_n_indicative': df.at[x, 'p_n_indicative'], 
                            'p_number': df.at[x, 'p_number'], 
                            'email': df.at[x, 'email'], 
                            'nationality': df.at[x, 'nationality'],
                            'address': df.at[x, 'address'], 
                            'id_type': df.at[x, 'id_type'], 
                            'id_number': df.at[x, 'id_number'], 
                            'credit_number': df.at[x, 'credit_number'],
                            'bill_address': df.at[x, 'bill_address'], 
                            'p_car': df.at[x, 'p_car'], 
                            'p_moto': df.at[x, 'p_moto'],
                            'm_license': df.at[x, 'm_license'], 
                            'em_name': df.at[x, 'em_name'], 
                            'p_em_indicative': df.at[x, 'p_em_indicative'],
                            'em_number': df.at[x, 'em_number'], 
                            'photos': df.at[x, 'photos'], 
                            'renting': df.at[x, 'renting'],
                            'code_renting': df.at[x, 'code_renting'], 
                            'last_update': df.at[x, 'last_update'], 
                            'code_last_update': df.at[x, 'code_last_update'],
                            'insertion_date': df.at[x, 'insertion_date'],
                            'code_insertion': df.at[x, 'code_insertion']
                        }

                        new_df_record = pd.DataFrame([new_df_record]) 

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")

            # Function to see the information about the current reservations of the selected client
            def check_client_reservation():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["client", "reservation", str(df.at[x, 'id_number']), "current"]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            # Function to see the information about the current vehicles of the selected client
            def check_vehicle_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_vehicle = ["client", "vehicle", str(df.at[x, 'id_number']), "current"]
                    self.pop_warning(new_window, get_vehicle, "showdbiteminfo")

            # Function to see the reservation history of the selected client
            def check_reservation_history():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["client", "reservation", str(df.at[x, 'id_number']), "history"]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            # Function to see the vehicle history of the selected client
            def check_vehicle_history():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_vehicle = ["client", "vehicle", str(df.at[x, 'id_number']), "history"]
                    self.pop_warning(new_window, get_vehicle, "showdbiteminfo")
                                    
            def verify_data():
                for index, row in df.iterrows():
                    not_num = []
                    must_be_number = {
                        'Phone Number': row['p_number'],
                        'Credit Card Number': row['credit_number'],
                        'Emergency Contact Number': row['em_number']                           
                    }

                    for column_num, value_num in must_be_number.items():
                        try:
                            int(value_num)
                        except ValueError:
                            not_num.append(value_num)

                    not_alpha = []
                    must_not_have_number = {
                        'Full Name': str(row['f_name']),
                        'Identification Type': str(row['id_type']),
                        'Preferred Car Type': str(row['p_car']),
                        'Preferred Motorcycle Type': str(row['p_moto']),
                        'Emergency Contact Name': str(row['em_name'])
                    }

                    for column_word, value_word in must_not_have_number.items():
                        clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                        if all(char.isalpha() for char in clean_value_word):
                            pass
                        else:
                            not_alpha.append(value_word)

                    is_empty = []
                    all_data = {
                        'Date of Birth': str(row['dob']),
                        'Phone Number Indicative': str(row['p_n_indicative']),
                        'Phone Number': str(row['p_number']),
                        'ID/Passport Number': str(row['id_number']),
                        'Credit Card Number': str(row['credit_number']),
                        'Emergency Contact Indicative': str(row['p_em_indicative']),
                        'Emergency Contact Number': str(row['em_number']),
                        'Full Name': str(row['f_name']),
                        'Identification Type': str(row['id_type']),
                        'Preferred Car Type': str(row['p_car']),
                        'Preferred Motorcycle Type': str(row['p_moto']),
                        'Emergency Contact Name': str(row['em_name']),
                        'Email': str(row['email']),
                        'Address': str(row['address']),
                        'Billing Address': str(row['bill_address']),
                        'Motorcycle License': str(row['m_license']),
                        'Client ID Photos': str(row['photos'])
                    }

                    for column_all, value_all in all_data.items():
                        if value_all == 'nan':
                            is_empty.append(value_all)
                        else:
                            pass

                    not_defined = []
                    must_be_defined = {
                        'Identification Type': (str(row['id_type']), id_types),
                        'Preferred Car Type': (str(row['p_car']), car_types),
                        'Preferred Motorcycle Type': (str(row['p_moto']), moto_types),
                        'Motorcycle License': (str(row['m_license']), license_class),
                        'Nationality': (str(row['nationality']), nationalities)
                    }

                    for column_defined, value_defined in must_be_defined.items():
                        if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                            not_defined.append(value_defined)
                        else:
                            pass

                    errors_found = not_num, not_alpha, is_empty, not_defined

                    possible_photo_path_list = str(row['photos'])

                    self.verify_photo_path(possible_photo_path_list)
                    if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                        pass
                    if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        is_empty.append("Photos")

                    date_to_check = str(row['dob'])
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    if any(len(error_list) > 0 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False:
                        result_of_validation = "Error Found"
                        self.change_row_color(treeview, index, "darkred")
                    else:
                        self.change_row_color(treeview, index, "#313131")
                        result_of_validation = "No Error Found"

                    if str(row['renting']) == "Yes":
                        self.change_row_color(treeview, index, "#ADD8E6")

            def refresh_tree(df):
                treeview.delete(*treeview.get_children())

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                df['dob'] = df['dob'].apply(convert_to_datetime)
                df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)

                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")

                columns_to_int = ['p_number', 'credit_number', 'em_number', 'p_n_indicative', 'p_em_indicative', 'id_number']
                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass             
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])
                    
                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0 
                    
                    column_width = max(heading_width, max_width) + 20 
                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.column("photos", width=120, minwidth=120)

                treeview.update_idletasks()

                verify_data()

            def clear_entries():
                entries = [p_n_indicative_entry, employee_code_entry, p_em_indicative_entry, full_name_entry, phone_entry, email_entry, address_entry, id_number_entry, credit_card_entry, billing_address_entry,
                            emergency_name_entry, emergency_phone_entry]
                for entry in entries:
                    entry.delete(0, END)
                    self.toggle_entry_colors(1, entry)

                read_only_entries = [dob_entry]
                for entry in read_only_entries:
                    entry.config(state=tk.NORMAL)
                    entry.delete(0, tk.END)
                    entry.config(state="readonly", readonlybackground="#313131")

                combos = [[id_type_combobox, id_types],[car_type_combobox, car_types], [moto_type_combobox, moto_types], [license_class_combobox, license_class], [nation_combobox, nationalities]]
                for combo in combos:
                    self.toggle_combo_text(1, combo[0])
                    combo[0].set(combo[1][0])

                if hasattr(self, 'photo_paths'):
                    del self.photo_paths
                see_photos_button.configure(state=tk.DISABLED)
                reload_show_photos_button.configure(image=self.update_photos_button_image)

            def select_record(e):
                clear_entries()
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    export_selected_button.configure(state=NORMAL)
                    client_reservations = Reservation.query.filter_by(id_passport_number=str(df.at[x, "id_number"]).lower()).all()
                    client_reservations_in_progress = Reservation.query.filter_by(id_passport_number=str(df.at[x, "id_number"]).lower(), reservation_state="In progress").all()

                    if len(client_reservations) > 0:
                        check_reservation_history_button.configure(state=NORMAL)
                        check_vehicle_history_button.configure(state=NORMAL)
                        if len(client_reservations_in_progress) > 0:
                            check_reservation_button.configure(state=NORMAL)
                            check_vehicle_button.configure(state=NORMAL)
                        else:
                            check_reservation_button.configure(state=DISABLED)
                            check_vehicle_button.configure(state=DISABLED)     
                    else:
                        check_reservation_history_button.configure(state=DISABLED)
                        check_vehicle_history_button.configure(state=DISABLED)
                        check_reservation_button.configure(state=DISABLED)
                        check_vehicle_button.configure(state=DISABLED)

                    type_id = str(df.at[x, "id_type"]).lower()

                    id_type_combobox.set(id_types[0])  
                    mapping = {t.lower(): id_types[i] for i, t in enumerate(id_types)}
                    id_type_combobox.set(mapping.get(type_id, mapping["not defined"]))

                    if id_type_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, id_type_combobox)
                    else:
                        self.toggle_combo_text(1, id_type_combobox)

                    p_car = str(df.at[x, "p_car"]).lower()

                    car_type_combobox.set(car_types[0]) 
                    mapping = {c.lower(): car_types[i] for i, c in enumerate(car_types)}
                    car_type_combobox.set(mapping.get(p_car, mapping["not defined"]))

                    if car_type_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, car_type_combobox)
                    else:
                        self.toggle_combo_text(1, car_type_combobox)

                    p_moto = str(df.at[x, "p_moto"]).lower()

                    moto_type_combobox.set(moto_types[0]) 
                    mapping = {m.lower(): moto_types[i] for i, m in enumerate(moto_types)}
                    moto_type_combobox.set(mapping.get(p_moto, mapping["not defined"]))

                    if moto_type_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, moto_type_combobox)
                    else:
                        self.toggle_combo_text(1, moto_type_combobox)

                    license = str(df.at[x, "m_license"]).lower()

                    license_class_combobox.set(license_class[0]) 
                    mapping = {c.lower(): license_class[i] for i, c in enumerate(license_class)}
                    license_class_combobox.set(mapping.get(license, mapping["not defined"]))

                    if license_class_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, license_class_combobox)
                    else:
                        self.toggle_combo_text(1, license_class_combobox)

                    nation = str(df.at[x, 'nationality']).lower()

                    nation_combobox.set(nationalities[0]) 
                    mapping = {n.lower(): nationalities[i] for i, n in enumerate(nationalities)}
                    nation_combobox.set(mapping.get(nation, mapping["not defined"]))

                    if nation_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, nation_combobox)
                    else:
                        self.toggle_combo_text(1, nation_combobox)

                    full_name_entry.insert(0, df.at[x, "f_name"])
                    phone_entry.insert(0, df.at[x, "p_number"])
                    email_entry.insert(0, df.at[x, "email"])
                    address_entry.insert(0, df.at[x, "address"])
                    id_number_entry.insert(0, df.at[x, "id_number"])
                    credit_card_entry.insert(0, df.at[x, "credit_number"])
                    billing_address_entry.insert(0, df.at[x, "bill_address"])
                    emergency_name_entry.insert(0, df.at[x, "em_name"])
                    emergency_phone_entry.insert(0, df.at[x, "em_number"])
                    p_n_indicative_entry.insert(0, df.at[x, "p_n_indicative"])
                    p_em_indicative_entry.insert(0, df.at[x, "p_em_indicative"])

                    dob_entry.config(state=tk.NORMAL)
                    dob_entry.insert(0, df.at[x, "dob"])
                    dob_entry.config(state="readonly")

                    date_to_check = str(df.at[x, "dob"])
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"
                    print(f"Date check: {bool(re.match(pattern, date_to_check))}")
                    if bool(re.match(pattern, date_to_check)) == False:
                        dob_entry.config(readonlybackground="darkred")
                    else:
                        dob_entry.config(readonlybackground="#313131")

                    must_not_empty_entries = {
                        full_name_entry: full_name_entry.get(),
                        p_n_indicative_entry: p_n_indicative_entry.get(),
                        p_em_indicative_entry: p_em_indicative_entry.get(),
                        dob_entry: dob_entry.get(),
                        phone_entry: phone_entry.get(),
                        email_entry: email_entry.get(),
                        address_entry: address_entry.get(),
                        id_number_entry: id_number_entry.get(),
                        credit_card_entry: credit_card_entry.get(),
                        billing_address_entry: billing_address_entry.get(),
                        emergency_name_entry: emergency_name_entry.get(),
                        emergency_phone_entry: emergency_phone_entry.get()
                    }
                    for column_entry_check, value_check in must_not_empty_entries.items():
                        if str(value_check).lower() == 'nan':
                            self.toggle_entry_colors_ifnan(0, column_entry_check)
                            column_entry_check.delete(0, "end")
                            column_entry_check.insert(0, "EMPTY")
                        else:
                            self.toggle_entry_colors_ifnan(1, column_entry_check)

                    must_be_number_entries = {
                        phone_entry: phone_entry.get(),
                        credit_card_entry: credit_card_entry.get(),
                        emergency_phone_entry: emergency_phone_entry.get()
                    }
                    for value_key, value in must_be_number_entries.items():
                        try:
                            int(value)
                            self.toggle_entry_colors(1, value_key)
                        except ValueError:
                            self.toggle_entry_colors(0, value_key)

                    must_not_have_number_entries = {
                        full_name_entry: full_name_entry.get(),
                        emergency_name_entry: emergency_name_entry.get()
                    }
                    for word_key, word in must_not_have_number_entries.items():
                        if any(not char.isalpha() for char in word) or str(word).lower() == "empty":
                            self.toggle_entry_colors(0, word_key)
                        else:
                            self.toggle_entry_colors(1, word_key)

                    self.verify_photo_path(str(df.at[x, "photos"]))
                    if str(df.at[x, "photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        self.toggle_button_colors(0, selected_client_photos_button)
                        self.red_bind_hover_effects(selected_client_photos_button)
                    else:
                        self.toggle_button_colors(1, selected_client_photos_button)
                        self.bind_hover_effects(selected_client_photos_button)
                        print(df.at[x, "photos"])
                else:
                    pass

            def update_record():
                must_be_number = {
                        'Phone Number': (phone_entry.get(), phone_entry),
                        'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                        'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry)
                    }

                must_not_have_number = {
                        'Full Name': (full_name_entry.get(), full_name_entry),
                        'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry)
                    }

                must_be_defined = {
                        'Identification Type': (selected_id_type.get(), id_type_combobox),
                        'Preferred Car Type': (selected_car_type.get(), car_type_combobox),
                        'Preferred Motorcycle Type': (selected_moto_type.get(), moto_type_combobox),
                        'Nationality' : (selected_nation.get(), nation_combobox),
                        'Motorcycle License': (selected_license_class.get(), license_class_combobox)
                }

                must_not_be_empty = {
                        'Date of Birth': (dob_entry.get(), dob_entry),
                        'Phone Number': (phone_entry.get(), phone_entry),
                        'Phone Number Indicative': (p_n_indicative_entry.get(), p_n_indicative_entry),
                        'Emergency Contact Indicative': (p_em_indicative_entry.get(), p_em_indicative_entry),
                        'ID/Passport Number': (id_number_entry.get(), id_number_entry),
                        'Credit Card Number': (credit_card_entry.get(), credit_card_entry),
                        'Emergency Contact Number': (emergency_phone_entry.get(), emergency_phone_entry),
                        'Full Name': (full_name_entry.get(), full_name_entry),
                        'Emergency Contact Name': (emergency_name_entry.get(), emergency_name_entry),
                        'Email': (email_entry.get(), email_entry),
                        'Address': (address_entry.get(), address_entry),
                        'Billing Address': (billing_address_entry.get(), billing_address_entry)
                    }


                self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    self.verify_photo_path(str(df.at[x, 'photos']))

                    if str(df.at[x, 'photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        if hasattr(self, 'photo_paths'):
                            pass
                        else:
                            is_empty.append("Photos")

                    date_to_check = str(dob_entry.get())
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    if any(len(error_list) > 1 for error_list in errors_found) or bool(re.match(pattern, date_to_check)) == False: 
                        result_of_validation = "Error Found"
                    else:
                        result_of_validation = "No Error Found"

                    if result_of_validation == "No Error Found":
                        result = self.check_employee_code(str(employee_code_entry.get()), False)
                        if result == "valid":
                            self.toggle_entry_colors(1, employee_code_entry)

                            cleaned_id_number = re.sub(r'[^\w\s]', '', str(df.at[x, 'id_number']).lower())
                            client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first()

                            new_id = re.sub(r'[^\w\s]', '', str(id_number_entry.get()).lower())
                            new_p_number = phone_entry.get()
                            new_credit_number = credit_card_entry.get()
                            new_em_number = emergency_phone_entry.get()
                            new_email = re.sub(r'[^\w\s]', '', str(email_entry.get()).lower())

                            exists_info = False
                            if new_id == client.id_number and new_p_number == client.p_number and new_credit_number == client.credit_number and new_em_number == client.em_number:
                                pass
                            else: 
                                existing_id = Client.query.filter(Client.id_number.ilike(new_id)).first()
                                existing_p_number = Client.query.filter(Client.p_number.ilike(new_p_number)).first()
                                existing_credit_number = Client.query.filter(Client.credit_number.ilike(new_credit_number)).first()
                                existing_em_number = Client.query.filter(Client.em_number.ilike(new_em_number)).first()

                                must_be_none = ([existing_id, new_id, client.id_number], [existing_p_number, new_p_number, client.p_number],
                                    [existing_credit_number, new_credit_number, client.credit_number], [existing_em_number, new_em_number, client.em_number])

                                exists = []
                                for must_be in must_be_none:
                                    if must_be[1] == must_be[2]:
                                        pass
                                    elif must_be[1] != must_be[2]:
                                        if must_be[0] is not None:
                                            exists.append(must_be[1])

                                if len(exists) > 0:
                                    exists_info = True
                                    self.pop_warning(new_window, exists, "updateexistingclientinfo")
                            if exists_info == True:
                                pass
                            elif exists_info == False:
                                if client.renting == "Yes":
                                    warning = "The selected record can't be updated now due to be currently renting"
                                    self.pop_warning(new_window, warning, "cantupdaterented")
                                else:
                                    try:
                                        date_update = str(datetime.now(timezone.utc).date())

                                        client.f_name = full_name_entry.get()
                                        client.dob = str(dob_entry.get())
                                        client.p_n_indicative = str(p_n_indicative_entry.get())
                                        client.p_number = str(phone_entry.get())
                                        client.email = str(email_entry.get())
                                        client.address = str(address_entry.get())
                                        client.nationality = selected_nation.get()
                                        client.id_type = selected_id_type.get()
                                        client.id_number = new_id
                                        client.credit_number = str(credit_card_entry.get())
                                        client.bill_address = str(billing_address_entry.get())
                                        client.p_car = selected_car_type.get()
                                        client.m_license = str(selected_license_class.get())
                                        client.p_moto = selected_moto_type.get()
                                        client.p_em_indicative = str(p_em_indicative_entry.get())
                                        client.em_name = emergency_name_entry.get()
                                        client.em_number = str(emergency_phone_entry.get())
                                        client.code_last_update = str(employee_code_entry.get())
                                        client.last_update = str(date_update)

                                        if hasattr(self, 'photo_paths'):
                                            client.photos = self.photo_paths
                                        else:
                                            pass

                                        db.session.commit()
                                        self.toggle_button_colors(1, selected_client_photos_button)

                                        df.at[x, "dob"] = dob_entry.get()
                                        df.at[x, "p_n_indicative"] = str(p_n_indicative_entry.get())
                                        df.at[x, "p_em_indicative"] = str(p_em_indicative_entry.get())
                                        df.at[x, "p_number"] = int(phone_entry.get())
                                        df.at[x, "nationality"] = selected_nation.get()
                                        df.at[x, "id_number"] = str(id_number_entry.get())
                                        df.at[x, "credit_number"] = int(credit_card_entry.get())
                                        df.at[x, "em_number"] = int(emergency_phone_entry.get())
                                        df.at[x, "f_name"] = full_name_entry.get()
                                        df.at[x, "em_name"] = emergency_name_entry.get()
                                        df.at[x, "email"] = email_entry.get()
                                        df.at[x, "address"] = address_entry.get()
                                        df.at[x, "bill_address"] = billing_address_entry.get()
                                        df.at[x, "id_type"] = selected_id_type.get()
                                        df.at[x, "p_car"] = selected_car_type.get()
                                        df.at[x, "p_moto"] = selected_moto_type.get()
                                        df.at[x, "m_license"] = selected_license_class.get()
                                        df.at[x, "code_last_update"] = str(employee_code_entry.get())
                                        df.at[x, "last_update"] = str(date_update)

                                        if hasattr(self, 'photo_paths'):
                                            df.at[x, 'photos'] = self.photo_paths
                                        else:
                                            pass

                                        clear_entries()
                                        refresh_tree(df)

                                    except OperationalError as e:
                                        warning = "Database is locked. Please close the Database and try again."
                                        self.pop_warning(new_window, warning, "databaselocked")
                                        db.session.rollback()
                                        print("Database is locked. Please try again later.")
                        else:
                            self.toggle_entry_colors(0, employee_code_entry)
                            self.pop_warning(new_window, result, "wrongemployeecode")      
                    else:

                        if bool(re.match(pattern, date_to_check)) == False:
                            wrong_text_format = str(df.at[x,'year'])
                            self.pop_warning(new_window, wrong_text_format, "wrongdatetextformat")

                        for key in must_not_be_empty:
                            if key in is_empty:
                                entry_value = must_not_be_empty[key][1]
                                self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                            else:
                                self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                        for key in must_be_defined:
                            if key in not_defined:
                                combobox_value = must_be_defined[key][1]
                                self.toggle_combo_text(0, must_be_defined[key][1])
                            else:
                                self.toggle_combo_text(1, must_be_defined[key][1])

                        for key in must_not_have_number:
                            if key in not_alpha or key in is_empty:
                                entry_value = must_not_have_number[key][1]
                                self.toggle_entry_colors(0, must_not_have_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_not_have_number[key][1])

                        if "Photos" in is_empty:
                            self.toggle_button_colors(0, select_photos_button)
                            self.red_bind_hover_effects(select_photos_button)
                        else:
                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                        for key in must_be_number:
                            if key in not_num or key in is_empty:
                                entry_value = must_be_number[key][1]
                                self.toggle_entry_colors(0, must_be_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_be_number[key][1])

                        errors_adding = []
                        for error_list in errors_found:
                            if len(error_list) > 1:
                                errors_adding.append(error_list)

                        if len(errors_adding) > 0:
                            self.pop_warning(new_window, errors_adding, "addrecvalidation")
                else:
                    warning = "Must select an item to Update"
                    self.pop_warning(new_window, warning, "noselectedtoupdate" )

            def remove_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    try:
                        if len(selected_items) == Client.query.count():
                            warning = "Can not delete all the data from the Client Database"
                            self.pop_warning(new_window, warning, "cannotdeletealldb" )
                        else:
                            code_check=self.check_employee_code(str(employee_code_entry.get()), True)
                            if code_check == "valid":
                                self.toggle_entry_colors(1, employee_code_entry)
                                can_not_delete = []
                                for record in selected_items:
                                    x = treeview.index(record)
                                    client = Client.query.filter(Client.id_number.ilike(str(df.at[x, 'id_number']).lower())).first()
                                    if client.renting == "Yes":
                                        can_not_delete.append(client.id_number)
                                    else:
                                        db.session.delete(client)
                                        db.session.commit()     
                                        treeview.delete(record)
                                        df.drop(index=x, inplace=True)
                                        df.reset_index(drop=True, inplace=True)
                                verify_data()
                                clear_entries()
                                if len(can_not_delete) > 0:
                                    self.pop_warning(new_window, can_not_delete, "cannotdeleteclient")
                            else:
                                self.toggle_entry_colors(0, employee_code_entry)
                                self.pop_warning(new_window, code_check, "wrongemployeecode")
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    warning = "Must select at least one record to remove"
                    self.pop_warning(new_window, warning, "noselectedtoremove")

            def selected_client_photos():
                selected_items = treeview.selection()
                print(selected_items)
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    photos_of_selected = str(df.at[x, "photos"])

                    if photos_of_selected.lower() != "nan":
                        self.verify_photo_path(photos_of_selected)

                        if len(valid_photo_type) > 0:
                            if len(valid_photo_paths) > 0:
                                def handle_photo_viewer_result(result, updated_photos):
                                    if result == "confirm":
                                        try:
                                            id_number = re.sub(r'[^\w\s]', '', str(df.at[x, 'id_number']).lower())
                                            client = Client.query.filter(Client.id_number.ilike(id_number)).first()
                                            client.photos = updated_photos
                                            db.session.commit()
                                            df.at[x, 'photos'] = updated_photos
                                        except OperationalError as e:
                                            warning = "Database is locked. Please close the Database and try again."
                                            self.pop_warning(new_window, warning, "databaselocked")
                                            db.session.rollback()
                                            print("Database is locked. Please try again later.")
                                    elif result == "cancel":
                                        print("User cancelled changes")

                                if str(df.at[x, "renting"]) == "Yes":
                                    mode = "View Mode"
                                else:
                                    mode = "Edit Mode"

                                updated_photos = []
                                self.photo_viewer(new_window, valid_photo_paths, mode, handle_photo_viewer_result, updated_photos)
                            if len(invalid_photo_paths) > 0:
                                self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                self.toggle_button_colors(0, selected_client_photos_button)
                        for path in invalid_photo_type:
                            if path == "":
                                invalid_photo_type.remove(path)
                        if len(invalid_photo_type) > 0:
                            self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                            self.toggle_button_colors(0, selected_client_photos_button)
                    else:
                        x += 1
                        self.pop_warning(new_window, str(x), "nanselectedphoto")
                        self.toggle_button_colors(0, selected_client_photos_button)
                else:
                    warning = "Must select a record to see photos"
                    self.pop_warning(new_window, warning, "noselectedtoseephotos")

            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                   command=update_record)
            update_button.grid(row=0, column=0, padx=5, pady=3)
            self.bind_hover_effects(update_button)

            clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                          command=clear_entries)
            clear_entries_button.grid(row=0, column=1, padx=5, pady=3)
            self.bind_hover_effects(clear_entries_button)

            selected_client_photos_button = Button(edit_treeview_frame, text="See Selected Client Photos",
                                                    fg="white",
                                                    bg="black", command=selected_client_photos)
            selected_client_photos_button.grid(row=0, column=2, padx=5, pady=3)
            self.bind_hover_effects(selected_client_photos_button)

            remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                            bg="black", command=remove_selected)
            remove_selected_button.grid(row=0, column=3, padx=5, pady=3)
            self.bind_hover_effects(remove_selected_button)

            refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                       bg="black", command=lambda: refresh_tree(df))
            refresh_tree_button.grid(row=0, column=4, padx=5, pady=3)
            self.bind_hover_effects(refresh_tree_button)

            employee_code_label = tk.Label(edit_treeview_frame, text="Employee Code:",
                              font=("Helvetica", 10), fg="white", bg="black")
            employee_code_label.grid(row=0, column=5, pady=5, padx=(20, 5), sticky=tk.E)

            employee_code_entry = tk.Entry(edit_treeview_frame, bd=2, width=10)
            employee_code_entry.grid(row=0, column=6, padx=5, pady=3)

            treeview.bind("<ButtonRelease-1>", select_record)

            check_reservation_button.config(command=check_client_reservation)
            check_vehicle_button.config(command=check_vehicle_info)
            check_reservation_history_button.config(command=check_reservation_history)
            check_vehicle_history_button.config(command=check_vehicle_history)
            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)

                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))
                reload_show_photos_button.configure(image=self.update_photos_button_image)

        edit_client_frame = tk.Frame(new_window)
        edit_client_frame.configure(bg="black")
        edit_client_frame.pack(pady=(0,10))

        full_name_label = tk.Label(edit_client_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        full_name_label.grid(row=0, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        full_name_entry.grid(row=0, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        dob_button = tk.Button(edit_client_frame, text="Select Date of Birth", width=15, borderwidth=2,
                                              fg="white", bg="black", command=lambda: self.datepicker(new_window, dob_entry, "dob"))

        dob_button.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        dob_entry = tk.Entry(edit_client_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        dob_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        phone_indicative_label = tk.Label(edit_client_frame, text="Phone Indicative:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_indicative_label.grid(row=2, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        p_n_indicative_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        p_n_indicative_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(edit_client_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        phone_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(edit_client_frame, text="Email:",
                               font=("Helvetica", 10), fg="white", bg="black")
        email_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        email_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        address_label = tk.Label(edit_client_frame, text="Address:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        address_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        address_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        address_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        nation_label = tk.Label(edit_client_frame, text="Nationality:",
                         font=("Helvetica", 10), fg="white", bg="black")
        nation_label.grid(row=6, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        nationalities = [
            "Not Defined","Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean", "Armenian", "Australian", "Austrian", "Azerbaijani",
            "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Barbudans", "Batswana", "Belarusian", "Belgian", "Belizean", "Beninese", "Bhutanese", "Bolivian",
            "Bosnian", "Brazilian", "British", "Bruneian", "Bulgarian", "Burkinabe", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean",
            "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese", "Costa Rican", "Croatian", "Cuban", "Cypriot", "Czech",
            "Danish", "Djibouti", "Dominican", "Dutch", "East Timorese", "Ecuadorean", "Egyptian", "Emirian", "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian",
            "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Greek", "Grenadian", "Guatemalan", "Guinea-Bissauan",
            "Guinean", "Guyanese", "Haitian", "Herzegovinian", "Honduran", "Hungarian", "I-Kiribati", "Icelander", "Indian", "Indonesian", "Iranian", "Iraqi",
            "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakhstani", "Kenyan", "Kittian and Nevisian", "Kuwaiti", "Kyrgyz",
            "Laotian", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtensteiner", "Lithuanian", "Luxembourger", "Macedonian", "Malagasy", "Malawian", "Malaysian",
            "Maldivan", "Malian", "Maltese", "Marshallese", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monacan", "Mongolian", "Moroccan",
            "Mosotho", "Motswana", "Mozambican", "Namibian", "Nauruan", "Nepalese", "New Zealander", "Ni-Vanuatu", "Nicaraguan", "Nigerian", "Nigerien", "North Korean",
            "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Panamanian", "Papua New Guinean", "Paraguayan", "Peruvian", "Polish", "Portuguese", "Qatari",
            "Romanian", "Russian", "Rwandan", "Saint Lucian", "Salvadoran", "Samoan", "San Marinese", "Sao Tomean", "Saudi", "Scottish", "Senegalese", "Serbian",
            "Seychellois", "Sierra Leonean", "Singaporean", "Slovakian", "Slovenian", "Solomon Islander", "Somali", "South African", "South Korean", "Spanish", "Sri Lankan",
            "Sudanese", "Surinamer", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian or Tobagonian",
            "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani", "Venezuelan", "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"
        ]
        selected_nation = tk.StringVar()
        nation_combobox = ttk.Combobox(edit_client_frame,
                                        textvariable=selected_nation,
                                        values=nationalities, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        nation_combobox.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        nation_combobox.set(nationalities[0]) 

        id_type_label = tk.Label(edit_client_frame, text="Identification Type:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        id_type_label.grid(row=0, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        id_types = ["Not Defined", "National ID", "Passport"]
        selected_id_type = tk.StringVar()
        id_type_combobox = ttk.Combobox(edit_client_frame,
                                        textvariable=selected_id_type,
                                        values=id_types, state="readonly", justify="center", height=4,
                                        style="TCombobox")
        id_type_combobox.grid(row=0, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        id_type_combobox.set(id_types[0])  

        id_number_label = tk.Label(edit_client_frame, text="ID/Passport Number:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        id_number_label.grid(row=1, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        id_number_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        id_number_entry.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        credit_card_label = tk.Label(edit_client_frame, text="Credit Card Number:",
                                     font=("Helvetica", 10), fg="white", bg="black")
        credit_card_label.grid(row=2, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        credit_card_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        credit_card_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        billing_address_label = tk.Label(edit_client_frame, text="Billing Address:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        billing_address_label.grid(row=3, column=2, pady=5, padx=(30, 5), sticky=tk.E)
        billing_address_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        billing_address_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        moto_license_label = tk.Label(edit_client_frame, text="Motorcycle License:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        moto_license_label.grid(row=4, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        license_class = ["Not Defined", "Not Applicable", "A1(125cc|11kw|0.1kw/kg)", "A2(max-35kw|0.2kw/kg)", "A"]
        selected_license_class = tk.StringVar()
        license_class_combobox = ttk.Combobox(edit_client_frame,
                                        textvariable=selected_license_class,
                                        values=license_class, state="readonly", justify="center", height=4,
                                        style="TCombobox")
        license_class_combobox.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        license_class_combobox.set(id_types[0])  

        car_type_label = tk.Label(edit_client_frame, text="Preferred Car Type:",
                                  font=("Helvetica", 10), fg="white", bg="black")
        car_type_label.grid(row=0, column=4, pady=5, padx=(30, 5), sticky=tk.E)
        car_types = ["Not Defined", "None", "Microcar", "Subcompact", "Compact", "Midsize", "Full-size", "SUV", "Crossover",
                     "Multi-Purpose Vehicle", "Convertible/Cabriolet", "Coupe", "Roadster", "Hot Hatch", "Sports Car"]
        selected_car_type = tk.StringVar()
        car_type_combobox = ttk.Combobox(edit_client_frame, textvariable=selected_car_type,
                                         values=car_types, state="readonly", justify="center", height=4)
        car_type_combobox.grid(row=0, column=5, pady=5, padx=(5, 20), sticky=tk.W)
        car_type_combobox.set(car_types[0]) 

        moto_type_label = tk.Label(edit_client_frame,
                                   text="Preferred Motorcycle Type:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        moto_type_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        moto_types = ["Not Defined", "None", "Sport Bikes", "Cruisers", "Touring Bikes", "Naked Bikes",
                      "Adventure Bikes", "Dirt Bikes", "Scooters",
                      "Electric Motorcycles", "Cafe Racers", "Choppers",
                      "Bobbers", "Trikes"]
        selected_moto_type = tk.StringVar()
        moto_type_combobox = ttk.Combobox(edit_client_frame,
                                          textvariable=selected_moto_type,
                                          values=moto_types, state="readonly", justify="center", height=4)
        moto_type_combobox.grid(row=1, column=5, pady=5, padx=(5, 20), sticky=tk.W)
        moto_type_combobox.set(moto_types[0]) 

        emergency_name_label = tk.Label(edit_client_frame, text="Emergency Contact Name:",
                                        font=("Helvetica", 10), fg="white", bg="black")
        emergency_name_label.grid(row=2, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        emergency_name_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        emergency_name_entry.grid(row=2, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        emergency_phone_indicative_label = tk.Label(edit_client_frame, text="Emergency Contact Indicative:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        emergency_phone_indicative_label.grid(row=3, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        p_em_indicative_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        p_em_indicative_entry.grid(row=3, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        emergency_phone_label = tk.Label(edit_client_frame, text="Emergency Contact Number:",
                                         font=("Helvetica", 10), fg="white", bg="black")
        emergency_phone_label.grid(row=4, column=4, pady=5, padx=(40, 5), sticky=tk.E)
        emergency_phone_entry = tk.Entry(edit_client_frame, bd=2, width=10)
        emergency_phone_entry.grid(row=4, column=5, pady=5, padx=(5, 20), sticky=tk.W)

        select_photos_button = tk.Button(edit_client_frame, text="Select Client ID Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=5, column=3, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)

        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(edit_client_frame, text="See Client ID Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=5, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(edit_client_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=5, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)

        export_selected_button = tk.Button(edit_client_frame, text="Export Selected Data", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_selected_button.grid(row=6, column=2, pady=5, padx=5)
        self.bind_hover_effects(export_selected_button)

        export_all_button = tk.Button(edit_client_frame, text="Export All Data", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_all_button.grid(row=6, column=3, pady=5, padx=5)
        self.bind_hover_effects(export_all_button)

        check_vehicle_button = tk.Button(edit_client_frame, text="Check Current Vehicle", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_vehicle_button.grid(row=6, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(check_vehicle_button)

        check_reservation_button = tk.Button(edit_client_frame, text="Check Current Reservation", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_reservation_button.grid(row=6, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_reservation_button)

        check_vehicle_history_button = tk.Button(edit_client_frame, text="Check Vehicle History", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_vehicle_history_button.grid(row=7, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(check_vehicle_history_button)

        check_reservation_history_button = tk.Button(edit_client_frame, text="Check Reservation History", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_reservation_history_button.grid(row=7, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_reservation_history_button)

        if df is not None and not df.empty:
            print("df is not none")
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to manage reservations
    def manage_reservations_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(pady=(140, 0))
        
        edit_treeview_frame = tk.Frame(new_window)
        edit_treeview_frame.pack(pady=10)
        edit_treeview_frame.configure(bg="black")

        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("reservation", con=engine)
            engine.dispose()
        except ValueError:
            print("ValueError")


        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'pick_up_date', 'drop_off_date', 'vehicle_id', 'rental_duration', 'cost_per_day', 'total_cost', 
                                                      'full_name', 'phone_number', 'email', 'id_passport_number', 'date_of_birth', 'nationality', 'emergency_contact_name', 
                                                      'emergency_contact_number', 'billing_address', 'payment_method', 'photos', 'reservation_state', 'date_confirm_completed_renting', 'code_confirm_completed_renting',
                                                       'date_cancel_reservation', 'code_cancel_reservation', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'pick_up_date': df.at[x, 'pick_up_date'],
                            'drop_off_date': df.at[x, 'drop_off_date'],
                            'vehicle_id': df.at[x, 'vehicle_id'], 
                            'rental_duration': df.at[x, 'rental_duration'], 
                            'cost_per_day': df.at[x, 'cost_per_day'], 
                            'total_cost': df.at[x, 'total_cost'],
                            'full_name': df.at[x, 'full_name'], 
                            'phone_number': df.at[x, 'phone_number'], 
                            'email': df.at[x, 'email'], 
                            'id_passport_number': df.at[x, 'id_passport_number'],
                            'date_of_birth': df.at[x, 'date_of_birth'], 
                            'nationality': df.at[x, 'nationality'], 
                            'emergency_contact_name': df.at[x, 'emergency_contact_name'],
                            'emergency_contact_number': df.at[x, 'emergency_contact_number'], 
                            'billing_address': df.at[x, 'billing_address'], 
                            'payment_method': df.at[x, 'payment_method'],
                            'photos': df.at[x, 'photos'], 
                            'reservation_state': df.at[x, 'reservation_state'], 
                            'date_confirm_completed_renting': df.at[x, 'date_confirm_completed_renting'],
                            'code_confirm_completed_renting': df.at[x, 'code_confirm_completed_renting'], 
                            'date_cancel_reservation': df.at[x, 'date_cancel_reservation'], 
                            'code_cancel_reservation': df.at[x, 'code_cancel_reservation'],
                            'last_update': df.at[x, 'last_update'],
                            'code_last_update': df.at[x, 'code_last_update'],
                            'insertion_date': df.at[x, 'insertion_date'],
                            'code_insertion': df.at[x, 'code_insertion']
                        }

                        new_df_record = pd.DataFrame([new_df_record])

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")

            # Function to see the information of the client inserted in the selected reservation
            def check_client_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["reservation", "client", str(df.at[x, 'id_passport_number'])]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            # Function to see the information of the vehicle inserted in the selected reservation
            def check_vehicle_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_vehicle = ["reservation", "vehicle", str(df.at[x, 'vehicle_id'])]
                    self.pop_warning(new_window, get_vehicle, "showdbiteminfo")

            # Function that allows to confirm that the selected reservation is completed
            def confirm_completed_renting():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    print(employee_code_entry.get())
                    result = self.check_employee_code(str(employee_code_entry.get()), False)
                    print(result)
                    if result == "valid":
                        try:
                            self.toggle_entry_colors(1, employee_code_entry)
                            current_date_str = str(datetime.now().date())
                            reservation = Reservation.query.filter_by(id=int(df.at[x, 'id'])).first()
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'vehicle_id']).lower())).first()
                            client = Client.query.filter(Client.id_number.ilike(str(df.at[x, 'id_passport_number']).lower())).first()

                            reservation.reservation_state = "Completed"
                            reservation.date_cancel_reservation = "Not Applicable"
                            reservation.code_cancel_reservation = "Not Applicable"
                            reservation.code_confirm_completed_renting = str(employee_code_entry.get())
                            reservation.date_confirm_completed_renting = current_date_str

                            db.session.commit()

                            client_reservations = Reservation.query.filter_by(id_passport_number=client.id_number, reservation_state="In progress").all()
                            if len(client_reservations) > 0:
                                client.renting = "Yes"
                            else:
                                client.renting = "No"
                                client.code_renting = str(employee_code_entry.get()) 

                            vehicle.rented = "No"
                            vehicle.code_rented = str(employee_code_entry.get()) 
                            inspection_date = datetime.strptime(vehicle.next_inspection, "%Y-%m-%d").date()
                            legalization_date = datetime.strptime(vehicle.next_legalization, "%Y-%m-%d").date()
                            current_date = datetime.now().date()

                            if vehicle.for_inspection == "Yes" or vehicle.for_legalization == "Yes" or legalization_date <= current_date or inspection_date <= current_date:
                                vehicle.availability = "Unavailable"
                            else:
                                vehicle.availability = "Available"
                                                    

                            db.session.commit()

                            df.at[x, 'reservation_state'] = "Completed"
                            df.at[x, 'code_cancel_reservation'] = "Not Applicable"
                            df.at[x, 'date_cancel_reservation'] = "Not Applicable"
                            df.at[x, 'code_confirm_completed_renting'] = str(employee_code_entry.get())
                            df.at[x, 'date_confirm_completed_renting'] = current_date
                            refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")

            # Function that allows canceling the selected reservation
            def cancel_reservation():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    result = self.check_employee_code(str(employee_code_entry.get()), True)
                    if result == "valid":
                        try:
                            self.toggle_entry_colors(1, employee_code_entry)
                            current_date_str = str(datetime.now().date())
                            reservation = Reservation.query.filter_by(id=int(df.at[x, 'id'])).first()
                            vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(str(df.at[x, 'vehicle_id']).lower())).first()
                            client = Client.query.filter(Client.id_number.ilike(str(df.at[x, 'id_passport_number']).lower())).first()

                            reservation.reservation_state = "Cancelled"
                            reservation.date_confirm_completed_renting = "Not Applicable"
                            reservation.code_confirm_completed_renting = "Not Applicable"
                            reservation.code_cancel_reservation = str(employee_code_entry.get())
                            reservation.date_cancel_reservation = current_date_str

                            db.session.commit()

                            client_reservations = Reservation.query.filter_by(id_passport_number=client.id_number, reservation_state="In progress").all()
                            if len(client_reservations) > 0:
                                client.renting = "Yes"
                            else:
                                client.renting = "No"
                                client.code_renting = str(employee_code_entry.get()) 

                            inspection_date = datetime.strptime(vehicle.next_inspection, "%Y-%m-%d").date()
                            legalization_date = datetime.strptime(vehicle.next_legalization, "%Y-%m-%d").date()
                            current_date = datetime.now().date()

                            vehicle.rented = "No"
                            vehicle.code_rented = str(employee_code_entry.get())  

                            if vehicle.for_inspection == "Yes" or vehicle.for_legalization == "Yes" or legalization_date <= current_date or inspection_date <= current_date:
                                vehicle.availability = "Unavailable"
                            else:
                                vehicle.availability = "Available"
                                                 

                            db.session.commit()

                            df.at[x, 'reservation_state'] = "Cancelled"
                            df.at[x, 'code_confirm_completed_renting'] = "Not Applicable"
                            df.at[x, 'date_confirm_completed_renting'] = "Not Applicable"
                            df.at[x, 'code_cancel_reservation'] = str(employee_code_entry.get())
                            df.at[x, 'date_cancel_reservation'] = current_date
                            refresh_tree(df)
                        except OperationalError as e:
                            warning = "Database is locked. Please close the Database and try again."
                            self.pop_warning(new_window, warning, "databaselocked")
                            db.session.rollback()
                            print("Database is locked. Please try again later.")
                    else:
                        self.toggle_entry_colors(0, employee_code_entry)
                        self.pop_warning(new_window, result, "wrongemployeecode")
                                    
            def verify_data():
                for index, row in df.iterrows():
                    not_num = []
                    must_be_number = {
                        'Rental Duration': row['rental_duration'],
                        'Cost Per Day': row['cost_per_day'],
                        'Total Cost': row['total_cost'],
                        'Phone Number': row['phone_number'],
                        'Emergency Contact Number': row['emergency_contact_number']

                    }
                    for column_num, value_num in must_be_number.items():
                        try:
                            int(value_num)
                        except ValueError:
                            not_num.append(value_num)

                    not_alpha = []
                    must_not_have_number = {
                        'Full Name': str(row['full_name']),
                        'Emergency Contact Name': str(row['emergency_contact_name']),
                        'Nationality': str(row['nationality']),
                        'Payment-Method': str(row['payment_method'])
                    }

                    for column_word, value_word in must_not_have_number.items():
                        clean_value_word = re.sub(r'[^\w\s]', '', value_word).replace(' ','')
                        if all(char.isalpha() for char in clean_value_word):
                            pass
                        else:
                            not_alpha.append(value_word)

                    is_empty = []
                    all_data = {
                        'Rental Duration': row['rental_duration'],
                        'Cost Per Day': row['cost_per_day'],
                        'Total Cost': row['total_cost'],
                        'Phone Number': row['phone_number'],
                        'Emergency Contact Number': row['emergency_contact_number'],
                        'Full Name': str(row['full_name']),
                        'Emergency Contact Name': str(row['emergency_contact_name']),
                        'Nationality': str(row['nationality']),
                        'Payment-Method': str(row['payment_method']),
                        'Pick-up Date': str(row['pick_up_date']),
                        'Drop-off Date': str(row['drop_off_date']),
                        'Vehicle ID': str(row['vehicle_id']),
                        'Email': str(row['email']),
                        'Date of Birth': str(row['date_of_birth']),
                        'Billing Address': str(row['billing_address']),
                        'ID/Passport Number': str(row['id_passport_number'])

                    }
                    for column_all, value_all in all_data.items():
                        if value_all == 'nan':
                            is_empty.append(value_all)
                        else:
                            pass

                    not_defined = []
                    must_be_defined = {
                        'Payment-Method': (str(row['payment_method']), pay_types)
                    }
                    for column_defined, value_defined in must_be_defined.items():
                        if value_defined[0].lower() not in [val.lower() for val in value_defined[1]] or value_defined[0].lower() == 'not defined':
                            not_defined.append(value_defined)
                        else:
                            pass

                    errors_found = not_num, not_alpha, is_empty, not_defined

                    possible_photo_path_list = str(row['photos'])

                    self.verify_photo_path(possible_photo_path_list)
                    if len(valid_photo_paths) > 0 or len(valid_photo_type) > 0:
                        pass
                    if len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        is_empty.append("Photos")

                    date_pick_check = str(row['pick_up_date'])
                    date_drop_check = str(row['drop_off_date'])

                    dates_to_check = [date_pick_check, date_drop_check]
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    existing_client = None
                    existing_vehicle = None

                    cleaned_id_number = re.sub(r'[^\w\s]', '', str(row['id_passport_number']).lower())
                    existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                    cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(row['vehicle_id']).lower())
                    existing_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()                                
                    

                    if any(len(error_list) > 0 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or existing_client == None or existing_vehicle == None: 
                        result_of_validation = "Error Found"
                        self.change_row_color(treeview, index, "darkred")
                    else:
                        self.change_row_color(treeview, index, "#313131")
                        result_of_validation = "No Error Found"

                    drop_date = datetime.strptime(str(row['drop_off_date']), "%Y-%m-%d")
                    
                    current_date = datetime.now()

                    days_left = (drop_date - current_date).days
                    days_left += 1

                    if str(row['reservation_state']) ==  "Completed":
                        self.change_row_color(treeview, index, "black")
                    elif str(row['reservation_state']) ==  "Cancelled":
                        self.change_row_color(treeview, index, "#A9A9A9")
                    elif str(row['reservation_state']) == "In progress":
                        if days_left <= 3:
                            if days_left <= 0:
                                self.change_row_color(treeview, index, "darkred")
                            else:
                                self.change_row_color(treeview, index, "#C56C00")
                        else:
                            self.change_row_color(treeview, index, "#313131")

            def refresh_tree(df):
                      
                treeview.delete(*treeview.get_children())

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                df['pick_up_date'] = df['pick_up_date'].apply(convert_to_datetime)
                df['drop_off_date'] = df['drop_off_date'].apply(convert_to_datetime)
                df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)
                df['date_confirm_completed_renting'] = df['date_confirm_completed_renting'].apply(convert_to_datetime)

                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")


                columns_to_int = ['rental_duration', 'cost_per_day', 'total_cost', 'vehicle_id', 'id_passport_number', 'phone_number', 'emergency_contact_number']
                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass              
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0  
                    
                    column_width = max(heading_width, max_width) + 20 
                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.column("photos", width=120, minwidth=120)
                treeview.update_idletasks()

                verify_data()

            def clear_entries():

                entries = [id_num_entry, vehicle_id_entry, employee_code_entry]
                for entry in entries:
                    entry.delete(0, END)
                    self.toggle_entry_colors(1, entry)

                read_only_entries = [pick_entry, drop_entry, rent_duration_entry, cost_day_entry, cost_total_entry, 
                full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                for entry in read_only_entries:
                    entry.config(state=tk.NORMAL)
                    entry.delete(0, tk.END)
                    entry.config(state="readonly", readonlybackground="#313131")

                combos = [[pay_type_combobox, pay_types]]
                for combo in combos:
                    self.toggle_combo_text(1, combo[0])
                    combo[0].set(combo[1][0])

                if hasattr(self, 'photo_paths'):
                    del self.photo_paths
                see_photos_button.configure(state=tk.DISABLED)
                reload_show_photos_button.configure(image=self.update_photos_button_image)

            def select_record(e):
                clear_entries()
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    self.toggle_entry_colors(1, employee_code_entry)
                    self.toggle_button_colors(1, select_photos_button)
                    self.bind_hover_effects(select_photos_button)

                    export_selected_button.configure(state=NORMAL)
                    check_vehicle_button.configure(state=NORMAL)
                    check_client_button.configure(state=NORMAL)

                    drop_date = datetime.strptime(str(df.at[x, 'drop_off_date']), "%Y-%m-%d").date()
                    current_date = datetime.now().date()

                    if str(df.at[x, 'reservation_state']) == "In progress":
                        cancel_reservation_button.configure(state=NORMAL)
                        if drop_date <= current_date:
                            confirm_completed_button.configure(state=NORMAL)
                        else:
                            confirm_completed_button.configure(state=DISABLED)
                    else:
                        cancel_reservation_button.configure(state=DISABLED)
                        confirm_completed_button.configure(state=DISABLED)

                    cleaned_id_number = re.sub(r'[^\w\s]', '', str(df.at[x, 'id_passport_number']).lower())
                    existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                    cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(df.at[x, 'vehicle_id']).lower())
                    existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                    must_exist = [[existing_client, "client"], [existing_cleaned_vehicle, "vehicle"]]
                    none_foundlist = []
                    for must in must_exist:
                        if must[0] == None:
                            none_foundlist.append(must[1])

                    type_pay = str(df.at[x, "payment_method"]).lower()

                    pay_type_combobox.set(pay_types[0]) 
                    mapping = {p.lower(): pay_types[i] for i, p in enumerate(pay_types)}
                    pay_type_combobox.set(mapping.get(type_pay, mapping["not defined"]))

                    if pay_type_combobox.get() == 'Not Defined':
                        self.toggle_combo_text(0, pay_type_combobox)
                    else:
                        self.toggle_combo_text(1, pay_type_combobox)

                    read_only_entries = [pick_entry, drop_entry, rent_duration_entry, 
                    cost_day_entry, cost_total_entry, full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                    client_read_only_entries = [full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                    for entry in read_only_entries:
                        entry.config(state=tk.NORMAL)

                    if "client" in none_foundlist:
                        self.toggle_entry_colors(0, id_num_entry)
                        id_num_entry.insert(0, "Not found")
                        for entry in client_read_only_entries:
                            entry.insert(0, "Not found")
                            entry.config(readonlybackground="darkred")
                            
                    elif "client" not in none_foundlist:
                        self.toggle_entry_colors(1, id_num_entry)
                        for entry in client_read_only_entries:
                            entry.config(readonlybackground="#313131")
                        full_name_entry.insert(0, str(df.at[x, 'full_name']))
                        phone_entry.insert(0, str(df.at[x, 'phone_number']))
                        email_entry.insert(0, str(df.at[x, 'email']))
                        dob_entry.insert(0, str(df.at[x, 'date_of_birth']))
                        em_name_entry.insert(0, str(df.at[x, 'emergency_contact_name']))
                        em_num_entry.insert(0, str(df.at[x, 'emergency_contact_number']))
                        bill_address_entry.insert(0, str(df.at[x, 'billing_address']))
                        id_num_entry.insert(0, str(df.at[x, 'id_passport_number']))
                        nationality_entry.insert(0, str(df.at[x, 'nationality']))

                    if "vehicle" in none_foundlist:
                        vehicle_id_entry.insert(0, "Not found")
                        self.toggle_entry_colors(0, vehicle_id_entry)
                    else:
                        vehicle_id_entry.insert(0, str(existing_cleaned_vehicle.license_plate))
                        self.toggle_entry_colors(1, vehicle_id_entry)

                    date_pick_check = str(df.at[x, 'pick_up_date'])
                    date_drop_check = str(df.at[x, 'drop_off_date'])

                    dates_to_check = [[date_pick_check, pick_entry], [date_drop_check, drop_entry]]
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"                                
                    inval_date = []
                    for date in dates_to_check:
                        if bool(re.match(pattern, date[0])) == False:
                            date[1].insert(0, str(date[0]))
                            date[1].config(readonlybackground="darkred")
                            inval_date.append(date)
                        else:
                            date[1].insert(0, str(date[0]))
                            date[1].config(readonlybackground="#313131")

                    if len(inval_date) > 0:
                        rent_duration_entry.insert(0, "Failed")
                        rent_duration_entry.config(readonlybackground="darkred")
                        cost_day_entry.insert(0, "Failed")
                        cost_day_entry.config(readonlybackground="darkred")
                        cost_total_entry.insert(0, "Failed")
                        cost_total_entry.config(readonlybackground="darkred")
                    else:
                        date_format = "%Y-%m-%d"
                        date_pick = datetime.strptime(date_pick_check, date_format)
                        date_drop = datetime.strptime(date_drop_check, date_format)

                        rent_duration_entry.config(readonlybackground="#313131")
                        cost_day_entry.config(readonlybackground="#313131")
                        cost_total_entry.config(readonlybackground="#313131")

                        difference = date_drop - date_pick
                        difference = difference.days + 1
                        rent_duration_entry.insert(0, difference)

                        try:
                            if existing_cleaned_vehicle.category.lower() == 'gold':
                                cost_day_entry.insert(0, 120)
                                total = int(difference) * 120
                                cost_total_entry.insert(0, int(total))
                            elif existing_cleaned_vehicle.category.lower() == 'silver':
                                cost_day_entry.insert(0, 80)
                                total = int(difference) * 80
                                cost_total_entry.insert(0, int(total))
                            elif existing_cleaned_vehicle.category.lower() == 'economic':
                                cost_day_entry.insert(0, 40)
                                total = int(difference) * 40
                                cost_total_entry.insert(0, int(total))
                        except AttributeError:
                            pass

                    for entry in read_only_entries:
                        entry.config(state="readonly")

                    self.verify_photo_path(str(df.at[x, "photos"]))
                    if str(df.at[x, "photos"]).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        self.toggle_button_colors(0, selected_receipt_photos_button)
                        self.red_bind_hover_effects(selected_receipt_photos_button)
                    else:
                        self.toggle_button_colors(1, selected_receipt_photos_button)
                        self.bind_hover_effects(selected_receipt_photos_button)
                        print(df.at[x, "photos"])
                else:
                    pass

            def update_record():
                must_be_number = {
                    }

                must_not_have_number = {}

                must_be_defined = {
                        'Payment-Method' : (selected_pay_type.get(), pay_type_combobox)
                }

                must_not_be_empty = {
                        'Vehicle ID': (vehicle_id_entry.get(), vehicle_id_entry),
                        'ID/Passport Number': (id_num_entry.get(), id_num_entry)
                    }

                self.validate_data("entries", must_be_number, must_not_have_number, must_be_defined, must_not_be_empty)

                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    self.verify_photo_path(str(df.at[x, 'photos']))

                    if str(df.at[x, 'photos']).lower() == "nan" or len(invalid_photo_paths) > 0 or len(invalid_photo_type) > 0:
                        if hasattr(self, 'photo_paths'):
                            pass
                        else:
                            is_empty.append("Photos")

                    date_pick_check = str(pick_entry.get())
                    date_drop_check = str(drop_entry.get())

                    dates_to_check = [date_pick_check, date_drop_check]
                    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

                    cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                    existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                    cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                    existing_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                    must_exist = [[existing_client, "client"], [existing_vehicle, "vehicle"]]
                    none_foundlist = []
                    for must in must_exist:
                        if must[0] == None:
                            none_foundlist.append(must[1]) 

                    if any(len(error_list) > 1 for error_list in errors_found) or any(bool(re.match(pattern, date)) == False for date in dates_to_check) or len(none_foundlist) > 0: 
                        result_of_validation = "Error Found"
                    else:
                        result_of_validation = "No Error Found"

                    if result_of_validation == "No Error Found":
                        result = self.check_employee_code(str(employee_code_entry.get()), False)
                        if result == "valid":
                            date_next_inspection = datetime.strptime(existing_vehicle.next_inspection, "%Y-%m-%d")
                            date_next_legalization = datetime.strptime(existing_vehicle.next_legalization, "%Y-%m-%d")
                            drop = datetime.strptime(drop_entry.get(), "%Y-%m-%d")

                            if drop >= date_next_inspection or drop >= date_next_legalization:
                                warning = "Drop-off date exceeds the inspection or legalization date"
                                self.pop_warning(new_window, warning, "dropdateexceeds")
                            else:
                                vehicle_cc = existing_vehicle.cc
                                client_motorcycle_license = existing_client.m_license
                                vehicle_type = existing_vehicle.vehicle_type

                                not_valid = False

                                if client_motorcycle_license == "A1(125cc|11kw|0.1kw/kg)":
                                    cc_list_class = ["<= 50 (11kw)", "51 - 125 (11kw)"]
                                    if vehicle_cc not in cc_list_class:
                                        not_valid = True
                                elif client_motorcycle_license == "A2(max-35kw|0.2kw/kg)":
                                    cc_list_class = ["<= 50 (35kw)", "51 - 125 (35kw)", "126 - 500 (35kw)", "501 - 1000 (35kw)", ">= 1000 (35kw)"]
                                    if vehicle_cc not in cc_list_class:
                                        not_valid = True
                                elif client_motorcycle_license == "Not Applicable":
                                    if vehicle_type.lower() == "motorcycles":
                                        not_valid = True
                                if not_valid == True:
                                    client_license = f"Client license class: {client_motorcycle_license}"
                                    self.pop_warning(new_window, client_license, "ccnotvalidlicense")
                                else:
                                    self.toggle_entry_colors(1, employee_code_entry)

                                    reservation  = Reservation.query.filter_by(id=int(df.at[x, 'id'])).first()

                                    if reservation.reservation_state == "In progress":
                                        warning = "The selected record can't be updated now due to the reservation being currently in progress"
                                        self.pop_warning(new_window, warning, "cantupdateinprogress")
                                    else:
                                        try:
                                            date_update = str(datetime.now(timezone.utc).date())

                                            def update_payment_record():
                                                pay_record = Payment.query.filter_by(id=reservation.id).first()
                                                pay_record.total_pay = cost_total_entry.get()
                                                pay_record.payment_method = str(selected_pay_type.get())
                                                pay_record.f_name = full_name_entry.get()
                                                pay_record.p_number = str(phone_entry.get())
                                                pay_record.id_number = cleaned_id_number
                                                pay_record.bill_address = bill_address_entry.get()
                                                pay_record.vehicle_id = cleaned_vehicle_plate_id_num
                                                pay_record.code_last_update = str(employee_code_entry.get())
                                                pay_record.last_update = str(date_update)

                                                if hasattr(self, 'photo_paths'):
                                                    pay_record.photos = self.photo_paths
                                                else:
                                                    pass

                                                db.session.commit()

                                            reservation.pick_up_date = str(pick_entry.get())
                                            reservation.drop_off_date = str(drop_entry.get())
                                            reservation.vehicle_id = cleaned_vehicle_plate_id_num
                                            reservation.rental_duration = rent_duration_entry.get()
                                            reservation.cost_per_day = cost_day_entry.get()
                                            reservation.total_cost = cost_total_entry.get()
                                            reservation.full_name = full_name_entry.get()
                                            reservation.phone_number = str(phone_entry.get())
                                            reservation.email = str(email_entry.get())
                                            reservation.id_passport_number = cleaned_id_number
                                            reservation.date_of_birth = dob_entry.get()
                                            reservation.nationality = nationality_entry.get()
                                            reservation.emergency_contact_name = em_name_entry.get()
                                            reservation.emergency_contact_number = str(em_num_entry.get())
                                            reservation.billing_address = bill_address_entry.get()
                                            reservation.payment_method = str(selected_pay_type.get())
                                            reservation.code_last_update = str(employee_code_entry.get())
                                            reservation.last_update = str(date_update)

                                            if hasattr(self, 'photo_paths'):
                                                reservation.photos = self.photo_paths
                                            else:
                                                pass

                                            db.session.commit()
                                            self.toggle_button_colors(1, selected_receipt_photos_button)

                                            df.at[x, "pick_up_date"] = pick_entry.get()
                                            df.at[x, "drop_off_date"] = drop_entry.get()
                                            df.at[x, "vehicle_id"] = cleaned_vehicle_plate_id_num
                                            df.at[x, "rental_duration"] = rent_duration_entry.get()
                                            df.at[x, "cost_per_day"] = cost_day_entry.get()
                                            df.at[x, "total_cost"] = cost_total_entry.get()
                                            df.at[x, "full_name"] = full_name_entry.get()
                                            df.at[x, "phone_number"] = str(phone_entry.get())
                                            df.at[x, "email"] = str(email_entry.get())
                                            df.at[x, "id_passport_number"] = cleaned_id_number
                                            df.at[x, "date_of_birth"] = dob_entry.get()
                                            df.at[x, "nationality"] = nationality_entry.get()
                                            df.at[x, "emergency_contact_name"] = em_name_entry.get()
                                            df.at[x, "emergency_contact_number"] = str(em_num_entry.get())
                                            df.at[x, "billing_address"] = bill_address_entry.get()
                                            df.at[x, "payment_method"] = str(selected_pay_type.get())
                                            df.at[x, "code_last_update"] = str(employee_code_entry.get())
                                            df.at[x, "last_update"] = str(date_update)

                                            if hasattr(self, 'photo_paths'):
                                                df.at[x, 'photos'] = self.photo_paths
                                            else:
                                                pass

                                            update_payment_record()
                                            clear_entries()
                                            refresh_tree(df)
                                        except OperationalError as e:
                                            warning = "Database is locked. Please close the Database and try again."
                                            self.pop_warning(new_window, warning, "databaselocked")
                                            db.session.rollback()
                                            print("Database is locked. Please try again later.")
                        else:
                            self.toggle_entry_colors(0, employee_code_entry)
                            self.pop_warning(new_window, result, "wrongemployeecode")
                    else:
                        if len(none_foundlist) > 0:
                            self.pop_warning(new_window, none_foundlist, "clientorvehiclenotindb")  

                        wrong_date_format = []
                        for date in dates_to_check:
                            if bool(re.match(pattern, date)) == False:
                                wrong_date_format.append(date)
                                self.pop_warning(new_window, wrong_date_format, "wrongdatetextformat")

                        for key in must_not_be_empty:
                            if key in is_empty:
                                entry_value = must_not_be_empty[key][1]
                                self.toggle_entry_colors_ifnan(0, must_not_be_empty[key][1])
                            else:
                                self.toggle_entry_colors_ifnan(1, must_not_be_empty[key][1])

                        for key in must_be_defined:
                            if key in not_defined:
                                combobox_value = must_be_defined[key][1]
                                self.toggle_combo_text(0, must_be_defined[key][1])
                            else:
                                self.toggle_combo_text(1, must_be_defined[key][1])

                        for key in must_not_have_number:
                            if key in not_alpha or key in is_empty:
                                entry_value = must_not_have_number[key][1]
                                self.toggle_entry_colors(0, must_not_have_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_not_have_number[key][1])

                        if "Photos" in is_empty:
                            self.toggle_button_colors(0, select_photos_button)
                            self.red_bind_hover_effects(select_photos_button)
                        else:
                            self.toggle_button_colors(1, select_photos_button)
                            self.bind_hover_effects(select_photos_button)

                        for key in must_be_number:
                            if key in not_num or key in is_empty:
                                entry_value = must_be_number[key][1]
                                self.toggle_entry_colors(0, must_be_number[key][1])
                            else:
                                self.toggle_entry_colors(1, must_be_number[key][1])

                        errors_adding = []
                        for error_list in errors_found:
                            if len(error_list) > 1:
                                errors_adding.append(error_list)
                        if len(errors_adding) > 0:
                            self.pop_warning(new_window, errors_adding, "addrecvalidation")
                else:
                    warning = "Must select an item to Update"
                    self.pop_warning(new_window, warning, "noselectedtoupdate" )

            def remove_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    try:
                        if len(selected_items) == Reservation.query.count():
                            warning = "Can not delete all the data from the Reservations Database"
                            self.pop_warning(new_window, warning, "cannotdeletealldb" )
                        else:
                            code_check=self.check_employee_code(str(employee_code_entry.get()), True)
                            if code_check == "valid":
                                self.toggle_entry_colors(1, employee_code_entry)
                                can_not_delete = []
                                for record in selected_items:
                                    x = treeview.index(record)
                                    reservation = Reservation.query.filter_by(id=int(df.at[x, 'id'])).first()
                                    if reservation.reservation_state == "In progress":
                                        can_not_delete.append(reservation.id)
                                    else:
                                        pay_record = Payment.query.filter_by(id=reservation.id).first()
                                        db.session.delete(reservation)
                                        db.session.delete(pay_record)
                                        db.session.commit()     
                                        treeview.delete(record)
                                        df.drop(index=x, inplace=True)
                                        df.reset_index(drop=True, inplace=True)
                                verify_data()
                                clear_entries()
                                if len(can_not_delete) > 0:
                                    self.pop_warning(new_window, can_not_delete, "cannotdeletereservation")
                            else:
                                self.toggle_entry_colors(0, employee_code_entry)
                                self.pop_warning(new_window, code_check, "wrongemployeecode")
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    warning = "Must select at least one record to remove"
                    self.pop_warning(new_window, warning, "noselectedtoremove")

            def selected_receipt_photos():
                selected_items = treeview.selection()
                print(selected_items)
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    photos_of_selected = str(df.at[x, "photos"])

                    if photos_of_selected.lower() != "nan":
                        self.verify_photo_path(photos_of_selected)

                        if len(valid_photo_type) > 0:
                            print(valid_photo_type)
                            if len(valid_photo_paths) > 0:
                                def handle_photo_viewer_result(result, updated_photos):
                                    if result == "confirm":
                                        try:
                                            reservation = Reservation.query.filter_by(id=int(df.at[x, 'id'])).first()
                                            reservation.photos = updated_photos
                                            pay_record = Payment.query.filter_by(id=reservation.id).first()
                                            pay_record.photos = updated_photos
                                            db.session.commit() 
                                            df.at[x, 'photos'] = updated_photos
                                        except OperationalError as e:
                                            warning = "Database is locked. Please close the Database and try again."
                                            self.pop_warning(new_window, warning, "databaselocked")
                                            db.session.rollback()
                                            print("Database is locked. Please try again later.")
                                    elif result == "cancel":
                                        print("User cancelled changes")

                                if str(df.at[x, "reservation_state"]) == "In progress":
                                    mode = "View Mode"
                                else:
                                    mode = "Edit Mode"

                                updated_photos = []
                                self.photo_viewer(new_window, valid_photo_paths, mode, handle_photo_viewer_result, updated_photos)
                            if len(invalid_photo_paths) > 0:
                                self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                        for path in invalid_photo_type:
                            if path == "":
                                invalid_photo_type.remove(path)
                        if len(invalid_photo_type) > 0:
                            self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                            self.toggle_button_colors(0, selected_receipt_photos_button)
                    else:
                        x += 1
                        self.pop_warning(new_window, str(x), "nanselectedphoto")
                        self.toggle_button_colors(0, selected_receipt_photos_button)
                else:
                    warning = "Must select a record to see photos"
                    self.pop_warning(new_window, warning, "noselectedtoseephotos")

            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            update_button = Button(edit_treeview_frame, text="Update Record", fg="white", bg="black",
                                   command=update_record)
            update_button.grid(row=0, column=0, padx=5, pady=3)
            self.bind_hover_effects(update_button)

            clear_entries_button = Button(edit_treeview_frame, text="Clear Entries", fg="white", bg="black",
                                          command=clear_entries)
            clear_entries_button.grid(row=0, column=1, padx=5, pady=3)
            self.bind_hover_effects(clear_entries_button)

            selected_receipt_photos_button = Button(edit_treeview_frame, text="See Selected Receipt Photos",
                                                    fg="white",
                                                    bg="black", command=selected_receipt_photos)
            selected_receipt_photos_button.grid(row=0, column=2, padx=5, pady=3)
            self.bind_hover_effects(selected_receipt_photos_button)

            remove_selected_button = Button(edit_treeview_frame, text="Remove Selected Record(s)", fg="white",
                                            bg="black", command=remove_selected)
            remove_selected_button.grid(row=0, column=3, padx=5, pady=3)
            self.bind_hover_effects(remove_selected_button)

            refresh_tree_button = Button(edit_treeview_frame, text="Refresh Tree", fg="white",
                                       bg="black", command=lambda: refresh_tree(df))
            refresh_tree_button.grid(row=0, column=4, padx=5, pady=3)
            self.bind_hover_effects(refresh_tree_button)

            employee_code_label = tk.Label(edit_treeview_frame, text="Employee Code:",
                              font=("Helvetica", 10), fg="white", bg="black")
            employee_code_label.grid(row=0, column=5, pady=5, padx=(20, 5), sticky=tk.E)

            employee_code_entry = tk.Entry(edit_treeview_frame, bd=2, width=10)
            employee_code_entry.grid(row=0, column=6, padx=5, pady=3)

            treeview.bind("<ButtonRelease-1>", select_record)

            check_client_button.config(command=check_client_info)
            check_vehicle_button.config(command=check_vehicle_info)
            confirm_completed_button.config(command=confirm_completed_renting)
            cancel_reservation_button.config(command=cancel_reservation)
            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)

            # Below is the code responsible to search the databse for all the reservations in each one of the three possible states (In progress/Completed/Cancelled)
            cancelled_reservations = Reservation.query.filter_by(reservation_state="Cancelled").all()
            if len(cancelled_reservations) > 0:
                see_cancelled_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "Cancelled"], "showdbiteminfo") , state=NORMAL)

            completed_reservations = Reservation.query.filter_by(reservation_state="Completed").all()
            if len(completed_reservations) > 0:
                see_completed_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "Completed"], "showdbiteminfo") , state=NORMAL)

            in_progress_reservations = Reservation.query.filter_by(reservation_state="In progress").all()
            if len(in_progress_reservations) > 0:
                see_in_progress_button.config(command=lambda: self.pop_warning(new_window, ["showcancelcompletedinprogress", "In progress"], "showdbiteminfo") , state=NORMAL)

        def check_if_photos():
            if hasattr(self, 'photo_paths'):
                see_photos_button.configure(state=tk.NORMAL)
                self.check_image_path = resource_path('resources/check.png')
                self.check_photos_image = ImageTk.PhotoImage(Image.open(self.check_image_path))
                reload_show_photos_button.configure(image=self.check_photos_image)
            else:
                see_photos_button.configure(state=tk.DISABLED)
                self.update_photos_button_image_path = resource_path('resources/update.png')
                self.update_photos_button_image = ImageTk.PhotoImage(Image.open(self.update_photos_button_image_path))
                reload_show_photos_button.configure(image=self.update_photos_button_image)

        edit_reservation_frame = tk.Frame(new_window)
        edit_reservation_frame.configure(bg="black")
        edit_reservation_frame.pack(pady=(0,10))

        def costs_of_rent(*args):
            try:
                cleaned_vehicle_plate_id_num = re.sub(r'[^\w\s]', '', str(vehicle_id_entry.get()).lower())
                existing_cleaned_vehicle = Vehicle.query.filter(Vehicle.license_plate.ilike(cleaned_vehicle_plate_id_num)).first()

                if existing_cleaned_vehicle:
                    vehicle_id_entry.config(bg="#313131")
                    cost_entries = [rent_duration_entry, cost_day_entry, cost_total_entry]

                    for entry in cost_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)

                    date_pick_check = pick_entry.get()
                    date_drop_check = drop_entry.get()

                    date_format = "%Y-%m-%d"
                    date_pick = datetime.strptime(date_pick_check, date_format)
                    date_drop = datetime.strptime(date_drop_check, date_format)

                    rent_duration_entry.config(readonlybackground="#313131")
                    cost_day_entry.config(readonlybackground="#313131")
                    cost_total_entry.config(readonlybackground="#313131")

                    difference = date_drop - date_pick

                    difference = int(difference.days) + 1
                    rent_duration_entry.insert(0, difference)
                    
                    if existing_cleaned_vehicle.category.lower() == 'gold':
                        cost_day_entry.insert(0, 120)
                        total = int(difference) * 120
                        cost_total_entry.insert(0, int(total))
                    elif existing_cleaned_vehicle.category.lower() == 'silver':
                        cost_day_entry.insert(0, 80)
                        total = int(difference) * 80
                        cost_total_entry.insert(0, int(total))
                    elif existing_cleaned_vehicle.category.lower() == 'economic':
                        cost_day_entry.insert(0, 40)
                        total = int(difference) * 40
                        cost_total_entry.insert(0, int(total))

                    for entry in cost_entries:
                        entry.config(state="readonly")
                else:
                    vehicle_id_entry.config(bg="darkred")
            except ValueError:
                pass

        def client_info(*args):
            try:
                cleaned_id_number = re.sub(r'[^\w\s]', '', str(id_num_entry.get()).lower())
                existing_client = Client.query.filter(Client.id_number.ilike(cleaned_id_number)).first() 

                if existing_client:
                    id_num_entry.config(bg="#313131")
                    client_entries = [full_name_entry, phone_entry, email_entry, dob_entry, em_name_entry, em_num_entry, bill_address_entry, nationality_entry]

                    for entry in client_entries:
                        entry.config(state=tk.NORMAL)
                        entry.delete(0, tk.END)

                    full_name_entry.insert(0, str(existing_client.f_name))
                    phone_entry.insert(0, int(existing_client.p_number))
                    email_entry.insert(0, str(existing_client.email))
                    dob_entry.insert(0, str(existing_client.dob))
                    em_name_entry.insert(0, str(existing_client.em_name))
                    em_num_entry.insert(0, int(existing_client.em_number))
                    bill_address_entry.insert(0, str(existing_client.bill_address))
                    nationality_entry.insert(0, str(existing_client.nationality))

                    for entry in client_entries:
                        entry.config(state="readonly")
                else:
                    id_num_entry.config(bg="darkred")
            except ValueError:
                pass

        select_photos_button = tk.Button(edit_reservation_frame, text="Select Receipt Photos", width=16, borderwidth=2,
                                         fg="white", bg="black", command=lambda: self.load_image(new_window))
        select_photos_button.grid(row=0, column=4, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(select_photos_button)

        def handle_photo_viewer_result(result, updated_photos):
            if result == "confirm":
                self.photo_paths = updated_photos
                if self. photo_paths == 'nan':
                    del self.photo_paths
                    check_if_photos()
            elif result == "cancel":
                print("User cancelled changes")

        updated_photos = []
        see_photos_button = tk.Button(edit_reservation_frame, text="See Receipt Photos", width=15, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED,
                                      command=lambda: self.photo_viewer(new_window, self.photo_paths, "Edit Mode", handle_photo_viewer_result, updated_photos))
        see_photos_button.grid(row=0, column=5, pady=5, padx=5, sticky="e")
        self.bind_hover_effects(see_photos_button)

        update_photos_button_image_path = resource_path('resources/update.png')
        self.update_photos_button_image = ImageTk.PhotoImage(Image.open(update_photos_button_image_path))
        reload_show_photos_button = tk.Button(edit_reservation_frame, image=self.update_photos_button_image,
                                              command=check_if_photos, borderwidth=0, highlightthickness=0)
        reload_show_photos_button.grid(row=0, column=6, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(reload_show_photos_button)

        select_vehicle_button = tk.Button(edit_reservation_frame, text="Select Vehicle", width=20, borderwidth=2,
                                              fg="white", bg="black")

        select_vehicle_button.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_vehicle_button)

        select_client_button = tk.Button(edit_reservation_frame, text="Select Client", width=15, borderwidth=2,
                                              fg="white", bg="black")

        select_client_button.grid(row=0, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(select_client_button)

        pick_button = tk.Button(edit_reservation_frame, text="Select the Pick-up Date", width=20, borderwidth=2,
                                              fg="white", bg="black", command=lambda: self.datepicker(new_window, pick_entry, "reservation", drop_button))

        pick_button.grid(row=1, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(pick_button)
        pick_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        pick_entry.grid(row=1, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        pick_entry.bind("<KeyRelease>", costs_of_rent)

        drop_button = tk.Button(edit_reservation_frame, text="Select the Drop-off Date", width=20, borderwidth=2,
                                              fg="white", bg="black", state=DISABLED, command=lambda: self.datepicker(new_window, drop_entry, "reservation", drop_button, pick_entry.get(), costs_of_rent))
        drop_button.grid(row=2, column=0, pady=5, padx=(10, 5), sticky=tk.E)
        self.bind_hover_effects(drop_button)
        drop_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        drop_entry.grid(row=2, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        drop_entry.bind("<KeyRelease>", costs_of_rent)

        vehicle_id_label = tk.Label(edit_reservation_frame, text="Vehicle ID:",
                               font=("Helvetica", 10), fg="white", bg="black")
        vehicle_id_label.grid(row=3, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        vehicle_id_entry = tk.Entry(edit_reservation_frame, bd=2, width=10)
        vehicle_id_entry.grid(row=3, column=1, pady=5, padx=(5, 10), sticky=tk.W)
        vehicle_id_entry.bind("<KeyRelease>", costs_of_rent)

        rent_duration_label = tk.Label(edit_reservation_frame, text="Rental duration:",
                               font=("Helvetica", 10), fg="white", bg="black")
        rent_duration_label.grid(row=4, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        rent_duration_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        rent_duration_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        cost_day_label = tk.Label(edit_reservation_frame, text="Cost per day:",
                               font=("Helvetica", 10), fg="white", bg="black")
        cost_day_label.grid(row=5, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        cost_day_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        cost_day_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        cost_total_label = tk.Label(edit_reservation_frame, text="Total cost:",
                               font=("Helvetica", 10), fg="white", bg="black")
        cost_total_label.grid(row=6, column=0, pady=5, padx=(20, 5), sticky=tk.E)
        cost_total_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        cost_total_entry.grid(row=6, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        export_selected_button = tk.Button(edit_reservation_frame, text="Export Selected Data", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_selected_button.grid(row=7, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(export_selected_button)

        export_all_button = tk.Button(edit_reservation_frame, text="Export All Data", width=22, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)

        export_all_button.grid(row=8, column=0, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(export_all_button)

        see_cancelled_button = tk.Button(edit_reservation_frame, text="See Cancelled Reservations", width=22, borderwidth=2,
                                              fg="white", bg="black", state=DISABLED)

        see_cancelled_button.grid(row=6, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(see_cancelled_button)

        see_completed_button = tk.Button(edit_reservation_frame, text="See Completed Reservations", width=22, borderwidth=2,
                                              fg="white", bg="black", state=DISABLED)

        see_completed_button.grid(row=7, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(see_completed_button)

        see_in_progress_button = tk.Button(edit_reservation_frame, text="See In Progress Reservations", width=22, borderwidth=2,
                                              fg="white", bg="black", state=DISABLED)

        see_in_progress_button.grid(row=8, column=2, columnspan=2, pady=5, padx=5)
        self.bind_hover_effects(see_in_progress_button)

        full_name_label = tk.Label(edit_reservation_frame, text="Full Name:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        full_name_label.grid(row=1, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        full_name_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        full_name_entry.grid(row=1, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        phone_label = tk.Label(edit_reservation_frame, text="Phone Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        phone_label.grid(row=2, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        phone_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        phone_entry.grid(row=2, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        email_label = tk.Label(edit_reservation_frame, text="Email:",
                               font=("Helvetica", 10), fg="white", bg="black")
        email_label.grid(row=3, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        email_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        email_entry.grid(row=3, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        id_num_label = tk.Label(edit_reservation_frame, text="ID/Passport Number:",
                               font=("Helvetica", 10), fg="white", bg="black")
        id_num_label.grid(row=4, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        id_num_entry = tk.Entry(edit_reservation_frame, bd=2, width=10)
        id_num_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)
        id_num_entry.bind("<KeyRelease>", client_info)

        dob_label = tk.Label(edit_reservation_frame, text="Date of Birth:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        dob_label.grid(row=5, column=2, pady=5, padx=(20, 5), sticky=tk.E)
        dob_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        dob_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        nationality_label = tk.Label(edit_reservation_frame, text="Nationality:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        nationality_label.grid(row=1, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        nationality_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        nationality_entry.grid(row=1, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        em_name_label = tk.Label(edit_reservation_frame, text="Emergency Contact Name:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        em_name_label.grid(row=2, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        em_name_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        em_name_entry.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        em_num_label = tk.Label(edit_reservation_frame, text="Emergency Contact Number:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        em_num_label.grid(row=3, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        em_num_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        em_num_entry.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        bill_address_label = tk.Label(edit_reservation_frame, text="Billing Address:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        bill_address_label.grid(row=4, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        bill_address_entry = tk.Entry(edit_reservation_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        bill_address_entry.grid(row=4, column=5, pady=5, padx=(5, 10), sticky=tk.W)     

        pay_method_label = tk.Label(edit_reservation_frame, text="Payment-Method:",
                                 font=("Helvetica", 10), fg="white", bg="black")
        pay_method_label.grid(row=5, column=4, pady=5, padx=(10, 5), sticky=tk.E)
        pay_types = ["Not Defined", "Cash", "Credit Card", "Paypal", "Bank Transfer", "Google Pay", "Apple Pay"]
        selected_pay_type = tk.StringVar()
        pay_type_combobox = ttk.Combobox(edit_reservation_frame,
                                        textvariable=selected_pay_type,
                                        values=pay_types, state="readonly",  justify="center", height=4, width=10,
                                        style="TCombobox")
        pay_type_combobox.grid(row=5, column=5, pady=5, padx=(5, 10), sticky=tk.W)
        pay_type_combobox.set(pay_types[0]) 

        get_vehicle_table = ["vehicle", vehicle_id_entry, costs_of_rent]
        select_vehicle_button.config(command=lambda: self.pop_warning(new_window, get_vehicle_table, "dbtotree"))

        get_client_table = ["client", id_num_entry, client_info]
        select_client_button.config(command=lambda: self.pop_warning(new_window, get_client_table, "dbtotree"))

        check_vehicle_button = tk.Button(edit_reservation_frame, text="Check Vehicle Information", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_vehicle_button.grid(row=6, column=4, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_vehicle_button)

        check_client_button = tk.Button(edit_reservation_frame, text="Check Client Information", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_client_button.grid(row=6, column=5, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(check_client_button)

        cancel_reservation_button = tk.Button(edit_reservation_frame, text="Cancel Reservation", width=20, borderwidth=2,
                              fg="white", bg="black", state=DISABLED)
        cancel_reservation_button.grid(row=7, column=4, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(cancel_reservation_button)

        confirm_completed_button = tk.Button(edit_reservation_frame, text="Confirm Reservation is Completed", width=25, borderwidth=2,
                              fg="white", bg="black", state=DISABLED)
        confirm_completed_button.grid(row=7, column=5, columnspan=2, pady=5, padx=5, sticky="w")
        self.bind_hover_effects(confirm_completed_button)

        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to see paymment records data, to update a payment record data or delete a record 
    # the user must do it to the reservaiton related to the intended record (same id) in the manage reservations section
    def payments_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(pady=(140, 0))
        
        treeview_frame = tk.Frame(new_window)
        treeview_frame.pack(pady=10)
        treeview_frame.configure(bg="black")
        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("payment", con=engine)
            engine.dispose()
        except ValueError:
            print("ValueError")

        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'total_pay', 'payment_method', 'f_name', 'p_number', 'id_number', 'bill_address', 
                                                      'vehicle_id', 'photos', 'last_update', 'code_last_update', 'insertion_date', 'code_insertion'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'total_pay': df.at[x, 'total_pay'],
                            'payment_method': df.at[x, 'payment_method'],
                            'f_name': df.at[x, 'f_name'], 
                            'p_number': df.at[x, 'p_number'], 
                            'id_number': df.at[x, 'id_number'], 
                            'bill_address': df.at[x, 'bill_address'],
                            'vehicle_id': df.at[x, 'vehicle_id'], 
                            'photos': df.at[x, 'photos'], 
                            'last_update': df.at[x, 'last_update'], 
                            'code_last_update': df.at[x, 'code_last_update'],
                            'insertion_date': df.at[x, 'insertion_date'],
                            'code_insertion': df.at[x, 'code_insertion']
                        }

                        new_df_record = pd.DataFrame([new_df_record])  

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")

            # Function to see the information of the client inserted in the reservation related to this payment
            def check_client_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["reservationinfo", "client", str(df.at[x, 'id_number'])]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            # Function to see the information of the vehicle inserted in the reservation related to this payment
            def check_vehicle_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_vehicle = ["reservationinfo", "vehicle", str(df.at[x, 'vehicle_id'])]
                    self.pop_warning(new_window, get_vehicle, "showdbiteminfo")

            # Function to see the information of the reservation related to this payment
            def check_reservation_info():
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    get_reservation = ["reservationinfo", "reservation", int((df.at[x, 'id']))]
                    self.pop_warning(new_window, get_reservation, "showdbiteminfo")

            def refresh_tree(df):
                      
                treeview.delete(*treeview.get_children())

                def convert_to_datetime(date_string):
                    try:
                        return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                    except ValueError:
                        return date_string

                df['insertion_date'] = df['insertion_date'].apply(convert_to_datetime)
                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")


                columns_to_int = ['total_pay', 'vehicle_id', 'id_number', 'p_number']
                for column in columns_to_int:
                    try:
                        df[column] = df[column].fillna(0).astype('int64')
                        df[column] = df[column].replace(0, 'nan')
                    except ValueError:
                        pass              
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0 
                    
                    column_width = max(heading_width, max_width) + 20
                    
                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.column("photos", width=120, minwidth=120)
                treeview.update_idletasks()

            def select_record(e):
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    export_selected_button.configure(state=NORMAL)
                    check_vehicle_button.configure(state=NORMAL)
                    check_client_button.configure(state=NORMAL)
                    check_reservation_button.configure(state=NORMAL)
                else:
                    pass

            def selected_receipt_photos():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])
                    photos_of_selected = str(df.at[x, "photos"])

                    if photos_of_selected.lower() != "nan":
                        self.verify_photo_path(photos_of_selected)
                        if len(valid_photo_type) > 0:
                            if len(valid_photo_paths) > 0:
                                self.photo_viewer(new_window, valid_photo_paths, "View Mode")
                            if len(invalid_photo_paths) > 0:
                                self.pop_warning(new_window, invalid_photo_paths,"filenotfound")
                                self.toggle_button_colors(0, selected_receipt_photos_button)
                        print(invalid_photo_type)
                        for path in invalid_photo_type:
                            if path == "":
                                invalid_photo_type.remove(path)
                        if len(invalid_photo_type) > 0:
                            self.pop_warning(new_window, invalid_photo_type,"invalidformat")
                            self.toggle_button_colors(0, selected_receipt_photos_button)
                    else:
                        x += 1
                        self.pop_warning(new_window, str(x), "nanselectedphoto")
                        self.toggle_button_colors(0, selected_receipt_photos_button)
                else:
                    warning = "Must select a record to see photos"
                    self.pop_warning(new_window, warning, "noselectedtoseephotos")

            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            selected_receipt_photos_button = Button(treeview_frame, text="See Selected Receipt Photos",
                                                    fg="white",
                                                    bg="black", command=selected_receipt_photos)
            selected_receipt_photos_button.grid(row=0, column=0, padx=20, pady=3)
            self.bind_hover_effects(selected_receipt_photos_button)

            export_selected_button = tk.Button(treeview_frame, text="Export Selected Data", width=22, borderwidth=2,
                                          fg="white", bg="black", state=DISABLED)
            export_selected_button.grid(row=0, column=1, pady=15, padx=20)
            self.bind_hover_effects(export_selected_button)

            export_all_button = tk.Button(treeview_frame, text="Export All Data", width=22, borderwidth=2,
                                          fg="white", bg="black", state=DISABLED)
            export_all_button.grid(row=0, column=2, pady=15, padx=20)
            self.bind_hover_effects(export_selected_button)

            treeview.bind("<ButtonRelease-1>", select_record)

            check_client_button.config(command=check_client_info)
            check_vehicle_button.config(command=check_vehicle_info)
            check_reservation_button.config(command=check_reservation_info)
            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)

        payments_frame = tk.Frame(new_window)
        payments_frame.configure(bg="black")
        payments_frame.pack(pady=(0,10))


        check_vehicle_button = tk.Button(payments_frame, text="Check Vehicle Information", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_vehicle_button.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        self.bind_hover_effects(check_vehicle_button)

        check_client_button = tk.Button(payments_frame, text="Check Client Information", width=20, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_client_button.grid(row=0, column=1, pady=20, padx=20, sticky="w")
        self.bind_hover_effects(check_client_button)

        check_reservation_button = tk.Button(payments_frame, text="Check Reservation Information", width=23, borderwidth=2,
                                      fg="white", bg="black", state=DISABLED)
        check_reservation_button.grid(row=0, column=2, pady=20, padx=20, sticky="w")
        self.bind_hover_effects(check_reservation_button)

        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Section to see employees data
    def employees_section(self, new_window):
        treeFrame = tk.Frame(new_window)
        treeFrame.pack(expand=True, fill="both")
        treeFrame.configure(bg="black")

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 10),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(pady=(140, 0))
        
        treeview_frame = tk.Frame(new_window)
        treeview_frame.pack(pady=10)
        treeview_frame.configure(bg="black")
        try:
            database_uri = self.flask_app.config['SQLALCHEMY_DATABASE_URI']
            engine = create_engine(database_uri)
            df = pd.read_sql_table("employee", con=engine)
            df = df.drop(columns=['password'])
            engine.dispose()
        except ValueError:
            print("ValueError")

        def create_tree_from_db(df):
            for widget in treeFrame.winfo_children():
                widget.destroy()

            treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrolly.pack(side="right", fill="y")

            treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
            treeScrollx.pack(side="bottom", fill="x")

            treeview = ttk.Treeview(treeFrame, show="headings",
                                    yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

            treeScrolly.config(command=treeview.yview)
            treeScrollx.config(command=treeview.xview)

            def export_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:

                    selected_df = pd.DataFrame(columns=['id', 'full_name', 'username', 'employee_code', 'employee_type'])
                    for record in selected_items: 
                        x = treeview.index(record)                                       
                        new_df_record = {
                            'id': df.at[x, 'id'],
                            'full_name': df.at[x, 'full_name'],
                            'username': df.at[x, 'username'],
                            'employee_code': df.at[x, 'employee_code'], 
                            'employee_type': df.at[x, 'employee_type']
                        }

                        new_df_record = pd.DataFrame([new_df_record])  

                        selected_df = pd.concat([selected_df, new_df_record], ignore_index=True)
                    self.pop_warning(new_window, selected_df, "export")


            def refresh_tree(df):
                      
                treeview.delete(*treeview.get_children())

                treeview["column"] = list(df)
                treeview["show"] = "headings"

                for column in treeview["column"]:
                    treeview.heading(column, text=column)
                    treeview.column(column, anchor="center")
           
                   
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    treeview.insert("", "end", values=row)

                for col in treeview["columns"]:
                    heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                    try:
                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                    except OverflowError:
                        max_width = 0 
                    
                    column_width = max(heading_width, max_width) + 20
                    
                    treeview.column(col, width=column_width, minwidth=column_width)

                treeview.update_idletasks()

            def select_record(e):
                selected_items = treeview.selection()

                if len(selected_items) > 0:
                    x = treeview.index(selected_items[0])

                    export_selected_button.configure(state=NORMAL)
                else:
                    pass

            def remove_selected():
                selected_items = treeview.selection()
                if len(selected_items) > 0:
                    try:
                        if len(selected_items) == Employee.query.count():
                            warning = "Can not delete all the data from the Employees Database"
                            self.pop_warning(new_window, warning, "cannotdeletealldb" )
                        else:
                            for record in selected_items:
                                x = treeview.index(record)
                                employee = Employee.query.filter_by(id=int(df.at[x, 'id'])).first()
                                db.session.delete(employee)
                                db.session.commit()     
                                treeview.delete(record)
                                df.drop(index=x, inplace=True)
                                df.reset_index(drop=True, inplace=True)
                    except OperationalError as e:
                        warning = "Database is locked. Please close the Database and try again."
                        self.pop_warning(new_window, warning, "databaselocked")
                        db.session.rollback()
                        print("Database is locked. Please try again later.")
                else:
                    warning = "Must select at least one record to remove"
                    self.pop_warning(new_window, warning, "noselectedtoremove")


            refresh_tree(df)
            treeview.pack(expand=True, fill="both")

            remove_selected_button = Button(treeview_frame, text="Remove Selected Record(s)",
                                                    fg="white",
                                                    bg="black", command=remove_selected)
            remove_selected_button.grid(row=0, column=0, padx=20, pady=3)
            self.bind_hover_effects(remove_selected_button)

            export_selected_button = tk.Button(treeview_frame, text="Export Selected Data", width=22, borderwidth=2,
                                          fg="white", bg="black", state=DISABLED)
            export_selected_button.grid(row=0, column=1, pady=15, padx=20)
            self.bind_hover_effects(export_selected_button)

            export_all_button = tk.Button(treeview_frame, text="Export All Data", width=22, borderwidth=2,
                                          fg="white", bg="black", state=DISABLED)
            export_all_button.grid(row=0, column=2, pady=15, padx=20)
            self.bind_hover_effects(export_all_button)

            treeview.bind("<ButtonRelease-1>", select_record)


            export_all_button.config(command=lambda: self.pop_warning(new_window, df, "export"), state=NORMAL)
            export_selected_button.config(command=export_selected)
            remove_selected_button.config(command=remove_selected)


        if df is not None and not df.empty:
            create_tree_from_db(df)
        else:
            print("Database table is empty")

    # Frame that is presented to the user after the login
    def show_authenticated_frame(self, authenticated_username, success_message=None):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        insert_menu = tk.Menu(menu_bar, tearoff=0)
        insert_menu.add_command(label="Insert Vehicles",
                                command=lambda: self.create_section_window("Insert Vehicles"))
        insert_menu.add_command(label="Insert Clients",
                                command=lambda: self.create_section_window("Insert Clients"))
        insert_menu.add_command(label="Make Reservations",
                                command=lambda: self.create_section_window("Make Reservations"))

        menu_bar.add_cascade(label="Insert", menu=insert_menu)

        manage_menu = tk.Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Manage Vehicles",
                                command=lambda: self.create_section_window("Manage Vehicles"))
        manage_menu.add_command(label="Manage Clients",
                                command=lambda: self.create_section_window("Manage Clients"))
        manage_menu.add_command(label="Manage Reservations",
                                command=lambda: self.create_section_window("Manage Reservations"))
        menu_bar.add_cascade(label="Manage", menu=manage_menu)

        pay_menu = tk.Menu(menu_bar, tearoff=0)
        pay_menu.add_command(label="Check Payment Records", command=lambda: self.create_section_window("Payment Records"))
        menu_bar.add_cascade(label="Payments", menu=pay_menu)

        employee = Employee.query.filter_by(username=authenticated_username).first()

        employee_menu = tk.Menu(menu_bar, tearoff=0)
        employee_menu.add_command(label="Check Employees Information", command=lambda: self.create_section_window("Employees Information")
                                 if employee.employee_type == "Manager" else self.pop_warning(self.root, "Only managers can access this area", "employeesdata"))
        menu_bar.add_cascade(label="Employees", menu=employee_menu)

        head_frame = tk.Frame(self.root)
        head_frame.pack(fill=tk.BOTH, expand=True)
        head_frame.pack_propagate(False)
        head_frame.configure(bg="black")

        # Each function below is linked to its respective button in the initial dashboard and sends a string to the create_tree_info
        # the function uses the string to search the string that matches it and displays the information related to the string 
        def show_rented_vehicles():
            create_tree_info("vehicles")
        def show_reservations():
            create_tree_info("reservations")       
        def show_inspection_expiring():
            create_tree_info("expiring_inspection")
        def show_legalization_expiring():
             create_tree_info("expiring_legalization")
        def show_last_clients():
            create_tree_info("clients")

        buttons = [
            ("Rented Vehicles", show_rented_vehicles),
            ("Reservations", show_reservations),
            ("Last Clients", show_last_clients)
        ]
        for i, (text, command) in enumerate(buttons):
            button = tk.Button(head_frame, text=text, width=14, borderwidth=1, fg="white", bg="black",
                               command=command)
            button.grid(row=0, column=i, sticky="w")
            self.bind_hover_effects(button)

        expiring_inspection_button = tk.Button(head_frame, text="Vehicles Expiring Inspection", width=23, borderwidth=1, fg="white", bg="black",
                           command=show_inspection_expiring)
        expiring_inspection_button.grid(row=0, column=3, sticky="w")
        self.bind_hover_effects(expiring_inspection_button)

        expiring_legalization_button = tk.Button(head_frame, text="Vehicles Expiring Legalization", width=23, borderwidth=1, fg="white", bg="black",
                           command=show_legalization_expiring)
        expiring_legalization_button.grid(row=0, column=4, sticky="w")
        self.bind_hover_effects(expiring_legalization_button)

        head_frame.grid_columnconfigure(5, weight=1)  

        welcome_label = tk.Label(head_frame, text=f"You're logged in as, {authenticated_username}",
                                 font=("Helvetica", 10), fg="white", bg="black")
        welcome_label.grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Check if the authenticated user is a manager and search for any vehicle expiring inspection/legalization, if any is found warns the manager
        if employee.employee_type == "Manager":
            vehicles = Vehicle.query.all()
            soon_to_expire = []
            for vehicle in vehicles:                
                current_date = datetime.now()

                date_next_inspection = datetime.strptime(str(vehicle.next_inspection), "%Y-%m-%d")
                days_left_to_inspection = (date_next_inspection - current_date).days
                days_left_to_inspection +=1

                date_next_legalization = datetime.strptime(str(vehicle.next_legalization), "%Y-%m-%d")
                days_left_to_legalization = (date_next_legalization - current_date).days
                days_left_to_legalization += 1
                if days_left_to_legalization <= 5 and days_left_to_legalization >= 0 or days_left_to_inspection <= 5 and days_left_to_inspection >= 0:
                    soon_to_expire.append(vehicle)
            if len(soon_to_expire) > 0:
                self.pop_warning(self.root, soon_to_expire, "managerexpirewarning")

        # Funtion that allows the user to logout 
        def logout():
            print("Cleanup tasks completed. Logging out...")
            success_message = "Logout successful!"
            self.show_main_window(authenticated=False, success_message=success_message)

        logout_button = tk.Button(head_frame, text="Logout", width=10, borderwidth=1, fg="white", bg="#800000",
                                  command=logout)
        logout_button.grid(row=0, column=7, sticky="e")
        self.red_bind_hover_effects(logout_button)

        info_frame = tk.Frame(self.root)
        info_frame.pack(fill=tk.BOTH, expand=True)
        info_frame.configure(bg="black")

        # Function that searches for specific data inside of the database, creates a dataframe and displays it to the user using the treeview widget
        def create_tree_info(info):
            try:
                for widget in treeFrame.winfo_children():
                    widget.destroy()

                if info == "vehicles":
                    reservations = Reservation.query.filter_by(reservation_state="In progress").all()
                    df = pd.DataFrame(columns=['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate', 'Number of Seats',
                        'Number of Wheels', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Doors', 'Vehicle Photos'])

                    for reservation in reservations:
                        vehicle = Vehicle.query.filter_by(license_plate=reservation.vehicle_id).first()
                        new_df_record = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                        'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                        'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                        new_df_record = pd.DataFrame([new_df_record]) 
                        df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "reservations":
                    reservations = Reservation.query.order_by(desc(Reservation.insertion_date)).all()
                    df = pd.DataFrame(columns=['Pick-up Date', 'Drop-off Date', 'Vehicle License Plate', 'Rental Duration', 'Cost Per Day', 'Total Cost', 
                                                  'Full Name', 'Phone Number', 'Email', 'ID/Passport Number', 'Date of Birth', 'Nationality', 'Emergency Contact Name', 
                                                  'Emergency Contact Number', 'Billing Address', 'Payment-Method', 'Reservation State','Receipt Photos'])

                    for reservation in reservations:                                                                    
                            new_df_record = {
                                'Pick-up Date': reservation.pick_up_date,
                                'Drop-off Date': reservation.drop_off_date,
                                'Vehicle License Plate': reservation.vehicle_id, 
                                'Rental Duration': reservation.rental_duration, 
                                'Cost Per Day': reservation.cost_per_day, 
                                'Total Cost': reservation.total_cost,
                                'Full Name': reservation.full_name, 
                                'Phone Number': reservation.phone_number, 
                                'Email': reservation.email, 
                                'ID/Passport Number': reservation.id_passport_number,
                                'Date of Birth': reservation.date_of_birth, 
                                'Nationality': reservation.nationality, 
                                'Emergency Contact Name': reservation.emergency_contact_name,
                                'Emergency Contact Number': reservation.emergency_contact_number, 
                                'Billing Address': reservation.billing_address, 
                                'Payment-Method': reservation.payment_method,
                                'Reservation State':reservation.reservation_state,
                                'Receipt Photos': reservation.photos
                            }

                            new_df_record = pd.DataFrame([new_df_record]) 

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "clients":
                    last_clients = Client.query.order_by(desc(Client.insertion_date)).all()
                    df = pd.DataFrame(columns=['Full Name', 'Date of Birth', "Phone Number Indicative", 'Phone Number', 'Email', 'Address', 'Nationality', 'Identification Type', 'Identification Number', 'Credit Number',
                            'Billing Address', 'Preferred Car Type', 'Preferred Motorcycle Type', 'Motorcycle License', 'Emergency Contact Name', 'Contact Number Indicative', 'Emergency Contact Number', 'Currently Renting', 'Client ID Photos'])

                    for client in last_clients:
                        new_df_record = {
                            'Full Name':client.f_name,
                            'Date of Birth':client.dob,
                            "Phone Number Indicative": str(client.p_n_indicative),
                            'Phone Number':str(client.p_number),
                            'Email':client.email,
                            'Address':client.address,
                            'Nationality':client.nationality,
                            'Identification Type':client.id_type,
                            'Identification Number':str(client.id_number),
                            'Credit Number':str(client.credit_number),
                            'Billing Address':client.bill_address,
                            'Preferred Car Type':client.p_car,
                            'Preferred Motorcycle Type':client.p_moto,
                            'Motorcycle License': client.m_license,
                            'Emergency Contact Name':client.em_name, 
                            'Contact Number Indicative':str(client.p_em_indicative),
                            'Emergency Contact Number':str(client.em_number),
                            'Currently Renting':client.renting,
                            'Client ID Photos':client.photos
                        }

                        new_df_record = pd.DataFrame([new_df_record]) 

                        df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "expiring_inspection":
                    vehicles = Vehicle.query.all()
                    df = pd.DataFrame(columns=['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate', 'Number of Seats',
                        'Number of Wheels', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Doors', 'Vehicle Photos'])

                    for vehicle in vehicles:
                        date_next_inspection = datetime.strptime(str(vehicle.next_inspection), "%Y-%m-%d")

                        current_date = datetime.now()
                        days_left_to_inspection = (date_next_inspection - current_date).days
                        days_left_to_inspection +=1

                        if days_left_to_inspection <= 15:
                            new_df_record = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                            'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                            'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                            new_df_record = pd.DataFrame([new_df_record]) 

                            df = pd.concat([df, new_df_record], ignore_index=True)

                elif info == "expiring_legalization":
                    vehicles = Vehicle.query.all()
                    df = pd.DataFrame(columns=['Vehicle Type', 'Category', 'Segment', 'Brand', 'Model', 'Year', 'License Plate', 'Number of Seats',
                        'Number of Wheels', 'Color', 'Fuel', 'Vehicle CC', 'Type of Gearbox', 'Number of Doors', 'Vehicle Photos'])

                    for vehicle in vehicles:
                        date_next_inspection = datetime.strptime(str(vehicle.next_inspection), "%Y-%m-%d")

                        current_date = datetime.now()

                        date_next_legalization = datetime.strptime(str(vehicle.next_inspection), "%Y-%m-%d")
                        days_left_to_legalization = (date_next_legalization - current_date).days

                        days_left_to_legalization += 1

                        if days_left_to_legalization <= 15:
                            new_df_record = {'Vehicle Type':vehicle.vehicle_type,'Category':vehicle.category,'Segment':vehicle.segment,'Brand':vehicle.brand,
                            'Model':vehicle.model,'Year':vehicle.year,'License Plate':vehicle.license_plate,'Number of Seats':vehicle.seats,'Number of Wheels':vehicle.wheels,
                            'Color':vehicle.color,'Fuel':vehicle.fuel, 'Vehicle CC': vehicle.cc, 'Type of Gearbox':vehicle.gearbox,'Number of Doors':vehicle.doors,'Vehicle Photos':vehicle.photos}

                            new_df_record = pd.DataFrame([new_df_record]) 

                            df = pd.concat([df, new_df_record], ignore_index=True)

                if len(df) > 0:
                    for widget in treeFrame.winfo_children():
                        widget.destroy()

                    treeScrolly = ttk.Scrollbar(treeFrame, orient="vertical")
                    treeScrolly.pack(side="right", fill="y")

                    treeScrollx = ttk.Scrollbar(treeFrame, orient="horizontal")
                    treeScrollx.pack(side="bottom", fill="x")

                    treeview = ttk.Treeview(treeFrame, show="headings",
                                            yscrollcommand=treeScrolly.set, xscrollcommand=treeScrollx.set)

                    treeScrolly.config(command=treeview.yview)
                    treeScrollx.config(command=treeview.xview)

                    def convert_to_datetime(date_string):
                        try:
                            return pd.to_datetime(date_string, format='%Y-%m-%d').date()
                        except ValueError:
                            return date_string

                    column_list = df.columns.tolist()

                    if 'Vehicle Type' in column_list:
                        df['Year'] = df['Year'].apply(convert_to_datetime)
                        columns_to_int = ['Number of Doors', 'Number of Wheels', 'Number of Seats']
                        photo_col = "Vehicle Photos"
                    elif 'Client ID Photos' in column_list:
                        df['Date of Birth'] = df['Date of Birth'].apply(convert_to_datetime)
                        columns_to_int = []
                        photo_col = "Client ID Photos"
                    elif 'Pick-up Date' in column_list:
                        df['Pick-up Date'] = df['Pick-up Date'].apply(convert_to_datetime)
                        columns_to_int = ['Rental Duration', 'Cost Per Day', 'Total Cost']
                        photo_col = "Receipt Photos"

                    def grab_photo_path(e):
                        global photos
                        selected_items = treeview.selection()
                        if len(selected_items) > 0:
                            x = treeview.index(selected_items[0])
                            verify_photo_button.config(state=NORMAL)
                            paths = df.at[x, photo_col]
                            photos = paths.split(',')

                    treeview["column"] = column_list
                    treeview["show"] = "headings"

                    for column in treeview["column"]:
                        treeview.heading(column, text=column)
                        treeview.column(column, anchor="center")

                    for column in columns_to_int:
                        try:
                            df[column] = df[column].fillna(0).astype('int64')
                            df[column] = df[column].replace(0, 'nan')
                        except ValueError:
                            pass             
                       
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        treeview.insert("", "end", values=row)

                    for col in treeview["columns"]:
                        heading_width = tkFont.Font().measure(treeview.heading(col)["text"])

                        max_width = max(
                            tkFont.Font().measure(str(treeview.set(item, col)))
                            for item in treeview.get_children("")
                        )
                        
                        column_width = max(heading_width, max_width) + 20 
                        treeview.column(col, width=column_width, minwidth=heading_width)

                    treeview.column(photo_col, width=120, minwidth=120)

                    treeview.pack(expand=True, fill="both")

                    verify_photo_frame = tk.Frame(treeFrame)
                    verify_photo_frame.pack(pady=(15,5), expand=True, fill="both")
                    verify_photo_frame.configure(bg="#313131")

                    verify_photo_button = Button(verify_photo_frame, text="Verify Photos of Selected", fg="white",
                                                   bg="black", width=20, state=DISABLED, command=lambda: self.photo_viewer(self.root, photos, "View Mode"))
                    verify_photo_button.pack(side="right", padx=5)
                    self.bind_hover_effects(verify_photo_button) 
                    treeview.bind("<ButtonRelease-1>", grab_photo_path)                                  
                else:
                    df_section_info = "0 items matched the search"
                    df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                                       fg="darkred", bg="black")
                    df_section_info_label.pack(ipady=(140))
                    pass

            except Exception as e:
                df_section_info = "Database table is empty"
                df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                                   fg="darkred", bg="black")
                df_section_info_label.pack(ipady=(140))
                pass

        treeFrame = tk.Frame(info_frame)
        treeFrame.pack()

        df_section_info = "Database table is empty"
        df_section_info_label = tk.Label(treeFrame, text=df_section_info, font=("Helvetica", 18),
                                           fg="darkred", bg="black")
        df_section_info_label.pack(ipady=(140))

        info_section_frame = tk.Frame(info_frame)
        info_section_frame.pack()
        info_section_frame.configure(bg="black")

        amount_available_label = tk.Label(info_section_frame, text="Available vehicles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        amount_available_label.grid(row=0, column=0, pady=(10,5), padx=5, sticky=tk.E)
        amount_available_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        amount_available_entry.grid(row=0, column=1, pady=(10,5), padx=(5, 10), sticky=tk.W)

        amount_rented_label = tk.Label(info_section_frame, text="Rented vehicles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        amount_rented_label.grid(row=0, column=4, pady=5, padx=5, sticky=tk.E)
        amount_rented_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        amount_rented_entry.grid(row=0, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        motorcycles_label = tk.Label(info_section_frame, text="--- Motorcycles ---",
                                   font=("Helvetica", 10), fg="white", bg="black")
        motorcycles_label.grid(row=1, column=0, columnspan=2, pady=(10,5), padx=5)               

        available_motorcycles_label = tk.Label(info_section_frame, text="Available motorcycles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_motorcycles_label.grid(row=2, column=0, pady=(10,5), padx=5, sticky=tk.E)
        available_motorcycles_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_motorcycles_entry.grid(row=2, column=1, pady=(10,5), padx=(5, 10), sticky=tk.W)

        available_gold_motorcycles_label = tk.Label(info_section_frame, text="Available gold category motorcycles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_gold_motorcycles_label.grid(row=3, column=0, pady=(10,5), padx=5, sticky=tk.E)
        available_gold_motorcycles_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_gold_motorcycles_entry.grid(row=3, column=1, pady=(10,5), padx=(5, 10), sticky=tk.W)

        available_silver_motorcycles_label = tk.Label(info_section_frame, text="Available silver category motorcycles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_silver_motorcycles_label.grid(row=4, column=0, pady=5, padx=5, sticky=tk.E)
        available_silver_motorcycles_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_silver_motorcycles_entry.grid(row=4, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        available_economic_motorcycles_label = tk.Label(info_section_frame, text="Available economic category motorcycles:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_economic_motorcycles_label.grid(row=5, column=0, pady=5, padx=5, sticky=tk.E)
        available_economic_motorcycles_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_economic_motorcycles_entry.grid(row=5, column=1, pady=5, padx=(5, 10), sticky=tk.W)

        cars_label = tk.Label(info_section_frame, text="--- Cars ---",
                                   font=("Helvetica", 10), fg="white", bg="black")
        cars_label.grid(row=1, column=2, columnspan=2, pady=(10,5), padx=5)  

        available_cars_label = tk.Label(info_section_frame, text="Available cars:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_cars_label.grid(row=2, column=2, pady=(10,5), padx=5, sticky=tk.E)
        available_cars_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_cars_entry.grid(row=2, column=3, pady=(10,5), padx=(5, 10), sticky=tk.W)

        available_gold_cars_label = tk.Label(info_section_frame, text="Available gold category cars:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_gold_cars_label.grid(row=3, column=2, pady=(10,5), padx=5, sticky=tk.E)
        available_gold_cars_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_gold_cars_entry.grid(row=3, column=3, pady=(10,5), padx=(5, 10), sticky=tk.W)

        available_silver_cars_label = tk.Label(info_section_frame, text="Available silver category cars:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_silver_cars_label.grid(row=4, column=2, pady=5, padx=5, sticky=tk.E)
        available_silver_cars_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_silver_cars_entry.grid(row=4, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        available_economic_cars_label = tk.Label(info_section_frame, text="Available economic category cars:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        available_economic_cars_label.grid(row=5, column=2, pady=5, padx=5, sticky=tk.E)
        available_economic_cars_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        available_economic_cars_entry.grid(row=5, column=3, pady=5, padx=(5, 10), sticky=tk.W)

        reservations_label = tk.Label(info_section_frame, text="--- Reservations Data ---",
                                   font=("Helvetica", 10), fg="white", bg="black")
        reservations_label.grid(row=1, column=4, columnspan=2, pady=(10,5), padx=5) 

        month_revenue_label = tk.Label(info_section_frame, text="Current month revenue:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        month_revenue_label.grid(row=2, column=4, pady=5, padx=5, sticky=tk.E)
        month_revenue_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        month_revenue_entry.grid(row=2, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        year_revenue_label = tk.Label(info_section_frame, text="Current year revenue:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        year_revenue_label.grid(row=3, column=4, pady=5, padx=5, sticky=tk.E)
        year_revenue_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        year_revenue_entry.grid(row=3, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        amount_reservations_cancelled_label = tk.Label(info_section_frame, text="Cancelled reservations:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        amount_reservations_cancelled_label.grid(row=4, column=4, pady=5, padx=5, sticky=tk.E)
        amount_reservations_cancelled_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        amount_reservations_cancelled_entry.grid(row=4, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        amount_reservations_completed_label = tk.Label(info_section_frame, text="Completed reservations:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        amount_reservations_completed_label.grid(row=5, column=4, pady=5, padx=5, sticky=tk.E)
        amount_reservations_completed_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        amount_reservations_completed_entry.grid(row=5, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        amount_reservations_in_progress_label = tk.Label(info_section_frame, text="Reservations in progress:",
                                   font=("Helvetica", 10), fg="white", bg="black")
        amount_reservations_in_progress_label.grid(row=6, column=4, pady=5, padx=5, sticky=tk.E)
        amount_reservations_in_progress_entry = tk.Entry(info_section_frame, bd=2, width=10, state="readonly", readonlybackground="#313131")
        amount_reservations_in_progress_entry.grid(row=6, column=5, pady=5, padx=(5, 10), sticky=tk.W)

        # Function responsible to gather the data to populate the initial dashboard
        def refresh_data():
            vehicles_available = Vehicle.query.filter_by(availability="Available").all()
            reservations_in_progress = Reservation.query.filter_by(reservation_state="In progress").all()

            current_month = datetime.now().month
            current_year = datetime.now().year

            current_month_reservations = Reservation.query.filter(
                extract('month', Reservation.insertion_date) == current_month,
                extract('year', Reservation.insertion_date) == current_year,
                Reservation.reservation_state != 'Cancelled'
            ).all()

            total_revenue_current_month = sum(reservation.total_cost for reservation in current_month_reservations)

            current_year_reservations = Reservation.query.filter(
                extract('year', Reservation.insertion_date) == current_year,
                Reservation.reservation_state != 'Cancelled'
            ).all()

            total_revenue_current_year = sum(reservation.total_cost for reservation in current_year_reservations)
            cancelled_reservations = Reservation.query.filter(Reservation.reservation_state == 'Cancelled').all()
            completed_reservations = Reservation.query.filter(Reservation.reservation_state == 'Completed').all()
            in_progress_reservations = Reservation.query.filter(Reservation.reservation_state == 'In progress').all()
            motorcycles_available = Vehicle.query.filter_by(availability="Available", vehicle_type="motorcycles").all()
            economic_motorcycles_available = Vehicle.query.filter_by(availability="Available", vehicle_type="motorcycles", category="economic").all()
            silver_motorcycles_available = Vehicle.query.filter_by(availability="Available", vehicle_type="motorcycles", category="silver").all()
            gold_motorcycles_available = Vehicle.query.filter_by(availability="Available", vehicle_type="motorcycles", category="gold").all()
            cars_available = Vehicle.query.filter_by(availability="Available", vehicle_type="cars").all()
            economic_cars_available = Vehicle.query.filter_by(availability="Available", vehicle_type="cars", category="economic").all()
            silver_cars_available = Vehicle.query.filter_by(availability="Available", vehicle_type="cars", category="silver").all()
            gold_cars_available = Vehicle.query.filter_by(availability="Available", vehicle_type="cars", category="gold").all()

            read_only = [amount_available_entry, amount_rented_entry, month_revenue_entry, year_revenue_entry, amount_reservations_cancelled_entry,
            amount_reservations_completed_entry, amount_reservations_in_progress_entry, available_cars_entry, available_gold_cars_entry, available_silver_cars_entry,
            available_economic_cars_entry, available_motorcycles_entry, available_gold_motorcycles_entry, available_silver_motorcycles_entry, available_economic_motorcycles_entry]

            for entry in read_only:
                entry.config(state=tk.NORMAL)
                entry.delete(0, END)

            amount_available_entry.insert(0, len(vehicles_available))
            amount_rented_entry.insert(0, len(in_progress_reservations))
            month_revenue_entry.insert(0, total_revenue_current_month)
            year_revenue_entry.insert(0, total_revenue_current_year)
            amount_reservations_cancelled_entry.insert(0, len(cancelled_reservations))
            amount_reservations_completed_entry.insert(0, len(completed_reservations))
            amount_reservations_in_progress_entry.insert(0, len(in_progress_reservations))
            available_motorcycles_entry.insert(0, len(motorcycles_available))
            available_economic_motorcycles_entry.insert(0, len(economic_motorcycles_available))
            available_silver_motorcycles_entry.insert(0, len(silver_motorcycles_available))
            available_gold_motorcycles_entry.insert(0, len(gold_motorcycles_available))
            available_cars_entry.insert(0, len(cars_available))
            available_economic_cars_entry.insert(0, len(economic_cars_available))
            available_silver_cars_entry.insert(0, len(silver_cars_available))
            available_gold_cars_entry.insert(0, len(gold_cars_available))

            for entry in read_only:
                entry.config(state="readonly")

        refresh_data_button = tk.Button(info_section_frame, text="Refresh Data", width=10, borderwidth=1, fg="white", bg="black",
                                  command=refresh_data)
        refresh_data_button.grid(row=6, column=2, columnspan=2, pady=(10,5), padx=5)
        self.bind_hover_effects(refresh_data_button)

        refresh_data()
        show_rented_vehicles()

    # Frame that is presented to the user that allows to logon, also shown after the log out
    def show_non_authenticated_frame(self, error_message=None, success_message=None):
        button_text = "Add new user"
        button_command = self.new_employee
        add_user_button = tk.Button(self.root, text=button_text, command=button_command, fg="white", bg="black")
        add_user_button.pack(side=tk.TOP, anchor=tk.NE, pady=(20, 0), padx=(0, 20))

        label_text = "Welcome to Luxury Wheels!"
        label_font = ("Helvetica", 30)
        label1 = tk.Label(self.root, text=label_text, font=label_font, fg="white", bg="black")
        label1.pack(expand=True, pady=(30, 20))

        username_label = tk.Label(self.root, text="Username:", fg="white", bg="black")
        username_label.pack(side=tk.TOP, padx=10, pady=2)
        username_entry = Entry(self.root, width=35, borderwidth=5)
        username_entry.pack(side=tk.TOP, pady=2)

        password_label = tk.Label(self.root, text="Password:", fg="white", bg="black")
        password_label.pack(side=tk.TOP, padx=10, pady=(10, 2))
        password_entry = Entry(self.root, show="*", width=35, borderwidth=5)
        password_entry.pack(side=tk.TOP, pady=2)

        # Function that allows the user to login
        def login():
            try:
                existing_user = Employee.query.filter(Employee.username.ilike(username_entry.get())).first()

                if existing_user:
                    user_password = existing_user.password
                    if bcrypt.check_password_hash(user_password, password_entry.get()):
                        authenticated_username = existing_user.username
                        self.show_main_window(authenticated=True, authenticated_username=authenticated_username,
                                              success_message="User logged in successfully!")
                    else:
                        self.show_main_window(authenticated=False, error_message="Incorrect Password")
                else:
                    self.show_main_window(authenticated=False, error_message="Invalid Username")
            except Exception as e:
                print(e)


        login_button = tk.Button(self.root, text="Login", command=login, fg="white", bg="#004d00")
        login_button.pack(side=tk.TOP, pady=(20, 130))
        self.green_bind_hover_effects(login_button)
        self.bind_hover_effects(add_user_button)

        error_label = tk.Label(self.root, text=error_message or "", foreground="red", background="black",
                               font=("Helvetica", 12))
        error_label.pack(side=tk.TOP, pady=(0, 10))

        if success_message:
            success_label = tk.Label(self.root, text=success_message, font=("Helvetica", 12),
                                     fg="green", bg="black")
            success_label.pack(side=tk.TOP, pady=(0, 10))
            self.root.after(3000, lambda: success_label.destroy())

    # Main window of the program, that will display the 'show_non_authenticated_frame' before the login and the 'show_authenticated_frame' after the login
    def show_main_window(self, authenticated=False, authenticated_username=None, success_message=None, error_message=None):
        for widget in self.root.winfo_children():
            widget.destroy()

        with self.flask_app.app_context():
            db.create_all()

        self.canvas.destroy()
        self.root.withdraw()
        self.root.overrideredirect(False)
        self.root.title("Luxury Wheels")
        self.root.resizable(1, 1)
        self.root.iconphoto(True, PhotoImage(file=resource_path('resources/lw.png')))
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.deiconify()

        # Check if the user is authenticated or not, the window content will be different for each situation
        if authenticated:
            self.show_authenticated_frame(authenticated_username, success_message)
        else:
            self.show_non_authenticated_frame(error_message, success_message)

# Check if this module is being run as the main program
if __name__ == '__main__':
    root = tk.Tk() # Create a Tkinter root window
    style = ttk.Style(root) # Create a style object for customizing widgets
    root.tk.call("source", resource_path("forest-dark.tcl")) # Load custom theme from 'forest-dark.tcl' file
    style.theme_use("forest-dark") # Set the theme to 'forest-dark'
    lw_app = Lw(root, app) # Create an instance of the Lw class, passing the root window and the 'app' object
    root.mainloop() # Start the Tkinter event loop to display the GUI