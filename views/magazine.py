from misApp.pp import i_getActiveAdminUser, i_getAllMagazines, i_getMagazine,\
    i_getMagazineByCode, i_getAllCombos, i_getActiveMagazines, i_getCombo,\
    i_getComboByCode, i_getComboById, i_hasPermission, i_getEmployee
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from misApp.models import tbl_magazine, tbl_magazineCombo, tbl_log,\
    tbl_magazinePeriod
from django.utils.dateformat import DateFormat
from misApp.views import workfortoDoList, v_allTaskList
from django.http import HttpResponse




def createlogforcombo(req,p1):
    p2=tbl_log()
    p2.tbl_name="MagazineCombo"
    p2.action="Add"
    p2.rowid=p1.id
    names=""
    for item in p1.magazines.all():
        names=names+'+'+item.name
    p2.newdata='name='+p1.name+'\n'+'code='+p1.code+'\n'+'description='+p1.description+'\n'+'price='+str(p1.price)+'\n'+'magazines='+names[1:]+'\n'+'status='+str(p1.isActive)
    p2.username=req.session['username']
    p2.save()
    

    
def work_for_magazine_log(req,p1):
    p2=tbl_log(tbl_name='magazine',rowid=p1.id,newdata='name='+p1.name+'\n'+'code='+p1.code+'\n'+'price='+str(p1.price)+'\n'+\
               'startdate='+str(p1.startDate)[:10]+'\n'+'enddate='+str(p1.endDate)[:10]+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
    p2.save()
    return

def v_magazine(req,url):
    
    options=url.split('/')
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if options[0]=='list' and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine','v'):
        if req.POST.get('submit_query',''):
            getparam=req.POST.get('passing_parameter','')
            magazines=tbl_magazine.objects.filter(name__icontains=getparam)
            return render_to_response('magazineList.html',locals(),context_instance=RequestContext(req))
        magazines=i_getAllMagazines()
        
        return render_to_response('magazineList.html',locals(),context_instance=RequestContext(req))
    
    elif options[0]=='add' and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine','a'):
        allMagPeriod=tbl_magazinePeriod.objects.filter()
        if req.POST.get('addMagazine',''):
            errors=[]
            
            name=req.POST.get('name','').strip()
            code=req.POST.get('code','').strip()
            price=req.POST.get('price','').strip()
            startdate=req.POST.get('startdate','').strip()
            enddate=req.POST.get('enddate','').strip()
            magPeriod=int(req.POST.get('magPeriod',''))
            active=req.POST.get('active','')
            
            if active=='1':
                active=True
            
                                       
            if name:
                if i_getMagazine(name):
                    errors.append("this magazine name is already exist !")
            else:
                errors.append("please enter a name !")
            
                            
            if code:
                if i_getMagazineByCode(code):
                    errors.append("this magazine code is already exist !")
            else:
                errors.append("please enter a code name !")
            
                
            if price:
                try:
                    int(price)
                except ValueError:
                    errors.append("Invalid value found for field price !")
            else:    
                errors.append("please enter a price !")
            
            try:
                getMagObject=tbl_magazinePeriod.objects.get(id=magPeriod)
            except:
                
                errors.append("Please select the magazine period")
            
                
            #----------------------
            
                
            if len(startdate)>0:
                try:
                    datetime.datetime.strptime(startdate,'%d-%m-%Y')
                    
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
                    flag=False
            
                            
            if len(enddate)>0:
                try:
                    datetime.datetime.strptime(enddate,'%d-%m-%Y')
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
                    flag=False
            
            
            if enddate and not startdate:
                errors.append('Please enter startDate first !')
            
            flag=True    
            if startdate and enddate and flag:
                datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                if datetime.datetime.strptime(startdate,'%d-%m-%Y')==datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('StartDate and endDate can not be same !')
                elif datetime.datetime.strptime(startdate,'%d-%m-%Y')>datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('EndDate must be greater than startDate !')
            
                             
            
            
            if not errors:
                if len(startdate)==0:
                    startdate=None
                    
                if len(enddate)==0:
                    enddate=None
                    
                if not startdate and enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=None,
                                            endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                                            isActive=active,
                                            magPeriodType=getMagObject
                                            )
                    work_for_magazine_log(req,magazinelog)
                elif startdate and not enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y'),
                                            endDate=None,
                                            isActive=active,
                                            magPeriodType=getMagObject
                                            )
                    work_for_magazine_log(req,magazinelog)
                elif startdate and enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y'),
                                            endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                                            isActive=active,
                                            magPeriodType=getMagObject
                                            )
                    work_for_magazine_log(req,magazinelog)
                else:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=None,
                                            endDate=None,
                                            isActive=active,
                                            magPeriodType=getMagObject
                                            )
                    work_for_magazine_log(req,magazinelog)
                return HttpResponseRedirect('/magazine/list')
            return render_to_response('addMagazine.html',locals(),context_instance=RequestContext(req))
            
        return render_to_response('addMagazine.html',locals(),context_instance=RequestContext(req))
    
    elif options[0]=='edit' and options[1] and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine','u'):
        
        mag=tbl_magazine.objects.get(id=int(options[1]))
        p2=tbl_log()
        p2.tbl_name='magazine'
        p2.rowid=mag.id
        p2.olddata='name='+mag.name+'\n'+'code='+mag.code+'\n'+'price='+str(mag.price)+'\n'+\
               'startdate='+str(mag.startDate)[:10]+'\n'+'enddate='+str(mag.endDate)[:10]+'\n'+'status='+str(mag.isActive)
        p2.action="Edit"
        p2.username=req.session['username']
        name=mag.name
        code=mag.code
        price=mag.price
        if mag.magPeriodType:
            
            magPeriodid=mag.magPeriodType.id
        if mag.startDate:
            startdate=DateFormat(mag.startDate).format('d-m-Y')
        if mag.endDate:
            enddate=DateFormat(mag.endDate).format('d-m-Y')
        active=mag.isActive
        allMagPeriod=tbl_magazinePeriod.objects.filter()
        #return HttpResponse(allMagPeriod)
        if req.POST.get('editMagazine',''):
            
            errors=[]
            
            name=req.POST.get('name','').strip()
            code=req.POST.get('code','').strip()
            price=req.POST.get('price','').strip()
            startdate=req.POST.get('startdate','').strip()
            enddate=req.POST.get('enddate','').strip()
            active=req.POST.get('active','')
            magPeriodid=int(req.POST.get('magPeriodid',''))
            remark=req.POST.get('remark','').strip()
            try:
                magPeriodobj=tbl_magazinePeriod.objects.get(id=magPeriodid)
            except:
                errors.append("Please select valid Magazine Period")
            if active=='1':
                active=True
            
                                       
            if name:
                if i_getMagazine(name) and i_getMagazine(name).name!=mag.name:
                    errors.append("this magazine name is already exist !")
            else:
                errors.append("please enter a name !")
            
                            
            if code:
                if i_getMagazineByCode(code) and i_getMagazineByCode(code).code!=mag.code:
                    errors.append("this magazine code is already exist !")
            else:
                errors.append("please enter a code name !")
            
                
            if price:
                try:
                    int(price)
                except ValueError:
                    errors.append("Invalid value found for field price !")
            else:    
                errors.append("please enter a price !")
            
                
            
                
            #----------------------
                
            if len(startdate)>0:
                try:
                    datetime.datetime.strptime(startdate,'%d-%m-%Y')
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
            
                            
            if len(enddate)>0:
                try:
                    datetime.datetime.strptime(enddate,'%d-%m-%Y')
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
            if not remark:
                errors.append('Please enter the remark!')
            if enddate and not startdate:
                errors.append('Please enter startDate first !')
            
            flag=True
            if startdate and enddate and flag:
                datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                if datetime.datetime.strptime(startdate,'%d-%m-%Y')==datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('StartDate and endDate can not be same !')
                elif datetime.datetime.strptime(startdate,'%d-%m-%Y')>datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('EndDate must be greater than startDate !')
            
            
            if not errors:
                if len(startdate)==0:
                    startdate=None
                    
                if len(enddate)==0:
                    enddate=None
                
                if not startdate and enddate:
                    mag.name=name
                    mag.code=code
                    mag.price=price
                    mag.magPeriodType=magPeriodobj
                    mag.startDate=None
                    mag.endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y')
                    mag.isActive=active
                    
                    mag.save()
                    p2.remarks=remark
                    p2.newdata='name='+mag.name+'\n'+'code='+mag.code+'\n'+'price='+str(mag.price)+'\n'+\
                    'startdate='+str(mag.startDate)[:10]+'\n'+'enddate='+str(mag.endDate)[:10]+'\n'+'status='+str(mag.isActive)
                    p2.save()
                    
                elif startdate and not enddate:
                    mag.name=name
                    mag.code=code
                    mag.magPeriodType=magPeriodobj
                    mag.price=price
                    mag.startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y')
                    mag.endDate=None
                    mag.isActive=active
                    mag.save()
                    p2.remarks=remark
                    
                    p2.newdata='name='+mag.name+'\n'+'code='+mag.code+'\n'+'price='+str(mag.price)+'\n'+\
                    'startdate='+str(mag.startDate)[:10]+'\n'+'enddate='+str(mag.endDate)[:10]+'\n'+'status='+str(mag.isActive)
                    p2.save()
                elif startdate and enddate:
                    mag.name=name
                    mag.code=code
                    mag.magPeriodType=magPeriodobj
                    mag.price=price
                    mag.startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y')
                    mag.endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y')
                    mag.isActive=active
                    mag.save()
                    p2.remarks=remark
                    
                    p2.newdata='name='+mag.name+'\n'+'code='+mag.code+'\n'+'price='+str(mag.price)+'\n'+\
                    'startdate='+str(mag.startDate)[:10]+'\n'+'enddate='+str(mag.endDate)[:10]+'\n'+'status='+str(mag.isActive)
                    p2.save()                    
                else:
                    mag.name=name
                    mag.magPeriodType=magPeriodobj
                    mag.code=code
                    mag.price=price
                    mag.startDate=None
                    mag.endDate=None
                    mag.isActive=active
                    mag.save()
                    
                    p2.remarks=remark
                    p2.newdata='name='+mag.name+'\n'+'code='+mag.code+'\n'+'price='+str(mag.price)+'\n'+\
                    'startdate='+str(mag.startDate)[:10]+'\n'+'enddate='+str(mag.endDate)[:10]+'\n'+'status='+str(mag.isActive)
                    p2.save()
                    
                combos_has_mag=tbl_magazineCombo.objects.filter(magazines=mag)
                for a_combo in combos_has_mag: 
                    if a_combo.magazines.filter(isActive=False):
                        a_combo.isActive=False
                        a_combo.save()
                    else:
                        a_combo.isActive=True
                        a_combo.save()
                
                return HttpResponseRedirect('/magazine/list')
            return render_to_response('editMagazine.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editMagazine.html',locals(),context_instance=RequestContext(req))
            
