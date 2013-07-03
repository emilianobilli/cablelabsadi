from xml.etree.ElementTree import *


class Insert(object):
    def __init__(self):
	self.asset = Asset()
	self.project = Project()
	self.assetData = AssetData()

    def ToElement(self):
	insert = Element("insert")
	insert.append(self.asset.ToElement())
	insert.append(self.project.ToElement())
	insert.append(self.assetData.ToElement())

	return insert

class Action(object):
    def __init__(self):
	self.insert = Insert()

    def ToElement(self):
	action = Element("action")
	action.append(self.insert.ToElement())

	return action

class XmlData(object):
    def __init__(self):
	self.action = Action()

    def ToElement(self):
	xmldata = Element("xmldata")
	xmldata.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
	xmldata.attrib["xsi:noNamespaceSchemaLocation"] = "mm_xmldata_3.0.xsd"
	xmldata.attrib["version"] = "3.0"
	xmldata.append(self.action.ToElement())

	return xmldata

class Genres(object):
    def __init__(self):
	self.standard = ''
	self.level1 = []
	self.level2 = []

    def ToElement(self):
	Genres = Element("genres")
	Genres.attrib["standard"] = self.standard
	

	for level1 in self.level1:
	    tmp = Element("level1")
	    tmp.text = level1    
	    Genres.append(tmp)

	for level2 in self.level2:
	    tmp = Element("level2")
	    tmp.text = level2
	    Genres.append(tmp)

	return Genres


class AssetData(object):
    def __init__(self):
	self.lang = ''
	self.data     = Data()
	self.images   = Images()
	self.ratings  = Ratings()
	self.chapters = Chapters()
	self.genres   = Genres()

    def ToElement(self):
	assetData = Element("assetData")
	assetData.attrib["lang"] = self.lang
	assetData.append(self.data.ToElement())
	assetData.append(self.images.ToElement())
	assetData.append(self.ratings.ToElement())
	assetData.append(self.genres.ToElement())
	assetData.append(self.chapters.ToElement())

	return assetData

