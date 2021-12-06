from tkinter import Tk, Label, Entry, Button, LabelFrame, Checkbutton
import sqlite3

root = Tk()
root.title('Task Manager')
root.geometry('390x370')

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

# Currying
def complete(id):
    def _complete():
        todo = c.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?', (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def remove_todo(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id,))
        conn.commit()
        render_todos()
    return _remove()

def render_todos():
    rows = c.execute('SELECT * FROM todo').fetchall()
    for widget in frame.winfo_children():
        widget.destroy()

    # print(rows)
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]

        color = '#00A623' if completed else '#EF4529'
        checkbutton = Checkbutton(frame, text=description, fg=color, width=40, anchor='w', command=complete(id))
        checkbutton.grid(row=i, column=0, sticky='w')
        checkbutton.select() if completed else checkbutton.deselect()
        btn = Button(frame, text='Delete', command=lambda: remove_todo(id))
        btn.grid(row=i, column=1)


def addTodo():
    todo = e.get()
    if todo:
        c.execute('INSERT INTO todo (description, completed) VALUES (?, ?)', (todo, False))
        conn.commit()
        e.delete(0, 'end')
        render_todos()
    else: pass


lb = Label(root, text='Task')
lb.grid(row=0, column=0)

e = Entry(root, width=40)
e.focus()
e.grid(row=0, column=1)

btn = Button(root, text='Add', command=addTodo)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='My tasks', borderwidth=0, padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

root.bind('<Return>', lambda _: addTodo())
render_todos()
root.mainloop()
