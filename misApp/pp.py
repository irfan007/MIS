from misApp.models import tbl_employee, tbl_role, tbl_departments, tbl_location,\
    tbl_magazine, tbl_permission, tbl_magazineCombo, ProjectScope, tbl_customer,\
    tbl_subscription, tbl_notify, tbl_tenure,\
    tbl_scheme, tbl_source, tbl_dispatch, tbl_complaint,\
    tbl_gift, tbl_supportedCourier, tbl_contentType
from django.db.models import Q
from django.core.mail import send_mail
from MIS.settings import EMAIL_HOST_USER, MEDIA_ROOT
from django.utils.dateformat import DateFormat
from datetime import datetime




def calcSuspendPeriod(suspendDate):
    suspendP=0
    import datetime
    suspendDate=suspendDate                            ;print "suspend day:%s"%(suspendDate)
    resumeDate=datetime.datetime.today()               ;print "resume day:%s"%(resumeDate)
    if suspendDate.year==resumeDate.year:
        if suspendDate.month==resumeDate.month:
            if suspendDate.day<21 and resumeDate.day>21:
                suspendP=1
    return suspendP+monthGapBetween(resumeDate,suspendDate)    
        
def monthGapBetween(d2,d1):
    import datetime
    return ((d2.year-d1.year)*12)+(d2.month-d1.month)

def hasLogedInEmployee(req):
    return i_getEmployee(req.session.get('username'))


def upload(fileObj,name):
    import os
    subDirectory=str(DateFormat(ProjectScope().getDate()).format('dmY'))
    try:
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name
    except IOError:
        os.mkdir(MEDIA_ROOT+subDirectory)
        with open(MEDIA_ROOT+subDirectory+'/'+str(name), 'w') as destination:
            for chunk in fileObj.chunks():
                destination.write(chunk)
        return subDirectory+'/'+name



def i_getEmployee(byUsername):
    try:
        return tbl_employee.objects.get(username=byUsername)
    except tbl_employee.DoesNotExist:
        return None

def i_getActiveAdminUser(byUsername):
    try:
        return tbl_employee.objects.get(isAdmin=True,isActive=True,username=byUsername)
    except tbl_employee.DoesNotExist:
        return None

def i_validateEmployee(usr,pwd):
    '''
    if employee is valid return employee object
    '''
    try:
        emp=tbl_employee.objects.get(username=usr,isActive=True)
        if emp.password==pwd:
            return emp
    except tbl_employee.DoesNotExist:
        return None   
    
def i_getAllEmployees():
    '''
    return all employee either active or not 
    '''
    try:
        return tbl_employee.objects.all()
    except tbl_employee.DoesNotExist:
        return None


def i_getAllEmployeesNA():
    '''
    return all employee either active or not but not admin 
    '''
    try:
        return tbl_employee.objects.filter(isAdmin=False).order_by('id')
    except tbl_employee.DoesNotExist:
        return None


def i_getEmployeeByEmail(email):
    try:
        return tbl_employee.objects.get(email=email)
    except tbl_employee.DoesNotExist:
        return None
    
    
def i_getActiveRoles():
    try:
        return tbl_role.objects.filter(isActive=True)
    except tbl_role.DoesNotExist:
        return None

def i_getActiveDepartments():
    try:
        return tbl_departments.objects.filter(isActive=True)
    except tbl_departments.DoesNotExist:
        return None

def i_getEmployeesCount():
    try:
        return tbl_employee.objects.all().count()
    except tbl_employee.DoesNotExist:
        return 0
    
def i_getAllCountries():
    try:
        return tbl_location.objects.filter(pid=0)
    except tbl_location.DoesNotExist:
        return 0
        
def i_getAllStates(byCountryId):
    try:
        return tbl_location.objects.filter(pid=byCountryId)
    except tbl_location.DoesNotExist:
        return 0
    
def i_getAllCities(byStateId):
    try:
        return tbl_location.objects.filter(pid=byStateId)
    except tbl_location.DoesNotExist:
        return 0

def i_getAllArea(byCityId):
    try:
        return tbl_location.objects.filter(pid=byCityId)
    except tbl_location.DoesNotExist:
        return 0


def i_getAllMagazines():
    try:
        return tbl_magazine.objects.all().order_by('createdOn')
    except tbl_magazine.DoesNotExist:
        return None
    
def i_getActiveMagazines():
    try:
        return tbl_magazine.objects.filter(isActive=True).order_by('createdOn')
    except tbl_magazine.DoesNotExist:
        return None
    
 

