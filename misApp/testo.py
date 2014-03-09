

#import datetime
#print datetime.datetime(2013,10,23,11,30)


#
#try:
#        
#    x="[[s'asdasdad','2013-10-2 0:0','2013-10-2 0:0','#ffffff','#002E8A'],['asdas','2013-10-2 0:0','2013-10-2 0:0','#ffffff','#002E8A']]"
#    
#    for x in eval(x):
#        print x
#except SyntaxError:
#    
#    

#import datetime 
#from misApp.models import tbl_events
##sd='2013-10-24 0:30'
##print datetime.datetime.strptime(sd,"%Y-%m-%d %H:%M")
#import datetime
#tbl_events.objects.create(username='irfan',event='test',startDate=datetime.datetime.strptime('2013-12-12 11:20',"%Y-%m-%d %H:%M"),endDate=datetime.datetime.strptime('2013-12-12 11:30',"%Y-%m-%d %H:%M"),fgColor="#"+'236464',bgColor="#"+'a31311')

#e=tbl_events.objects.all()[0].startDate
#print str(e)
#e=tbl_events.objects.get(event="irfan")
#import datetime
#print e.startDate
#print datetime.datetime.today()
#import pytz,datetime
#utc=pytz.UTC
##now_aware = utc.localize(e.startDate)
#
#print datetime.datetime.today()
#print datetime.datetime.now()
#print datetime.datetime.utcnow()

#For the UTC timezone, it is not really necessary to use localize since there is no daylight savings time calculation to handle:

#now_aware = unaware.replace(tzinfo=pytz.UTC)
