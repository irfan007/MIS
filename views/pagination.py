#from django.http import HttpResponse
from misApp.pp import i_getCustomerHasSub, i_getActiveSubscription,\
    i_getInactiveSubscription
from misApp.models import ProjectScope, tbl_customer, tbl_subscription
from django.shortcuts import render_to_response
from django.template.context import RequestContext

 
def v_next(req,itemType,nextStart):
    if itemType=='subscription':
        ps=ProjectScope()
        nextStart=int(nextStart)
        rows=[s for s in tbl_subscription.objects.filter(isActive=True,isCompliment=False,isSuspend=False).order_by('id')]
        totalRows=len(rows)
    
        hasNext=False
        hasPre=False
        nextStop=(ps.SPP+nextStart)
        
        FROM=nextStart+1
        TO=totalRows
        try:
            if rows[(ps.SPP+nextStart)]:
                hasNext=True
                
                TO=nextStop
        except:
            pass
        
        if (nextStart-ps.SPP)>=0:
            hasPre=True
        
        return render_to_response('subscriptionList.html',{'FROM':FROM,'TO':TO,'nextStart':nextStop,'hasNext':hasNext,'hasPre':hasPre,'totalRows':totalRows,'rows':rows[nextStart:nextStop],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
    elif itemType=='subscriber':
        ps=ProjectScope()
        nextStart=int(nextStart)
        customers=[c for c in tbl_customer.objects.all().order_by('id')]
        totalRows=len(customers)
    
        hasNext=False
        hasPre=False
        nextStop=(ps.SBRPP+nextStart)
        
        FROM=nextStart+1
        TO=totalRows
        try:
            if customers[(ps.SBRPP+nextStart)]:
                hasNext=True
                
                TO=nextStop
        except:
            pass
        
        if (nextStart-ps.SBRPP)>=0:
            hasPre=True
        
        customers=customers[nextStart:nextStop]
        nextStart=nextStop
        return render_to_response('customerList.html',locals(),context_instance=RequestContext(req))
    elif itemType=='lapse':
        ps=ProjectScope()
        nextStart=int(nextStart)
        rows=[s for s in tbl_subscription.objects.filter(isActive=False).order_by('id')]
        totalRows=len(rows)
    
        hasNext=False
        hasPre=False
        nextStop=(ps.SPP+nextStart)
        
        FROM=nextStart+1
        TO=totalRows
        try:
            if rows[(ps.SPP+nextStart)]:
                hasNext=True
                
                TO=nextStop
        except:
            pass
        
        if (nextStart-ps.SPP)>=0:
            hasPre=True
        
        return render_to_response('renewalList.html',{'FROM':FROM,'TO':TO,'nextStart':nextStop,'hasNext':hasNext,'hasPre':hasPre,'totalRows':totalRows,'rows':rows[nextStart:nextStop],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
    
def v_previous(req,itemType,nextStart):
    if itemType=='subscription':
        ps=ProjectScope()
        rows=[s for s in tbl_subscription.objects.filter(isActive=True,isCompliment=False,isSuspend=False).order_by('id')]
        totalRows=len(rows)
        
        hasNext=True
        hasPre=False
        nextStart=int(nextStart)
        
        TO=(nextStart-ps.SPP)
        FROM=TO-ps.SPP+1
        if ((nextStart-(ps.SPP*2))-1)>0:
            hasPre=True
        
        
        return render_to_response('subscriptionList.html',{'FROM':FROM,'TO':TO,'nextStart':TO,'hasNext':hasNext,'hasPre':hasPre,'totalRows':totalRows,'rows':rows[FROM-1:TO],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))
    elif itemType=='subscriber':
        ps=ProjectScope()
        customers=[c for c in tbl_customer.objects.all().order_by('id')]
        totalRows=len(customers)
        
        hasNext=True
        hasPre=False
        nextStart=int(nextStart)
        
        TO=(nextStart-ps.SBRPP)
        FROM=TO-ps.SBRPP+1
        if ((nextStart-(ps.SBRPP*2))-1)>0:
            hasPre=True
        
        nextStart=TO
        customers=customers[FROM-1:TO]
        return render_to_response('customerList.html',locals(),context_instance=RequestContext(req))
    elif itemType=='lapse':
        ps=ProjectScope()
        rows=[s for s in tbl_subscription.objects.filter(isActive=False).order_by('id')]
        totalRows=len(rows)
        
        hasNext=True
        hasPre=False
        nextStart=int(nextStart)
        
        TO=(nextStart-ps.SPP)
        FROM=TO-ps.SPP+1
        if ((nextStart-(ps.SPP*2))-1)>0:
            hasPre=True
        
        
        return render_to_response('renewalList.html',{'FROM':FROM,'TO':TO,'nextStart':TO,'hasNext':hasNext,'hasPre':hasPre,'totalRows':totalRows,'rows':rows[FROM-1:TO],'prefix':ps.getSubPrefix(),'cprefix':ps.getCustomerPrefix()},context_instance=RequestContext(req))    