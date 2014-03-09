from django.db import models

import datetime
from django.utils.dateformat import DateFormat
from MIS.settings import uploadFolder


# Create your models here.
class ProjectScope:
    '''
    SPP / no. of Subscription Per Page would be shown
    SBRPP / no. of Subscriber Per Page
    '''
    SPP=20
    SBRPP=10
    TICKET_PREFIX='00'
    FOLLOWUP_PREFIX='00'
    
    def getDate(self):
        return datetime.datetime.today()
    def dDate(self):
        return DateFormat(self.getDate()).format('d M Y')
    def getSubPrefix(self):
        '''
        this is an subscription code prefix
        '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        return "SUB000"
        
    def getComplaintPrefix(self):
        '''
        this is an subscription code prefix
        '''
        return "CMP000"
        
    def empCodePrefix(self):
        return "EMP000"

    def getCustomerPrefix(self):
        return "C000"
    
    def onlyDate(self):
        return DateFormat(self.getDate()).format('d-m-Y')

#---------------------MODELS------------------------------------------------------




class tbl_events(models.Model):
    username=models.CharField(max_length=25)
    event=models.TextField(null=True,blank=True)
    startDate=models.DateTimeField(null=True,blank=True)
    endDate=models.DateTimeField(null=True,blank=True)
    fgColor=models.CharField(max_length=10)
    bgColor=models.CharField(max_length=10)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    def __unicode__(self):
        return "%s-%s"%(self.username,self.event)



class tbl_magazinePeriod(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    daysPeriod=models.IntegerField(default=0)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s-%s"%(str(self.id),self.name,str(self.daysPeriod))


class tbl_branch(models.Model):
    code=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=12,null=True,blank=True)
    description=models.CharField(max_length=150,null=True,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
    city=models.CharField(max_length=20,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    isActive=models.BooleanField(default=True)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s-%s"%(self.id,self.code,self.name)
    
class tbl_log(models.Model):
    tbl_name=models.CharField(max_length=20,null=True,blank=True)
    rowid=models.IntegerField(null=True,blank=True)
    olddata=models.TextField(null=True,blank=True)
    newdata=models.TextField(null=True,blank=True)
    action=models.CharField(max_length=15,null=True,blank=True)
    remarks=models.CharField(max_length=50,null=True,blank=True)
    datetime=models.DateTimeField(default=ProjectScope().getDate())
    username=models.CharField(max_length=25,null=True,blank=True)
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def __unicode__(self):
        return "%s-%s"%(self.id,self.remarks)
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def getDate(self):
        try:
            x=datetime.datetime.strptime(str(self.datetime.date()), '%Y-%m-%d')
            return x.strftime('%d-%m-%Y')
        except:
            return ''


class tbl_giftHistory(models.Model):
    giftid=models.IntegerField(default=0,null=True,blank=True)
    reason=models.TextField(null=True,blank=True)
    date=models.DateField(default=ProjectScope().getDate().date)
    quantity=models.IntegerField(default=0)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
       
    def __unicode__(self):
        return "%s-%s"%(self.id,self.reason)
      
class tbl_location(models.Model):
    name=models.CharField(max_length=100)
    pid=models.IntegerField(null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    type=models.CharField(max_length=2,null=True,blank=True)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s-%s"%(self.id,self.name,self.pid)
           



class tbl_departments(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    
    
    isActive=models.BooleanField(default=False)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)




class tbl_contentType(models.Model):
    category=models.CharField(max_length=100)
    name=models.CharField(max_length=100,unique=True)
    isActive=models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s %s %s'%(self.id,self.category,self.name) 
    

class tbl_permission(models.Model):
    content=models.ForeignKey(tbl_contentType)
    view=models.BooleanField(default=False)
    add=models.BooleanField(default=False)
    update=models.BooleanField(default=False)
    delete=models.BooleanField(default=False)
    
    createdOn=models.DateField(default=datetime.date.today())
    updatedOn=models.DateField(default=datetime.date.today())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=datetime.date.today()
    def __unicode__(self):
        return "%s-%s- View/%s - Add/%s - Update/%s - Delete/%s "%(self.id,self.content,self.view,self.add,self.update,self.delete)

class tbl_role(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    permissions=models.ManyToManyField(tbl_permission,null=True,blank=True)
    assignedBy=models.IntegerField(null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    createdOn=models.DateField(default=datetime.date.today())
    updatedOn=models.DateField(default=datetime.date.today())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=datetime.date.today()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)




class tbl_employee(models.Model):
    
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=100,unique=True)
    
    department=models.ForeignKey(tbl_departments,null=True,blank=True)
    designation=models.CharField(max_length=100,null=True,blank=True)
    role=models.ForeignKey(tbl_role,null=True,blank=True)
    
    title_choice=(('m','Mr.'),('f','Mrs.'))
    sex_choice=(('m','Male'),('f','Female'))
    title=models.CharField(max_length=5,choices=title_choice,null=True,blank=True)
    firstName=models.CharField(max_length=30,null=True,blank=True)
    lastName=models.CharField(max_length=30,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    sex=models.CharField(max_length=1,choices=sex_choice,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    city=models.ForeignKey(tbl_location,related_name='forCity',null=True,blank=True)
    state=models.ForeignKey(tbl_location,related_name='forState',null=True,blank=True)
    country=models.ForeignKey(tbl_location,related_name='forCountry',null=True,blank=True)
    pin=models.CharField(max_length=50,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    mobileNo=models.CharField(max_length=10,null=True,blank=True)
    image=models.ImageField(upload_to=str(DateFormat(ProjectScope().getDate()).format('dmY')),null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    isAdmin=models.BooleanField(default=False)
       
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "EMP ID:%s"%(self.id)
    def getImageURL(self):
        if self.image:
            return uploadFolder+self.image.url

    def getEmpId(self):
        return ProjectScope().empCodePrefix()+str(self.id)    
    

class tbl_taskList(models.Model):
    username=models.ForeignKey(tbl_employee,null=True,blank=True)
    completedDate=models.DateTimeField(default=ProjectScope().getDate())
    description=models.TextField(null=True,blank=True)
    isActive=models.BooleanField(default=True)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.description)

class tbl_magazine(models.Model):
    '''
    code - MGCODE
    '''
    code=models.CharField(max_length=50,null=True,blank=True)
    name=models.CharField(max_length=50,unique=True)
    price=models.IntegerField(default=0)
    startDate=models.DateField(null=True,blank=True)
    endDate=models.DateField(null=True,blank=True)
    isActive=models.BooleanField(default=False)
    magPeriodType=models.ForeignKey(tbl_magazinePeriod,null=True,blank=True)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)

    
class tbl_magazineCombo(models.Model):
    
    name=models.CharField(max_length=50,unique=True)
    code=models.CharField(max_length=50,null=True,blank=True,unique=True)
    description=models.TextField(null=True,blank=True)
    magazines=models.ManyToManyField(tbl_magazine)
    price=models.IntegerField(default=0,null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)
    def magComboPrice(self):
        x=0
        unique=tbl_magazineCombo.objects.get(id=self.id)
        for item in unique.magazines.all():
            x=x+item.price
        return x 

class tbl_tenure(models.Model):
    '''
    tenureFor values can be:
    sc for scheme
    sb for subscription
     '''
   
   
    name=models.CharField(max_length=50,blank=True,null=True)
    timePeriod=models.IntegerField()
    
    isActive=models.BooleanField(default=False)

    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.name,self.timePeriod)
    '''def getType(self):
        if self.tenureFor=='sc':
            return 'Scheme'
        else:
            return 'Subscription'
            ''' 
class tbl_gift(models.Model):
    code=models.CharField(unique=True,max_length=50)
    name=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    stockQuantity=models.IntegerField(default=0)
    updated=models.IntegerField(default=0)
    isActive=models.BooleanField(default=False)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
       
    def __unicode__(self):
        return "%s-%s"%(self.code,self.name)
class tbl_source(models.Model):
   
   
    categoryName=models.CharField(max_length=50)
    pid=models.IntegerField()
    isActive=models.BooleanField(default=False)

    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.categoryName)

    def getParentCategory(self):
        try:
            obj=tbl_source.objects.get(id=self.pid)
            return obj.categoryName
        except:
            pass


class tbl_scheme(models.Model):
    name=models.CharField(max_length=50)
    magazine=models.ForeignKey(tbl_magazine,null=True,blank=True)
    magazineCombo=models.ForeignKey(tbl_magazineCombo,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    cost=models.IntegerField()
    tenure=models.ForeignKey(tbl_tenure)
    gifts=models.ForeignKey(tbl_gift,null=True,blank=True)
    startDate=models.DateField(null=True,blank=True)
    endDate=models.DateField(null=True,blank=True)
    isActive=models.BooleanField(default=False)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
       
    def __unicode__(self):
        
        if self.magazine:
            return "%s-%s-%s"%(self.id,self.name,self.magazine.name)
        else:
            return "%s-%s-%s"%(self.id,self.name,self.magazineCombo.name)
   
    def getshortdescription(self):
        return self.description[:20] 
    def getmagazinename(self):
        try:
            obj=tbl_magazine.objects.get(id=self.magazine.id)
            return obj.name
        except:
            return "None"
    def getmagazineComboname(self):
        try:
            obj=tbl_magazineCombo.objects.get(id=self.magazineCombo.id)
            return obj.name
        except:
            return "None"
    def getenddate(self):
        try:
            return str(self.endDate)
        except:
            return "None"
    def getstartDate(self):
        try:
            return str(self.startDate)
        except:
            return "None"
    def getgiftname(self):
        try:
            obj=tbl_gift.objects.get(id=self.gifts.id)
            return obj.name
        except:
            return ""            





class tbl_competitor(models.Model):
    companyName=models.CharField(max_length=25,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s"%(self.companyName)

class tbl_compMagazine(models.Model):
    companyName=models.IntegerField(null=True,blank=True)
    magName=models.CharField(max_length=25,null=True,blank=True)
    coverPrice=models.IntegerField(default=0)
    issueType=models.CharField(max_length=25,null=True,blank=True)
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s"%(self.magName)
    def getCompanyName(self):
        try:
            return tbl_competitor.objects.get(id=self.companyName).companyName
        except:
            return ''
   
class tbl_compMagOffer(models.Model):
    compMagazine=models.IntegerField(null=True,blank=True)
    oldPrice=models.IntegerField(default=0)
    month=models.IntegerField(null=True,blank=True)
    year=models.IntegerField(null=True,blank=True)
    duration=models.CharField(max_length=25,null=True,blank=True)
    mrp=models.IntegerField(default=0)
    noofIssues=models.IntegerField(default=0)
    subsPrice=models.IntegerField(default=0)
    offers=models.TextField(null=True,blank=True)   
    remark=models.CharField(max_length=25,null=True,blank=True)
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s"%(self.id)
class tbl_supportedCourier(models.Model):
    code=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    isActive=models.BooleanField(default=True)

    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate() 
    def __unicode__(self):
        return "%s-%s"%(self.id,self.name)

class tbl_dispatch(models.Model):
    '''
    MIS has only two dispatched Items each has associated values for itemType
    for magazine : itemType=m
    for gift     : itemType=g
    
    itemCode
    if itemType is magazine,itemCode will contain unique id of magazine
    if itemType is gift,itemCode will contain unique id of gift
    
    status values can be
    >inprocess='i'
    >hold='h'
    >dispatched='d'    
    '''
    itemTypes=(('m','Magazine'),('g','gift'))
    
    customerId=models.IntegerField()
    subId=models.IntegerField(null=True,blank=True)
    dispatchDate=models.DateField(null=True,blank=True)
    courierNo=models.CharField(max_length=100,null=True,blank=True)
    receivedBy=models.CharField(max_length=50,null=True,blank=True)
    receivedDate=models.DateField(null=True,blank=True)
    receiverContact=models.CharField(max_length=10,null=True,blank=True)
    dispatchAddress1=models.TextField(null=True,blank=True)
    dispatchAddress2=models.TextField(null=True,blank=True)
    issueMonth=models.IntegerField(null=True,blank=True)#only for magazine
    issueYear=models.IntegerField(null=True,blank=True)#only for magazine
    courierType=models.ForeignKey(tbl_supportedCourier,null=True,blank=True)
    status=models.CharField(max_length=5,null=True,blank=True)
    itemType=models.CharField(max_length=3,choices=itemTypes)
    itemCode=models.IntegerField(null=True,blank=True)
    quantity=models.IntegerField(default=1,null=True,blank=True)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
        
    def getItemName(self):
        try:
            if self.itemType=='m':
                return tbl_magazine.objects.get(id=self.itemCode).name
            elif self.itemType=='g':
                return tbl_gift.objects.get(id=self.itemCode).name
        except:
            return None
    def getIssueMonth(self):
        Mon={1:'Jan',2:'Feb',3:'March',4:'April',5:'May',6:'June',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
        return Mon[self.issueMonth] 
    def getIssueYear(self):
        return self.issueYear
    def getStatus(self):
        try:
            if self.status=='i':
                return "IN PROCESS"
            elif self.status=='h':
                return "ON HOLD"
            elif self.status=='d':
                return "DISPATCHED"
        except:
            return None
    def __unicode__(self):
        if self.itemType=="m":
            return "%s-%s-%s-%s-%s-%s"%(self.id,self.itemType,self.getItemName(),self.issueMonth,self.issueYear,self.getStatus())
        elif self.itemType=="g":
            return "%s-%s-%s-%s"%(self.id,self.itemType,self.getItemName(),self.getStatus())
            
class tbl_subscription(models.Model):
    '''
    date - DTENTRY
    period -  PERIOD
    magazine - tbl_magazineObj
