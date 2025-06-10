def main_menu():
    while True:
        print("\n📚 Study Agent Menu:")
        print("1. Manage To-Do / Reminders")
        print("2. Track DSA Progress")
        print("3. Generate Weekly Test")
        print("4. Practice Aptitude")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("📋 Task Manager (Coming soon)")
        elif choice == '2':
            print("📊 DSA Tracker (Coming soon)")
        elif choice == '3':
            print("🧪 Test Generator (Coming soon)")
        elif choice == '4':
            print("🧠 Aptitude Trainer (Coming soon)")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")