def i_getMagazine(byName):
    try:
        return tbl_magazine.objects.get(name=byName)
    except tbl_magazine.DoesNotExist:
        return None
    
def i_getMagazineByCode(code):
    try:
        return tbl_magazine.objects.get(code=code)
    except tbl_magazine.DoesNotExist:
        return None

def i_getAllRoles():
    try:
        return tbl_role.objects.all()
    except tbl_role.DoesNotExist:
        return None

def i_getRole(byName):
    try:
        return tbl_role.objects.get(name=byName)
    except tbl_role.DoesNotExist:
        return None

def i_getAllCombos():
    try:
        return tbl_magazineCombo.objects.all()
    except tbl_magazineCombo.DoesNotExist:
        return None

def i_getActiveCombos():
    try:
        return tbl_magazineCombo.objects.filter(isActive=True)
    except tbl_magazineCombo.DoesNotExist:
        return None
    
def i_getCombo(byName):
    try:
        return tbl_magazineCombo.objects.get(name=byName)
    except tbl_magazineCombo.DoesNotExist:
        return None

def i_getComboById(pkid):
    try:
        return tbl_magazineCombo.objects.get(id=pkid)
    except tbl_magazineCombo.DoesNotExist:
        return None
    
def i_getComboByCode(code):
    try:
        return tbl_magazineCombo.objects.get(code=code)
    except tbl_magazineCombo.DoesNotExist:
        return None

def i_hasPermission(forEmployee,forContent,ofType='v'):
    
    '''
    
    * if user not exist it will return false 
    * if content not exist it will return false
    * if ofType not exist it will return false
     
    ofType can be
    
    for view:ofType='v'
    for add:ofType='a'
    for update:ofType='u'
    for delete:ofType='d'
    
    default ofType is 'v'
    '''
    
    
    if not forEmployee:
        return False
    elif forEmployee.isAdmin:
        return True
    
    
    permissionQuerySet=forEmployee.role.permissions
    try:
        forContent=tbl_contentType.objects.get(name=forContent)
    except:
        forContent=None
        
        
    if ofType=='v':
        try:
            return permissionQuerySet.get(content=forContent).view
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='a':
        try:
            return permissionQuerySet.get(content=forContent).add
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='u':
        try:
            return permissionQuerySet.get(content=forContent).update
        except tbl_permission.DoesNotExist:
            return False
    elif ofType=='d':
        try:
            return permissionQuerySet.get(content=forContent).delete
        except tbl_permission.DoesNotExist:
            return False
    else:
        return False


def i_getActiveSubscription():
    try:
        return tbl_subscription.objects.filter(isActive=True)
    except:
        return None 

def i_getMagSubs():
    ''' subscription that are active and not suspended''' 
    try:
        return tbl_subscription.objects.filter(isActive=True,isSuspend=False)
    except:
        return None 

def i_getInactiveSubscription():
    try:
        return tbl_subscription.objects.filter(isActive=False)
    except:
        return None 

def i_getSubscriptionsEnd(forMagazine,onMonth):
    '''
    return all active subscription that comes to end on any month passed for any magazine
    '''
    try:
        
        mag=tbl_magazine.objects.get(name=forMagazine);#print mag
        subs=tbl_subscription.objects.filter(magazine=mag,isActive=True);#print subs
        return [s for s in subs if ((s.date.day<=20 and s.date.month+s.period==onMonth) or (s.date.day>20 and 1+s.date.month+s.period==onMonth))]
    except:
        return None 

def i_getCustomerHasSub(sub):
    '''
    return a customer has a subscription
    '''
    try:
        return tbl_customer.objects.get(subscriptions=sub)
    except:
        return None 

def i_getCustomer(byID):
    try:
        return tbl_customer.objects.get(id=byID)
    except:
        return None

def i_getSubscription(byID):
    try:
        return tbl_subscription.objects.get(id=byID)
    except:
        return None

def i_getDateAfterMonth(oldDate,addMonth):
    import datetime
    year, month= divmod(oldDate.month+addMonth, 12)
    if month == 0:
        month = 12
        year = year -1
    return datetime.datetime(oldDate.year + year, month, 1)
