from xml.etree.ElementTree import *



class person(object):
    def __init__(self):
	self.mname = ''
	self.fname = ''
	self.lname = ''
	self.role  = ''
	
    def ToElement(self):
	person = Element('person')
	person.attrib['mname'] = self.mname
	person.attrib['fname'] = self.fname
	person.attrib['lname'] = self.lname
	person.attrib['role']  = self.role
	
	return person

class actor(person):
    def __init__(self):
	person.__init__(self)
	self.role = 'Actor'
    
class director(person):
    def __init__(self):
	person.__init__(self)
	self.role = 'Director'

class assetPackage(object):
    def __init__(self):
	self.verb    = ''
	self.type    = ''
	self.product = ''
	self.providerName = ''
	self.providerID   = ''
	self.asset_name   = ''

	self.metadata = metadata()
	self.businessMetadata = businessMetadata()
	self.rightsMetadata   = rightsMetadata()
	self.assetFeature     = assetFeature()
	self.assetPoster      = assetPoster()

    def ToElement(self):
	assetPackage = Element('assetPackage')
	assetPackage.attrib['verb'] = self.verb
	assetPackage.attrib['type'] = self.type
	assetPackage.attrib['product'] = self.product
	assetPackage.attrib['providerName'] = self.providerName
	assetPackage.attrib['providerID']   = self.providerID
	assetPackage.attrib['asset_name']   = self.asset_name
	assetPackage.append(self.metadata.ToElement())
	assetPackage.append(self.businessMetadata.ToElement())
	assetPackage.append(self.rightsMetadata.ToElement())
	assetPackage.append(self.assetFeature.ToElement())
	assetPackage.append(self.assetPoster.ToElement())
	
	root = Element('assetPackages')
	root.attrib['xmlns:date'] = "http://exslt.org/dates-and-times"
	root.attrib['xmlns:xsd']  = "http://www.w3.org/2001/XMLSchema"
	root.attrib['xsi:noNamespaceSchemaLocation'] = "vodmetadata.xsd"
	root.attrib['xmlns:xsi']  = "http://www.w3.org/2001/XMLSchema-instance"
	root.attrib['formatVersion'] = "1.0"
	root.append(assetPackage)
	return root

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def toAdiFile(Element=None, FileName=None):
    if Element is not None and FileName is not None:
	element = Element.ToElement()
	indent(element)
	string = tostring(element, encoding="UTF-8")
	fd = open(FileName, "wb")
	fd.write(string)
	fd.close()
	return True
    else:
	return False
    
	
class asset(object):
    def __init__(self):
	self.verb    = ''
	self.type    = ''
	self.asset_name = ''
	self.content = ''
	self.metadata = None

    def ToElement(self):
	asset = Element('asset')
	asset.attrib['verb'] = self.verb
	asset.attrib['type'] = self.type
	asset.attrib['asset_name'] = self.asset_name
	content = Element('content')
	content.text = self.content
	if self.metadata is not None:
	    asset.append(self.metadata.ToElement())
	asset.append(content)
	
	return asset
		
class assetPoster(asset):
    def __init__(self):
	asset.__init__(self)
	self.metadata = metadataPoster()
	
class assetFeature(asset):
    def __init__(self):
	asset.__init__(self)
	self.metadata = metadataFeature()

class metadataPoster(object):
    def __init__(self):
	self.assetID = ''
	self.providerID = ''
	self.rating_value = ''
	self.rating_system = ''
	
    def ToElement(self):
	metadataPoster = Element('metadata')
	assetID = Element('assetID')
	providerID = Element('providerID')
	language_iso639 = Element('language_iso639')
	rating = Element('rating')
	
	assetID.text = self.assetID
	providerID.text = self.providerID
	rating.attrib['value'] = self.rating_value
	rating.attrib['rating_system'] = self.rating_system

	metadataPoster.append(assetID)
	metadataPoster.append(providerID)
	metadataPoster.append(rating)
			
	return metadataPoster

