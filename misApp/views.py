# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q


from misApp.pp import i_getAllStates, i_getActiveAdminUser, i_hasPermission,\
    i_getEmployee

from misApp.pp import i_getAllStates, i_getActiveAdminUser, i_getEmployee,\
    i_hasPermission

from misApp.models import tbl_employee, tbl_departments,  tbl_magazine,\
    ProjectScope, tbl_magazineCombo, tbl_location,\
    tbl_competitor, tbl_source, tbl_scheme, tbl_tenure, tbl_gift,\
    tbl_customer, tbl_supportedCourier,\
    tbl_subscription, tbl_complaint,\
    tbl_branch, tbl_role, tbl_taskList, tbl_log, tbl_compMagazine,\
    tbl_compMagOffer
import datetime
from xlwt import Workbook
from xlwt.Style import easyxf
from django.core.servers.basehttp import FileWrapper
from MIS.settings import MEDIA_ROOT
from django.db.models import Max

def v_deductgift(req,c):
    cid=int(c)
    uniquecust=tbl_customer.objects.get(id=cid)
    for item in uniquecust.gift.all():
        uniquegift=tbl_gift.objects.get(id=item.id)
        uniquegift.updated=uniquegift.updated-1
        uniquegift.save()
    return
def v_moreList(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    
    try:
        uncompletedTask=tbl_taskList.objects.filter(isActive=True,username=tbl_employee.objects.get(username=req.session['username']))
        completedTask=tbl_taskList.objects.filter(isActive=False,username=tbl_employee.objects.get(username=req.session['username']))
    except:
        pass    
    return render_to_response("MoreList.html",locals(),context_instance=RequestContext(req))
    

def v_allTaskList(req):
    try:
        empobj=tbl_employee.objects.get(username=req.session['username'])
        alltasklist=tbl_taskList.objects.filter(isActive=True,username=empobj)
        return alltasklist
    except:
        pass

def workfortoDoList(req):
    try:
        empobj=tbl_employee.objects.get(username=req.session['username'])
        alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
        if req.POST.get('Submitlist',''):
            for item in alltask:
                if req.POST.get('xxx'+str(item.id),''):
                    item.isActive=False
                    item.completedDate=ProjectScope().getDate()
                    item.save()
            description=req.POST.get('tododescription','').strip()
            
            if description:
                
                p1=tbl_taskList(description=description,username=tbl_employee.objects.get(username=req.session['username']))
                p1.save()  
    except:
        pass
    

def v_log(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    records=tbl_log.objects.all().order_by('-datetime')
    allEmp=tbl_employee.objects.filter()
    modulesList=['magazine','MagazinePeriod','tenure','department','branch','courier','MagazineCombo','gift','scheme']
    
    return render_to_response('logrecord.html',locals(),context_instance=RequestContext(req))
    '''username=req.session['username']
    return HttpResponse(username)'''
def v_fulllogview(req,id):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    iD=int(id)
    uniquerow=tbl_log.objects.get(id=iD)
    
    
    return render_to_response("viewfull_log.html",locals(),context_instance=RequestContext(req))
'''manav section'''
def v_search(req):
    
    
    if req.method=="POST":
        search_option=req.POST.get('select_option_to_be_search','')
        parameter=req.POST.get('passing_parameter','')
        if search_option=="Role":
            findrole=tbl_role.objects.filter(Q(name__contains=parameter))
            return render_to_response('findRole.html',locals(),context_instance=RequestContext(req))
        if search_option=="User":
            uniempid=parameter
            findemp=tbl_employee.objects.filter(Q(username__contains=parameter)|Q(email=parameter)\
                                                |Q(designation__contains=parameter)|Q(firstName=parameter)|Q(mobileNo=parameter))
            checkempcode=uniempid[len(ProjectScope().empCodePrefix()):]
            try:
                find_by_empcode=tbl_employee.objects.filter(id=int(checkempcode))
            except:
                pass    
            return render_to_response('findemployee.html',locals(),context_instance=RequestContext(req))
        if search_option=="Subscriber":
            unisubid=parameter
            checksubcode=unisubid[len(ProjectScope().getSubPrefix()):]
            try:
                find_by_checksubcode=tbl_customer.objects.get(subscriptions=int(checksubcode))
                unique_subscription=tbl_subscription.objects.get(id=int(checksubcode))
            except:
                pass
            checkcustcode=unisubid[len(ProjectScope().getCustomerPrefix()):]
            try:
                find_by_checkcustcode=tbl_customer.objects.get(id=int(checkcustcode))
            except:
                pass
            findcust=tbl_customer.objects.filter(Q(firstName=parameter)|Q(mobileNo=parameter)|Q(email=parameter))
            return render_to_response('findsubs.html',locals(),context_instance=RequestContext(req))
            #return HttpResponse("asjah")
        if search_option=="Department":
            rows=tbl_departments.objects.filter(name__contains=parameter)
            return render_to_response('departments.html',locals(),context_instance=RequestContext(req))
        if search_option=="Magazine":
            magazines=tbl_magazine.objects.filter(Q(name__contains=parameter)|Q(code__contains=parameter))
            return render_to_response('magazineList.html',locals(),context_instance=RequestContext(req))
        if search_option=="MagazineCombo":
            combos=tbl_magazineCombo.objects.filter(Q(name__contains=parameter)|Q(code__contains=parameter))
            return render_to_response('comboList.html',locals(),context_instance=RequestContext(req))
        if search_option=="Gift":
            gifts=tbl_gift.objects.filter(Q(name__contains=parameter)|Q(code__contains=parameter))
            return render_to_response('gifts.html',locals(),context_instance=RequestContext(req))
        if search_option=="Tenure":
            tenures=tbl_tenure.objects.filter(name__contains=parameter)
            return render_to_response('tenures.html',locals(),context_instance=RequestContext(req))
        if search_option=="Source":
            try:
                parentsource=tbl_source.objects.get(categoryName=parameter,pid=0)
                sources=tbl_source.objects.filter(pid=parentsource.id)
            except:
                sources=tbl_source.objects.filter(categoryName__contains=parameter,pid__gt=0)    
            return render_to_response('sources.html',locals(),context_instance=RequestContext(req))
        if search_option=="Courier":
            rows=tbl_supportedCourier.objects.filter(Q(code__contains=parameter)|Q(name__contains=parameter))
            return render_to_response('courier.html',locals(),context_instance=RequestContext(req))
        if search_option=="Scheme":
            rows=tbl_scheme.objects.filter(name__contains=parameter)
            return render_to_response("schemes.html",locals(),context_instance=RequestContext(req))
        if search_option=="Branch":
            rows=tbl_branch.objects.filter(name__contains=parameter,code__contains=parameter)
            return render_to_response('branch.html',locals(),context_instance=RequestContext(req))
        if search_option=="CRM":
            dup_para=parameter
            cmpid=int(dup_para[len(ProjectScope().getComplaintPrefix()):])
            try:
                row=tbl_complaint.objects.get(id=cmpid)
                subscrip=tbl_subscription.objects.get(id=row.subId)
                custom=tbl_customer.objects.get(subscriptions=subscrip)
            except:
                pass
            return render_to_response("findcrm.html",locals(),context_instance=RequestContext(req))
        
            
    return HttpResponse(search_option)    
        


                                  
def javascript_for_crm_and_competitors(req):
    
    
    
    if req.GET.get('subid',''):
        
        subid=req.GET.get('subid','').strip()
        
        try:
            if ProjectScope().getSubPrefix()==subid[0:len(ProjectScope().getSubPrefix())]:
                customer=tbl_customer.objects.get(subscriptions=int(subid[len(ProjectScope().getSubPrefix()):]))
                subscription=customer.subscriptions.get(id=int(subid[len(ProjectScope().getSubPrefix()):]))
                firstName=customer.firstName
                email=customer.email
                name=subscription.magazine.name
                template="<div class='section'>\
                <label>Name</label>\
                <div> <input type='text' name='name' value='"+firstName+"' class='large' readonly /></div>\
                </div>\
                <div class='section'>\
                <label>Email ID</label>\
                <div> <input type='text' name='email' value='"+email+"' class='large' readonly  /></div>\
                </div>\
                <div class='section' >\
                <label>Magazine</label>\
                <div>\
                <input type='text' name='magazine' value='"+name+"' class='large' readonly  />\
                </div>\
                </div>\
                "
                return HttpResponse(template)
            else:
                raise ValueError
        except:
            customer=None
            subscription=None
            return HttpResponse('<div class="section">\
            <label>Name</label>\
            <div> <input type="text" name="name" class="large" readonly /></div>\
            </div>\
            <div class="section" >\
            <label>Email ID</label>\
            <div> <input type="text" name="email" class="large" readonly  /></div>\
            </div>\
            <div class="section" >\
            <label>Magazine</label>\
            <div>\
            <input type="text" name="magazine" class="large" readonly  />\
            </div>\
            </div>\
            ')
        
    if req.GET.get('brand',''):
        brand=req.GET.get('brand','').strip()
        row=tbl_competitor.objects.filter(brandName=brand)
        cp=str(row[0].coverPrice)
        if row:
            template="\
            <div class='section' >\
            <label>Cover Price</label>\
            <div> <input type='text' name='coverprice' class='large' value='"+cp+"' readonly /></div>\
            </div>"
            return HttpResponse(template)
    return HttpResponse('data not found !')
    

def dateformatConvertor(date):
    date=datetime.datetime.strptime(date, '%d-%m-%Y')
    
    return date.strftime('%Y-%m-%d')
def dateformatReverse(date):
    date=datetime.datetime.strptime(date, '%Y-%m-%d')
    
    return date.strftime('%d-%m-%Y')



def i_getAllStates(iD):
    
    states=tbl_location.objects.filter(pid=iD)
    return states





#location section
def v_locations(req):
    if not i_hasPermission(i_getEmployee(req.session.get('username','')),'location','v'):
        return None
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    

    listing=[]
    rows=tbl_location.objects.filter(type='a')

    for item in rows:
        try:
            forcity=tbl_location.objects.get(id=item.pid)
        
            forstate=tbl_location.objects.get(id=forcity.pid)
        
            forcountry=tbl_location.objects.get(id=forstate.pid)
            d={'forcity':forcity.name,'forstate':forstate.name,'forcountry':forcountry.name,\
           'name':item.name,'pincode':item.pincode,'iD':item.id}
        
            listing.append(d)
            d={}
        except:
            pass
    return render_to_response('location.html',{'list':listing,'alltask':alltask},context_instance=RequestContext(req))


def v_addLocation(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'location','a'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        countries=tbl_location.objects.filter(pid=0)
        errors=[]
        
        if req.POST.get('addcountrybutton',''):
            country=str(req.POST.get('addcountryname','').strip())
            if(len(country)<1):
                errors.append('Please enter country name!')
                return render_to_response('addLocation.html',locals(),context_instance=RequestContext(req))
            row=tbl_location(name=country,pid=0)
            row.save()
            
            return HttpResponseRedirect('/location/add/')
        if req.POST.get('addstatebutton',''):
                
            country=req.POST.get('country','')
            
            state=str(req.POST.get('addstatename','').strip())
            country=int(country)
            states=tbl_location.objects.filter(pid=country)
            if(country<1):
                errors.append('Please enter country name!')
            if(len(state)<1):
                errors.append('Please enter country name!')        
            if errors:    
                return render_to_response('addLocation.html',locals(),context_instance=RequestContext(req))
            
            stateadd=tbl_location(name=state,pid=country,type="s")
            stateadd.save()
            return HttpResponseRedirect('/location/add/')
                
        if req.POST.get('addcitybutton',''):
                
                
            city=str(req.POST.get('addcityname','').strip())
            country=req.POST.get('country','')
            stateid=req.POST.get('getstate','')
            country=int(country)
            stateid=int(stateid)
            states=tbl_location.objects.filter(pid=country)
            if(country<0):    
                errors.append('Please select country!')
                
            if(stateid<0):
                
                errors.append('Please select state!')
            if(len(city)<1):
                errors.append('Please enter complete details!')    
            if errors:
                return render_to_response('addLocation.html',locals(),context_instance=RequestContext(req))        
            
            cityadd=tbl_location(name=city,pid=stateid,type="c")
            cityadd.save()
            return HttpResponseRedirect('/location/add/') 
            
        if req.POST.get('addLocation',''):
                   
            
            errors=[]
            country=int(req.POST.get('country',''))
            stateid=int(req.POST.get('getstate',''))
            cityid=int(req.POST.get('getcity',''))
            area=str(req.POST.get('getarea','').strip())
            pincode=str(req.POST.get('pincode','').strip())
            
            states=tbl_location.objects.filter(pid=country)
            cities=tbl_location.objects.filter(pid=stateid)
            if(country<1):
                errors.append('Please enter complete details!')
            if(stateid<1):
                errors.append('Please enter complete details!')
            if cityid<1:
                errors.append('Please enter complete details!')
        
            if(len(area)<1):
                errors.append("Please enter complete details!")        
            if(len(pincode)<1):
                errors.append("Please enter complete details!")
            if(errors):
                return render_to_response('addLocation.html',locals(),context_instance=RequestContext(req))    
           
            row=tbl_location(name=area,pincode=pincode,pid=cityid,type='a')
            row.save()            
            return HttpResponseRedirect('/locations/')
        
                
        return render_to_response('addLocation.html',locals(),context_instance=RequestContext(req))



def v_editLocation(req,locid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'location','u'):
        
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        errors=[]
        iD=int(locid)
        getarearow=tbl_location.objects.get(id=iD)
        getarea=getarearow.name
        getpincode=getarearow.pincode
        
        getcityrow=tbl_location.objects.get(id=getarearow.pid)
        getcity=getcityrow.name
        getstaterow=tbl_location.objects.get(id=getcityrow.pid)
        getstate=getstaterow.name
        getcountryname=tbl_location.objects.get(id=getstaterow.pid)
        getcountry=getcountryname.name
        if(req.POST.get('editLocation','')):
            pincode=str(req.POST.get('pincode','').strip())
            area=str(req.POST.get('area','').strip())
            city=str(req.POST.get('city','').strip())
            state=str(req.POST.get('state','').strip())
            country=str(req.POST.get('country','').strip())
            if(len(country)<1):
                errors.append("Please enter country name!")
            if(len(state)<1):
                errors.append("Please enter state name!")
            if(len(city)<1):
                errors.append("Please enter city name!")
            if(len(area)<1):
                errors.append("Please enter area name!")
            if(len(pincode)<1):
                errors.append("Please enter pincode!")    
            if errors:
                return render_to_response('editLocation.html',{'passpincode':pincode,'passcountry':country,\
                                                               'passstate':state,'passcity':city,'passarea':area,\
                                                               'iD':iD,'errors':errors},context_instance=RequestContext(req))
            
            
            getcountryname.name=country
            getcountryname.save()
                        
            getstaterow.name=state
            getstaterow.save()
            
            getcityrow.name=city
            getcityrow.save()
                    
            getarearow.name=area
            getarearow.save()
            
            getarearow.pincode=pincode
            getarearow.save()
            
            return HttpResponseRedirect('/locations/')
        else:    
            
            
            return render_to_response('editLocation.html',locals(),context_instance=RequestContext(req))
                              
                              
# tenure section(completed)

                  
    
def v_accMresponder(req):
    if req.GET.get('country',''):
        
        states=i_getAllStates(int(req.GET.get('country','')))
        template="\n\
        <div class='selectWidth1' id='statediv'>\
        <select class='small' name='state' onchange='getCity(this.value)'>\n\
        <option value='-1'> ---- </option>\n"
        if states:
            for s in states:
                template=template+"<option value='"+str(s.id)+"'>"+s.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        </div>"
        return HttpResponse(template)

    if req.GET.get('state',''):
        cities=i_getAllStates(int(req.GET.get('state','')))
        template="\n\
        <div class='selectWidth1' id='citydiv'>\
        <select class='small' name='city'>\n\
        <option value='-1'> ---- </option>\n"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        </div>"
        return HttpResponse(template)

def v_Mresponder(req):
    
    
    if req.GET.get('country',''):
        
 
        states=i_getAllStates(int(req.GET.get('country','')))
        template="\n\
        <div class='selectWidth1' id='statediv'>\
        <select class='small' name='getstate' onchange='getCity(this.value)'>\n\
        <option value='-1'> ---- </option>\n"
        if states:
            for s in states:
                template=template+"<option value='"+str(s.id)+"'>"+s.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        <input type='text' name='addstatename' value='' size='20' maxlength='100'  /><br>\
        <input type='submit' name='addstatebutton' value='add'></input>\
        </div>"
        return HttpResponse(template)

    if req.GET.get('state',''):
        cities=i_getAllStates(int(req.GET.get('state','')))
        template="\n\
        <div class='selectWidth1' id='citydiv'>\
        <select class='small' name='getcity'>\n\
        <option value='-1'> ---- </option>\n"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n<input type='text' name='addcityname' value='' size='20' maxlength='100'  />\
        <input type='submit' name='addcitybutton' value='add'></input>\
        </div>"
        return HttpResponse(template)
    if req.GET.get('company',''):
        
        compmag=tbl_compMagazine.objects.filter(companyName=int(req.GET.get('company','')))
        #return HttpResponse('compmag')
        template="\n\
        <div id='compmagazinediv'>\
        <select class='small' name='magazineid'>\n\
        <option value='-1'> ---- </option>\n"
        if compmag:
            for m in compmag:
                template=template+"<option value='"+str(m.id)+"'>"+m.magName+"</option>\n"
        else:
            template=template+"<option value='-1'> NOT FOUND !</option>\n"
        template=template+"</select>\n\
        </div>"
        return HttpResponse(template)

def v_logFilter(req,para1,para2):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    allEmp=tbl_employee.objects.filter()
    modulesList=['magazine','MagazinePeriod','tenure','department','branch','courier','MagazineCombo','gift','scheme']
    if para1=="All":
        if para2=="All":
            return HttpResponseRedirect('/log/')
        else:
            records=tbl_log.objects.filter(tbl_name=para2)
            return render_to_response('logrecord.html',locals(),context_instance=RequestContext(req))
    else:
        if para2=="All":
            records=tbl_log.objects.filter(username=para1)
            return render_to_response('logrecord.html',locals(),context_instance=RequestContext(req))
        else:
            records=tbl_log.objects.filter(username=para1,tbl_name=para2)
            return render_to_response('logrecord.html',locals(),context_instance=RequestContext(req))