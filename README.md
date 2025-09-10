Library Management System

A desktop application built with Python 3 and PyQt5 for managing books, members, and loan transactions in a library. The system uses a PostgreSQL database to ensure data integrity and persistence.

Features

    Book Management: Add, update, and delete book records.

    Member Management: Add, update, and delete member information.

    Loan Management: Check out and return books, with automated tracking of availability.

    Database Integration: Connects to a PostgreSQL database to store and retrieve data.

    User-friendly GUI: Intuitive graphical interface for easy interaction.

    Logging: All application actions and errors are logged to a file for easy debugging and monitoring.

Prerequisites

To run this application, you need to have the following installed on your system:

    Python 3.8+

    PostgreSQL

    Python Libraries: The required Python libraries are listed in requirements.txt.

Installation & Setup

Follow these steps to set up the project locally.

Step 1: Clone the repository

First, clone the project from GitHub to your local machine:
Bash

git clone https://github.com/YourUsername/repository-name.git
cd repository-name

Step 2: Install Python dependencies

Install the necessary Python libraries using pip. It is highly recommended to use a virtual environment.
Bash

pip install -r requirements.txt

Step 3: Database setup

This application requires a PostgreSQL database.

    Install PostgreSQL: If you haven't already, install PostgreSQL on your system.

    Create a database: Open a SQL client (like psql or pgAdmin) and create a new database.
    SQL

CREATE DATABASE myDatabase;

Create tables: Connect to your new database and run the following SQL commands to create the necessary tables for the system.
SQL

CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13),
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255)
);

CREATE TABLE Loans (
    loan_id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES Books(book_id),
    member_id INTEGER REFERENCES Members(member_id),
    loan_date DATE NOT NULL,
    return_date DATE
);

Configure the connection: Open the library_app.py file and update the database connection details in the init_db_connection method with your own credentials.
Python

    self.db_conn = psycopg2.connect(
        host="localhost",
        database="myDatabase",
        user="postgres",
        password="your_password" # Update your password here
    )

How to Run the Application

    Make sure your PostgreSQL service is running.

    Open a terminal or command prompt.

    Navigate to the directory where you cloned the project.

    Run the application using the following command:
    Bash

    python library_app.py

A graphical user interface (GUI) window will pop up, and you can start managing your library.

Logging

The application logs all significant events and errors to a file named library_app.log in the project directory. This file is useful for debugging and tracking application activity.
