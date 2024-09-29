from flask import Flask, render_template, request 
from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import os
import datetime

app = Flask(__name__)


global details, user


def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:8545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'EHR.json' #counter feit contract code
    deployed_contract_address = '0xa96dE0AD5fBc1b88399877d6e71AC333561Cfc20' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUsers().call()
    if contract_type == 'report':
        details = contract.functions.getreport().call()
    if contract_type == 'appointments':
        details = contract.functions.getappointments().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'EHR.json' #Counter feit contract file
    deployed_contract_address = '0xa96dE0AD5fBc1b88399877d6e71AC333561Cfc20' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'report':
        details+=currentData
        msg = contract.functions.addreport(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'appointments':
        details+=currentData
        msg = contract.functions.addappointments(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)



@app.route('/AddDoctorAction', methods=['POST'])
def AddDoctorAction():
    if request.method == 'POST':
        
        username = request.form['t1']
        password = request.form['t2']
        number = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        spe = request.form['t6']
        exp = request.form['t7']

        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0]== 'Doctor' and array[1] == username:
                status = username + " Already Exists"
                context = status  
                return render_template('DoctorRegister.html', msg=context)
                break

        if status == "none":
            data = "Doctor#"+username+"#"+password+"#"+number+"#"+email+"#"+address+"#"+spe+"#"+exp+"\n"
            saveDataBlockChain(data, "adduser")
            context = "SignUp Completed and details are saved to blockchain"  
            return render_template('DoctorRegister.html', msg=context)
        else:
            context = 'Error in signup process'  
            return render_template('DoctorRegister.html', msg=context)


@app.route('/DoctorLoginAction', methods=['POST'])
def DoctorLoginAction():
    if request.method == 'POST':
        global user
        username = request.form['t1']
        password = request.form['t2']
        user = username
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Doctor' and array[1] == username and array[2] == password:
                status = 'success'
                break

        if status == 'success':
            context = username + ' Welcome'
            return render_template('DoctorScreen.html', msg=context)
        else:
            context = 'Invalid Details'
            return render_template('DoctorLogin.html', msg=context)


@app.route('/AddPatientAction', methods=['POST'])
def AddPatientAction():
    if request.method == 'POST':
        
        username = request.form['t1']
        password = request.form['t2']
        number = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        age = request.form['t6']
        prev = request.form['t7']
        bmi = request.form['t8']


        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0]== 'Patient' and array[1] == username:
                status = username + " Already Exists"
                context = status  
                return render_template('PatientRegister.html', msg=context)
                break

        if status == "none":
            data = "Patient#"+username+"#"+password+"#"+number+"#"+email+"#"+address+"#"+age+"#"+prev+"#"+bmi+"\n"
            saveDataBlockChain(data, "adduser")
            context = "SignUp Completed and details are saved to blockchain"  
            return render_template('PatientRegister.html', msg=context)
        else:
            context = 'Error in signup process'  
            return render_template('PatientRegister.html', msg=context)

@app.route('/PatientLoginAction', methods=['POST'])
def PatientLoginAction():
    if request.method == 'POST':
        global user
        username = request.form['t1']
        password = request.form['t2']
        user = username
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Patient' and array[1] == username and array[2] == password:
                status = 'success'
                break

        if status == 'success':
            context = username + ' Welcome'
            return render_template('PatientScreen.html', msg=context)
        else:
            context = 'Invalid Details'
            return render_template('PatientLogin.html', msg=context)

@app.route('/PatientInformation', methods=['GET', 'POST'])
def PatientInformation():
    if request.method == 'GET':
        
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Patient Username', 'Patient Password','Patient Number', 'Patient Email','Patient Address' ,'Patient Age','Patient Previous History','Patient BMI']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")
            if array[0] == 'Patient':
                output += '<tr>'
                for cell in array[1:9]:
                    output += f'<td>{font}{cell}{font}</td>'
                output += '</tr>'
        output += '</table><br/><br/><br/>'

        return render_template('PatientInformation.html', data=output)

def getusernames():
    readDetails('adduser')
    arr = details.split("\n")
    user_names = []

    for i in range(len(arr) - 1):
        array = arr[i].split("#")
        if array[0] == 'Patient':
            user_names.append(array[1])

    return user_names


@app.route('/AddReport', methods=['GET'])
def AddReport():
    global user
    username = getusernames()
    return render_template('AddReport.html', username_all=username)


@app.route('/AddReport', methods=['POST'])
def AddReports():
    global user
    status = "none"
    name = request.form['username']
    des = request.form['t1']
    file = request.files['t2']
    
    filename = file.filename
    print("@@ Input posted = ", filename)
    file_path = os.path.join('static/files/', filename)
    file.save(file_path)

   
    data = name+"#"+des+"#"+filename+"\n"
    saveDataBlockChain(data, "report")
    context = 'Report Added Successfully to Blockchain.'
    return render_template('AddReport.html', msg=context)
   




