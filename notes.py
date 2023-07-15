import json
from datetime import datetime

class Note:
    def __init__(self, title, body):
        self.id = id(self)
        self.title = title
        self.body = body
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def update(self, title=None, body=None):
        if title:
            self.title = title
        if body:
            self.body = body
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class NotesApplication:
    def __init__(self, file_name='notes.json'):
        self.file_name = file_name
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
                for note_data in data:
                    note = Note(note_data['title'], note_data['body'])
                    note.id = note_data['id']
                    note.created_at = note_data['created_at']
                    note.updated_at = note_data['updated_at']
                    self.notes.append(note)
        except FileNotFoundError:
            pass

    def save_notes(self):
        data = [note.to_dict() for note in self.notes]
        with open(self.file_name, 'w') as f:
            json.dump(data, f)

    def create_note(self, title, body):
        note = Note(title, body)
        self.notes.append(note)
        self.save_notes()

    def list_notes(self):
        for note in self.notes:
            print(f'ID: {note.id}')
            print(f'Title: {note.title}')
            print(f'Body: {note.body}')
            print(f'Created at: {note.created_at}')
            print(f'Updated at: {note.updated_at}')
            print('---')

    def view_note(self, id):
        note = next((note for note in self.notes if note.id == id), None)
        if not note:
            print('Note not found')
            return
        print(f'ID: {note.id}')
        print(f'Title: {note.title}')
        print(f'Body: {note.body}')
        print(f'Created at: {note.created_at}')
        print(f'Updated at: {note.updated_at}')

    def update_note(self, id, title=None, body=None):
        note = next((note for note in self.notes if note.id == id), None)
        if not note:
            print('Note not found')
            return
        note.update(title=title, body=body)
        self.save_notes()

    def delete_note(self, id):
        note = next((note for note in self.notes if note.id == id), None)
        if not note:
            print('Note not found')
            return
        self.notes.remove(note)
        self.save_notes()

def main():
    app = NotesApplication()
    while True:
        command = input('Enter command (new/list/view/update/delete/quit): ')
        if command == 'new':
            title = input('Enter title: ')
            body = input('Enter body: ')
            app.create_note(title, body)
        elif command == 'list':
            app.list_notes()
        elif command == 'view':
            id = int(input('Enter ID: '))
            app.view_note(id)
        elif command == 'update':
            id = int(input('Enter ID: '))
            title = input('Enter new title (leave empty to keep current): ')
            body = input('Enter new body (leave empty to keep current): ')
            app.update_note(id, title=title or None, body=body or None)
        elif command == 'delete':
            id = int(input('Enter ID: '))
            app.delete_note(id)
        elif command == 'quit':
            break

if __name__ == '__main__':
    main()