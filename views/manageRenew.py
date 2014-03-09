from misApp.pp import i_hasPermission, i_getEmployee, i_getAllStates,\
    i_getActiveMagazines, i_getActiveCombos, i_getActiveTenures,\
    i_getActiveSources, i_getActiveSchemes, i_getActiveGifts,\
    i_setNotificationFor, i_setIssues, i_getCustomerHasSub, i_getLocId
from misApp.models import ProjectScope, tbl_branch, tbl_supportedCourier,\
    tbl_location, tbl_source, tbl_magazineCombo, tbl_customer, tbl_subscription,\
    tbl_transaction, tbl_magazine, tbl_dispatch
import datetime
from misApp.views import v_deductgift
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def v_renew(req,subId):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'sub','u'):
        
        customer=i_getCustomerHasSub(subId)
        date=ProjectScope().dDate()
        states=i_getAllStates(1)
        mags=[[m.id,m.name,False,None,None,None,None,False] for m in i_getActiveMagazines()]  
        combos=i_getActiveCombos()
        tenures=i_getActiveTenures()
        sources=i_getActiveSources(0)
        schemes=i_getActiveSchemes()
        gifts=i_getActiveGifts()
        branches=tbl_branch.objects.filter(isActive=True)
        couriers=tbl_supportedCourier.objects.all()
        date=ProjectScope().dDate()
        #stateName=None
        #cityName=None
        if customer.city:
            cityName=customer.city
            city=i_getLocId(cityName)
        if customer.state:
            stateName=customer.state
            state=i_getLocId(stateName)
            cities=tbl_location.objects.filter(pid=state)
        
        subSource=customer.subSource
        source=tbl_source.objects.get(id=subSource.pid).id
        subSource=subSource.id#so that in subscource dropdown value will be subSource id
        subsources=tbl_source.objects.filter(pid=source)
        #sschemes=[]
        #sgifts=[]
        #for ss in customer.scheme.all():
        #    sschemes.append(ss.id)
        #for sg in customer.gift.all():
        #    sgifts.append(sg.id)
            
        if req.method=="POST":
            errors=[]
            '''
            assuming all subscription will be compliment
            because in all compliments if a single non compliment exists ,then Total Subscription amount must be entered   
            '''
            allCompliments=True
            
            date=req.POST.get('date','')
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
            branch=int(req.POST.get('branch',''))
            courier=int(req.POST.get('courier',''))
            
            '''__________________________________'''
            
            TRAForShow=req.POST.get('TRAForShow','0').strip()
            combo=int(req.POST.get('combo','-1').strip())
            discount=req.POST.get('discount','').strip()
            comdiscount=req.POST.get('comdiscount','').strip()
            addiscount=req.POST.get('addiscount','').strip()
            ocharges=req.POST.get('ocharges','').strip()
            
            sumOfRAmnt=req.POST.get('sumOfRAmnt','').strip()
            sumOfRecAmnt=req.POST.get('sumOfRecAmnt','').strip()
            sumOfEAmnt=req.POST.get('sumOfEAmnt','').strip()
            
            sschemes=req.POST.getlist('sschemes','')
            sschemes=[int(s) for s in sschemes]
            sgifts=req.POST.getlist('sgifts','')
            sgifts=[int(g) for g in sgifts]
                #return HttpResponse(str(sgifts))
            source=int(req.POST.get('source','').strip())
            subSource=int(req.POST.get('subSource','').strip())
            #empid=req.POST.get('empid','').strip()
            
            '''__________________________________'''
            
            paymode=req.POST.get('paymode','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            bank=req.POST.get('bank','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()
            
            
            '''__________________________________'''
            cityName=None
            stateName=None
            schemeName=None
            contactNo=None
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            if source!=-1:
                subsources=tbl_source.objects.filter(pid=source)
            
            hasSM=0
            for m in mags:
                pkid=str(m[0])
                if req.POST.get('c_'+pkid):
                    m[2]=True
                    hasSM=hasSM+1
                    if req.POST.get('com_c_'+pkid):
                        m[7]=True
                    else:
                        allCompliments=False
                
                period=int(req.POST.get('t_'+pkid,''))
                if m[2] and period==-1:
                    errors.append("please select tenure for "+m[1].title())
                else:
                    m[3]=int(period)
                
                
                estAmnt=req.POST.get('estAmnt_'+pkid,'')
                if estAmnt:
                    m[4]=estAmnt
                
                #if req.POST.get('com_c_'+pkid):
                #    
                #    m[7]=True
                #else:
                #    if req.POST.get('c_'+pkid):
                #        allCompliments=False
                    
                
                realAmnt=req.POST.get('realAmount_'+pkid,'')
                if m[2] and not realAmnt and not m[7]:
                    errors.append("please enter offer Price for "+m[1].title())
                    
                else:
                    try:
                        if realAmnt:
                            realAmnt=int(realAmnt)
                            if realAmnt==0:
                                errors.append("please enter valid offer Price for "+m[1].title())
                            else:
                                m[5]=realAmnt
                    except ValueError:
                        errors.append("please enter valid offer Price for "+m[1].title())
                        m[5]=realAmnt
                
                recAmnt=req.POST.get('recAmount_'+pkid,'')
                if not recAmnt:
                    recAmnt=0
                else:
                    try:
                        if recAmnt:
                            recAmnt=int(recAmnt)
                            m[6]=recAmnt
                    except ValueError:
                        errors.append("please enter valid received amount for "+m[1].title())
                        m[6]=recAmnt
            
            
            if hasSM==0:
                errors.append("please select at least one magazine !") 
                    
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
            elif sumOfRAmnt==0 and not allCompliments:
                errors.append("total subscription amount can not be 0 !")
            elif paymode=='-1' and not allCompliments:
                errors.append("please select one payment mode !")
            elif paymode!='out' and paymode!='-1' and not sumOfRecAmnt:
                errors.append("please enter total received amount or change Payment mode !")
            elif paymode=='out' and sumOfRecAmnt:
                errors.append("please remove total received amount OR change payment mode !")
            else:
                temp=None    
                try:
                    if not allCompliments:
                        temp='total subscription amount';sumOfRAmnt=int(sumOfRAmnt)
                    
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
                    
                    if discount:
                        temp='discount';discount=int(discount)
                    else:
                        discount=0
                    
                    if comdiscount:
                        temp='commission discount';comdiscount=int(comdiscount)
                    else:
                        comdiscount=0
                    
                    if addiscount:
                        temp='additional discount';addiscount=int(addiscount)
                    else:
                        addiscount=0
                    
                    if ocharges:
                        temp='other charges';ocharges=int(ocharges)
                    else:
                        ocharges=0
                    
                    if sumOfRecAmnt:
                        temp='total received amount';sumOfRecAmnt=int(sumOfRecAmnt)
                    else:
                        sumOfRecAmnt=0
                    
                    
                    
                    if state!=-1:
                        stateName=tbl_location.objects.get(id=int(state)).name
                    else:
                        stateName=None
                    
                    if city!=-1:
                        cityName=tbl_location.objects.get(id=int(city)).name
                    else:
                        cityName=None
                    
                    if dob:
                        temp='Date Of Birth,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(dob,'%d-%m-%Y')
                    
                    if chequedate:
                        temp='Cheque DD date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                    if depositedate:
                        temp='Cheque/DD Deposite Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                    if cleardate:
                        temp='Cheque/DD Clearance Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                    
                    
                        
                    
                    #temp="employee Id";pre=ProjectScope().empCodePrefix()
                    #if empid:
                    #    if empid[:len(pre)]==pre:
                    #        int(empid[len(pre):])
                    #    else:
                    #        temp="employee Id"
                    #        raise ValueError
                
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
                
            
            
                    
                
            if not errors:
                #return HttpResponse(mags)
                '''____________________must be execute at last '''
                #if empid:
                #    empid=int(empid[len(pre):])
                if not age:
                    age=None
                if sex=='-1':
                    sex=None    
                #if not empid:
                #    empid=None
                if not sumOfRAmnt:
                    sumOfRAmnt=0
                
                if subSource!=-1:
                    subSource=tbl_source.objects.get(id=subSource)
                
                if combo!=-1:
                    combo=tbl_magazineCombo.objects.get(id=combo)
                else:
                    combo=None
                
                if branch!=-1:
                    branch=tbl_branch.objects.get(id=branch)
                else:
                    branch=None
                
                if courier!=-1:
                    courier=tbl_supportedCourier.objects.get(id=courier)
                else:
                    courier=None
                    
                if not chequedate:
                    chequedate=None
                else:
                    chequedate=datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                if not depositedate:
                    depositedate=None
                else:
                    depositedate=datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                if not cleardate:
                    cleardate=None
                else:
                    cleardate=datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                    
                if not dob:
                    dob=None
                else:
                    dob=datetime.datetime.strptime(dob,'%d-%m-%Y')
                '''______________________________________'''
                createdSubIDs=''
                #return HttpResponse(str(empid)+"/"+str(subSource)+"/"+str(combo)+"/"+str(sumOfRAmnt)+"/"+str(sumOfRecAmnt)+"/"+str(discount)+"/"+str(comdiscount)+"/"+str(addiscount)+"/"+str(title)+"/"+str(firstname)+"/"+str(lastname)+"/"+str(dob)+"/"+str(age)+"/"+str(sex)+"/"+str(designation)+"/"+str(company)+"/"+str(address1)+"/"+str(address2)+"/"+str(address3)+"/"+str(stateName)+"/"+cityName+"/"+str(pincode)+"/"+str(teleo)+"/"+str(teler)+"/"+str(mobileno)+"/"+str(email))
                new_customer=tbl_customer.objects.create(branch=branch,courier=courier,empId=i_getEmployee(req.session.get('username','')).id,subSource=subSource,combo=combo,TSAmnt=sumOfRAmnt,TRAmnt=sumOfRecAmnt,title=title,firstName=firstname,lastName=lastname,dob=dob,age=age,sex=sex,designation=designation,company=company,address1=address1,address2=address2,address3=address3,state=stateName,city=cityName,pincode=pincode,tel_O=teleo,tel_R=teler,mobileNo=mobileno,email=email,isActive=True)
                for sm in mags:
                    if sm[2]:
                        new_sub=tbl_subscription.objects.create(period=sm[3],magazine=tbl_magazine.objects.get(id=sm[0]),subAmnt=sm[5],recAmnt=sm[6],isActive=True)
                        new_customer.subscriptions.add(new_sub)
                        i_setNotificationFor(new_sub.id,ProjectScope().getDate(),sm[3])
                        i_setIssues(new_sub)
                        if not sm[7]:
                            '''when subscription is not compliment'''
                            createdSubIDs=createdSubIDs+str(new_sub.id)+','
                        
                        '''when compliment,mark subscription'''
                        new_sub.isCompliment=sm[7]
                        new_sub.save()
                if hasSM==1 and not allCompliments:
                    new_customer.transactions.add(tbl_transaction.objects.create(oCharges=ocharges,dis=discount,comdis=comdiscount,addis=addiscount,OSAmnt=(sumOfRAmnt+ocharges)-(sumOfRecAmnt+comdiscount+addiscount),amount=sumOfRecAmnt,payMode=paymode,subId=createdSubIDs,chequeDate=chequedate,chequeNo=chequeno,bankName=bank,depositeDate=depositedate,clearDate=cleardate))
                else:
                    new_customer.transactions.add(tbl_transaction.objects.create(oCharges=ocharges,dis=discount,comdis=comdiscount,addis=addiscount,OSAmnt=(sumOfRAmnt+ocharges)-(sumOfRecAmnt+comdiscount+addiscount),amount=sumOfRecAmnt,payMode=paymode,subId=createdSubIDs,chequeDate=chequedate,chequeNo=chequeno,bankName=bank,depositeDate=depositedate,clearDate=cleardate))
                
                
                for sg in sgifts:
                    new_customer.gift.add(sg)
                    tbl_dispatch.objects.create(customerId=new_customer.id,subId=None,receiverContact=contactNo,dispatchAddress1=address1,status='i',itemType='g',itemCode=sg,quantity=1)
                
                if -1 not in sschemes:
                    for ss in sschemes:
                        new_customer.scheme.add(ss)
                v_deductgift(req,new_customer.id)
                
                if allCompliments:
                    return HttpResponseRedirect("/compliment/")
                else:
                    return HttpResponseRedirect("/subscription/list")
                
            return render_to_response('manageRenew.html',locals(),context_instance=RequestContext(req))
        return render_to_response('manageRenew.html',locals(),context_instance=RequestContext(req))