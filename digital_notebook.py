import json
from pathlib import Path
from datetime import datetime
import textwrap

class Note:
    def __init__(self, title, content, timestamp = None):
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now()

class Notebook:
    def __init__(self):
        self.notes = []
        self.load_notes()
    
    def load_notes(self):
        path = Path('D:/Desktop/Notebook.json')
        if not path.exists():
            return
        with open(path, 'r') as file:
            contents = json.load(file)
            for content in contents:
                note = Note(content['Title'], content['Content'], datetime.fromisoformat(content['Timestamp']) )
                self.notes.append(note) 


    def save_notes(self):
        path = Path('D:/Desktop/Notebook.json')
        notebook = []
        for note in  self.notes:
            notebook.append({'Title':note.title,
                             'Content':note.content,
                             'Timestamp':note.timestamp.isoformat()})    
        with open(path, 'w') as file:
            json.dump(notebook, file, indent=2 )

    def add_notes(self):
        title = input("Enter title: ")
        content = input("Enter content: ")
        self.create_notes(title, content)

    def create_notes(self, title, content):
        if title.strip():
            note = Note(title, content)
            self.notes.append(note)
            self.save_notes()
            print("✅ Note saved!")
        else:
            print("❌ Title can not be empty")


    def view_notes(self):
        if self.notes:
            print("___________________")
            print("--Saved Notes--")
            for note in self.notes:
                print(f"\nTitle: {note.title}")
                """wrapping the text to make it appear more refined"""
                wrapped_content = textwrap.fill(note.content, width = 60)
                print(f"-{wrapped_content}")
                print(f"last update: {note.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print("___________________")
        else:
            print('No notes found')

    def view_by_title(self):
        keyword = input("Enter the title to search: ").lower()
        found = False
        for note in self.notes:
            if note.title.lower() == keyword:
                wrapped_content = textwrap.fill(note.content, width=60)
                print(f"-{wrapped_content}")
                found = True
        if not found:
             print(f"{keyword.title()} not found")
    
    def update_note(self, note, new_title = None, new_content = None):
        if new_title:
            note.title = new_title
        if new_content:
            note.content = new_content
    
    def prompt_edit_note(self, note):
        while True:
            choice = input("Enter t to edit title and n for note(q to go back): ").lower()
            if choice == 't':
                new_title = input(f'Title: ' )
                if new_title.strip():
                    self.update_note(note, new_title=new_title)
                else:
                    print("❎Title can not be empty")
            elif choice == 'n':
                new_content = input(f'Content: ' )
                self.update_note(note, new_content=new_content)
            elif choice == 'q': 
                break
            else:
                print('invalid input')

    def edit_notes(self):
        print("----select the note to edit----")
        select = input("Title: ")
        for note in self.notes:
            if note.title.lower() == select.lower():
                self.prompt_edit_note(note)
                note.timestamp = datetime.now()
                self.save_notes()
                print('\n✅ Note successfully updated')
                return
        print(f"{select.title()} not found")

    def delete_notes(self):
        print('----select the note to delete----')
        select = input('Title: ')
        for idx, note in enumerate(self.notes):
            if note.title.lower() == select.lower():
                del self.notes[idx]
                print(f'{select} successfully deleted! ✅')
                self.save_notes()
                return
        print(f"{select.title()} not found")

       
    def run(self):
        while True:
            print("\n----------------DIGITAL NOTEBOOK---------------")
            print("\nSelect Your Choice:")
            print("1. Add Note 📝")
            print("2. View Available Notes 🧾")
            print("3. Search Notes 🔍")         
            print("4. Edit Note ✒️")
            print("5. Delete Note 🚮")
            print("6. Exit 🚪")
            print("\n------------------------------------------------")
            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("please enter an integer only")
            else:
                match choice:
                    case 1:
                        self.add_notes()
                    case 2:
                        self.view_notes()
                    case 3:
                        self.view_by_title()
                    case 4:
                        self.edit_notes()
                    case 5:
                        self.delete_notes()
                    case 6:
                        break
                    case _:
                        print("invalid input, try again")

                ask = input("\nGo back to menu?(y/n): ").lower()
                if ask != "y":
                    break
note_1 = Notebook()
note_1.run()