# => '2012-06-01'
def i_setIssues(subObj):
    '''
    will set 'issues,rIssues' field of tbl_subscription 
    '''
    issues=[]
    start=None
    end=None
    currentDate=subObj.date
    period=subObj.period
    if currentDate.day<=20:
        start=1
        end=period+1
    else:
        start=2
        end=period+2
    for x in range(start,end):
        nd=i_getDateAfterMonth(currentDate,x)
        issues.append("'"+str(nd.year)+','+str(nd.month)+"'"+':0')
    
    subObj.issues='{'+(','.join(issues))+'}'
    subObj.rIssues=period
    

def i_setMagazinesStatus(subs,forYear,forMonth):
    for s in subs:
        try:
            oldDict=eval(s.issues)
            if oldDict[str(forYear)+','+str(forMonth)]==0:
                oldDict[str(forYear)+','+str(forMonth)]=1#changed
                s.issues=str(oldDict)
                s.rIssues=s.rIssues-1
                s.save()
        except:
            pass
        
def i_setNotificationFor(subId,subDate,subPeriod):
    import datetime
    import calendar
    try:
        first=None
        second=None
        third=None
        fourth=None
        startDate=None
        if subDate.day<=20:
            #print "sub date :"+str(subDate)
            startDate=i_getDateAfterMonth(subDate,1)
            date=(subDate+datetime.timedelta(subPeriod*30))
            endDate=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            try:
                date=(subDate+datetime.timedelta((subPeriod-2)*30))
            except:
                pass
            
            try:
                first=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            except:
                pass
            
            try:
                date=(subDate+datetime.timedelta((subPeriod-1)*30))
            except:
                pass
            
            try:
                second=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            except:
                pass
            
            try:
                third=datetime.date(endDate.year,endDate.month,calendar.monthrange(endDate.year,endDate.month)[1]-15)
            except:
                pass
            
            try:
                fourth=datetime.date(endDate.year,endDate.month,calendar.monthrange(endDate.year,endDate.month)[1]-7)
            except:
                pass
            
            
            #print "sub End date :"+str(endDate)
            #print "1st date :"+str(first)
            #print "2nd date :"+str(second)
            #print "3 date :"+str(third)
            #print "4 date :"+str(fourth)
            tbl_notify.objects.create(startDate=startDate,subId=subId,subPeriod=subPeriod,subDate=subDate,subEndDate=endDate,firstDate=first,secondDate=second,thirdDate=third,fourthDate=fourth)
            
        else:
            #print "else sub date :"+str(subDate)
            startDate=i_getDateAfterMonth(subDate,2)
            subStartDate=(subDate+datetime.timedelta(1*30))
            date=(subStartDate+datetime.timedelta(subPeriod*30))
            endDate=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            
            try:
                date=(subStartDate+datetime.timedelta((subPeriod-2)*30))
            except:
                pass
            try:
                first=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            except:
                pass
            try:
                date=(subStartDate+datetime.timedelta((subPeriod-1)*30))
            except:
                pass
            try:
                second=datetime.date(date.year,date.month,calendar.monthrange(date.year,date.month)[1])
            except:
                pass
            try:
                third=datetime.date(endDate.year,endDate.month,calendar.monthrange(endDate.year,endDate.month)[1]-15)
            except:
                pass
            try:
                fourth=datetime.date(endDate.year,endDate.month,calendar.monthrange(endDate.year,endDate.month)[1]-7)
            except:
                pass
            
            #print "sub End date :"+str(endDate)
            #print "1st date :"+str(first)
            #print "2nd date :"+str(second)
            #print "3 date :"+str(third)
            #print "4 date :"+str(fourth)
            tbl_notify.objects.create(startDate=startDate,subId=subId,subPeriod=subPeriod,subDate=subDate,subEndDate=endDate,firstDate=first,secondDate=second,thirdDate=third,fourthDate=fourth)
    except Exception,e:
        print e
    
    

def i_notifier():
    import datetime
    today=datetime.date.today()
    prefix=ProjectScope().getSubPrefix()
    try:
        rows=[[tbl_customer.objects.get(subscriptions=n.subId),tbl_subscription.objects.get(id=n.subId),n.subEndDate] for n in tbl_notify.objects.filter(Q(firstDate=today)|Q(secondDate=today)|Q(thirdDate=today)|Q(fourthDate=today)) if not tbl_subscription.objects.get(id=n.subId).isSuspend ]
        for row in rows:
            try:
                if row[1].isActive:
                    msg="\nDear Customer,\n\nYour subscription for Magazine '"+row[1].magazine.name+"' with subscription code "+prefix+str(row[1].id)+",\nwill expire on "+DateFormat(row[2]).format('d M Y')+" ,to continue your subscritpion \nplease renew it before the end Date.\n\n\nThanks,\nTransasia Team"
                    send_mail('Transasia Subscription Alert',msg,EMAIL_HOST_USER,[row[0].email])
            except:
                pass
            #print msg
    except Exception,e:
        print e



