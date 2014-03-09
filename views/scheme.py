from misApp.pp import i_getActiveAdminUser, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from misApp.models import tbl_scheme, tbl_magazine, tbl_tenure, tbl_gift,\
    tbl_magazineCombo, tbl_log
from django.utils.dateformat import DateFormat
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from misApp.views import dateformatConvertor, dateformatReverse, workfortoDoList,\
    v_allTaskList
def v_schemes(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'scheme','v'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('submit_query',''):
        getparam=req.POST.get('passing_parameter','')
        rows=tbl_scheme.objects.filter(name__icontains=getparam)
        return render_to_response('schemes.html',locals(),context_instance=RequestContext(req))
    
    
    
    rows=tbl_scheme.objects.filter()
    
    for row in rows:
        if(row.endDate!=None):
            if(row.endDate<datetime.date.today()):
                row.isActive=False
                row.save()
    rows=tbl_scheme.objects.filter().order_by('-createdOn')    
    return render_to_response('schemes.html',locals(),context_instance=RequestContext(req))
def v_addScheme(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'scheme','a'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    magazines=tbl_magazine.objects.filter(isActive=True)
    tenures=tbl_tenure.objects.filter(isActive=True)
    gifts=tbl_gift.objects.filter(isActive=True)
    magazinecombos=tbl_magazineCombo.objects.filter(isActive=True)
    
    if req.POST.get('addScheme',''):
        
        
        errors=[]
        name=req.POST.get('name','').strip()
        cost=req.POST.get('cost','').strip()
        startdate=req.POST.get('startdate','')
        enddate=req.POST.get('enddate','')
        description=req.POST.get('description','')
        magazine=req.POST.get('magazine','')
        magazinecombo=req.POST.get('magazinecombo','')
        tenure=req.POST.get('tenure','')
        
        gift=req.POST.get('gift','')
        try:
            gift=int(gift)
        except:
            gift=0
        try:
            magazine=int(magazine)
        except:
            magazine=-1
        try:
            magazinecombo=int(magazinecombo)        
        except:
            magazinecombo=-1
        try:
            tenure=int(tenure)
        except:
            tenure=-1
        status=req.POST.get('status','')
        if not req.POST.get('name',''):
            errors.append("Please enter the name!")
            return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        existedname=tbl_scheme.objects.filter(name=name)
        if existedname:
            errors.append("Please enter the different name!")
            return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        try:
            cost=int(cost)
        except:
            errors.append("Please enter valid cost!")
            return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))    
        
        if len(str(startdate))>4:
            if len(str(enddate))>4:
                if datetime.datetime.strptime(startdate,'%d-%m-%Y')>datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append("end date must be greater than startdate!")
                    return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        if len(str(enddate))>4:
            if not len(str(startdate))>4:
                errors.append("end date must be specified only when start date exist!")
                return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        
        if magazine==-1:
            if magazinecombo==-1:
                errors.append("Please select either the magazine or magazine combo!")
                return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))        
        
        if magazine>0:
            if magazinecombo>0:
                errors.append("You can select either only the magazine or magazine combo!")
                return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
            
        
                        
        
        if tenure==-1:
            errors.append("Please select tenure!")     
            return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        
                
        try:
            startdate=dateformatConvertor(startdate)
        except:
            startdate=None
        try:
            enddate=dateformatConvertor(enddate)
        except:
            enddate=None    
        if(req.POST.get('status','')):
            status=req.POST.get('status','')
            if status=='1':
                isActive=True
            else:
                isActive=False
        if gift>0:
                    
            giftobject=tbl_gift.objects.get(id=gift)
        else:
            giftobject=None
        if magazine>0:
            magazineobject=tbl_magazine.objects.get(id=magazine)
        else:
            magazineobject=None
        if magazinecombo>0:
            magazinecomboobject=tbl_magazineCombo.objects.get(id=magazinecombo)
        else:
            magazinecomboobject=None    
            
        row=tbl_scheme(name=name,cost=cost,startDate=startdate,endDate=enddate,magazine=magazineobject,tenure=tbl_tenure.objects.get(id=tenure),\
                       gifts=giftobject,description=description,isActive=isActive,magazineCombo=magazinecomboobject)    
        row.save()
        
        p2=tbl_log(tbl_name='scheme',rowid=row.id,newdata='name='+row.name+'\n'+'cost='+str(row.cost)+'\n'+'description='+row.description+'\n'+'startdate='+str(row.getstartDate())+\
                    '\n'+'enddate='+str(row.getenddate())+'\n'+'magazine='+row.getmagazinename()+'\n'+'combo='+row.getmagazineComboname()+'\n'+'tenure='+row.tenure.name+'\n'+'gift='+\
                    row.getgiftname()+'\n'+'status='+str(row.isActive),action="Add",username=req.session['username'])
            
        p2.save()
        return HttpResponseRedirect('/schemes/')
    else:
        return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))



