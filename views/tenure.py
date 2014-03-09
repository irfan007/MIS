from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from misApp.models import tbl_tenure, tbl_log, tbl_employee, tbl_taskList
from misApp.views import  workfortoDoList
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def v_tenures(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'tenure','v'):
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        tenures=tbl_tenure.objects.filter(name__icontains=getparam)
        return render_to_response('tenures.html',locals(),context_instance=RequestContext(req))
    tenures=tbl_tenure.objects.all().order_by("-createdOn")
   
   
    return render_to_response('tenures.html',locals(),context_instance=RequestContext(req))                   
 
def v_addTenure(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'tenure','a'):
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    errors=[]
    if req.POST.get('addtenure',''):
       
        name=req.POST.get('name','').strip()
        timePeriod=req.POST.get('period','').strip()
        status=req.POST.get('status','')
       
       
        if not timePeriod:
            errors.append("Please enter time period!")
        else:
            try:
                timePeriod=int(timePeriod)
            except:
                errors.append("Please enter valid time period!")   
        if not name:
            errors.append('Please enter the name!')
        dupname=tbl_tenure.objects.filter(name=name)
        if dupname:
            errors.append("Please enter the different name!")
        try:   
            duplicate_rows=tbl_tenure.objects.filter(timePeriod=timePeriod)
            if duplicate_rows:
                errors.append("Please enter the different time period!")
        except:
            pass           
        if errors:
            return render_to_response('addTenure.html',{'errors':errors,'timePeriod':timePeriod,'name':name,\
                                                        'status':status,'alltask':alltask},context_instance=RequestContext(req))
       
       
           
       
        if(status=="1"):
                isActive=True
        else:
                isActive=False
        try:
            timePeriod=int(timePeriod)
        except:
            timePeriod=0           
        row=tbl_tenure(name=name,timePeriod=timePeriod,isActive=isActive)
        row.save()
        p2=tbl_log(tbl_name='tenure',rowid=row.id,newdata='name='+row.name+'\n'+'Time='+str(row.timePeriod)+'\n'+'status='+str(row.isActive),action="Add",username=req.session['username'])
        p2.save()
        return HttpResponseRedirect('/tenures/')
    else:
        return render_to_response('addTenure.html',locals(),context_instance=RequestContext(req))

def v_editTenure(req,tid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'tenure','u'):
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    tenureid=int(tid)
   
    row=tbl_tenure.objects.get(id=tenureid)
   
    p2=tbl_log()
    p2.olddata='name='+row.name+'time='+str(row.timePeriod)+'\n'+'status='+str(row.isActive)
    p2.tbl_name='tenure'
    p2.rowid=tenureid
    p2.action="Edit"
    p2.username=req.session['username']   
    if req.POST.get('edittenure',''):
        errors=[]                           
        getname=req.POST.get('name','').strip()
        getperiod=req.POST.get('period','').strip()
        getremark=req.POST.get('remark','').strip()
       
        getstatus=req.POST.get('status','')
       
        if not getname:
            errors.append("Please enter the name!")
        try:
            getperiod=int(getperiod)
        except:   
            errors.append('Please enter valid time period!')
        dupname=tbl_tenure.objects.filter(name=getname).exclude(id=tenureid)
        if dupname:
            errors.append("Please enter the different name!")
        if not errors:
           
            duplicaterow=tbl_tenure.objects.filter(timePeriod=getperiod).exclude(id=tenureid)
           
            if duplicaterow:
                errors.append("Please enter the different time period!")
        if not getremark:
            errors.append("Please enter the remark!")   
        if errors:
            return render_to_response('editTenure.html',{'errors':errors,'name':getname,'timeperiod':getperiod,\
                                                         'status':getstatus,'tenureid':tenureid,'alltask':alltask},context_instance=RequestContext(req))
        
        if(getstatus=="1"):
            row.isActive=True
        else:
            row.isActive=False
       
               
       
        row.name=getname
        row.timePeriod=getperiod
       
       
        row.save() 
       
        p2.remarks=getremark
        p2.newdata='name='+getname+'\n'+'time='+str(getperiod)+'\n'+'status='+str(row.isActive)
        p2.save()
         
        return HttpResponseRedirect('/tenures/')
    else:
        return render_to_response('editTenure.html',{'row':row,'tenureid':tenureid,'alltask':alltask},context_instance=RequestContext(req))