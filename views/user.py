from misApp.models import ProjectScope, tbl_employee, tbl_departments, tbl_role,\
    tbl_location
from misApp.pp import i_getActiveAdminUser, i_getAllEmployeesNA,\
    i_getActiveRoles, i_getActiveDepartments, i_getEmployeesCount,\
    i_getAllStates, i_getEmployee, i_getEmployeeByEmail, upload, i_hasPermission
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from misApp.views import workfortoDoList, v_allTaskList

def v_user(req,url):
    
    options=url.split('/')
    emppre=ProjectScope().empCodePrefix()
    if options[0]=='list' and i_hasPermission(i_getEmployee(req.session.get('username','')),'employee','v'):
        workfortoDoList(req)
        alltask=v_allTaskList(req)
        if req.POST.get('submit_query',''):
            getparam=req.POST.get('passing_parameter','')
            employees=tbl_employee.objects.filter(isAdmin=False,username__icontains=getparam).order_by('id')
            return render_to_response('employeeList.html',locals(),context_instance=RequestContext(req))
            
        employees=i_getAllEmployeesNA()
        
        return render_to_response('employeeList.html',locals(),context_instance=RequestContext(req))
    elif options[0]=='add' and i_hasPermission(i_getEmployee(req.session.get('username','')),'employee','a'):
            roles=i_getActiveRoles()
            departments=i_getActiveDepartments()
            empid=i_getEmployeesCount()+1
            states=i_getAllStates(1)
            if req.POST.get('addUser',''):
                errors=[]
                (username,password,email,designation,role,active,department,name,mobileno,address,city,state,imagePath)=('','','','',-1,False,-1,'','','',None,None,None)
                countryName=None
                username=req.POST.get('username','').strip()
                password=req.POST.get('password','').strip()
                cpassword=req.POST.get('cpassword','').strip()
                email=req.POST.get('email','').strip()
                designation=req.POST.get('designation','').strip()
                role=int(req.POST.get('role',''))
                active=req.POST.get('active','')
                department=int(req.POST.get('department',''))
                name=req.POST.get('name','').strip()
                mobileno=req.POST.get('mobileno','').strip()
                address=req.POST.get('address','').strip()
                #country=req.POST.get('country','')
                state=int(req.POST.get('state',''))
                city=int(req.POST.get('city',''))
                if state!=-1:
                    cities=tbl_location.objects.filter(pid=int(state))
                    
                
                if active==1:
                    active=True
                
                #-----------------cleaning done----------------
                if len(username)==0:
                    errors.append("please enter a username !")
                elif not 5 <= len(username) <= 15:
                    errors.append("username length should be between 5-15 characters !")
                elif i_getEmployee(username):
                    errors.append("this username is already exist !")
                
                elif len(password)==0:
                    errors.append("please enter a password !")
                elif not 5 <= len(password) <= 15:
                    errors.append("password length should be between 5-15 characters !")
                elif not password==cpassword:
                    errors.append("both password fields must be match !")
                
                elif '@' not in email:
                    errors.append("please enter a valid email address !")
                elif i_getEmployeeByEmail(email):
                    errors.append("this email ID is already registered !")
                
                elif len(designation)==0:
                    errors.append("please enter a designation !")
                elif role==-1:
                    errors.append("please select atleast one role !")
                elif department==-1:
                    errors.append("please select atleast one department !")
                
                    
                elif len(mobileno)!=0 and len(mobileno)!=10:
                    errors.append("please enter a valid mobile no. !")
                elif True:
                    temp=None
                    try:
                        #temp="role";role=int(role)
                        #temp="active";active=int(active)
                        #temp="department";department=int(department)
                        if mobileno:
                            temp="contact";mobileno=int(mobileno)
                    except ValueError:
                        if temp:
                            errors.append('Invalid value found for field '+temp+' !')
                    
                    
                    if req.FILES.get('image'):
                        imagePath=upload(req.FILES['image'],username+'.jpeg')
                        
                if not errors:
                    if state!=-1:
                        state=tbl_location.objects.get(id=int(state))
                        country=tbl_location.objects.get(id=int(1))
                    else:
                        state=None
                        country=None
                    
                    if city!=-1:
                        city=tbl_location.objects.get(id=int(city))
                    else:
                        city=None
                        
                    tbl_employee.objects.create(username=username,
                                                password=password,
                                                email=email,
                                                department=tbl_departments.objects.get(id=int(department)),
                                                designation=designation,
                                                role=tbl_role.objects.get(id=int(role)),
                                                isActive=active,
                                                firstName=name,
                                                mobileNo=mobileno,
                                                address=address,
                                                city=city,
                                                country=country,
                                                state=state,
                                                image=imagePath,
                                                )
                    return HttpResponseRedirect('/user/list')
                return render_to_response('addEmployee.html',locals(),context_instance=RequestContext(req))     
            return render_to_response('addEmployee.html',locals(),context_instance=RequestContext(req))
        
        
        
    elif options[0]=='edit' and options[1] and i_hasPermission(i_getEmployee(req.session.get('username','')),'employee','u'):
            roles=i_getActiveRoles()
            departments=i_getActiveDepartments()
            states=i_getAllStates(1)
            emp=tbl_employee.objects.get(id=int(options[1]))
            (username,password,email,designation,role,active,department,name,mobileno,address,city,state,imagePath)=(emp.username,emp.password,emp.email,emp.designation,emp.role.id,emp.isActive,emp.department.id,'','','',None,None,None)
            imageName=None
            state=None
            if emp.image:
                imageName=emp.image.url.split('/')[1]
                imagePath=emp.image.url
            if emp.firstName:
                name=emp.firstName
            if emp.mobileNo:
                mobileno=emp.mobileNo
            if emp.address:
                address=emp.address
            
            if emp.image:
                image=emp.image
            if emp.state:
                state=emp.state.id
                cities=tbl_location.objects.filter(pid=state)
            if emp.city:
                city=emp.city.id
            
            if req.POST.get('editUser',''):
                errors=[]
                username=req.POST.get('username','').strip()
                password=req.POST.get('password','').strip()
                cpassword=req.POST.get('cpassword','').strip()
                email=req.POST.get('email','').strip()
                designation=req.POST.get('designation','').strip()
                role=int(req.POST.get('role',''))
                active=req.POST.get('active','')
                department=int(req.POST.get('department',''))
                name=req.POST.get('name','').strip()
                mobileno=req.POST.get('mobileno','').strip()
                address=req.POST.get('address','').strip()
                #country=req.POST.get('country','')
                state=int(req.POST.get('state',''))
                city=int(req.POST.get('city',''))
                if state!=-1:
                    cities=tbl_location.objects.filter(pid=int(state))
                    
                if active=='1':
                    active=True
                
                #----------------------------------    
                if len(username)==0:
                    errors.append("please enter a username !")
                elif not 5 <= len(username) <= 15:
                    errors.append("username length should be between 5-15 characters !")
                elif i_getEmployee(username) and i_getEmployee(username).username!=emp.username:
                    errors.append("this username is already exist !")
                
                elif len(password)==0:
                    errors.append("please enter a password !")
                elif not 5 <= len(password) <= 15:
                    errors.append("password length should be between 5-15 characters !")
                elif emp.password!=password and not password==cpassword:
                    errors.append("both password fields must be match !")
                
                elif '@' not in email:
                    errors.append("please enter a valid email address !")
                elif i_getEmployeeByEmail(email) and i_getEmployeeByEmail(email).email!=emp.email:
                    errors.append("this email ID is already registered !")
                
                elif len(designation)==0:
                    errors.append("please enter a designation !")
                elif role==-1:
                    errors.append("please select atleast one role !")
                elif department==-1:
                    errors.append("please select atleast one department !")
                elif len(mobileno)!=0 and len(mobileno)!=10:
                    errors.append("please enter a valid mobile no. !")
                elif True:
                    temp=None
                    try:
                        #temp="role";role=int(role)
                        #temp="active";active=int(active)
                        #temp="department";department=int(department)
                        if mobileno:
                            temp="contact";mobileno=int(mobileno)
                    except ValueError:
                        if temp:
                            errors.append('Invalid value found for field '+temp+' !')
                    
                    if req.FILES.get('image'):
                        imagePath=upload(req.FILES['image'],username+'.jpeg')
                
                
                        
                    
                
                    
                
                #-----------------done----------------
                    
                if not errors:
                    if state!=-1:
                        state=tbl_location.objects.get(id=int(state))
                        country=tbl_location.objects.get(id=int(1))
                    else:
                        state=None
                        country=None
                
                    if city!=-1:
                        city=tbl_location.objects.get(id=int(city))
                    else:
                        city=None
                
                    emp.username=username
                    emp.password=password
                    emp.email=email
                    emp.designation=designation
                    emp.role=tbl_role.objects.get(id=role)
                    emp.isActive=active
                    emp.department=tbl_departments.objects.get(id=department)
                    emp.firstName=name
                    emp.mobileNo=mobileno
                    emp.address=address
                    emp.city=city    
                    emp.state=state
                    emp.country=country
                    emp.image=imagePath
                    
                    emp.save()
                    return HttpResponseRedirect('/user/list')
                return render_to_response('editEmployee.html',locals(),context_instance=RequestContext(req))     
            return render_to_response('editEmployee.html',locals(),context_instance=RequestContext(req))
            
