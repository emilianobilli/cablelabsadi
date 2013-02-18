from xml.etree.ElementTree import *




class RiGHTvAssets(object):
    def __init__(self):
	self.VideoAssets = VideoAssets()

    def ToElement(self):
	RiGHTvAssets = Element("RiGHTAssets")
	RiGHTvAssets.attrib["xmlns"] = "http://www.orca.tv/RiGHTv/5.1/Asset"
	RiGHTvAssets.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
	RiGHTvAssets.attrib["xsi:schemaLocation"] = "http://www.orca.tv/RiGHTv/5.1/AssetRiGHTvAsset.xsd"

	RiGHTvAssets.append(self.VideoAssets.ToElement())
	return RiGHTvAssets


class LicensingWindow(object):
    def __init__(self):
	self.StartDateTime	= ''
	self.EndDateTime	= ''

    def ToElement(self):
	LicensingWindow = Element("LicensingWindow")
	LicensingWindow.attrib["StartDateTime"] = self.StartDateTime
	LicensingWindow.attrib["EndDateTime"]	= self.EndDateTime

	return LicensingWindow


class VideoAssets(object):
    def __init__(self):
	self.ID 		= ''
	self.ProviderID 	= ''
	self.Title		= ''
	self.Description	= ''
	self.ParentalRating	= ''
	self.Advisories		= ''
	self.LicensingWindow	= LicensingWindow()
	self.PosterFiles	= PosterFiles()
	self.MediaFiles		= MediaFiles()
	self.ExtraFields	= []
	self.AMSPath		= ''

    def addExtraFields(self, Name='', Value=''):
	ExtraField = Element("ExtraField")
	ExtraField.attrib["Name"] = Name
	ExtraField.attrib["Value"] = Value
	self.ExtraFields.append(ExtraField)

    def ToElement(self):

	VideoAssets = Element("VideoAssets")
	VideoAsset  = Element("VideoAsset")
	VideoAsset.attrib["ID"] = self.ID
	VideoAsset.attrib["ProviderID"] = self.ProviderID
	Description	= Element("Description")
	Title		= Element("Title")
	AMSPath		= Element("AMSPath")
	ParentalRating	= Element("ParentalRating")
	Advisories	= Element("Advisories")
	ExtraFields	= Element("ExtraFields")
	
	for ef in self.ExtraFields:
	    ExtraFields.append(ef)


	Description.text = self.Description
	Title.text	 = self.Title
	ParentalRating.text = self.ParentalRating
	Advisories.text		= self.Advisories
	AMSPath.text			= self.AMSPath

	VideoAsset.append(Title)
	VideoAsset.append(Description)
	VideoAsset.append(ParentalRating)
	VideoAsset.append(Advisories)
	VideoAsset.append(self.LicensingWindow.ToElement())
	VideoAsset.append(self.PosterFiles.ToElement())
	VideoAsset.append(AMSPath)
	VideoAsset.append(ExtraFields)
	VideoAsset.append(self.MediaFiles.ToElement())
    
	VideoAssets.append(VideoAsset)
	return VideoAssets



class PosterFiles(object):
    def __init__(self):
	self.Name        = ''
	self.Description = ''
	self.FileName    = ''

    def ToElement(self):
	PosterFiles = Element("PosterFiles")
	LinkedFile  = Element("LinkedFile")

	LinkedFile.attrib["Name"] = self.Name
	LinkedFile.attrib["Description"] = self.Description
	LinkedFile.attrib["FileName"]	= self.FileName

	PosterFiles.append(LinkedFile)
	return PosterFiles



class Density(object):
    def __init__(self):
	self.Type  = ''
	self.Value = ''

    def ToElement(self):
	Density = Element("Density")
	Density.attrib["Type"]  = self.Type
	Density.attrib["Value"] = self.Value
	return Density


class ServiceDistribution(object):
    def __init__(self):
	self.Name	= ''
	self.Density	= Density()
    
    def ToElement(self):
	ServiceDistributions = Element("ServiceDistributions")
	ServiceDistribution  = Element("ServiceDistribution")
	AutoCDN		     = Element("AutoCDN")
	ServiceDistribution.attrib["Name"] = self.Name
	ServiceDistribution.append(self.Density.ToElement())
	ServiceDistribution.append(AutoCDN)
	ServiceDistributions.append(ServiceDistribution)
	
	return ServiceDistributions
	
class MediaFiles(object):
    def __init__(self):
	self.FileName    = ''
	self.Encoding    = ''
	self.TransferURL = ''
	self.RunTime	 = ''
	self.BitRate     = ''
	self.Encryption  = ''
	self.DisplayType = ''

	self.ServiceDistribution = ServiceDistribution()

    def ToElement(self):
	MediaFiles	= Element("MediaFiles")
	MediaFile	= Element("MediaFile")

	TransferURL	= Element("TransferURL")
	TransferURL.text= self.TransferURL

	RunTime		= Element("RunTime")
	RunTime.text	= self.RunTime

	BitRate		= Element("BitRate")
	BitRate.text	= self.BitRate
    
	Encryption	= Element("Encryption")
	Encryption.text = self.Encryption

	DisplayType	= Element("DisplayType")
	DisplayType.text= self.DisplayType

	MediaFile.append(self.ServiceDistribution.ToElement())
	MediaFile.append(TransferURL)
	MediaFile.append(RunTime)
	MediaFile.append(BitRate)
	MediaFile.append(Encryption)
	MediaFile.append(DisplayType)

	MediaFiles.append(MediaFile)
	return MediaFiles

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
	string = tostring(element, encoding="ISO-8859-1")
	fd = open(FileName, "wb")
	fd.write(string)
	fd.close()
	return True
    else:
	return False



