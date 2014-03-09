from misApp.models import  ProjectScope, tbl_location, tbl_source,\
    tbl_subscription,tbl_notify,\
    tbl_history
from django.shortcuts import render_to_response
from misApp.pp import i_hasPermission, i_getEmployee, i_getAllStates,\
    i_getActiveSources,\
    i_getActiveMagazines,\
    i_getSubscription, i_getCustomerHasSub,\
    i_getRowsOFDispatch, i_getAllComplaintsOf, i_getLocId, i_getActiveTenures
import datetime
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.utils.dateformat import DateFormat


def v_complementary(req):
    ps=ProjectScope()
    rows=[s  for s in tbl_subscription.objects.filter(isCompliment=True)]
    return render_to_response("complement.html",{'rows':rows,'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))

def v_editComplement(req,pkid):
    if pkid and i_hasPermission(i_getEmployee(req.session.get('username','')),'compliment','u'):
        prefix=ProjectScope().getSubPrefix()
        '''history'''
        #renewalHistory=tbl_renewal.objects.filter(subId=pkid)
        #chistory=tbl_history.objects.filter(subId=pkid)
        #cancels=[[prefix+pkid[1],c.data.split(':')[0],datetime.datetime.strptime(c.data.split(':')[1],'%Y-%m-%d').date,c.date]for c in  chistory.filter(type="can")]
        #extends=renewalHistory.filter(type='a')
        #conversions=chistory.filter(type="m")
        #renewals=renewalHistory.filter(type='r')
        #return HttpResponse(cancels)
        '''________'''
        tenures=i_getActiveTenures()
        magazines=i_getActiveMagazines()
        states=i_getAllStates(1)
        sources=i_getActiveSources(0)
        
        subscription=i_getSubscription(pkid)
        customer=i_getCustomerHasSub(pkid)
        disGifts=i_getRowsOFDispatch(customer.id,'g')
        #ts=customer.transactions.all()
        #return HttpResponse(disGift)
        
        complaints=i_getAllComplaintsOf(subscription.id)
        date=DateFormat(subscription.date).format('d-m-Y')
        subid=prefix+str(subscription.id)
        '''they are surely exist'''
        title=customer.title
        firstname=customer.firstName
        lastname=customer.lastName
        address1=customer.address1
        subSource=customer.subSource
        email=customer.email
        subStatus=None
        if subscription.isActive:
            subStatus='1'
        else:
            subStatus='0'
        '''not sure'''
        stateName=None
        cityName=None
        
        if customer.mobileNo:
            mobileno=customer.mobileNo
        if customer.sex:
            sex=customer.sex
        if customer.combo:
            combo=customer.combo.id
        if customer.age:
            age=customer.age
        if customer.dob:
            dob=DateFormat(customer.dob).format('d-m-Y')
        if customer.designation:
            designation=customer.designation
        if customer.company:
            company=customer.company
        if customer.address2:
            address2=customer.address2
        if customer.address3:
            address3=customer.address3
        if customer.city:
            cityName=customer.city
            city=i_getLocId(cityName)
        if customer.state:
            stateName=customer.state
            state=i_getLocId(stateName)
            cities=tbl_location.objects.filter(pid=state)
        if customer.pincode:
            pincode=customer.pincode
        if customer.tel_O:
            teleo=customer.tel_O
        if customer.tel_R:
            teler=customer.tel_R
        if customer.TRAmnt:
            TRAmnt=customer.TRAmnt
        
       
        
        
        source=tbl_source.objects.get(id=subSource.pid).id
        subsources=tbl_source.objects.filter(pid=source)
        subSourceName=subSource.categoryName
        subSource=subSource.id#so that in Info dropdown value will be subSource id
        if customer.empId:
            empid=ProjectScope().empCodePrefix()+str(customer.empId)
        if subscription.isActive:
            subStatus='1'
        else:
            subStatus='0'
        
        
        submag=subscription.magazine.name
        subperiod=subscription.period
        
        
        
        nr=tbl_notify.objects.get(subId=subscription.id)
        start_issue=str(nr.startDate.month)+"-"+str(nr.startDate.year)
        end_issue=str(nr.subEndDate.month)+"-"+str(nr.subEndDate.year)
        sschemes=customer.scheme.all()
        
        #allSubs=customer.subscriptions.all()
        
        
        
        if req.POST.get('editCom'):
            errors=[]
            cStatus=True
            
            title=req.POST.get('title','')
            firstname=req.POST.get('firstname','').strip()
            lastname=req.POST.get('lastname','').strip()
            dob=req.POST.get('dob','').strip()
            age=req.POST.get('age','').strip()
            sex=req.POST.get('sex','')
            designation=req.POST.get('designation','').strip()
            company=req.POST.get('company','').strip()
            address1=req.POST.get('address1','').strip()
            address2=req.POST.get('address2','').strip()
            address3=req.POST.get('address3','').strip()
            state=int(req.POST.get('state','').strip())
            city=int(req.POST.get('city','').strip())
            pincode=req.POST.get('pincode','').strip()
            teleo=req.POST.get('teleo','').strip()
            teler=req.POST.get('teler','').strip()
            mobileno=req.POST.get('mobileno','').strip()
            email=req.POST.get('email','').strip()
            
            
            source=int(req.POST.get('source','').strip())
            subSource=int(req.POST.get('subSource','').strip())
            empid=req.POST.get('empid','').strip()
            subStatus=req.POST.get('subStatus','').strip()
            
            
            
            
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not firstname:
                errors.append("please enter first Name !")
            elif not lastname:
                errors.append("please enter last Name !")
            
            elif not address1:
                errors.append("please enter address line 1 !")
            elif state==-1:
                errors.append("please select one state !")
            elif city==-1:
                errors.append("please select one city !")
            elif not pincode:
                errors.append("please enter pincode !")
            elif not teleo and not teler and not mobileno:
                errors.append("please enter at least one contact no. !")
            elif mobileno and len(mobileno)!=10:
                    errors.append("Mobile no. must be of 10 digits !")
            #elif not email:
            #    errors.append("please enter email Id !")
            elif email and '@' not in email:
                errors.append("please enter valid email Id !")
            elif source==-1:
                errors.append("please select at least one source !")
            elif source!=-1 and subSource==-1:
                errors.append("please select at least one Source Info !")
            
            else:
                temp=None    
                try:
                    if age:
                        temp='age';age=int(age)
                                        
                    if teleo:
                        temp='telephone(o)';teleo=int(teleo)
                        contactNo=teleo
                    if teler:
                        temp='telephone(r)';teler=int(teler)
                        contactNo=teler
                    if mobileno:
                        temp='mobile no.';mobileno=int(mobileno)
                        contactNo=mobileno
                    
                    if dob:
                        temp='Date Of Birth,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(dob,'%d-%m-%Y')
                    
                                        
                    
                    '''____________________must be execute at last '''
                    
                    temp="employee Id";pre=ProjectScope().empCodePrefix()
                    if empid:
                        if empid[:len(pre)]==pre:
                            int(empid[len(pre):])
                        else:
                            temp="employee Id"
                            raise ValueError
                    
                    '''______________________________________'''
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                if empid:
                    empid=int(empid[len(pre):])
                if state and city and state!=-1 and city!=-1:
                    cityName=tbl_location.objects.get(id=int(city)).name
                    stateName=tbl_location.objects.get(id=int(state)).name
                else:
                    cityName=''
                    stateName=''
                        
                if not age:
                    age=None
                if sex=='-1':
                    sex=None    
                        
                if subStatus=='1':
                    subStatus=True
                else:
                    subStatus=False

                if subSource!=-1:
                    subSource=tbl_source.objects.get(id=subSource)
                    
                if not dob:
                    dob=None
                else:
                    dob=datetime.datetime.strptime(dob,'%d-%m-%Y')

                '''save personal details'''
                customer.title=title
                customer.firstName=firstname
                customer.lastName=lastname
                customer.dob=dob
                customer.age=age
                customer.sex=sex
                customer.designation=designation
                customer.company=company
                customer.address1=address1
                customer.address2=address2
                customer.address3=address3
                customer.state=stateName
                customer.city=cityName
                customer.pincode=pincode
                customer.tel_O=teleo
                customer.tel_R=teler
                customer.mobileNo=mobileno
                customer.email=email
                customer.subSource=subSource
                customer.empId=empid
                
                                
                subscription.isActive=subStatus
                if not subscription.isActive:
                    tbl_history.objects.create(data=subscription.magazine.name+':'+str(subscription.date),custId=customer.id,subId=subscription.id,type='can')
                
                subscription.save()
                customer.save()
                #return HttpResponse(str(teleo)+"/"+str(teler)+"/"+str(mobileno))
                
                return HttpResponseRedirect("/compliment/edit/"+pkid)
            return render_to_response('editComplement.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editComplement.html',locals(),context_instance=RequestContext(req))