@app.route('/CheckMedicalReport', methods=['GET', 'POST'])
def CheckMedicalReport():

    if request.method == 'GET':
        global user
        
        output = '<table border=1 align=center width=100%>'
        font = '<font size=3 color=black>'
        headers = ['Description','Download']

        output += "<tr>"
        for header in headers:
            output += "<th>" + font + header + "</th>"
        output += "</tr>"

        
        readDetails('report')

        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user:
                output += "<tr><td>" + font + array[1] + "</td>"
                output += f'<td><a href="/static/files/{array[2]}" download="{array[2]}">Download</a></td>'

        output += "</table><br/><br/><br/>"

        return render_template('CheckMedicalReport.html', msg=output)


@app.route('/DoctorInformation', methods=['GET', 'POST'])
def DoctorInformation():

    if request.method == 'GET':
        global user
        
        output = '<table border=1 align=center width=100%>'
        font = '<font size=3 color=black>'
        headers = ['Doctor Name','Doctor Number','Doctor Email','Doctor Address','Doctor Specialization','Doctor Experience']

        output += "<tr>"
        for header in headers:
            output += "<th>" + font + header + "</th>"
        output += "</tr>"

        
        readDetails('adduser')

        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Doctor':
                output += "<tr><td>" + font + array[1] + "</td>"
                output += "<td>" + font + array[3] + "</td>"
                output += "<td>" + font + array[4] + "</td>"
                output += "<td>" + font + array[5] + "</td>"
                output += "<td>" + font + array[6] + "</td>"
                output += "<td>" + font + array[7] + "</td></tr>"

        output += "</table><br/><br/><br/>"

        return render_template('DoctorInformation.html', msg=output)

def getdoctorname():
    readDetails('adduser')
    arr = details.split("\n")
    doctor_names = []

    for i in range(len(arr) - 1):
        array = arr[i].split("#")
        if array[0] == 'Doctor':
            doctor_names.append(array[1])

    return doctor_names

@app.route('/AddAppointment', methods=['GET'])
def AddAppointments():
    global user
    username = getdoctorname()
    return render_template('AddAppointment.html', username_all=username)


@app.route('/AddAppointment', methods=['POST'])
def AddAppointment():
    global user
    name = request.form['username']
    time = request.form['t1']
   
    data = user+"#"+name+"#"+time+"\n"
    saveDataBlockChain(data, "appointments")
    context = 'Appointment booked successfully'
    return render_template('AddAppointment.html', msg=context)

@app.route('/ViewAppointment', methods=['GET', 'POST'])
def ViewAppointment():
    if request.method == 'GET':
        global user
        
        output = '<table border=1 align=center width=100%>'
        font = '<font size=3 color=black>'
        headers = ['Patient Name','Appointment Timings and Date']

        output += "<tr>"
        for header in headers:
            output += "<th>" + font + header + "</th>"
        output += "</tr>"

        
        readDetails('appointments')

        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == user:
                output += "<tr><td>" + font + array[0] + "</td>"
                output += "<td>" + font + array[2] + "</td></tr>"

        output += "</table><br/><br/><br/>"

        return render_template('ViewAppointment.html', data=output)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/ViewAppointment', methods=['GET', 'POST'])
def ViewAppointmentss():
    if request.method == 'GET':
       return render_template('ViewAppointment.html', msg='')

@app.route('/AddAppointment', methods=['GET', 'POST'])
def AddAppointmentss():
    if request.method == 'GET':
       return render_template('AddAppointment.html', msg='')

@app.route('/PatientScreen', methods=['GET', 'POST'])
def PatientScreens():
    if request.method == 'GET':
       return render_template('PatientScreen.html', msg='')

@app.route('/DoctorInformation', methods=['GET', 'POST'])
def DoctorInformations():
    if request.method == 'GET':
       return render_template('DoctorInformation.html', msg='')

@app.route('/PatientLogin', methods=['GET', 'POST'])
def PatientLogins():
    if request.method == 'GET':
       return render_template('PatientLogin.html', msg='')

@app.route('/AddReport', methods=['GET', 'POST'])
def AddReportss():
    if request.method == 'GET':
       return render_template('AddReport.html', msg='')

@app.route('/DoctorLogin', methods=['GET', 'POST'])
def DoctorLogin():
    if request.method == 'GET':
       return render_template('DoctorLogin.html', msg='')

@app.route('/DoctorRegister', methods=['GET', 'POST'])
def DoctorRegister():
    if request.method == 'GET':
       return render_template('DoctorRegister.html', msg='')

@app.route('/DoctorScreen', methods=['GET', 'POST'])
def DoctorScreen():
    if request.method == 'GET':
       return render_template('DoctorScreen.html', msg='')

@app.route('/PatientRegister', methods=['GET', 'POST'])
def PatientRegister():
    if request.method == 'GET':
       return render_template('PatientRegister.html', msg='')

@app.route('/PatientInformation', methods=['GET', 'POST'])
def PatientInformations():
    if request.method == 'GET':
       return render_template('PatientInformation.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('index.html', msg='')

    
if __name__ == '__main__':
    app.run()       