def i_getActiveTenures():
    try:
        return tbl_tenure.objects.filter(isActive=True).order_by('timePeriod')
    except:
        return None
    

def i_getSchemeByMagazineId(pkid):
    try:
        return tbl_scheme.objects.filter(magazine=tbl_magazine.objects.get(id=pkid),isActive=True)
    except:
        return None

def i_getSchemeByComboId(pkid):
    try:
        return tbl_scheme.objects.filter(magazineCombo=tbl_magazineCombo.objects.get(id=pkid),isActive=True)
    except:
        return None

#print i_getSchemeByMagazineId(1)
def i_getGiftInScheme(bySchemeId):
    try:
        scheme=tbl_scheme.objects.get(id=bySchemeId)
        if scheme.gifts:
            return scheme.gifts
        else:
            return None
    except:
        return None
    

def i_getActiveSources(byPid):
    try:
        return tbl_source.objects.filter(pid=byPid,isActive=True)
    except:
        return None






#print [[(r[1]+12,r[0]+d.year] for r in (divmod(d.month+m, 12) for m in range(1,25))]


def i_getLocName(byId):
    try:
        return tbl_location.objects.get(id=byId).name
    except:
        return None


def i_getLocId(byName):
    try:
        return tbl_location.objects.get(name=byName).id
    except:
        return None

def i_getScheme(byName):
    try:
        return tbl_scheme.objects.get(name=byName)
    except:
        return None

def i_getSource(byName):
    try:
        return tbl_source.objects.get(categoryName=byName)
    except:
        return None

def i_getAllSubSources(byPid):
    try:
        return tbl_source.objects.filter(pid=byPid)
    except:
        return None


def i_getRowsOFDispatch(ofCustomerId,itemType='m'):
    try:
        return tbl_dispatch.objects.filter(customerId=ofCustomerId,itemType=itemType)
    except:
        return None
    
def i_getAllComplaintsOf(subcriptionId):
    try:
        return tbl_complaint.objects.filter(subId=subcriptionId)
    except:
        return None

def i_get2Dtuple(tuple,ofLen):
    flag=0
    loopcounter=len(tuple)
    temp=[]
    tOFt=[]
    for t in tuple:
        temp.append(t)
        flag=flag+1
        if flag==ofLen:
            tOFt.append(temp)
            temp=[]
            flag=0
        loopcounter=loopcounter-1
        if loopcounter==0 and temp:
            tOFt.append(temp)
    return tOFt

def i_manageMagLabel(sub):
    customer=i_getCustomerHasSub(sub)
    import textwrap
    subscription=sub
    pre=ProjectScope().getSubPrefix()
    line1=subscription.magazine.name+" / "+pre+str(subscription.id)
    line2="SUBSCRIPTION END ( "+DateFormat(tbl_notify.objects.get(subId=subscription.id).subEndDate).format('M Y')+" )"
    line3=customer.getTitle()+" "+customer.firstName+" "+customer.lastName
    line4=""
    line5=""
    line6=""
    line7=""
    line8=""
    line9=''
    
    if customer.designation:
        line4=line4+customer.designation
    if customer.company:
        line4=line4+" / "+customer.company
    
    address=customer.address1+" "+customer.address2+" "+customer.address3
    address=textwrap.fill(textwrap.dedent(address).strip(),width=40)
    splitAdd=address.split("\n")
    try:
        line5=splitAdd[0]
        line6=splitAdd[1]
        line7=splitAdd[2]
        line8=splitAdd[3]
    except:
        pass
    
    
    if customer.city:
        line9=line9+customer.city
    if customer.pincode:
        line9=line9+"/"+customer.pincode
    line10=customer.mobileNo
    
    
    return [line1,line2,line3.title(),line4.upper(),line5.upper(),line6.upper(),line7.upper(),line8.upper(),line9.upper(),line10.upper()]


