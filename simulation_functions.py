import mysql.connector
def insert(adno,company,amount,prices,table,chand,pwd):
    try:
        if not adno.isalnum():
            return 'Admission Number is invalid'
        db=mysql.connector.connect(host='localhost', user='root', password=pwd, database='simulations')
        mc= db.cursor()
        mc.execute(f'select cash_in_hand,{company} from {table} where ID=\'{adno}\'')
        fetch= mc.fetchall()
        if fetch==[]:
            print(chand)
            mc.execute(f"insert into {table} (ID,cash_in_hand,{company}) values (\'{adno}\',{chand-(prices[company]*amount)},{amount})")

        else:
            cash=fetch[0][0]
            comp=fetch[0][1]
            mc.execute(f"update {table} set cash_in_hand={cash-prices[company]*amount},{company}={comp+amount} where ID=\'{adno}\'")
        db.commit()
        db.close()
    except Exception as e:
        db.close()
        return e



def delete(adno,company,amount,prices,table,pwd):
    try:
        db=mysql.connector.connect(host='localhost', user='root', password=pwd, database='simulations')
        mc= db.cursor()
        mc.execute(f'select cash_in_hand,{company} from {table} where ID=\'{adno}\'')
        fetch= mc.fetchall()

        if fetch==[]:
            return 'Inputted person does not exist.'
        else:
            cash=fetch[0][0]
            comp = fetch[0][1]
            mc.execute(f"update {table} set cash_in_hand={cash+prices[company]*amount},{company}={comp-amount} where ID=\'{adno}\'")
        db.commit()
        db.close()
    except Exception as e:
        db.close()
        print(e)
        return e
