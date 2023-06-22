import uuid
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Note class to represent each note
class Note:
    def __init__(self, title, content):
        self.note_id = str(uuid.uuid4())  # Generate a unique Note ID
        self.title = title
        self.content = content

# Linked list class to manage the notes
class NoteLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def prepend(self, note):
        new_node = NoteNode(note)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1

    def remove(self, note_id):
        if self.head is None:
            return

        if self.head.note.note_id == note_id:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return

        current = self.head
        while current.next is not None:
            if current.next.note.note_id == note_id:
                current.next = current.next.next
                if current.next is None:
                    self.tail = current
                self.size -= 1
                return
            current = current.next

    def get_notes(self):
        notes = []
        current = self.head
        while current is not None:
            notes.append(current.note)
            current = current.next
        return notes

class NoteNode:
    def __init__(self, note):
        self.note = note
        self.next = None

# instance of the linked list
note_list = NoteLinkedList()

# Route for the home page
@app.route('/')
def home():
    notes = note_list.get_notes()
    return render_template('index.html', notes=notes)

# Route for adding a new note
@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    note = Note(title, content)
    note_list.prepend(note)  # Adding the note at the beginning of the list
    return redirect('/')

# Route for deleting a note
@app.route('/delete/<note_id>')
def delete_note(note_id):
    note_list.remove(note_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
