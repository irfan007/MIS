from django.template.context import RequestContext
from django.shortcuts import render_to_response
from misApp.models import tbl_location, tbl_branch, tbl_log
from django.http import HttpResponseRedirect
from misApp.views import workfortoDoList, v_allTaskList
from misApp.pp import i_getEmployee, i_hasPermission
def v_branch(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'branch','v'):
        return None
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        rows=tbl_branch.objects.filter(name__icontains=getparam)
        return render_to_response('branch.html',locals(),context_instance=RequestContext(req))
    rows=tbl_branch.objects.all()
    return render_to_response("branch.html",locals(),context_instance=RequestContext(req))
def v_addBranch(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'branch','a'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    getstates=tbl_location.objects.filter(pid=1)
    
    if req.POST.get('addBranch',''):
        errors=[]
        code=req.POST.get('code','').strip()
        name=req.POST.get('name','').strip()
        contactno=req.POST.get('contactno','').strip()
        description=req.POST.get('description','').strip()
        getstate=int(req.POST.get('state',''))
        getcities=tbl_location.objects.filter(pid=getstate)
        getcity=int(req.POST.get('city',''))
        address=req.POST.get('address','').strip()
        pincode=req.POST.get('pincode','').strip()
        status=req.POST.get('status','')
        if contactno:
            try:
                contactno=int(contactno)
            except:
                errors.append("Please enter valid contact no!")
        if pincode:
            try:
                pincode=int(pincode)
            except:
                errors.append("Please enter the valid pincode!")
        status=req.POST.get('status','')
        if not code:
            errors.append("Please enter the code!")
            
        if not name:
            errors.append("Please enter the name!")
        if getstate==-1:
            errors.append("Please select the state!")
        if getcity==-1:
            errors.append("Please select the city!")
        if not address:
            errors.append("Please enter the address!")
            
        
        dupcode=tbl_branch.objects.filter(code=code)
        if dupcode:
            errors.append("Please enter the different code,this code already exist!")
        dupname=tbl_branch.objects.filter(name=name)
        if dupname:
            errors.append("Please enter the different name,this name already exist!")
        if errors:
            return render_to_response('addBranch.html',locals(),context_instance=RequestContext(req))
        if status=="1":
            isActive=True
        else:
            isActive=False    
            
        branchstate=tbl_location.objects.get(id=getstate)
        branchcity=tbl_location.objects.get(id=getcity)
        p1=tbl_branch(name=name,code=code,description=description,state=branchstate.name,city=branchcity.name,\
                isActive=isActive,address=address,pincode=pincode,contactno=contactno)
        p1.save()
        p2=tbl_log(tbl_name='branch',rowid=p1.id,newdata='code='+p1.code+'\n'+'name='+p1.name+'\n'+'description='+p1.description+'\n'+\
                   'contact='+str(p1.contactno)+'\n'+'state='+p1.state+'\n'+'city='+p1.city+'\n'\
                   +'address='+p1.address+'\n'+'pincode='+str(p1.pincode)+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
        p2.save()
        return HttpResponseRedirect("/branch/")
    
    return render_to_response("addBranch.html",locals(),context_instance=RequestContext(req))
def v_editBranch(req,branchID):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'branch','u'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    iD=int(branchID)
    getstates=tbl_location.objects.filter(pid=1)
    fun=tbl_branch.objects.get(id=iD)
    p2=tbl_log()
    p2.olddata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+'\n'+\
                'contact='+str(fun.contactno)+'\n'+'state='+fun.state+'\n'+'city='+fun.city+'\n'\
                +'address='+fun.address+'\n'+'pincode='+str(fun.pincode)+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='branch'
    p2.rowid=iD
    p2.action="Edit"
    p2.username=req.session['username']
    if req.POST.get('editBranch',''):
        errors=[]
        contactno=req.POST.get('contactno','').strip()
        code=req.POST.get('code','').strip()
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
        branchstate=int(req.POST.get('state',''))
        getcities=tbl_location.objects.filter(pid=branchstate)
        branchcity=int(req.POST.get('city',''))
        if contactno:
            try:
                contactno=int(contactno)
            except:
                errors.append("Please enter valid contactno!")    
        if branchcity==-1:
            errors.append("Please select the city!")
        
                
        address=req.POST.get('address','').strip()
        pincode=req.POST.get('pincode','').strip()
        remark=req.POST.get('remark','').strip()
        if pincode:
            try:
                pincode=int(pincode)
            except:
                errors.append("Please enter the valid pincode!")
        status=req.POST.get('status','')
        if not code:
            errors.append("Please enter the code!")
        dupcode=tbl_branch.objects.filter(code=code).exclude(id=iD)
        if dupcode:
            errors.append("Same code already exist,please enter different code!")
                
        if not name:
            errors.append("Please enter the name!")
        dupname=tbl_branch.objects.filter(name=name).exclude(id=iD)
        if dupname:
            errors.append("Same name already exist,please enter different name!")
        if not address:
            errors.append("Please enter the address!")
        if not remark:
            errors.append("Please enter the remark!")
        if errors:
            return render_to_response("editBranch.html",locals(),context_instance=RequestContext(req))
        if status=="1":
            isActive=True
        else:
            isActive=False     
        uniquerow=tbl_branch.objects.get(id=iD)
        uniquerow.contactno=contactno
        uniquerow.code=code
        uniquerow.name=name
        uniquerow.description=description
        uniquerow.address=address
        uniquerow.isActive=isActive
        uniquerow.pincode=pincode
        uniquerow.state=tbl_location.objects.get(id=branchstate).name
        uniquerow.city=tbl_location.objects.get(id=branchcity).name
        uniquerow.save()
        p2.remarks=remark
        p2.newdata='code='+uniquerow.code+'\n'+'name='+uniquerow.name+'\n'+'description='+uniquerow.description+'\n'+\
                'contact='+str(uniquerow.contactno)+'\n'+'state='+uniquerow.state+'\n'+'city='+uniquerow.city+'\n'\
                +'address='+uniquerow.address+'\n'+'pincode='+str(uniquerow.pincode)+'\n'+'status='+str(uniquerow.isActive)
        p2.save()
        return HttpResponseRedirect('/branch/')
    row=tbl_branch.objects.get(id=iD)
    getstates=tbl_location.objects.filter(pid=1)
    stateobj=tbl_location.objects.filter(name=row.state)
    getcities=tbl_location.objects.filter(pid=stateobj[0].id)
    return render_to_response('editBranch.html',locals(),context_instance=RequestContext(req))