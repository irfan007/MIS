
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views.authenticate import v_home, v_loginUser, v_logoutUser,\
    v_forgotPassword
from views.user import v_user
from views.magazine import v_magazine, v_combo
from views.role import v_role, v_addRole, v_editRole
from views.subscription import v_subscription, v_MDispatch, v_GDispatch,\
    v_viewTransaction, v_addTransaction, v_customer
from views.notification import v_notification, v_emailNotification
from views.labelPrint import v_printMLabel, v_printGLabel
from views.compliment import v_complementary, v_editComplement
from views.i_other import v_responder
from views.suspend import v_suspended, v_resume, v_suspend, v_suspendReason,\
    v_viewReason
from misApp.views import  v_locations, v_editLocation,\
    v_addLocation,v_Mresponder, v_accMresponder,\
    javascript_for_crm_and_competitors, v_search, v_moreList, v_log,\
    v_fulllogview, v_logFilter
from views.myaccount import v_change_employee_detail
from views.courier import v_courier, v_addCourier, v_editCourier
from views.gift import v_gifts, v_addGift, v_editGift, v_giftstock,\
    v_giftEditStock, v_gifthistory
from views.source import v_sources, v_addSource, v_editSource
from views.tenure import v_tenures, v_addTenure, v_editTenure
from views.department import v_departments, v_addDepartment, v_editDepartment
from views.scheme import v_schemes, v_addScheme, v_editScheme
from views.CRM import  v_addCRM, v_editCRM, v_addComplaint
from views.branch import v_branch, v_addBranch, v_editBranch
from views.changepassword import v_reset_password
from views.reports import v_reportchequedeposit, v_reportdraftdeposit,\
    v_reportGift, v_offerReport, v_srcsubReport, v_reportneftdeposit,\
    v_reportonlinepayment, v_reportcashpayment, v_monthlySubscription,\
    v_activesubscriptionreport, v_POreport
from views.popup import v_popUp
from views.pagination import v_next, v_previous
from views.competitor import v_competitors, v_editCompetitor, v_addCompetitor,\
    v_excel_for_competitors

from views.crm2 import  v_crmHome, v_newTicketStep1, v_newTicketStep2,\
    v_editTicket, v_transferTicket, v_crmSales, v_contact, v_followUpAsNew,\
    v_searchSub, v_followUpAsSub, v_eventCalander




from views.magazinePeriod import v_magazinePeriod, v_addMagazinePeriod,\
    v_editMagazinePeriod, v_magPeriod, v_getMagPeriod


admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^test/([\d]+)',v_renew),
    
    # Examples:
    # url(r'^$', 'MIS.views.home', name='home'),
    # url(r'^MIS/', include('MIS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^CRM/$',v_crmHome),
    url(r'^CRM/([\d]+)/$',v_editTicket),
    url(r'^CRM/newticket/$',v_newTicketStep1),
    url(r'^CRM/add/([\d]+)/$',v_newTicketStep2),
    url(r'^CRM/transfer/([\d]+)/$',v_transferTicket),
    url(r'^CRM/events/$',v_eventCalander),
    

    url(r'^sales/$',v_crmSales),
    url(r'^sales/contact/([\d]+)/$',v_contact),
    url(r'^sales/followup_as_new/$',v_followUpAsNew),
    url(r'^sales/followup_as_sub/$',v_searchSub),
    url(r'^sales/followup_as_sub/([\d]+)/$',v_followUpAsSub),

    

    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^responder/',v_responder),
    url(r'^add/(.+)/',v_popUp),
    
    #----------PP Started-----------------------
    
    url(r'^$',v_home),
    url(r'^login/',v_loginUser),
    url(r'^logout/',v_logoutUser),
    url(r'^forgotPassword/',v_forgotPassword),
    
    url(r'^user/(.+)+',v_user),
    url(r'^magazine/(.+)+',v_magazine),
    url(r'^combo/(.+)+',v_combo),
    
    url(r'^role/list/$',v_role),
    url(r'^role/add/$',v_addRole),
    url(r'^role/edit/([\d]+)',v_editRole),
    
    url(r'^customer/$',v_customer),
    url(r'^subscription/(.+)+',v_subscription),
    url(r'^notification/$',v_notification),
    url(r'^notification/email/(.+)+',v_emailNotification),
    url(r'^dispatch/medit/([\d]+)+',v_MDispatch),
    url(r'^dispatch/gedit/([\d]+)+',v_GDispatch),
    url(r'^Mlabel/',v_printMLabel),
    url(r'^Glabel/',v_printGLabel),
    url(r'^transaction/([\d]+)+',v_viewTransaction),
    url(r'^transaction/add/([\d]+)+',v_addTransaction),
    
    url(r'^compliment/$',v_complementary),
    #url(r'^compliment/add/$',v_addComplement),
    url(r'^compliment/edit/([\d]+)+',v_editComplement),
    
    url(r'^suspended/$',v_suspended),
    url(r'^suspend/([\d]+)$',v_suspend),
    url(r'^suspendreason/([\d]+)$',v_suspendReason),
    url(r'^resume/([\d]+)$',v_resume),
    url(r'^reason/([\d]+)$',v_viewReason),
    
    
    
    url(r'^next/(.+)/([\d]+)$',v_next),
    url(r'^previous/(.+)/([\d]+)$',v_previous),
    
    
    #-------------------------------------------------------------manav
    
    url(r'^report/PO/',v_POreport),
    url(r'^log/fullview/([\d]+)/$',v_fulllogview),
    url(r'^log/$',v_log),
    url(r'^getData/(.+)/(.+)/$',v_logFilter),
    url(r'^giftstock/$',v_giftstock),
    url(r'^giftstock/edit/([\d]+)/$',v_giftEditStock),
    url(r'^gifthistory/([\d]+)/$',v_gifthistory),
    
    url(r'^resetPassword/$',v_reset_password),
    url(r'^myaccount/$',v_change_employee_detail),
    
    
    url(r'^couriers/$',v_courier),
    url(r'^courier/add/$',v_addCourier),
    url(r'^courier/edit/(.+)+/$',v_editCourier),
    
    
    url(r'^gifts/$',v_gifts),
    url(r'^gift/add/$',v_addGift),
    url(r'^gift/edit/(.+)+/$',v_editGift),
    
    #source section
    url(r'^sources/$',v_sources),
    url(r'^source/add/$',v_addSource),
    url(r'^source/edit/(.+)+/$',v_editSource), 
    
    #tenure section
    url(r'^tenures/$',v_tenures),
    url(r'^tenure/add/$',v_addTenure),
    url(r'^tenure/edit/(.+)+/$',v_editTenure),
    
    #department section
    url(r'^departments/$',v_departments),
    url(r'^department/add/$',v_addDepartment),
    url(r'^department/edit/(.+)+/$',v_editDepartment),
    
     
    #scheme section
    url(r'^schemes/$',v_schemes),
    url(r'^scheme/add/$',v_addScheme),
    url(r'^scheme/edit/(.+)+/$',v_editScheme),
    
    # incentive section
    
    
    
   # location section
   url(r'^locations/$',v_locations), 
   url(r'^location/edit/(.+)+/$',v_editLocation),
   url(r'^location/add/$',v_addLocation),
   
   
   # competitor section
   url(r'^competitors/$',v_competitors), 
   url(r'^competitor/edit/(.+)+/$',v_editCompetitor),
   url(r'^competitor/add/$',v_addCompetitor),
   url(r'^excelcompetitor/$',v_excel_for_competitors),
   
   url(r'^Mresponder/$',v_Mresponder),
   url(r'^accMresponder/$',v_accMresponder),
   #CRM section
   
   
   url(r'^CRM/add/$',v_addCRM),
   url(r'^CRM/edit/(.+)+/$',v_editCRM),
   url(r'^CRMresponder/$',javascript_for_crm_and_competitors),
   url(r'^branch/$',v_branch),
   url(r'^branch/add/$',v_addBranch),
   url(r'^branch/edit/(.+)+/$',v_editBranch),
   
   
   url(r'^Complaint/add/(.+)+/$',v_addComplaint),
   url(r'^search/$',v_search),
   url(r'^MoreList/$',v_moreList),
   #url(r'^reports/$',v_reports),
   url(r'^report/cheque/$',v_reportchequedeposit),
   url(r'^report/draft/$',v_reportdraftdeposit),
   url(r'^report/gift/$',v_reportGift),
   url(r'^report/offer/$',v_offerReport),
   url(r'^report/srcsub/$',v_srcsubReport),
   url(r'^report/neft/$',v_reportneftdeposit),
   url(r'^report/online/$',v_reportonlinepayment),
   url(r'^report/cash/$',v_reportcashpayment),
  
   url(r'^report/monthlySubscriptions/$',v_monthlySubscription),
   
   url(r'^report/MIS/$',v_activesubscriptionreport),
   url(r'^magazinePeriods/$',v_magazinePeriod),
   url(r'^magazinePeriod/add/$',v_addMagazinePeriod),
   url(r'^magazinePeriod/edit/(.+)+/$',v_editMagazinePeriod),
   url(r'^adding/magazinePeriod/$',v_magPeriod),
   url(r'^getMagazinePeriod/$',v_getMagPeriod)
   
   

    
)
