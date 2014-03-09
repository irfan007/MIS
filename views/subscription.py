from misApp.models import ProjectScope, tbl_location, tbl_source,\
    tbl_magazineCombo, tbl_customer, tbl_subscription, tbl_transaction,\
    tbl_dispatch, tbl_renewal, tbl_history, tbl_notify, tbl_magazine,\
    tbl_supportedCourier, tbl_branch
from misApp.pp import i_hasPermission, i_getEmployee, i_getCustomerHasSub,\
    i_getActiveSubscription, i_getAllStates, i_getActiveCombos,\
    i_getActiveTenures, i_getActiveSources, i_getActiveSchemes, i_getActiveGifts,\
    i_getActiveMagazines, i_setNotificationFor, i_getSubscription,\
    i_getRowsOFDispatch, i_getAllComplaintsOf, i_getLocId,\
    i_getInactiveSubscription, i_setIssues
    
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.dateformat import DateFormat
from misApp.views import v_deductgift


def v_customer(req):
    '''
    list customers either active/inactive order by id
    with navigation control on page 
    '''
    ps=ProjectScope()
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','v'):
        try:
            customers=[c for c in tbl_customer.objects.all().order_by('id')]
            totalRows=len(customers)
            FROM=1
            TO=totalRows
            hasNext=False
            if len(customers)>ps.SBRPP:
                hasNext=True
                TO=ps.SBRPP
        except:
            pass
        
        nextStart=ps.SBRPP
        customers=customers[:ps.SBRPP]
        return render_to_response('customerList.html',locals(),context_instance=RequestContext(req))