def i_manageGiftLabel(item):
    dispatchRow=tbl_dispatch.objects.get(id=item[0])
    customer=tbl_customer.objects.get(id=dispatchRow.customerId)
    subscription=customer.subscriptions.all()[0]#always first subscription will be shown in gift label
    courier=tbl_supportedCourier.objects.get(id=item[1])
    gift=tbl_gift.objects.get(id=dispatchRow.itemCode)
    
    import textwrap
    pre=ProjectScope().getSubPrefix()
    line1=gift.name.upper()+"( "+gift.code.upper()+" ) / "+courier.name.upper()
    line2=subscription.magazine.name.upper()+" / "+pre+str(subscription.id)
    line3=customer.getTitle()+" "+customer.firstName+" "+customer.lastName
    line4=""
    line5=""
    line6=""
    line7=""
    line8=""
    line9=''
    
    if customer.designation:
        line4=line4+customer.designation
    if customer.company:
        line4=line4+" / "+customer.company
    
    address=customer.address1+" "+customer.address2+" "+customer.address3
    address=textwrap.fill(textwrap.dedent(address).strip(),width=40)
    splitAdd=address.split("\n")
    try:
        line5=splitAdd[0]
        line6=splitAdd[1]
        line7=splitAdd[2]
        line8=splitAdd[3]
    except:
        pass
    
    
    if customer.city:
        line9=line9+customer.city
    if customer.pincode:
        line9=line9+" / "+customer.pincode
    line10=customer.mobileNo
    
    
    return [line1,line2,line3.title(),line4.upper(),line5.upper(),line6.upper(),line7.upper(),line8.upper(),line9.upper(),line10.upper()]


def i_createMagLabel(c,pagesize,subs2D):
    
    width,height=pagesize
    '''origin(0,0) will be on bottom left corner of page'''
    x=25
    y=height-25
    
    labelWidth=width/2-35
    labelheight=height/4-25
    labelVGap=45
    labelHGap=8
    
    
    
    
    flag=0
    for row in subs2D:
        print "current row:%s,flag=%s"%(row,flag)
        if flag==4:
            flag=0
            c.showPage()#cause page to change
            '''initializing after page change'''
            x=25
            y=height-25
            
            labelWidth=width/2-35
            labelheight=height/4-25
            labelVGap=45
            labelHGap=8
        for label in row:
            c.rect(x, y,labelWidth,-labelheight)
            textobject = c.beginText()
            textobject.setTextOrigin(x+5,y-20)
            for count,line in enumerate(i_manageMagLabel(label)):
                if count==0:
                    textobject.setFont("Helvetica-Bold", 14)
                elif count==1:
                    textobject.setFont("Helvetica", 11)
                elif count==2:
                    textobject.setFont("Helvetica", 14)
                elif count==3:
                    textobject.setFont("Helvetica", 10,leading=25)
                elif count==7:
                    textobject.setFont("Helvetica", 10,leading=25)
                else:
                    textobject.setFont("Helvetica",10)
                textobject.textLine(line)
            x=labelWidth+labelVGap
            c.drawText(textobject)
        flag=flag+1
        x=25
        y=y-210+labelHGap


def i_createGiftLabel(c,pagesize,row2D):
    
    width,height=pagesize
    '''origin(0,0) will be on bottom left corner of page'''
    x=25
    y=height-25
    
    labelWidth=width/2-35
    labelheight=height/4-25
    labelVGap=45
    labelHGap=8
    
    flag=0
    for row in row2D:
        if flag==4:
            c.showPage()
            '''initializing after page change'''
            x=25
            y=height-25
            
            labelWidth=width/2-35
            labelheight=height/4-25
            labelVGap=45
            labelHGap=8
        for label in row:
            c.rect(x, y,labelWidth,-labelheight)
            textobject = c.beginText()
            textobject.setTextOrigin(x+5,y-20)
            for count,line in enumerate(i_manageGiftLabel(label)):
                if count==0:
                    textobject.setFont("Helvetica-Bold", 14)
                elif count==1:
                    textobject.setFont("Helvetica", 11)
                elif count==2:
                    textobject.setFont("Helvetica", 14)
                elif count==3:
                    textobject.setFont("Helvetica", 10,leading=25)
                elif count==7:
                    textobject.setFont("Helvetica", 10,leading=25)
                else:
                    textobject.setFont("Helvetica",10)
                textobject.textLine(line)
            x=labelWidth+labelVGap
            c.drawText(textobject)
        flag=flag+1
        x=25
        y=y-210+labelHGap


def i_getActiveGifts():
    try:
        return tbl_gift.objects.filter(isActive=True,updated__gte=1)
    except:
        return None
    
def i_getActiveSchemes():
    try:
        return tbl_scheme.objects.filter(isActive=True)
    except:
        return None

