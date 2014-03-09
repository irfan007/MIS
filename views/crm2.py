from misApp.pp import i_hasPermission, i_getEmployee, i_getLocId
from misApp.models import tbl_ticket, tbl_subscription, ProjectScope,\
tbl_customer, tbl_ticketType, tbl_employee, tbl_followUp, tbl_departments,\
tbl_transfer,tbl_transfer,tbl_location, tbl_contact, tbl_notify, tbl_events

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.mail import send_mail
from MIS.settings import EMAIL_HOST_USER
from django.utils.dateformat import DateFormat
from django.core.paginator import Paginator, PageNotAnInteger

def v_eventCalander(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        eventsData="["
        import datetime
        events=tbl_events.objects.filter(username=req.session.get('username',''))
        i=0
        for e in events:
            eventsData=eventsData+"['"+e.event+"','"+str(e.startDate)+"','"+str(e.endDate)+"','"+e.fgColor+"','"+e.bgColor+"','"+str(e.createdOn)+"']"
            try:
                events[i+1]
                eventsData=eventsData+","
            except IndexError:
                pass
            i=i+1
        eventsData=eventsData+"]"
        return render_to_response("calendar.html",locals(),context_instance=RequestContext(req))
    
#-----------------------------------------------------------------------------------
def v_crmHome(req):
    '''
    NOTE : My tickets will first search all tickets has last follower as current user if not found then
        it will return all tickets created by him   
    '''
    itemOnPage=10
    tickets=[]
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        
        
        errors=[]
        cuWarnings=[]
        ps=ProjectScope()
        
        search_ticket=req.POST.get('search_ticket','')
        search_subscription=req.POST.get('search_subscription','')
        search_status=req.POST.get('search_status','')
        page = req.GET.get('page','1')
        
        allTickets=tbl_ticket.objects.all().order_by('-updatedOn')
        
        if not search_status:
            
            search_status = req.GET.get('search_status','n')
            if search_status=='-1':#means my tickets
                tickets=allTickets.filter(currentFollower=i_getEmployee(req.session.get('username','')).id).order_by('-updatedOn')
        
        
        
        
        
        
        
        if req.POST.get('my_tickets'):
            search_status=req.POST.get('search_status','-1')
            page=1
            emp=i_getEmployee(req.session.get('username',''))
            tickets=allTickets.filter(currentFollower=emp.id).order_by('-updatedOn')
            if not tickets:
                tickets=allTickets.filter(createdBy=emp.id).order_by('-updatedOn')
            
        
        elif req.POST.get('crm_search',''):
            page=1
            if not tickets and search_ticket:
                if search_ticket[:len(ps.TICKET_PREFIX)].lower()!=ps.TICKET_PREFIX.lower():
                    errors.append('Invalid ticket No. !')
                else:
                    if search_ticket[len(ps.TICKET_PREFIX):]:
                        try:
                            tickets=allTickets.filter(id=search_ticket[len(ps.TICKET_PREFIX):])
                        except ValueError:
                            pass
                        
                            
            elif not tickets and search_subscription:
                if search_subscription[:len(ps.getSubPrefix())].lower()!=ps.getSubPrefix().lower():
                    errors.append('Invalid Subscription No. !')
                else:
                    if search_subscription[len(ps.getSubPrefix()):]:
                        #return HttpResponse(search_subscription[len(ps.getSubPrefix()):])
                        try:
                            tickets=allTickets.filter(subId=search_subscription[len(ps.getSubPrefix()):])
                        except ValueError:
                            pass
        
        
        
        
#                
        if not tickets:
            tickets=allTickets.filter(status=search_status)
            
            
            
        if not search_subscription and not search_ticket:
            '''
            ensure that paginator will work only without search_subscription and search_ticket 
            '''
            myPaginator=Paginator(tickets,itemOnPage)
            try:
                tickets=myPaginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                tickets=myPaginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                tickets=myPaginator.page(myPaginator.num_pages)
        
        return render_to_response("crmHome.html",locals(),context_instance=RequestContext(req))



def v_newTicketStep1(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','a'):
        ps=ProjectScope()
        cuWarnings=['Please search a subscription first and then create a new ticket for it !']
        
        
        if req.POST.get('crm_search',''):
            cuWarnings=[]
            errors=[]
            
            search_subscription=req.POST.get('search_subscription','').strip()
            search_subscriber=req.POST.get('search_subscriber','').strip()
            search_mobile=req.POST.get('search_mobile','').strip()
            search_email=req.POST.get('search_email','').strip()
            
            if search_subscription and search_subscription[:len(ps.getSubPrefix())].lower()!=ps.getSubPrefix().lower():
                errors.append('Invalid Subscription No. !')
            else:
                search_subscription=search_subscription[len(ps.getSubPrefix()):]
            
            
            if not errors:
                foundSub=[]
                if search_subscription:
                    foundSub=tbl_subscription.objects.filter(id=search_subscription)
                
                if foundSub:
                    rows=[(foundSub[0],tbl_customer.objects.filter(subscriptions=search_subscription)[0])]
                else:
                    customers=[]
                    if search_subscriber:
                        customers=tbl_customer.objects.filter(firstName__icontains=search_subscriber)
                    if not customers and search_mobile:
                        customers=tbl_customer.objects.filter(mobileNo=search_mobile)
                    if not customers and search_email:
                        customers=tbl_customer.objects.filter(email=search_email)
                    
                    if not customers:
                        cuWarnings.append('Not Found !')    
                    
                    subs=[]
                    for c in customers:
                        for s in c.subscriptions.all():
                            subs.append(s)
                    
                    rows=[(s,tbl_customer.objects.get(subscriptions=s.id)) for s in subs ]
#                
                #return HttpResponse(rows)
                if search_subscription:
                    search_subscription=ps.getSubPrefix()+search_subscription      
        return render_to_response("newTicket1.html",locals(),context_instance=RequestContext(req))
    


def v_newTicketStep2(req,sub_id):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','a'):
        cuWarnings=[]
        ps=ProjectScope()
        s=tbl_subscription.objects.get(id=sub_id)
        c=tbl_customer.objects.get(subscriptions=s)
        types=tbl_ticketType.objects.all()
        
        
        
        
        if not c.email:
            cuWarnings.append('customer has no email id, email communication disabled !')
        
        if req.POST.get('crm_create'):
            cuWarnings=[]
            errors=[]
            complaint=req.POST.get('complaint','').strip()
            reply=req.POST.get('reply','').strip()
            
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            #return HttpResponse(complaint_domain+":"+complaint_resource+":"+status)
            if not complaint:
                errors.append('Please enter complain matter !')
            elif len(complaint)<5:
                errors.append('Complain matter seems invalid !')
            if not errors:
                #followUps=models.ManyToManyField(tbl_followUp,null=True,blank=True)
                empObj=tbl_employee.objects.get(username=req.session.get('username'))
                tick=tbl_ticket.objects.create(subId=int(sub_id),createdBy=empObj.id,complaint=complaint,type=tbl_ticketType.objects.get(id=complaint_domain),resource=complaint_resource,status=status,currentDepartment=empObj.department)
                if reply:
                    tick.currentFollower=empObj.id
                    tick.save()
                    tick.followUps.add(tbl_followUp.objects.create(by=empObj.id,reply=reply,subId=int(sub_id)))
                
                return HttpResponseRedirect('/CRM/')
            #return render_to_response("newTicket2.html",locals(),context_instance=RequestContext(req))
        elif req.POST.get('crm_create_and_mail'):
            cuWarnings=[]
            errors=[]
            complaint=req.POST.get('complaint','').strip()
            reply=req.POST.get('reply','').strip()
            
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            #return HttpResponse(complaint_domain+":"+complaint_resource+":"+status)
            if not complaint:
                errors.append('Please enter complain matter !')
            elif len(complaint)<5:
                errors.append('Complain matter seems invalid !')
            elif not reply:
                errors.append('Please enter reply message in box !')
            if not errors:
                #followUps=models.ManyToManyField(tbl_followUp,null=True,blank=True)
                empObj=tbl_employee.objects.get(username=req.session.get('username'))
                tick=tbl_ticket.objects.create(subId=int(sub_id),createdBy=empObj.id,complaint=complaint,type=tbl_ticketType.objects.get(id=complaint_domain),resource=complaint_resource,status=status,currentDepartment=empObj.department)
                tick.currentFollower=empObj.id
                tick.save()
                tick.followUps.add(tbl_followUp.objects.create(by=empObj.id,reply=reply,subId=int(sub_id)))
                send_mail('Transasia Team',reply,EMAIL_HOST_USER,[c.email])
                return HttpResponseRedirect('/CRM/')
            #return HttpResponse('in create and mail')
        elif req.POST.get('crm_transfer'):
            return HttpResponse('in transfer')
            
    return render_to_response("newTicket2.html",locals(),context_instance=RequestContext(req))


def v_editTicket(req,ticket_no):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','u'):
        ps=ProjectScope()
        types=tbl_ticketType.objects.all()
        
        ticket=tbl_ticket.objects.get(id=ticket_no)
        s=tbl_subscription.objects.get(id=ticket.subId)
        c=tbl_customer.objects.get(subscriptions=s)
        
        complaint_domain=ticket.type.id
        complaint_resource=ticket.resource
        status=ticket.status
        
        if req.POST.get('crm_save'):
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            reply=req.POST.get('reply')
            
            ticket.type=tbl_ticketType.objects.get(id=complaint_domain)
            ticket.resource=complaint_resource
            ticket.status=status
            
            if reply:
                empObj=tbl_employee.objects.get(username=req.session.get('username'))
                ticket.currentFollower=empObj.id
                ticket.followUps.add(tbl_followUp.objects.create(by=empObj.id,reply=reply,subId=ticket.subId))
            
            ticket.save()        
            return HttpResponseRedirect('/CRM/')
        elif req.POST.get('crm_save_and_mail'):
            errors=[]
            
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            reply=req.POST.get('reply')
            
            ticket.type=tbl_ticketType.objects.get(id=complaint_domain)
            ticket.resource=complaint_resource
            ticket.status=status
            
            if not reply:
                errors.append('Please enter reply message in box !')
            if not errors:
                empObj=tbl_employee.objects.get(username=req.session.get('username'))
                ticket.followUps.add(tbl_followUp.objects.create(by=empObj.id,reply=reply,subId=ticket.subId))
                ticket.currentFollower=empObj.id
                send_mail('Transasia Team',reply,EMAIL_HOST_USER,[c.email])
                
                ticket.save()
                return HttpResponseRedirect('/CRM/')
        elif req.POST.get('crm_transfer'):
            return HttpResponseRedirect('/CRM/transfer/'+str(ticket.id))
                
        return render_to_response("editTicket.html",locals(),context_instance=RequestContext(req))




def v_transferTicket(req,ticket_no):
    
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','u'):
        ps=ProjectScope()
        errors=[]
        
        types=tbl_ticketType.objects.all()
        departments=tbl_departments.objects.filter(isActive=True)
        
        ticket=tbl_ticket.objects.get(id=ticket_no)
        s=tbl_subscription.objects.get(id=ticket.subId)
        c=tbl_customer.objects.get(subscriptions=s)
        
        complaint_domain=ticket.type.id
        complaint_resource=ticket.resource
        status=ticket.status
        
        
        byEmpObj=tbl_employee.objects.get(username=req.session.get('username'))
        if ticket.currentFollower:
            if not byEmpObj.isAdmin and byEmpObj.id!=ticket.currentFollower:
                errors.append('Only a current follower can transfer this ticket !')
        
        if req.POST.get('crm_transfer'):
            
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            reply=req.POST.get('reply').strip()
            to_department=int(req.POST.get('to_department'))
            to_employee=int(req.POST.get('to_employee',-1))
            try:
                employees=tbl_employee.objects.filter(department=to_department)
            except tbl_employee.DoesNotExist:
                pass
            
            if to_department==-1:
                errors.append('please select department !')
            else:
                if to_employee!=-1:
                    if ticket.currentFollower==to_employee:
                        errors.append('please choose a different employee to transfer !')
                else:
                    if ticket.currentDepartment:
                        if ticket.currentDepartment.id==to_department:
                            errors.append('please choose a different department !')
                    
                    
                    
                    
                
                
            if not errors:
                ticket.type=tbl_ticketType.objects.get(id=complaint_domain)
                ticket.resource=complaint_resource
                ticket.status=status
                
                
                if reply:
                    ticket.followUps.add(tbl_followUp.objects.create(by=byEmpObj.id,reply=reply,subId=ticket.subId))
                
                if to_employee!=-1:
                    toEmp=tbl_employee.objects.get(id=to_employee)
                    ticket.currentFollower=toEmp.id
                else:
                    ticket.currentFollower=None
                
                
                to_department=tbl_departments.objects.get(id=to_department)
                ticket.currentDepartment=to_department
                
                
                ticket.transferRecord.add(tbl_transfer.objects.create(by=byEmpObj.id,to=to_employee,department=to_department))
                ticket.save()
                
                return HttpResponseRedirect('/CRM/')
            
        elif req.POST.get('crm_transfer_and_mail'):
            
            complaint_domain=int(req.POST.get('complaint_domain'))
            complaint_resource=req.POST.get('complaint_resource')
            status=req.POST.get('status')
            reply=req.POST.get('reply').strip()
            to_department=int(req.POST.get('to_department'))
            to_employee=int(req.POST.get('to_employee',-1))
            
            
            try:
                employees=tbl_employee.objects.filter(department=to_department)
            except tbl_employee.DoesNotExist:
                pass    
            
            
            if not reply:
                errors.append('please enter reply message !')
            elif to_department==-1:
                errors.append('please select department !')
            else:
                if to_employee!=-1:
                    if ticket.currentFollower==to_employee:
                        errors.append('please choose a different employee to transfer !')
                else:
                    if ticket.currentDepartment:
                        if ticket.currentDepartment.id==to_department:
                            errors.append('please choose a different department !')
                
                
            if not errors:
                ticket.type=tbl_ticketType.objects.get(id=complaint_domain)
                ticket.resource=complaint_resource
                ticket.status=status
                
                
                ticket.followUps.add(tbl_followUp.objects.create(by=byEmpObj.id,reply=reply,subId=ticket.subId))
                
                if to_employee!=-1:
                    toEmp=tbl_employee.objects.get(id=to_employee)
                    ticket.currentFollower=toEmp.id
                else:
                    ticket.currentFollower=None
                
                
                to_department=tbl_departments.objects.get(id=to_department)
                ticket.currentDepartment=to_department
                
                ticket.transferRecord.add(tbl_transfer.objects.create(by=byEmpObj.id,to=to_employee,department=to_department))
                ticket.save()
                
                send_mail('Transasia Team',reply,EMAIL_HOST_USER,[c.email])
                return HttpResponseRedirect('/CRM/')
                
            
        return render_to_response("transferTicket.html",locals(),context_instance=RequestContext(req))







#def v_crmSubscription(req):
#    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
#        ps=ProjectScope()
#        months=[(1,'JAN'),(2,'FEB'),(3,'MAR'),(4,'APRIL'),(5,'MAY'),(6,'JUNE'),(7,'JULY'),(8,'AUG'),(9,'SEP'),(10,'OCT'),(11,'NOV'),(12,'DEC')]
#        search_ticket=req.POST.get('search_ticket','')
#        search_subscription=req.POST.get('search_subscription','')
#        search_status=req.POST.get('search_status','n')
#        
#        errors=[]
#        cuWarnings=[]
#        
#        
#        
#        
#        
#        if req.POST.get('crm_search',''):
#            
#            if search_ticket:
#                if search_ticket[:len(ps.TICKET_PREFIX)].lower()!=ps.TICKET_PREFIX.lower():
#                    errors.append('Invalid ticket No. !')
#                else:
#                    if search_ticket[len(ps.TICKET_PREFIX):]:
#                        try:
#                            tickets=allTickets.filter(id=search_ticket[len(ps.TICKET_PREFIX):])
#                        except ValueError:
#                            pass
#                        
#                            
#            elif not tickets and search_subscription:
#                if search_subscription[:len(ps.getSubPrefix())].lower()!=ps.getSubPrefix().lower():
#                    errors.append('Invalid Subscription No. !')
#                else:
#                    if search_subscription[len(ps.getSubPrefix()):]:
#                        #return HttpResponse(search_subscription[len(ps.getSubPrefix()):])
#                        try:
#                            tickets=allTickets.filter(subId=search_subscription[len(ps.getSubPrefix()):])
#                        except ValueError:
#                            pass
#                
#            else:
#                tickets=allTickets.filter(status=search_status)
#                
#            return render_to_response("crmSubscriptionHome.html",locals(),context_instance=RequestContext(req))
#        
#        
#        
#        tickets=allTickets.filter(status=search_status)
#        
#        return render_to_response("crmSubscriptionHome.html",locals(),context_instance=RequestContext(req))
#   
#        
#        




#-----------------------------------------------------------------------sales-----------------------------------------




def v_crmSales(req):
    itemOnPage=10
    contacts=[]
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        ps=ProjectScope()
        errors=[]
        cuWarnings=[]
        
        followup_id=req.POST.get('followup_id','')
        subscription_no=req.POST.get('subscription_no','')
        search_status=req.POST.get('search_status','')
        page = req.GET.get('page','1')
        
        fetchedContacts=tbl_contact.objects.all().order_by('-updatedOn')
        
        if not search_status:
            search_status = req.GET.get('search_status','n')
            if search_status=='o':#means my contacts
                contacts=fetchedContacts.filter(createdBy=i_getEmployee(req.session.get('username','')).id).order_by('-updatedOn')
        
        
        if req.POST.get('my_followup'):
            page=1
            search_status=req.POST.get('search_status','o')
            contacts=tbl_contact.objects.filter(createdBy=i_getEmployee(req.session.get('username','')).id).order_by('-updatedOn')
            #return render_to_response("salesHome.html",locals(),context_instance=RequestContext(req))
    
        if req.POST.get('crm_search',''):
            page=1
            if not contacts and followup_id:
                if followup_id[:len(ps.FOLLOWUP_PREFIX)].lower()!=ps.FOLLOWUP_PREFIX.lower():
                    errors.append('Invalid follow up id !')
                else:
                    if followup_id[len(ps.FOLLOWUP_PREFIX):]:
                        try:
                            contacts=fetchedContacts.filter(id=followup_id[len(ps.FOLLOWUP_PREFIX):])
                        except ValueError:
                            pass
                        
                            
            elif not contacts and subscription_no:
                if subscription_no[:len(ps.getSubPrefix())].lower()!=ps.getSubPrefix().lower():
                    errors.append('Invalid Subscription No. !')
                else:
                    if subscription_no[len(ps.getSubPrefix()):]:
                        #return HttpResponse(search_subscription[len(ps.getSubPrefix()):])
                        try:
                            contacts=fetchedContacts.filter(subId=subscription_no[len(ps.getSubPrefix()):])
                        except ValueError:
                            pass
                
            
                
            
        if not contacts:
            contacts=fetchedContacts.filter(status=search_status)
        
        if not followup_id and not subscription_no:
            '''
            ensure that paginator will work only without search_subscription and search_ticket 
            '''
            myPaginator=Paginator(contacts,itemOnPage)
            try:
                contacts=myPaginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                contacts=myPaginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                contacts=myPaginator.page(myPaginator.num_pages)
        
        return render_to_response("salesHome.html",locals(),context_instance=RequestContext(req))



    


def v_followUpAsNew(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        import datetime
        countries=tbl_location.objects.filter(pid=0)
        if req.POST.get('crm_create',''):
            errors=[]
            
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
            
            cityName=None
            stateName=None
            if country!=-1:
                states=tbl_location.objects.filter(pid=country)
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not firstname:
                errors.append("please enter first Name !")
            elif not lastname:
                errors.append("please enter last Name !")
            elif state==-1:
                errors.append("please select one state !")
            elif city==-1:
                errors.append("please select one city !")
            elif mobileno and len(mobileno)<10:
                    errors.append("please enter valid Mobile no. !")
            elif email and '@' not in email and '.' not in email:
                errors.append("please enter valid email Id !")
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
                
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                if not dob:
                    dob=None
                else:
                    dob=datetime.datetime.strptime(dob,'%d-%m-%Y')
                
                if not age:
                    age=None
                
                tbl_contact.objects.create(createdBy=i_getEmployee(req.session.get('username','')).id,
                                           status='n',
                                           title=title,
                                           firstName=firstname,
                                           lastName=lastname,
                                           dob=dob,
                                           age=age,
                                           sex=sex,
                                           designation=designation,
                                           company=company,
                                           address1=address1,
                                           address2=address2,
                                           address3=address3,
                                           state=stateName,
                                           city=cityName,
                                           pincode=pincode,
                                           tel_O=teleo,
                                           tel_R=teler,
                                           mobileNo=mobileno,
                                           email=email
                                           )
                
                return HttpResponseRedirect('/sales/')
        return render_to_response("followup_as_new.html",locals(),context_instance=RequestContext(req))
  


  


def v_contact(req,contact_id):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','u'):
        
        contact=tbl_contact.objects.get(id=contact_id)
        countries=tbl_location.objects.filter(pid=0)
        
        title=contact.title
        firstname=contact.firstName
        lastname=contact.lastName
        address1=contact.address1
        email=contact.email
        status=contact.status
        ps=ProjectScope()
        
        if contact.sex:
            sex=contact.sex
        if contact.age:
            age=contact.age
        if contact.dob:
            dob=DateFormat(contact.dob).format('d-m-Y')
        if contact.designation:
            designation=contact.designation
        if contact.company:
            company=contact.company
        if contact.address2:
            address2=contact.address2
        if contact.address3:
            address3=contact.address3
        if contact.city:
            cityName=contact.city
            city=i_getLocId(cityName)
            
        if contact.state:
            stateName=contact.state
            state=i_getLocId(stateName)
            cities=tbl_location.objects.filter(pid=state)
            
            country=tbl_location.objects.get(id=tbl_location.objects.get(name=contact.state).pid)
            states=tbl_location.objects.filter(pid=country.id)
            country=country.id
        
        if contact.pincode:
            pincode=contact.pincode
        if contact.tel_O:
            teleo=contact.tel_O
        if contact.tel_R:
            teler=contact.tel_R
        if contact.mobileNo:
            mobileno=contact.mobileNo
        
        if req.POST.get('crm_save',''):
            import datetime
            errors=[]
            
            
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
            
            reply=req.POST.get('reply','').strip()
            status=req.POST.get('status','').strip()
            
            cityName=None
            stateName=None
            if country!=-1:
                states=tbl_location.objects.filter(pid=country)
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not firstname:
                errors.append("please enter first Name !")
            elif not lastname:
                errors.append("please enter last Name !")
            elif state==-1:
                errors.append("please select one state !")
            elif city==-1:
                errors.append("please select one city !")
            elif mobileno and len(mobileno)<10:
                    errors.append("please enter valid Mobile no. !")
            elif email and '@' not in email and '.' not in email:
                errors.append("please enter valid email Id !")
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
                
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                contact.createdBy=i_getEmployee(req.session.get('username','')).id
                contact.status=status
                contact.title=title
                contact.firstName=firstname
                contact.lastName=lastname
                
                
                if not dob:
                    contact.dob=None
                else:
                    contact.dob=datetime.datetime.strptime(dob,'%d-%m-%Y')
                    
                if age:
                    contact.age=age
                    
                if sex:
                    contact.sex=sex
                
                contact.designation=designation
                contact.company=company
                contact.address1=address1
                contact.address2=address2
                contact.address3=address3
                contact.state=stateName
                contact.city=cityName
                contact.pincode=pincode
                
                contact.tel_O=teleo
                contact.tel_R=teler
                contact.mobileNo=mobileno
                contact.email=email
                
                
                
                #send_mail('Transasia Team',reply,EMAIL_HOST_USER,[c.email])
                if reply:
                    contact.followUps.add(tbl_followUp.objects.create(by=i_getEmployee(req.session['username']).id,reply=reply))
                    
                contact.save()
                return HttpResponseRedirect('/sales/')
            return render_to_response("followup_as_new_edit.html",locals(),context_instance=RequestContext(req))
        elif req.POST.get('crm_save_and_mail',''):
            import datetime
            errors=[]
            
            
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
            
            
            status=req.POST.get('status','').strip()    
            reply=req.POST.get('reply','').strip()
            
            cityName=None
            stateName=None
            if country!=-1:
                states=tbl_location.objects.filter(pid=country)
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not firstname:
                errors.append("please enter first Name !")
            elif not lastname:
                errors.append("please enter last Name !")
            elif state==-1:
                errors.append("please select one state !")
            elif city==-1:
                errors.append("please select one city !")
            elif mobileno and len(mobileno)<10:
                    errors.append("please enter valid Mobile no. !")
            elif email and '@' not in email and '.' not in email:
                errors.append("please enter valid email Id !")
            elif email and not reply:
                errors.append("please enter reply message !")
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
                
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                contact.createdBy=i_getEmployee(req.session.get('username','')).id
                contact.status=status
                contact.title=title
                contact.firstName=firstname
                contact.lastName=lastname
                
                
                if not dob:
                    contact.dob=None
                else:
                    contact.dob=datetime.datetime.strptime(dob,'%d-%m-%Y')
                    
                if age:
                    contact.age=age
                    
                if sex:
                    contact.sex=sex
                
                contact.designation=designation
                contact.company=company
                contact.address1=address1
                contact.address2=address2
                contact.address3=address3
                contact.state=stateName
                contact.city=cityName
                contact.pincode=pincode
                
                contact.tel_O=teleo
                contact.tel_R=teler
                contact.mobileNo=mobileno
                contact.email=email
                
                
                
                
                contact.followUps.add(tbl_followUp.objects.create(by=i_getEmployee(req.session['username']).id,reply=reply))
                send_mail('Transasia Team',reply,EMAIL_HOST_USER,[contact.email])  
                
                contact.save()
                return HttpResponseRedirect('/sales/')
            return render_to_response("followup_as_new_edit.html",locals(),context_instance=RequestContext(req))
        
    
        return render_to_response("followup_as_new_edit.html",locals(),context_instance=RequestContext(req))

    
    
    
    


def v_searchSub(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        import datetime
        ps=ProjectScope()
        months=[(1,'JAN'),(2,'FEB'),(3,'MAR'),(4,'APRIL'),(5,'MAY'),(6,'JUNE'),(7,'JULY'),(8,'AUG'),(9,'SEP'),(10,'OCT'),(11,'NOV'),(12,'DEC')]
        
        errors=[]
        cuWarnings=[]
        cuMessages=[]
        
#        _today=datetime.date.today()
#        lapse_year=_today.year
#        lapse_month=_today.month
        
        if req.POST.get('crm_search',''):
            subscription_no=req.POST.get('subscription_no','').strip()
            first_name=req.POST.get('first_name','').strip()
            last_name=req.POST.get('last_name','').strip()
            mobile_no=req.POST.get('mobile_no','').strip()
            email=req.POST.get('email','').strip()
            lapse_year=req.POST.get('lapse_year').strip()
            lapse_month=int(req.POST.get('lapse_month','-1').strip())
            
            foundSubs=[]
            customers=[]
            
            
            if subscription_no:
                if subscription_no[:len(ps.getSubPrefix())].lower()!=ps.getSubPrefix().lower():
                    errors.append('Invalid Subscription No. !')
                else:
                    try:
                        foundSubs.append(tbl_subscription.objects.get(id=subscription_no[len(ps.getSubPrefix()):]))
                    except (ValueError,tbl_subscription.DoesNotExist):
                        pass
            
            if not foundSubs and first_name and last_name:
                customers=tbl_customer.objects.filter(firstName__icontains=first_name,lastName__icontains=last_name)
            if not foundSubs and first_name:
                customers=tbl_customer.objects.filter(firstName__icontains=first_name)    
            if not foundSubs and last_name:
                customers=tbl_customer.objects.filter(lastName__icontains=last_name)
            if not customers and mobile_no:
                customers=tbl_customer.objects.filter(mobileNo=mobile_no)
            if not customers and email:
                customers=tbl_customer.objects.filter(email=email)
            if not customers and not foundSubs and lapse_month!=-1 and not lapse_year:
                errors.append('please enter year !')
            if not customers and not foundSubs and lapse_year and lapse_month:
                try:
                    lapse_year=int(lapse_year)
                    [foundSubs.append(tbl_subscription.objects.get(id=n.subId)) for n in tbl_notify.objects.filter(subEndDate__month=lapse_month,subEndDate__year=lapse_year)]
                except ValueError:
                    errors.append('Invalid Lapse on Year !')
            if not customers and not foundSubs and lapse_year:
                try:
                    lapse_year=int(lapse_year)
                    [foundSubs.append(tbl_subscription.objects.get(id=n.subId)) for n in tbl_notify.objects.filter(subEndDate__year=lapse_year)]
                except ValueError:
                    errors.append('Invalid Lapse on Year !')
                
                
            
            if not foundSubs:
                for c in customers:
                    for s in c.subscriptions.all():
                        foundSubs.append(s)
            
            if not errors:
                if not foundSubs:
                    cuWarnings.append('Not found !')
                else:
                    rows=[[tbl_customer.objects.get(subscriptions=s),s,tbl_notify.objects.get(subId=s.id).subEndDate] for s in foundSubs]
        
        return render_to_response("search_sub.html",locals(),context_instance=RequestContext(req))
    
    
    
    
def v_followUpAsSub(req,sub_id):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'crm','v'):
        import datetime
        countries=tbl_location.objects.filter(pid=0)
        customer=tbl_customer.objects.get(subscriptions=tbl_subscription.objects.get(id=sub_id))
        
        title=customer.title
        firstname=customer.firstName
        lastname=customer.lastName
        address1=customer.address1
        email=customer.email
        
        ps=ProjectScope()
        
        if customer.sex:
            sex=customer.sex
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
        if customer.mobileNo:
            mobileno=customer.mobileNo
        
        
        
        if req.POST.get('crm_create',''):
            errors=[]
            
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
            
            cityName=None
            stateName=None
            if country!=-1:
                states=tbl_location.objects.filter(pid=country)
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            
            
            if title=='-1':
                errors.append("please select at least one title !")
            elif not firstname:
                errors.append("please enter first Name !")
            elif not lastname:
                errors.append("please enter last Name !")
            elif state==-1:
                errors.append("please select one state !")
            elif city==-1:
                errors.append("please select one city !")
            elif mobileno and len(mobileno)<10:
                    errors.append("please enter valid Mobile no. !")
            elif email and '@' not in email and '.' not in email:
                errors.append("please enter valid email Id !")
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
                
                except ValueError:
                    if temp:
                        errors.append("Invalid value found for field "+temp+" !")
                    temp=None
            if not errors:
                if not dob:
                    dob=None
                else:
                    dob=datetime.datetime.strptime(dob,'%d-%m-%Y')
                
                if not age:
                    age=None
                    
                tbl_contact.objects.create(createdBy=i_getEmployee(req.session.get('username','')).id,
                                           status='n',
                                           title=title,
                                           firstName=firstname,
                                           lastName=lastname,
                                           dob=dob,
                                           age=age,
                                           sex=sex,
                                           designation=designation,
                                           company=company,
                                           address1=address1,
                                           address2=address2,
                                           address3=address3,
                                           state=stateName,
                                           city=cityName,
                                           pincode=pincode,
                                           tel_O=teleo,
                                           tel_R=teler,
                                           mobileNo=mobileno,
                                           email=email,
                                           subId=sub_id
                                           )
                
                return HttpResponseRedirect('/sales/')
        return render_to_response("followup_as_new.html",locals(),context_instance=RequestContext(req))
