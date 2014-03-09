from misApp.pp import i_getActiveAdminUser, upload
from django.http import HttpResponseRedirect
from misApp.models import tbl_location, tbl_employee
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from misApp.views import workfortoDoList, v_allTaskList

def v_change_employee_detail(req):
    
    unique_user_name=req.session.get('username','')
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('Save',''):
        errors=[]
        username=req.POST.get('username','')
        email=req.POST.get('email','').strip()
        
        
        
        fname=req.POST.get('fname','').strip()
        lname=req.POST.get('lname','').strip()
        address=req.POST.get('address','').strip()
        contact=req.POST.get('contactno','').strip()
        if contact:
            try:
                contact=int(contact)
            except:
                errors.append("Please enter valid contact no!")
                
        pincode=req.POST.get('pincode','').strip()
        if pincode:
            try:
                pincode=int(pincode)
            except:
                errors.append("Please enter valid pincode!")
        
        getstate=int(req.POST.get('state',''))
        getcity=int(req.POST.get('city',''))
    
            
        getcities=tbl_location.objects.filter(pid=getstate)
        getstates=tbl_location.objects.filter(pid=1)
        getcountries=tbl_location.objects.filter(pid=0)
        if '@' not in email:
            errors.append("Please enter valid emailid!")
        
        edata=tbl_employee.objects.filter(email=email).exclude(username=username)
        if edata:
            errors.append("this email ID is already registered!")
        if errors:
            return render_to_response('my_account.html',locals(),context_instance=RequestContext(req))
        
            
        ob=tbl_employee.objects.get(username=username)
        
        ob.email=email
        ob.firstName=fname
        ob.lastName=lname
        try:
            ob.city=tbl_location.objects.get(id=getcity)
        except:
            pass
        try:    
            ob.state=tbl_location.objects.get(id=getstate)
        except:
            pass
           
            
        ob.pin=pincode
        ob.mobileNo=contact
        ob.address=address
        if req.FILES.get('image'):
            imagePath=upload(req.FILES['image'],username+'.jpeg')
            ob.image=imagePath
        ob.save()           
        return HttpResponseRedirect('/')
    else:
        
        employeedata=tbl_employee.objects.get(username=unique_user_name)
            
        username=employeedata.username
        
        
        email=employeedata.email
        fname=employeedata.firstName
        lname=employeedata.lastName
        
        address=employeedata.address
        try:
            getcountry=int(employeedata.country.id)
        except:
            getcountry=-1
            
        getstates=tbl_location.objects.filter(pid=1)
            
        try:    
            getstate=int(employeedata.state.id)
        except:
            getstate=-1
        getcities=tbl_location.objects.filter(pid=getstate)
        try:
                    
            getcity=int(employeedata.city.id)
        except:
            getcity=-1    
            
            
            
        
            
        getcountries=tbl_location.objects.filter(pid=0)  
        contact=employeedata.mobileNo
        pincode=employeedata.pin
    
        return render_to_response('my_account.html',locals(),context_instance=RequestContext(req))  
  
  
