# feature to add -- reset expense tracker(deletes the json and resets the app)

from datetime import date, datetime
from pathlib import Path
import json

class ExpenseAttribute:

    def __init__(self, e_date, category, amount, note):
        self.e_date = e_date
        self.category = category
        self.amount = amount
        self.note = note
    
    def to_dict(self):
        return {
            'date':self.e_date.isoformat(),
            'category':self.category,
            'amount':self.amount,
            'note':self.note
            }
    
    @staticmethod
    def from_dict(data):
        return ExpenseAttribute(
            date.fromisoformat(data['date']),
            data['category'],
            data['amount'],
            data.get('note')
            )

class Expense:
    monthly_budget = 0
    expenses = []


    def __init__(self):
        self.path = Path("D:/Desktop/Expenses.json")
        self.load_expense()

    @classmethod
    def initialize_budget(cls):
        budget_path = Path("D:/Desktop/Budget.json")
        while True:
            budget = input("Enter your budget of the month: ")
            try:
                budget = float(budget)
                if budget < 0:
                    print("Budget can't be negative!")
                    continue
                break
            except ValueError:
                print("Invalid budget input, please enter a number!!")
        cls.monthly_budget = budget
        with budget_path.open('w', encoding='utf-8') as file:
            json.dump({'monthly_budget':cls.monthly_budget}, file)
        print(f"\nBudget succesfully set to ₹{cls.monthly_budget}")
        
    @classmethod
    def load_or_set_budget(cls):
        budget_path = Path("D:/Desktop/Budget.json")
        if budget_path.exists():
            with budget_path.open('r', encoding='utf-8') as file:
                content = json.load(file)
                try:
                    cls.monthly_budget = content['monthly_budget']
                except (KeyError, TypeError, ValueError):
                    print("⚠️ Budget file is invalid. Resetting budget...")
                    cls.set_initial_budget()
        else: cls.initialize_budget()

    @classmethod
    def check_budget(cls, amount):
        current_spent = sum(exp.amount for exp in cls.expenses)
        if current_spent + amount >= cls.monthly_budget:
            print(f'\nWarning❗ ₹{amount} exceeds your monthly budget limit!!')
            print(f"Current Budget: ₹{cls.monthly_budget}")
            print(f"Remaining Budget: ₹{cls.monthly_budget-current_spent}")
            confirm = input("\nWould you still like to add Expense?(y/n):").lower().strip()
            if confirm == 'y':
                return False
            return True
        return False
    
    @classmethod
    def manage_budget(cls):
        print("\n1. View Current Budget")
        print("2. Change Current Budget")
        while True:
            choice = input('Select(1-2): ')
            try:
                choice = int(choice)
                break
            except ValueError:
                print("\nInvalid, please enter number only!!")
        if choice == 1: print(f"Current Budget: ₹{cls.monthly_budget}")
        elif choice == 2: cls.initialize_budget()

    def add_expense(self):
        while True:
                amount = input("Amount: ").strip()
                try:
                    amount = float(amount)
                    if float(amount) < 0:
                        print("\nAmount can't be negative!")
                        continue
                    break
                except ValueError:print("\nInvalid, please enter a number only❗")
        if self.check_budget(amount):
            return
        ask_date = input("\nAdd date?(y/n): ").strip().lower()
        if ask_date == 'y':
            while True:
                raw_date = input("Date: ")
                try: e_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
                except ValueError:print(f"invalid date format please use"
                          f" 'YYYY-MM-DD' format, example-{date.today()}!!")
                else:break
        else:
            print("\nDate not added, "
                  f"it will be defaulted to current date/-{date.today()}")
            e_date = date.today()
        category = input("Category: ")
        ask_note = input("Add note?(y/n): ").strip().lower()
        if ask_note == 'y': note = input("Add Note: ")
        else: note = ''
        expense = ExpenseAttribute(e_date, category, float(amount), note)
        Expense.expenses.append(expense)
        self.save_expense()
        print("\nExpense successfully added ✅")
    
    def save_expense(self):
        path = self.path
        with path.open('w', encoding='utf-8') as file:
            json.dump([e.to_dict() for e in Expense.expenses], file, indent=2)
    
    def load_expense(self):
        path = self.path
        if not path.is_file():
            return
        else:
            with path.open('r', encoding='utf-8') as file:
                contents = json.load(file)
            for content in contents:
                Expense.expenses.append(ExpenseAttribute.from_dict(content))

    def view_expense(self):
        if Expense.expenses:
            print("\n------------- Available Expenses -------------\n")
            for idx, exp in enumerate(Expense.expenses, start=1):
                print(f"Expense {idx}/-  ₹{exp.amount} - {exp.category}"
                      f" on {exp.e_date} ({exp.note or 'No note added!'})")
            print("\n----------------------------------------------")
        else:
            print("\nNo Current Expense❗")

    def continue_update(self, ask):
        to_continue = input("\nContinue updating"
                    f" Expense {ask}?(y/n): ").strip().lower()
        return to_continue == 'y'
        
    def update_expense(self):
        if not Expense.expenses:
            print("\nNo Available Expense to update❗")
            return
        
        while True:
            ask = input("\nEnter the Expense no. to update: ")
            try:
                ask = int(ask)
                break
            except ValueError: print('\nPlease select a valid Expense no.❗')
        if not (ask >= 1 and ask <= len(self.expenses)):
            print(f"\nExpense no.{ask} doesn't exist❗")
            return 
        exp = Expense.expenses[ask - 1]
            
        while True:
            choice = input("\nEnter the field you"
                    " want to update(q to quit): ").lower().strip()
            if choice == 'q':break
            elif choice == 'date':
                while True:
                    collect = input('Enter new date: ')
                    try:
                        updated_date = datetime.strptime(collect, '%Y-%m-%d').date()
                        break
                    except ValueError:
                        print(f"invalid date format please use"
                            f" 'YYYY-MM-DD' format, example-{date.today()}!!")
                exp.e_date = updated_date
                self.save_expense()
                print(f"\n{choice} successfully updated ✅")
                if not self.continue_update(ask):return
            elif choice == 'category':
                updated_category = input('Enter new category: ')
                exp.category = updated_category
                self.save_expense()
                print(f"\n{choice} successfully updated ✅")
                if not self.continue_update(ask):return
            elif choice == 'amount':
                while True:
                    updated_amount = input('Enter new amount: ')
                    try:
                        updated_amount = float(updated_amount)
                        if float(updated_amount) < 0:
                            print("Amount can't be negative")
                            continue
                        break
                    except ValueError: print("\nInvalid amount, "
                                             "please enter amount in numbers❗")
                exp.amount = updated_amount
                self.save_expense()
                print(f"\n{choice} successfully updated ✅")
                if not self.continue_update(ask):return
            elif choice == 'note':
                updated_note = input('Enter Note: ')
                exp.note = updated_note
                self.save_expense()
                print(f"\n{choice} successfully updated ✅")
                if not self.continue_update(ask):return
            else: print(f"\n{choice} is not a valid field!!")
        
    def delete_expense(self):
        if not Expense.expenses:
            print("\nNo Available Expense to delete❗")
            return
        while True:
            ask = input("\nEnter the Expense no. you want to delete: ")
            try:
                ask = int(ask)
                break
            except ValueError: print('\nPlease select a valid Expense no.❗')
        if not (ask >= 1 and ask <= len(Expense.expenses)):
            print(f"\nExpense no.{ask} doesn't exist❗")
            return 
        confirm = input("\nAre you sure you want to delete"
                            f"Expense '{ask}'?(y/n): ").strip().lower()
        if confirm != 'y':return
        exp = Expense.expenses[ask - 1]
        Expense.expenses.remove(exp)
        self.save_expense()
        print(f"\nExpense '{ask}' successfully deleted ✅")
                
    def run(self):
        print("************* PYTHON EXPENSE TRACKER ***************")
        self.load_or_set_budget()
        while True:
            print("\n1. Add Expense")
            print("2. View Expense")
            print("3. Update Expense")
            print("4. Delete Expense")
            print("5. Manage Budget")
            print("6. Exit")
            try:
                ask = int(input("\nSelect: "))
            except ValueError:
                print('\nPlease select a valid choice❗')
                continue
            match ask:
                case 1:
                    self.add_expense()
                case 2:
                    self.view_expense()
                case 3:
                    self.update_expense()
                case 4:
                    self.delete_expense()
                case 5:
                    self.manage_budget()
                case 6:
                    break
                case _:
                    print("\nInvalid input!!")

exp = Expense()
exp.run()
