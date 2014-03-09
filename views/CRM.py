from misApp.models import tbl_customer, tbl_complaint, tbl_subscription,\
    tbl_employee, tbl_complaintResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from misApp.models import ProjectScope
#from django.db.models import Q
from django.core.mail import send_mail
from MIS.settings import EMAIL_HOST_USER
from django.http import HttpResponseRedirect
#from django.http import HttpResponse
from misApp.views import workfortoDoList, v_allTaskList
from misApp.pp import i_hasPermission, i_getEmployee


def v_CRM(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        rows=tbl_complaint.objects.all().order_by('-createdOn')
        try:
            rows=[[tbl_customer.objects.get(subscriptions=s.subId),tbl_subscription.objects.get(id=s.subId),s]for s in rows]
        except:
            pass
        return render_to_response("crm.html",locals(),context_instance=RequestContext(req))
        
def v_addCRM(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('srchSubscription','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','a'):
        
        subid=req.POST.get('subid','').strip()
        iD=subid[len(ProjectScope().getSubPrefix()):]
        subName=req.POST.get('subName','').strip()
        
        emailid=req.POST.get('emailid','').strip()
        mobno=req.POST.get('mobno','').strip()
        if not mobno and not subName and not emailid and  not subid:
            return HttpResponseRedirect('/CRM/') 
        
        customers=tbl_customer.objects.filter(email__contains=emailid,mobileNo__contains=mobno,firstName__contains=subName)
        anysub=[]
        if iD:
            try:
                customers=customers.filter(subscriptions=iD)
            except:
                pass
            for item in customers:
                try:
                
                    subscription=item.subscriptions.get(id=iD)
                
                    anysub.append(item.firstName)
                
                    anysub.append(item.getcusID())
                
                    anysub.append(item.mobileNo)
                
                    anysub.append(subscription.date)
                    anysub.append(subscription.getsubID())
                    anysub.append(subscription.id)
                
                except:
                    x=1
                    anysub=[]
                    customers=[]
                    return render_to_response('addCRM.html',locals(),context_instance=RequestContext(req))
                    
        x=1
        return render_to_response('addCRM.html',locals(),context_instance=RequestContext(req))
    return render_to_response('addCRM.html',locals(),context_instance=RequestContext(req)) 
def v_addComplaint(req,id):
    iD=id
    subID=ProjectScope().getSubPrefix()+iD
    getusername=req.session['username']
    uniemp=tbl_employee.objects.get(username=getusername)
    defdate=ProjectScope().getDate()
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('save','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','a'):
        errors=[]
        empID=req.POST.get('empID','').strip()
        subId=req.POST.get('subID','').strip()
        startdate=req.POST.get('startdate','').strip()
        description=req.POST.get('description','').strip()
        getstatus=req.POST.get('status','')
        
        x=0
        try:
            uniquecust=tbl_customer.objects.get(subscriptions=int(subId[len(ProjectScope().getSubPrefix()):]))
        except:
            pass
            
        if(empID[0:len(ProjectScope().empCodePrefix())]==ProjectScope().empCodePrefix()):
            
            #return render_to_response("addCRM.html",locals(),context_instance=RequestContext(req))
            try:
                x=int(empID[len(ProjectScope().empCodePrefix()):])
                employee=tbl_employee.objects.get(id=x)
            except:    
                errors.append("Please enter valid empid!")
        else:
            errors.append("Please enter valid empid!")
                    
        
        
        '''try:
            sDate=dateformatConvertor(startdate)
        except:
            errors.append("Please enter valid date!")'''
        if not description:
            errors.append("Please enter the description!")                
        if errors : 
            return render_to_response("ComplaintAdd.html",locals(),context_instance=RequestContext(req))
        
        newrow=tbl_complaint(subId=int(subId[len(ProjectScope().getSubPrefix()):]),date=defdate,description=description,status=getstatus,empId=x)
        newrow.save()
        return HttpResponseRedirect("/CRM/")
    if(req.POST.get('savemail','')):
        errors=[]
        empID=req.POST.get('empID','').strip()
        subId=req.POST.get('subID','').strip()
        startdate=req.POST.get('startdate','').strip()
        description=req.POST.get('description','').strip()
        getstatus=req.POST.get('status','')
        
        x=0
        try:
            uniquecust=tbl_customer.objects.get(subscriptions=int(subId[len(ProjectScope().getSubPrefix()):]))
        except:
            pass
            
        if(empID[0:len(ProjectScope().empCodePrefix())]==ProjectScope().empCodePrefix()):
            
            #return render_to_response("addCRM.html",locals(),context_instance=RequestContext(req))
            try:
                x=int(empID[len(ProjectScope().empCodePrefix()):])
                employee=tbl_employee.objects.get(id=x)
            except:    
                errors.append("Please enter valid empid!")
        else:
            errors.append("Please enter valid empid!")
                    
        
        
        '''try:
            sDate=dateformatConvertor(startdate)
        except:
            errors.append("Please enter valid date!")'''
        if not description:
            errors.append("Please enter the description!")                
        if errors : 
            return render_to_response("ComplaintAdd.html",locals(),context_instance=RequestContext(req))
        
        
        response=req.POST.get('description','').strip()
            
        msg="\nHi "+uniquecust.firstName+",\n\n"+description+"\n\nThanks,\nTransasia Team"
        
        send_mail('Transasia',msg,EMAIL_HOST_USER,[uniquecust.email])
        newrow=tbl_complaint(subId=int(subId[len(ProjectScope().getSubPrefix()):]),date=defdate,description=description,status=getstatus,empId=x)
        newrow.save()        
        
        
        return HttpResponseRedirect("/CRM/")
    return render_to_response('ComplaintAdd.html',locals(),context_instance=RequestContext(req))       
    
def v_editCRM(req,iD):
    iD=int(iD)
    getusername=req.session['username']
                                            
    uniqueemp=tbl_employee.objects.get(username=getusername)        
    uniquerow=tbl_complaint.objects.get(id=iD)
    customer=tbl_customer.objects.get(subscriptions=uniquerow.subId)
    subscription=customer.subscriptions.get(id=uniquerow.subId)
    responses=tbl_complaintResponse.objects.filter(compId=iD)
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('save','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','u'):
        error=[]
        empid=req.POST.get('empId','').strip()
        '''empid=req.POST.get('empid','').strip()
        response=req.POST.get('response','').strip()
        getstatus=req.POST.get('status','')
        errors=[]
        if(empid[0:len(ProjectScope().empCodePrefix())]!=ProjectScope().empCodePrefix()):
            errors.append("Please enter valid employee id!")
            return render_to_response("editCRM.html",locals(),context_instance=RequestContext(req))
        try:
            employee=tbl_employee.objects.get(id=int(empid[len(ProjectScope().empCodePrefix()):]))
        except:
            errors.append("Please enter valid employee id!")
        
            return render_to_response("editCRM.html",locals(),context_instance=RequestContext(req))        
        
        uniquerow.description=uniquerow.description+"\n"+response
        uniquerow.save()
        if(req.POST.get('savemail','')):
            response=req.POST.get('response','').strip()
            if not response:
                errors.append("Please enter the response!")
                return render_to_response("editCRM.html",locals(),context_instance=RequestContext(req))
            msg="\nHi "+customer.firstName+",\n\n"+response+"\n\nThanks,\nTransasia Team"
        
            send_mail('Transasia',msg,EMAIL_HOST_USER,[customer.email])
        return HttpResponseRedirect('/CRM/')'''
        response=req.POST.get('response','').strip()
        if not response:
            error.append('Please enter some response!')
        if error:
            return render_to_response('editCRM.html',locals(),context_instance=RequestContext(req))
        p1=tbl_complaintResponse(description=response,subId=subscription.id,empId=int(empid[len(ProjectScope().empCodePrefix()):]),compId=iD)
        p1.save()
        getstatus=req.POST.get('status','')
        uniquerow.status=getstatus
        uniquerow.save()
        
        
        
        
        return HttpResponseRedirect("/CRM/")
    if(req.POST.get('savemail','')):
        
        error=[]
        empid=req.POST.get('empId','').strip()
        response=req.POST.get('response','').strip()
        if not response:
            error.append("Please enter the response!")
            return render_to_response("editCRM.html",locals(),context_instance=RequestContext(req))
        
        
        
        p1=tbl_complaintResponse(description=response,subId=subscription.id,empId=int(empid[len(ProjectScope().empCodePrefix()):]),compId=iD)
        p1.save()
        getstatus=req.POST.get('status','')
        uniquerow.status=getstatus
        uniquerow.save()
        
        msg="\nHi "+customer.firstName+",\n\n"+response+"\n\nThanks,\nTransasia Team"
        
        send_mail('Transasia',msg,EMAIL_HOST_USER,[customer.email])
        return HttpResponseRedirect("/CRM/")
    return render_to_response('editCRM.html',locals(),context_instance=RequestContext(req))
