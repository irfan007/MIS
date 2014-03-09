from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group,User
from django.contrib.admin.options import ModelAdmin
from misApp.models import tbl_employee,tbl_departments,\
    tbl_permission, tbl_role, tbl_location, tbl_magazine,\
    tbl_magazineCombo, tbl_tenure, tbl_gift, tbl_source,\
    tbl_competitor, tbl_customer, tbl_subscription,\
     tbl_dispatch,\
    tbl_notify, tbl_supportedCourier, tbl_complaint, tbl_transaction,\
    tbl_history, tbl_renewal, tbl_branch, tbl_complaintResponse, tbl_taskList,\
    tbl_log, tbl_giftHistory, tbl_ticket, tbl_ticketType, tbl_followUp,\
    tbl_magazinePeriod, tbl_contentType, tbl_contact, tbl_transfer, tbl_scheme,\
    tbl_events

    




class locationOption(ModelAdmin):
    list_display=('id','name','pid')
     
class subscriptionsOption(ModelAdmin):
    list_display=('id','isActive','issues')

class customerOption(ModelAdmin):
    list_display=('id','email','isActive')



admin.site.register(tbl_tenure)
admin.site.register(tbl_gift)
admin.site.register(tbl_scheme)
admin.site.register(tbl_source)
admin.site.register(tbl_competitor)
'''-----start employee models----------------'''
admin.site.register(tbl_events)
admin.site.register(tbl_departments)
admin.site.register(tbl_permission)
admin.site.register(tbl_role)
admin.site.register(tbl_employee)
admin.site.register(tbl_location,locationOption)
admin.site.register(tbl_magazine)
admin.site.register(tbl_magazineCombo)
admin.site.register(tbl_magazinePeriod)
'''-----end employee models----------------'''


'''-----start customer models----------------'''

admin.site.register(tbl_contentType)
admin.site.register(tbl_contact)
admin.site.register(tbl_transfer)
admin.site.register(tbl_followUp)
admin.site.register(tbl_ticketType)
admin.site.register(tbl_ticket)
admin.site.register(tbl_subscription,subscriptionsOption)
admin.site.register(tbl_customer,customerOption)
admin.site.register(tbl_dispatch)
admin.site.register(tbl_supportedCourier)
admin.site.register(tbl_complaint)
admin.site.register(tbl_notify)
admin.site.register(tbl_transaction)
admin.site.register(tbl_history)
admin.site.register(tbl_renewal)
admin.site.register(tbl_branch)
admin.site.register(tbl_complaintResponse)
admin.site.register(tbl_taskList)
admin.site.register(tbl_log)
admin.site.register(tbl_giftHistory)

'''-----end customer models----------------'''
admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(User)