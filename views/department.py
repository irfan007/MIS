from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from misApp.models import tbl_departments, tbl_log
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from misApp.views import v_allTaskList, workfortoDoList
def v_departments(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'department','v'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        rows=tbl_departments.objects.filter(name__icontains=getparam)
        return render_to_response('departments.html',locals(),context_instance=RequestContext(req))
    rows=tbl_departments.objects.all().order_by('-createdOn')
    
    return render_to_response('departments.html',locals(),context_instance=RequestContext(req))
def v_addDepartment(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'department','a'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('addDepartment',''):
        errors=[]
        status=int(req.POST.get('status',''))
        description=req.POST.get('description','').strip()
        name=req.POST.get('name','').strip()
        if not name:
            errors.append('Please enter the name!')
        existedName=tbl_departments.objects.filter(name=name)
        if existedName:
            errors.append("This name already exists!")
        if errors:
            return render_to_response('addDepartment.html',locals(),context_instance=RequestContext(req))
        else:
             
            p1=tbl_departments(name=name,description=description,isActive=status)
            p1.save()
            p2=tbl_log(tbl_name='department',rowid=p1.id,newdata='name='+p1.name+'\n'+'description='+p1.description+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
            p2.save()
            return HttpResponseRedirect('/departments/')    
    else:
        return render_to_response('addDepartment.html',locals(),context_instance=RequestContext(req))
    
    
    
def v_editDepartment(req,deptid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'department','u'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    depid=int(deptid)
    fun=tbl_departments.objects.get(id=depid)
    p2=tbl_log()
    p2.olddata='name='+fun.name+'\n'+'description='+fun.description+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='department'
    p2.rowid=depid
    p2.action="Edit"
    p2.username=req.session['username']
    
    if req.POST.get('editDepartment',''):
        errors=[]
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
       
        remark=req.POST.get('remark','').strip()   
        status=req.POST.get('status','')
        if not name:
            errors.append("Please enter the name!")
        existedName=tbl_departments.objects.filter(name=name).exclude(id=depid)
        if existedName:
            errors.append("Please enter the different name!")
        if not remark:
            errors.append("Please enter the remark!")
        if errors:    
            return render_to_response('editDepartment.html',{'errors':errors,'name':name,'description':description,'depid':depid,\
                                                             'status':status,'alltask':alltask\
                                                             },context_instance=RequestContext(req))
        
        item=tbl_departments.objects.get(id=depid)
        item.name=name
        item.description=description
            
        if status=='1':
            item.isActive=True
        else:
            item.isActive=False
            
        item.save()
        p2.remarks=remark
        p2.newdata='name='+name+'\n'+'description='+description+'\n'+'status='+str(item.isActive)
        p2.save()
        return HttpResponseRedirect('/departments/')
    else:
        row=tbl_departments.objects.get(id=depid)
        return render_to_response('editDepartment.html',locals(),context_instance=RequestContext(req))
    
