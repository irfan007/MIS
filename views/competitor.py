from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from misApp.models import tbl_employee, tbl_departments,  tbl_magazine,\
    ProjectScope, tbl_magazineCombo, tbl_location,\
    tbl_competitor,tbl_compMagazine,\
    tbl_compMagOffer
import datetime
from xlwt import Workbook
from xlwt.Style import easyxf
from django.core.servers.basehttp import FileWrapper
from MIS.settings import MEDIA_ROOT
from django.db.models import Max
from misApp.pp import i_hasPermission, i_getEmployee

def v_competitors(req):
    errors=[]
    months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    companies=tbl_competitor.objects.all()
    
    month=int(ProjectScope().getDate().month)
    curyear=int(ProjectScope().getDate().year)
   
    durations=['1 year','2 year','3 year','4 year','5 year']
    if req.POST.get('getcompetitor','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'com','v'):
        month=int(req.POST.get('getmonth',''))
        curyear=(req.POST.get('curyear',''))
        companyid=int(req.POST.get('getcompany',''))
        magazineid=int(req.POST.get('magazineid',''))
        
        try:
            curyear=int(curyear)
        except:
            errors.append("Please enter the year ")
            return render_to_response('competitors.html',locals(),context_instance=RequestContext(req))    
        
        
        
        if companyid>0:
            selectmags=tbl_compMagazine.objects.filter(companyName=companyid)
            if magazineid>0:
                mag=tbl_compMagazine.objects.filter(id=magazineid)
                temp=[]
                overall=[]
                for item in mag:
                    temp=[]
                    alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
                    if len(alloffers)<1:
                        continue
                    temp.append(len(alloffers))
                    temp.append(item.getCompanyName())
                    temp.append(item.magName)
                    temp.append(alloffers[0].oldPrice)
                    temp.append(item.issueType)
                    temp.append(alloffers)
                    overall.append(temp)

                
                return render_to_response('competitors.html',locals(),context_instance=RequestContext(req))
            mag=tbl_compMagazine.objects.filter(companyName=companyid)
            temp=[]
            overall=[]
    
            for item in mag:
                temp=[]
                alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
                if len(alloffers)<1:
                        continue
                temp.append(len(alloffers))
                temp.append(item.getCompanyName())
                temp.append(item.magName)
                temp.append(alloffers[0].oldPrice)
                temp.append(item.issueType)
                temp.append(alloffers)
                overall.append(temp)
            return render_to_response('competitors.html',locals(),context_instance=RequestContext(req))
    if req.POST.get('whenexport','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'com','v'):
        curyear=req.POST.get('curyear','')
        month=int(req.POST.get('getmonth',''))
        companyid=int(req.POST.get('getcompany',''))
        magazineid=int(req.POST.get('magazineid',''))
        selectmags=tbl_compMagazine.objects.filter(companyName=companyid)
        try:
            curyear=int(curyear)
        except:
            errors.append("Please enter valid year!")
            return render_to_response('competitors.html',locals(),context_instance=RequestContext(req))
        if companyid>0:
            if magazineid>0:
                mag=tbl_compMagazine.objects.filter(id=magazineid)
                temp=[]
                overall=[]
                for item in mag:
                    temp=[]
                    alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
                    if len(alloffers)<1:
                        continue
                    temp.append(len(alloffers))
                    temp.append(item.getCompanyName())
                    temp.append(item.magName)
                    temp.append(alloffers[0].oldPrice)
                    temp.append(item.issueType)
                    temp.append(alloffers)
                    overall.append(temp)
                return v_excel_for_competitors(overall,month,curyear)   
            else:        
                
                
                mag=tbl_compMagazine.objects.filter(companyName=companyid)
                temp=[]
                overall=[]
    
                for item in mag:
                    temp=[]
                    alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
                    if len(alloffers)<1:
                            continue
                    temp.append(len(alloffers))
                    temp.append(item.getCompanyName())
                    temp.append(item.magName)
                    temp.append(alloffers[0].oldPrice)
                    temp.append(item.issueType)
                    temp.append(alloffers)
                    overall.append(temp)
                return v_excel_for_competitors(overall,month,curyear)    
                    
        else:
            allmag=tbl_compMagazine.objects.all()
            
            temp=[]
            overall=[]
    
            for item in allmag:
                temp=[]
                alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
                if len(alloffers)<1:
                    continue
                temp.append(len(alloffers))
                temp.append(item.getCompanyName())
                temp.append(item.magName)
                temp.append(alloffers[0].oldPrice)
                temp.append(item.issueType)
                temp.append(alloffers)
                overall.append(temp)
                
            return v_excel_for_competitors(overall,month,curyear)
                
           
        
        
    allmag=tbl_compMagazine.objects.all()
    temp=[]
    overall=[]
    
    for item in allmag:
        temp=[]
        alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=curyear,month=month)
        if len(alloffers)<1:
            continue
        temp.append(len(alloffers))
        temp.append(item.getCompanyName())
        temp.append(item.magName)
        temp.append(alloffers[0].oldPrice)
        temp.append(item.issueType)
        temp.append(alloffers)
        overall.append(temp)
                    
               
    

    return render_to_response('competitors.html',locals(),context_instance=RequestContext(req))

def v_excel_for_competitors(overall,month,curyear):
    if len(overall)<1:
        return HttpResponse("<script>alert('no records found !');location.href='/competitors/'</script>")
    w = Workbook()
    ws = w.add_sheet('Source_Subscription_Report')
    ws.col(1).width=25*256
    ws.col(2).width=25*256
    ws.col(9).width=35*256
    
    
    styletoprow1=easyxf('align: vertical center, horizontal center;'
                            'font: name Arial,bold true;'
                 
                            'border:bottom thin,right thin,top thin;'
                            )
    styletoprow=easyxf('align: vertical top, horizontal left;'
                            'font: name Arial;'
                            'border:bottom thin,right thin,top thin;'
                            )
    dadic={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}
    
    ws.write_merge(0,0,0,9,"Competition Report"+str(dadic[month])+str(curyear),styletoprow1)
    ws.write(1,0,'SrNo',styletoprow1)
    ws.write(1,1,'Company',styletoprow1)
    ws.write(1,2,'Magazine',styletoprow1)
    ws.write(1,3,'CoverPrice',styletoprow1)
    ws.write(1,4,'IssueType',styletoprow1)
    ws.write(1,5,'Duration',styletoprow1)
    ws.write(1,6,'Mrp',styletoprow1)
    ws.write(1,7,'Issues',styletoprow1)
    ws.write(1,8,'SubsPrice',styletoprow1)
    ws.write(1,9,'Offers',styletoprow1)
    lowerlimit=2
    x=1
    row=2
    
    for item in overall:
        y=0
        upperlimit=lowerlimit+item[0]-1
        ws.write_merge(lowerlimit,upperlimit,0,0,x,styletoprow)
        ws.write_merge(lowerlimit,upperlimit,1,1,item[1],styletoprow)
        ws.write_merge(lowerlimit,upperlimit,2,2,item[2],styletoprow)
        ws.write_merge(lowerlimit,upperlimit,3,3,item[3],styletoprow)
        ws.write_merge(lowerlimit,upperlimit,4,4,item[4],styletoprow)
        for data in item[5]:
            
            ws.write(row,5,item[5][y].duration,styletoprow)
            ws.write(row,6,item[5][y].mrp,styletoprow)
            ws.write(row,7,item[5][y].noofIssues,styletoprow)
            ws.write(row,8,item[5][y].subsPrice,styletoprow)
            ws.write(row,9,item[5][y].offers,styletoprow)
            
            
            
            row=row+1
            y=y+1
        
        
        
        lowerlimit=upperlimit+1
        x=x+1
    w.save(MEDIA_ROOT+'Competitors_Report.xls')
    myfile=open(MEDIA_ROOT+'Competitors_Report.xls',"r")
    response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Competitors_Report.xls'
    return response
 
    
    
    

    
    ''''w.save(MEDIA_ROOT+'competitor.xls')
    myfile=open(MEDIA_ROOT+'competitor.xls',"r")
    response = HttpResponse(FileWrapper(myfile), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=competitor_report.xls'
    return response'''


def v_addCompetitor(req):
    months=['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
    companies=tbl_competitor.objects.all()
    
    month=int(ProjectScope().getDate().month)
    curyear=int(ProjectScope().getDate().year)
    allmag=tbl_compMagazine.objects.all()
    temp=[]
    overall=[]
    
    durations=['1 year','2 year','3 year','4 year','5 year']
    
    
    for item in allmag:
        temp=[]
        getrows=tbl_compMagOffer.objects.filter(compMagazine=item.id,year__lte=curyear,month__lte=month).aggregate(Max('year'),Max('month'))
        alloffers=tbl_compMagOffer.objects.filter(compMagazine=item.id,year=getrows['year__max'],month=getrows['month__max'])
        if len(alloffers)<1:
            continue
        temp.append(len(alloffers))
        temp.append(item.getCompanyName())
        temp.append(item.magName)
        temp.append(alloffers[0].oldPrice)
        temp.append(item.issueType)
        temp.append(alloffers)
        overall.append(temp)

    
    if req.POST.get('saveall','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'com','a'):
            
        error=""
        if req.POST.get('magazinename1',''):
            newComp=int(req.POST.get('competitors',''))
            
            magazinename1=req.POST.get('magazinename1','').strip()
            coverPrice1=req.POST.get('coverPrice1','').strip()
            
            issuetype1=req.POST.get('issuetype1','')
            
            compet=tbl_competitor.objects.filter(companyName=newComp)
            
            try:
                coverPrice1=int(coverPrice1)        
            except:
                error="Please enter valid cover Price!"
                return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
            
            dupmag=tbl_compMagazine.objects.filter(magName=magazinename1)
            if dupmag:
                    xxx=dupmag[0].id
            else:
                p2=tbl_compMagazine(companyName=newComp,magName=magazinename1,coverPrice=coverPrice1,issueType=issuetype1)
                p2.save()
                xxx=p2.id
            i=1 
            month=int(ProjectScope().getDate().month)
            curyear=int(ProjectScope().getDate().year)   
            while(i<6):
                
                duration=req.POST.get('duration'+str(i),'')
                
                mrp=req.POST.get('mrp'+str(i),'').strip()
                if mrp:
                    try:
                        mrp=int(mrp)        
                    except:
                        error="Please enter valid mrp!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                
                issues=(req.POST.get('issues'+str(i),'').strip())
                if issues:
                    try:
                        issues=int(issues)
                    except:
                        error="Please enter valid issues!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                    
                subprice=req.POST.get('subprice'+str(i),'').strip()
                if subprice:
                    try:
                        subprice=int(subprice)
                    except:
                        error="Please enter valid subprice!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                   
                    offers=req.POST.get('offers'+str(i),'').strip()
                    p3=tbl_compMagOffer(compMagazine=xxx,oldPrice=coverPrice1,month=month,year=curyear,duration=duration,mrp=mrp,noofIssues=issues,subsPrice=subprice,offers=offers)
                    p3.save()
                i=int(i)
                i=i+1
        if req.POST.get('magazinename2',''):
            newComp=int(req.POST.get('competitors2',''))
            
            magazinename=req.POST.get('magazinename2','').strip()
            coverPrice=req.POST.get('coverPrice2','').strip()
            issuetype=req.POST.get('issuetype2','')
            
            compet=tbl_competitor.objects.filter(companyName=newComp)
            
            try:
                coverPrice=int(coverPrice)        
            except:
                error="Please enter valid cover Price!"
                return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
            
            dupmag=tbl_compMagazine.objects.filter(magName=magazinename)
            if dupmag:
                    xxx=dupmag[0].id
            else:
                p2=tbl_compMagazine(companyName=newComp,magName=magazinename,coverPrice=coverPrice,issueType=issuetype)
                p2.save()
                xxx=p2.id
            i=6 
            month=int(ProjectScope().getDate().month)
            curyear=int(ProjectScope().getDate().year)   
            while(i<11):
                
                duration=req.POST.get('duration'+str(i),'')
                
                mrp=req.POST.get('mrp'+str(i),'').strip()
                if mrp:
                    try:
                        mrp=int(mrp)        
                    except:
                        error="Please enter valid mrp!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                
                issues=(req.POST.get('issues'+str(i),'').strip())
                if issues:
                    try:
                        issues=int(issues)
                    except:
                        error="Please enter valid issues!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                    
                subprice=req.POST.get('subprice'+str(i),'').strip()
                if subprice:
                    try:
                        subprice=int(subprice)
                    except:
                        error="Please enter valid subprice!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                   
                    offers=req.POST.get('offers'+str(i),'').strip()
                    p3=tbl_compMagOffer(compMagazine=xxx,oldPrice=coverPrice,month=month,year=curyear,duration=duration,mrp=mrp,noofIssues=issues,subsPrice=subprice,offers=offers)
                    p3.save()
                i=int(i)
                i=i+1
                
        if req.POST.get('magazinename3',''):
            newComp=int(req.POST.get('competitors3',''))
            
            magazinename=req.POST.get('magazinename3','').strip()
            coverPrice=req.POST.get('coverPrice3','').strip()
            issuetype=req.POST.get('issuetype3','')
            
            compet=tbl_competitor.objects.filter(companyName=newComp)
            
            try:
                coverPrice=int(coverPrice)        
            except:
                error="Please enter valid cover Price!"
                return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
            
            dupmag=tbl_compMagazine.objects.filter(magName=magazinename)
            if dupmag:
                    xxx=dupmag[0].id
            else:
                p2=tbl_compMagazine(companyName=newComp,magName=magazinename,coverPrice=coverPrice,issueType=issuetype)
                p2.save()
                xxx=p2.id
            i=11 
            month=int(ProjectScope().getDate().month)
            curyear=int(ProjectScope().getDate().year)   
            while(i<16):
                
                duration=req.POST.get('duration'+str(i),'')
                
                mrp=req.POST.get('mrp'+str(i),'').strip()
                if mrp:
                    try:
                        mrp=int(mrp)        
                    except:
                        error="Please enter valid mrp!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                
                issues=(req.POST.get('issues'+str(i),'').strip())
                if issues:
                    try:
                        issues=int(issues)
                    except:
                        error="Please enter valid issues!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                    
                subprice=req.POST.get('subprice'+str(i),'').strip()
                if subprice:
                    try:
                        subprice=int(subprice)
                    except:
                        error="Please enter valid subprice!"
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))
                   
                    offers=req.POST.get('offers'+str(i),'').strip()
                    p3=tbl_compMagOffer(compMagazine=xxx,oldPrice=coverPrice,month=month,year=curyear,duration=duration,mrp=mrp,noofIssues=issues,subsPrice=subprice,offers=offers)
                    p3.save()
                i=int(i)
                i=i+1        
        return HttpResponseRedirect('/competitors/')
    if req.POST.get('updateall','') and i_hasPermission(i_getEmployee(req.session.get('username','')),'com','u'):
        errors=[]
        curyear=req.POST.get('curyear','').strip()    
        try:
            curyear=int(curyear)
        except:
            errors.append("Please enter valid year!")
        month=int(req.POST.get('getmonth','').strip())
        coverPrice=0
        for item in overall:
            x=1
            for data in item[5]:
                if x==1:
                    try:
                        coverPrice=int(req.POST.get(str(data.id)+'coverPrice',''))
                        
                    except:
                        errors.append("Please enter valid coverPrice")
                        return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))    
                        
                mrp=req.POST.get(str(data.id)+'mrp','').strip()
                if mrp:
                    try:
                        mrp=int(mrp)
                    except:
                        mrp=0    
                
                
                    
                    
                subsPrice=req.POST.get(str(data.id)+'subsPrice','').strip()
                try:
                    subsPrice=int(subsPrice)
                except:
                    subsPrice=0
                    
                duration=req.POST.get(str(data.id)+'duration','')
                issues=req.POST.get(str(data.id)+'noofIssues','').strip()
                try:
                    issues=int(issues)
                except:
                    issues=0
                    
                offers=req.POST.get(str(data.id)+'offers','').strip()
                uniqueoffer=tbl_compMagOffer.objects.get(id=data.id)
                p1=tbl_compMagOffer()
                p1.duration=duration
                p1.noofIssues=issues
                p1.subsPrice=subsPrice
                p1.offers=offers
                p1.mrp=mrp
                p1.year=curyear
                p1.month=month
                p1.oldPrice=coverPrice
                p1.compMagazine=uniqueoffer.compMagazine
                if p1.subsPrice>0:
                    
                    p1.save()
                x=x+1
        return HttpResponseRedirect('/competitors/')        
    return render_to_response('addCompetitor.html',locals(),context_instance=RequestContext(req))


def v_editCompetitor(req,compid):
    
    iD=int(compid)
    getrow=tbl_compMagOffer.objects.get(id=iD)
    if req.POST.get('savenew',''):
        coverPrice=req.POST.get('coverPrice','')
        duration=req.POST.get('duration','')
        mrp=req.POST.get('mrp','')
        issues=req.POST.get('issues','')
        subsprice=req.POST.get('subsprice','')
        offers=req.POST.get('offers','')
        p1=tbl_compMagOffer(compMagazine=getrow.compMagazine,oldPrice=coverPrice,month=7,year=2013,duration=duration,\
                            noofIssues=issues,subsPrice=subsprice,offers=offers,mrp=mrp)
        p1.save()
        uniobject=tbl_compMagazine.objects.get(id=getrow.compMagazine)
        uniobject.coverPrice=coverPrice
        uniobject.save()
        
    return HttpResponseRedirect('/competitors/')

