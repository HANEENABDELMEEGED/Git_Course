from customtkinter import *  
from PIL import Image, ImageTk
from datetime import date  # to get the date of the new program that user write
app = CTk()  # the window
app.geometry("600x500")  # the size of the frame
set_appearance_mode("light")  # the mode of the window light or dark

bg_image = Image.open("p.jpeg")  # the name of the image (main frame)
bg_image = bg_image.resize((1200, 1100), Image.Resampling.LANCZOS)  # to match window size
bg_photo = ImageTk.PhotoImage(bg_image)  # store the image

def create_background_canvas():
    canvas = CTkCanvas(master=app, width=180, height=400, bg='white', highlightthickness=0)  # the line on the main frame
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)
    canvas.pack(fill="both", expand=True)  # here to display the image
    return canvas

background_canvas = create_background_canvas()  # Create background canvas

def create_main_page():  # Create the main frame 
    main_frame = CTkFrame(master=background_canvas, fg_color="#DCDCDC", border_color="#FCFAF2", border_width=0, corner_radius=15)
    label = CTkLabel(master=main_frame, font=("Georgia", 25), text="Haneen Abdelmeeged ", text_color="#1C1C1C")
    check_button = CTkButton(master=main_frame, text="Check programs", font=("Georgia", 14), fg_color="#1C1C1C", hover_color="#585858", border_width=0, command=switch_to_check)
    space_label = CTkLabel(master=main_frame, font=("Georgia", 16), text="or", text_color="#585858")
    add_button = CTkButton(master=main_frame, text="Add program", font=("Georgia", 14), fg_color="#1C1C1C", hover_color="#585858", border_width=2, command=switch_to_add)
    
    # Packing the widgets
    label.pack(anchor="n", pady=20, padx=30)
    check_button.pack(anchor="n", pady=10, padx=30)
    space_label.pack(anchor="n", pady=5, padx=5)
    add_button.pack(anchor="n", pady=10, padx=30)
    main_frame.pack(anchor="center", expand=True) 

    return main_frame

def create_add_page():
    add_frame = CTkFrame(master=background_canvas, fg_color="#DCDCDC", border_color="#FCFAF2", border_width=1, corner_radius=15)
    label = CTkLabel(master=add_frame, text="Add program", font=("Georgia", 22), text_color="#1C1C1C")
    
    global title_entry, description_entry, date_entry
    title_entry = CTkEntry(master=add_frame, placeholder_text="Title", text_color="#585858")
    description_label = CTkLabel(master=add_frame, text="Description:", font=("Georgia", 22), text_color="#1C1C1C")
    description_entry = CTkTextbox(master=add_frame, text_color="#06081F", border_width=2)

    # New date entry field for optional custom date
    date_entry = CTkEntry(master=add_frame, placeholder_text="Date", text_color="#585858")

    add_button = CTkButton(master=add_frame, text="Save", fg_color="#1C1C1C", hover_color="#585858", border_width=2,
                           command=lambda: handle_add(title_entry.get(), description_entry.get("1.0", "end-1c"), date_entry.get()))
    back_button = CTkButton(master=add_frame, text="Back", fg_color="#1C1C1C", hover_color="#585858", border_width=2, command=switch_to_main)

    # Packing widgets
    label.pack(anchor="n", pady=10, padx=30)
    title_entry.pack(anchor="n", pady=10, padx=30)
    description_label.pack(anchor="nw", pady=10, padx=10)
    description_entry.pack(expand=True, fill="both", padx=20, pady=20)
    date_entry.pack(anchor="n", pady=10, padx=30)  # Add date entry
    add_button.pack(anchor="n", pady=10, padx=30)
    back_button.pack(anchor="n", pady=10, padx=30)

    return add_frame

# Function to create the check page with buttons for each title
def create_check_page():  # Create the check page
    check_frame = CTkFrame(master=background_canvas, fg_color="#DCDCDC", border_color="#FCFAF2", border_width=1, corner_radius=15)
    
    # Create a canvas and a scrollbar for scrolling functionality
    scroll_canvas = CTkCanvas(master=check_frame, bg="#DCDCDC")
    scroll_frame = CTkFrame(master=scroll_canvas, fg_color="#DCDCDC")

    # Add a scrollbar to the canvas
    scrollbar = CTkScrollbar(master=check_frame, orientation="vertical", command=scroll_canvas.yview) #Sets the scrollbar orientation to vertical,Links the scrollbar with the vertical view of the canvas.
    scroll_canvas.configure(yscrollcommand=scrollbar.set) #The scrollbar’s position is linked to the vertical scrolling of the canvas.

    scrollbar.pack(side="right", fill="y")  # Makes the scrollbar fill the vertical space
    scroll_canvas.pack(side="left", fill="both", expand=True)  #the side of the titles's name
    scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Load titles and dynamically create buttons
    titles = load_titles()  # Load titles from the file

    for title in titles:
        title_button = CTkButton(master=scroll_frame, text=title, fg_color="#1C1C1C", hover_color="#585858", border_width=2, #Each button is placed inside the scroll_frame, text is the titles's name that it will write on each button
                                 command=lambda t=title: show_program_details(t, check_frame)) #t=title: Creates an anonymous function (lambda function) that captures the current value of title and passes it to the show_program_details function.
        title_button.pack(pady=15, padx=30)                                                     #(t, check_frame): This function is called when the button is clicked. It receives the title of the program (t) and the current frame (check_frame) as arguments.

    # Update scroll region to encompass all items
    scroll_frame.update_idletasks()  #Updates the scroll_frame to ensure all buttons are rendered before adjusting the scroll region.
    scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))  #all: This argument specifies that the bounding box should encompass all items in the canvas.

    # Create Back button
    back_button = CTkButton(master=check_frame, text="Back", fg_color="#1C1C1C", hover_color="#585858", border_width=2, command=switch_to_main)
    back_button.pack(anchor="se",pady=190)

    return check_frame