class Data (object):
    def __init__(self):
        self.title=''
	self.subtitle=''
	self.originalTitle=''
	self.descriptionShort=''
	self.descriptionLong=''
	self.keywords=''
	self.links=''
	self.copyright=''
	self.distribution=''
	self.releaseDateCinema=''
	self.eanCode=''
	self.isChildrenMovie=''
	self.country=''
	self.year=''
	self.runtime=''
	self.productionCompany=''
	self.producer=''
	self.director=''
	self.scriptwriter=''
	self.cast=''
	self.awards=''
	self.label=''
	self.contractor=''


    def ToElement(self):
	title=Element("title")
	subtitle=Element("subtitle")
	originalTitle=Element("originalTitle")
	descriptionShort=Element("descriptionShort")
	descriptionLong=Element("descriptionLong")
	keywords=Element("keywords")
	links=Element("links")
	copyright=Element("copyright")
	distribution=Element("distribution")
	releaseDateCinema=Element("releaseDateCinema")
	eanCode=Element("eanCode")
	isChildrenMovie=Element("isChildrenMovie")
	country=Element("country")
	year=Element("year")
	runtime=Element("runtime")
	productionCompany=Element("productionCompany")
	producer=Element("producer")
	director=Element("director")
	scriptwriter=Element("scriptwriter")
	cast=Element("cast")
	awards=Element("awards")
	label=Element("label")
	contractor=Element("contractor")


	title.text="<![CDATA[ " + self.title+" ]]>"
	subtitle.text="<![CDATA[ " + self.subtitle+" ]]>"
	originalTitle.text="<![CDATA[ " + self.originalTitle+" ]]>"
	descriptionShort.text="<![CDATA[ " + self.descriptionShort+" ]]>"
	descriptionLong.text="<![CDATA[ " + self.descriptionLong+" ]]>"
	keywords.text="<![CDATA[ " + self.keywords+" ]]>"
	links.text="<![CDATA[ " + self.links+" ]]>"
	copyright.text="<![CDATA[ " + self.copyright+" ]]>"
	distribution.text="<![CDATA[ " + self.distribution+" ]]>"
	releaseDateCinema.text="<![CDATA[ " + self.releaseDateCinema+" ]]>"
	eanCode.text="<![CDATA[ " + self.eanCode+" ]]>"
	isChildrenMovie.text = self.isChildrenMovie
	country.text="<![CDATA[ " + self.country+" ]]>"
	year.text="<![CDATA[ " + self.year+" ]]>"
	runtime.text = self.runtime
	productionCompany.text="<![CDATA[ " + self.productionCompany+" ]]>"
	producer.text="<![CDATA[ " + self.producer+" ]]>"
	director.text="<![CDATA[ " + self.director+" ]]>"
	scriptwriter.text="<![CDATA[ " + self.scriptwriter+" ]]>"
	cast.text="<![CDATA[ " + self.cast+" ]]>"
	awards.text="<![CDATA[ " + self.awards+" ]]>"
	label.text="<![CDATA[ " + self.label+" ]]>"
	contractor.text="<![CDATA[ " + self.contractor+" ]]>"

	data= Element("data")
	data.append(title)
	data.append(subtitle)
	data.append(originalTitle)
	data.append(descriptionShort)
	data.append(descriptionLong)
	data.append(keywords)
	data.append(links)
	data.append(copyright)
	data.append(distribution)
	data.append(releaseDateCinema)
	data.append(eanCode)
	data.append(isChildrenMovie)
	data.append(country)
	data.append(runtime)
	data.append(year)
	data.append(productionCompany)
	data.append(producer)
	data.append(director)
	data.append(scriptwriter)
	data.append(cast)
	data.append(awards)
	data.append(label)
	data.append(contractor)

	return data




class Ratings(object):
    def __init__(self):
	self.general	= ''
	self.fun	= ''
	self.action	= ''
	self.erotic	= ''
	self.tension	= ''
	self.emotion	= ''


    def ToElement(self):
	Ratings = Element("ratings")
	General	= Element("general")
	Fun	= Element("fun")
	Action	= Element("action")
	Erotic	= Element("erotic")
	Tension	= Element("tension")
	Emotion	= Element("emotion")

	General.text 	= self.general
	Fun.text	= self.fun
	Action.text	= self.action
	Erotic.text	= self.erotic
	Tension.text	= self.tension
	Emotion.text	= self.emotion

	Ratings.append(General)
	Ratings.append(Fun)
	Ratings.append(Action)
	Ratings.append(Erotic)
	Ratings.append(Tension)
	Ratings.append(Emotion)

	return Ratings


class Images(object):
    def __init__(self):
	self.image = []

    def AddImage(self, type, imageFile,title,copyright):
	self.image.append(Image(type,imageFile,title,copyright))

    def ToElement(self):
	images = Element("images")
	for image in self.image:
	    images.append(image.ToElement())

	return images

class Image(object):
    def __init__(self, type='', imageFile='',title='',copyright=''):
	self.type 	= type
	self.imageFile 	= imageFile
	self.title 	= title
	self.copyright	= copyright

    def ToElement(self):
	Image = Element("image")
	Image.attrib["type"] = self.type

	ImageFile 	= Element("imageFile")
	ImageFile.text 	= self.imageFile
	Title		= Element("title")
	Title.text	= "<![CDATA[ " + self.title + " ]]>"
	CopyRight	= Element("copyright")
	CopyRight.text  = "<![CDATA[ " + self.copyright + " ]]>"

	Image.append(ImageFile)
	Image.append(Title)
	Image.append(CopyRight)

	return Image


