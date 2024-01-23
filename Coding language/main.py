import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import subprocess

var_dict = {}

# Variable to store the project name
project_name = "nameless"

def run_code():
    code = code_text.get("1.0", tk.END)
    try:
        # Explicitly pass var_dict to exec
        exec(code, globals(), var_dict)
        if "print(" in code:
            # Extract variable name or value from print statement
            variable_or_value = code.split("print(")[1].split(")")[0].strip()
            if variable_or_value.startswith('"') and variable_or_value.endswith('"'):
                # Print a specific value
                output_log.config(state=tk.NORMAL)
                output_log.insert(tk.END, f"{variable_or_value[1:-1]}\n")
            elif variable_or_value in var_dict:
                # Print the variable value
                output_log.config(state=tk.NORMAL)
                output_log.insert(tk.END, f"{var_dict[variable_or_value]}\n")
            else:
                output_log.config(state=tk.NORMAL)
                output_log.insert(tk.END, f"Error: Variable '{variable_or_value}' not found\n")
        else:
            output_log.config(state=tk.NORMAL)
            output_log.insert(tk.END, "Code executed successfully\n")
    except Exception as e:
        output_log.config(state=tk.NORMAL)
        output_log.insert(tk.END, f"Error: {e}\n")
    finally:
        output_log.config(state=tk.DISABLED)

def show_help():
    help_window = tk.Toplevel(window)
    help_window.title("Help Page")
    
    # Create a back button
    back_button = tk.Button(help_window, text="Back", command=help_window.destroy)
    back_button.pack()

# Function to auto-complete parentheses, double quotes, and single quotes
def auto_complete(event):
    current_char = code_text.get("insert")
    
    if current_char in ["(", "'", '"']:
        code_text.insert("insert", current_char)
        code_text.insert("insert", current_char)

# Function to add closing parentheses when "print(" is typed
def print_auto_complete(event):
    current_line = code_text.get("insert linestart", "insert")
    
    if "print(" in current_line:
        code_text.insert("insert", ")")

# Function to create an open_window command
def open_window():
    new_window = tk.Toplevel(window)
    new_window.title("New Window")
    var_dict["window_main"] = new_window

# Function to set text in the window
def window_text(text):
    if "window_main" in var_dict:
        text_widget = tk.Label(var_dict["window_main"], text=text)
        text_widget.pack()
    else:
        print("Error: 'window_main' is not defined")

# Function to create a window button
def window_button(name):
    if "window_main" in var_dict:
        button = tk.Button(var_dict["window_main"], text=name, command=lambda: handle_button_click(name))
        button.pack()
        # Store button name in var_dict
        var_dict[name] = f"if ('{name}' in var_dict): create_popup('Popup Text')"
    else:
        print("Error: 'window_main' is not defined")

# Function to handle button click events
def handle_button_click(button_name):
    if button_name in var_dict:
        try:
            exec(var_dict[button_name], globals(), var_dict)
        except Exception as e:
            print(f"Error in button click: {e}")
    else:
        print(f"Error: Button '{button_name}' not defined")

# Function to create a popup
def create_popup(text):
    popup = tk.Toplevel(window)
    popup.title("Popup")
    
    label = tk.Label(popup, text=text)
    label.pack(padx=10, pady=10)
    
    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(pady=5)

# Function to set window size
def window_size(size):
    if "window_main" in var_dict:
        try:
            height, width = map(int, size.split())
            var_dict["window_main"].geometry(f"{width}x{height}")
        except ValueError:
            print("Error: Invalid size format. Use 'height width'")
    else:
        print("Error: 'window_main' is not defined")

# Function to name the window
def window_name(name):
    global project_name
    if "window_main" in var_dict:
        var_dict["window_main"].title(name)
        project_name = name
        update_window_title()
    else:
        print("Error: 'window_main' is not defined")

