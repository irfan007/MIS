from misApp.pp import i_hasPermission, i_getEmployee, i_getActiveMagazines,\
    i_getAllStates, i_getCustomerHasSub, i_get2Dtuple, i_createMagLabel,\
    i_createGiftLabel, i_setMagazinesStatus
from misApp.models import tbl_subscription, tbl_location,\
    tbl_dispatch, tbl_notify, tbl_supportedCourier, tbl_customer, tbl_branch
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from datetime import datetime
import threading

def v_printMLabel(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'print','v'):
        months=[[pkid,name]for pkid,name in zip([1,2,3,4,5,6,7,8,9,10,11,12],['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec'])]
        magazines=i_getActiveMagazines()
        states=i_getAllStates(1)
        month=datetime.today().month
        branches=tbl_branch.objects.filter(isActive=True)
        if req.POST.get('mprint'):
            subs=[]
            errors=[]
            month=int(req.POST.get('month',''))
            magazine=int(req.POST.get('magazine',''))
            state=int(req.POST.get('state',''))
            city=int(req.POST.get('city',''))
            pincode=req.POST.get('pincode','')
            branch=int(req.POST.get('branch',''))
            
            cities=None
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
            
            try:
                queryDate=datetime(datetime.today().year,month,datetime.today().day)
                subs=[tbl_subscription.objects.get(id=nt.subId) for nt in tbl_notify.objects.filter(startDate__lte=queryDate,subEndDate__gte=queryDate) if not tbl_subscription.objects.get(id=nt.subId).isSuspend] 
                #return HttpResponse(subs)
            except:
                pass
            
            
            if month==-1:
                errors.append("please select at least one month !")
                
            if month!=-1 and not subs:
                errors.append("No issues found for selected month !")
            
            if subs and magazine!=-1:
                subs=[s for s in subs if s.magazine.id==magazine ]
                if not subs:
                    errors.append("No issues found for selected magazine for "+str(months[month-1][1])+" month !")
            
            if subs and branch!=-1:
                filterSubs=[]
                for s in subs:
                    cust=i_getCustomerHasSub(s)
                    if cust.branch and cust.branch.id==branch:
                        filterSubs.append(s)
                    subs=filterSubs
                if not subs:
                    errors.append("No issues found for selected branch !")
            if subs and state!=-1:
                subs=[s for s in subs if i_getCustomerHasSub(s).state==tbl_location.objects.get(id=state).name]
                if not subs:
                    errors.append("No issues found for selected state !")
                
            if subs and city!=-1:
                subs=[s for s in subs if i_getCustomerHasSub(s).city==tbl_location.objects.get(id=city).name]
                if not subs:
                    errors.append("No issues found for selected city !")
                
            if subs and pincode:
                subs=[s for s in subs if i_getCustomerHasSub(s).pincode==pincode]
                if not subs:
                    errors.append("No issues found for pincode !")
                    
            if not errors:
                subs2D=i_get2Dtuple(subs,2)
                from reportlab.lib.pagesizes import A4
                from reportlab.pdfgen import canvas
                #from django.core.servers.basehttp import FileWrapper
                response = HttpResponse(mimetype='application/pdf')
                #response['Content-Disposition']="attachment;filename=label.pdf"
                response['Content-Disposition']="filename=Magazine_label.pdf"
                c = canvas.Canvas(response, pagesize=A4)
                i_createMagLabel(c,A4,subs2D)
                threading.Thread(target=i_setMagazinesStatus,args=[subs,datetime.today().year,month]).start()
                c.save()
                return response
                    
                #return HttpResponse("received:mon:"+str(month)+"  state:"+str(state)+" city:"+str(city)+" area:"+str(area)+" magazine:"+str(magazine))
            return render_to_response('Mlabel.html',locals(),context_instance=RequestContext(req))
        return render_to_response('Mlabel.html',locals(),context_instance=RequestContext(req))

def v_printGLabel(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'print','v'):
        months=[[pkid,name]for pkid,name in zip([1,2,3,4,5,6,7,8,9,10,11,12],['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec'])]
        states=i_getAllStates(1)
        couriers=tbl_supportedCourier.objects.filter(isActive=True)
        branches=tbl_branch.objects.filter(isActive=True)
        #courierID=1#couriers to be used for gift dispatch 
        status='ih'#all gift has status either i or h 
        if req.POST.get('gprint'):
            errors=[]
            status=req.POST.get('status','')
            courier=int(req.POST.get('courier',''))
            month=int(req.POST.get('month',''))
            
            state=int(req.POST.get('state',''))
            city=int(req.POST.get('city',''))
            pincode=req.POST.get('pincode','')
            branch=int(req.POST.get('branch',''))
            
            cities=None
            if state!=-1:
                cities=tbl_location.objects.filter(pid=state)
                
            if status=='-1':
                errors.append("please select at least one status !")
            
            if courier==-1:
                errors.append("please select at least one courier !")
                 
            rows=[[dispatchRow.id,courier] for dispatchRow in tbl_dispatch.objects.filter(itemType="g",status__in=status)]
            
 
            #return HttpResponse(subs)
            
            
            if courier!=-1 and not rows:
                errors.append("No gifts found for selected status !")
            
            if rows and month!=-1:
                rows=[r for r in rows if tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=r[0]).customerId).subscriptions.all()[0].date.month==month ]
                if not rows:
                    errors.append("No gifts found for selected month !")
            
            if rows and branch!=-1:
                filterrows=[]
                for r in rows:
                    cust=tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=r[0]).customerId)
                    if cust.branch and cust.branch.id==branch:
                        filterrows.append(r)
                    rows=filterrows
                if not rows:
                    errors.append("No gifts found for selected branch !")
            if rows and state!=-1:
                rows=[r for r in rows if tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=r[0]).customerId).state==tbl_location.objects.get(id=state).name]
                if not rows:
                    errors.append("No gifts found for selected state !")
                
            if rows and city!=-1:
                rows=[r for r in rows if tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=r[0]).customerId).city==tbl_location.objects.get(id=city).name]
                if not rows:
                    errors.append("No gifts found for selected city !")
                
            if rows and pincode:
                rows=[r for r in rows if tbl_customer.objects.get(id=tbl_dispatch.objects.get(id=r[0]).customerId).pincode==pincode]
                if not rows:
                    errors.append("No gifts found for pincode !")
                    
            if not errors:
                row2D=i_get2Dtuple(rows,2)
                from reportlab.lib.pagesizes import A4
                from reportlab.pdfgen import canvas
                #from django.core.servers.basehttp import FileWrapper
                response = HttpResponse(mimetype='application/pdf')
                #response['Content-Disposition']="attachment;filename=label.pdf"
                response['Content-Disposition']="filename=Magazine_label.pdf"
                c = canvas.Canvas(response, pagesize=A4)
                i_createGiftLabel(c,A4,row2D)
                c.save()
                return response
                    
                #return HttpResponse("received:mon:"+str(month)+"  state:"+str(state)+" city:"+str(city)+" area:"+str(area)+" magazine:"+str(magazine))
            return render_to_response('Glabel.html',locals(),context_instance=RequestContext(req))
        return render_to_response('Glabel.html',locals(),context_instance=RequestContext(req))
    
    