class Asset (object):
    def __init__(self):
	self.cpId=''
	self.clipId=''
	self.clipFile=''
	self.clipData=''
	self.clipCategory=''
	self.clipUsage=''
	self.clipDuration=''
	self.clipOriginalId=''
	self.clipAudioTracks = ClipAudioTracks()

    def ToElement(self):
	cpId=Element("cpId")
	clipId=Element("clipId")
	clipFile=Element("clipFile")
	clipData=Element("clipData")
	clipCategory=Element("clipCategory")
	clipUsage=Element("clipUsage")
	clipDuration=Element("clipDuration")
	clipOriginalId=Element("clipOriginalId")


	cpId.text=self.cpId
	clipId.text=self.clipId
	clipFile.text=self.clipFile
	clipData.text=self.clipData
	clipCategory.text=self.clipCategory
	clipUsage.text=self.clipUsage
	clipDuration.text=self.clipDuration
	clipOriginalId.text=self.clipOriginalId
	
	asset= Element("asset")
	asset.append(cpId)
	asset.append(clipId)
	asset.append(clipFile)
	asset.append(clipData)
	asset.append(clipCategory)
	asset.append(clipUsage)
	asset.append(clipDuration)
	asset.append(clipOriginalId)
	asset.append(self.clipAudioTracks.ToElement())

	return asset


class Chapter(object):
    def __init__(self,no='',title='',timecode=''):
	self.no       = no
	self.title    = title
	self.timecode = timecode

    def ToElement(self):
	chapter = Element("chapter")
	chapter.attrib["no"] = self.no
	title	= Element("title")
	title.text = "<![CDATA[ " + self.title + "]]>"
	timecode = Element("timecode")
	timecode.text = self.timecode

	chapter.append(title)
	chapter.append(timecode)

	return chapter

class Chapters(object):
    def __init__(self):
	self.chapters = []

    def AddChapter(self,no,title,timecode):
	self.chapters.append(Chapter(no,title,timecode))

    def ToElement(self):
	chapters = Element("chapters")
	for chapter in self.chapters:
	    chapters.append(chapter.ToElement())

	return chapters

class ClipAudioTrack(object):
    def __init__(self, no='', lang='', soundmix='', sorting=''):
	self.no = no
	self.lang= lang
	self.soundmix= soundmix
	self.sorting= sorting

    def ToElement(self):
	clipAudioTrack = Element("clipAudioTrack")
	clipAudioTrack.attrib["no"] = self.no
	clipAudioTrack.attrib["lang"] = self.lang
	clipAudioTrack.attrib["soundmix"] = self.soundmix
	clipAudioTrack.attrib["sorting"] = self.sorting

	return clipAudioTrack

class ClipAudioTracks(object):
    def __init__(self):
	self.clipAudioTrack = []

    def AddClipAudioTrack(self, no, lang, soundmix, sorting):
	self.clipAudioTrack.append(ClipAudioTrack(no,lang,soundmix,sorting))

    def ToElement(self):

	clipAudioTracks = Element("clipAudioTracks")
	for clipAudioTrack in self.clipAudioTrack:
	    clipAudioTracks.append(clipAudioTrack.ToElement())

	return clipAudioTracks


class Project (object):
    def __init__(self):
	self.projectId=''
	self.adultRating=''
	self.onlineFrom=''
	self.onlineUntil=''
	self.priceId=''

    def ToElement(self):
	projectId=Element("projectId")
	adultRating=Element("adultRating")
	onlineFrom=Element("onlineFrom")
	onlineUntil=Element("onlineUntil")
	priceId=Element("priceId")


        projectId.text=self.projectId
	adultRating.text=self.adultRating
	onlineFrom.text=self.onlineFrom
	onlineUntil.text=self.onlineUntil
	priceId.text=self.priceId


	project= Element("project")
	project.append(projectId)
	project.append(adultRating)
	project.append(onlineFrom)
	project.append(onlineUntil)
	project.append(priceId)

	return project

