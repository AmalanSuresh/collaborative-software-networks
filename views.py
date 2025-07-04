from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import io
import base64
import matplotlib.pyplot as plt
from datetime import date
import pymysql
import numpy as np

global username

def Graph(request):
    if request.method == 'GET':
        height = [40, 60, 80, 95]
        bars = ['2010', '2015', '2020', '2025']
        y_pos = np.arange(len(bars))
        plt.figure(figsize = (5, 3)) 
        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.xlabel("Years")
        plt.ylabel("Collaborative Users %")
        plt.xticks(rotation=70)
        plt.title("No of people using Collaborative tool")
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        #plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        plt.clf()
        plt.cla()
        context= {'data':"No of people using Collaborative tool Graph", 'img': img_b64}
        return render(request, 'UserScreen.html', context)       

def UploadCodeAction(request):
    if request.method == 'POST':
        global username
        mid = request.POST.get('t1', False)
        myfile = request.FILES['t2'].read()
        fname = request.FILES['t2'].name
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update distributeModule set status='Completed', module_code_file='"+fname+"' where module_id='"+mid+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if os.path.exists("SoftwareApp/static/files/"+fname):
            os.remove("SoftwareApp/static/files/"+fname)
        with open("SoftwareApp/static/files/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        output = "Module code file "+fname+" successfully submitted to project owner"
        context= {'data':output}
        return render(request, 'UserScreen.html', context) 

def UploadCode(request):
    if request.method == 'GET':
        name = request.GET.get('requester', False)
        output = '<tr><td><font size="3" color="black">Module&nbsp;ID</td><td><input type="text" name="t1" size="10" value="'+name+'" readonly/></td></tr>'
        context= {'data1':output}
        return render(request, 'UploadCode.html', context)   

def Download(request):
    if request.method == 'GET':
        name = request.GET.get('requester', False)
        with open("SoftwareApp/static/files/"+name, "rb") as file:
            data = file.read()
        file.close()        
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response

def UpdateStatus(request):
    if request.method == 'GET':
        global username
        index = 0
        output = "<font size=3 color=red>You dont have any module assignment</font>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM distributeModule where project_owner='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if index == 0:
                    output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Module ID</th><th><font size="3" color="black">Project ID</th>'
                    output+='<th><font size="3" color="black">Project Owner</th><th><font size="3" color="black">Member Name</th><th><font size="3" color="black">Assigned Module Name</th><th><font size="3" color="black">Module Description</th>'
                    output += '<th><font size="3" color="black">End Date</th><th><font size="3" color="blue">Module Code File</th>'
                    output += '<th><font size="3" color="black">Status</th><th><font size="3" color="blue">Download Module Code</th></tr>'
                    index = 1
                output += '<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[4])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[5])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[6])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[7])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[8])+'</td>'
                if row[8] != 'Pending':
                    output +='<td><a href=\'Download?requester='+str(row[7])+'\'><font size=3 color=blue>Click Here</font></a></td></tr>'
                else:
                    output += '<td><font size="3" color="red">Expected Soon</td></tr>'

        with con:    
            cur = con.cursor()
            cur.execute("select * FROM distributeModule where member_name='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if index == 0:
                    output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Module ID</th><th><font size="3" color="black">Project ID</th>'
                    output+='<th><font size="3" color="black">Project Owner</th><th><font size="3" color="black">Member Name</th><th><font size="3" color="black">Assigned Module Name</th><th><font size="3" color="black">Module Description</th>'
                    output += '<th><font size="3" color="black">End Date</th><th><font size="3" color="blue">Module Code File</th>'
                    output += '<th><font size="3" color="black">Status</th><th><font size="3" color="blue">Upload Completed Module Code</th></tr>'
                    index = 1
                output += '<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[4])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[5])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[6])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[7])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[8])+'</td>'
                if row[8] == "Pending":
                    output +='<td><a href=\'UploadCode?requester='+str(row[0])+'\'><font size=3 color=blue>Click Here to Upload</font></a></td></tr>'
                else:
                    output += '<td><font size="3" color="blue">Done</td>'
        output += "</table><br/><br/><br/><br/>"    
        context= {'data':output}
        return render(request, 'UserScreen.html', context)  

def AssignModuleAction(request):
    if request.method == 'POST':
        global username
        project = request.POST.get('t1', False)
        member = request.POST.get('t2', False)
        module = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        end = request.POST.get('t5', False)
        mid = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(module_id) from distributeModule")
            rows = cur.fetchall()
            for row in rows:
                mid = row[0]
                break
        if mid is not None:
            mid = mid + 1
        else:
            mid = 1
        output = "Error in adding module to group member"    
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO distributeModule VALUES('"+str(mid)+"','"+project+"','"+username+"','"+member+"','"+module+"','"+desc+"','"+end+"','Pending','Pending')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = module+" New module created with Module ID = "+str(mid)+"<br/>Module Assigned to Member = "+member 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def ModuleAssignment(request):
    if request.method == 'GET':
        global fileList
        name = request.GET.get('requester', False)
        members = ""
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select group_members FROM project where project_id='"+name+"'")
            rows = cur.fetchall()
            for row in rows:
                members = row[0]
                break
        members = members.split(",")
        output = '<tr><td><font size="3" color="black">Project&nbsp;ID</td><td><input type="text" name="t1" size="10" value="'+name+'" readonly/></td></tr>'
        output += '<tr><td><font size="3" color="black">Choose&nbsp;Group&nbsp;Member</td><td><select name="t2">'
        for i in range(len(members)):
            output += '<option value="'+members[i]+'">'+members[i]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output}
        return render(request, 'AssignModule.html', context)      
        

def AssignModule(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Project ID</th><th><font size="3" color="black">Project Owner</th>'
        output+='<th><font size="3" color="black">Project Tag</th><th><font size="3" color="black">Description</th><th><font size="3" color="black">Group Members</th><th><font size="3" color="black">Start Date</th>'
        output += '<th><font size="3" color="black">End Date</th><th><font size="3" color="blue">Click to Assign Module</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM project where project_owner='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                output += '<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[1])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[2])+'</td><td><font size="3" color="black">'+str(row[3])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[4])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[5])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[6])+'</td>'
                output +='<td><a href=\'ModuleAssignment?requester='+str(row[0])+'\'><font size=3 color=blue>Click Here</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"    
        context= {'data':output}
        return render(request, 'UserScreen.html', context)  

def CreateProjectAction(request):
    if request.method == 'POST':
        global username
        project = request.POST.get('t1', False)
        description = request.POST.get('t2', False)
        group = request.POST.getlist('group')
        start = request.POST.get('t3', False)
        end = request.POST.get('t4', False)
        pid = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select max(project_id) from project")
            rows = cur.fetchall()
            for row in rows:
                pid = row[0]
                break
        if pid is not None:
            pid = pid + 1
        else:
            pid = 1
        output = "Error in adding project to database"    
        members = ','.join(str(x) for x in group)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO project VALUES('"+str(pid)+"','"+username+"','"+project+"','"+description+"','"+members+"','"+start+"','"+end+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = "New project created with Project ID = "+str(pid)+"<br/>Choosen Group Members = "+members 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)         

def CreateProject(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Choose&nbsp;Group&nbsp;Members</td><td><select name="group" multiple>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output}
        return render(request, 'CreateProject.html', context)

def ViewMembers(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%><tr><th><font size="3" color="black">Username</th><th><font size="3" color="black">Qualification</th>'
        output+='<th><font size="3" color="black">Experienced</th><th><font size="3" color="black">Gender</th><th><font size="3" color="black">Contact No</th><th><font size="3" color="black">Email ID</th>'
        output += '<th><font size="3" color="black">Address</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                output += '<tr><td><font size="3" color="black">'+str(row[0])+'</td><td><font size="3" color="black">'+str(row[2])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[3])+'</td><td><font size="3" color="black">'+str(row[4])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[5])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[6])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[7])+'</td></tr>'
        output += "</table><br/><br/><br/><br/>"    
        context= {'data':output}
        return render(request, 'UserScreen.html', context)      

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        qualification = request.POST.get('qualification', False)
        experience = request.POST.get('experience', False)
        gender = request.POST.get('gender', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+qualification+"','"+experience+"','"+gender+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Login to perform software collaborative development activities"
        context= {'data':output}
        return render(request, 'Register.html', context)    

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'software',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'UserLogin.html', context)

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})
