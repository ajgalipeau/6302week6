# application/VIEW/view.py

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import pprint
from BLL.students import Student
import os
import logging

class View(toga.App):
    def startup(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Determine the role from environment variables
        role = os.getenv('DB_ROLE', 'admin_user')  # Default to 'read_only' if not set
        logging.info(f"Starting application with role: {role}")
        
        # Instantiate Business Logic Layer with role-based DAL
        self.bll = Student(role=role)
        
        # Fetch student data from the database
        try:
            self.data = self.bll.getStudentsWithClasses()
        except Exception as e:
            logging.error(f"Error fetching student data: {e}")
            self.data = []
        
        # Debugging: Print fetched data to console
        logging.info("Fetching Data from the Database:")
        pprint.pprint(self.data)  # Console output
        
        # Format data for the Toga Table
        formatted_data = [
            (
                row.get('StudentFirstName', 'N/A'),
                row.get('StudentLastName', 'N/A'),
                row.get('StudentEmail', 'N/A'),
                row.get('ClassSubjects', 'N/A'),  # Concatenated subjects if available
                row.get('ClassGrades', 'N/A'),    # Concatenated grades if available
                row.get('TeacherNames', 'N/A'),   # Concatenated teacher names if available
                row.get('AverageGrade', 'N/A')    # Average grade if calculated
            )
            for row in self.data
        ]
        
        # Set up the table to show the data
        self.left_container = toga.Table(
            headings=["First Name", 
                      "Last Name", 
                      "Email", 
                      "Class Subjects", 
                      "Class Grades", 
                      "Teacher Names", 
                      "Average Grade"], 
            style=Pack(flex=1, padding=10), 
            data=formatted_data
        )

        # Input form elements for adding a new student
        right_content = toga.Box(
            style=Pack(direction=COLUMN, padding_top=20, alignment="center")
        )
        
        # Title: Student Entry Form
        form_title = toga.Label(
            "Student Entry Form", 
            style=Pack(font_size=24, font_weight="bold", text_align=CENTER, padding_bottom=20)
        )
        right_content.add(form_title)
        
        # First Name and Last Name in a row
        name_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))

        # First Name Input
        input_box_fn = toga.Box(style=Pack(direction=COLUMN, padding_right=10))
        fn_label = toga.Label("First Name", style=Pack(padding_bottom=5))
        self.first_name = toga.TextInput(placeholder="First Name", style=Pack(width=200))
        input_box_fn.add(fn_label)
        input_box_fn.add(self.first_name)
        
        # Last Name Input
        input_box_ln = toga.Box(style=Pack(direction=COLUMN))
        ln_label = toga.Label("Last Name", style=Pack(padding_bottom=5))
        self.last_name = toga.TextInput(placeholder="Last Name", style=Pack(width=200))
        input_box_ln.add(ln_label)
        input_box_ln.add(self.last_name)

        # Add name fields to name_box
        name_box.add(input_box_fn)
        name_box.add(input_box_ln)

        # Add the name box to the form
        right_content.add(name_box)

        # Email Address Input
        input_box_email = toga.Box(style=Pack(direction=COLUMN, padding_bottom=10, alignment=CENTER))
        email_label = toga.Label("Email Address", style=Pack(padding_bottom=5, text_align=CENTER))
        self.email = toga.TextInput(placeholder="youremail@school.edu", style=Pack(width=400))
        input_box_email.add(email_label)
        input_box_email.add(self.email)
        right_content.add(input_box_email)

        # Grade Year Input
        input_box_grade = toga.Box(style=Pack(direction=COLUMN, padding_bottom=10, alignment=CENTER))
        grade_label = toga.Label("Grade Year", style=Pack(padding_bottom=5, text_align=CENTER))
        self.grade = toga.TextInput(placeholder="e.g 6 for 6th Grade", style=Pack(width=400))
        input_box_grade.add(grade_label)
        input_box_grade.add(self.grade)
        right_content.add(input_box_grade)

        # Date of Birth Input
        input_box_dob = toga.Box(style=Pack(direction=COLUMN, padding_bottom=20, alignment=CENTER))
        dob_label = toga.Label("Date of Birth", style=Pack(padding_bottom=5, text_align=CENTER))
        self.date_of_birth = toga.TextInput(placeholder="YYYY-MM-DD", style=Pack(width=400))
        input_box_dob.add(dob_label)
        input_box_dob.add(self.date_of_birth)
        right_content.add(input_box_dob)

        # Add User Button
        self.add_user_button = toga.Button(
            "Add User",
            on_press=self.button_handler,
            style=Pack(width=200, padding=20, alignment=CENTER)
        )
        right_content.add(self.add_user_button)
        
        # Success/Error Message Label
        self.message_label = toga.Label(
            "",  # Initially empty
            style=Pack(padding_top=10, text_align=CENTER)
        )
        right_content.add(self.message_label)
        
        # Admin-Only Button (Delete All Students) - Visible Only to Admin Users
        if role == 'admin_user':
            self.delete_all_button = toga.Button(
                "Delete All Students",
                on_press=self.delete_all_students_handler,
                style=Pack(width=200, padding=20, alignment=CENTER, background_color='red', color='white')
            )
            right_content.add(self.delete_all_button)
        
        # Scroll Container for Right Content
        right_container = toga.ScrollContainer(horizontal=False)
        right_container.content = right_content

        # Split Container to Separate Table and Form
        split = toga.SplitContainer()
        split.content = [(self.left_container, 3), (right_container, 1.35)]

        # Create the main window with a specified size
        self.main_window = toga.MainWindow(title="BHMS Student Database - Poway Unified School District", 
                                           size=(1400, 800),
                                           position=(100, 100)
                                           )
        self.main_window.content = split
        self.main_window.show()
        
        # Handle window close event
        self.main_window.on_close = self.on_close_handler

    def on_close_handler(self, widget):
        logging.info("\nWindow is closing.\n")
        self.bll.disconnect()  # Disconnect DAL connections
        return True

    def button_handler(self, widget):
        """
        Handles the Add User button press.
        Validates input and attempts to add a new student.
        Displays success or error messages accordingly.
        """
        # Clear previous messages
        self.message_label.text = ""
        
        # Validation - Input fields
        if not self.first_name.value or not self.last_name.value or not self.email.value or not self.grade.value:
            error_msg = "Error: All fields must be filled out."
            logging.error(error_msg)
            self.message_label.text = error_msg
            return

        # Validation - Email
        if "@" not in self.email.value or "." not in self.email.value:
            error_msg = "Error: Invalid email format."
            logging.error(error_msg)
            self.message_label.text = error_msg
            return

        # Validation - Grade Number
        try:
            grade_int = int(self.grade.value)
            if grade_int < 1 or grade_int > 12:
                raise ValueError
        except ValueError:
            error_msg = "Error: Grade must be a number between 1 and 12."
            logging.error(error_msg)
            self.message_label.text = error_msg
            return

        # Validation - Date of Birth Format (Optional)
        dob = self.date_of_birth.value.strip() if self.date_of_birth.value else None
        if dob:
            try:
                # Simple check for YYYY-MM-DD format
                parts = dob.split('-')
                if len(parts) != 3 or not all(part.isdigit() for part in parts):
                    raise ValueError
            except ValueError:
                error_msg = "Error: Date of Birth must be in YYYY-MM-DD format."
                logging.error(error_msg)
                self.message_label.text = error_msg
                return

        # Create a new Student object with the specified role
        student = self.bll  # Already initialized with role
        student.first_name = self.first_name.value.strip()
        student.last_name = self.last_name.value.strip()
        student.email = self.email.value.strip()
        student.date_of_birth = dob if dob else None
        student.grade = grade_int
        
        # Attempt to add the student using the stored procedure
        try:
            student.add()  # Correct method call to avoid AttributeError
            self.data = student.getStudentsWithClasses()
            if self.data:
                # Ensure the SQL data is fetched correctly
                logging.info("Raw Data from Query:")
                pprint.pprint(self.data)  # Debugging

                # Update the formatted data
                formatted_data = [
                    (
                        row["StudentFirstName"], 
                        row["StudentLastName"], 
                        row["StudentEmail"], 
                        row.get("ClassSubjects", "N/A"),  # Concatenated subjects
                        row.get("ClassGrades", "N/A"),    # Concatenated grades
                        row.get("TeacherNames", "N/A"),   # Concatenated teacher names
                        row.get("AverageGrade", "N/A")    # Average grade
                    )
                    for row in self.data
                ]
                
                # Update the table with the new data
                self.left_container.data = formatted_data

            # Clear form input fields
            self.first_name.value = ""
            self.last_name.value = ""
            self.email.value = ""
            self.grade.value = ""
            self.date_of_birth.value = ""

            # Set success message
            success_msg = "Student Successfully Added!"
            logging.info(success_msg)
            self.message_label.text = success_msg

        except AttributeError as e:
            # This should not occur if BLL is correctly implemented
            error_msg = f"Attribute Error: {e}"
            logging.error(error_msg)
            self.message_label.text = "An unexpected error occurred. Please contact the administrator."
        except Exception as e:
            # Catch-all for any other exceptions
            error_msg = f"Error: {e}"
            logging.error(error_msg)
            self.message_label.text = f"Error: {e}"

    def delete_all_students_handler(self, widget): # THIS IS NOT WORKING....
        """
        Handles the Delete All Students button press.
        Attempts to delete all student records.
        """
        # Show confirmation dialog
        confirmation = self.main_window.confirm_dialog(
            title="Confirmation",
            message="Are you sure you want to delete all students? This action cannot be undone."
        )
        if confirmation == "Delete All":
            try:
                self.bll.deleteAllStudents()
                self.data = self.bll.getStudentsWithClasses()
                if self.data:
                    formatted_data = [
                        (
                            row["StudentFirstName"], 
                            row["StudentLastName"], 
                            row["StudentEmail"], 
                            row.get("ClassSubjects", "N/A"),  # Concatenated subjects
                            row.get("ClassGrades", "N/A"),    # Concatenated grades
                            row.get("TeacherNames", "N/A"),   # Concatenated teacher names
                            row.get("AverageGrade", "N/A")    # Average grade
                        )
                        for row in self.data
                    ]
                    
                    # Update the table with the new data
                    self.left_container.data = formatted_data

                # Set success message
                success_msg = "All students have been deleted successfully!"
                logging.info(success_msg)
                self.message_label.text = success_msg

            except Exception as e:
                error_msg = f"Error deleting all students: {e}"
                logging.error(error_msg)
                self.message_label.text = error_msg
        else:
            # User canceled the deletion
            logging.info("User canceled the deletion operation.")

    def on_close_handler(self, widget):
        logging.info("\nWindow is closing.\n")
        self.bll.disconnect()  # Disconnect DAL connections
        return True
