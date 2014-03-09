from MIS.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from misApp.models import tbl_notify, ProjectScope
from misApp.pp import i_hasPermission, i_getEmployee, i_getActiveMagazines,\
    i_getCustomerHasSub, i_getSubscriptionsEnd, i_getSubscription
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def sendMail(prefix,rows):
    from django.utils.dateformat import DateFormat
    try:
        for row in rows:
            try:
                msg="\nDear Customer,\n\nYour subscription for Magazine '"+row[1].magazine.name+"' with subscription code "+prefix+str(row[1].id)+",\nwill expire on "+str(DateFormat(tbl_notify.objects.get(subId=row[1].id).subEndDate).format('d M Y'))+" ,to continue your subscritpion please renew it \nbefore the end Date.\n\n\nThanks,\nTransasia Team"
                send_mail('Transasia Subscription Alert',msg,EMAIL_HOST_USER,[row[0].email])
            except:
                pass
    except Exception,e:
        print e         



def v_notification(req):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'notification','v'):
        magazines=i_getActiveMagazines()
        months=[[pkid,name]for pkid,name in zip([1,2,3,4,5,6,7,8,9,10,11,12],['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec'])]
        if req.POST.get('whenview'):
            errors=[]
            magazine=req.POST.get('magazine','')
            month=int(req.POST.get('month',''))
        
            if magazine=='-1':
                errors.append("please select at least one magazine !")
            elif month==-1:
                errors.append("please select at least one month !")
        
            if not errors:
                rows=None
                prefix=ProjectScope().getSubPrefix()
                try:
                    rows=[[i_getCustomerHasSub(s),s]for s in i_getSubscriptionsEnd(magazine,month)]
                except:
                    pass
            
            
                if req.POST.get('whenview',''):
                    return render_to_response('notification.html',locals(),context_instance=RequestContext(req))
                elif req.POST.get('whenSend',''):
                    selectedRows=[r for r in rows if req.POST.get(str(r[1].id),'')=='1']
                
                    from threading import Thread
                    Thread(target=sendMail,args=[prefix,selectedRows]).start()        
                    return HttpResponse("\
                        <script>alert('notification sent!');\
                        location.href = '/notification/'\
                        </script>\
                        ")
                elif req.POST.get('whenexport',''):
                    return HttpResponse("export panding..")
                elif req.POST.get('whenprint',''):
                    return HttpResponse("print panding..")
                
            return render_to_response('notification.html',locals(),context_instance=RequestContext(req))
    
        return render_to_response('notification.html',locals(),context_instance=RequestContext(req))


def v_emailNotification(req,cid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'notification','v'):
        s=i_getSubscription(int(cid))
        customer=i_getCustomerHasSub(s)
    
        if customer:
            from threading import Thread
            Thread(target=sendMail,args=[ProjectScope().getSubPrefix(),[[customer,s]]]).start()
            return HttpResponse("\
            <script>alert('notification sent');\
            location.href = '/notification/'\
            </script>\
            ")
            
            
