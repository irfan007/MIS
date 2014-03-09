from misApp.models import tbl_contentType





def setUpContentType():
	'''
	_types contains content type as
	'category':'name1,name2,...' 
	
	NOTE: must be updated!!!!
	'''
	_types=[
		['Configuration','location:department:role:employee:magazine:magazine combo:scheme:gift:source:tenure:courier:branch'],
		['Subscription','subscription'],
		['Report','report'],
		['Label Print','print'],
		['Manual Notification','notification'],
		['CRM','crm'],
		['Gift Stock','stock']
		]
	
	for cat,names in _types:
		for name in names.split(':'):
			tbl_contentType.objects.create(category=cat,name=name,isActive=True)
	
	print '<<CONTENT TYPE DONE>>'		
		
#setUpContentType()