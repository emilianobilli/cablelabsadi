from xml.etree.ElementTree import *


class NepeXml(object):
    def __init__(self):
	self.ItemID = ''
	self.ExportDate = ''
	self.Distributor = ''
	self.StartWindow = ''
	self.EndWindow = ''
	self.ContentType = ''
	self.Title = ''
	self.OriginalTitle = ''
	self.ShotDescription = ''
	self.LongDescription = ''
	self.Country = ''
	self.Actors = ''
	self.Directors = ''
	self.Brand = ''
	self.Category = ''
	self.Duration = ''
	self.Standard = ''
	self.Rating = ''
	self.ImageFile = ''
	self.AudioType = ''
	self.VideoFile = ''
	self.VideoFormat = ''

    def ToElement(self):
	NepeXml = Element("NepeXml")
	
	ItemID      = Element('ItemID')
	ExportDate  = Element('ExportDate')
	Distributor = Element('Distributor')
	StartWindow = Element('StartWindow')
	EndWindow   = Element('EndWindow')
	ContentType = Element('ContentType')
	Title       = Element('Title')
	OriginalTitle   = Element('OriginalTitle')
	ShortDescription = Element('ShortDescription')
	LongDescription = Element('LongDescription')
	Country     = Element('Country')
	Actors      = Element('Actors')
	Directors   = Element('Directors')
	Brand       = Element('Brand')
	Category    = Element('Category')
	Duration    = Element('Duration')
	Standard    = Element('Standard')
	Rating      = Element('Rating')
	ImageFile   = Element('ImageFile')
	AudioType   = Element('AudioType')
	VideoFile   = Element('VideoFile')
	VideoFormat = Element('VideoFormat')
	
	ItemID.text      = self.ItemID
	ExportDate.text  = self.ExportDate
	Distributor.text = self.Distributor
	StartWindow.text = self.StartWindow
	EndWindow.text   = self.EndWindow
	ContentType.text = self.ContentType
	Title.text       = self.Title
	OriginalTitle.text   = self.OriginalTitle
	ShortDescription.text = self.ShortDescription
	LongDescription.text = self.LongDescription
	Country.text     = self.Country
	Actors.text      = self.Actors
	Directors.text   = self.Directors
	Brand.text       = self.Brand
	Category.text    = self.Category
	Duration.text    = self.Duration
	Standard.text    = self.Standard
	Rating.text      = self.Rating
	ImageFile.text   = self.ImageFile
	AudioType.text   = self.AudioType
	VideoFile.text   = self.VideoFile
	VideoFormat.text = self.VideoFormat
	
	NepeXml.append(ItemID)
	NepeXml.append(ExportDate)
	NepeXml.append(Distributor)
	NepeXml.append(StartWindow)
	NepeXml.append(EndWindow)
	NepeXml.append(ContentType)
	NepeXml.append(Title)
	NepeXml.append(OriginalTitle)
	NepeXml.append(ShortDescription)
	NepeXml.append(LongDescription)
	NepeXml.append(Country)
	NepeXml.append(Actors)
	NepeXml.append(Directors)
	NepeXml.append(Brand)
	NepeXml.append(Category)
	NepeXml.append(Duration)
	NepeXml.append(Standard)
	NepeXml.append(Rating)
	NepeXml.append(ImageFile)
	NepeXml.append(AudioType)
	NepeXml.append(VideoFile)
	NepeXml.append(VideoFormat)
	
	return NepeXml
	
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
	
def fromAdiFile(FileName=None):
    if FileName is not None:
	
	Element = parse(FileName)
	dump(Element)
	Nepe = NepeXml()
	if Element is not None:
	    ItemID = Element.find("ItemID")
	    dump(ItemID)
	    if ItemID is not None:
		Nepe.ItemID = ItemID.text 
	    ItemID = Element.find("ItemID") 
	    if ItemID is not None:
		Nepe.ItemID = ItemID.text
	    ExportDate = Element.find("ExportDate")
	    if ExportDate is not None:
		Nepe.ExportDate = ExportDate.text
	    Distributor = Element.find("Distributor")
	    if Distributor is not None:
		Nepe.Distributor = Distributor.text
	    StartWindow = Element.find("StartWindow")
	    if StartWindow is not None:
		Nepe.StartWindow = StartWindow.text
	    EndWindow = Element.find("EndWindow")
	    if EndWindow is not None:
		Nepe.EndWindow = EndWindow.text
	    ContentType = Element.find("ContentType")
	    if ContentType is not None:
		Nepe.ContentType = ContentType.text
	    Title = Element.find("Title")
	    if Title is not None:
		Nepe.Title = Title.text
	    OriginalTitle = Element.find("OriginalTitle")
	    if OriginalTitle is not None:
		Nepe.OriginalTitle = OriginalTitle.text
	    ShortDescription = Element.find("ShortDescription")
	    if ShortDescription is not None:
		Nepe.ShortDescription = ShortDescription.text
	    LongDescription = Element.find("LongDescription")
	    if LongDescription is not None:
		Nepe.LongDescription = LongDescription.text
	    Country = Element.find("Country")
	    if Country is not None:
		Nepe.Country = Country.text
	    Actors = Element.find("Actors")
	    if Actors is not None:
		Nepe.Actors = Actors.text
	    Directors = Element.find("Directors")
	    if Directors is not None:
		Nepe.Directors = Directors.text
	    Brand = Element.find("Brand")
	    if Brand is not None:
		Nepe.Brand = Brand.text
	    Category = Element.find("Category")
	    if Category is not None:
		Nepe.Category = Category.text
	    Duration = Element.find("Duration")
	    if Duration is not None:
		Nepe.Duration = Duration.text
	    Standard = Element.find("Standard")
	    if Standard is not None:
		Nepe.Standard = Standard.text
	    Rating = Element.find("Rating")
	    if Rating is not None:
		Nepe.Rating = Rating.text
	    ImageFile = Element.find("ImageFile")
	    if ImageFile is not None:
		Nepe.ImageFile = ImageFile.text
	    AudioType = Element.find("AudioType")
	    if AudioType is not None:
		Nepe.AudioType = AudioType.text
	    VideoFile = Element.find("VideoFile")
	    if VideoFile is not None:
		Nepe.VideoFile = VideoFile.text
	    VideoFormat = Element.find("VideoFormat")
	    if VideoFormat is not None:
		Nepe.VideoFormat = VideoFormat.text

	return Nepe