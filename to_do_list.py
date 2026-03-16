# 📋 2. To-Do List with Prioritization
# A console-based task tracker where tasks have deadlines and priorities.
# You’ll Practice:
# - Classes for tasks with attributes (like title, due date, status)
# - Sorting and filtering
# - File I/O (save/load tasks)
# Stretch goal:
# - Export tasks to CSV or show task summaries using simple ASCII tables
from pathlib import Path
from datetime import datetime, time
import json
import sys

class TaskInfo:
    def __init__(self, title, description, due_date, priority, status = 'Pending',
                  creation_date = None):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.creation_date = creation_date if creation_date else datetime.now()
        

class CreateTask:

    priority_map = {1:"High",
                    2:"Medium",
                    3:"Low"}
    
    def __init__(self):
        self.tasks = []
        self.path = Path('D:/Desktop/Tasks.json')
        self.load_task()
    
    def get_valid_date(self):
        while True:
            ask_date_time = input("Due Date and Time (press 'q' to quit): ")
            if ask_date_time.lower().strip() == 'q':
                sys.exit()
            try:
                f_date = datetime.strptime(ask_date_time, "%Y-%m-%d %H:%M")
            except ValueError:
                pass
            else:
                if datetime.now() < f_date:
                    return f_date
                else:
                    print("You Can't Select An Already Passed Date")
                    continue
            try:
                ask_date = datetime.strptime(ask_date_time, "%Y-%m-%d")
                f_date = datetime.combine(ask_date, time.max.replace(microsecond=0))
            except ValueError:
                print("Invalid Date, please use 'YYYY-MM-DD H:M' or 'YYYY-MM-DD' format")
            else:
                if datetime.now() < f_date:
                    return f_date
                else:
                    print("You Can't Select An Already Passed Date")
            
    def get_valid_priority(self):
        while True:
            try:
                priority = int(input("Priority: "))
            except ValueError:
                print('Choose Valid priority (1-High, 2-Medium, 3-Low)')
                print("press any random number to select default")
                print("Default Priority: High")
            else:
                return priority
            
    def add_task(self):
        check = self.check_ovedue()
        if check:
            print("\nWarning! There are Tasks overdue!\n")
            ask = input("would you still like to add task(y/n): ").lower().strip()
            if ask != 'y':
                return
        title = input("\nTitle: ")
        description = input("Description: ")
        date = self.get_valid_date()
        get_priority = self.get_valid_priority()
        priority = CreateTask.priority_map.get(get_priority, "High")
        if get_priority not in CreateTask.priority_map:
            print("Invalid Priority Selected. Defaulting to High")
        task = TaskInfo(title, description, date, priority)
        self.tasks.append(task)
        self.save_task()
        print("\nTask successfully created!\n")
    
    def view_task(self):
        if self.tasks:  
            print("\n----Current Tasks----")
            for task in self.tasks: 
                print(f"\nTitle: {task.title}")
                print(f"Description: {task.description}")
                print(f"Due date: {task.due_date}")
                print(f"Priority: {task.priority}")
                print(f"Status: {task.status}")
                print("___________________")
                print(f"Created at {task.creation_date.strftime('%Y-%m-%d %H:%M')}")
                self.show_overdue(task.due_date, task.status)
            print("\n-------------------")
        else:
            print("\nNo Current Tasks!\n")
    
    def prompt_edit_task(self, edit):
        new_edit = input(f"Enter new {edit}: ")
        while not new_edit:
            print(f"\n{edit} can not be empty.")
            new_edit = input(f"Enter new {edit}: ")
        return new_edit

    def edit_task(self):
        valid_edit = ['title', 'description', 'due date', 'priority']
        found = True
        if self.tasks:
            ask_title = input("Title: ")
            for task in self.tasks:
                if ask_title.strip().lower() == task.title.lower():
                    found = False
                    while True:
                        choice = input("Select the part to edit(q to quit): ").strip().lower()
                        if choice == 'q':
                            break
                        elif choice in valid_edit:
                            if choice == "title":
                                task.title = self.prompt_edit_task("title")
                            elif choice == "description":
                                task.description = self.prompt_edit_task("description")
                            elif choice == "due date":
                                task.due_date = self.get_valid_date()
                            elif choice == "priority":
                                get_priority = self.get_valid_priority()
                                task.priority = CreateTask.priority_map.get(get_priority, "High")
                                if get_priority not in CreateTask.priority_map:
                                    print("Invalid Priority Selected. Defaulting to High")
                            self.save_task()   
                            print(f"{choice} successfully Edited!")
                        else:
                            print(f"{choice} is invalid, please select a valid input."
                                  "Valid - ('title', 'description', 'due date', 'priority')")
            if found:
                print(f"\n{ask_title} not found")    
        else:
            print("\nNo Task Available!")        


    def show_prt_task(self, prt):
        if prt:
                for task in prt:
                    print(f"\nTitle: {task.title}")
                    print(f"Description: {task.description}")
                    print(f"Due date: {task.due_date}")
                    print(f"Priority: {task.priority}")
                    print(f"Status: {task.status}")
                    print("___________________")
                    print(f"Created at {task.creation_date.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("\n-No Task Available")
            print("____________________________")
         
    def group_by_priority(self):
        high_prt = []
        medium_prt = []
        low_prt = []
        if self.tasks:
            for task in self.tasks:
                if task.priority == "High":
                    high_prt.append(task)
                elif task.priority == "Medium":
                    medium_prt.append(task)
                elif task.priority == "Low":
                    low_prt.append(task)
            print("\n______Priority - High______")
            self.show_prt_task(high_prt)

            print("\n______Priority - Medium______")
            self.show_prt_task(medium_prt)

            print("\n______Priority - Low______")
            self.show_prt_task(low_prt)

        else:
            print("\nNo Available task to Sort!")

    def sort_by_priority(self):
        if self.tasks:
            pr_map = {"High":1, "Medium":2, "Low":3}
            self.tasks = sorted(self.tasks, key = lambda task: pr_map[task.priority])
            self.save_task()
            print("\nTasks Successfully Sorted by Priority")
        else:
            print("\nNo Task Available to Sort")
            
    def mark_task(self):
        ask_title = input("Title: ").strip().lower()
        for task in self.tasks:
            if ask_title == task.title.lower():
                task.status = "Completed"
                self.save_task()
                print(f"\nTask '{ask_title}' marked as completed!\n")
                return
        print("\nTask not found!\n")
    
    def show_overdue(self, overdue, status):
        if datetime.now() > overdue and status != "Completed":
            print("❗PAST DUE DATE")

    def check_ovedue(self):
        over_due = []
        for task in self.tasks:
            if datetime.now() > task.due_date and task.status != "Completed":
                over_due.append(task)
                return over_due

    def show_overdue_task(self):
        over_due = self.check_ovedue()
        if over_due:
            print("\n______Overdue Tasks______")
            self.show_prt_task(over_due)
        else:
            print("\n No Overdue Tasks Found")
    
    def delete_task(self):
        if self.tasks:
            title_to_delete = input("\nTitle: ")
            for task in self.tasks:
                if task.title.lower() == title_to_delete.lower():
                    self.tasks.remove(task)
                    print("\nTask Successfully Deleted!")
                    self.save_task()
                    return
            print(f"\nTask '{title_to_delete}' not found!")
        else:
            print("\nNo Available Task to delete!")
   
    def save_task(self):
        tasks = []
        for task in self.tasks:
            tasks.append({
                "title":task.title,
                "description":task.description,
                "due Date":task.due_date.strftime('%Y-%m-%d %H:%M'),
                "priority":task.priority,
                "status":task.status,
                "created at":task.creation_date.strftime('%Y-%m-%d %H:%M')
            })
        path = self.path
        with path.open('w') as file:
            json.dump(tasks, file, indent = 2)
    
    def load_task(self):
        path = self.path
        if not path.exists():
            return
        else:
            with path.open('r') as file:
                contents = json.load(file)
            for content in contents:
                task = TaskInfo(content["title"], content["description"],
                                 datetime.strptime(content["due Date"],
                                                   "%Y-%m-%d %H:%M"), content["priority"], 
                                 content["status"], 
                                 datetime.strptime(content["created at"], "%Y-%m-%d %H:%M"))
                self.tasks.append(task)
    
    def clear_task(self):
        if self.tasks:
            check = input("\nAre You Sure You Want To Delete All Tasks?(y/n): ").strip().lower()
            if check == 'y':
                self.tasks = []
                self.save_task()
                print("\nAll Tasks Successfully Deleted!")
            else:
                return
        else:
            print("\nNo Available Task to delete!")
              
    def run(self):
        print("\n-------------- TO-DO LIST PROGRAM -------------\n")
        while True:
            print("\n1. Add Task")
            print("2. Edit Task")
            print("3. View Tasks")
            print("4. View Tasks by Priority")
            print("5. Sort Tasks by Priority")
            print("6. Show Overdue Tasks")
            print("7. Mark Completed Task")
            print("8. Delete Task")
            print("9. Delete All Tasks")
            print("0. Exit")
            try: 
                option = int(input("\nSelect Your Choice: "))
            except ValueError:
                print("\nPlease enter an integer only\n")
            else:
                match option:
                    case 1:
                        self.add_task()
                    case 2:
                        self.edit_task()
                    case 3:
                        self.view_task()
                    case 4:
                        self.group_by_priority()
                    case 5:
                        self.sort_by_priority()
                    case 6:
                        self.show_overdue_task()
                    case 7:
                        self.mark_task()
                    case 8:
                        self.delete_task()
                    case 9:
                        self.clear_task()
                    case 0:
                        break
                    case _:
                        print("Invalid input, try again!")
                        continue
                ask = input("\nPress enter to go back to menu, Q to exit: ")
                if ask.lower() == 'q':
                    break

task = CreateTask()
task.run()