class metadataFeature(object):
    def __init__(self):
	self.assetID = ''
	self.providerID = ''
	self.HD = ''
	self.language_iso639 = ''
	self.rating_value = ''
	self.rating_system = ''
	self.audio = ''
	
    def ToElement(self):
	metadataFeature = Element('metadata')
	assetID = Element('assetID')
	providerID = Element('providerID')
	HD = Element('HD')
	language_iso639 = Element('language_iso639')
	rating = Element('rating')
	audio = Element('audio')
	
	assetID.text = self.assetID
	providerID.text = self.providerID
	HD.text = self.HD
	language_iso639.text = self.language_iso639
	rating.attrib['value'] = self.rating_value
	rating.attrib['rating_system'] = self.rating_system
	
	audio.text = self.audio
	
	metadataFeature.append(assetID)
	metadataFeature.append(providerID)
	metadataFeature.append(HD)
	metadataFeature.append(language_iso639)
	metadataFeature.append(rating)
	metadataFeature.append(audio)
	
	return metadataFeature


class rightsMetadata(object):
    def __init__(self):
	self.licensingWindowStart = ''
	self.licensingWindowEnd = ''
	self.availabilityWindowStart = ''
	self.availabilityWindowEnd = ''
	self.daystoLastChance = ''
	self.newReleaseWindow = ''
	self.maximumViewingLimit = ''
	
    def ToElement(self):
	rightsMetadata 		= Element('rightsMetadata')
	licensingWindowStart 	= Element('licensingWindowStart')
	licensingWindowEnd 	= Element('licensingWindowEnd')
	availabilityWindowStart = Element('availabilityWindowStart')
	availabilityWindowEnd 	= Element('availabilityWindowEnd')
	daystoLastChance 	= Element('daystoLastChance')
	newReleaseWindow 	= Element('newReleaseWindow')
	maximumViewingLimit 	= Element('maximumViewingLimit')
	
	licensingWindowStart.text 	= self.licensingWindowStart
	licensingWindowEnd.text 	= self.licensingWindowEnd
	availabilityWindowStart.text 	= self.availabilityWindowStart
	availabilityWindowEnd.text 	= self.availabilityWindowEnd
	daystoLastChance.text 		= self.daystoLastChance
	newReleaseWindow.text 		= self.newReleaseWindow
	maximumViewingLimit.text 	= self.maximumViewingLimit
	
	rightsMetadata.append(licensingWindowStart)
	rightsMetadata.append(licensingWindowEnd)
	rightsMetadata.append(availabilityWindowStart)
	rightsMetadata.append(availabilityWindowEnd)
	rightsMetadata.append(daystoLastChance)
	rightsMetadata.append(newReleaseWindow)
	rightsMetadata.append(maximumViewingLimit)
	
	return rightsMetadata
	


class businessMetadata(object):
    def __init__(self):
	self.suggestedPrice = ''
	self.currency_iso3166_2 = ''
	self.billingID = ''
	
    def ToElement(self):
	businessMetadata 	= Element('businessMetadata')
	
	suggestedPrice 		= Element('suggestedPrice')
	currency_iso3166_2 	= Element('currency_iso3166-2')
	billingID 		= Element('billingID')
	
	suggestedPrice.text 	= self.suggestedPrice
	currency_iso3166_2.text = self.currency_iso3166_2
	billingID.text 		= self.billingID
		
	businessMetadata.append(suggestedPrice)
	businessMetadata.append(currency_iso3166_2)
	businessMetadata.append(billingID)
			
	return businessMetadata


class categorizacion(object):
    def __init__(self):
	self.category1 = ''
	self.category2 = ''
	
    def ToElement(self):
	categorizacion = Element('categorizacion')
	category1 = Element('category1')
	category2 = Element('category2')
	category1.attrib['name'] = self.category1
	category2.attrib['name'] = self.category2
	categorizacion.append(category1)
	categorizacion.append(category2)
	
	return categorizacion
	
	

