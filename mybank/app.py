from flask import Flask,request,jsonify,render_template
from db import getConnection
from autogeneration import generateTransactionId,generateAccNo
import pymysql

app = Flask("__name__")
#api for checking connection
@app.route("/")
def home():
    return render_template("index.html")
#api for checking connection
#create a route for createcystomer.html
@app.route("/createCustomer")
def createCustomer():
    return render_template("createCustomer.html")

@app.route("/")
def home():
    d = {"message":"server running well"}
    return jsonify(d)
@app.route("/insertData",methods=["Post"])
def insertData():
    print(data)
    data = request.form
    cname = data["name"]
    cmobile = data["mob"]
    cemail = data["email"]
    caccno = data["accno"]
    caccno = generateAccNo()
    cbalance = data["balance"]
    password = "Test@123"  
    
    conn = getConnection() 
    cmd = conn.cursor()
    cmd.execute('''
                Insert into customer
                (cname,cmobile,cemail,accno,balance,password)
                values
                (%s,%s,%s,%s,%s,%s);'''
                ,(cname,int(cmobile),cemail,caccno,cbalance,password))
    conn.commit()
    conn.close()
    return jsonify({"message":"customer inserted to db"})
# api to delete customer data
@app.route("/deleteCustomer",methods=["POST"])
def deleteCustomer():
    data = request.get_json()
    caccno = data["accno"]
    conn = getConnection()
    cmd = conn.cursor()
    cmd.execute("DELETE FROM CUSTOMER WHERE accno=%s",(caccno,))
    conn.commit()
    conn.close()
    return jsonify({"message":f"{caccno} person data deleted!!!!"})
#create api to update the cusomer details
@app.route("/updateCustomer",methods=["POST"])
def updateCustomer():
     
    data = request.get_json()
    caccno = data["caccno"]
    uname = data["uname"]
    umobile = data["umobile"]
    uemail = data["uemail"]
    upassword = data["upassword"]
    conn = getConnection()
    cmd = conn.cursor()
    cmd.execute("SELECT cname,cmobile,cemail,password FROM customer")
    d = cmd.fetchone()
    conn.close()
    print(d)
    cname = d[0]
    cmobile = int(d[1])
    cemail  = d[2]
    cpassword = d[3]
    if uname == "":
        uname = cname
          
    if umobile == "":
        umobile = cmobile
          
    if uemail == "":
        uemail = cemail
          
    if upassword == "":
        upassword = cpassword
     
     

    conn = getConnection()
    cmd = conn.cursor()
    cmd.execute('''
                UPDATE CUSTOMER
                SET
                cname=%s,
                cmobile=%s,
                cemail=%s,
                password=%s
                where accno=%s''',
                (uname,umobile,uemail,upassword,caccno))
    conn.commit()
    conn.close()
     

#api forb deposite to customer api
@app.route("/deposite",methods=["POST"])
def deposite():
    data = request.get_json()
    caccno = data["accno"]
    amt = data["amt"]
    conn = getConnection()
    cmd  = conn.cursor(pymysql.cursors.DictCursor)
    cmd.execute("SELECT balance FROM CUSTOMER WHERE accno=%s;",(caccno,))
    data = cmd.fetchone()
    print(data)
    #deposite means addind adding amt to existing balance
    updatedB  = amt + float(data["balance"])
    cmd.execute("UPDATE CUSTOMER SET balance=%s where accno=%s;",(updatedB,caccno))
    conn.commit()
    conn.close()

    return jsonify({"msg":f"{amt} is deposited successfully updated balance is {updatedB}"})



if __name__ == "__main__":
    app.run(debug=True)