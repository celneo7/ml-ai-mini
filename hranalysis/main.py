import mysql.connector

# referenced from https://www.geeksforgeeks.org/employee-management-system-using-python/

connection = mysql.connector.connect(
    host = "localhost", user= "root", password="password", database = "emp"
)

# function for checking if employee with given id exists
def check(id):
    query = 'SELECT * FROM employees WHERE id=%s'

    cursor = connection.cursor(buffered= True)
    data = (id,)

    cursor.execute(query, data)
    employee = cursor.fetchone()

    cursor.close()

    return employee is not None


# function to add employee
def add():
    id = input("Enter Employee ID: ")

    if check(id):
        print("Employee already exists. Please try again with different ID.")
        return
    
    else:
        name = input("Enter Employee Name: ")
        post = input("Enter Employee Post: ")
        salary = input("Enter Employee Salary: ")
        
        # insert employee details into sql employee table
        query = 'INSERT INTO employees (id, name, position, salary) VALUES (%s, %s, %s, %s)'
        data = (id, name, post, salary,)
        cursor = connection.cursor

        try:
            # execute sql query
            cursor.execute(query, data)

            connection.commit()
            print("Employee Added Successfully")

        except mysql.connector.Error as e:
            print(f'Error: {e}')
            connection.rollback()

        finally:
            cursor.close()

# function to remove employee given id
def remove():
    id = input("Enter Employee ID: ")

    if not check(id):
        print("Employee doesn't exist")
        return
    
    else:
        query = 'DELETE FROM employees WHERE id=%s'
        data = (id,)
        cursor = connection.cursor

        try:
            cursor.execute(query, data)
            
            connection.commit()
            print("Employee Removed Successfully.")
        
        except mysql.connector.Error as e:
            print(f'Error: {e}')
            connection.rollback()

        finally:
            cursor.close()



# function for promoting employee
def promote():
    id = input("Enter Employee ID: ")

    if not check(id):
        print("Employee doesn't exist")
        return
    
    else:
        try:
            incr = float(input("Enter Salary Increase: "))

            query = 'SELECT salary FROM employees WHERE id=%s'
            data = (id,)
            cursor = connection.cursor()

            cursor.execute(query, data)

            # fetch salary of employee with given id
            curr = cursor.fetchone()[0]
            new = curr + incr

            update = "UPDATE employees SET salary=%s WHERE id=%s"
            data_new = (new, id)

            cursor.execute(update, data_new)

            connection.commit()
            print("Employee Promoted Successfully. Employee's Salary Updated.")

        except (ValueError, mysql.connector.Error) as e:
            print(f'Error: {e}')
            connection.rollback()

        finally:
            cursor.close()


def display():
    try:
        query = 'SELECT * FROM employees'
        cursor = connection.cursor()
        cursor.execute()

        table = cursor.fetchall()
        for employee in table:
            print("Employee Id : ", employee[0])
            print("Employee Name : ", employee[1])
            print("Employee Post : ", employee[2])
            print("Employee Salary : ", employee[3])
            print("------------------------------------")
    
    except mysql.connector.Error as e:
        print(f'Error: {e}')

    finally:
        cursor.close()


def menu():
    while True:
        print("\nWelcome to Employee Management Record\n"
            "Press:\n"
            "1 to Add Employee\n"
            "2 to Remove Employee\n"
            "3 to Promote Employee\n"
            "4 to Display Employees\n"
            "5 to Exit")

        input = input("Enter choice: ")

        if input == '1':
            add()
        elif input == '2':
            remove()
        elif input == '3':
            promote()
        elif input == '4':
            display()
        elif input == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    menu()