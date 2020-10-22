import tkinter as tk
import calculate as calc
#Window object
window = tk.Tk()
#Calculator object
solver = calc.Calculate()

#######################
## Widgets
#######################
top_label = tk.Label(text="Enter function below")
function_entry = tk.Entry()
eval_button = tk.Button(text="Eval")
result_label = tk.Label()

#n=top, e=right, s=bot, w=left
top_label.grid(row=0, column=0, sticky="n")
function_entry.grid(row=1,column=0, padx=(10,10))
eval_button.grid(row=1,column=1, sticky="n")
result_label.grid(row=2,column=0, sticky="n")

#######################
## Event Handlers
#######################
def handle_eval(event):
    result_label["text"] = solver.eval(function_entry.get())
    solver.clear()

#######################
## Event Binds
#######################
eval_button.bind("<Button-1>", handle_eval)

#######################
## Window Specs
#######################
#window.columnconfigure([0,1,2], weight=)
#window.rowconfigure([0, 1], weight=1)
window.title("Sym - A Symbolic Calculator")
window.iconbitmap(default='icons/title.ico')
window.minsize(500,500)
window.mainloop()