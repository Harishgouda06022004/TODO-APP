import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account

# Initialize Firebase Admin SDK with your new credentials
cred = credentials.Certificate("/home/Harish/todoapp/todoapp-be603-firebase-adminsdk-ahg1a-7c156b8024.json")  # Path to your new JSON key file
firebase_admin.initialize_app(cred)

# Or initialize Firestore with custom credentials if not using Firebase Admin SDK
credentials = service_account.Credentials.from_service_account_file(
    '/home/Harish/todoapp/todoapp-be603-firebase-adminsdk-ahg1a-7c156b8024.json'  # Path to your new service account key
)

# Initialize the Firestore client with the new credentials
db = firestore.Client(credentials=credentials)

# Display menu
def show_menu():
    print("== To-Do List ==")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")
    print("Waiting for input...")

# View tasks from Firestore
def view_task():
    tasks = db.collection("tasks").stream()  # Fetch all tasks
    task_list = [(doc.id, doc.to_dict()["name"]) for doc in tasks]  # List of (id, name)

    if not task_list:
        print("No tasks available.")
    else:
        print("\nAvailable Tasks:")
        for i, (task_id, task_name) in enumerate(task_list, start=1):
            print(f"{i}. {task_name} (ID: {task_id})")
    return task_list

# Add a task to Firestore
def add_task():
    while True:
        task = input("Enter the task (or type 'cancel' to exit): ").strip()
        if not task:
            print("Please enter a valid task.")
        elif task.lower() == "cancel":
            print("Task addition canceled.")
            return
        else:
            db.collection("tasks").add({"name": task})  # Add task to Firestore
            print("Task added successfully.")
            return

# Remove a task by Firestore document ID
def remove_task():
    print("\nTasks available:")
    view_task()
    task_id = input("\nEnter the task ID to remove: ").strip()
    try:
        db.collection("tasks").document(task_id).delete()  # Remove task
        print("Task removed successfully.")
    except Exception as e:
        print(f"Error removing task: {e}. Ensure the Task ID is correct.")

# Main loop
def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice == '1':
            view_task()
        elif choice == '2':
            add_task()
        elif choice == '3':
            remove_task()
        elif choice == '4':
            print("Goodbye!")
            break  # This breaks the loop and ends the program
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
