import mysql.connector
import flask as f
from simulation_functions import *
import pickle

app = f.Flask(__name__, template_folder="", static_folder="")
app.config.update(TEMPLATES_AUTO_RELOAD=True)
prices = {}
table = ""
chand = None
pwd = ""
tempprices = {}


def setup():
    global tempprices
    global pwd
    global chand
    global table
    global prices
    print("\t\tWelcome to the stock market simulation")
    pwd = input("Enter your MySQL password: ")
    db = mysql.connector.connect(host="localhost", user="root", password=pwd)
    cur = db.cursor()
    cur.execute("create database if not exists simulations;")
    cur.execute("use simulations;")
    db.close()
    cur.close()
    try:
        ch = int(
            input(
                "1- Simulation already exists\n2- You want to create a simulation\n3. Update the prices of your simulation(or add more companies)\n--> "
            )
        )
        if ch == 1:
            table = input("Enter the name of the table: ")
            db = mysql.connector.connect(
                host="localhost", user="root", password=pwd, database="simulations"
            )
            cur = db.cursor()
            cur.execute("show tables;")
            for i in cur.fetchall():
                print(i)
                if table in i:
                    break
            else:
                db.close()
                cur.close()
                raise "error"

            with open("price.bin", "rb") as f:
                prices = pickle.load(f)
                chand = pickle.load(f)

        elif ch == 2:
            table = input("Enter the name of the table: ")
            db = mysql.connector.connect(
                host="localhost", user="root", password=pwd, database="simulations"
            )
            cur = db.cursor()
            cur.execute("show tables;")
            for i in cur.fetchall():
                print(i)
                if table in i:
                    print("table already exists")
                    db.close()
                    cur.close()
                    raise "error"

            n = int(input("Enter number of companies: "))
            chand = float(input("Give a starting cash in hand: "))
            for i in range(n):
                tempcomp = input("Enter name of the company: ").lower()
                tempprice = float(
                    input("Enter the price for one share of that company: ")
                )
                tempprices.update({tempcomp: tempprice})
            else:
                prices.update(tempprices)

            cur.execute(
                f"create table if not exists {table}(ID varchar(255) primary key, cash_in_hand float not null default {chand}, check (cash_in_hand>=0));"
            )
            print("prices", prices)
            print(prices.values())
            for i in list(prices.keys()):
                cur.execute(f"alter table {table} add {i} int default 0")
                cur.execute(f"alter table {table} add constraint check({i}>=0);")
            db.close()
            cur.close()
            with open("price.bin", "wb") as f:
                pickle.dump(prices, f)
                pickle.dump(chand, f)
        elif ch == 3:
            db = mysql.connector.connect(
                host="localhost", user="root", password=pwd, database="simulations"
            )
            cur = db.cursor()
            table = input("Enter name of the simulation: ").lower()
            cur.execute("show tables;")
            for i in cur.fetchall():
                print(i)
                if table in i:
                    break
            else:
                print("Simulation doesn't exist")
                db.close()
                cur.close()
                raise "error"

            with open("price.bin", "rb") as f:
                prices = pickle.load(f)
                chand = pickle.load(f)
            n = int(
                input(
                    "Enter number of companies you want to change the price for(this includes the companies you want to add, if any): "
                )
            )

            for i in range(n):
                tempcomp = input("Enter name of the company: ").lower()
                tempprice = float(
                    input("Enter the price for one share of that company: ")
                )
                if tempcomp in list(prices.values())[0].keys():
                    tempprices.update({tempcomp: tempprice})
                elif tempcomp not in list(prices.values())[0].keys():
                    tempprices.update({tempcomp: tempprice})
                    cur.execute(f"alter table {table} add {tempcomp} int default 0")
                    cur.execute(
                        f"alter table {table} add constraint check({tempcomp}>=0);"
                    )
            else:
                prices.update(tempprices)

            db.close()
            cur.close()
            with open("price.bin", "wb") as f:
                pickle.dump(prices, f)
                pickle.dump(chand, f)

    except Exception as e:
        print(e)
        print("Invalid input")
        quit()


app.before_request_funcs = [(None, setup())]


@app.route("/", methods=["POST", "GET"])
def home():
    display = "No errors were caught."
    if f.request.method == "POST":
        buybtn = f.request.form.get("buy")
        sellbtn = f.request.form.get("sell")
        admno = f.request.form["admno"]
        comp = f.request.form["company"].lower()
        try:
            shares = int(f.request.form["noshares"])
            if buybtn:
                msg = insert(admno, comp, shares, prices, table, chand, pwd)
                display = msg
                if msg:
                    # print(type(str(msg)))
                    # print(str(msg)[:4])
                    # print(msg)
                    if str(msg)[:4] == "3819":
                        display = "You don't have enough money."
                    elif str(msg)[:4] in ("1064", "1054"):
                        display = "Inputted admission number is invalid."

            elif sellbtn:
                msg = delete(admno, comp, shares, prices, table, pwd)
                if msg:
                    display = msg
                    print(msg)
                    if str(msg)[:4] == "3819":
                        display = "You don't have enough shares."
                    elif str(msg)[:4] in ("1064", "1054"):
                        display = "Inputted admission number is invalid."

        except Exception as e:
            display = "Inputted number of shares is invalid."
    db = mysql.connector.connect(
        host="localhost", user="root", password=pwd, database="simulations"
    )
    cur = db.cursor()
    cur.execute(f"select * from {table};")
    data = cur.fetchall()
    db.close()
    cur.close()
    cur.close()
    print(table)
    print(prices)
    return f.render_template(
        "index.html",
        data=data,
        display=display,
        prices=list(prices.items()),
        companies=prices.keys(),
    )


if __name__ == "__main__":
    app.run()
