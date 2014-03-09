from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from misApp.views import v_allTaskList, workfortoDoList, dateformatConvertor
from misApp.models import tbl_subscription, tbl_magazine, tbl_transaction,\
    ProjectScope, tbl_customer, tbl_dispatch, tbl_scheme, tbl_source, tbl_tenure,\
    tbl_history, tbl_renewal, tbl_branch, tbl_supportedCourier
from xlwt.Style import easyxf
from MIS.settings import MEDIA_ROOT
from xlwt import Workbook
from xlwt.Style import easyxf
from django.core.servers.basehttp import FileWrapper
from xlwt.Formatting import Font

from django.http import HttpResponse
from django.template.context import RequestContext
from django.db.models import Q
from misApp.pp import i_hasPermission, i_getEmployee
'''
def v_reports(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('getoption',''):
        getvalue=req.POST.get('opinions','')
        if getvalue=='competitors':
            return HttpResponseRedirect('/competitors/')
        elif getvalue=="chequedepositReport":
            return HttpResponseRedirect('/report/chequedeposit/')
        elif getvalue=="giftReport":
            return HttpResponseRedirect('/report/gift/')
        elif getvalue=="offerReport":
            return HttpResponseRedirect('/report/offer/')
        elif getvalue=="srcsubReport":
            return HttpResponseRedirect('/report/srcsub/')
    return render_to_response('reports.html',locals())

''' 
def getdataforGiftReport(startdate,enddate):
    
    rows=tbl_dispatch.objects.filter(dispatchDate__gte=startdate,dispatchDate__lte=enddate,itemType="g")
    data=[]
    for item in rows:
        row=[]
        getcust=tbl_customer.objects.get(id=item.customerId)
        getsub=getcust.subscriptions.all()
        if len(getsub)>1:
            row.append(item)
            row.append(getcust)
            custid=ProjectScope().getCustomerPrefix()+str(getcust.id)
            row.append(custid)
        else:
            row.append(item)
            row.append(getcust)
            subid=ProjectScope().getSubPrefix()+str(getsub[0].id)
            row.append(subid)
            
           
        data.append(row)

    return data

