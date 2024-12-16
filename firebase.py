from datetime import datetime
import firebase_admin
from firebase_admin import firestore, credentials, auth

# Application Default credentials are automatically created.
cred = credentials.Certificate("homeworktracker-3e466-firebase-adminsdk-s34hm-b3cfc90953.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def sign_in():
    email = input("Enter email: ")
    password = input("Enter password: ")

    try:
        user = auth.get_user_by_email(email)
        print(f"Welcome back, {email}")
        return email
    except Exception as e:
        print(f"Sign-in failed: {e}")
        return None

def create_account():
    try:
        email = input("Enter email: ")
        password = input("Enter password: ")

        # Create new user
        user = auth.create_user(
            email=email,
            password=password
        )
        print(F"Successfully created user: {user.uid}")

        user_data = {
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        db.collection('users').document(email).set(user_data)
        print(f"User added to Firestore: {email}")

    except Exception as e:
        print(F"Error creating user: {e}")

def manage_classes(email):
    user_classes_ref = db.collection('users').document(email).collection('classes')
    classes = [doc.id for doc in user_classes_ref.stream()]

    print("\nYour classes:")
    if not classes:
        print("No classes found.")
    else:
        for i, cls in enumerate(classes, 1):
            print(f"{i}. {cls}")
    print(f"{len(classes) + 1}. Add a new class")
    print(f"{len(classes) + 2}. Remove a class")

    choice = int(input("Select an option: "))
    if choice == len(classes) + 1:
        class_name = input("Enter the new class name: ")
        add_class(email, class_name)
        return class_name
    elif choice == len(classes) + 2:
        class_name = input("Enter the class name to remove: ")
        remove_class(email, class_name)
        return None
    elif 1 <= choice <= len(classes):
        return classes[choice - 1]
    else:
        print("Invalid option. Try again.")
        return manage_classes(email)


def add_class(email, class_name):
    try:
        class_ref = db.collection('users').document(email).collection('classes').document(class_name)
        class_ref.set({'created_at': datetime.now().isoformat()})
        print(f"Class '{class_name}' added successfully.")
    except Exception as e:
        print(f"Error adding class: {e}")

def remove_class(email, class_name):
    try:
        class_ref = db.collection('users').document(email).collection('classes').document(class_name)

        # Get all subcollections in the class document
        subcollections = class_ref.collections()
        for subcollection in subcollections:
            # Iterate through all documents in each subcollection and delete them
            docs = subcollection.stream()
            for doc in docs:
                subcollection.document(doc.id).delete()
            print(f"Subcollection '{subcollection.id}' deleted.")

        # Finally, delete the class document itself
        class_ref.delete()
        print(f"Class '{class_name}' and all its subcollections removed successfully.")
    except Exception as e:
        print(f"Error removing class '{class_name}': {e}")

def add_assignment(email, class_name):
    try:
        assignment_name = input("Enter the assignment name: ")
        assignment_ref = (
            db.collection('users')
            .document(email)
            .collection('classes')
            .document(class_name)
            .collection('assignments')
            .document(assignment_name)
        )
        assignment_ref.set({
            'task_name': assignment_name,
            'created_at': datetime.now().isoformat()
        })
        print(f"Assignment '{assignment_name}' added to class '{class_name}'.")
    except Exception as e:
        print(f"Error adding assignment: {e}")

def remove_assignment(email, class_name):
    try:
        assignment_name = input("Enter the assignment name to remove: ")
        assignment_ref = (
            db.collection('users')
            .document(email)
            .collection('classes')
            .document(class_name)
            .collection('assignments')
            .document(assignment_name)
        )
        assignment_ref.delete()
        print(f"Assignment '{assignment_name}' removed successfully.")
    except Exception as e:
        print(f"Error removing assignment: {e}")

def view_tasks(email, class_name):
    try:
        tasks_ref = (
            db.collection('users')
            .document(email)
            .collection('classes')
            .document(class_name)
            .collection('assignments')
        )
        tasks = tasks_ref.stream()

        print(f"\nTasks for class '{class_name}':")
        task_list = []
        for task in tasks:
            task_data = task.to_dict()
            task_name = task.id
            created_at = task_data.get('created_at', 'Unknown date')
            task_list.append((task_name, created_at))

        if task_list:
            for idx, (task_name, created_at) in enumerate(task_list, start=1):
                print(f"{idx}. Task Name: {task_name}\n   Created At: {created_at}\n")
        else:
            print(f"No tasks found for class '{class_name}'.")
    except Exception as e:
        print(f"Error viewing tasks: {e}")

if __name__ == "__main__":
    while True:
        print("\nWelcome to Homework Tracker!")
        print("1. Create Account")
        print("2. Sign In")
        print("3. Exit")

        option = input("Choose an option: ")
        if option == "1":
            create_account()
        elif option == "2":
            email = sign_in()
            if email:
                while True:
                    print("\nWhat would you like to do?")
                    print("1. Add assignment")
                    print("2. Remove assignment")
                    print("3. View tasks")
                    print("4. Log Out")

                    action = input("Choose an option: ")

                    if action == "1":
                        class_name = manage_classes(email)
                        if class_name:
                            add_assignment(email, class_name)
                    elif action == "2":
                        class_name = manage_classes(email)
                        if class_name:
                            remove_assignment(email, class_name)
                    elif action == "3":
                        class_name = manage_classes(email)
                        if class_name:
                            view_tasks(email, class_name)
                    elif action == "4":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again.")
        elif option == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
