from doctest import OutputChecker
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My Code Editor") 

input_frame = tk.Frame(root)
input_frame.pack(side="left", fill="both", expand=True)

tk.Label(input_frame, text="Code Input").pack() 


output_frame = tk.Frame(root)
output_frame.pack(side="left", fill="both", expand=True) 

tk.Label(output_frame, text="Output Log").pack()

highlight_colors = {
    "keyword": "yellow",
    "builtin": "orange",
    "string": "green",
    "comment": "red"
}

def highlight(event):
    code = code_text.get("1.0", "end-1c")
    tokens = code.split()
    
    for token in tokens:
        if token in highlight_colors:
            start = code.index(token)
            end = start + len(token)
            code_text.tag_add(token, start, end)
            code_text.tag_config(token, foreground=highlight_colors[token])

# Create left frame 
output_frame = tk.Frame(root)
output_frame.pack(fill="both", padx=10, pady=10) 


# Output text in left frame instead of separate window
# Keep existing output window and run button

output_log = tk.Text(output_frame) 
output_log.pack(fill='both', expand=True, side='top')


def run_code():

  code = code_text.get("1.0", "end-1c") 
  
  try:
    exec(code)
  except Exception as e:
    print(e)

  output = ""
  for line in code.split('\n'):
    if line.startswith("print("):
      # Extract print argument
      start = line.find('"') + 1  
      end = line.rfind('"')
      text = line[start:end]
      output += text + "\n"

  output_log.config(state='normal')
  output_log.insert('end', output)
  output_log.config(state='disabled')






# Show both input and output side-by-side
input_frame = tk.Frame(root)
input_frame.pack(side="left", fill="both", expand=True)

input_field = tk.Entry(input_frame)
input_field.pack(fill='x') 

# Add read-only state to output log
output_log = tk.Text(output_frame, font=("Arial", 16), state='disabled')
output_log.config(state='normal')



output_log.config(state='disabled')

# Update clear log to reset state def clear_log():
def clear_log():
  output_log.config(state='normal')
  output_log.delete('1.0', tk.END)
  output_log.config(state='disabled')
  output_log.config(fg="black", bg="white")
 

# Add scrollbar for output log
scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side='right', fill='y')

output_log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_log.yview)

clear_button = tk.Button(root, text="Clear Log", command=clear_log) 
clear_button.pack(side="bottom") 





run_button = tk.Button(root, text="Run", command=run_code)
run_button.pack(side="bottom")


code_text = tk.Text(root)
code_text.pack()

code_text.bind("<KeyRelease>", highlight)


root.mainloop()
