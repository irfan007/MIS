from misApp.models import tbl_gift, tbl_log, tbl_giftHistory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from misApp.views import workfortoDoList, v_allTaskList


def v_giftstock(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'stock','v'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        gifts=tbl_gift.objects.all()
        return render_to_response('giftStock.html',locals(),context_instance=RequestContext(req))
def v_giftEditStock(req,id):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'stock','u'):
        return None
    iD=int(id)
    fun=tbl_gift.objects.get(id=iD)
    p2=tbl_log()
    p2.olddata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+\
    '\n'+'InitialQuantity='+str(fun.stockQuantity)+'\n'+'UpdatedQuantity='+str(fun.updated)+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='giftStock'
    p2.rowid=iD
    p2.action="Edit"
    p2.username=req.session['username']
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('addquantity',''):
        errors=[]
        name=req.POST.get('name','')
        updated=req.POST.get('updated','')
        addstock=req.POST.get('addstock','')
        remark=req.POST.get('remark','')
        if not remark:
            errors.append("Please enter remark!")    
        if not addstock:
            errors.append("Please enter Add Stock!")
        if addstock:
            try:
                addstock=int(addstock)
            except:
                errors.append("Please enter valid data in Add Stock!")        
        if errors:
            return render_to_response('editGiftstock.html',locals(),context_instance=RequestContext(req))    
        hobj=tbl_giftHistory()
        hobj.giftid=fun.id
        hobj.reason=remark
        hobj.quantity=addstock
        hobj.save()    
        ob=tbl_gift.objects.get(id=iD)
        ob.updated=ob.updated+addstock
        ob.save()
        p2.remarks=remark
        p2.newdata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+\
        '\n'+'InitialQuantity='+str(fun.stockQuantity)+'\n'+'UpdatedQuantity='+str(ob.updated)+'\n'+\
        'AddedQuantity='+str(addstock)+'\n'+'status='+str(fun.isActive)
        p2.save() 
        return HttpResponseRedirect('/giftstock/')
    if req.POST.get('subquantity','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'stock','u'):
        perrors=[]
        name=req.POST.get('name','')
        updated=req.POST.get('updated','')
        deduce=req.POST.get('deduce','')
        reason=req.POST.get('reason','')
            
        if not deduce:
            perrors.append("Please enter Deduce Quantity!")
        if deduce:
            try:
                deduce=int(deduce)
            except:
                perrors.append("Please enter valid data in Deduce Quantity!")
        if not reason:
            perrors.append("Please enter the reason!")
        if perrors:
            return render_to_response('editGiftstock.html',locals(),context_instance=RequestContext(req))
        ob=tbl_gift.objects.get(id=iD)
        if ob.updated-deduce<0:
            perrors.append("Deduction cannot be performed!")
            return render_to_response('editGiftstock.html',locals(),context_instance=RequestContext(req))
        hobj=tbl_giftHistory()
        hobj.giftid=fun.id
        hobj.reason=reason
        hobj.quantity=deduce
        hobj.save()
        
        ob.updated=ob.updated-deduce
        ob.save()
        p2.remarks=reason
        p2.newdata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+\
        '\n'+'InitialQuantity='+str(fun.stockQuantity)+'\n'+'UpdatedQuantity='+str(ob.updated)+'\n'+\
        'DeducedQuantity='+str(deduce)+'\n'+'status='+str(fun.isActive)
        p2.save() 
        return HttpResponseRedirect('/giftstock/')
    stkgift=tbl_gift.objects.get(id=iD)
        
    return render_to_response('editGiftstock.html',locals(),context_instance=RequestContext(req))
def v_gifthistory(req,iD):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'stock','v'):
        iD=int(iD)
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        allrows=tbl_giftHistory.objects.filter(giftid=iD)
        return render_to_response('gifthistory.html',locals(),context_instance=RequestContext(req))

