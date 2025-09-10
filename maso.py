# این فایل باید به صورت مستقل با دستور 'python library_app.py' در ترمینال اجرا شود.

import sys
import psycopg2
import logging
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QTabWidget, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('library_app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db_conn = None
        self.db_cursor = None
        self.init_db_connection()
        if self.db_conn:
            self.init_ui()

    def init_db_connection(self):
        """Initializes the connection to the PostgreSQL database."""
        try:
            logging.info("Attempting to connect to the database...")
            self.db_conn = psycopg2.connect(
                host="localhost",
                database="myDatabase",
                user="postgres",
                password="1360"
            )
            self.db_cursor = self.db_conn.cursor()
            logging.info("Successfully connected to the database.")
        except psycopg2.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            QMessageBox.critical(self, "database error", f"error in connection to the database: {e}")
            self.db_conn = None

    def init_ui(self):
        """Sets up the main user interface."""
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Tab for Books
        self.books_tab = QWidget()
        self.tab_widget.addTab(self.books_tab, "Books management")
        self.setup_books_tab()

        # Tab for Members
        self.members_tab = QWidget()
        self.tab_widget.addTab(self.members_tab, "Members management")
        self.setup_members_tab()
        
        # Tab for Loans
        self.loans_tab = QWidget()
        self.tab_widget.addTab(self.loans_tab, "Loan management")
        self.setup_loans_tab()

        # Refresh data on startup
        self.refresh_books_table()
        self.refresh_members_table()
        self.refresh_loans_table()
        logging.info("Application UI initialized and data refreshed.")

    def setup_books_tab(self):
        """Sets up the UI for the Books tab."""
        layout = QVBoxLayout(self.books_tab)

        # Form for adding/updating books
        form_layout = QGridLayout()
        self.book_title_input = QLineEdit()
        self.book_author_input = QLineEdit()
        self.book_isbn_input = QLineEdit()
        
        # Set validator for ISBN
        self.book_isbn_input.setValidator(QIntValidator())
        
        form_layout.addWidget(QLabel("Book Name:"), 0, 0)
        form_layout.addWidget(self.book_title_input, 0, 1)
        form_layout.addWidget(QLabel("Author:"), 1, 0)
        form_layout.addWidget(self.book_author_input, 1, 1)
        form_layout.addWidget(QLabel("ISBN:"), 2, 0)
        form_layout.addWidget(self.book_isbn_input, 2, 1)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_book_btn = QPushButton("Add a Book")
        self.add_book_btn.clicked.connect(self.add_book)
        self.update_book_btn = QPushButton("Update Book")
        self.update_book_btn.clicked.connect(self.update_book)
        self.delete_book_btn = QPushButton("Remove Book")
        self.delete_book_btn.clicked.connect(self.delete_book)
        
        button_layout.addWidget(self.add_book_btn)
        button_layout.addWidget(self.update_book_btn)
        button_layout.addWidget(self.delete_book_btn)
        layout.addLayout(button_layout)

        # Table to display books
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["ID", "Label", "Author", "ISBN"])
        self.books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.books_table.itemClicked.connect(self.select_book)
        layout.addWidget(self.books_table)

    def setup_members_tab(self):
        """Sets up the UI for the Members tab."""
        layout = QVBoxLayout(self.members_tab)

        # Form for adding/updating members
        form_layout = QGridLayout()
        self.member_name_input = QLineEdit()
        self.member_email_input = QLineEdit()
        
        form_layout.addWidget(QLabel("Member Name:"), 0, 0)
        form_layout.addWidget(self.member_name_input, 0, 1)
        form_layout.addWidget(QLabel("Email:"), 1, 0)
        form_layout.addWidget(self.member_email_input, 1, 1)
        
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_member_btn = QPushButton("Add Member")
        self.add_member_btn.clicked.connect(self.add_member)
        self.update_member_btn = QPushButton("Member Update")
        self.update_member_btn.clicked.connect(self.update_member)
        self.delete_member_btn = QPushButton("Remove Member")
        self.delete_member_btn.clicked.connect(self.delete_member)
        
        button_layout.addWidget(self.add_member_btn)
        button_layout.addWidget(self.update_member_btn)
        button_layout.addWidget(self.delete_member_btn)
        layout.addLayout(button_layout)

        # Table to display members
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(3)
        self.members_table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        self.members_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.members_table.itemClicked.connect(self.select_member)
        layout.addWidget(self.members_table)
    
    def setup_loans_tab(self):
        """Sets up the UI for the Loans tab."""
        layout = QVBoxLayout(self.loans_tab)

        # Form for adding/returning a book
        form_layout = QGridLayout()
        self.loan_book_id_input = QLineEdit()
        self.loan_member_id_input = QLineEdit()
        
        # Set validators for loan IDs
        self.loan_book_id_input.setValidator(QIntValidator())
        self.loan_member_id_input.setValidator(QIntValidator())
        
        form_layout.addWidget(QLabel("Book ID:"), 0, 0)
        form_layout.addWidget(self.loan_book_id_input, 0, 1)
        form_layout.addWidget(QLabel("Member ID:"), 1, 0)
        form_layout.addWidget(self.loan_member_id_input, 1, 1)
        
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.loan_book_btn = QPushButton("Loan a Book")
        self.loan_book_btn.clicked.connect(self.loan_book)
        self.return_book_btn = QPushButton("Retrurn a book")
        self.return_book_btn.clicked.connect(self.return_book)
        
        button_layout.addWidget(self.loan_book_btn)
        button_layout.addWidget(self.return_book_btn)
        layout.addLayout(button_layout)

        # Table to display loans
        self.loans_table = QTableWidget()
        self.loans_table.setColumnCount(5)
        self.loans_table.setHorizontalHeaderLabels(["ID", "Book id", "Member id", "Loan Date", "Date of Return"])
        layout.addWidget(self.loans_table)


    # --- CRUD Functions for Books ---
    def add_book(self):
        title = self.book_title_input.text()
        author = self.book_author_input.text()
        isbn_text = self.book_isbn_input.text()

        if not title or not author:
            logging.warning("Attempted to add a book with missing title or author.")
            QMessageBox.warning(self, "خطا", "please insert name ans author.")
            return

        if not isbn_text.isdigit() and isbn_text:
            logging.warning(f"Attempted to add book '{title}' with non-numeric ISBN: {isbn_text}")
            QMessageBox.warning(self, "خطا", "ISBN must be a number.")
            return
        
        isbn = int(isbn_text) if isbn_text else None

        try:
            self.db_cursor.execute(
                "INSERT INTO Books (title, author, isbn) VALUES (%s, %s, %s)",
                (title, author, isbn)
            )
            self.db_conn.commit()
            logging.info(f"Book '{title}' added successfully.")
            QMessageBox.information(self, "Success", f"کتاب '{title}' added successfully.")
            self.refresh_books_table()
            self.clear_book_inputs()
        except Exception as e:
            logging.error(f"Error adding book '{title}': {e}")
            QMessageBox.critical(self, "Errorا", f"Error in adding book: {e}")
            self.db_conn.rollback()

    def refresh_books_table(self):
        """Fetches and displays all books from the database."""
        try:
            self.db_cursor.execute("SELECT book_id, title, author, isbn FROM Books")
            books = self.db_cursor.fetchall()
            self.books_table.setRowCount(len(books))
            for row_index, row_data in enumerate(books):
                for col_index, col_data in enumerate(row_data):
                    self.books_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data) if col_data is not None else ""))
            logging.info("Books table refreshed.")
        except Exception as e:
            logging.error(f"Error fetching books from database: {e}")
            QMessageBox.critical(self, "خطا", f"error in receive book: {e}")

    def select_book(self, item):
        """Loads selected row data into input fields."""
        row = item.row()
        self.selected_book_id = self.books_table.item(row, 0).text()
        self.book_title_input.setText(self.books_table.item(row, 1).text())
        self.book_author_input.setText(self.books_table.item(row, 2).text())
        
        # Check if item exists before setting text
        isbn_item = self.books_table.item(row, 3)
        if isbn_item:
            self.book_isbn_input.setText(isbn_item.text())
        logging.info(f"Book with ID {self.selected_book_id} selected.")

    def update_book(self):
        try:
            book_id = self.selected_book_id
            title = self.book_title_input.text()
            author = self.book_author_input.text()
            isbn_text = self.book_isbn_input.text()

            if not isbn_text.isdigit() and isbn_text:
                logging.warning(f"Attempted to update book {book_id} with non-numeric ISBN: {isbn_text}")
                QMessageBox.warning(self, "خطا", "ISBN must be a number.")
                return

            isbn = int(isbn_text) if isbn_text else None
            
            self.db_cursor.execute(
                "UPDATE Books SET title = %s, author = %s, isbn = %s WHERE book_id = %s",
                (title, author, isbn, book_id)
            )
            self.db_conn.commit()
            logging.info(f"Book with ID {book_id} updated successfully.")
            QMessageBox.information(self, "success", "book updated successfully.")
            self.refresh_books_table()
            self.clear_book_inputs()
        except Exception as e:
            logging.error(f"Error updating book {book_id}: {e}")
            QMessageBox.critical(self, "errorا", f"error in updating book: {e}")
            self.db_conn.rollback()

    def delete_book(self):
        try:
            book_id = self.selected_book_id
            self.db_cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
            self.db_conn.commit()
            logging.info(f"Book with ID {book_id} removed successfully.")
            QMessageBox.information(self, "success", "book removed suuccessfully.")
            self.refresh_books_table()
            self.clear_book_inputs()
        except Exception as e:
            logging.error(f"Error removing book {book_id}: {e}")
            QMessageBox.critical(self, "error", f"error in remove book: {e}")
            self.db_conn.rollback()

    def clear_book_inputs(self):
        self.book_title_input.clear()
        self.book_author_input.clear()
        self.book_isbn_input.clear()
        self.selected_book_id = None
        logging.info("Book input fields cleared.")

    # --- CRUD Functions for Members ---
    def add_member(self):
        name = self.member_name_input.text()
        email = self.member_email_input.text()
        if not name:
            logging.warning("Attempted to add a member with missing name.")
            QMessageBox.warning(self, "error", "please insert the members name.")
            return

        try:
            self.db_cursor.execute(
                "INSERT INTO Members (name, email) VALUES (%s, %s)",
                (name, email)
            )
            self.db_conn.commit()
            logging.info(f"Member '{name}' added successfully.")
            QMessageBox.information(self, "success", f"member '{name}' added successfully.")
            self.refresh_members_table()
            self.clear_member_inputs()
        except Exception as e:
            logging.error(f"Error adding member '{name}': {e}")
            QMessageBox.critical(self, "error", f"error in adding member: {e}")
            self.db_conn.rollback()
    
    def refresh_members_table(self):
        """Fetches and displays all members from the database."""
        try:
            self.db_cursor.execute("SELECT member_id, name, email FROM Members")
            members = self.db_cursor.fetchall()
            self.members_table.setRowCount(len(members))
            for row_index, row_data in enumerate(members):
                for col_index, col_data in enumerate(row_data):
                    self.members_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data) if col_data is not None else ""))
            logging.info("Members table refreshed.")
        except Exception as e:
            logging.error(f"Error fetching members from database: {e}")
            QMessageBox.critical(self, "خطا", f"error in member receive: {e}")
            
    def select_member(self, item):
        """Loads selected row data into input fields."""
        row = item.row()
        self.selected_member_id = self.members_table.item(row, 0).text()
        self.member_name_input.setText(self.members_table.item(row, 1).text())
        
        # Check if item exists before setting text
        email_item = self.members_table.item(row, 2)
        if email_item:
            self.member_email_input.setText(email_item.text())
        logging.info(f"Member with ID {self.selected_member_id} selected.")
        
    def update_member(self):
        try:
            member_id = self.selected_member_id
            name = self.member_name_input.text()
            email = self.member_email_input.text()
            
            self.db_cursor.execute(
                "UPDATE Members SET name = %s, email = %s WHERE member_id = %s",
                (name, email, member_id)
            )
            self.db_conn.commit()
            logging.info(f"Member with ID {member_id} updated successfully.")
            QMessageBox.information(self, "success", "member updated successfully.")
            self.refresh_members_table()
            self.clear_member_inputs()
        except Exception as e:
            logging.error(f"Error updating member {member_id}: {e}")
            QMessageBox.critical(self, "errorا", f"error in member update: {e}")
            self.db_conn.rollback()

    def delete_member(self):
        try:
            member_id = self.selected_member_id
            self.db_cursor.execute("DELETE FROM Members WHERE member_id = %s", (member_id,))
            self.db_conn.commit()
            logging.info(f"Member with ID {member_id} removed successfully.")
            QMessageBox.information(self, "success", "member removed successfully.")
            self.refresh_members_table()
            self.clear_member_inputs()
        except Exception as e:
            logging.error(f"Error removing member {member_id}: {e}")
            QMessageBox.critical(self, "error", f"error in member remove: {e}")
            self.db_conn.rollback()

    def clear_member_inputs(self):
        self.member_name_input.clear()
        self.member_email_input.clear()
        self.selected_member_id = None
        logging.info("Member input fields cleared.")
        
    # --- CRUD Functions for Loans ---
    def loan_book(self):
        book_id_text = self.loan_book_id_input.text()
        member_id_text = self.loan_member_id_input.text()
        
        if not book_id_text or not member_id_text:
            logging.warning("Attempted to loan a book with missing book or member ID.")
            QMessageBox.warning(self, "error", "please insert the book and the members id.")
            return
        
        # Check if inputs are numbers
        if not book_id_text.isdigit() or not member_id_text.isdigit():
            logging.warning("Attempted loan with non-numeric IDs.")
            QMessageBox.warning(self, "خطا", "Book ID and Member ID must be numbers.")
            return

        book_id = int(book_id_text)
        member_id = int(member_id_text)
        
        try:
            logging.info(f"Attempting to loan book ID {book_id} to member ID {member_id}.")
            
            # Check if book exists and is available
            self.db_cursor.execute("SELECT is_available FROM Books WHERE book_id = %s", (book_id,))
            result = self.db_cursor.fetchone()
            if not result:
                logging.error(f"Book with ID {book_id} does not exist.")
                QMessageBox.critical(self, "error", "This book doesn't exist.")
                return
            if not result[0]:
                logging.warning(f"Book with ID {book_id} is already on loan.")
                QMessageBox.critical(self, "error", "This book is currently on loan.")
                return

            # Check if member exists
            self.db_cursor.execute("SELECT 1 FROM Members WHERE member_id = %s", (member_id,))
            if not self.db_cursor.fetchone():
                logging.error(f"Member with ID {member_id} does not exist.")
                QMessageBox.critical(self, "error", "This member doesn't exist.")
                return

            # Insert new loan record
            self.db_cursor.execute(
                "INSERT INTO Loans (book_id, member_id, loan_date) VALUES (%s, %s, CURRENT_DATE)",
                (book_id, member_id)
            )
            
            # Update book availability
            self.db_cursor.execute("UPDATE Books SET is_available = FALSE WHERE book_id = %s", (book_id,))
            
            self.db_conn.commit()
            logging.info(f"Loan of book {book_id} to member {member_id} completed successfully.")
            QMessageBox.information(self, "موفقیت", "the book got loaned successfully.")
            self.refresh_loans_table()
        except Exception as e:
            logging.error(f"Error loaning book: {e}")
            QMessageBox.critical(self, "error", f"error in loan: {e}")
            self.db_conn.rollback()

    def return_book(self):
        book_id_text = self.loan_book_id_input.text()
        if not book_id_text:
            logging.warning("Attempted to return a book with missing book ID.")
            QMessageBox.warning(self, "error", "please insert the book id.")
            return

        # Check if input is a number
        if not book_id_text.isdigit():
            logging.warning("Attempted to return book with non-numeric ID.")
            QMessageBox.warning(self, "خطا", "Book ID must be a number.")
            return
            
        book_id = int(book_id_text)

        try:
            logging.info(f"Attempting to return book with ID {book_id}.")
            
            # Check if book is currently on loan
            self.db_cursor.execute("SELECT 1 FROM Loans WHERE book_id = %s AND return_date IS NULL", (book_id,))
            if not self.db_cursor.fetchone():
                logging.warning(f"Book with ID {book_id} is not currently on loan.")
                QMessageBox.critical(self, "error", " This book didn't got loaned or has been returned.")
                return

            # Update loan record with return date
            self.db_cursor.execute(
                "UPDATE Loans SET return_date = CURRENT_DATE WHERE book_id = %s AND return_date IS NULL", 
                (book_id,)
            )
            
            # Update book availability
            self.db_cursor.execute("UPDATE Books SET is_available = TRUE WHERE book_id = %s", (book_id,))
            
            self.db_conn.commit()
            logging.info(f"Book with ID {book_id} returned successfully.")
            QMessageBox.information(self, "success", "book returned successfully.")
            self.refresh_loans_table()
        except Exception as e:
            logging.error(f"Error returning book: {e}")
            QMessageBox.critical(self, "errorا", f"error in the book turn back: {e}")
            self.db_conn.rollback()

    def refresh_loans_table(self):
        """Fetches and displays all loan records from the database."""
        try:
            self.db_cursor.execute("SELECT * FROM Loans")
            loans = self.db_cursor.fetchall()
            self.loans_table.setRowCount(len(loans))
            for row_index, row_data in enumerate(loans):
                for col_index, col_data in enumerate(row_data):
                    self.loans_table.setItem(row_index, col_index, QTableWidgetItem(str(col_data) if col_data is not None else ""))
            logging.info("Loans table refreshed.")
        except Exception as e:
            logging.error(f"Error fetching loan records from database: {e}")
            QMessageBox.critical(self, "error", f"error in loan list: {e}")

    def closeEvent(self, event):
        """Closes the database connection when the application is closed."""
        if self.db_conn:
            self.db_cursor.close()
            self.db_conn.close()
            logging.info("Database connection closed.")
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LibraryApp()
    if ex.db_conn:
        ex.show()
        sys.exit(app.exec_())