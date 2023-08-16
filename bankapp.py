import sqlite3
import time,os

conn = sqlite3.connect('bank216.db')
cur = conn.cursor()

cur.execute('''
      CREATE TABLE IF NOT EXISTS Account(
      name VARCHAR(10),
      acc_no INTEGER(10) PRIMARY KEY,
      dob VARCHAR(10),
      contact INTEGER,
      passw INTEGER,
      balance INTEGER
      )
      ''')
cur.execute('''
       CREATE TABLE IF NOT EXISTS Transaction1(
       transaction_id INTEGER PRIMARY KEY,
       acc_no INTEGER(10),
       transaction_type TEXT,
       amount INTEGER,
       FOREIGN KEY(acc_no) REFERENCES Account(acc_no)
       )
       ''')

def main():

    print("--------------------Welcome to the Dena Bank--------------------")

    print("1.OPEN NEW ACCOUNT")

    print("2.DEPOSIT AMOUNT")

    print("3.WITHDRAW MONEY")

    print("4.DISPLAY MINI  STATEMENT")

    print("Thank You for visiting our Bank")
    choice = input("Enter the task you want to perform:  ")
    print("\n")
    if (choice == '1'):
        open_acc()
    elif (choice == '2'):
        deposit()
    elif (choice == '3'):
        withdraw_money()
    elif(choice =='4'):
        disp_mini_statement()
    else:
        print("Invalid option")
        main()



def open_acc():

    nm = input("Enter your good name:  ")
    acc = input(" Enter the Account No:  ")
    date = input("Enter your date of birth:  ")
    contact = int(input("Enter your contact number:  "))
    passw = int(input("Enter password. It should be in numbers!  "))
    ob = int(input("Enter the opening balance:  "))
    cur.execute('''
        INSERT INTO Account(name,acc_no,dob,contact,passw,balance)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nm, acc, date, contact, passw, ob))
    conn.commit()
    cur.execute('select * from Account')
    a = cur.fetchone()
    print("Username:{}\nA\c Number: {}".format(a[0],a[1]))
    print("congratulations your account has been opened")
    # cur.execute('select * from Amount')
    # x = cur.fetchall()
    # print(x)
    time.sleep(3)
    main()

def deposit():

    account_no = int(input("Enter your account  no  "))
    amount= int(input("Enter the amount you want to deposit in your account  "))
#update account balance
    cur.execute('''
                UPDATE Account SET balance = balance+? WHERE acc_no = ?''', (account_no,amount)
            )
#insert transaction record
    cur.execute('''
            INSERT INTO Transaction1(acc_no,transaction_type,amount)
            VALUES (?,?,?)
        ''', (account_no,'deposit',amount))
    conn.commit()
    cur.execute('select * from Account')
    s = cur.fetchone()
    print("Username:{}\nA\c Number: {}".format(s[0], s[1]))



    print("Congratulations your money has been deposited")
    time.sleep(3)
    exit()
    main()

def withdraw_money():

    account_no = int(input("Enter your account number  "))
    withdraw = int(input("Enter the amount you want to withdraw  "))
    #to check if suffiecent balance is there
    cur.execute('''
                    SELECT  balance FROM Account  WHERE acc_no = ?''', (account_no,)
                )
    balance = cur.fetchone()

    if (balance[0] >= withdraw):
        cur.execute('''
                        UPDATE Account SET balance = balance-? WHERE acc_no = ?''', (account_no,withdraw)
                    )
        #insert withdrawl transaction

        cur.execute('''
                INSERT INTO Transaction1(acc_no,transaction_type,amount)
                VALUES (?,?,?)
            ''', (account_no, 'withdraw', withdraw))
        cur.execute('select * from Transaction1')
        s = cur.fetchall()
        conn.commit()
        cur.execute('select * from Account')
        z = cur.fetchone()
        print("Username:{}\nA\c Number: {}".format(z[0], z[1]))

        print("------WITHDRAWL SUCCESSFUL------")



    else:
        print("INSUFFICIENT BALANCE")
    time.sleep(3)

    exit()
    main()



def disp_mini_statement():

    with open("bank.txt","w") as f:
        acc_no = int(input("Enter your account number "))
        cur.execute('''
                        SELECT * FROM Transaction1  WHERE acc_no = ?''', (acc_no,)
                )
        transactions=cur.fetchall()
        if transactions:
          f.write("Mini statement for account number "  )
          f.write(f"{acc_no}\n")
          f.write("-----------------------------------------\n")
          for transaction in transactions:
            f.write("Transaction id  ")
            f.write(f"{transaction[0]}\n")
            f.write("Transaction Type:  ")
            f.write(f"{transaction[2]}\n")
            f.write("Amount:"   )
            f.write(f"{transaction[3]}\n")
            f.write("--------------------\n")
        else:
             f.write("No transaction history")
    with open("bank.txt","r") as f:
         content=f.read()
         print(content)
         time.sleep(3)
    exit()
    main()

main()
cur.close()
