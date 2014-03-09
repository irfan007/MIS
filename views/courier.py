from django.template.context import RequestContext
from django.shortcuts import render_to_response
from misApp.models import tbl_supportedCourier, tbl_log
from django.http import HttpResponseRedirect
from misApp.pp import i_getActiveAdminUser, i_getEmployee, i_hasPermission
from misApp.views import workfortoDoList, v_allTaskList
def v_courier(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'courier','v'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        rows=tbl_supportedCourier.objects.filter(name__icontains=getparam)
        return render_to_response('courier.html',locals(),context_instance=RequestContext(req))
    
    rows=tbl_supportedCourier.objects.all().order_by('createdOn')
    return render_to_response('courier.html',locals(),context_instance=RequestContext(req))
def v_addCourier(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'courier','a'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('addCourier',''):
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
        status=req.POST.get('status','')
        code=req.POST.get('code','').strip()
        
        errors=[]
        if not name:
            errors.append('Please enter the name!')
        if not(len(str(code))>1):
            errors.append('Please enter the code!')
        existedcode=tbl_supportedCourier.objects.filter(code=code)
        if existedcode:
            errors.append("Please enter different code!")
        existedname=tbl_supportedCourier.objects.filter(name=name)
        if existedname:
            errors.append("Please enter different name!")    
        if errors:
            return render_to_response('addCourier.html',locals(),context_instance=RequestContext(req))
                                  
        else:
           
            if(status=="1"):
                isActive=True
            else:
                isActive=False    
            
            p1=tbl_supportedCourier(code=code,name=name,description=description,isActive=isActive)
            
            p1.save()
            p2=tbl_log(tbl_name='courier',rowid=p1.id,newdata='code='+p1.code+'\n'+'name='+p1.name+'\n'+'description='+p1.description+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username']) 
            p2.save()
            return HttpResponseRedirect('/couriers/')    
    else:
        

        return render_to_response('addCourier.html',locals(),context_instance=RequestContext(req))
def v_editCourier(req,courierid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'courier','u'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    courierid=int(courierid)
    fun=tbl_supportedCourier.objects.get(id=courierid)
    p2=tbl_log()
    p2.olddata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='courier'
    p2.rowid=courierid
    p2.action="Edit"
    p2.username=req.session['username']
    if req.POST.get('editCourier',''):
        errors=[]
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
        code=req.POST.get('code','').strip()
        status=req.POST.get('status','')
        remark=req.POST.get('remark','')
        if not name:
            errors.append("Please enter the name!")
        if not code:
            errors.append("Please enter the code!")    
        existedcode=tbl_supportedCourier.objects.filter(code=code).exclude(id=courierid)
        if existedcode:
            errors.append("Please enter the different code!")
        existedname=tbl_supportedCourier.objects.filter(name=name).exclude(id=courierid)
        if existedname:
            errors.append("Please enter the different name!")
        if not remark:
            errors.append("Please enter the remark!")
        if errors:    
            return render_to_response('editCourier.html',locals(),context_instance=RequestContext(req))
        
                 
             
        item=tbl_supportedCourier.objects.get(id=courierid)
        item.code=code
        item.name=name
        item.description=description
        
            
        if status=='1':
            item.isActive=True
        else:
            item.isActive=False
            
            
        item.save()
        p2.remarks=remark
        p2.newdata='code='+code+'\n'+'name='+name+'\n'+'description='+description+'\n'+'status='+str(item.isActive)
        p2.save()
        return HttpResponseRedirect('/couriers/')
    else:
        item=tbl_supportedCourier.objects.get(id=courierid)
        return render_to_response('editCourier.html',locals(),context_instance=RequestContext(req))                
        
    
            
                

