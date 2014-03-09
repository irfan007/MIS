from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from misApp.models import tbl_tenure, tbl_log, tbl_employee, tbl_taskList,\
    tbl_magazinePeriod
from misApp.views import  workfortoDoList
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse

def v_magazinePeriod(req):# this method is used for listing of magazine periods
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'magazinePeriod','v'):#authentication+validation
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        magazinePeriods=tbl_magazinePeriod.objects.filter(name__contains=getparam)
        return render_to_response('magazinePeriods.html',locals(),context_instance=RequestContext(req))
    magazinePeriods=tbl_magazinePeriod.objects.all().order_by("-createdOn")
    return render_to_response('magazinePeriods.html',locals(),context_instance=RequestContext(req))                   
 
def v_addMagazinePeriod(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'magazinePeriod','a'):
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    errors=[]
    if req.POST.get('addMagazinePeriod',''):
       
        name=req.POST.get('name','').strip()
        timePeriod=req.POST.get('timePeriod','').strip()
        if not name:
            errors.append("Please enter the name")
        else:
            duprows=tbl_magazinePeriod.objects.filter(name=name)
            if duprows:
                errors.append("Please enter the different name.This name already exist!")
        try:
            timePeriod=int(timePeriod)
        except:
            errors.append("Please enter the valid time period!")
            
                
                   
        if errors:
            return render_to_response('addMagazinePeriod.html',locals(),context_instance=RequestContext(req))
       
        duprows=tbl_magazinePeriod.objects.filter(daysPeriod=timePeriod)
        if duprows:
            errors.append("Please enter the different time Period.This is already exist in record!")
            return render_to_response('addMagazinePeriod.html',locals(),context_instance=RequestContext(req))
        row=tbl_magazinePeriod(name=name,daysPeriod=timePeriod)
        row.save()
        p2=tbl_log(tbl_name='MagazinePeriod',rowid=row.id,newdata='name='+row.name+'\n'+'Time Period='+str(row.daysPeriod),action="Add",username=req.session['username'])
        p2.save()
        return HttpResponseRedirect('/magazinePeriods/')
    else:
        return render_to_response('addMagazinePeriod.html',locals(),context_instance=RequestContext(req))

def v_editMagazinePeriod(req,tid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'magazinePeriod','u'):
        return None
    workfortoDoList(req)
    empobj=tbl_employee.objects.get(username=req.session['username'])
    alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
    para=int(tid)
   
    row=tbl_magazinePeriod.objects.get(id=para)
   
    p2=tbl_log()
    p2.olddata='name='+row.name+'\n'+'Time Period='+str(row.daysPeriod)
    p2.tbl_name='MagazinePeriod'
    p2.rowid=para
    p2.action="Edit"
    p2.username=req.session['username']   
    if req.POST.get('editMagazinePeriod',''):
        errors=[]                           
        getname=req.POST.get('name','').strip()
        getperiod=req.POST.get('period','').strip()
        getremark=req.POST.get('remark','').strip()
       
        
       
        if not getname:
            errors.append("Please enter the name!")
        try:
            getperiod=int(getperiod)
        except:   
            errors.append('Please enter valid time period!')
        dupname=tbl_magazinePeriod.objects.filter(name=getname).exclude(id=para)
        if dupname:
            errors.append("Please enter the different name!")
        if not errors:
           
            duplicaterow=tbl_magazinePeriod.objects.filter(daysPeriod=getperiod).exclude(id=para)
           
            if duplicaterow:
                errors.append("Please enter the different time period!")
        if not getremark:
            errors.append("Please enter the remark!")   
        if errors:
            return render_to_response('editMagazinePeriod.html',{'errors':errors,'name':getname,'timeperiod':getperiod,\
                                                                 'para':para,'alltask':alltask},context_instance=RequestContext(req))
           
           
       
       
       
        
       
               
       
        row.name=getname
        row.daysPeriod=getperiod
       
       
        row.save() 
       
        p2.remarks=getremark
        p2.newdata='name='+getname+'\n'+'time='+str(getperiod)
        p2.save()
         
        return HttpResponseRedirect('/magazinePeriods/')
    else:
        return render_to_response('editMagazinePeriod.html',{'row':row,'para':para,'alltask':alltask},context_instance=RequestContext(req))
def v_magPeriod(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine','a'):
        return None
    if req.POST.get('addPopMagPeriod',''):
        errors=[]
        name=req.POST.get('name','').strip()
        timePeriod=req.POST.get('timePeriod','').strip()
        if not name:
            errors.append("Please enter the name")
        else:
            duprows=tbl_magazinePeriod.objects.filter(name=name)
            if duprows:
                errors.append("Please enter the different name.This name already exist!")
        try:
            timePeriod=int(timePeriod)
        except:
            errors.append("Please enter the valid time period!")
            
                
                   
        if errors:
            return render_to_response('popMagazinePeriod.html',locals(),context_instance=RequestContext(req))
       
        duprows=tbl_magazinePeriod.objects.filter(daysPeriod=timePeriod)
        if duprows:
            errors.append("Please enter the different time Period.This is already exist in record!")
            return render_to_response('popMagazinePeriod.html',locals(),context_instance=RequestContext(req))
        row=tbl_magazinePeriod(name=name,daysPeriod=timePeriod)
        row.save()
        p2=tbl_log(tbl_name='MagazinePeriod',rowid=row.id,newdata='name='+row.name+'\n'+'Time Period='+str(row.daysPeriod),action="Add",username=req.session['username'])
        p2.save()
        temp="\n\
        <script>\n\
        try{\n\
            window.opener.setPopMagazinePeriod("
        temp=temp+str(row.id)+")\n\
            window.close();\n\
            }catch(error){alert(error);}\n\
        </script>"
        return HttpResponse("<p>"+temp+"</p>")

            
            
        return render_to_response('popMagazinePeriod.html',locals(),context_instance=RequestContext(req))
    return render_to_response("popMagazinePeriod.html",locals(),context_instance=RequestContext(req))


def v_getMagPeriod(req):
    if req.GET.get('popMagazinePeriod',''):
        selectPeriod=int(req.GET.get('popMagazinePeriod',''))
        
        allMagPeriod=tbl_magazinePeriod.objects.filter()
        template='<select name="magPeriod"><option value="-1">Select</option>'
        for item in allMagPeriod:
            if item.id==selectPeriod:
                
                template=template+"<option value='"+str(item.id)+"' selected>"+item.name+"</option>"
            else:
                template=template+"<option value='"+str(item.id)+"'>"+item.name+"</option>"
        template=template+"</select>"
        return HttpResponse(template)