<<<<<<< HEAD
    subAmnt - AMOUNT
    recAmnt - AMT1
=======
  subAmnt - AMOUNT
  recAmnt - AMT1
>>>>>>> 2804549d27cbb57a6f8444cdb6ff92a8ab4d6c53
    isCompliment -( if AMOUNT and AMT1 is 0 or blank )
    isSuspend - not exist
    suspendDate - not exist
   issues - STISS/ENISS (is advance subscription possible)
   rIssues - not exist
   isActive - (ENISS GREATER THAN CURRENT YEAR and month)
  
    >>>>>>>>>>>>>>>>>>>>>>>>-most important<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    when inserting data in this table 
    also insert data in tbl_dispatch 
    1st for gift
    nth times for magazine n=total no. of month magazine subscribe
    -------------------------------------------------------------------------------
    period is always in >>>>MONTHS<<<<
    
    rIssues(remaining no. of isssues)
    
    issues hold magazine issued and remains in format like below so that i could parse string to dictionary object for calculation purpose
    issues="'2013,3':0,'2013,4':0,'2013,5':1"
    here "'2013,3':0" shows single issue detail as "'issue year,issue month':issue status(0 not issued/1 issued)"
    '''
    
    cId=models.IntegerField(null=True,blank=True)
    cName=models.CharField(max_length=100,null=True,blank=True)
    cCity=models.CharField(max_length=100,null=True,blank=True)
    
    date=models.DateField(null=True,blank=True,default=ProjectScope().getDate())
    period=models.IntegerField()
    magazine=models.ForeignKey(tbl_magazine,null=True,blank=True) 
    subAmnt=models.IntegerField(null=True,blank=True,default=0)
    recAmnt=models.IntegerField(null=True,blank=True,default=0)
    
    
    isCompliment=models.BooleanField(default=False)
    isSuspend=models.BooleanField(default=False)
    suspendDate=models.DateField(null=True,blank=True,default=ProjectScope().getDate())
    
    issues=models.TextField(null=True,blank=True)
    rIssues=models.IntegerField(null=True,blank=True)
    
    isActive=models.BooleanField(default=False)
    
    def __unicode__(self):
        return "SUB ID-%s"%(self.id)
    def getsubID(self):
        return ProjectScope().getSubPrefix()+str(self.id)
    def getBranchId(self):
        uniquecus=tbl_customer.objects.get(subscriptions=self.id)
        if uniquecus.branch==None:
            return ''
        else:
            return uniquecus.branch.name
    def getCourierId(self):
        uniquecus=tbl_customer.objects.get(subscriptions=self.id)
        if uniquecus.courier==None:
            return ''
        else:
            return uniquecus.courier.name


class tbl_transaction(models.Model):
    '''payment details
    
    date -  DTENTRY
    
    payMode can be
    for credit/debit card ='cd'
    for cash ='c'
    for draft='d'
    cheque='chq'
    ANEFT='a'
    online='o'
    outstanding='out'
    complimentary='com'
    
    
    subid will be comma separated values
    '''
    date=models.DateField(null=True,blank=True,default=ProjectScope().getDate())
    amount=models.IntegerField(null=True,blank=True,default=0)
    OSAmnt=models.IntegerField(null=True,blank=True,default=0)
    subId=models.CharField(null=True,blank=True,max_length=200)
    payMode=models.CharField(max_length=5,null=True,blank=True)
    chequeDate=models.DateField(null=True,blank=True)
    chequeNo=models.CharField(max_length=50,null=True,blank=True)
    bankName=models.CharField(max_length=100,null=True,blank=True)
    depositeDate=models.DateField(null=True,blank=True)
    clearDate=models.DateField(null=True,blank=True)
    
    
    dis=models.IntegerField(null=True,blank=True,default=0)
    comdis=models.IntegerField(null=True,blank=True,default=0)
    addis=models.IntegerField(null=True,blank=True,default=0)
    oCharges=models.IntegerField(null=True,blank=True,default=0)
    
    def getPaymentMode(self):
        if self.payMode=='c':
            return "Cash"
        elif self.payMode=='d':
            return "Draft"
        elif self.payMode=='chq':
            return "Cheque"
        elif self.payMode=='a':
            return "NEFT"
        elif self.payMode=='o':
            return "Online"
        elif self.payMode=='out':
            return "Outstanding"
            
    def __unicode__(self):
        return "ID:%s-SUBID:%s-RA:%s-MODE:%s"%(self.id,self.subId,self.amount,self.payMode)

    def getSubs(self):
        temp=''
        if self.subId:
            for sub in self.subId.split(',')[:-1]:
                temp=temp+ProjectScope().getSubPrefix()+sub+','
            if temp=='':
                return ProjectScope().getSubPrefix()+self.subId
            else:
                return temp[:-1]
        
    
    def CDL(self):
        '''return C heque D ate L abel based on type'''
        if self.payMode=='c':
            return "RECEIPT DATE"
        elif self.payMode=='d':
            return "DD DATE"
        elif self.payMode=='chq':
            return "CHEQUE DATE"
        elif self.payMode=='a':
            return "NEFT DATE"
        elif self.payMode=='o':
            return "TRANSACTION DATE"
    def CNL(self):
        '''return C heque N umber L abel based on type'''
        if self.payMode=='c':
            return "RECEIPT NO."
        elif self.payMode=='d':
            return "DD NO."
        elif self.payMode=='chq':
            return "CHEQUE NO."
        elif self.payMode=='a':
            return "NEFT NO."
        elif self.payMode=='o':
            return "TRANSACTION NO."
    def DDL(self):
        '''return D eposite D ate  L abel based on type'''
        
        if self.payMode=='d':
            return "DD DEPOSITE DATE"
        elif self.payMode=='chq':
            return "CHEQUE DEPOSITE DATE"
        elif self.payMode=='a':
            return "NEFT DEPOSITE DATE"
    
    def CLDL(self):
        '''return C L earanc D ate  L abel based on type'''
        
        if self.payMode=='d':
            return "DD CLEARANCE DATE"
        elif self.payMode=='chq':
            return "CHEQUE CLEARANCE DATE"
        elif self.payMode=='a':
            return "TRANSACTION TRANSFERRED DATE"
        
    
        
class tbl_customer(models.Model):
    '''
                        MIGRATION 
    title -  PREFIX
    firstName - FNAME
    lastName - LNAME
   DOB - 
    age - AGE
    sex - SEX
    designation - DESIG1,DESIG2,DESIG
    company - COMPANY
    address1 - ADD1
    address2 - ADD2
    address3 - ADD3
    state - STATE
    city - CITY
    pincode -  PINCODE
    tel_O - TEL_O
    tel_R - TEL_R
    mobileNo - MOBILE cases(9971259656,09341975164,9447577770-71,001-4084629042,9899099042/43,918056262626)
    email - EMAIL
    '''
    title_choice=(('m','Mr.'),('f','Mrs.'),('mis','Miss'),('d','Dr.'),('o','Other'))
    sex_choice=(('m','Male'),('f','Female'))
    
    subscriptions=models.ManyToManyField(tbl_subscription)
    transactions=models.ManyToManyField(tbl_transaction,null=True,blank=True)
    scheme=models.ManyToManyField(tbl_scheme,null=True,blank=True)
    gift=models.ManyToManyField(tbl_gift,null=True,blank=True)
    combo=models.ForeignKey(tbl_magazineCombo,null=True,blank=True)
    branch=models.ForeignKey(tbl_branch,null=True,blank=True)
    courier=models.ForeignKey(tbl_supportedCourier,null=True,blank=True)
    
    TSAmnt=models.IntegerField(null=True,blank=True,default=0)
    TRAmnt=models.IntegerField(null=True,blank=True,default=0)
    
    subSource=models.ForeignKey(tbl_source,null=True,blank=True)
    empId=models.IntegerField(null=True,blank=True)
    
    
    title=models.CharField(max_length=5,choices=title_choice,null=True,blank=True)
    firstName=models.CharField(max_length=50,null=True,blank=True)
    lastName=models.CharField(max_length=50,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    sex=models.CharField(max_length=5,choices=sex_choice,null=True,blank=True)
    designation=models.CharField(max_length=100,null=True,blank=True)
    company=models.CharField(max_length=100,null=True,blank=True)
    address1=models.CharField(max_length=100)
    address2=models.CharField(max_length=100,null=True,blank=True)
    address3=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    tel_O=models.CharField(max_length=20,null=True,blank=True)
    tel_R=models.CharField(max_length=20,null=True,blank=True)
    mobileNo=models.CharField(max_length=20,null=True,blank=True)
    email=models.CharField(max_length=100)
    
    isActive=models.BooleanField(default=False)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "ID:%s-%s-%s"%(self.id,self.firstName,self.email)
    def getTitle(self):
        if self.title=='m':
            return "Mr."
        elif self.title=='f':
            return "Mrs."
        elif self.title=='d':
            return "Dr."
        elif self.title=='mis':
            return "Miss."
        elif self.title=='o':
            return ""
    
    def getcusID(self):
        return ProjectScope().getCustomerPrefix()+str(self.id)
    
class tbl_history(models.Model):
    
    '''contain only active subscription history
                                                                  use delimiter ':'
    type 
    m-magazine(conversion) data=oldmagazine/startDate/endDate/period::newmagazine/startDate/endDate/period
    c-combo    data=combo/startDate/endDate
    sch-scheme data=scheme/startDate/endDate 
    g-gift     data=gift/oldscheme
    p-period   data=oldmagazine/oldPeriod 
    sou-source data=magazine/subSourceId
    <not required pay-payment data=oldmodecode/subAmnt/recAmnt/chequeDate/chequeDDNo./bank/checkqueDeposit/clearenceDate/>
    can-cancel(cancellation)  data=magazine/startDate
    
    sus-suspend  data=suspend Date / resumed Date / suspend Period(in month) / SubstartDate / old subEnddate /  old Period / new period /  Newsub End date  
    '''
    Mon={1:'Jan',2:'Feb',3:'March',4:'April',5:'May',6:'June',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    date=models.DateField(null=True,blank=True,default=ProjectScope().getDate())
    data=models.TextField(null=True,blank=True)
    custId=models.IntegerField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)
    type=models.CharField(null=True,blank=True,max_length=5)
    
    def m_OM(self):
        try:
            return self.data.split('::')[0].split(':')[0]
        except:
            pass
    
    def m_OSI(self):
        
        try:
            dl=self.data.split('::')[0].split(':')[1].split('-')
            return self.Mon[int(dl[1])]+" "+dl[0]
        except:
            pass
    
    def m_OEI(self):
        
        try:
            dl=self.data.split('::')[0].split(':')[2].split('-')
            return self.Mon[int(dl[1])]+" "+dl[0]
        except:
            pass
        
    
    def m_OP(self):
        try:
            return self.data.split('::')[0].split(':')[3]
        except:
            pass
    
    def m_NM(self):
        try:
            return self.data.split('::')[1].split(':')[0]
        except:
            pass
    
    def m_NSI(self):
        
        try:
            dl=self.data.split('::')[1].split(':')[1].split('-')
            return self.Mon[int(dl[1])]+" "+dl[0]
        except:
            pass
    
    def m_NEI(self):
        
        try:
            dl=self.data.split('::')[1].split(':')[2].split('-')
            return self.Mon[int(dl[1])]+" "+dl[0]
        except:
            pass
    
    def m_NP(self):
        try:
            return self.data.split('::')[1].split(':')[3]
        except:
            pass
    '''---------------------------suspend------------'''
    def sus_SD(self):
        '''suspend Date'''
        try:
            y_m_d=self.data.split(":")[0].split('-')
            return self.Mon[int(y_m_d[1])]+" "+y_m_d[2]+", "+y_m_d[0]
        except:
            try:
                return tbl_subscription.objects.get(id=self.subId).suspendDate
            except:
                pass
            
            
    
    def sus_RD(self):
        '''resume Date'''
        try:
            y_m_d=self.data.split(":")[1].split('-')
            return self.Mon[int(y_m_d[1])]+" "+y_m_d[2]+", "+y_m_d[0]
        except:
            pass
    def sus_P(self):
        '''suspend period'''
        try:
            return self.data.split(":")[2]
        except:
            pass
    
    def sus_SSD(self):
        '''subscription start Date'''
        try:
            y_m_d=self.data.split(":")[3].split('-')
            return self.Mon[int(y_m_d[1])]+" "+y_m_d[2]+", "+y_m_d[0]
        except:
            pass
    
    def sus_OED(self):
        '''subscription start Date'''
        try:
            y_m_d=self.data.split(":")[4].split('-')
            return self.Mon[int(y_m_d[1])]+" "+y_m_d[2]+", "+y_m_d[0]
        except:
            pass
    
    def sus_OP(self):
        '''old period'''
        try:
            return self.data.split(":")[5]
        except:
            pass
    def sus_NP(self):
        '''New period'''
        try:
            return self.data.split(":")[6]
        except:
            pass
    
    def sus_NED(self):
        '''New End Date'''
        try:
            y_m_d=self.data.split(":")[7].split('-')
            return self.Mon[int(y_m_d[1])]+" "+y_m_d[2]+", "+y_m_d[0]
        except:
            pass
    def getmagazinename(self):
        try:
            getsub=tbl_subscription.objects.get(id=self.subId)
            return getsub.magazine.name
        except:
            pass
    def __unicode__(self):
        return "Type:%s"%(self.type)    
    


class tbl_complaint(models.Model):
    '''
    status can be
    new="n"
    under process="u"
    resolved="r"
    
    '''
    subId=models.IntegerField(null=True,blank=True)
    empId=models.IntegerField(null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    description=models.TextField(max_length=100,null=True,blank=True)
    status=models.CharField(max_length=10,null=True,blank=True)
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
            
    def __unicode__(self):
        return "ID:%s-%s"%(self.id,self.subId)
    def getComplaintNo(self):
        return ProjectScope().getComplaintPrefix()+str(self.id)
    def getDepartment(self):
        if tbl_employee.objects.get(id=self.empId).department:
            return tbl_employee.objects.get(id=self.empId).department.name
        else:
            "----"
    def getEmployeeId(self):
        return ProjectScope().empCodePrefix()+str(self.empId)
    def getStatus(self):
        if self.status=='n':
            return "NEW"
        elif self.status=='u':
            return "UNDER PROCESS"
        elif self.status=='r':
            return "RESOLVED"
    def getSubId(self):
        return ProjectScope().getSubPrefix() + str(self.subId)
    
    
    


class tbl_ticketType(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        return "%s"%(self.name)
class tbl_followUp(models.Model):
    '''
    subId has taken for reverse lookup 
    
    if this is first followup then 
    transferedBy=-1
    '''
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    by=models.IntegerField(null=True,blank=True)
    #transferedBy=models.IntegerField(null=True,blank=True)
    reply=models.TextField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return "%s"%(self.reply)



class tbl_transfer(models.Model):
    date=models.DateTimeField(default=ProjectScope().getDate())
    by=models.IntegerField(null=True,blank=True)
    to=models.IntegerField(null=True,blank=True)
    department=models.ForeignKey(tbl_departments,null=True,blank=True)
    
    def __unicode__(self):
        return "ID:%s - by:%s - to:%s - dpt:%s"%(self.id,self.by,self.to,self.department.name)
class tbl_ticket(models.Model):
    '''
    status can be
    new            =n
    under process  =u
    resolved       =r
    
    
    
    resource can be
    phone     =p
    email     =e
    letter    =l    
    other     =o
    
    '''
    createdBy=models.IntegerField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)
    
    complaint=models.TextField(null=True,blank=True)
    type=models.ForeignKey(tbl_ticketType,null=True,blank=True)
    resource=models.CharField(max_length=5,null=True,blank=True)
    status=models.CharField(max_length=5,null=True,blank=True)
    
    currentFollower=models.IntegerField(null=True,blank=True)
    currentDepartment=models.ForeignKey(tbl_departments,null=True,blank=True)
    
    followUps=models.ManyToManyField(tbl_followUp,null=True,blank=True)
    transferRecord=models.ManyToManyField(tbl_transfer,null=True,blank=True)
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    
    
    
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def hasSubscriberName(self):
        return tbl_subscription.objects.get(id=self.subId).cName
    def hasStatus(self):
        status={'n':'NEW','u':'IN PROCESS','r':'RESOLVED'}
        return status[self.status]
    def hasResource(self):
        resource={'p':'PHONE','e':'EMAIL','l':'LETTER','o':'OTHER'}
        return resource[self.resource]

    def __unicode__(self):
        return "TICKET NO.:%s"%(self.id)

    
    
class tbl_contact(models.Model):
    '''
    follow up status can be
    new               =n
    in follow up      =i
    close             =c
    become lead       =l
    
    
    NOTE:
    subid when contact created through existing subscription
    
    '''
    title_choice=(('m','Mr.'),('f','Mrs.'),('mis','Miss'),('d','Dr.'),('o','Other'))
    sex_choice=(('m','Male'),('f','Female'))
    
    title=models.CharField(max_length=5,choices=title_choice,null=True,blank=True)
    firstName=models.CharField(max_length=50,null=True,blank=True)
    lastName=models.CharField(max_length=50,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    sex=models.CharField(max_length=5,choices=sex_choice,null=True,blank=True)
    designation=models.CharField(max_length=100,null=True,blank=True)
    company=models.CharField(max_length=100,null=True,blank=True)
    address1=models.CharField(max_length=100)
    address2=models.CharField(max_length=100,null=True,blank=True)
    address3=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    tel_O=models.CharField(max_length=20,null=True,blank=True)
    tel_R=models.CharField(max_length=20,null=True,blank=True)
    mobileNo=models.CharField(max_length=20,null=True,blank=True)
    email=models.CharField(max_length=100)
    
    
    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    createdBy=models.IntegerField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)
    
    status=models.CharField(max_length=5,null=True,blank=True)
    currentFollower=models.IntegerField(null=True,blank=True)
    
    followUps=models.ManyToManyField(tbl_followUp,null=True,blank=True)
    
    
    
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def hasStatus(self):
        status={'n':'NEW','i':'IN FOLLOW-UP','c':'CLOSED','l':'BECOME LEAD'}
        return status[self.status]

#-----------------------------------------------------------------------------------------END NEW CRM    

    

    

class tbl_renewal(models.Model):
    '''
    type
    a-advance renewal/extend
    r-renewal 
    periods=if advance(oldPeriod-extend-newPeriod) if renewal(oldPeriod-newPeriod)
    when advance renewal magazines,periods,mrps,subAmnts,recAmnts will contain only single values for subscription  which is extending 
    '''
    date=models.DateField(null=True,blank=True,default=ProjectScope().getDate())
    custId=models.IntegerField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)
    type=models.CharField(null=True,blank=True,max_length=2)
    
    magazines=models.CharField(null=True,blank=True,max_length=500)
    periods=models.CharField(null=True,blank=True,max_length=100)
    mrps=models.CharField(null=True,blank=True,max_length=300)
    subAmnts=models.CharField(null=True,blank=True,max_length=300)
    recAmnts=models.CharField(null=True,blank=True,max_length=300)
    
    dis=models.CharField(null=True,blank=True,max_length=100)
    comdis=models.CharField(null=True,blank=True,max_length=100)
    addis=models.CharField(null=True,blank=True,max_length=100)
    scheme=models.CharField(null=True,blank=True,max_length=500)
    gift=models.CharField(null=True,blank=True,max_length=500)
    subSource=models.CharField(null=True,blank=True,max_length=100)
    empid=models.CharField(null=True,blank=True,max_length=100)
    
    #payMode=models.CharField(max_length=5,null=True,blank=True)
    #checkDate=models.CharField(null=True,blank=True)
    #checkNo=models.CharField(max_length=50,null=True,blank=True)
    #bankName=models.CharField(max_length=100,null=True,blank=True)
    #depositeDate=models.DateField(null=True,blank=True)
    #clearDate=models.DateField(null=True,blank=True)
    
    TSAmnt=models.CharField(null=True,blank=True,max_length=100)
    TRAmnt=models.CharField(null=True,blank=True,max_length=100)
    
    
    def __unicode__(self):
        return "Type:%s"%(self.type)
    def getSchemes(self):
        if self.scheme:
            return self.scheme.replace(':',',')[:-1]
        else:
            return '----'
    def getGifts(self):
        if self.gift:
            return self.gift.replace(':',',')[:-1]
        else:
            return '----'
    def OP(self):
        try:
            return self.periods.split('-')[0]
        except:
            pass
    def NP(self):
        try:
            return self.periods.split('-')[2]
        except:
            pass
    def EP(self):
        try:
            return self.periods.split('-')[1]
        except:
            pass
    
    '''_______________for type='r'_______________'''
    def r_OM(self):
        try:
            return self.magazines.split(':')[0]
        except:
            pass
    def r_OP(self):
        try:
            return self.periods.split(':')[0]
        except:
            pass
        
    def r_OMRP(self):
        try:
            return self.mrps.split(':')[0]
        except:
            pass    
        
    def r_OSAmnt(self):
        try:
            return self.subAmnts.split(':')[0]
        except:
            pass
    
    def r_ORAmnt(self):
        try:
            return self.recAmnts.split(':')[0]
        except:
            pass
    
    def r_ODis(self):
        try:
            temp=self.dis.split(':')[0]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass

    def r_OCDis(self):
        try:
            temp=self.comdis.split(':')[0]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_OADis(self):
        try:
            temp=self.addis.split(':')[0]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_OScheme(self):
        try:
            temp=self.scheme.split('-')[0].replace(':',',')[:-1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_OGift(self):
        try:
            temp=self.gift.split('-')[0].replace(':',',')[:-1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass

    def r_OSource(self):
        try:
            return self.subSource.split(':')[0]
        except:
            pass
    
    def r_OEmpId(self):
        try:
            temp=self.empid.split(':')[0]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_OTSAmnt(self):
        try:
            return self.TSAmnt.split(':')[0]
        except:
            pass
    
    def r_OTRAmnt(self):
        try:
            return self.TRAmnt.split(':')[0]
        except:
            pass
    
    def r_NM(self):
        try:
            return self.magazines.split(':')[1]
        except:
            pass
    
    def r_NP(self):
        try:
            return self.periods.split(':')[1]
        except:
            pass
        
    def r_NMRP(self):
        try:
            return self.mrps.split(':')[1]
        except:
            pass    
        
    def r_NSAmnt(self):
        try:
            return self.subAmnts.split(':')[1]
        except:
            pass
    
    def r_NRAmnt(self):
        try:
            return self.recAmnts.split(':')[1]
        except:
            pass
    
    def r_NDis(self):
        try:
            temp=self.dis.split(':')[1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass

    def r_NCDis(self):
        try:
            temp=self.comdis.split(':')[1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_NADis(self):
        try:
            temp=self.addis.split(':')[1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_NScheme(self):
        try:
            temp=self.scheme.split('-')[1].replace(':',',')[:-1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_NGift(self):
        try:
            
            temp=self.gift.split('-')[1].replace(':',',')[:-1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass

    def r_NSource(self):
        try:
            return self.subSource.split(':')[1]
        except:
            pass
    
    def r_NEmpId(self):
        try:
            temp=self.empid.split(':')[1]
            if temp=='':
                return "----"
            else:
                return temp
        except:
            pass
    
    def r_NTSAmnt(self):
        try:
            return self.TSAmnt.split(':')[1]
        except:
            pass
    
    def r_NTRAmnt(self):
        try:
            return self.TRAmnt.split(':')[1]
        except:
            pass

    def getMagazineName(self):
        try:
            getsub=tbl_subscription.objects.get(id=self.subId)
            return getsub.magazine.name

        except:
            pass


        
    '''__________________________'''

class tbl_notify(models.Model):
    '''subId is subscription id'''
    
    subId=models.IntegerField(unique=True,null=True,blank=True)
    subPeriod=models.IntegerField(null=True,blank=True)
    subDate=models.DateField(null=True,blank=True)
    startDate=models.DateField(null=True,blank=True)
    subEndDate=models.DateField(null=True,blank=True)
    firstDate=models.DateField(null=True,blank=True)
    secondDate=models.DateField(null=True,blank=True)
    thirdDate=models.DateField(null=True,blank=True)
    fourthDate=models.DateField(null=True,blank=True)
    def __unicode__(self):
        return "%s-(%s)"%(self.id,self.subId)
    
    
    
class tbl_complaintResponse(models.Model):
    compId=models.IntegerField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    empId=models.IntegerField(null=True,blank=True)
    subId=models.IntegerField(null=True,blank=True)
    date=models.DateTimeField(default=ProjectScope().getDate())    
    createdOn=models.DateTimeField(default=ProjectScope().getDate())
    updatedOn=models.DateTimeField(default=ProjectScope().getDate())
    def validate_unique(self, exclude=None):
        models.Model.validate_unique(self, exclude=exclude)
        self.updatedOn=ProjectScope().getDate()
    def __unicode__(self):
        return "%s-%s"%(self.id,self.description)
    def getEmpId(self):
        return ProjectScope().empCodePrefix()+str(self.empId)
    def getuser(self):
        return tbl_employee.objects.get(id=self.empId).username
    