# Function to save the script
def save_script():
    global project_name
    script = code_text.get("1.0", tk.END)
    
    # If the project has been named, use that name for saving
    if project_name != "nameless":
        file_path = filedialog.asksaveasfilename(defaultextension=".s--", initialfile=f"{project_name}.s--", filetypes=[("Script files", "*.s--")])
    else:
        # Otherwise, ask for a new name
        file_path = filedialog.asksaveasfilename(defaultextension=".s--", filetypes=[("Script files", "*.s--")])
    
    if file_path:
        with open(file_path, "w") as file:
            file.write(script)
        
        # Update the project name after saving
        project_name = file_path.split("/")[-1].split(".s--")[0]
        update_window_title()

# Function to open a script
def open_script():
    global project_name
    file_path = filedialog.askopenfilename(defaultextension=".s--", filetypes=[("Script files", "*.s--")])
    
    if file_path:
        with open(file_path, "r") as file:
            script_content = file.read()
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, script_content)
        
        # Update the project name after opening
        project_name = file_path.split("/")[-1].split(".s--")[0]
        update_window_title()

# Function to update the window title
def update_window_title():
    if project_name != "nameless":
        window.title(f"s-- {project_name}")
    else:
        window.title("Python Code Interpreter")

# Function to build APK using Gradle
def build_apk():
    try:
        # Replace 'your_project_directory' with the actual path to your Android project
        gradle_command = "./gradlew assembleDebug"
        subprocess.run(gradle_command, shell=True, check=True)
        output_log.config(state=tk.NORMAL)
        output_log.insert(tk.END, "APK built successfully\n")
    except subprocess.CalledProcessError as e:
        output_log.config(state=tk.NORMAL)
        output_log.insert(tk.END, f"Error building APK: {e}\n")
    finally:
        output_log.config(state=tk.DISABLED)

# Function to replace the current line with a selected code completion
def replace_current_line(completion):
    current_line_start = code_text.index("insert linestart")
    current_line_end = code_text.index("insert lineend")
    code_text.delete(current_line_start, current_line_end)
    code_text.insert(current_line_start, completion)

# Create the main window
window = tk.Tk()
window.title("Python Code Interpreter")

# Text field for coding
code_text = scrolledtext.ScrolledText(window, width=50, height=10)
code_text.pack(padx=10, pady=10)

# Code completions listbox
completions_listbox = tk.Listbox(window, selectmode=tk.SINGLE)
completions_listbox.pack(pady=5)

# Run button
run_button = tk.Button(window, text="Run", command=run_code)
run_button.pack(pady=5)

# Help button
help_button = tk.Button(window, text="Help", command=show_help)
help_button.pack(pady=5)

# Save button
save_button = tk.Button(window, text="Save", command=save_script)
save_button.pack(pady=5)

# Open button
open_button = tk.Button(window, text="Open", command=open_script)
open_button.pack(pady=5)

# Build APK button
build_button = tk.Button(window, text="Build APK", command=build_apk)
build_button.pack(pady=5)

# Output log
output_log = scrolledtext.ScrolledText(window, width=50, height=5, state=tk.DISABLED)
output_log.pack(padx=10, pady=10)

# Code completion (dummy function for illustration)
def code_complete():
    # Dummy list of code completions
    completions = ["print", "input", "for", "if", "else", "var", "open_window()", "window_text('text_here')", "window_size('height width')", "window_name('window_name_here')", "window_button('Button')", "if ('Button' in var_dict): create_popup('Popup Text')"]
    current_text = code_text.get("insert linestart", "insert")
    matching_completions = [comp for comp in completions if comp.startswith(current_text)]
    
    # Display completions in the listbox
    completions_listbox.delete(0, tk.END)
    for comp in matching_completions:
        completions_listbox.insert(tk.END, comp)

# Key binding for code completion
code_text.bind("<KeyRelease>", lambda event: code_complete())

# Event binding for selecting code completion from the listbox
completions_listbox.bind("<ButtonRelease-1>", lambda event: replace_current_line(completions_listbox.get(completions_listbox.curselection())))

# Run the Tkinter event loop
window.mainloop()