def v_subscription(req,url):
    '''
    manage subscription based on 'option type' captured on url path as (list,add,edit,extend,renew)
    
    * listlisting also done searching based on parameters defined on subscription list page  and has navigation control
    
    
    '''
    options=url.split('/')
    ps=ProjectScope()
    totalRows=0
    if options[0]=='list' and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','v'):
        if req.POST.get('advancesearch',''):
            searchsubid=req.POST.get('searchsubid','').strip()
            searchfname=req.POST.get('searchfname','').strip()
            searchlname=req.POST.get('searchlname','').strip()
            
            searchdesig=req.POST.get('searchdesig','').strip()
            
            searchcompany=req.POST.get('searchcompany','').strip()
            searchcustId=req.POST.get('searchcustId','').strip()
            
            searchemail=req.POST.get('searchemail','').strip()
            
            searchcontactno=req.POST.get('searchcontactno','').strip()
            temp=[]
            list=[]
            customer=tbl_customer.objects.filter(firstName__contains=searchfname,lastName__contains=searchlname,\
                                                    designation__contains=searchdesig,company__contains=searchcompany,\
                                                    email__contains=searchemail,mobileNo__contains=searchcontactno)
                
            if searchcustId:
                
                    if searchcustId[:len(ProjectScope().getCustomerPrefix())].upper()==ProjectScope().getCustomerPrefix():
                        try:
                            customer=customer.filter(id=int(searchcustId[len(ProjectScope().getCustomerPrefix()):]))
                        except:
                            return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
                    else:
                        return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
                    if searchsubid:
                        if searchsubid[:len(ProjectScope().getSubPrefix())].upper()==ProjectScope().getSubPrefix():
                            try:
                                for item in customer:
                                    for subscription in item.subscriptions.filter(id=int(searchsubid[len(ProjectScope().getSubPrefix()):]),isActive=True):
                                        list.append(item.getcusID())
                                        list.append(subscription.getsubID())
                                        list.append(item.firstName+' '+item.lastName)
                                        list.append(subscription.date)
                                        list.append(item.city)
                                        list.append(item.mobileNo)
                                        list.append(subscription.isActive)
                                        list.append(subscription.id)
                                        temp.append(list)
                                        list=[]
                    
                                return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
                            except:
                                return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
            else:
                if searchsubid:
                    if searchsubid[:len(ProjectScope().getSubPrefix())].upper()==ProjectScope().getSubPrefix():
                        try:
                            getSubscription=tbl_subscription.objects.get(id=int(searchsubid[len(ProjectScope().getSubPrefix()):]))
                            customer=customer.filter(subscriptions=getSubscription)
                            for item in customer:
                                for subscription in item.subscriptions.filter(id=getSubscription.id,isActive=True):
                                    list.append(item.getcusID())
                                    list.append(subscription.getsubID())
                                    list.append(item.firstName+' '+item.lastName)
                                    list.append(subscription.date)
                                    list.append(item.city)
                                    list.append(item.mobileNo)
                                    list.append(subscription.isActive)
                                    list.append(subscription.id)
                                    temp.append(list)
                                    list=[]
                                    
                            return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
                            
                        except:
                            
                
                            return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
                    else:
                        return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))
            for item in customer:
                for subscription in item.subscriptions.filter(isActive=True):
                    list.append(item.getcusID())
                    list.append(subscription.getsubID())
                    list.append(item.firstName+' '+item.lastName)
                    list.append(subscription.date)
                    list.append(item.city)
                    list.append(item.mobileNo)
                    list.append(subscription.isActive)
                    list.append(subscription.id)
                    temp.append(list)
                    list=[]
                    
            return render_to_response('advancesearch.html',locals(),context_instance=RequestContext(req))        
                    


        
        
        
        try:
            rows=None
            customer=tbl_customer.objects.get(id=options[1])
            subs=customer.subscriptions.all()
            
            return render_to_response('subscriptionList.html',{'cust':customer,'byCustomer':True,'cid':customer.id,'subs':subs,'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
        except:
            rows=None
            rows=[s for s in tbl_subscription.objects.filter(isActive=True,isCompliment=False,isSuspend=False).order_by('id')]
            
            
            totalRows=len(rows)
            FROM=1
            TO=totalRows
            hasNext=False
            if len(rows)>ps.SPP:
                hasNext=True
                TO=ps.SPP
            
            return render_to_response('subscriptionList.html',{'FROM':FROM,'TO':TO,'nextStart':ps.SPP,'hasNext':hasNext,'hasPre':False,'totalRows':totalRows,'rows':rows[:ps.SPP],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
    
    
    elif options[0]=='add' and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','a'):
        '''
         mags is 2d array of 1-d array of each magazine, shows on add subscription page
         1-d has format like [ 0 magazine ID , 1 magazine Name , 2 is selected , 3 period in month , 4 MRP price , 5 offer price , 6 received price ,7 is complement ]
           
        '''
        date=ProjectScope().dDate()
        countries=tbl_location.objects.filter(pid=0)
        #states=i_getAllStates(1)
        mags=[[m.id,m.name,False,None,None,None,None,False] for m in i_getActiveMagazines()]  
        combos=i_getActiveCombos()
        tenures=i_getActiveTenures()
        sources=i_getActiveSources(0)
        schemes=i_getActiveSchemes()
        gifts=i_getActiveGifts()
        branches=tbl_branch.objects.filter(isActive=True)
        couriers=tbl_supportedCourier.objects.all()
        warned='n'#default warning status is no means not warn a user before
        
        if req.POST.get('addSub'):
            errors=[]
            warns=[]
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
            country=int(req.POST.get('country','').strip())
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
            
            TRAForShow=req.POST.get('TRAForShow','0').strip()#will not store,show off on payment tab 
            
            combo=int(req.POST.get('combo','-1').strip())
            discount=req.POST.get('discount','').strip()
            comdiscount=req.POST.get('comdiscount','').strip()
            addiscount=req.POST.get('addiscount','').strip()
            ocharges=req.POST.get('ocharges','').strip()
            
            sumOfRAmnt=req.POST.get('sumOfRAmnt','').strip()#form total subscription price
            sumOfRecAmnt=req.POST.get('sumOfRecAmnt','').strip()#form total received amount
            sumOfEAmnt=req.POST.get('sumOfEAmnt','').strip()#will not store (form total MRP price) 
            
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
            if country!=-1:
                states=tbl_location.objects.filter(pid=country)
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
                    
                    if not datetime.datetime.strptime(dob,'%d-%m-%Y')<datetime.datetime.today():
                        errors.append('Invalid Date Of Birth !')
                    
                    if chequedate:
                        temp='Cheque DD date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                    if depositedate:
                        temp='Cheque/DD Deposite Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                    if cleardate:
                        temp='Cheque/DD Clearance Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                    
                    if mobileno!='':
                        if tbl_customer.objects.filter(mobileNo=mobileno):
                            warns.append("Subscriber with this mobile no. already exist")
                    if email!='':
                        if tbl_customer.objects.filter(email=email):
                            warns.append("Subscriber with this email Id already exist")
                            
                    if warns:
                        warns.append(",to Continue please submit")
                        
                    
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
                
            
            ''' warn a customer if not already warned '''
            if req.POST.get('warned','')=='n':
                if warns:
                    warned='y'
                    return render_to_response('addSubscription.html',locals(),context_instance=RequestContext(req))
                    
                
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
                
                
                createdSubIDs=''#contain non compliment subs id , for storing in transaction done for which subscriptions
                '''
                first created customer then create subscription one by one and add it to customer 
                '''
                #return HttpResponse(str(empid)+"/"+str(subSource)+"/"+str(combo)+"/"+str(sumOfRAmnt)+"/"+str(sumOfRecAmnt)+"/"+str(discount)+"/"+str(comdiscount)+"/"+str(addiscount)+"/"+str(title)+"/"+str(firstname)+"/"+str(lastname)+"/"+str(dob)+"/"+str(age)+"/"+str(sex)+"/"+str(designation)+"/"+str(company)+"/"+str(address1)+"/"+str(address2)+"/"+str(address3)+"/"+str(stateName)+"/"+cityName+"/"+str(pincode)+"/"+str(teleo)+"/"+str(teler)+"/"+str(mobileno)+"/"+str(email))
                new_customer=tbl_customer.objects.create(branch=branch,courier=courier,empId=i_getEmployee(req.session.get('username','')).id,subSource=subSource,combo=combo,TSAmnt=sumOfRAmnt,TRAmnt=sumOfRecAmnt,title=title,firstName=firstname,lastName=lastname,dob=dob,age=age,sex=sex,designation=designation,company=company,address1=address1,address2=address2,address3=address3,state=stateName,city=cityName,pincode=pincode,tel_O=teleo,tel_R=teler,mobileNo=mobileno,email=email,isActive=True)
                for sm in mags:
                    if sm[2]:
                        new_sub=tbl_subscription.objects.create(cId=new_customer.id,cName=firstname+' '+lastname,cCity=cityName,period=sm[3],magazine=tbl_magazine.objects.get(id=sm[0]),subAmnt=sm[5],recAmnt=sm[6],isActive=True)
                        new_customer.subscriptions.add(new_sub)
                        i_setNotificationFor(new_sub.id,ProjectScope().getDate(),sm[3])
                        i_setIssues(new_sub)
                        if not sm[7]:
                            '''when subscription is not compliment'''
                            createdSubIDs=createdSubIDs+str(new_sub.id)+','
                        
                        '''when compliment,mark subscription'''
                        new_sub.isCompliment=sm[7]
                        new_sub.save()
                        
                '''
                creating transaction for each
                '''        
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
                v_deductgift(req,new_customer.id)#manage stock
                
                if allCompliments:
                    return HttpResponseRedirect("/compliment/")
                else:
                    return HttpResponseRedirect("/subscription/list")
                
            return render_to_response('addSubscription.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addSubscription.html',locals(),context_instance=RequestContext(req))
    
    elif options[0]=='edit' and options[1] and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','u'):
        prefix=ProjectScope().getSubPrefix()
        '''history'''
        renewalHistory=tbl_renewal.objects.filter(subId=options[1])
        chistory=tbl_history.objects.filter(subId=options[1])#all history of edit subscription
        cancels=[[prefix+options[1],c.data.split(':')[0],datetime.datetime.strptime(c.data.split(':')[1],'%Y-%m-%d').date,c.date]for c in  chistory.filter(type="can")]
        extends=renewalHistory.filter(type='a')
        conversions=chistory.filter(type="m")
        renewals=renewalHistory.filter(type='r')
        suspends=chistory.filter(type='sus')
        #return HttpResponse(suspends)
        '''________'''
        tenures=i_getActiveTenures()
        magazines=i_getActiveMagazines()
        countries=tbl_location.objects.filter(pid=0)
        
        #states=i_getAllStates(1)
        sources=i_getActiveSources(0)
        
        subscription=i_getSubscription(options[1])
        customer=i_getCustomerHasSub(options[1])
        disGifts=i_getRowsOFDispatch(customer.id,'g')
        ts=customer.transactions.all()
        #return HttpResponse(disGift)
        
        complaints=i_getAllComplaintsOf(subscription.id)
        date=DateFormat(subscription.date).format('d-m-Y')
        subid=prefix+str(subscription.id)
        '''they are surely exist'''
        title=customer.title
        firstname=customer.firstName
        lastname=customer.lastName
        address1=customer.address1
        if customer.subSource:
            subSource=customer.subSource
            source=tbl_source.objects.get(id=subSource.pid).id
            #subSourceName=subSource.categoryName
            subSource=subSource.id#so that in subscource dropdown value will be subSource id
            subsources=tbl_source.objects.filter(pid=source)
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
            
            country=tbl_location.objects.get(id=tbl_location.objects.get(name=customer.state).pid)
            states=tbl_location.objects.filter(pid=country.id)
            country=country.id
        if customer.pincode:
            pincode=customer.pincode
        if customer.tel_O:
            teleo=customer.tel_O
        if customer.tel_R:
            teler=customer.tel_R
        if customer.TRAmnt:
            TRAmnt=customer.TRAmnt
        
        #if customer.dis:
        #   dis=customer.dis
        
        #if customer.comdis:
        #    comdis=customer.comdis
        
        #if customer.addis:
        #    addis=customer.addis
        
        
        
        if customer.empId:
            empid=ProjectScope().empCodePrefix()+str(customer.empId)
        if subscription.isActive:
            subStatus='1'
        else:
            subStatus='0'
        
        #return HttpResponse(subStatus)
        submag=subscription.magazine.name
        subperiod=subscription.period
        subamnt=subscription.subAmnt
        if subscription.recAmnt:
            recamnt=subscription.recAmnt
        else:
            recamnt=0
        
        TSAmnt=customer.TSAmnt
        
        nr=tbl_notify.objects.get(subId=subscription.id)
        start_issue=str(nr.startDate.month)+"-"+str(nr.startDate.year)
        end_issue=str(nr.subEndDate.month)+"-"+str(nr.subEndDate.year)
        sschemes=customer.scheme.all()
        
        allSubs=customer.subscriptions.all()
        
        
        
        if req.POST.get('editSub'):
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
            country=int(req.POST.get('country','').strip())
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
            
            #dis=req.POST.get('dis','').strip()
            #comdis=req.POST.get('comdis','').strip()
            #addis=req.POST.get('addis','').strip()
            
            TSAmnt=req.POST.get('TSAmnt','').strip()
            TRAmnt=req.POST.get('TRAmnt','').strip()
            
            
            '''_______________'''
            
            for s in allSubs:
                pkid=str(s.id)
                
                if req.POST.get('samnt_'+pkid,'').strip():
                    try:
                        if subscription.id==s.id:
                            subscription.subAmnt=int(req.POST.get('samnt_'+pkid,'').strip())
                        else:
                            s.subAmnt=int(req.POST.get('samnt_'+pkid,'').strip())
                            s.save()
                    except ValueError:
                        errors.append("Invalid subscription amount of "+s.magazine.name+" !")
                else:
                    if not s.isCompliment:
                        errors.append("please enter subscription amount of "+s.magazine.name+" !")
                
                if req.POST.get('ramnt_'+pkid,'').strip():
                    try:
                        if subscription.id==s.id:
                            subscription.recAmnt=int(req.POST.get('ramnt_'+pkid,'').strip())
                        else:
                            s.recAmnt=int(req.POST.get('ramnt_'+pkid,'').strip())
                            s.save()
                    except ValueError:
                        errors.append("Invalid received amount of "+s.magazine.name+" !")
                #return HttpResponse(str(s.subAmnt)+":"+str(s.recAmnt))
                
            
            '''_______________'''
            
            
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
            elif not TSAmnt:
                errors.append("please enter total subscription amount !")
            else:
                temp=None    
                try:
                    
                    #temp='total subscription amount';sumOfRAmnt=int(sumOfRAmnt)
                    
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
                    
                    if not datetime.datetime.strptime(dob,'%d-%m-%Y')<datetime.datetime.today():
                        errors.append('Invalid Date Of Birth !')
                                        
                    if TSAmnt:
                        temp='total subscription amount';TSAmnt=int(TSAmnt)
                    else:
                        TSAmnt=0    
                    if TRAmnt:
                        temp='total received amount';TRAmnt=int(TRAmnt)
                    else:
                        TRAmnt=0
                    
                    #if dis:
                    #    temp='discount';dis=int(dis)
                    #else:
                    #    dis=0
                    
                    #if comdis:
                    #    temp='commission discount';comdis=int(comdis)
                    #else:
                    #    comdis=0
                    
                    #if addis:
                    #    temp='additional discount';addis=int(addis)
                    #else:
                    #    addis=0
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
                if not empid:
                    empid=None
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
                
                #customer.dis=dis
                #customer.comdis=comdis
                #customer.addis=addis
                customer.TSAmnt=TSAmnt
                customer.TRAmnt=TRAmnt
                
                subscription.isActive=subStatus
                if not subscription.isActive:
                    tbl_history.objects.create(data=subscription.magazine.name+':'+str(subscription.date),custId=customer.id,subId=subscription.id,type='can')
                
                customer.subscriptions.all().update(cName=firstname+' '+lastname,cCity=cityName)
                subscription.save()
                
                
                
                
                
                if customer.subscriptions.filter(isActive=True):
                    customer.isActive=True
                else:
                    customer.isActive=False
                
                customer.save()
                #return HttpResponse(str(teleo)+"/"+str(teler)+"/"+str(mobileno))
                
                return HttpResponseRedirect("/subscription/edit/"+options[1])
            return render_to_response('editSubscription.html',locals(),context_instance=RequestContext(req))
        return render_to_response('editSubscription.html',locals(),context_instance=RequestContext(req))
    elif options[0]=='extend' and options[1] and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','u'):
        
        csub=tbl_subscription.objects.get(id=options[1])
        ccust=i_getCustomerHasSub(csub)
        nt=tbl_notify.objects.get(subId=csub.id)
        subPrefix=ProjectScope().getSubPrefix()
        subid=subPrefix+str(csub.id)
        date=csub.date
        submag=csub.magazine.id
        start_issue=DateFormat(nt.startDate).format('M Y')
        end_issue=DateFormat(nt.subEndDate).format('M Y')
        
        magazines=i_getActiveMagazines()
        schemes=i_getActiveSchemes()
        gifts=i_getActiveGifts()
        
        #sschemes=[s.id for s in ccust.scheme.all()]
        #sgifts=[s.id for s in ccust.gift.all()]
        warn=1
        if req.POST.get('extendSub'):
            errors=[]
            warns=[]
            warn=int(req.POST.get('warn',''))
            
            submag=int(req.POST.get('submag',''))
            experiod=req.POST.get('experiod','')
            exsubamnt=req.POST.get('exsubamnt','')
            exrecamnt=req.POST.get('exrecamnt','')
            
            paymode=req.POST.get('paymode','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            bank=req.POST.get('bank','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()

            sschemes=req.POST.getlist('sschemes','')
            sschemes=[int(s) for s in sschemes]
            sgifts=req.POST.getlist('sgifts','')
            sgifts=[int(g) for g in sgifts]
            
            dis=req.POST.get('dis','').strip()
            comdis=req.POST.get('comdis','').strip()
            addis=req.POST.get('addis','').strip()
            #return HttpResponse(str(sgifts))
            today=ProjectScope().getDate()
            #return HttpResponse(str(nt.subEndDate.month)+"="+str(today.month)+"  "+str(nt.subEndDate.year)+"="+str(today.year)+"  "+str(today.day)+" >20")
            if submag==-1:
                errors.append("please select at least one magazine !")
            elif not experiod:
                errors.append("please enter extend period !")
            elif not exsubamnt:
                errors.append("please enter extend subscription amount !")
            elif not exrecamnt:
                errors.append("please enter extend received amount !")
            elif nt.subEndDate.month==today.month and nt.subEndDate.year==today.year and today.day >20 :
                errors.append("Subscription can only be extend before 20th of subscription end Month !")
            elif not csub.isActive:
                errors.append("Subscription must be renewed first !")
            elif paymode=='-1':
                errors.append("please select one payment mode !")
            
            else:
                temp=None    
                try:
                    temp='extend period ';experiod=int(experiod)
                    temp='extend subscription amount ';exsubamnt=int(exsubamnt)
                    temp='extend received amount ';exrecamnt=int(exrecamnt)
                    if experiod==0:
                        errors.append("Extend period can not be 0 !")
                    if (experiod+csub.period)<0:
                        errors.append("decreasing period exceeds old subscription period !")
                    if chequedate:
                        temp='Cheque DD date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                    if depositedate:
                        temp='Cheque/DD Deposite Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                    if cleardate:
                        temp='Cheque/DD Clearance Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                    
                    if dis:
                        temp='discount';dis=int(dis)
                    else:
                        dis=0
                    
                    if comdis:
                        temp='commission discount';comdis=int(comdis)
                    else:
                        comdis=0
                    
                    if addis:
                        temp='additional discount';addis=int(addis)
                    else:
                        addis=0
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
                
                if csub.magazine.id!=submag and warn==1:
                    warns.append("you have changed old magazine that cause conversion,for continue click on save button!")
                    warn=0
            
            if not errors and not warns:
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
                    
                '''history renewal in advance '''
                tempSchemes=''
                tempGifts=''
                for  s in ccust.scheme.all():
                    tempSchemes=tempSchemes+s.name+':'
                for  g in ccust.gift.all():
                    tempGifts=tempGifts+g.name+':'
                tbl_renewal.objects.create(type='a',custId=ccust.id,subId=csub.id,magazines=csub.magazine.name,periods=str(csub.period)+'-'+str(experiod)+'-'+str((csub.period+experiod)),mrps=csub.magazine.price,subAmnts=csub.subAmnt,recAmnts=csub.recAmnt,dis=dis,comdis=comdis,addis=addis,scheme=tempSchemes,gift=tempGifts,TSAmnt=ccust.TSAmnt,TRAmnt=ccust.TRAmnt)
                '''___________________'''
                
                for sg in sgifts:
                    ccust.gift.add(sg)
                    tbl_dispatch.objects.create(customerId=ccust.id,subId=None,receiverContact=ccust.mobileNo,dispatchAddress1=ccust.address1,status='i',itemType='g',itemCode=sg,quantity=1)
                
                for ss in sschemes:
                    ccust.scheme.add(ss)
                
                '''history magazine conversion part1'''
                oldData=None
                newData=None
                if csub.magazine.id!=submag:
                    oldData=csub.magazine.name+':'+str(nt.startDate)+':'+str(nt.subEndDate)+":"+str(nt.subPeriod)
                    
                '''___________________'''
                
                    
                csub.magazine=tbl_magazine.objects.get(id=submag)    
                csub.period=experiod+csub.period
                
                csub.subAmnt=csub.subAmnt+exsubamnt
                csub.recAmnt=csub.recAmnt+exrecamnt
                ccust.TSAmnt=ccust.TSAmnt+exsubamnt
                ccust.TRAmnt=ccust.TRAmnt+exrecamnt
                
                '''
                delete old notification data
                '''
                nt.delete()
                csub.save()
                ccust.save()
                
                '''
                create new notification data
                '''
                i_setNotificationFor(csub.id,csub.date,csub.period)
                
                
                '''
                add transaction for extend amount 
                '''
                ccust.transactions.add(tbl_transaction.objects.create(dis=dis,comdis=comdis,addis=addis,OSAmnt=exsubamnt-(exrecamnt+dis+comdis+addis),amount=exrecamnt,payMode=paymode,subId=csub.id,chequeDate=chequedate,chequeNo=chequeno,bankName=bank,depositeDate=depositedate,clearDate=cleardate))
                '''history magazine conversion part2'''
                
                
                '''
                finally setting extend history(required before and after both detail) by part 1 & 2 
                '''
                if oldData:
                    lnt=tbl_notify.objects.get(subId=csub.id)
                    newData=csub.magazine.name+':'+str(lnt.startDate)+':'+str(lnt.subEndDate)+":"+str(lnt.subPeriod)
                    tbl_history.objects.create(data=oldData+"::"+newData,custId=ccust.id,subId=csub.id,type='m')
                '''_______________'''
                    
                    
                
                return HttpResponseRedirect('/subscription/edit/'+options[1])
            return render_to_response('extendSubscription.html',locals(),context_instance=RequestContext(req))
        return render_to_response('extendSubscription.html',locals(),context_instance=RequestContext(req))
    elif options[0]=='renew' and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','v'):
        '''
        listing and renewal done by same function
        '''
        flag=None  #default is listing
        try:
            if options[1]:#option 1 mean when an integer is passed in url string, for renewal 
                flag=True
        except:
            pass
        
        
        if not flag:
            rows=None
            try:
                rows=[s for s in tbl_subscription.objects.filter(isActive=False).order_by('id')]
            except:
                pass
            
            totalRows=len(rows)
            FROM=1
            TO=totalRows
            hasNext=False
            if len(rows)>ps.SPP:
                hasNext=True
                TO=ps.SPP
            
            return render_to_response('renewalList.html',{'FROM':FROM,'TO':TO,'nextStart':ps.SPP,'hasNext':hasNext,'hasPre':False,'totalRows':totalRows,'rows':rows[:ps.SPP],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
        elif flag and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','u'):
            prefix=ProjectScope().getSubPrefix()
            
            '''history'''
            renewalHistory=tbl_renewal.objects.filter(subId=options[1])
            chistory=tbl_history.objects.filter(subId=options[1])
            
            cancels=[[prefix+options[1],c.data.split(':')[0],datetime.datetime.strptime(c.data.split(':')[1],'%Y-%m-%d').date,c.date]for c in  chistory.filter(type="can")]
            extends=renewalHistory.filter(type='a')
            conversions=chistory.filter(type="m")
            '''________'''
            
            schemes=i_getActiveSchemes()
            gifts=i_getActiveGifts()
            
            tenures=i_getActiveTenures()
            magazines=i_getActiveMagazines()
            #states=i_getAllStates(1)
            countries=tbl_location.objects.filter(pid=0)
            sources=i_getActiveSources(0)
            
            subscription=i_getSubscription(options[1])
            customer=i_getCustomerHasSub(subscription.id)
            
            date=DateFormat(subscription.date).format('d-m-Y')
            subid=prefix+str(subscription.id)
            '''they are surely exist'''
            title=customer.title
            firstname=customer.firstName
            lastname=customer.lastName
            address1=customer.address1
            if customer.subSource:
                subSource=customer.subSource
                source=tbl_source.objects.get(id=subSource.pid).id
                #subSourceName=subSource.categoryName
                subsources=tbl_source.objects.filter(pid=source)
                subSource=subSource.id
                #so that in Info dropdown value will be subSource id
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
                
                country=tbl_location.objects.get(id=tbl_location.objects.get(name=customer.state).pid)
                states=tbl_location.objects.filter(pid=country.id)
                country=country.id
            if customer.pincode:
                pincode=customer.pincode
            if customer.tel_O:
                teleo=customer.tel_O
            if customer.tel_R:
                teler=customer.tel_R
            if customer.TRAmnt:
                TRAmnt=customer.TRAmnt
        
            #if customer.dis:
            #    dis=customer.dis
        
            #if customer.comdis:
            #    comdis=customer.comdis
        
            #if customer.addis:
            #    addis=customer.addis
        
            
            #if customer.empId:
            #    empid=ProjectScope().empCodePrefix()+str(customer.empId)
            if subscription.isActive:
                subStatus='1'
            else:
                subStatus='0'
                
            #return HttpResponse(subStatus)
            submag=subscription.magazine.id
            
            sschemes=[s.id for s in customer.scheme.all()]
            
            if req.POST.get('renewSub'):
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
                country=int(req.POST.get('country','').strip())
                state=int(req.POST.get('state','').strip())
                city=int(req.POST.get('city','').strip())
                pincode=req.POST.get('pincode','').strip()
                teleo=req.POST.get('teleo','').strip()
                teler=req.POST.get('teler','').strip()
                mobileno=req.POST.get('mobileno','').strip()
                email=req.POST.get('email','').strip()
            
                submag=int(req.POST.get('submag','').strip())
                subperiod=int(req.POST.get('subperiod','').strip())
                subamnt=req.POST.get('subamnt','').strip()
                rows=[[i_getCustomerHasSub(s),s]for s in i_getInactiveSubscription().order_by('-id')]
                recamnt=req.POST.get('recamnt','').strip()
                
                sschemes=req.POST.getlist('sschemes','')
                sschemes=[int(s) for s in sschemes]
                sgifts=req.POST.getlist('sgifts','')
                sgifts=[int(g) for g in sgifts]
                
                source=int(req.POST.get('source','').strip())
                subSource=int(req.POST.get('subSource','').strip())
                #empid=req.POST.get('empid','').strip()
                subStatus=req.POST.get('subStatus','').strip()
                
                
                paymode=req.POST.get('paymode','').strip()
                chequedate=req.POST.get('chequedate','').strip()
                chequeno=req.POST.get('chequeno','').strip()
                bank=req.POST.get('bank','').strip()
                depositedate=req.POST.get('depositedate','').strip()
                cleardate=req.POST.get('cleardate','').strip()
                
                
                dis=req.POST.get('dis','').strip()
                comdis=req.POST.get('comdis','').strip()
                addis=req.POST.get('addis','').strip()
                
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
                elif subperiod==-1:
                    errors.append("please select one period !")
                elif source==-1:
                    errors.append("please select at least one source !")
                elif source!=-1 and subSource==-1:
                    errors.append("please select at least one Source Info !")
                elif submag==-1:
                    errors.append("please select one magazine !")
                elif paymode=='-1':
                    errors.append("please select one payment mode !")
                elif not subamnt:
                    errors.append("please enter subscription amount !")
                else:
                    temp=None    
                    try:
                        if state and city and state!=-1 and city!=-1:
                            cityName=tbl_location.objects.get(id=int(city)).name
                            stateName=tbl_location.objects.get(id=int(state)).name
                        else:
                            cityName=''
                            stateName=''
                        
                        temp='subscription amount';subamnt=int(subamnt)
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
                        
                        if not datetime.datetime.strptime(dob,'%d-%m-%Y')<datetime.datetime.today():
                            errors.append('Invalid Date Of Birth !')
                                        
                        if subamnt:
                            temp='subscription amount';subamnt=int(subamnt)
                            if subamnt<=0:
                                errors.append("please enter valid subscription amount !")
                        
                        if recamnt:
                            temp='received amount';recamnt=int(recamnt)
                        
                        
                        if state and city and state!=-1 and city!=-1:
                            cityName=tbl_location.objects.get(id=int(city)).name
                            stateName=tbl_location.objects.get(id=int(state)).name
                        
                        if chequedate:
                            temp='Cheque DD date,format must be in (dd-mm-yyyy)'
                            datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                        if depositedate:
                            temp='Cheque/DD Deposite Date,format must be in (dd-mm-yyyy)'
                            datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                        if cleardate:
                            temp='Cheque/DD Clearance Date,format must be in (dd-mm-yyyy)'
                            datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                        
                        if dis:
                            temp='discount';dis=int(dis)
                        else:
                            dis=0
                        if comdis:
                            temp='commission discount';comdis=int(comdis)
                        else:
                            comdis=0
                    
                        if addis:
                            temp='additional discount';addis=int(addis)
                        else:
                            addis=0
                        '''____________________must be execute at last '''
                        #temp="employee Id";pre=ProjectScope().empCodePrefix()
                        #if empid:
                        #    if empid[:len(pre)]==pre:
                        #        int(empid[len(pre):])
                        #    else:
                        #        temp="employee Id"
                        #        raise ValueError
                    
                        '''______________________________________'''
                    except ValueError:
                        if temp:
                            errors.append("Invalid value found for field "+temp+" !")
                        temp=None
                
                if not errors:
                    
                    if not age:
                        age=None
                    if sex=='-1':
                        sex=None    
                    #if not empid:
                    #    empid=None
                    if not recamnt:
                        recamnt=0
                    
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
                  
                    if subSource!=-1:
                        subSource=tbl_source.objects.get(id=subSource)
                    #if empid:
                    #    empid=int(empid[len(pre):])
                    '''_________________________'''
                    
                    ''' for renewal purpose '''
                    r_OM=subscription.magazine.name
                    r_OP=subscription.period
                    r_OMRP=subscription.magazine.price
                    r_OSAmnt=subscription.subAmnt
                    r_ORAmnt=subscription.recAmnt
                    r_ODis=''
                    r_OCdis=''
                    r_OAdis=''
                    r_OScheme=''
                    r_OGift=''
                    r_OEmpid=''
                    r_NEmpid=''
                    for s in customer.scheme.all():
                        r_OScheme=r_OScheme+s.name+':'
                    for g in customer.gift.all():
                        r_OGift=r_OGift+g.name+':'
                    r_OSource=customer.subSource.categoryName
                    if customer.empId:
                        r_OEmpid=ProjectScope().getCustomerPrefix()+str(customer.empId)
                    
                    r_NEmpid=ProjectScope().getCustomerPrefix()+str(i_getEmployee(req.session.get('username','')).id)
                    r_OTSAmnt=customer.TSAmnt
                    r_OTRAmnt=customer.TRAmnt
                    
                    #return HttpResponse("done")
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
                    customer.empId=i_getEmployee(req.session.get('username','')).id
                    
                    nt=tbl_notify.objects.get(subId=subscription.id)
                    '''history magazine conversion part1'''
                    oldData=None
                    newData=None
                    if subscription.magazine.id!=submag:
                        oldData=subscription.magazine.name+':'+str(nt.startDate)+':'+str(nt.subEndDate)+":"+str(nt.subPeriod)
                    '''___________________'''
                    
                    subscription.magazine=tbl_magazine.objects.get(id=submag)    
                    
                    '''
                    delete old & create new notification
                    '''
                    nt.delete()
                    i_setNotificationFor(subscription.id,subscription.date,subperiod)
                
                    '''history magazine conversion part2'''
                    if oldData:
                        lnt=tbl_notify.objects.get(subId=subscription.id)
                        newData=subscription.magazine.name+':'+str(lnt.startDate)+':'+str(lnt.subEndDate)+":"+str(lnt.subPeriod)
                        tbl_history.objects.create(data=oldData+"::"+newData,custId=customer.id,subId=subscription.id,type='m')
                    '''_______________'''                    
                    
                    subscription.period=subperiod
                    
                    customer.TSAmnt=customer.TSAmnt-subscription.subAmnt
                    customer.TSAmnt=customer.TSAmnt+subamnt
                    
                    if not customer.TRAmnt:
                        customer.TRAmnt=0
                    
                    
                        
                    customer.TRAmnt=customer.TRAmnt-subscription.recAmnt
                    customer.TRAmnt=customer.TRAmnt+recamnt
                    
                    subscription.subAmnt=subamnt
                    subscription.recAmnt=recamnt
                    
                    '''scheme can be change or add '''
                    customer.scheme=[]
                    for ss in sschemes:
                        customer.scheme.add(ss)
                    
                    '''gifts will only add '''
                    customer.gift=[]
                    tbl_dispatch.objects.filter(customerId=customer.id).delete()
                    for sg in sgifts:
                        customer.gift.add(sg)
                        tbl_dispatch.objects.create(customerId=customer.id,subId=None,receiverContact=customer.mobileNo,dispatchAddress1=customer.address1,status='i',itemType='g',itemCode=sg,quantity=1)
                    #customer.dis+customer.comdis+customer.addis+
                    customer.transactions.add(tbl_transaction.objects.create(dis=dis,comdis=comdis,addis=addis,OSAmnt=customer.TSAmnt-(customer.TRAmnt+dis+comdis+addis),amount=recamnt,payMode=paymode,subId=subscription.id,chequeDate=chequedate,chequeNo=chequeno,bankName=bank,depositeDate=depositedate,clearDate=cleardate))
                    subscription.isActive=True
                    
                    subscription.save()
                    customer.save()
                    '''must be call after save() store renewal history'''
                    r_NScheme=''
                    r_NGift=''
                    for s in customer.scheme.all():
                        r_NScheme=r_NScheme+s.name+':'
                    for g in customer.gift.all():
                        r_NGift=r_NGift+g.name+':'
                    tbl_renewal.objects.create(
                                               type='r',custId=customer.id,subId=subscription.id,
                                               magazines=r_OM+':'+subscription.magazine.name,
                                               periods=str(r_OP)+':'+str(subscription.period),
                                               mrps=str(r_OMRP)+':'+str(subscription.magazine.price),
                                               subAmnts=str(r_OSAmnt)+':'+str(subscription.subAmnt),
                                               recAmnts=str(r_ORAmnt)+':'+str(subscription.recAmnt),
                                               dis=str(r_ODis)+':'+str(dis),
                                               comdis=str(r_OCdis)+':'+str(comdis),
                                               addis=str(r_OAdis)+':'+str(addis),
                                               scheme=r_OScheme+'-'+r_NScheme,
                                               gift=str(r_OGift)+'-'+str(r_NGift),
                                               subSource=r_OSource+':'+customer.subSource.categoryName,
                                               empid=r_OEmpid+':'+r_NEmpid,
                                               TSAmnt=str(r_OTSAmnt)+':'+str(customer.TSAmnt),
                                               TRAmnt=str(r_OTRAmnt)+':'+str(customer.TRAmnt)
                                               )
                        #return HttpResponse(str(teleo)+"/"+str(teler)+"/"+str(mobileno))
                    return HttpResponseRedirect("/subscription/edit/"+options[1])
                return render_to_response('renewSubscription.html',locals(),context_instance=RequestContext(req))
            return render_to_response('renewSubscription.html',locals(),context_instance=RequestContext(req))
            
    else:#outer else
        return HttpResponseRedirect("/")
    
    
    
    
    
def v_viewTransaction(req,tid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','v'):
        t=tbl_transaction.objects.get(id=tid)
        date=t.date
        amount=t.amount
        mode=t.getPaymentMode()
        if t.chequeDate:
            chequeDate=t.chequeDate
        if t.chequeNo:
            chequeNo=t.chequeNo
        if t.bankName:
            bankName=t.bankName
        if t.depositeDate:
            depositeDate=t.depositeDate
        if t.clearDate:
            clearDate=t.clearDate
        return render_to_response('viewTransaction.html',locals(),context_instance=RequestContext(req))

def v_addTransaction(req,sid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','a'):
        c=i_getCustomerHasSub(sid)
        cid=str(c.id)
        cid=ProjectScope().getCustomerPrefix()+cid
        TSAmnt=c.TSAmnt
        TRAmnt=c.TRAmnt
        if c.subscriptions.count()==1:
            subid=ProjectScope().getSubPrefix()+sid
        
        if req.method=="POST":
            errors=[]
            
            subid=req.POST.get('subid','').strip()
            recAmnt=req.POST.get('recAmnt','').strip()
            paymode=req.POST.get('paymode','').strip()
            chequedate=req.POST.get('chequedate','').strip()
            chequeno=req.POST.get('chequeno','').strip()
            bank=req.POST.get('bank','').strip()
            depositedate=req.POST.get('depositedate','').strip()
            cleardate=req.POST.get('cleardate','').strip()
            
            dis=req.POST.get('dis','').strip()
            comdis=req.POST.get('comdis','').strip()
            addis=req.POST.get('addis','').strip()
            
            if paymode=='-1':
                errors.append("please select one payment mode !")
            elif not recAmnt:
                errors.append("please enter received amount !")
            else:
                temp=None    
                try:
                    temp='received amount';recAmnt=int(recAmnt)
                    if subid:
                        pre=ProjectScope().getSubPrefix()
                        collectsubsID=''
                        for s in subid.split(','):
                            if s[:len(pre)]==pre:
                                if s and not i_getSubscription(int(s[len(pre):])):
                                    temp="subscripton Id,id does not exist"
                                    raise ValueError
                                collectsubsID=collectsubsID+s[len(pre):]+','
                            else:
                                temp="subscripton Id"
                                raise ValueError
                    
                    if chequedate:
                        temp='Cheque DD date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(chequedate,'%d-%m-%Y')
                    
                    if depositedate:
                        temp='Cheque/DD Deposite Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(depositedate,'%d-%m-%Y')
                    
                    if cleardate:
                        temp='Cheque/DD Clearance Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(cleardate,'%d-%m-%Y')
                    if dis:
                        temp='discount';dis=int(dis)
                    else:
                        dis=0
                    
                    if comdis:
                        temp='commission discount';comdis=int(comdis)
                    else:
                        comdis=0
                    
                    if addis:
                        temp='additional discount';addis=int(addis)
                    else:
                        addis=0
                        
                    if chequedate>depositedate or chequedate>cleardate or depositedate>cleardate:
                        errors.append("Invalid date found !")
                    else:
                        if not subid:
                            collectsubsID=None
                        
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
                    
                    '''______________________________________'''
                except ValueError:
                    if temp:
                        errors.append("Invalid  "+temp+" !")
                    temp=None
            if not errors:
                c.TRAmnt=c.TRAmnt+recAmnt
                #+c.dis+c.comdis+c.addis
                c.transactions.add(tbl_transaction.objects.create(OSAmnt=c.TSAmnt-(c.TRAmnt+dis+comdis+addis),dis=dis,comdis=comdis,addis=addis,bankName=bank,subId=collectsubsID,amount=recAmnt,payMode=paymode,chequeDate=chequedate,chequeNo=chequeno,depositeDate=depositedate,clearDate=cleardate))
                c.save()
                return HttpResponseRedirect("/subscription/edit/"+sid)
            return render_to_response('addTransaction.html',locals(),context_instance=RequestContext(req))
        return render_to_response('addTransaction.html',locals(),context_instance=RequestContext(req))



def v_MDispatch(req,pkid):
    
    if pkid and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','u'):
        try:
            magRow=tbl_dispatch.objects.get(id=pkid)
            couriers=tbl_supportedCourier.objects.all()
        except:
            pass
             
        magazine=magRow.getItemName()
        issuemonth=magRow.getIssueMonth()
        issueyear=magRow.getIssueYear()
        if magRow.courierType:
            courier=magRow.courierType.id
        if magRow.courierNo:
            courierno=magRow.courierNo
        if magRow.dispatchDate:
            dispatchdate=DateFormat(magRow.dispatchDate).format('d-m-Y')
        if magRow.receivedDate:
            receiveddate=DateFormat(magRow.receivedDate).format('d-m-Y')
        if magRow.receivedBy:
            receivedby=magRow.receivedBy
        if magRow.receiverContact:
            receivercontact=magRow.receiverContact
        if magRow.dispatchAddress1:
            dispatchaddress1=magRow.dispatchAddress1
        if magRow.dispatchAddress2:
            dispatchaddress2=magRow.dispatchAddress2
        if magRow.status:
            status=magRow.status
                
        '''after loaded end'''
        if req.method=="POST":
            errors=[]
            courier=int(req.POST.get('courier','').strip())
            courierno=req.POST.get('courierno','').strip()
            dispatchdate=req.POST.get('dispatchdate','').strip()
            receiveddate=req.POST.get('receiveddate','').strip()
            receivedby=req.POST.get('receivedby','').strip()
            receivercontact=req.POST.get('receivercontact','').strip()
            dispatchaddress1=req.POST.get('dispatchaddress1','').strip()
            dispatchaddress2=req.POST.get('dispatchaddress2','').strip()
            status=req.POST.get('status','').strip()
            if courierno and courier==-1:
                errors.append("please select at least one courier name !")
            elif not courierno and courier!=-1:
                errors.append("please enter a tracking no. !")
            elif courierno and not dispatchaddress1:
                errors.append("please enter a dispatch address 1 !")
            elif status=="-1":
                errors.append("please select at least one status !")
            elif status=="d" and not courierno:
                errors.append("Please enter tracking no. of dispatched item !")
            elif status=="d" and not dispatchdate :
                errors.append("Item cannot be dispatched without dispatched date !")
            elif status=="d" and not receiveddate :
                errors.append("Item cannot be dispatched without received date !")
            else:
                temp=None    
                try:
                    
                    if dispatchdate:
                        temp='dispatch Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(dispatchdate,'%d-%m-%Y')
                    
                    if receiveddate:
                        temp='received Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(receiveddate,'%d-%m-%Y')
                    
                    if (dispatchdate and receiveddate) and dispatchdate>receiveddate:
                        errors.append('In valid received date !')
                    
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                
                    
                if courier!=-1:
                    courier=tbl_supportedCourier.objects.get(id=courier)    
                else:
                    courier=None
                if not dispatchdate:
                    dispatchdate=None
                else:
                    dispatchdate=datetime.datetime.strptime(dispatchdate,'%d-%m-%Y')
                    
                if not receiveddate:
                    receiveddate=None
                else:
                    receiveddate=datetime.datetime.strptime(receiveddate,'%d-%m-%Y')
                    status='d'
                magRow.courierNo=courierno
                magRow.courierType=courier
                magRow.dispatchDate=dispatchdate
                magRow.receivedDate=receiveddate
                magRow.receivedBy=receivedby
                magRow.receiverContact=receivercontact
                magRow.dispatchAddress1=dispatchaddress1
                magRow.dispatchAddress2=dispatchaddress2
                magRow.status=status
                magRow.save()
                return HttpResponseRedirect('/subscription/list/')
        return render_to_response('dispatchMEdit.html',locals(),context_instance=RequestContext(req))
    return render_to_response('dispatchMEdit.html',locals(),context_instance=RequestContext(req))
    
def v_GDispatch(req,pkid):
    
    if pkid and i_hasPermission(i_getEmployee(req.session.get('username','')),'subscription','u'):
        try:
            magRow=tbl_dispatch.objects.get(id=pkid)
            couriers=tbl_supportedCourier.objects.all()
        except:
            pass
             
        gift=magRow.getItemName()
        #scheme=tbl_customer.objects.get(id=magRow.customerId).subscriptions.all()[0].scheme.name
        if magRow.courierType:
            courier=magRow.courierType.id
        if magRow.courierNo:
            courierno=magRow.courierNo
        if magRow.dispatchDate:
            dispatchdate=DateFormat(magRow.dispatchDate).format('d-m-Y')
        if magRow.receivedDate:
            receiveddate=DateFormat(magRow.receivedDate).format('d-m-Y')
        if magRow.receivedBy:
            receivedby=magRow.receivedBy
        if magRow.receiverContact:
            receivercontact=magRow.receiverContact
        if magRow.dispatchAddress1:
            dispatchaddress1=magRow.dispatchAddress1
        if magRow.dispatchAddress2:
            dispatchaddress2=magRow.dispatchAddress2
        if magRow.status:
            status=magRow.status
                
        '''after loaded end'''
        if req.method=="POST":
            errors=[]
            courier=int(req.POST.get('courier','').strip())
            courierno=req.POST.get('courierno','').strip()
            dispatchdate=req.POST.get('dispatchdate','').strip()
            receiveddate=req.POST.get('receiveddate','').strip()
            receivedby=req.POST.get('receivedby','').strip()
            receivercontact=req.POST.get('receivercontact','').strip()
            dispatchaddress1=req.POST.get('dispatchaddress1','').strip()
            dispatchaddress2=req.POST.get('dispatchaddress2','').strip()
            status=req.POST.get('status','').strip()
            if courierno and courier==-1:
                errors.append("please select at least one courier name !")
            elif not courierno and courier!=-1:
                errors.append("please enter a tracking no. !")
            elif courierno and not dispatchaddress1:
                errors.append("please enter a dispatch address 1 !")
            elif status=="-1":
                errors.append("please select at least one status !")
            elif status=="d" and not courierno:
                errors.append("Please enter tracking no. of dispatched item !")
            elif status=="d" and not dispatchdate :
                errors.append("Item cannot be dispatched without dispatched date !")
            elif status=="d" and not receiveddate :
                errors.append("Item cannot be dispatched without received date !")
            else:
                temp=None    
                try:
                    
                    if dispatchdate:
                        temp='dispatch Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(dispatchdate,'%d-%m-%Y')
                    
                    if receiveddate:
                        temp='received Date,format must be in (dd-mm-yyyy)'
                        datetime.datetime.strptime(receiveddate,'%d-%m-%Y')
                    
                    if (dispatchdate and receiveddate) and dispatchdate>receiveddate:
                        errors.append('In valid received date !')
                    
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                
                    
                if courier!=-1:
                    courier=tbl_supportedCourier.objects.get(id=courier)    
                else:
                    courier=None
                if not dispatchdate:
                    dispatchdate=None
                else:
                    dispatchdate=datetime.datetime.strptime(dispatchdate,'%d-%m-%Y')
                    
                if not receiveddate:
                    receiveddate=None
                else:
                    receiveddate=datetime.datetime.strptime(receiveddate,'%d-%m-%Y')
                    status='d'
                magRow.courierNo=courierno
                magRow.courierType=courier
                magRow.dispatchDate=dispatchdate
                magRow.receivedDate=receiveddate
                magRow.receivedBy=receivedby
                magRow.receiverContact=receivercontact
                magRow.dispatchAddress1=dispatchaddress1
                magRow.dispatchAddress2=dispatchaddress2
                magRow.status=status
                magRow.save()
                
                if tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=pkid).customerId).TSAmnt==0:
                    return HttpResponseRedirect('/compliment/')
                return HttpResponseRedirect('/subscription/list/')
        return render_to_response('dispatchGEdit.html',locals(),context_instance=RequestContext(req))
    return render_to_response('dispatchGEdit.html',locals(),context_instance=RequestContext(req))
