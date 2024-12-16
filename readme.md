## Overview

**Project Title**: Homework Tracker

**Project Description**:  
Homework Tracker is a software application that allows users to manage homework assignments for various classes. Users can create an account, sign in, add classes, assign tasks to specific classes, and manage them within a structured cloud-based database using Firebase.

**Project Goals**:  
The primary goal is to provide a simple and efficient way for users to organize and track their homework tasks, ensuring productivity and time management.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Clone the repository to your local machine.
2. Install the necessary dependencies, including the Firebase Admin SDK, using `pip install firebase-admin`.
3. Replace the Firebase credentials file (`homeworktracker-3e466-firebase-adminsdk-s34hm-b3cfc90953.json`) with your own Firebase project credentials.
4. Run the script using `python <filename>.py`.

Instructions for using the software:

1. Launch the software and choose either "Create Account" or "Sign In."
2. After signing in, manage classes by adding, selecting, or removing them.
3. Add tasks to selected classes and manage existing tasks as needed.

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.8 or later
* Firebase Admin SDK (`firebase-admin`)
* Firestore database setup in Google Firebase Console

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Firebase Documentation](https://firebase.google.com/docs)
* [Python Firebase Admin SDK Guide](https://firebase.google.com/docs/admin/setup)
* [Google Firestore Overview](https://firebase.google.com/docs/firestore)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add a function to update tasks and their statuses.
* [ ] Implement real-time notifications for task updates.
* [ ] Enhance error handling and input validation.
* [ ] Add a user-friendly graphical interface (GUI).
* [ ] Expand user authentication with password recovery and multi-factor authentication.
