from misApp.pp import hasLogedInEmployee
from misApp.models import tbl_employee





def currentUser(req):
    CUP={}
    autoRedirect={
                  'admin':'/subscription/list/',
                  'stock':'/giftstock/',
                  'location':'/locations/',
                  'department':'/departments/',
                  'role':'/role/list/',
                  'employee':'/user/list',
                  'magazine':'/magazine/list/',
                  'magazine combo':'/combo/list/',
                  'scheme':'/schemes/',
                  'gift':'/gifts/',
                  'source':'/sources/',
                  'tenure':'/tenures/',
                  'subscription':'/subscription/list',
                  'compliment':'/compliment/',
                  'com':'',
                  'report':'/report/gift/',
                  'print':'/Mlabel/',
                  'notification':'/notification/',
                  'crm':'/CRM/',
                  'courier':'/couriers/',
                  'branch':'/branch/',
                  'stock':'/giftstock/'
                  
    }
    '''
    CUP/current user permissions  
    '''
    config=['location','department','role','employee','magazine','magazine combo','scheme','gift','source','tenure','courier','branch']
            
    try:
        for p in tbl_employee.objects.get(username=req.session['username']).role.permissions.all():
            CUP[p.content.name]=[p.view,p.add,p.update,p.delete]
            
            
        anyConfig=[key for key in CUP.iterkeys() if key in config]
        if anyConfig:
            CUP['config']=[True,autoRedirect[anyConfig[0]]]
       
    except:
        '''
        no permissions will be found in tbl_permission for admin 
        '''
        try:
            if tbl_employee.objects.get(username=req.session['username']).isAdmin:
                CUP['config']=[True,'/user/list/']
        except:
            pass
    

    return {'cu':hasLogedInEmployee(req),'CUP':CUP}