def v_gifts(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'gift','v'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('submit_query',''):
            getparam=req.POST.get('passing_parameter','')
            gifts=tbl_gift.objects.filter(name__icontains=getparam)
            return render_to_response('gifts.html',locals(),context_instance=RequestContext(req))
    
        gifts=tbl_gift.objects.all().order_by('-createdOn')
        return render_to_response('gifts.html',locals(),context_instance=RequestContext(req))                    
  
def v_addGift(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'gift','a'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('addGift',''):
            name=req.POST.get('name','').strip()
            description=req.POST.get('description','').strip()
            status=req.POST.get('status','')
            quantity=req.POST.get('quantity','').strip()
            
            code=req.POST.get('code','').strip()
            errors=[]
            if not name:
                errors.append('Please enter the name!')
            if not code:
                errors.append('Please enter the code!')
            existedname=tbl_gift.objects.filter(name=name)
            if existedname:
                errors.append("Please enter different name!")
            existedcode=tbl_gift.objects.filter(code=code)
            if existedcode:
                errors.append("Please enter different code!")
            
            try:
                quantity=int(quantity)
            except:
                errors.append("Please enter valid quantity!")
            
                        
            if errors:
                return render_to_response('addGift.html',locals(),context_instance=RequestContext(req))
                    
            else:
                if not quantity:
                    quantity=0
                if(status=="1"):
                    isActive=True
                else:
                    isActive=False
                p1=tbl_gift(code=code,name=name,description=description,isActive=isActive,stockQuantity=quantity,updated=quantity)
                p1.save()
                p2=tbl_log(tbl_name='gift',rowid=p1.id,newdata='code='+p1.code+'\n'+'name='+p1.name+'\n'+'description='+p1.description+\
                           '\n'+'InitialQuantity='+str(p1.stockQuantity)+'\n'+'UpdatedQuantity='+str(p1.updated)+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
                p2.save()
                return HttpResponseRedirect('/gifts/')
        else:
            return render_to_response('addGift.html',locals(),context_instance=RequestContext(req))



def v_editGift(req,giftid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'gift','u'):
        return None
    giftid=int(giftid)
    fun=tbl_gift.objects.get(id=giftid)
    p2=tbl_log()
    p2.olddata='code='+fun.code+'\n'+'name='+fun.name+'\n'+'description='+fun.description+\
    '\n'+'InitialQuantity='+str(fun.stockQuantity)+'\n'+'UpdatedQuantity='+str(fun.updated)+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='gift'
    p2.rowid=giftid
    p2.action="Edit"
    p2.username=req.session['username']
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('editGift',''):
    
        
        errors=[]
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
        code=req.POST.get('code','').strip()
        remark=req.POST.get('remark','').strip()
        status=req.POST.get('status','')
        quantity=req.POST.get('quantity','').strip()
        if not name:
            errors.append("Please enter the name!")
        if not code:
            errors.append("Please enter the code!")
        if not remark:
            errors.append("Please enter the remark!")    
        existedcode=tbl_gift.objects.filter(code=code).exclude(id=giftid)
        if existedcode:
            errors.append("Please enter the different code!")
        existedname=tbl_gift.objects.filter(name=name).exclude(id=giftid)
        if existedname:
            errors.append("Please enter the different name!")    
        if errors:    
            return render_to_response('editGift.html',locals(),context_instance=RequestContext(req))
             
        item=tbl_gift.objects.get(id=giftid)
        item.code=code
        item.name=name
        item.description=description
        
            
        if status=='1':
            item.isActive=True
        else:
            item.isActive=False
            
            
        item.save()
        p2.remarks=remark
        p2.newdata='code='+code+'\n'+'name='+name+'\n'+'description='+description+'\n'+'InitialQuantity='+str(item.stockQuantity)+'\n'+'UpdatedQuantity='+str(item.updated)+'\n'+'status='+str(item.isActive)
        p2.save()
        return HttpResponseRedirect('/gifts/')
    else:
        item=tbl_gift.objects.get(id=giftid)
        return render_to_response('editGift.html',locals(),context_instance=RequestContext(req))                
        

