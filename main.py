

from flask import Flask, send_from_directory, current_app
from flask import render_template
from flask import request

import pyodbc


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', msg = '')


@app.route('/login', methods=['post'])
def login():
    username = request.form['txtUserName']
    if (username==''):
        msg = 'Please Enter Username..'
        return render_template('index.html', msg=msg)
    else:
        chkCreate = request.form.get('chkCreate')
        if(chkCreate):
            return render_template('AddPic.html')

        else:
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=picshareserver.database.windows.net;DATABASE=Picshare;UID=sam1991;PWD=azure2018.')
            cursor = cnxn.cursor()
            cursor.execute("SELECT pictitle, createddate, nooflikes, picture, Id  FROM picdata where username = '"+username+"'")
            data = cursor.fetchall()
            msg = ''
            return render_template('index.html',msg = msg, username=username, data = data)


def ShowData():
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=picshareserver.database.windows.net;DATABASE=Picshare;UID=sam1991;PWD=azure2018.')
    cursor = cnxn.cursor()
    cursor.execute("SELECT pictitle, createddate, nooflikes, picture  FROM picdata")
    data = cursor.fetchall()
    msg = 'none'
    return render_template('index.html', msg=msg, username='Sam', data=data)


@app.route('/increaselikes/<dataid>')
def increaselikes(dataid):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=picshareserver.database.windows.net;DATABASE=Picshare;UID=sam1991;PWD=azure2018.')
    cursor = cnxn.cursor()
    cursor.execute("SELECT nooflikes  FROM picdata where Id = " +dataid)
    data = cursor.fetchone()
    nooflikes = data[0]
    nooflikes = nooflikes + 1
    updatequery = "update picdata set nooflikes ="+ str(nooflikes) +" where Id=" +dataid
    cursor.execute(updatequery)
    cnxn.commit()
    #ShowData()
    return render_template('index.html', msg='liked..')


@app.route('/addpicture', methods=['post'])
def addpicture():
    file = request.files['filename']
    file.save(file.filename)
    filename = file.filename
    username = request.form['txtusername']
    #filename = 'sam.jpg'
    #imagedata = request.files['filename'].read()
    pictitle = request.form['txttitle']
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=picshareserver.database.windows.net;DATABASE=Picshare;UID=sam1991;PWD=azure2018.')
    cursor = cnxn.cursor()
    insertquery = "insert into picdata ( Username, pictitle, createddate, nooflikes, picture) values ('"+username+"', '"+pictitle+"', getdate(), 1, '"+ filename +"')"
    cursor.execute(insertquery)
    cnxn.commit()
    msg = 'Picture added successfully..'
    return  render_template('AddPic.html', msg = msg)


if __name__ == '__main__':
    app.run()