class metadata(object):
    def __init__(self):
	
	self.language 		= ''
    
	self.assetID 		= ''
	self.providerID 	= ''
	self.showType 		= ''
	self.title 		= ''
	self.sortTitle 		= ''
	self.reducedTitle 	= ''
	self.summary 		= ''
	self.shortSummary 	= ''
	self.episodeNumber 	= ''
	self.cgmsaLevel 	= ''
	self.runTimeMinutes 	= ''
	self.release_year 	= ''
	self.countryRegionCode 	= ''
	self.studio 		= ''
	self.studioDisplayName 	= ''
	self.category 		= ''
	self.category1		= ''
	self.category2		= ''
	self.autoDeploy 	= ''
	self.autoImport 	= ''
	self.actor 	        = actor()
	self.director		= director()
	self.categorizacion	= categorizacion()    

    def ToElement(self):
	metadata = Element("metadata")
	
	assetID 		= Element('assetID')
	providerID 		= Element('providerID')
	showType 		= Element('showType')
	title 			= Element('title')
	sortTitle 		= Element('sortTitle')
	reducedTitle 		= Element('reducedTitle')
	summary 		= Element('summary')
	shortSummary 		= Element('shortSummary')
	episodeNumber 		= Element('episodeNumber')
	cgmsaLevel 		= Element('cgmsaLevel')
	runTimeMinutes 		= Element('runTimeMinutes')
	release_year 		= Element('release_year')
	countryRegionCode 	= Element('countryRegionCode')
	studio 			= Element('studio')
	studioDisplayName 	= Element('studioDisplayName')
	category 		= Element('category')
	category1		= Element('category')
	category2		= Element('category')
	autoDeploy 		= Element('autoDeploy')
	autoImport 		= Element('autoImport')
			
			
	title.attrib['language']	= self.language
	sortTitle.attrib['languaje'] 	= self.language
	reducedTitle.attrib['languaje'] = self.language
	summary.attrib['language'] 	= self.language
	shortSummary.attrib['language'] = self.language
	
			
	assetID.text 		= self.assetID
	providerID.text 	= self.providerID
	showType.text 		= self.showType
	title.text 		= self.title
	sortTitle.text 		= self.sortTitle
	reducedTitle.text 	= self.reducedTitle
	summary.text 		= self.summary
	shortSummary.text 	= self.shortSummary
	episodeNumber.text 	= self.episodeNumber
	cgmsaLevel.text 	= self.cgmsaLevel
	runTimeMinutes.text 	= self.runTimeMinutes
	release_year.text 	= self.release_year
	countryRegionCode.text 	= self.countryRegionCode
	studio.text 		= self.studio
	studioDisplayName.text 	= self.studioDisplayName
	category.text 		= self.category
	category1.text		= self.category1
	category2.text		= self.category2
	autoDeploy.text 	= self.autoDeploy
	autoImport.text 	= self.autoImport
	
	metadata.append(assetID)
	metadata.append(providerID)
	metadata.append(showType)
	metadata.append(title)
	metadata.append(sortTitle)
	metadata.append(reducedTitle)
	metadata.append(summary)
	metadata.append(shortSummary)
	metadata.append(episodeNumber)
	metadata.append(cgmsaLevel)
	metadata.append(runTimeMinutes)
	metadata.append(release_year)
	metadata.append(countryRegionCode)
	metadata.append(studio)
	metadata.append(studioDisplayName)
	metadata.append(category)
	if self.category1 != '':
	    metadata.append(category1)
	if self.category2 != '':
	    metadata.append(category2)    
	metadata.append(autoDeploy)
	metadata.append(autoImport)
	metadata.append(self.actor.ToElement())
	metadata.append(self.director.ToElement())
	metadata.append(self.categorizacion.ToElement())
	
	return metadata

