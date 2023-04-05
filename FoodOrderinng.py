# Menu viewing application - This project allows the customer to view the menu of a restaurant and choose food items according to their preference.
# Food ordering system - With this project, customers can place their food orders by entering their name, mobile number, food ID, and food quantity.
# Order tracking system - The system provides an order ID to the customer, which they can use to track the status of their food order.
# Online food ordering application - The project allows the customers to place their food orders online and get them delivered to their doorstep.
# Restaurant management system - This project is a part of the restaurant management system that helps the customers to view the menu and place their orders.

''' The project is a Python-based food order system that allows users to view the menu,of a restaurant and choose food items according to their preference. customers can order their food by entering their name, mobile number, food ID, and food quantity. 
The system provides an order ID to the customer,which they can use to track the status of their food order.in this project I have done exception handling to ensure entry of wrong data. The system is designed to enhance user experience and provide a seamless ordering process for customers.'''

import mysql.connector as mysql
# The mysql.connector module to connect to a MySQL database hosted on the local machine.
from tabulate import tabulate
# hear we imports the tabulate module, which can be used to display the query results in a nicely formatted table.
my_database = mysql.connect(host="localhost", user="root", password="Kunal1996@", database="food")
cursor = my_database.cursor()
#the database name is food 

cursor.execute("create table if not exists food (food_id int primary key auto_increment, foodname varchar(100), food_type varchar(100), price int, check(food_type='veg' or food_type='non-veg'))")

# alter table food   auto_increment = 1;

def view_menu():
# hear we create a view_menu function
# in that function we used food_type 
    food_type = input("  WHAT WOULD YOU LIKE TO EAT VEG,NONVEG OR BOTH? :- ") 
    food_type = food_type.lower()
    if food_type == "veg":
        sql = "SELECT * FROM food WHERE food_type = 'veg'"
   
    elif food_type == "nonveg":
        sql = "SELECT * FROM food WHERE food_type = 'non-veg'"

    elif food_type == "both":
        sql="select * from food"

    else:
        print("Invalid choice!")
        return

    cursor.execute(sql)
    result = cursor.fetchall()
# display  results in a nicely table formatted .
# the main purpose of this tabulate function to makes it easier for the user to read and understand the query result.
    headers = ["Food Id", "Food Name", "Food Type", "Price"]
    print(tabulate(result, headers=headers, tablefmt="grid"))


# hear i create a table name is orderFood 
# in that table we use auto_increment value 
cursor.execute("create table if not exists OrderFood( order_id int primary key auto_increment, Name varchar(100),MOBNumber varchar(20),Food_id int, Food_qty int)")

def order_food():
# This is a Python function that allows the user to place an order 
# for a specific food item 
# by entering
#  their name, mobile number, food ID, and food quantity.
    name = input("Enter your name: ")
# The function first prompts the user for their name and mobile number, 
# ensuring that the mobile number is a valid 10-digit integer. 
    while True:
        try:
            mob_number = int(input("Enter your mobile number (10 digits): "))
            if len(str(mob_number)) == 10:
                break
            else:
                print("Mobile number must be 10 digits long!")
        except ValueError:
            print("Invalid mobile number!")# if youser enter a wrong number or abc,** that time gives invalid number 
# It then prompts the user for the food ID, and checks whether the entered ID exists in the "food" table. 
# If not, it prompts the user to enter a valid ID.
    food_id = int(input("Enter food ID: "))
    a=[]
    sql= "select food_id from Food"
    cursor.execute(sql)
    A=cursor.fetchall()
    for i in A:
        a.append(int(i[0]))
    while food_id not in a:
        print("Invalid food_id!!!")
        food_id=int(input("Reenter food ID: "))
    food_qty = int(input("Enter quantity: "))
# After the user enters a valid food ID, 
# the function prompts them for the quantity, 
# ensuring that the quantity is between 1 and 10. 
# If not, it asks the user to re-enter a valid quantity
    while food_qty>10 or food_qty<1:
        print("Minimum and Maximum quantitiy allowed are 1 and 10 ")
        food_qty = int(input("Reenter quantity: "))

    sql = "INSERT INTO OrderFood (Name, MOBNumber, Food_id, Food_qty) VALUES (%s, %s, %s, %s)"
    order = (name, mob_number, food_id, food_qty)
    cursor.execute(sql, order)
    my_database.commit()
    sql="select max(order_id) from OrderFood"
    cursor.execute(sql)
    A=cursor.fetchall()
# The function then fetches the maximum order ID generated by the database for the current session,
#  and displays it to the user as a confirmation message.
    print("YOUR ORDER ID : ",A[0][0]," HAS BEEN GENERATED SUCCESSFUL")


def view_order():
    while True:
        try:
# asks the user to enter their order ID, and checks 
# if it exists in the "OrderFood" table. 
# If the order ID is invalid, it asks the user to re-enter a valid ID.
            order_id = int(input("Enter your order_Id: "))

            a=[]
            sql="select order_id from OrderFood"
            cursor.execute(sql)
            o=cursor.fetchall()
            for i in o:
                a.append(int(i[0]))
            if order_id in a:
                break
            else:
                print("Order ID does not exist!")
        except ValueError:
            print("Please enter valid order ID")

    sql = "SELECT order_id, Name, MOBNumber, Food_id FROM OrderFood WHERE Order_Id = %s"


    cursor.execute(sql, (order_id,))
    result = cursor.fetchall()

    sql="SELECT food_qty, food_id FROM orderfood WHERE order_id = %s"
    cursor.execute(sql, (order_id,))
    food_qty=cursor.fetchall()
    # print(food_qty[0][0])   it well give me 1

    sql2="SELECT price FROM food WHERE food_id = %s"
    cursor.execute(sql2, (food_qty[0][1],))
    price=cursor.fetchall()

    sql="SELECT foodname FROM food WHERE food_id = %s"
    cursor.execute(sql, (food_qty[0][1],))
    foodname=cursor.fetchall()
    result=list(result[0]) 
    # print(result)   [2, 'pritam g khade', '9881563724', 11]
    result.append(foodname[0][0]) # get a pizza name and append it
    
    total_price=food_qty[0][0] * price[0][0]
    headers = ["Order ID", "Name", "Mobile Number", "Food ID","Food Name" ,"Food Quantity","Total_Price"]
    result=result + [int(food_qty[0][0]), total_price]
    result=tuple(result)
    result=[result]
    print(tabulate(result, headers=headers, tablefmt="grid"))

def exit_program():
    print("Thank you for comming")



def display_menu():
    print("------------FOOD_ORDERING_SYSTEM!-------------")
    print("1. View Menu")
    print("2. Order Food")
    print("3. View Order")
    print("0. Exit")


def food_ordering_system():
    while True:
        display_menu()
        user_choice = int(input("Enter your choice: "))
        match user_choice:
            case 1:
                view_menu()
            case 2:
                order_food()
            case 3:
                view_order()
            case 0:
                exit_program()
                break
            case _:
                print("Invalid choice! Please enter a number between 0 and 3.")


def run():
    try:
        food_ordering_system()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        my_database.close()

run()
