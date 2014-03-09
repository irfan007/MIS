from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext

from misApp.models import ProjectScope, tbl_subscription, tbl_notify,\
    tbl_history
from misApp.pp import i_getCustomerHasSub, i_getEmployee, i_hasPermission,\
    calcSuspendPeriod, i_setNotificationFor
from django.shortcuts import render_to_response


def v_suspended(req):
    ps=ProjectScope()
    rows=[s for s in tbl_subscription.objects.filter(isSuspend=True)]
    return render_to_response("suspend.html",{'rows':rows,'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))

def v_resume(req,pkid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'sub','u'):
        
        sub=tbl_subscription.objects.get(id=pkid)
        '''
         
        data=suspend Date / resumed Date / suspend Period(in month) / SubstartDate / old subEnddate /  old Period / new period /  Newsub End date  / reason'''
        nt=tbl_notify.objects.get(subId=sub.id)
        susPeriod=calcSuspendPeriod(sub.suspendDate)
        data=str(sub.suspendDate)+":"+str(ProjectScope().getDate().date())+":"+str(susPeriod)+":"+str(nt.startDate)+":"+str(nt.subEndDate)+":"+str(sub.period)
        sub.period=sub.period+susPeriod
        sub.save()
        nt.delete()
        i_setNotificationFor(sub.id,sub.date,sub.period)

        nt=tbl_notify.objects.get(subId=sub.id)
        data=data+":"+str(sub.period)+":"+str(nt.subEndDate)
        
        
        HRow=tbl_history.objects.filter(subId=pkid).order_by('-id')[0]
        HRow.data=data+':'+HRow.data
        HRow.save()
        #tbl_history.objects.create(data=data,subId=sub.id,type='sus')
        sub.isSuspend=False
        sub.save()

        return HttpResponse("\
        <script>alert('subscription successfully resumed !');\
        location.href = '/subscription/edit/"+pkid+"'</script>\
        ")


def v_suspendReason(req,pkid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'sub','u'):
        sub=tbl_subscription.objects.get(id=pkid)
        
        
        if req.method=="POST":
            errors=[]
            if len(req.POST.get('reason','').strip())<5:
                errors.append('Please enter valid reason !')
            if not errors:
                tbl_history.objects.create(data=req.POST.get('reason',''),subId=pkid,type='sus')
                return HttpResponseRedirect('/suspend/'+pkid)
            return render_to_response('reason.html',locals())
        return render_to_response('reason.html')
        
    
    
def v_suspend(req,pkid):
    if i_hasPermission(i_getEmployee(req.session.get('username','')),'sub','u'):
        sub=tbl_subscription.objects.get(id=pkid)
        sub.isSuspend=True
        sub.suspendDate=ProjectScope().getDate()
        sub.save()
        
        return HttpResponse("\
        <script>alert('subscription successfully suspended !');\
        window.opener.location.href = '/suspended/';\
        window.close();\
        </script>\
        ")


def v_viewReason(re,pkid):
    data=tbl_history.objects.get(id=pkid).data.split(':')
    if len(data)==1:
        '''
        when view before resume
        means data field will only contain reason other will details will be written when resume is called 
        '''
        data=data[0]
    else:
        '''
        when view after resume
        '''
        data=data[8]
    return render_to_response('reason.html',{'reason':data})
    