def v_reportGift(req):
    #months=['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    errors=[]
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('whenview','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'report','v'):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
        rows=getdataforGiftReport(startdate1,enddate1)
        
        return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforGiftReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/gift/'</script>")
        w = Workbook()
        ws = w.add_sheet('GiftReport')
        ws.col(4).width=25*256
        ws.col(2).width=25*256
        ws.col(3).width=15*256
        ws.col(1).width=25*256
        ws.col(5).width=20*256
        ws.col(0).width=5*256
        ws.col(6).width=15*256
        ws.col(7).width=25*256
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write_merge(0,0,0,7,"Gift Tracking Report from "+str(startdate1)+" to "+str(enddate1),styletoprow1)
        ws.write(1,0,'S.No',styletoprow1)                                  
        ws.write(1,1,'Subscriber Name',styletoprow1)
        ws.write(1,2,'SubsId/CustId',styletoprow1)
        ws.write(1,3,'GiftName',styletoprow1)
        ws.write(1,4,'Dispatch Date',styletoprow1)
        ws.write(1,5,'Dispatch Through',styletoprow1)
        ws.write(1,6,'AWB Details',styletoprow1)
        ws.write(1,7,'Dispatch Status',styletoprow1)
        x=2
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data[1].firstName,styletoprow)
                    
            
                ws.write(x,2,data[2],styletoprow)
            
                ws.write(x,3,data[0].getItemName(),styletoprow)
                ws.write(x,4,str(data[0].dispatchDate),styletoprow)
                ws.write(x,5,data[0].courierType.name,styletoprow)
                ws.write(x,6,data[0].courierNo,styletoprow)
                ws.write(x,7,data[0].getStatus(),styletoprow)
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'gift report.xls')
        myfile=open(MEDIA_ROOT+'gift report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=giftreport_report.xls'
        return response

    #month=int(ProjectScope().getDate().month)
    #curyear=ProjectScope().getDate().year
    if (i_hasPermission(i_getEmployee(req.session.get('username','')),'report','v')):
        month=int(ProjectScope().getDate().month)
        curyear=ProjectScope().getDate().year
        if month<10:
            startdate='01-0'+str(month)+'-'+str(curyear)
        else:
            startdate='01-'+str(month)+'-'+str(curyear)   
        startdate1=dateformatConvertor(startdate)
        enddate=ProjectScope().onlyDate()
        enddate1=dateformatConvertor(enddate)
        rows=getdataforGiftReport(startdate1,enddate1)
        
        return render_to_response('giftReport.html',locals(),context_instance=RequestContext(req))
    

def v_offerReport(req):
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    errors=[]
            
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('offerReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('offerReport.html',locals(),context_instance=RequestContext(req))
        overall=getdataforOfferReport(startdate1,enddate1)
            
        return render_to_response('offerReport.html',locals())
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('offerReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('offerReport.html',locals(),context_instance=RequestContext(req))
        overall=getdataforOfferReport(startdate1,enddate1)
        if len(overall)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/offer/'</script>")         
        w = Workbook()
    
        ws = w.add_sheet('OfferReport')
        ws.col(1).width=20*256
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                           'border:bottom thin,right thin,top thin;'
                           )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                     
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write_merge(0,0,0,6,"Offers Report from "+str(startdate1)+" to "+str(enddate1),styletoprow)
        ws.write(1,0,'S.No',styletoprow1)                                  
        ws.write(1,1,'Magazine Name',styletoprow1)
        ws.write(1,2,'Tenure',styletoprow1)
        ws.write(1,3,'MRP',styletoprow1)
        ws.write(1,4,'OfferPrice',styletoprow1)
        ws.write(1,5,'YouSave',styletoprow1)
        ws.write(1,6,'FreeGift',styletoprow1)
        lowerlimit=2
        x=1
        for data in overall:
            
            ws.write_merge(lowerlimit,lowerlimit+int(data[0])-1,0,0,x,styletoprow)
            count=1
            for values in data[1]:
                if count==1:
                    if values.magazine!=None:
                        
                        ws.write_merge(lowerlimit,lowerlimit+int(data[0])-1,1,1,values.magazine.name,styletoprow)
                    else:
                        ws.write_merge(lowerlimit,lowerlimit+int(data[0])-1,1,1,values.magazineCombo.name,styletoprow)    
                ws.write(lowerlimit,2,values.tenure.name,styletoprow)
                if values.magazine:
                    ws.write(lowerlimit,3,values.magazine.price,styletoprow)
                else:
                    ws.write(lowerlimit,3,values.magazineCombo.magComboPrice(),styletoprow)    
                ws.write(lowerlimit,4,values.cost,styletoprow)
                ws.write(lowerlimit,5,values.description,styletoprow)
                ws.write(lowerlimit,6,values.getgiftname(),styletoprow)
                lowerlimit=lowerlimit+1
                count=count+1
            
            #lowerlimit=lowerlimit+1
            x=x+1
        
        w.save(MEDIA_ROOT+'offer report.xls')
        myfile=open(MEDIA_ROOT+'offer report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=offerreport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    
    
    overall=getdataforOfferReport(startdate1,enddate1)
    return render_to_response('offerReport.html',locals(),context_instance=RequestContext(req))

def getdataforOfferReport(startdate1,enddate1):
    
    overall=[]
    allrows=tbl_scheme.objects.filter(startDate__lte=enddate1)
    allrows=allrows.filter(Q(isActive=True)|Q(endDate__gte=startdate1))
    
    allrows=allrows.filter(~Q(magazine=None))

    magazine=allrows.values('magazine').annotate()
    for item in magazine:
        rows=allrows.filter(magazine=item['magazine'])
        length=len(rows)
    
        temp=[]
        temp.append(length)
        for value in rows:
            if value.magazine:
                mrp=int(value.magazine.price)*int(value.tenure.timePeriod)
                value.magazine.price=mrp
                value.description=str(mrp-value.cost)
        temp.append(rows)
        
        
        overall.append(temp)
        
        
    allrows=tbl_scheme.objects.filter(startDate__lte=enddate1)
    allrows=allrows.filter(Q(isActive=True)|Q(endDate__gte=startdate1))
    
    allrows=allrows.filter(~Q(magazineCombo=None))

    magazineCombo=allrows.values('magazineCombo').annotate()
    for item in magazineCombo:
        rows=allrows.filter(magazineCombo=item['magazineCombo'])
        length=len(rows)
    
        temp=[]
        temp.append(length)
        for value in rows:
            if value.magazineCombo:
                mrp=int(value.magazineCombo.magComboPrice())*int(value.tenure.timePeriod)
                value.magazineCombo.price=mrp
                value.description=str(mrp-value.cost)
        temp.append(rows)
        
        
        overall.append(temp)    
            
    return overall


def getallmagazines():
    
    return tbl_magazine.objects.all()
    
def v_srcsubReport(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    
    magrows=getallmagazines()
    
    errors=[]
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))
        rows=getdataforsrcsubReport(startdate1,enddate1)
            
        return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))
        rows=getdataforsrcsubReport(startdate1,enddate1)
        
        
        magrows=getallmagazines()
            
        w = Workbook()
        ws = w.add_sheet('Source_Subscription_Report')
        ws.col(0).width=25*256
    
    
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        styletoprow=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial;'
                            'border:bottom thin,right thin,top thin;'
                            )
        length=len(magrows)
        ws.write_merge(0,0,0,0+length,"Source Subscription Report from "+str(startdate1)+" to "+str(enddate1),styletoprow1)
        ws.write(1,0,'Source/Magazine',styletoprow1)
        length=1
        for mag in magrows:
            ws.col(length).width=30*256
            ws.write(1,length,mag.name,styletoprow1)
            length=length+1
        length=2    
        for data in rows:
            ws.write(length,0,data[0],styletoprow1)
            col=1
            for items in data[1]:
                ws.write(length,col,items,styletoprow)
                col=col+1
            
            length=length+1
        w.save(MEDIA_ROOT+'Source_Subscription_Report.xls')
        myfile=open(MEDIA_ROOT+'Source_Subscription_Report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Source_Subscription_Report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    
    
    
    rows=getdataforsrcsubReport(startdate1,enddate1)
    return render_to_response('srcsubReport.html',locals(),context_instance=RequestContext(req))

    
def getdataforsrcsubReport(startdate1,enddate1): 
    
    customer=tbl_customer.objects.filter()
    sources=tbl_source.objects.filter(pid=0)
    magazines=getallmagazines()
    overall=[]
    for item in customer:
        subscription=item.subscriptions.filter(date__gte=startdate1,date__lte=enddate1)
        for sub in subscription:
            list=[]
        
            
            magazine=sub.magazine.name
            source=item.subSource.getParentCategory()
            list.append(magazine)
            list.append(source)
            overall.append(list)

    newoverall=[]        
    for source in sources:
        count=0
        data=[]
        len=[]
        data.append(source.categoryName)
        for magazine in magazines:
        
            for item in overall:
                if item[0]==magazine.name:
                
                        if item[1]==source.categoryName:
                            count=count+1
                    
            len.append(count)
        
            count=0
        data.append(len)    
        len=[]    
        newoverall.append(data)

    return newoverall    

#Payment Section

def getdataforChequeReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='chq',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows
def v_reportchequedeposit(req):
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    errors=[]
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforChequeReport(startdate1,enddate1)
        return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforChequeReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/cheque/'</script>")
        w = Workbook()
        ws = w.add_sheet('ChequeReport')
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'ChequeNo',styletoprow1)
        ws.write(0,2,'ChequeDate',styletoprow1)
        ws.write(0,3,'BankName',styletoprow1)
        ws.write(0,4,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                ws.write(x,3,data.bankName,styletoprow)
                ws.write(x,4,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'cheque report.xls')
        myfile=open(MEDIA_ROOT+'cheque report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=chequereport_report.xls'
        return response
    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    rows=getdataforChequeReport(startdate1,enddate1)
    return render_to_response('chequeReport.html',locals(),context_instance=RequestContext(req))
def getdataforDraftReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='d',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows
def v_reportdraftdeposit(req):
    errors=[]
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforDraftReport(startdate1,enddate1)
        return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforDraftReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/draft/'</script>")
        w = Workbook()
        ws = w.add_sheet('DraftReport')
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'DraftNo',styletoprow1)
        ws.write(0,2,'DraftDate',styletoprow1)
        ws.write(0,3,'BankName',styletoprow1)
        ws.write(0,4,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                ws.write(x,3,data.bankName,styletoprow)
                ws.write(x,4,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'draft report.xls')
        myfile=open(MEDIA_ROOT+'draft report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=draftreport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    rows=getdataforDraftReport(startdate1,enddate1)
    return render_to_response('draftReport.html',locals(),context_instance=RequestContext(req))





def getdataforneftReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='a',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows
def v_reportneftdeposit(req):
    errors=[]
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforneftReport(startdate1,enddate1)
        return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))
        
            
        
            
        
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforneftReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/neft/'</script>")
        w = Workbook()
        ws = w.add_sheet('neftReport')
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'NeftNo',styletoprow1)
        ws.write(0,2,'NeftDate',styletoprow1)
        ws.write(0,3,'BankName',styletoprow1)
        ws.write(0,4,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                ws.write(x,3,data.bankName,styletoprow)
                ws.write(x,4,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'neft report.xls')
        myfile=open(MEDIA_ROOT+'neft report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=neftreport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    rows=getdataforneftReport(startdate1,enddate1)
    return render_to_response('neftReport.html',locals(),context_instance=RequestContext(req))

def getdataforonlineReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='o',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows


def v_reportonlinepayment(req):
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    errors=[]
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforonlineReport(startdate1,enddate1)
        return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))    
        
            
        
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforonlineReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/online/'</script>")
        w = Workbook()
        ws = w.add_sheet('onlineReport')
        ws.col(1).width=20*256
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'TransactionNo',styletoprow1)
        ws.write(0,2,'TransactionDate',styletoprow1)
        ws.write(0,3,'BankName',styletoprow1)
        ws.write(0,4,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                ws.write(x,3,data.bankName,styletoprow)
                ws.write(x,4,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'online report.xls')
        myfile=open(MEDIA_ROOT+'online report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=onlinereport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    
    rows=getdataforonlineReport(startdate1,enddate1)
    return render_to_response('onlineReport.html',locals(),context_instance=RequestContext(req))
def getdataforcreditReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='cd',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows
def v_CreditReport(req):
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    errors=[]
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforcreditReport(startdate1,enddate1)
        return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforcreditReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/credit-debit/'</script>")
        w = Workbook()
        ws = w.add_sheet('credit_debitReport')
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'CardNo',styletoprow1)
        ws.write(0,2,'Date',styletoprow1)
        ws.write(0,3,'BankName',styletoprow1)
        ws.write(0,4,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                ws.write(x,3,data.bankName,styletoprow)
                ws.write(x,4,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'credit_debit report.xls')
        myfile=open(MEDIA_ROOT+'credit_debit report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=credit_debitreport_report.xls'
        return response
    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    rows=getdataforcreditReport(startdate1,enddate1)
    return render_to_response('credit-debit.html',locals(),context_instance=RequestContext(req))

def getdataforcashReport(startdate1,enddate1):
    rows=tbl_transaction.objects.filter(payMode='c',chequeDate__gte=startdate1,chequeDate__lte=enddate1)
    
    return rows


def v_reportcashpayment(req):
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    errors=[]
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforcashReport(startdate1,enddate1)    
        
            
        return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))
        
        rows=getdataforcashReport(startdate1,enddate1)
        if len(rows)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/cash/'</script>")
        w = Workbook()
        ws = w.add_sheet('cashReport')
        ws.col(1).width=20*256
        ws.col(2).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write(0,0,'S.No',styletoprow1)                                  
        ws.write(0,1,'ReceiptNo',styletoprow1)
        ws.write(0,2,'ReceiptDate',styletoprow1)
       
        ws.write(0,3,'Amount',styletoprow1)
        
        x=1
    
        for data in rows:
            try:
                ws.write(x,0,x,styletoprow)                                  
                ws.write(x,1,data.chequeNo,styletoprow)
                    
            
                ws.write(x,2,str(data.chequeDate),styletoprow)
            
                
                ws.write(x,3,data.amount,styletoprow)
             
                x=x+1
            except:
                pass    
        w.save(MEDIA_ROOT+'cash report.xls')
        myfile=open(MEDIA_ROOT+'cash report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=cashreport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    
    rows=getdataforcashReport(startdate1,enddate1)
    return render_to_response('cashReport.html',locals(),context_instance=RequestContext(req))

#Subscription Report
def getallMagz():
    
    return tbl_magazine.objects.all()
def getallTenu():
    return tbl_tenure.objects.all()
def getdataformonthlySubscription(month,curyear):
    tenrows=getallTenu()
    magrows=getallMagz()
    allsubscription=tbl_subscription.objects.filter(date__month=month,date__year=curyear)
    temp=[]
    for magazine in magrows:
        for tenure in tenrows:
            count=0
            for item in allsubscription:
                if item.period==tenure.timePeriod:
                    if item.magazine.name==magazine.name:
                        count=count+1  
            temp.append(count)
    return temp
def v_monthlySubscription(req):
    months=['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    magrows=getallMagz()
    tenrows=getallTenu()
    forrowspan=len(tenrows)
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('whenview',''):
        month=int(req.POST.get('getmonth',''))
        
        try:
        
            curyear=int(req.POST.get('year',''))
            temp=getdataformonthlySubscription(month,curyear)
            
        except:
            
            temp=[]
                
        return render_to_response('monthSubs.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        month=int(req.POST.get('getmonth',''))
        
        try:
        
            curyear=int(req.POST.get('year',''))
            temp=getdataformonthlySubscription(month,curyear)
            
        except:
            
            temp=[]
        if len(temp)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/monthlySubscriptions/'</script>")
        w = Workbook()
        ws = w.add_sheet('SubsReport')
        ws.col(0).width=20*256
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        dadic={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
        ws.write(0,0,dadic[month]+str(curyear),styletoprow1)
        ws.write(1,0,'Magazines',styletoprow1)
        ws.write(2,0,'Tenures',styletoprow1)
        ws.write(3,0,'Subscriptions',styletoprow1)
        
        x=1
        y=1
        for item in magrows: 
            ws.write_merge(1,1,x,x+(len(tenrows)-1),item.name,styletoprow1)
            x=x+len(tenrows)
            for values in tenrows:
                ws.write(2,y,values.name,styletoprow1)
                y=y+1
        y=1        
        for item in temp:
            ws.write(3,y,item,styletoprow)
            y=y+1
                
       
        w.save(MEDIA_ROOT+'Monthly report.xls')
        myfile=open(MEDIA_ROOT+'Monthly report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Monthlyreport_report.xls'
        return response

    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    temp=getdataformonthlySubscription(month,curyear)
    return render_to_response('monthSubs.html',locals(),context_instance=RequestContext(req))

def get_data_for_active_subscription(startdate1,enddate1):
    magrows=getallmagazines()
    #dadic={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
    firstrow=['subscription as on']
    allsubs=tbl_subscription.objects.filter(isActive=True)
    secondrow=['Lapse/cancelled']
    hisrows=tbl_history.objects.filter(type='can',date__gte=startdate1,date__lte=enddate1)
    thirdrow=['renewed in advance']
    allrenewed=tbl_renewal.objects.filter(type='a',date__gte=startdate1,date__lte=enddate1)
    fourthrow=['active after cancellation']
    renewed=tbl_renewal.objects.filter(type='r',date__gte=startdate1,date__lte=enddate1)
    fifthrow=['conversion']
    allhis=tbl_history.objects.filter(type='m',date__gte=startdate1,date__lte=enddate1)
    sixthrow=['New subscriptions generated']
    getdata=tbl_subscription.objects.filter(date__gte=startdate1,date__lte=enddate1)
    seventhrow=['Subscription as on '+str(ProjectScope().getDate().date())]
    final=[]
    for item in magrows:
        rows=allsubs.filter(magazine=item)
        firstrow.append(len(rows))
        
    
        count=0
        for data in hisrows:
            if item.name==data.getmagazinename():
                count=count+1
        secondrow.append(count)
    
    
        count=0
        for value in allrenewed:
            if item.name==value.getMagazineName():
                count=count+1
        thirdrow.append(count)
    
    
        count=0
        for value in renewed:
            if item.name==value.getMagazineName():
                count=count+1
        fourthrow.append(count)    
    
    
        count=0
        for value in allhis:
            if item.name==value.getmagazinename():
                count=count+1
        fifthrow.append(count)
    
    
        count=0
        for data in getdata:
            if item.name==data.magazine.name:
                count=count+1
        sixthrow.append(count)          
        
        
        
        
        rows=allsubs.filter(magazine=item)
        seventhrow.append(len(rows))
    
    final.append(firstrow)
    final.append(secondrow)
    final.append(thirdrow)
    final.append(fourthrow)
    final.append(fifthrow)
    final.append(sixthrow)
    final.append(seventhrow)
    return final
def v_activesubscriptionreport(req):
    
    errors=[]
    magrows=getallmagazines()
    
    
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if req.POST.get('whenview',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('activesubscriptionreport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('activesubscriptionreport.html',locals(),context_instance=RequestContext(req))
        
        temp=get_data_for_active_subscription(startdate1,enddate1)
                
        return render_to_response('activesubscriptionreport.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport',''):
        startdate=req.POST.get('startdate','')
        try:
            startdate1=dateformatConvertor(startdate)
        except:
            errors.append("Please enter From date in valid format!")
            return render_to_response('activesubscriptionreport.html',locals(),context_instance=RequestContext(req))
        
        enddate=req.POST.get('enddate','')
        try:
            enddate1=dateformatConvertor(enddate)
        except:
            errors.append("Please enter To date in valid format!")
            return render_to_response('activesubscriptionreport.html',locals(),context_instance=RequestContext(req))
        
        temp=get_data_for_active_subscription(startdate1,enddate1)
        
        if len(temp)<1:
            return HttpResponse("<script>alert('no records found !');location.href='/report/MIS2/'</script>")
        w = Workbook()
        ws = w.add_sheet('MISReport')
        ws.col(0).width=30*256
        
        
        styletoprow=easyxf('align: vertical center, horizontal center;'
                           'font: name Arial;'
                 
                           'border:bottom thin,right thin,top thin;'
                          )
        styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
        ws.write_merge(0,0,0,4,"MIS Report from "+str(startdate1)+" to "+str(enddate1),styletoprow)
        ws.write(1,0,'Subscriptions/Magazine',styletoprow1)
        xx=1
        for item in magrows:
            ws.col(xx).width=20*256
            ws.write(1,xx,item.name,styletoprow1)
            xx=xx+1
        xx=0
        for item in temp[1]:
            
            ws.write(2,xx,item,styletoprow1)
            xx=xx+1
        xx=0
        for item in temp[2]:
            
            ws.write(3,xx,item,styletoprow1)
            xx=xx+1
                
        xx=0
        for item in temp[3]:
            
            ws.write(4,xx,item,styletoprow1)
            xx=xx+1
        
        xx=0
        for item in temp[4]:
            
            ws.write(5,xx,item,styletoprow1)
            xx=xx+1
        xx=0
        for item in temp[5]:
            
            ws.write(6,xx,item,styletoprow1)
            xx=xx+1
          
          
        xx=0
        for item in temp[6]:
            
            ws.write(7,xx,item,styletoprow1)
            xx=xx+1        
            
            
        w.save(MEDIA_ROOT+'MIS report.xls')
        myfile=open(MEDIA_ROOT+'MIS report.xls',"r")
        response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mis_report.xls'
        return response

    
    month=int(ProjectScope().getDate().month)
    curyear=ProjectScope().getDate().year
    
    if month<10:
        startdate='01-0'+str(month)+'-'+str(curyear)
    else:
        startdate='01-'+str(month)+'-'+str(curyear)   
    startdate1=dateformatConvertor(startdate)
    enddate=ProjectScope().onlyDate()
    enddate1=dateformatConvertor(enddate)
    
    

    
    temp=get_data_for_active_subscription(startdate1,enddate1)
   
    
    
                    
    return render_to_response("activesubscriptionreport.html",locals(),context_instance=RequestContext(req))
def v_POreport(req):
    months=['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    workfortoDoList(req)
    alltask=v_allTaskList(req)
    if (i_hasPermission(i_getEmployee(req.session.get('username','')),'report','v')):
        month=int(ProjectScope().getDate().month)
        curyear=ProjectScope().getDate().year
    
        branches=getallBranches()
        couriers=getallcouriers()
        
        
        if req.POST.get('whenview',''):
            month=int(req.POST.get('getmonth',''))
            try:
            
                curyear=int(req.POST.get('year',''))
                temp=get_data_for_PO_report(month,curyear)
                
            except:
                
                temp=[]
                    
            return render_to_response('POreport.html',locals(),context_instance=RequestContext(req))
        if req.POST.get('whenexport',''):
            month=int(req.POST.get('getmonth',''))
            
            try:
            
                curyear=int(req.POST.get('year',''))
                temp=get_data_for_PO_report(month,curyear)
                
            except:
                
                temp=[]
            
            w = Workbook()
            ws = w.add_sheet('POReport')
            ws.col(0).width=25*256
            
            styletoprow=easyxf('align: vertical center, horizontal center;'
                               'font: name Arial;'
                     
                               'border:bottom thin,right thin,top thin;'
                              )
            styletoprow1=easyxf('align: vertical center, horizontal center;'
                                'font: name Arial,bold true;'
                     
                                'border:bottom thin,right thin,top thin;'
                                )
            dadic={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
            ws.write_merge(0,0,0,len(couriers)+len(branches)+1,"PO Report for "+dadic[month]+str(curyear),styletoprow1)
            ws.write(1,0,'Magazines',styletoprow1)
            x=1
            for item in branches:
                ws.write(1,x,item.code,styletoprow1)
                x=x+1
            for item in couriers:
                ws.write(1,x,item.code,styletoprow1)
                x=x+1
            ws.write(1,x,'Total',styletoprow1)    
            y=2
            x=0
                   
            for data in temp:
                while x<len(data):
                    ws.write(y,x,data[x],styletoprow)
                    
                    
                      
                    x=x+1
                y=y+1
                x=0    
           
            w.save(MEDIA_ROOT+'PO report.xls')
            myfile=open(MEDIA_ROOT+'PO report.xls',"r")
            response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=POreport_report.xls'
            return response

            
    

    
        temp=get_data_for_PO_report(month,curyear)
        
        #return HttpResponse(temp)
        return render_to_response('POreport.html',locals(),context_instance=RequestContext(req))
    
def get_data_for_PO_report(month,year):
    magazines=getallmagazines()
    branches=getallBranches()
    couriers=getallcouriers()
    temp=[]
    month=month
    year=year
    length=0
    overall=[]
    total=0
    
    for item in magazines:
        temp.append(item.name)
        string="'"+str(year)+","+str(month)+"'"+": 1"
        
        subs=tbl_subscription.objects.filter(magazine=item,issues__icontains=string)
        
        for b in branches:
            length=0
            for s in subs:
                if b.name==s.getBranchId():
                    length=length+1
                    
            temp.append(length)
            total=total+length
        for c in couriers:
            length=0
            for s in subs:
                if c.name==s.getCourierId():
                    length=length+1
            temp.append(length)
            total=total+length
        temp.append(total)    
        total=0
        overall.append(temp)
        temp=[]    
                
    return overall
def getallBranches():
    return tbl_branch.objects.all()
def getallcouriers():
    return tbl_supportedCourier.objects.all()     