def v_editScheme(req,schemeid):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'scheme','u'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    tenures=tbl_tenure.objects.filter(isActive=True)
    offers=tbl_gift.objects.filter(isActive=True)
    magazines=tbl_magazine.objects.filter()
    magazinecombos=tbl_magazineCombo.objects.filter()
    id=int(schemeid)
    fun=tbl_scheme.objects.get(id=id)
    p2=tbl_log()
    p2.olddata='name='+fun.name+'\n'+'cost='+str(fun.cost)+'\n'+'description='+fun.description+'\n'\
                +'startdate='+str(fun.getstartDate())+'\n'+'enddate='+str(fun.getenddate())+'\n'+\
                'magazine='+fun.getmagazinename()+'\n'+'combo='+fun.getmagazineComboname()+'\n'+'tenure='+fun.tenure.name+\
                '\n'+'gift='+fun.getgiftname()+'\n'+'status='+str(fun.isActive)
    p2.tbl_name='scheme'
    p2.rowid=id
    p2.action="Edit"
    p2.username=req.session['username']
    if req.POST.get('editScheme',''):
        
        errors=[]
        name=req.POST.get('name','').strip()
        description=req.POST.get('description','').strip()
        startdate=req.POST.get('startdate1','')
        enddate=req.POST.get('enddate1','')
        cost=req.POST.get('cost','').strip()
        gift=int(req.POST.get('gift',''))
        tenure=int(req.POST.get('tenure',''))
        magazine=int(req.POST.get('magazine',''))
        magazinecombo=int(req.POST.get('magazinecombo',''))
        status=req.POST.get('status','')
        remark=req.POST.get('remark','')
        if(len(str(name))<1):
            errors.append("Please enter the name!")
            return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))
        existedname=tbl_scheme.objects.filter(name=name).exclude(id=id)
        if existedname:
            errors.append("Please enter the different name!")
            return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))
        if len(str(startdate))>4:
            if len(str(enddate))>4:
                if datetime.datetime.strptime(startdate,'%d-%m-%Y')>datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append("end date must be greater than start date!")
                    return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))
        if len(str(enddate))>4:
            if not len(str(startdate))>4:
                errors.append("end date must be specified only when start date exist!")
                return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))            
        
        if magazine==-1:
            if magazinecombo==-1:
                errors.append("Please select either magazine or magazine combo!")
                return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))
        
        if magazine>0:
            if magazinecombo>0:
                errors.append("You can select either only the magazine or magazine combo!")
                return render_to_response('addScheme.html',locals(),context_instance=RequestContext(req))
        
        
        try:
            cost=int(cost)
        except:
            errors.append("Please enter valid cost!")
            return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))    
        
        if tenure==-1:
            errors.append("Please select the tenure!")
            return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req)) 
        if not remark:
            errors.append("Please enter the remark!")
            return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))   
        
    
             
        item=tbl_scheme.objects.get(id=id)
        item.name=name
        item.description=description
            
        item.cost=cost
        try:
            item.magazine=tbl_magazine.objects.get(id=magazine)
        except:
            item.magazine=None
        try:
            item.magazineCombo=tbl_magazineCombo.objects.get(id=magazinecombo)
        except:
            item.magazineCombo=None    
                
        item.tenure=tbl_tenure.objects.get(id=tenure)
        if gift!=-1:
            item.gifts=tbl_gift.objects.get(id=gift)
        else:
            item.gifts=None    
        
        if(req.POST.get('status','')):
            status=req.POST.get('status','')
            if status=='1':
                item.isActive=True
            else:
                item.isActive=False
            
        try:
            startdate=dateformatConvertor(startdate)
        except:
            startdate=None
        try:        
            
            enddate=dateformatConvertor(enddate)
        except:
            enddate=None    
        item.startDate=startdate
        item.endDate=enddate
        item.save()
        p2.remarks=remark
        p2.newdata='name='+item.name+'\n'+'cost='+str(item.cost)+'\n'+'description='+item.description+'\n'\
                +'startdate='+str(item.getstartDate())+'\n'+'enddate='+str(item.getenddate())+'\n'+\
                'magazine='+item.getmagazinename()+'\n'+'combo='+item.getmagazineComboname()+'\n'+'tenure='+item.tenure.name+\
                '\n'+'gift='+item.getgiftname()+'\n'+'status='+str(item.isActive)
        p2.save()
        return HttpResponseRedirect('/schemes/')
    else:
        row=tbl_scheme.objects.get(id=id)
        try:
            sd=dateformatReverse(str(row.startDate))
        except:
            sd=None
        try:    
            ed=dateformatReverse(str(row.endDate))
        except:
            ed=None    
        return render_to_response('editScheme.html',locals(),context_instance=RequestContext(req))

