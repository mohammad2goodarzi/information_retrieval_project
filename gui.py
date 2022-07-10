from tkinter import *

from search import process_query


def open_document(doc_id):
    destroy_children_widget(top)
    file = open(f'txtfiles/{doc_id}.txt', encoding="utf-8")
    content = file.readlines()
    text = Text(top, background=top.cget('background'), relief='flat', height=10)
    text.insert('1.0', content)
    text.configure(state='disabled')
    scroll = Scrollbar(top, orient='vertical', command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    scroll.pack(side='right', fill='y')
    text.pack(side='left', fill='both', expand=True)


def onclick(event):
    doc_id = event.widget.cget('text')
    open_document(doc_id)


def func():
    destroy_children_widget(result_frame)
    query = entry.get()
    query = query.replace(chr(1610), chr(1740))
    results = process_query(query)
    for result in results:
        the_label = Label(result_frame, text=str(result))
        the_label.bind('<Button>', onclick)
        the_label.pack()


def destroy_children_widget(widget):
    if widget.children:
        for key in widget.children.copy():
            widget.children[key].destroy()


root = Tk()
root.title("The Search Engine")
top = Toplevel(root)
frame = LabelFrame(root)
frame.pack()
label = Label(frame, text="Enter the word: ")
label.grid(row=0, column=0)
entry = Entry(frame, width=50, borderwidth=5)
entry.grid(row=0, column=1)
button = Button(frame, text='Search', command=func)
button.grid(row=1, column=0, columnspan=2)
result_frame = LabelFrame(frame)
result_frame.grid(row=2, column=0, columnspan=2)


root.mainloop()
