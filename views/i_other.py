
from misApp.models import tbl_magazineCombo, tbl_scheme,\
    tbl_magazine, tbl_source, tbl_tenure, tbl_gift, tbl_role, tbl_departments,\
    tbl_branch, tbl_competitor, tbl_ticketType, tbl_employee, ProjectScope,\
    tbl_events
from misApp.pp import i_getAllStates, i_getAllCities, i_getAllArea,\
    i_getAllSubSources, i_getActiveGifts, i_getActiveCombos, i_getActiveTenures,\
    i_getActiveMagazines
from django.http import HttpResponse




    
def v_responder(req):
    
    if req.GET.get('updateCal',''):
        data=req.GET.get('updateCal','')
        
        res="ok"
        try:
            # d is list has format [title,start date (as 2013-12-4 0:0),end date,foregroundColor,backgroundColor]
            tbl_events.objects.filter(username=req.session['username']).delete()
            for title,sd,ed,fc,bc in eval(data):
                try:
                    import datetime
                    tbl_events.objects.create(username=req.session['username'],event=title,startDate=datetime.datetime.strptime(sd,"%Y-%m-%d %H:%M"),endDate=datetime.datetime.strptime(ed,"%Y-%m-%d %H:%M"),fgColor="#"+fc,bgColor="#"+bc)
                except:
                    pass
        except SyntaxError:
            res="error"
        
            
        return HttpResponse(res)
    elif req.GET.get('employeesOfDepartment',''):
        ps=ProjectScope()
        employees=tbl_employee.objects.filter(department=req.GET.get('employeesOfDepartment','-1'))
        
        template="<select class='small' name='to_employee' >\n\
        <option value='-1' selected>----</option>"
        if employees:
            for e in employees:
                template=template+"<option value='"+str(e.id)+"' >"+ps.empCodePrefix()+str(e.id)+'/'+e.firstName.title()+' '+e.lastName.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        
        template=template+"</select>"
        return HttpResponse(template)
    
    elif req.GET.get('popComplain',''):
        types=tbl_ticketType.objects.all()
        template="<select class='small' name='complaint_domain' >"
        if types:
            for d in types:
                if d.id==int(req.GET.get('popComplain','')):
                    template=template+"<option value='"+str(d.id)+"' selected>"+d.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(d.id)+"' >"+d.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    
    elif req.GET.get('popCompetitor',''):
        companies=tbl_competitor.objects.all()
        template="<select class='small' name='competitors' >\n\
        <option value='-1' selected>Select Company</option>"
        if companies:
            
            for c in companies:
                if c.id==int(req.GET.get('popCompetitor','')):
                    
                    template=template+"<option value='"+str(c.id)+"' selected>"+c.companyName+"</option>\n"
                else:
                    
                    template=template+"<option value='"+str(c.id)+"' >"+c.companyName+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('country',''):
        states=i_getAllStates(int(req.GET.get('country','')))
        template="<div class='selectWidth1' id='statediv'>\n<select class='full' name='state' onchange='getCity(this.value)'>\n\
        <option value='-1'> ---- </option>\n"
        if states:
            for s in states:
                template=template+"<option value='"+str(s.id)+"'>"+s.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('state',''):
        cities=i_getAllCities(int(req.GET.get('state','')))
        template="<div class='selectWidth1' id='citydiv'>\n<select class='small' name='city' onchange='getArea(this.value)'>\n<option value='-1' >Select City</option>"
        if cities:
            for c in cities:
                template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    
    elif req.GET.get('city',''):
        areas=i_getAllArea(int(req.GET.get('city','')))
        template="<div class='selectWidth1' id='areadiv'>\n<select class='small' name='area' >\n"
        if areas:
            for a in areas:
                template=template+"<option value='"+str(a.id)+"'>"+a.name.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    elif req.GET.get('source',''):
        subSources=i_getAllSubSources(int(req.GET.get('source','')))
        template='''<div class='selectWidth1' id='sub_source_div'>\n<select class='small' id='selectOfsubsource' name='subSource' onchange="setRecAmount(document.getElementById('received').value);">\n\
        <option value='-1'> Select Subsource </option>\n'''
        if subSources:
            for s in subSources:
                template=template+"<option value='"+str(s.id)+"'>"+s.categoryName.title()+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n</div>"
        return HttpResponse(template)
    
    elif req.GET.get('combo',''):
        
        byId=req.GET.get('combo','')
        temp=''
        for m in tbl_magazineCombo.objects.get(id=byId).magazines.all():
            temp=temp+str(m.id)+","
        temp=temp+"|"
        
        for s in tbl_scheme.objects.filter(magazineCombo=byId):
            temp=temp+str(s.id)+","
        temp=temp+"|"
        
        for g in tbl_scheme.objects.filter(magazineCombo=byId):
            temp=temp+str(g.gifts.id)+","
        return HttpResponse(temp)
    
    elif req.GET.get('magId',''):
        return HttpResponse(tbl_magazine.objects.get(id=req.GET.get('magId','')).price)
    
    elif req.GET.get('schemeAndTRA',''):
        '''this block return string that will be split at client side to set received amount 
           when scheme and totalReceievd amount is entered.
           dataString will have form like
           "id:displayprice:id:displayprice..... |commission discount|additional discount|other charges"
        '''
        
        scheme=tbl_scheme.objects.get(id=req.GET.get('schemeAndTRA','').split(',')[0])
        TRA=int(req.GET.get('schemeAndTRA','').split(',')[1])
        byAgent=False
        
        try:
            ms=tbl_source.objects.get(categoryName='telecaller').id
            ss=tbl_source.objects.get(id=req.GET.get('schemeAndTRA','').split(',')[2])
            if ss.pid!=ms:
                byAgent=True
        except:
            pass       
         
            
            
        if scheme.magazine:
            if TRA<=scheme.cost:
                data=str(scheme.magazine.id)+","+str(TRA)+":|"
            else:
                data=str(scheme.magazine.id)+","+str(scheme.cost)+":|"
        else:
            scheme.cost
            if TRA<=scheme.cost:
                calRec=[[m.id,int(round(TRA*(float(m.price)*100)/reduce(lambda x,y:x+y,[m.price for m in scheme.magazineCombo.magazines.all()])/100))] for m in scheme.magazineCombo.magazines.all()]
            else:
                calRec=[[m.id,int(round(scheme.cost*(float(m.price)*100)/reduce(lambda x,y:x+y,[m.price for m in scheme.magazineCombo.magazines.all()])/100))] for m in scheme.magazineCombo.magazines.all()]
            data=''
            for id,rec in calRec:
                data=data+str(id)+","+str(rec)+":"
            data=data+"|"
        
        if TRA<scheme.cost and byAgent:
            data=data+str(scheme.cost-TRA)+"|"
        else:
            data=data+'0'+'|'
        
        if TRA<scheme.cost and not byAgent:
            data=data+str(scheme.cost-TRA)+'|'
        else:
            data=data+'0'+'|'
            
        if TRA>scheme.cost:
            data=data+str(TRA-scheme.cost)+'|'
        else:
            data=data+'0'
            
        return HttpResponse(data)
    
    elif req.GET.get('scheme',''):
        schemeObj=tbl_scheme.objects.get(id=req.GET.get('scheme',''))
        schemeComboId=None
        schemeMagsId=None
        schemeGiftId=None
        schemeTenure=None
        
        discount=0
        totalMRP=0
        totalOffereMRP=0
        magsOfferPrice={}
        import math
        schemeTenure=schemeObj.tenure.timePeriod
        if schemeObj.gifts:
            schemeGiftId=schemeObj.gifts.id
        if schemeObj.magazineCombo:
            schemeComboId=schemeObj.magazineCombo.id
            schemeMagsId=[m.id for m in schemeObj.magazineCombo.magazines.all()]
            totalMRP=reduce(lambda x,y:x+y,[(m.price*schemeTenure) for m in schemeObj.magazineCombo.magazines.all()])
            
            PMP=[m.price for m in schemeObj.magazineCombo.magazines.all()]
            #offerPricesForShow=[str(round((percent*schemeObj.cost/100),1)).split('.')[0]+'.'+str(round((percent*5000/100),1)).split('.')[1][:2] for percent in [(float(price*100)/reduce(lambda x,y:x+y,PMP)) for price in PMP]]
            offerPricesForShow=[[m.id,str(int(round(schemeObj.cost*(float(m.price)*100)/reduce(lambda x,y:x+y,[m.price for m in schemeObj.magazineCombo.magazines.all()])/100)))] for m in schemeObj.magazineCombo.magazines.all()]
            for m,showprice in offerPricesForShow:
                magsOfferPrice[m]=showprice
            totalOffereMRP=schemeObj.cost
            discount=totalMRP-totalOffereMRP
            
                
            #sumOfOMRP=0
            #lastMag=None
            #for m in schemeObj.magazineCombo.magazines.all():
            #    sumOfOMRP=sumOfOMRP+int(magsOfferPrice[m.id])
            #    lastMag=m.id
                 
            #if sumOfOMRP<totalOffereMRP:
            #    magsOfferPrice[lastMag]=str(int(magsOfferPrice[lastMag])+(totalOffereMRP-sumOfOMRP))
                
        else:
            schemeMagsId=[schemeObj.magazine.id]
            totalMRP=(schemeObj.magazine.price*schemeTenure)
            totalOffereMRP=schemeObj.cost
            discount=totalMRP-totalOffereMRP
            magsOfferPrice={schemeObj.magazine.id:schemeObj.cost}
        
        gifts=i_getActiveGifts()
        combos=i_getActiveCombos()
        mags=i_getActiveMagazines()
        tenures=i_getActiveTenures()
        
        
        
        
        template="\
            <style>\n\
            define style here!\
            </style>\n\
            \n\n\n"
            
        
       
        
        
        
        '''_______________________________manage combo list__________________________'''
        
       
        
        
        
        
        
        
        
        
        
        '''
         template=template+"\n\n\
        <div class='section'>\n\
            <label>Magazine Combo</label>\n\
            <div class='selectWidth1'>\n\
                <select class='small' id='combo'  name='combo'>\n\
                <option value='-1' selected>Select Combo</option>\n"
        if combos:
            for c in combos:
                if c.id==schemeComboId:
                    template=template+"<option value='"+str(c.id)+"'selected>"+c.name.title()+"/"+c.code+"</option>\n"
                else:
                    template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"/"+c.code+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n\
            </div>\n\
        </div>\n"
        
        template=template+"\n\
        <div class='section'>\n\
            <label>Received Amount</label>\n\
            <div>\n\
            <input id='received' type='text' value='' onchange='setRecAmount(this.value);'/>\n\
            </div>\n\
        </div>"
        
        template=template+"\n\
        <div class='section'>\n\
            <label>Total Received Amount</label>\n\
            <div>\n\
            <input style='color:green;' type='text' value='' onchange='setRecAmount(this.value);'/>\n\
            </div>\n\
        </div>"
            
            
        
        template=template+"\n\n\
        <div class='section'>\n\
            <label>Magazine Combo</label>\n"
        if schemeObj.magazineCombo:
            template=template+"</select>\n\
            <input type='text' class='small' id='combo'  name='combo' readonly value='"+schemeObj.magazineCombo.name+"'/>\n"
        else:
            template=template+"</select>\n\
            <input type='text' class='small' id='combo'  name='combo' readonly value=''/>\n"
        
        template=template+"</select>\n\
        </div>\n"
        '''
        '''_______________________________manage amount section__________________________'''
        
        template=template+"\n\
        &nbsp;&nbsp;&nbsp;\n\
        <div class='section'>\n\
            <table width='100%' border='0' cellspacing='0' cellpadding='5' bordercolor='#cdcdcd' style='border-collapse:collapse'>\n\
                <tr class='tr_bg_list'>\n\
                    <td width=''>Compliment</td>\n\
                    <td width=''>Magazine</td>\n\
                    <td width=''>Select</td>\n\
                    <td width=''>Tenure</td>\n\
                    <td width=''>MRP Price</td>\n\
                    <td width=''>Offer Price</td>\n\
                    <td width=''>Received Amount</td>\n\
                </tr>\n"
        
        
        if mags:
            for i,m in enumerate(mags):
                template=template+"\n\
                <tr>\n\
                    <td><input name='com_c_"+str(m.id)+"' id='com_c_"+str(m.id)+"' type='checkbox'  value='1' ></td>\n"
                
                template=template+"\n\
                    <td>"+m.name.title()+"</td>\n"
                
                if m.id in schemeMagsId:
                    template=template+"\n\
                    <td><input name='c_"+str(m.id)+"' id='c_"+str(m.id)+"' type='checkbox'  value='1' checked></td>"
                else:
                    template=template+"\n\
                    <td><input name='c_"+str(m.id)+"' id='c_"+str(m.id)+"' type='checkbox'  value='1'></td>\n"
                template=template+"\n\
                <td>\n\
                <select class='small' name='t_"+str(m.id)+"' onchange='getMagEstimatedAmnt("+str(m.id)+",this.value,"+str(len(mags))+","+str((i+1))+");'>\n\
                            <option value='-1'  selected>Select Period</option>"
                if tenures:
                    for t in tenures:
                        if t.timePeriod==schemeTenure and m.id in schemeMagsId:
                            template=template+"\n\
                            <option value='"+str(t.timePeriod)+"' selected>"+str(t.name.title())+"</option>\n"
                        else:
                            template=template+"\n\
                            <option value='"+str(t.timePeriod)+"'>"+str(t.name.title())+"</option>\n"
                else:
                    template=template+"\n\
                    <option value='-1' > no periods found! </option>\n"
                template=template+"\n\
                </select>\n\
                </td>\n"
                if m.id in schemeMagsId:
                    template=template+"\n\
                    <td><input type='text' id='estimatedAmount_"+str((i+1))+"_"+str((i+1))+"' name='estAmnt_"+str(m.id)+"' value='"+str((schemeTenure*m.price))+"' class='subs_txtbox' readonly/></td>\n\
                    <td><input type='text' style='color:red;' name='realAmount_"+str(m.id)+"' id='realAmount_"+str((i+1))+"_"+str((i+1))+"'  value='"+str(magsOfferPrice[m.id])+"' class='subs_txtbox'  onchange='calcSUMRA("+str(len(mags))+");'/></td>\n\
                    <td><input type='text' style='color:green;' name='recAmount_"+str(m.id)+"' id='recAmount_"+str((i+1))+"_"+str((i+1))+"'  value='' class='subs_txtbox'  onchange='calcSUMRecA("+str(len(mags))+");'/></td>\n"
                else:
                    template=template+"\n\
                    <td><input type='text' id='estimatedAmount_"+str((i+1))+"_"+str((i+1))+"' name='estAmnt_"+str(m.id)+"' value='' class='subs_txtbox' readonly/></td>\n\
                    <td><input type='text' style='color:red;' name='realAmount_"+str(m.id)+"' id='realAmount_"+str((i+1))+"_"+str((i+1))+"'  value='' class='subs_txtbox'  onchange='calcSUMRA("+str(len(mags))+");'/></td>\n\
                    <td><input type='text' style='color:green;' name='recAmount_"+str(m.id)+"' id='recAmount_"+str((i+1))+"_"+str((i+1))+"'  value='' class='subs_txtbox'  onchange='calcSUMRecA("+str(len(mags))+");'/></td>\n"    
                    
                template=template+"\n\
                </tr>\n"
        else:
            template=template+"\n\
                <tr style='background:lightcyan;' >\n\
                    <td colspan='7' align='center'>no magazines found !</td>\n\
                </tr>"
        
        template=template+"\n\
                <tr style='background:lightcyan;'>\n\
                    <td colspan='4' align='right'><label>Offer Discount</label></td>\n\
                    <td align='left'><input  name='discount' id='discount' value='"+str(discount)+"' type='text'/></td>\n\
                    <td colspan='1' align='right'><label>Total MRP Price</label></td>\n\
                    <td><input name='sumOfEAmnt'  id='SumOfEAmnt' type='text' value='"+str(totalMRP)+"' readonly/></td>\n\
                </tr>\n\
                \n\
                \n\
                <tr style='background:lightcyan;'>\n\
                    <td colspan='4' align='right'><label>Comission Discount</label></td>\n\
                    <td align='left'><input name='comdiscount' type='text' id='comdis' value=''/></td>\n\
                    <td colspan='1' align='right' ><label>Total Subscription Price</label></td>\n\
                    <td><input style='color:red;' name='sumOfRAmnt' id='SumOfRAmnt' type='text' value='"+str(totalOffereMRP)+"'readonly/></td>\n\
                </tr>\n\
                \n\
                \n\
                <tr style='background:lightcyan;'>\n\
                    <td colspan='4' align='right'><label>Additional Discount</label></td>\n\
                    <td align='left'><input name='addiscount' type='text' id='addis' value='' /></td>\n\
                    <td colspan='1' align='right'><label>Total Received Amount</label></td>\n\
                    <td><input style='color:green;' name='sumOfRecAmnt' id='SumOfRecAmnt' type='text' value='' onchange='setRecAmount(this.value);' readonly/></td>\n\
                </tr>\n\
                \n\
                \n\
                <tr style='background:lightcyan;'>\n\
                    <td colspan='4' align='right'><label>Other Charges</label></td>\n\
                    <td align='left' colspan='3'><input name='ocharges' id='ocharge' type='text' value='' /></td>\n\
                </tr>\n\
        </table>\n\
        </div>\n"
         
        '''_______________________________manage gift list__________________________'''
        template=template+"\
        <div class='section' >\n\
            <label>gift</label>\n\
            <div class='selectWidth1' id='giftdiv'>\n\
            <select class='small'  id='selectofgifts' name='sgifts' multiple>\n"
        
        if gifts:
            for g in gifts:
                if g.id==schemeGiftId:
                    template=template+"<option value='"+str(g.id)+"'selected>"+g.name.title()+"/"+g.code+"</option>\n"
                else:
                    template=template+"<option value='"+str(g.id)+"'>"+g.name.title()+"/"+g.code+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n\
            </div>\n\
        </div>\n"
   
        return HttpResponse(template)
    
    
    
    elif req.GET.get('changeCombo',''):
        template="<select class='small' name='combo'>\n\
        <option value='-1' selected>Select Combo</option>"
        combos=i_getActiveCombos()
        if combos:
            for c in combos:
                if c.id==int(req.GET.get('changeCombo','')):
                    template=template+"<option value='"+str(c.id)+"'selected>"+c.name.title()+"/"+c.code+"</option>\n"
                else:
                    template=template+"<option value='"+str(c.id)+"'>"+c.name.title()+"/"+c.code+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('changeTenure',''):
        #return HttpResponse('you have passed: '+req.GET.get('changeTenure',''))
        idAndPeriod=req.GET.get('changeTenure','').split(',')
        magid=int(idAndPeriod[0])
        period=int(idAndPeriod[1])
        mags=tbl_magazine.objects.filter(isActive=True)
        id_in_template=[i for i,m in enumerate(mags) if m.id==magid][0]+1
        if magid and period:
            template="\
            <style>\
            define style here!\
            </style>\
            "
            template=template+"<select  class='small' name='t_"+str(magid)+"' onchange='getMagEstimatedAmnt("+str(magid)+",this.value,"+str(mags.count())+","+str(id_in_template)+");'>\n\
             <option value='-1'  selected>Select Period</option>"
            tenures=i_getActiveTenures()
            if tenures:
                for t in tenures:
                    if period==t.timePeriod:
                        template=template+"<option value='"+str(t.timePeriod)+"'selected>"+t.name.title()+"</option>\n"
                    else:
                        template=template+"<option value='"+str(t.timePeriod)+"'>"+t.name.title()+"</option>\n"
            else:
                template=template+"<option value='-1'> not found !</option>\n"
            template=template+"</select>"
            return HttpResponse(template)
    
    
    elif req.GET.get('getMagIds',''):
        magazines=tbl_magazine.objects.filter(isActive=True)
        temp=''
        for m in magazines:
            temp=temp+str(m.id)+','
        return HttpResponse(temp)
    
    
    
    elif req.GET.get('setRecs',''):
        ''' this method will receive selected mags that are checked without scheme'''
        
        selectedMags=[tbl_magazine.objects.get(id=mid) for mid in req.GET.get('setRecs','').split(':')[0].split(',')]
        TRA=int(req.GET.get('setRecs','').split(':')[1])
        offerCost=int(req.GET.get('setRecs','').split(':')[3])
        #scheme=tbl_scheme.objects.get(id=req.GET.get('schemeAndTRA','').split(',')[0])
        #TRA=int(req.GET.get('schemeAndTRA','').split(',')[1])
        byAgent=False
        
        try:
            ms=tbl_source.objects.get(categoryName='telecaller').id
            ss=tbl_source.objects.get(id=req.GET.get('setRecs','').split(':')[2])
            if ss.pid!=ms:
                byAgent=True
        except:
            pass       
         
            
        if TRA<=offerCost:
            calRec=[[m.id,int(round(TRA*(float(m.price)*100)/reduce(lambda x,y:x+y,[m.price for m in selectedMags])/100))] for m in selectedMags]
        else:
            calRec=[[m.id,int(round(offerCost*(float(m.price)*100)/reduce(lambda x,y:x+y,[m.price for m in selectedMags])/100))] for m in selectedMags]
        data=''
        for id,rec in calRec:
            data=data+str(id)+","+str(rec)+":"
        data=data+"|"
        
        if TRA<offerCost and byAgent:
            data=data+str(offerCost-TRA)+"|"
        else:
            data=data+'0'+'|'
        
        if TRA<offerCost and not byAgent:
            data=data+str(offerCost-TRA)+'|'
        else:
            data=data+'0'+'|'
            
        if TRA>offerCost:
            data=data+str(TRA-offerCost)+'|'
        else:
            data=data+'0'
            
        return HttpResponse(data)
    elif req.GET.get('popMagazine',''):
        magazines=tbl_magazine.objects.filter(isActive=True)
        template="<select class='small' name='magazine' >\n\
        <option value='-1' selected>Select Magazine</option>"
        if magazines:
            for m in magazines:
                if m.id==int(req.GET.get('popMagazine','')):
                    template=template+"<option value='"+str(m.id)+"' selected>"+m.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(m.id)+"' >"+m.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('popTenure',''):
        tenures=tbl_tenure.objects.filter(isActive=True)
        template="<select class='small' name='tenure' >\n\
        <option value='-1' selected>Select Tenure</option>"
        if tenures:
            for t in tenures:
                if t.id==int(req.GET.get('popTenure','')):
                    template=template+"<option value='"+str(t.id)+"' selected>"+t.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(t.id)+"' >"+t.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('popGift',''):
        gifts=tbl_gift.objects.filter(isActive=True)
        template="<select class='small' name='gift' >\n\
        <option value='-1' selected>Select Gift</option>"
        if gifts:
            for g in gifts:
                if g.id==int(req.GET.get('popGift','')):
                    template=template+"<option value='"+str(g.id)+"' selected>"+g.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(g.id)+"' >"+g.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('popRole',''):
        roles=tbl_role.objects.filter(isActive=True)
        template="<select class='small' name='role' >\n\
        <option value='-1' selected>Select Role</option>"
        if roles:
            for r in roles:
                if r.id==int(req.GET.get('popRole','')):
                    template=template+"<option value='"+str(r.id)+"' selected>"+r.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(r.id)+"' >"+r.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
       
    elif req.GET.get('popDepartment',''):
        departments=tbl_departments.objects.filter(isActive=True)
        template="<select class='small' name='department' >\n\
        <option value='-1' selected>Select Department</option>"
        if departments:
            for d in departments:
                if d.id==int(req.GET.get('popDepartment','')):
                    template=template+"<option value='"+str(d.id)+"' selected>"+d.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(d.id)+"' >"+d.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('popBranch',''):
        branches=tbl_branch.objects.filter(isActive=True)
        template="<select class='small' name='branch' >\n\
        <option value='-1' selected>Select Branch</option>"
        if branches:
            for b in branches:
                if b.id==int(req.GET.get('popBranch','')):
                    template=template+"<option value='"+str(b.id)+"' selected>"+b.name+"</option>\n"
                else:
                    template=template+"<option value='"+str(b.id)+"' >"+b.name+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>"
        return HttpResponse(template)
    elif req.GET.get('popSource',''):
        template=''
        mainSources=tbl_source.objects.filter(isActive=True,pid=0)
        msId=tbl_source.objects.get(id=int(req.GET.get('popSource',''))).pid
        subSources=tbl_source.objects.filter(isActive=True,pid=msId)
        template=template+"\n\
        <div class='section' >\n\
                   <label>Main Source <sup>*</sup></label>\n\
                   <div class='selectWidth1'>\n\
                   <table border='0'>\n\
                       <tr>\n\
                           <td>\n\
                               <select class='small'  name='source'  onchange='getSubSources(this.value);'>\n\
                                   <option value='-1'  selected>Select Main Source</option>"
        if mainSources:
            for ms in mainSources:
                if ms.id==msId:
                    template=template+"<option value='"+str(ms.id)+"' selected>"+ms.categoryName+"</option>\n"
                else:
                    template=template+"<option value='"+str(ms.id)+"' >"+ms.categoryName+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n\
                            </td>\n\
                            <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n\
                            <td><a href='' onclick='return openURLInCenterOfScreen('/add/source');'><img src='{% static 'images/icon_addlink.gif' %}'></a></td>\n\
                        </tr>\n\
                    </table>\n\
                    </div>\n\
        </div>\n\
        <div class='section'>\n\
            <label>Sub source <sup>*</sup></label>\n\
            <div class='selectWidth1'  id='sub_source_div' >\n\
                <select class='small'  name='subSource' id='selectOfsubsource'>\n\
                    <option value='-1' selected >Select Subsource</option>"
        
        if subSources:
            for ss in subSources:
                if ss.id==int(req.GET.get('popSource','')):
                    template=template+"<option value='"+str(ss.id)+"' selected>"+ss.categoryName+"</option>\n"
                else:
                    template=template+"<option value='"+str(ss.id)+"' >"+ss.categoryName+"</option>\n"
        else:
            template=template+"<option value='-1'> not found !</option>\n"
        template=template+"</select>\n\
            </div>\n\
        </div>"
        return HttpResponse(template)
       
          