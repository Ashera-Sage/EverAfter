# EverAfter – Wedding Events & RSVP Management System

## Project Overview

EverAfter is a Flask-based Wedding Events and RSVP Management System developed as a mini project. It helps administrators create and manage wedding events while allowing guests to view wedding invitations and submit their RSVP responses. The application uses JSON files for data storage instead of a database.

---

## Features

- Admin Login Authentication
- Create Wedding Events
- View All Weddings
- Edit Wedding Details
- Delete Wedding Events
- Wedding Invitation Page
- Guest RSVP Registration
- RSVP Attendee List
- Wedding Summary (Capacity & Registration Status)
- Upcoming and Completed Wedding Classification
- Flash Messages
- Responsive User Interface
- File Handling using JSON
- Date Handling
- Exception Handling

---

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JSON
- Jinja2 Templates

---

## Project Structure

```
EverAfter/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── weddings.json
│   └── rsvps.json
│
├── static/
│   ├── css/
│   └── images/
│
└── templates/
    ├── index.html
    ├── admin_login.html
    ├── dashboard.html
    ├── create_wedding.html
    ├── view_weddings.html
    ├── edit.html
    ├── invitation.html
    ├── rsvp.html
    ├── rsvp_list.html
    └── summary.html
```

---

## Modules

### Admin Module
- Secure Admin Login
- Dashboard
- Create, Edit and Delete Wedding Events
- View RSVP List
- View Wedding Summary

### Guest Module
- View Wedding Invitation
- Submit RSVP Response

---

## Data Storage

The application stores all data using JSON files.

- **weddings.json** – Stores wedding details.
- **rsvps.json** – Stores guest RSVP responses.

---

## How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

### Step 3: Open the Browser

```
http://127.0.0.1:5000
```

## Screenshots

### Home Page

![Home](screenshots/Homepage.png)

---

### Admin Login

![Admin Login](screenshots/Admin_login.png)

---

### Dashboard

![Dashboard](screenshots/Admin_Dashboard.png)

---

### Create Wedding

![Create Wedding](screenshots/Wedding_Form.png)

---

### Wedding Invitation

![Invitation](screenshots/InvitationCard.png)

---

### RSVP Form

![RSVP Form](screenshots/RSVP_Form.png)

---

### RSVP List

![RSVP List](screenshots/Rsvp_List.png)

---

### Summary

![Summary](screenshots/Summary.png)

---

## Admin Login

**Username:** `admin`

**Password:** `Admin@123`

---

## Project Highlights

- Flask Web Framework
- CRUD Operations
- JSON File Handling
- Date Handling
- Exception Handling
- Responsive User Interface
- RSVP Management
- Wedding Capacity Summary

---

## Future Enhancements

- Email Invitation System
- Database Integration (MySQL/SQLite)
- QR Code Invitations
- Photo Gallery
- Online Gift Registry
- Guest Search and Filter

---

## Developed By

**Ashera Sage**