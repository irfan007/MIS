from django.shortcuts import render_to_response
from misApp.pp import i_getMagazine, i_getMagazineByCode, i_getActiveAdminUser,\
    i_getRole, i_getEmployee, i_hasPermission
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from misApp.models import tbl_magazine, tbl_employee, tbl_taskList, tbl_tenure,\
    tbl_log, tbl_gift, tbl_role, tbl_permission, tbl_departments, tbl_location,\
    tbl_branch, tbl_source, tbl_competitor, tbl_ticketType, tbl_contentType
from views.magazine import work_for_magazine_log
from django.template.context import RequestContext
from misApp.views import workfortoDoList, v_allTaskList


def v_popUp(req,option):
    
    #return HttpResponse(option)
    if option=="complaintype":
        if req.POST.get('addComplaintType',''):
            errors=[]
            
            name=req.POST.get('name').strip()
            if not name:
                errors.append('please enter name !')
            else:
                c=tbl_ticketType.objects.create(name=name)
                temp="\n\
                    <script>\n\
                    try{\n\
                        window.opener.setPopComplain("
                temp=temp+str(c.id)+")\n\
                        window.close();\n\
                        }catch(error){alert(error);}\n\
                    </script>"
                return HttpResponse(temp)
        
                
        return render_to_response('popComplaintType.html',locals(),context_instance=RequestContext(req))
    
    elif option=="Competitor" and i_hasPermission(i_getEmployee(req.session.get('username','')),'com','a'):
        
    
        if req.POST.get('addCompetitor',''):
            errors=[]
            name=req.POST.get('name','').strip()
            
            description=req.POST.get('description','').strip()
            status=req.POST.get('status','')
            if not name:
                errors.append("Please enter the name!")
            
            
            
        
            dupname=tbl_competitor.objects.filter(companyName=name)
            
            if dupname:
                errors.append("Please enter the different name,this name already exist!")
            
            if errors:
                return render_to_response('popCompet.html',locals())
                
            
            
            p1=tbl_competitor(companyName=name,description=description)
            p1.save()
            
             
            temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopCompetitor("
            temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
            return HttpResponse(temp)
    
        
        
        return render_to_response('popCompet.html',locals())  
    
    
    elif option=='source' and i_hasPermission(i_getEmployee(req.session.get('username','')),'source','a'):
        
        categories=tbl_source.objects.filter(pid__lt=1)
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('addnewcategory',''):
            errors=[]
            newcategory=req.POST.get('addcategory','').strip()
            if not newcategory:
                errors.append("Please enter the value!")
                return render_to_response('popSource.html',{'errors':errors,'newcategoryname':newcategory,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
            
            existedNameObj=tbl_source.objects.filter(categoryName=newcategory)
            if existedNameObj:
                errors.append("Please enter the different category name!")
                return render_to_response('popSource.html',{'errors':errors, 'newcategoryname':newcategory,\
                                                        'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
            
            p1=tbl_source(categoryName=newcategory,pid=0,isActive=True)
            p1.save()
            
            return render_to_response('popSource.html',{'categories':categories,'alltask':alltask},context_instance=RequestContext(req))    
        
        elif req.POST.get('addSource',''):
            errors=[]
            status=req.POST.get('status','')
            name=req.POST.get('name','').strip()
            category=req.POST.get('category','')
            category=int(category)
            if(category==-1):
                errors.append('Please choose the category!')
            if len(str(name))<1:
                errors.append('Please enter the name!')
       
            if errors:
                return render_to_response('popSource.html',{'errors':errors,'category':category,'name':name,\
                                                        'status':status,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
            existedNameObj=tbl_source.objects.filter(categoryName=name)
            
            if existedNameObj:
                errors.append("Please enter different name or information!")
                return render_to_response('popSource.html',{'name':name,'category':category,'errors':errors,\
                                                        'status':status,'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
            if(status=="1"):
                isActive=True
            else:
                isActive=False    
            
            p1=tbl_source(categoryName=name,pid=category,isActive=isActive)
            p1.save()
            temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopSource("
            temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
            return HttpResponse(temp)    
        else:
            return render_to_response('popSource.html',{'categories':categories,'alltask':alltask},context_instance=RequestContext(req))
    elif option=='branch' and i_hasPermission(i_getEmployee(req.session.get('username','')),'branch','a'):
        
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        getstates=tbl_location.objects.filter(pid=1)
    
        if req.POST.get('addBranch',''):
            errors=[]
            code=req.POST.get('code','').strip()
            
            name=req.POST.get('name','').strip()
            contactno=req.POST.get('contactno','').strip()
            description=req.POST.get('description','').strip()
            getstate=int(req.POST.get('state',''))
            getcities=tbl_location.objects.filter(pid=getstate)
            getcity=int(req.POST.get('city',''))
            address=req.POST.get('address','').strip()
            pincode=req.POST.get('pincode','').strip()
            status=req.POST.get('status','')
            if contactno:
                try:
                    contactno=int(contactno)
                except:
                    errors.append("Please enter valid contact no!")
            if pincode:
                try:
                    pincode=int(pincode)
                except:
                    errors.append("Please enter the valid pincode!")
            status=req.POST.get('status','')
            if not code:
                errors.append("Please enter the code!")
            
            if not name:
                errors.append("Please enter the name!")
            if getstate==-1:
                errors.append("Please select the state!")
            if getcity==-1:
                errors.append("Please select the city!")
            if not address:
                errors.append("Please enter the address!")
            
        
            dupcode=tbl_branch.objects.filter(code=code)
            
            if dupcode:
                errors.append("Please enter the different code,this code already exist!")
            dupname=tbl_branch.objects.filter(name=name)
            if dupname:
                errors.append("Please enter the different name,this name already exist!")
            if errors:
                return render_to_response('popBranch.html',locals(),context_instance=RequestContext(req))
            if status=="1":
                isActive=True
            else:
                isActive=False    
            
            branchstate=tbl_location.objects.get(id=getstate)
            branchcity=tbl_location.objects.get(id=getcity)
            p1=tbl_branch(name=name,code=code,description=description,state=branchstate.name,city=branchcity.name,\
            isActive=isActive,address=address,pincode=pincode,contactno=contactno)
            p1.save()
            p2=tbl_log(tbl_name='branch',rowid=p1.id,newdata='code='+p1.code+'\n'+'name='+p1.name+'\n'+'description='+p1.description+'\n'+\
                   'contact='+str(p1.contactno)+'\n'+'state='+p1.state+'\n'+'city='+p1.city+'\n'\
                   +'address='+p1.address+'\n'+'pincode='+str(p1.pincode)+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
            p2.save()
            temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopBranch("
            temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
            return HttpResponse(temp)
    
        return render_to_response("popBranch.html",locals(),context_instance=RequestContext(req))
        
    elif option=='department' and i_hasPermission(i_getEmployee(req.session.get('username','')),'department','a'):
        
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('addDepartment',''):
            errors=[]
            status=req.POST.get('status','')
            description=req.POST.get('description','').strip()
            name=req.POST.get('name','').strip()
        
            
            if not name:
                errors.append('Please enter the name!')
        
        
            existedName=tbl_departments.objects.filter(name=name)
            if existedName:
                errors.append("This name already exists!")
            if errors:
                return render_to_response('popDepartment.html',{'errors':errors,'name':name,'description':description,\
                                                            'status':status,'alltask':alltask},context_instance=RequestContext(req))
            else:
                if(status=="1"):
                    isActive=True
                else:
                    isActive=False    
            
                p1=tbl_departments(name=name,description=description,isActive=isActive)
                p1.save()
                p2=tbl_log(tbl_name='department',rowid=p1.id,newdata='name='+p1.name+'\n'+'description='+p1.description+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
                p2.save()
                temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopDepartment("
                temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
                return HttpResponse("<p>"+temp+"</p>")
        else:
            return render_to_response('popDepartment.html',locals(),context_instance=RequestContext(req))
    

    elif option=='role' and i_hasPermission(i_getEmployee(req.session.get('username','')),'role','a'):
        

        MAP=[]
        oldcat=None
        for c in tbl_contentType.objects.filter(isActive=True).order_by('category'):
            if c.category==oldcat:
                MAP.append(['',c.name,0,0,0,0])
            else:
                MAP.append([c.category,c.name,0,0,0,0])
                oldcat=c.category
        
        


        if req.POST.get('addRole',''):
            errors=[]
            name=req.POST.get('name',None).strip()
            desc=req.POST.get('desc','').strip()
            active=req.POST.get('active',False)
            
            if not name:
                errors.append("please enter role name !")
            elif name and tbl_role.objects.filter(name=name):
                errors.append("Role with this name already exist !")
            
            for i,row in enumerate(MAP):
                MAP[i][2]=int(req.POST.get(row[1]+'_v',0))
                MAP[i][3]=int(req.POST.get(row[1]+'_a',0))
                MAP[i][4]=int(req.POST.get(row[1]+'_u',0))
                MAP[i][5]=int(req.POST.get(row[1]+'_d',0))
            
                
    #            if not [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
    #                errors.append("please check at least one check box !")        
            
            if not errors:
                #return HttpResponse((tbl_systemUser.objects.get(username=req.session['username']).id))
                role=tbl_role.objects.create(name=name,description=desc,assignedBy=(tbl_employee.objects.get(username=req.session['username']).id),isActive=bool(active))
                for r in [r for r in MAP if r[2]==1 or r[3]==1 or r[4]==1 or r[5]==1 ]:
                    c=tbl_contentType.objects.get(name=r[1])
                    p=tbl_permission.objects.create(content=c,view=r[2],add=r[3],update=r[4],delete=r[5])
                    role.permissions.add(p)
                
                temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopRole("
                temp=temp+str(role.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
                return HttpResponse("<p>"+temp+"</p>")            
            return render_to_response('popRole.html',locals(),context_instance=RequestContext(req))
        return render_to_response('popRole.html',locals(),context_instance=RequestContext(req)) 
    
    
    elif option=='gift' and i_hasPermission(i_getEmployee(req.session.get('username','')),'gift','a'):
        
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('addGift',''):
            name=req.POST.get('name','').strip()
            description=req.POST.get('description','').strip()
            status=req.POST.get('status','')
            quantity=req.POST.get('quantity','')
        
            code=req.POST.get('code','').strip()
            errors=[]
            if not name:
                errors.append('Please enter the name!')
            if not code:
                errors.append('Please enter the code!')
            existedname=tbl_gift.objects.filter(name=name)
            if existedname:
                errors.append("Please enter different name!")
            existedcode=tbl_gift.objects.filter(code=code)
            if existedcode:
                errors.append("Please enter different code!")
            if quantity:
                try:
                    quantity=int(quantity)
                except:
                    errors.append("Please enter valid quantity!")
        
                    
            if errors:
                return render_to_response('popGift.html',locals(),context_instance=RequestContext(req))
                
            else:
                if not quantity:
                    quantity=0
                if(status=="1"):
                    isActive=True
                else:
                    isActive=False
                p1=tbl_gift(code=code,name=name,description=description,isActive=isActive,stockQuantity=quantity,updated=quantity)
                p1.save()
                p2=tbl_log(tbl_name='gift',rowid=p1.id,newdata='code='+p1.code+'\n'+'name='+p1.name+'\n'+'description='+p1.description+\
                       '\n'+'InitialQuantity='+str(p1.stockQuantity)+'\n'+'UpdatedQuantity='+str(p1.updated)+'\n'+'status='+str(p1.isActive),action="Add",username=req.session['username'])
                p2.save()
                temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopGift("
                temp=temp+str(p1.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
                return HttpResponse("<p>"+temp+"</p>")
        else:
            return render_to_response('popGift.html',locals(),context_instance=RequestContext(req))
    
    
    
    elif option=='tenure' and i_hasPermission(i_getEmployee(req.session.get('username','')),'tenure','a'):
        
        workfortoDoList(req)
        empobj=tbl_employee.objects.get(username=req.session['username'])
        alltask=tbl_taskList.objects.filter(isActive=True,username=empobj)
        errors=[]
        
        if req.POST.get('addtenure',''):
            name=req.POST.get('name','').strip()
            timePeriod=req.POST.get('period','').strip()
            status=req.POST.get('status','')
       
            if not timePeriod:
                errors.append("Please enter time period!")
            else:
                try:
                    timePeriod=int(timePeriod)
                except:
                    errors.append("Please enter valid time period!")   
            if not name:
                errors.append('Please enter the name!')
                dupname=tbl_tenure.objects.filter(name=name)
                if dupname:
                    errors.append("Please enter the different name!")
            try:
                duplicate_rows=tbl_tenure.objects.filter(timePeriod=timePeriod)
                if duplicate_rows:
                    errors.append("Please enter the different time period!")
            except:
                pass           
            
            if errors:
                return render_to_response('popTenure.html',{'errors':errors,'timePeriod':timePeriod,'name':name,\
                                                        'status':status,'alltask':alltask},context_instance=RequestContext(req))
            if(status=="1"):
                isActive=True
            else:
                isActive=False
            try:
                timePeriod=int(timePeriod)
            except:
                timePeriod=0           
            row=tbl_tenure(name=name,timePeriod=timePeriod,isActive=isActive)
            row.save()
            p2=tbl_log(tbl_name='tenure',rowid=row.id,newdata='name='+row.name+'\n'+'Time='+str(row.timePeriod)+'\n'+'status='+str(row.isActive),action="Add",username=req.session['username'])
            p2.save()
            temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopTenure("
            temp=temp+str(row.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
            return HttpResponse("<p>"+temp+"</p>")
            
        return render_to_response('popTenure.html',locals(),context_instance=RequestContext(req))
        
    elif option=='magazine' and i_hasPermission(i_getEmployee(req.session.get('username','')),'magazine','a'):
        
        if req.POST.get('addMagazine',''):
            errors=[]
            
            name=req.POST.get('name','').strip()
            code=req.POST.get('code','').strip()
            price=req.POST.get('price','').strip()
            startdate=req.POST.get('startdate','').strip()
            enddate=req.POST.get('enddate','').strip()
            active=req.POST.get('active','')
            if active=='1':
                active=True
            
                                       
            if name:
                if i_getMagazine(name):
                    errors.append("this magazine name is already exist !")
            else:
                errors.append("please enter a name !")
            
                            
            if code:
                if i_getMagazineByCode(code):
                    errors.append("this magazine code is already exist !")
            else:
                errors.append("please enter a code name !")
            
                
            if price:
                try:
                    int(price)
                except ValueError:
                    errors.append("Invalid value found for field price !")
            else:    
                errors.append("please enter a price !")
            
            
            
                
            #----------------------
            
                
            if len(startdate)>0:
                try:
                    datetime.datetime.strptime(startdate,'%d-%m-%Y')
                    
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
                    flag=False
            
                            
            if len(enddate)>0:
                try:
                    datetime.datetime.strptime(enddate,'%d-%m-%Y')
                except ValueError:
                    errors.append("Invalid value found for field startDate !")
                    flag=False
            
            
            if enddate and not startdate:
                errors.append('Please enter startDate first !')
            
            flag=True    
            if startdate and enddate and flag:
                datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                if datetime.datetime.strptime(startdate,'%d-%m-%Y')==datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('StartDate and endDate can not be same !')
                elif datetime.datetime.strptime(startdate,'%d-%m-%Y')>datetime.datetime.strptime(enddate,'%d-%m-%Y'):
                    errors.append('EndDate must be greater than startDate !')
            
                             
            
            
            if not errors:
                
                if len(startdate)==0:
                    startdate=None
                    
                if len(enddate)==0:
                    enddate=None
                    
                if not startdate and enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=None,
                                            endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                                            isActive=active
                                            )
                    work_for_magazine_log(req,magazinelog)
                elif startdate and not enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y'),
                                            endDate=None,
                                            isActive=active
                                            )
                    work_for_magazine_log(req,magazinelog)
                elif startdate and enddate:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=datetime.datetime.strptime(startdate,'%d-%m-%Y'),
                                            endDate=datetime.datetime.strptime(enddate,'%d-%m-%Y'),
                                            isActive=active
                                            )
                    work_for_magazine_log(req,magazinelog)
                else:
                    magazinelog=tbl_magazine.objects.create(
                                            name=name,
                                            code=code,
                                            price=price,
                                            startDate=None,
                                            endDate=None,
                                            isActive=active
                                            )
                    work_for_magazine_log(req,magazinelog)
                temp="\n\
                <script>\n\
                try{\n\
                    window.opener.setPopMagazine("
                temp=temp+str(magazinelog.id)+")\n\
                    window.close();\n\
                    }catch(error){alert(error);}\n\
                </script>"
                return HttpResponse("<p>"+temp+"</p>")
            
            return render_to_response('popMagazine.html',locals(),context_instance=RequestContext(req))
        return render_to_response('popMagazine.html',locals(),context_instance=RequestContext(req))
    