def v_combo(req,url):
    options=url.split('/')
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if options[0]=='list' and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine combo','v'):
        if req.POST.get('submit_query',''):
            getparam=req.POST.get('passing_parameter','')
            combos=tbl_magazineCombo.objects.filter(name__icontains=getparam)
            return render_to_response('comboList.html',locals(),context_instance=RequestContext(req))
        combos=i_getAllCombos()
        return render_to_response('comboList.html',locals(),context_instance=RequestContext(req))
    elif options[0]=='add' and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine combo','a'):
        magazines=i_getActiveMagazines()
        MagStatus=[]
        [MagStatus.append((m.id,m.name,False)) for m in magazines]
        if req.POST.get('addCombo',''):
            errors=[]
            MagStatus=[]
            name=req.POST.get('name','').strip()
            code=req.POST.get('code','').strip()
            description=req.POST.get('description','').strip()
            #price=req.POST.get('price','').strip()
            price=None
            active=req.POST.get('active','')
            flag=0
            for m in magazines:
                v=req.POST.get(str(m.id),'')
                if v=='1':
                    MagStatus.append((m.id,m.name,True))
                    flag=flag+1
                else:
                    MagStatus.append((m.id,m.name,False))
            
            
            
            if active=='1':
                active=True
            
                                       
            if name:
                if i_getCombo(name):
                    errors.append("combo with this name is already exist !")
            else:
                errors.append("please enter a name !")
            
                            
            if code:
                if i_getComboByCode(code):
                    errors.append("combo with this code is already exist !")
            else:
                errors.append("please enter a code name !")
            
                
            #if price:
            #    try:
            #        int(price)
            #    except ValueError:
            #        errors.append("Invalid value found for field price !")
            #else:    
            #    errors.append("please enter a price !")
            
            if flag<2:
                errors.append("please select atleast two magazines !")
            
            
            if not errors:
                newCombo=tbl_magazineCombo.objects.create(name=name,code=code,description=description,price=price,isActive=active)
                for m in MagStatus:
                    if m[2]:
                        newCombo.magazines.add(tbl_magazine.objects.get(id=m[0]))
                createlogforcombo(req,newCombo)        
                return HttpResponseRedirect('/combo/list')
            return render_to_response('addCombo.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addCombo.html',locals(),context_instance=RequestContext(req))
    elif options[0]=='edit' and options[1] and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine combo','u'):
        combo=i_getComboById(int(options[1]))
        maglog=""
        for item in combo.magazines.all():
            maglog=maglog+'+'+item.name
            
        p2=tbl_log()
        p2.tbl_name='MagazineCombo'
        p2.rowid=combo.id
        p2.olddata='name='+combo.name+'\n'+'code='+combo.code+'\n'+'description='+str(combo.description)+'\n'+\
               'price='+str(combo.price)+'\n'+'magazines='+maglog[1:]+'\n'+'status='+str(combo.isActive)
        p2.action="Edit"
        p2.username=req.session['username']
        name=combo.name
        code=combo.code
        description=combo.description
        #price=combo.price
        active=combo.isActive
        MagStatus=[]
        selectedMags=combo.magazines
        for m in i_getActiveMagazines():
            try:
                exist=selectedMags.get(id=m.id)
                if exist:
                    MagStatus.append((m.id,m.name,exist.isActive))
            except tbl_magazine.DoesNotExist:
                MagStatus.append((m.id,m.name,False))
        del selectedMags
        if req.POST.get('editCombo',''):
            errors=[]
            MagStatus=[]
            name=req.POST.get('name','').strip()
            code=req.POST.get('code','').strip()
            description=req.POST.get('description','').strip()
            #price=req.POST.get('price','').strip()
            price=None
            active=req.POST.get('active','')
            remark=req.POST.get('remark','')
            flag=0
            for m in i_getActiveMagazines():
                v=req.POST.get(str(m.id),'')
                if v=='1':
                    MagStatus.append((m.id,m.name,True))
                    flag=flag+1
                else:
                    MagStatus.append((m.id,m.name,False))
            
            if active=='1':
                active=True
            
            if not remark:
                errors.append("Please enter the remark! ")                           
            if name:
                if i_getCombo(name) and i_getCombo(name).name!=combo.name:
                    errors.append("combo with this name is already exist !")
            else:
                errors.append("please enter a name !")
            
                            
            if code:
                if i_getComboByCode(code) and i_getComboByCode(code).code!=combo.code:
                    errors.append("combo with this code is already exist !")
            else:
                errors.append("please enter a code name !")
            
                
            #if price:
            #    try:
            #        int(price)
            #    except ValueError:
            #        errors.append("Invalid value found for field price !")
            #else:    
            #    errors.append("please enter a price !")
            
            if flag<2:
                errors.append("please select atleast two magazines !")
                
            if not errors:
                combo.name=name
                combo.code=code
                combo.description=description
                combo.price=price
                combo.isActive=active
                combo.save()
                [combo.magazines.remove(obj) for obj in combo.magazines.all()]
                for m in MagStatus:
                    if m[2]:
                        combo.magazines.add(tbl_magazine.objects.get(id=m[0]))
                maglog=""
                for item in combo.magazines.all():
                    maglog=maglog+'+'+item.name
                p2.remarks=remark
                p2.newdata='name='+combo.name+'\n'+'code='+combo.code+'\n'+'description='+str(combo.description)+'\n'+\
               'price='+str(combo.price)+'\n'+'magazines='+maglog[1:]+'\n'+'status='+str(combo.isActive)
                
                p2.save()
                return HttpResponseRedirect('/combo/list')
            return render_to_response('editCombo.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editCombo.html',locals(),context_instance=RequestContext(req))