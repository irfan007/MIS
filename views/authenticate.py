#from django.http import HttpResponse
from misApp.pp import i_validateEmployee, i_getEmployeeByEmail,\
    hasLogedInEmployee
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from MIS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from misApp.views import workfortoDoList
from misApp.models import tbl_employee


def i_findURl(emp):
    autoRedirect={
                  'admin':'/subscription/list/',
                  'stock':'/giftstock/',
                  'location':'/locations/',
                  'department':'/departments/',
                  'role':'/role/list/',
                  'employee':'/user/list',
                  'magazine':'/magazine/list/',
                  'magazine combo':'/combo/list/',
                  'scheme':'/schemes/',
                  'gift':'/gifts/',
                  'source':'/sources/',
                  'tenure':'/tenures/',
                  'subscription':'/subscription/list',
                  'compliment':'',
                  'com':'',
                  'report':'/report/gift/',
                  'print':'/Mlabel/',
                  'notification':'/notification/',
                  'crm':'/CRM/',
                  'courier':'/couriers/',
                  'branch':'/branch/',
                  'stock':'/giftstock/'
                  
    }
    try:
        if emp.isAdmin:
            return autoRedirect['admin'] 
        return autoRedirect[emp.role.permissions.filter(view=True)[0].content.name]
    except:
        return "/myaccount/"
    
def v_home(req):
    
    if hasLogedInEmployee(req):
        workfortoDoList(req)
        try:
            empobj=tbl_employee.objects.get(username=req.session['username'])
            #alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
        except:
            pass
        return HttpResponseRedirect(i_findURl(empobj))
    return HttpResponseRedirect("/login")

def v_loginUser(req):
    if  hasLogedInEmployee(req):
        return HttpResponseRedirect("/")
        
    if req.method=='POST':
        errors=[]
        employee=None
        username=req.POST.get('username','').strip()
        password=req.POST.get('password','').strip()
        if len(username)==0:
            errors.append("Please enter username !")
        elif len(password)==0:
            errors.append("Please enter password !")
        employee=i_validateEmployee(username,password)
        if not employee:
            errors.append("Invalid Username Or Password !")
        if not errors:
            req.session['username']=employee.username
            return HttpResponseRedirect(i_findURl(employee))
        return render_to_response("login.html",locals())
    return render_to_response("login.html")

def v_logoutUser(req):
    if req.session.get('username',''):
        del req.session['username']
    return HttpResponseRedirect('/')

def v_forgotPassword(req):
    if  hasLogedInEmployee(req):
        return HttpResponseRedirect("/")
    if req.method=='POST':
        errors=[]
        employee=None
        email=req.POST.get('email','').strip()
        if len(email)==0:
            errors.append("Please enter a email address !")
        elif '@' not in email:
            errors.append("Please enter a valid email address !")
        else:
            employee=i_getEmployeeByEmail(email)
            if not employee:
                errors.append("We have no user with this email Id !")
        if not errors:
            msg="\nHi "+employee.firstName+",\n\nYour Forgotten Password is inside '()' :("+employee.password+")\n\nThanks,\nTransasia Team"
            send_mail('Transasia',msg,EMAIL_HOST_USER,[email])
            return render_to_response('forgotPassword.html',{'done':True})
        return render_to_response('forgotPassword.html',locals())
        
    return render_to_response('forgotPassword.html')