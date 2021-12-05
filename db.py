from tkinter import Tk, Label, Entry, Button, LabelFrame
import sqlite3

root = Tk()
root.title('Task Manager')
root.geometry('410x300')

conn = sqlite3.connect('todo.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

def addTodo():
    todo = e.get()
    c.execute('INSERT INTO todo (description, completed) VALUES (?, ?)', (todo, False))
    conn.commit()
    e.delete(0, 'end')


lb = Label(root, text='Task')
lb.grid(row=0, column=0)

e = Entry(root, width=40)
e.focus()
e.grid(row=0, column=1)

btn = Button(root, text='Add', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='My tasks', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

root.bind('<Return>', lambda _: addTodo())
root.mainloop()
