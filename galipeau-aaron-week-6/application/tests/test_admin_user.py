import mysql.connector
from faker import Faker

# Verbose helper function to display test result
def show_test_result(test_name, success=True):
    status = "PASSED" if success else "FAILED"
    print(f"{test_name} - {status}")

# Create a Faker instance for generating test data
fake = Faker()

# Connect as admin_user
print("\nConnecting as admin_user...")
cnx = mysql.connector.connect(
    user='admin_user',
    password='admin1234',
    host='127.0.0.1',
    database='SCHOOL'
)
cursor = cnx.cursor()

# Test 1: Read operation (should succeed)
print("\nTest 1: Read operation for admin_user (should succeed):")
try:
    cursor.execute("CALL getStudentsWithClasses();")
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
        show_test_result("Read operation for admin_user", success=True)
    else:
        print("\nEnd of results\n")
except mysql.connector.Error as err:
    print(f"\nError: {err}\n")
    show_test_result("Read operation for admin_user", success=False)

# Test 2: Write operation (should succeed)
print("\nTest 2: Write operation for admin_user (should succeed):")
try:
    fname = fake.first_name()
    lname = fake.last_name()
    email = fake.email()
    dob = fake.date_of_birth(minimum_age=10, maximum_age=15)
    grade = 6

    cursor.execute("CALL InsertStudent(%s, %s, %s, %s, %s);", (fname, lname, email, dob, grade))
    cnx.commit()
    print(f"\nStudent added: {fname} {lname}, Email: {email}, DOB: {dob}, Grade: {grade}\n")
    show_test_result("Write operation for admin_user", success=True)
except mysql.connector.Error as err:
    print(f"\nError: {err}\n")
    show_test_result("Write operation for admin_user", success=False)

# Test 3: GRANT operation (should succeed)
print("\nTest 3: GRANT operation for admin_user (should succeed):")
try:
    cursor.execute("GRANT SELECT ON SCHOOL.* TO 'read_only'@'localhost';")
    show_test_result("GRANT operation for admin_user", success=True)
except mysql.connector.Error as err:
    print(f"\nError: {err}\n")
    show_test_result("GRANT operation for admin_user", success=False)

# Test 4: REVOKE operation (should succeed)
print("\nTest 4: REVOKE operation for admin_user (should succeed):")
try:
    cursor.execute("REVOKE SELECT ON SCHOOL.* FROM 'read_only'@'localhost';")
    show_test_result("REVOKE operation for admin_user", success=True)
except mysql.connector.Error as err:
    print(f"\nError: {err}\n")
    show_test_result("REVOKE operation for admin_user", success=False)

# Close connection
cursor.close()
cnx.close()
print("\nDisconnected from the database.")
