import toga
from toga.style.pack import COLUMN, ROW, CENTER, Pack
import toga.widgets
from BLL.students import Student

# Instantiate Business Logic Layer
bll = Student()

# Create View Layer

class View(toga.App):
    def startup(self):
        # Fetch student data from the database
        self.data = bll.getStudentsWithClasses()

        # Debugging
        print("\nFetching Data from the Database:\n")
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
        self.email = toga.TextInput(placeholder="youremail@merrimack.edu", style=Pack(width=400))
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
        self.date_of_birth = toga.TextInput(placeholder="01/01/2001", style=Pack(width=400))
        input_box_dob.add(dob_label)
        input_box_dob.add(self.date_of_birth)
        right_content.add(input_box_dob)

        right_content.add(
            toga.Button(
                "Add User",
                on_press=self.button_handler,
                style=Pack(width=200, padding=20, alignment=CENTER)
            )
        )
        
        self.success_message = toga.Label(
            "",  # Initially empty
            style=Pack(padding_top=10, text_align=CENTER)
        )
        right_content.add(self.success_message)
        
        right_container = toga.ScrollContainer(horizontal=False)
        right_container.content = right_content

        split = toga.SplitContainer()
        split.content = [(self.left_container, 3), (right_container, 1.35)]

        # Create the main window with a specified size
        self.main_window = toga.MainWindow(title="Bernardo Heights Middle School Student Database", 
                                           size=(1400, 800),
                                           position=(100, 100)
                                           )
        self.main_window.content = split
        self.main_window.show()
        
        self.main_window.on_close = self.on_close_handler

    def on_close_handler(self, widget):
        print("\nWindow is closing.\n")
        return True

    def button_handler(self, widget):
        # Validation - Input fields
        if not self.first_name.value or not self.last_name.value or not self.email.value or not self.grade.value:
            print("Error: All fields must be filled out.")
            self.success_message.text = "Error: All fields must be filled out."
            return

        # Validation - Email
        if "@" not in self.email.value or "." not in self.email.value:
            print("Error: Invalid email format.")
            self.success_message.text = "Error: Invalid email format."
            return

        # Validation - Grade Number
        try:
            int(self.grade.value)
        except ValueError:
            print("Error: Grade must be a number.")
            self.success_message.text = "Error: Grade must be a number."
            return

        # Create a new Student object
        student = Student(
            first_name=self.first_name.value,
            last_name=self.last_name.value,
            email=self.email.value,
            date_of_birth='2000-01-01',  # For simplicity, hardcoded DOB
            grade=self.grade.value
        )
        # Add the student to the database
        student.add()
        self.data = student.getStudentsWithClasses()
        if self.data:
            
            # Ensure the SQL data is fetched correctly
            print("Raw Data from Query:", self.data)  # Debugging

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
        self.success_message.text = "Student Successfully Added!"
        print("Student added successfully and table updated!")
        
# if __name__ == '__main__' :
#     View("CSC6302 SCHOOL DB", "User Views App").main_loop()