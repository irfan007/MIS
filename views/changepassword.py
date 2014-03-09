from misApp.pp import i_getActiveAdminUser
from django.http import HttpResponseRedirect
from misApp.models import tbl_employee
from django.shortcuts import render_to_response
from django.template.context import RequestContext
def v_reset_password(req):
    if not i_getActiveAdminUser(req.session.get('username','')):
        return HttpResponseRedirect('/')
    if(req.method=="POST"):
        errors=[]
        unique_user_name=req.session.get('username','')    
        try:
            empdata=tbl_employee.objects.get(username=unique_user_name)
        except:
            return HttpResponseRedirect('/')
        
        opassword=req.POST.get('opassword','').strip()
        npassword=req.POST.get('npassword','').strip()
        cpassword=req.POST.get('cpassword','').strip()
        if(empdata.password!=opassword):
            errors.append('Old password must be valid!')
        if len(str(npassword))<5:
            errors.append('Length of password must be between 5 and 15 characters !')
        if len(str(npassword))>15:
            errors.append('Length of password must be between 5 and 15 characters !')
        if cpassword!=npassword:
            errors.append('New password and confirm password must be same !')
        if errors:
            return render_to_response('change_password.html',locals(),context_instance=RequestContext(req))
        empdata.password=npassword
        empdata.save()
        return HttpResponseRedirect('/')                     
    return render_to_response('change_password.html',locals(),context_instance=RequestContext(req)) 
