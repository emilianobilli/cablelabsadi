

class assetPackages(object):



class assetPackage(object):


class title(object):
    def __init__(self):
	self.languaje   = ''
	self.title      = ''

    def Set(languaje='', title=''):
	self.languaje = languaje
	self.title    = title    
    
class sortTitle(object):
    def __init__(self):
	self.languaje = ''
	self.title    = ''
	
    def Set(languaje='',title=''):
	self.languaje = languaje
	self.title    = title  	
    

class metadata(object):
    self.assetID    = ''
    self.providerID = ''
    self.title      = title()
    self.


class bussinessMetadata(object):
    def __init__(self):
	self.suggestedPrice=''
	self.currency_iso3166-2=''
	

class rigthsMetadata(object):
    def __init__(self):
        self.licensingWindowStart    =''
	self.licensingWindowEnd      =''
	self.availabilityWindowStart =''
	self.availabilityWindowEnd   =''
	self.maximumViewingLimit     =''
	

    def ToElement(self):
	














