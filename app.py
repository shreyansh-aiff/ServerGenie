import requests
import json
from requests.auth import HTTPBasicAuth
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
API_KEY = 'GWLhnarUnn7hVUcRG8tze7Eh2CJwtOreszqogw1e'
baseUrl = "https://bvsai1b537.execute-api.ap-south-1.amazonaws.com/dev"

def getServers():
    headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    return requests.get(f"{baseUrl}/get-servers",  headers=headers).json()

def getApplications():
    headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    return requests.get(f"{baseUrl}/get-applications", headers=headers).json()

@app.route('/home')
def home():
    servers = getServers()
    applications = getApplications()
    return render_template('home.jinja2', title='Homepage', servers = servers, applications = applications)

@app.route('/post/addServer')
def addServer():
    return render_template('addServer.jinja2', title = 'addServerForm')

@app.route('/post/getSpecificServer')
def getSpecificServer():
    return render_template('getSpecificServer.jinja2', title = 'getSpecificServerForm')

@app.route('/post/deleteServer')
def deleteServer():
    return render_template('deleteServer.jinja2', title = 'deleteServerForm')


@app.route('/post/addApplication')
def addApplication():
    return render_template('addApplication.jinja2', title = 'addApplicationForm')

@app.route('/post/getSpecificApplication')
def getSpecificApplication():
    return render_template('getSpecificApplication.jinja2', title = 'getSpecificApplicationForm')

@app.route('/post/deleteApplication')
def deleteApplication():
    return render_template('deleteApplication.jinja2', title = 'deleteApplicationForm')

@app.route('/post/getSpecificServerDetails', methods=["POST"])
def getSpecificServerAPICall():
    location = request.form.get('location')
    osType = request.form.getlist('os-type')
    print(location, osType)
    # serverId = request.form.get('server-id')
    # headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    # print(serverId)
    # response = requests.get(f"{baseUrl}/get-servers?id={serverId}", headers=headers).json()
    # return render_template('specificServer.jinja2', data = response)

@app.route('/post/addApplicationAPICall', methods=["POST"])
def addApplicationAPICall():
    toAdd = {
        "application-id": {"S": request.form.get('app-id')},
        "server-id": {"S": request.form.get('server-id')},
        "version": {"S": request.form.get('version')},
        "port": {"N": str(request.form.get('port'))},
        'Status Active': {
            'BOOL': True if request.form.get('status') == 'True' else False
        }
    }
    addApplicationUrl = f"{baseUrl}/add-application"
    headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    response = requests.post(addApplicationUrl, json = toAdd, headers=headers)

    print(response)
    return redirect(url_for('home'))

@app.route('/post/deleteSpecificServerAPICall', methods=["POST"])
def deleteSpecificServerAPICall():
    serverId = request.form.get('server-id')
    print(serverId)
    deleteServerUrl = f"{baseUrl}/delete-server?id={serverId}"
    headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    response = requests.get(deleteServerUrl, headers=headers)

    print(response)
    return redirect(url_for('home'))

@app.route('/post/deleteSpecificApplicationAPICall', methods=["POST"])
def deleteSpecificApplicationAPICall():
    pass

@app.route('/post/deleteSpecificApplicationDetails', methods=["POST"])
def getSpecificApplicationAPICall():
    pass

@app.route('/post/createServer', methods=["POST"])
def create():
    toAdd = {
        "server-id": {"N": request.form.get('server-id')},
        "Name": {"S": request.form.get('server-name')},
        "CPU": {"S": request.form.get('cpu')},
        "Disk Space": {"N": str(request.form.get('diskspace'))},
        "IP": {"S": request.form.get('ip')},
        "Location": {"S": request.form.get('location')},
        "OS": {"S": request.form.get('os')},
        "RAM": {"N": str(request.form.get('ram'))},
        'Status Active': {
            'BOOL': True if request.form.get('status') == 'True' else False
        },
        'Applications': {"N": str(request.form.get('applications'))}
    }

    addServerUrl = f"{baseUrl}/add-server"
    headers = {'Accept': 'application/json', 'x-api-key': API_KEY}
    response = requests.post(addServerUrl, json = toAdd, headers=headers)

    print(response)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)