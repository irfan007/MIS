# source section
from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from misApp.models import tbl_source
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from misApp.views import workfortoDoList, v_allTaskList


def v_sources(req):
    
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'source','v'):
        return None
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        try:
            parentsource=tbl_source.objects.get(categoryName=getparam,pid=0)
            sources=tbl_source.objects.filter(pid=parentsource.id)
        except:
            sources=tbl_source.objects.filter(categoryName__contains=getparam,pid__gt=0)    
        return render_to_response('sources.html',locals(),context_instance=RequestContext(req))
    sources=tbl_source.objects.filter(pid__gt=0).order_by('-createdOn')
    return render_to_response('sources.html',locals(),context_instance=RequestContext(req))                    
  
def v_addSource(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'source','a'):
        return None
    categories=tbl_source.objects.filter(pid__lt=1)
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('addnewcategory',''):
        errors=[]
        newcategory=req.POST.get('addcategory','').strip()
        if not newcategory:
            errors.append("Please enter the value!")
            return render_to_response('addSource.html',{'errors':errors, 'newcategoryname':newcategory,\
                                                        'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
        existedNameObj=tbl_source.objects.filter(categoryName=newcategory)
            
        if existedNameObj:
            errors.append("Please enter the different category name!")
            
            return render_to_response('addSource.html',{'errors':errors, 'newcategoryname':newcategory,\
                                                        'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
        p1=tbl_source(categoryName=newcategory,pid=0,isActive=True)
        p1.save()
        return render_to_response('addSource.html',{'categories':categories,'alltask':alltask},context_instance=RequestContext(req))    
    if req.POST.get('addSource',''):
        errors=[]
        
            
        status=req.POST.get('status','')
        name=req.POST.get('name','').strip()
        category=req.POST.get('category','')
        category=int(category)
        if(category==-1):
            errors.append('Please choose the category!')
        if len(str(name))<1:
            errors.append('Please enter the name!')
       
        if errors:
            return render_to_response('addSource.html',{'errors':errors,'category':category,'name':name,\
                                                        'status':status,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
        
        existedNameObj=tbl_source.objects.filter(categoryName=name)
        
        if existedNameObj:
            errors.append("Please enter different name or information!")
          
        
        
            return render_to_response('addSource.html',{'name':name,'category':category,'errors':errors,\
                                                        'status':status,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
        if(status=="1"):
            isActive=True
        else:
            isActive=False    
            
        p1=tbl_source(categoryName=name,pid=category,isActive=isActive)
            
        p1.save()
        return HttpResponseRedirect('/sources/')    
    else:
        
        return render_to_response('addSource.html',{'categories':categories,'alltask':alltask},context_instance=RequestContext(req))



def v_editSource(req,sourceid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'source','u'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    categories=tbl_source.objects.filter(pid__lt=1)
    srcid=int(sourceid)
    errors=[]
    uniquerow=tbl_source.objects.get(id=srcid)
    if req.POST.get('editSource',''):
        
        category=req.POST.get('category','').strip()
        name=req.POST.get('name','').strip()
        status=req.POST.get('status','')
        
            
        if not name:
            errors.append('Please enter source name!')
        if not category:
            errors.append('Please enter category name!')
        existedNameObj=tbl_source.objects.filter(categoryName=name).exclude(id=srcid)
        
        if existedNameObj:
            errors.append("Please enter different name/information!")
        existedNameCategory=tbl_source.objects.filter(categoryName=category).exclude(id=uniquerow.pid)
        if existedNameCategory:
            errors.append("Please enter different Category Name!")
        if errors:
            return render_to_response('editSource.html',{'errors':errors,'category':category,'name':name,\
                                                         'srcid':srcid,'status':status,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
        
        prow=tbl_source.objects.get(id=uniquerow.pid)
        prow.categoryName=category
        prow.save()
        item=tbl_source.objects.get(id=srcid)
        
        item.categoryName=name
        if status=="1":
           
            item.isActive=True
        else:
            item.isActive=False    
        item.save()
        return HttpResponseRedirect('/sources/')
    else:
        item=tbl_source.objects.get(id=srcid)
        
        return render_to_response('editSource.html',locals(),context_instance=RequestContext(req))                