# Function to hide the current frame and switch to main
def back_to_main(frame):
    frame.pack_forget()  # Hide the current frame
    switch_to_main()  # Show the main frame

# Function to load titles from a file
def load_titles():
    titles = []
    try:
        with open(data_file, "r") as file:
            for line in file:
                # Check if the line contains at least two commas, indicating title, description, and date
                if line.count(",") >= 2:
                    # Split the line at the first two commas only
                    parts = line.strip().split(",", 2)
                    title, description, date = parts[0], parts[1], parts[2]  # Assign parts accordingly
                    titles.append(title)  # Add title to the list of titles
                    data[title] = {"description": description, "date": date}  # Store title, description, and date in data dictionary
                else:
                    print(f"Skipping line (invalid format): {line.strip()}")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error reading file: {e}")
    return titles


# Function to show program details
def show_program_details(title, current_frame):
    # Hide the current frame (the check_frame)
    current_frame.pack_forget()

    # Fetch the program details from the data dictionary
    if title in data:
        information = data.get(title, {})
        description = information.get("description", "No description")
        date = information.get("date", "No date ")
        
        # Display the details in a new frame
        show_the_information(title, description, date)

# Function to display the title, date, and description
def show_the_information(title, description, date):
    show_frame = CTkFrame(master=background_canvas, fg_color="#DCDCDC", border_color="#FCFAF2", border_width=1, corner_radius=15)  # Frame for showing details

    # Title, date, and description labels
    title_label = CTkLabel(master=show_frame, text=f"Title: {title}", font=("Georgia", 22), text_color="#06081F")
    day_label = CTkLabel(master=show_frame, text=f"Date: {date}", font=("Georgia", 20), text_color="#06081F")
    description_label = CTkLabel(master=show_frame, text="Description:", font=("Georgia", 20), text_color="#06081F")
    
    # Textbox for the description
    description_textbox = CTkTextbox(master=show_frame, text_color="#06081F", border_width=0)
    description_textbox.insert("1.0", description)  # Insert description at the start of the textbox
    description_textbox.configure(state="disabled")  # Make the textbox read-only

    # Back button to go back to the main page
    back_button = CTkButton(master=show_frame, text="Back", font=("Georgia", 14), fg_color="#1C1C1C", hover_color="#585858", border_width=2, 
                            command=lambda: back_to_main(show_frame))

    # Pack widgets in the frame
    title_label.pack(anchor="nw", pady=10, padx=10)  
    day_label.pack(anchor="nw", pady=10, padx=10)
    description_label.pack(anchor="nw", pady=10, padx=10)
    description_textbox.pack(expand=True, fill="both", padx=10, pady=10)  
    back_button.pack(pady=20)  

    # Show this frame
    show_frame.pack(expand=True, fill="both", padx=40, pady=40)
    return show_frame


today = date.today()
day = today.strftime("%d/%m/%Y")

def handle_add(title, description, custom_date):
    if title and description:
        # Use the custom date if provided, otherwise default to today's date
        if custom_date.strip():  # Check if custom_date is not empty or just spaces
            saved_date = custom_date
        else:
            today = date.today()
            saved_date = today.strftime("%d/%m/%Y")

        # Save the data
        data[title] = {"description": description, "date": saved_date}
        
        # Save the information in the file
        save_information_in_file()

        # Show the added information
        show_the_information(title, description, saved_date)
        switch_to_main()
    else:
        print("Title or description is empty!")



def save_information_in_file():  
        with open(data_file, "w") as file:
         for title, information in data.items():
            description = information["description"]
            date = information["date"]
            file.write(f"{title},{description},{date}\n")

data_file = "cv.txt"
data = {}  # Dictionary to store titles, descriptions, and dates
data_file = "cv.txt"
data = {}  # Dictionary to store titles, descriptions, and dates
try:
    with open(data_file, "r") as file:
        current_title, current_description, current_date = None, None, None  # Variables for tracking multi-line descriptions
        for line in file:
            line = line.strip()

            # Check if the line contains at least two commas for title, description, and date
            if line.count(",") >= 2:
                parts = line.split(",", 2)  # Split only at the first two commas
                title, description, date = parts[0], parts[1], parts[2]  # Extract the title, description, and date
                data[title] = {"description": description, "date": date}  # Store the data in the dictionary
                current_title, current_description, current_date = title, description, date  # Set current variables
            else:
                # If the line doesn't contain two commas, it's part of the description
                if current_title is not None:
                    current_description += " " + line  # Add the line to the current description
                    data[current_title]["description"] = current_description  # Update the description in the data dictionary
                else:
                    print(f"Skipping invalid line: {line}")
                    
except FileNotFoundError:
    print("File not found. Starting with an empty data set.")
except Exception as e:
    print(f"Error reading file: {e}")
    
def back_to_main(frame):
    frame.pack_forget()  # Hide the frame
    switch_to_main()  # Switch back to the main page

def switch_to_check():
    main_frame.pack_forget()
    check_page.pack(expand=True)


def switch_to_add():
    main_frame.pack_forget()
    add_page.pack( expand=True)
    title_entry.delete(0, 'end')
    description_entry.delete("1.0", "end")

def switch_to_main():
    add_page.pack_forget()
    check_page.pack_forget()
    main_frame.pack( expand=True)

# Create frames
check_page = create_check_page()  # Call the function to create the check page
main_frame = create_main_page()  # Call the function to create the main page
add_page = create_add_page()     # Call the function to create the add page

main_frame.pack(expand=True)

app.mainloop()




