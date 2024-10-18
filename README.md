# CSC6302 Week 6 Project - Student Database with Toga GUI

This project is a student database application built using Python and Toga GUI. It allows users to manage student records, including displaying student information, adding new students, and calculating average grades from multiple tables in a relational database.

## Prerequisites

Before starting, ensure you have the following installed:

- Python 3.10 or later
- Docker Desktop
  - Windows/Mac: Download and install from [Docker Desktop](https://docs.docker.com/desktop/)
  - Linux: Use your package manager or follow Docker's installation guide
- MySQL Workbench
  - Download from [MySQL Downloads](https://dev.mysql.com/downloads/workbench/)
  - Follow the installation wizard for your operating system
- **Important**: After installing Docker and MySQL Workbench, restart your computer to ensure all services are properly initialized

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ajgalipeau/6302week6.git
   cd "$(pwd)/6302week6"    # Unix/Mac
   # or
   cd "$PWD\6302week6"      # Windows PowerShell
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Unix/Mac
   python3 -m venv togavenv
   source togavenv/bin/activate

   # Windows PowerShell
   python -m venv togavenv
   .\togavenv\Scripts\Activate.ps1
   # Note: If you encounter execution policy errors, run:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install Required Packages**
   ```bash
   # Using make (recommended)
   make install
   
   # Alternative method
   pip install -r requirements.txt
   ```

4. **Docker and MySQL Setup**
   ```bash
   # Pull MySQL image
   docker pull mysql

   # Create and start MySQL container
   docker run --name student_db \
   -e MYSQL_ROOT_PASSWORD=db123456 \
   -e MYSQL_DATABASE=student_db \
   -e lower_case_table_names=1 \
   -p 3306:3306 \
   -d mysql
   ```

## Troubleshooting MySQL Port Conflicts

### Windows
If port 3306 is already in use:
```powershell
# Find process using port 3306
netstat -aon | findstr :3306
# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

### macOS/Linux
```bash
# Stop MySQL if running through Homebrew
brew services stop mysql

# Or find and kill the process
sudo lsof -i :3306
sudo kill <PID>
```

## Database Setup
After starting the Docker container, use MySQL Workbench to run the setup scripts in this order:
1. Connect to localhost:3306 using root/db123456
2. Execute the following SQL scripts in order:
   ```
   sql/ddl.sql
   sql/dml.sql
   sql/users.sql
   sql/permissions.sql
   sql/procedure_functions.sql
   sql/query.sql
   ```

## Running the Application

1. **Clean the Environment**
   ```bash
   make clean
   ```
   The Makefile is a build automation tool that simplifies common tasks. The `clean` command removes cache files and ensures a fresh start.

2. **Start the Application**
Navigate to the application directory and perform the following steps depending on the role you want to use. 
1. Open students.py and modify the role in line 8.
2. Open view.py and modify the role in line 17.
3. In your terminal execute the following commands, ensuring you use the correct role from the .env file.
   ```bash
   export DB_ROLE=read_only
   python3 main.py
   ```

This will launch the [Toga](https://toga.readthedocs.io/en/stable/) GUI application. Toga is a native, Python native GUI toolkit that allows for creating native mobile and desktop applications.

## License

Educational License

This project is licensed under the Educational License for the purposes of learning, academic exercises, and research.

Holder:  
Aaron Galipeau  
M.S. Computer Science Student  
Merrimack College  
Lecturer: Robert Sands  
Course: CSC6302 Database Principles

This license allows the project to be used, modified, and shared for educational purposes only. Commercial use or redistribution is strictly prohibited without prior written permission.