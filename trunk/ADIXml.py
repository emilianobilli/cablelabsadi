from ElementTree import *


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

#
# App_Data_Element(): Crea un Elemento de la forma:
#
# <App_Data App="" Name="" Value=""/>
#
# Y lo rellena con los valores pasados por parametro
#
# Retorna: El Elemento creado
#
def App_Data_Element(App=u'', Name=u'', Value=u'', Target_Language=u'', Target_Country=u''):
    App_Data = Element("App_Data")
    
    App_Data.attrib["App"]   = App
    if Target_Language != '':
	App_Data.attrib["Target_Language"] = Target_Language

    if Target_Country  != '':
	App_Data.attrib["Target_Country"]  = Target_Country
    App_Data.attrib["Name"]  = Name    
    App_Data.attrib["Value"] = Value


    return App_Data

#
# AMS_Element(): Crea un Elemento de la forma:
#
# <AMS Provider=""
#      Product=""
#      Asset_Name=""
#      Version_Major=""
#      Version_Minor=""
#      Description=""
#      Creation_Date=""
#      Provider_ID=""
#      Asset_ID=""
#      Asset_Class=""
#  />
#
# Rellena los valores con los atributos del Objeto de la clase AMS
#
# Retorna: El Elemento creado
#   
def AMS_Element(AMSData = None):
    if AMSData is not None:
        AMS = Element("AMS")
        AMS.attrib["Provider"]      = AMSData.Provider
        AMS.attrib["Product"]       = AMSData.Product
        AMS.attrib["Asset_Name"]    = AMSData.Asset_Name
        AMS.attrib["Version_Major"] = AMSData.Version_Major
        AMS.attrib["Version_Minor"] = AMSData.Version_Minor
        AMS.attrib["Description"]   = AMSData.Description
        AMS.attrib["Creation_Date"] = AMSData.Creation_Date
        AMS.attrib["Provider_ID"]   = AMSData.Provider_ID
        AMS.attrib["Asset_ID"]      = AMSData.Asset_ID
        AMS.attrib["Asset_Class"]   = AMSData.Asset_Class
        return AMS

#
# Attrib_fromElement(): 
#
def Attrib_fromElement(element, attrib):
    return (u'', element.get(attrib))[element.get(attrib) is not None]

#
# NameValue_fromApp_DataElement():
#

def NameValue_fromApp_DataElement(App_DataElement = None):
    if App_DataElement is not None:
        Name  = Attrib_fromElement(App_DataElement, "Name") 
        Value = Attrib_fromElement(App_DataElement, "Value")
        return (Name, Value)    

    return (u'', u'')


def AssetElementList_fromTitleElement(TitleElement = None):
    ret = None
    if TitleElement is not None:
        ret = TitleElement.findall("Asset")

    return ret
    

def AMS_fromElement(AMS_Element = None):
    if AMS_Element is not None:
        AMSData = AMS()
        AMSData.Provider	=	Attrib_fromElement(AMS_Element,"Provider")	
        AMSData.Product		=	Attrib_fromElement(AMS_Element,"Product")	
        AMSData.Asset_Name	=       Attrib_fromElement(AMS_Element,"Asset_Name")	
        AMSData.Version_Major	=	Attrib_fromElement(AMS_Element,"Version_Major")	
        AMSData.Version_Minor	=	Attrib_fromElement(AMS_Element,"Version_Minor")	
        AMSData.Description	=	Attrib_fromElement(AMS_Element,"Description")	
        AMSData.Creation_Date	=	Attrib_fromElement(AMS_Element,"Creation_Date")	
        AMSData.Provider_ID	=	Attrib_fromElement(AMS_Element,"Provider_ID")	
        AMSData.Asset_ID	=	Attrib_fromElement(AMS_Element,"Asset_ID")	
        AMSData.Asset_Class	=	Attrib_fromElement(AMS_Element,"Asset_Class")	
        return AMSData
    
        


class AMS(object):
    def __init__(self, Asset_Class=None):
        self.Provider      = u''
        self.Product       = u''        # 20 Chars
        self.Asset_Name    = u''        # 50 Chars
        self.Version_Major = u'1'
        self.Version_Minor = u'0'
        self.Description   = u''        
        self.Creation_Date = u''
        self.Provider_ID   = u''        
        self.Asset_ID      = u''        # 20 Chars 4 alfa Chars and 16 numbers
        self.Asset_Class = Asset_Class


class Media(object):
    def __init__(self, Asset_Class=None, App_Data_App=None, toBuild=True):
        if Asset_Class is not None and toBuild==True:
            self.AMS = AMS(Asset_Class)
        else:
            self.AMS = None
        self.App_Data_App = App_Data_App
        self.Type         = Asset_Class
        self.Content_FileSize = u''
        self.Content_CheckSum = u''
        self.Content_Value    = u''

	self.Custom_Metadata = []


class StillImage(Media):
    def __init__(self, Asset_Class=None, App_Data_App=None, toBuild=True):
        super(StillImage,self).__init__(Asset_Class, App_Data_App,toBuild)
        self.Image_Aspect_Ratio = u''


    def AssetElement(self):
        Asset    = Element("Asset")
        Content  = Element("Content")
        Metadata = Element("Metadata")

        AMS = AMS_Element(self.AMS)
        Metadata.append(AMS)
        Metadata.append(App_Data_Element(self.App_Data_App, "Type", self.Type))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_FileSize", self.Content_FileSize))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_CheckSum", self.Content_CheckSum))
	
		#
	# Custom Metadata ??? Agregale tu campo custom al XML
	#
	for CM in self.Custom_Metadata:
	    Metadata.append(App_Data_Element(self.App_Data_App, CM.Name, CM.Value, CM.Target_Language, CM.Target_Contry))
	
	if self.Image_Aspect_Ratio != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Image_Aspect_Ratio", self.Image_Aspect_Ratio))

        Content.attrib["Value"] = self.Content_Value
        
        Asset.append(Metadata)
        Asset.append(Content)

        return Asset

    def AddCustomMetadata(self, Name = None, Value = None, Target_Language=u'', Target_Country=u''):
	if Name is not None and Value is not None:
	    self.Custom_Metadata.append(CustomMetadata(Name,Value,Target_Language, Target_Country))

class Poster(StillImage):
    def __init__(self, App_Data_App=None, toBuild=True):
        super(Poster,self).__init__("poster", App_Data_App, toBuild)

class BoxCover(StillImage):
    def __init__(self, App_Data_App=None, toBuild=True):
        super(BoxCover,self).__init__("box cover", App_Data_App, toBuild)


class Preview(Media):
    def __init__(self, App_Data_App=None, toBuild=True):
	super(Preview,self).__init__("preview", App_Data_App, toBuild)
	self.Audio_Type		    = u''
	self.Resolution		    = u''
	self.Frame_Rate		    = u''
	self.Codec		    = u''
	self.Bit_Rate		    = u''
	self.Run_Time		    = u''
	self.Rating		    = u''
	
    def AssetElement(self):
        Asset    = Element("Asset")
        Content  = Element("Content")
        Metadata = Element("Metadata")

        AMS = AMS_Element(self.AMS)
        Metadata.append(AMS)

	#
	# Campos de Metadata Obligatorios
	#

        Metadata.append(App_Data_Element(self.App_Data_App, "Type", self.Type))
	Metadata.append(App_Data_Element(self.App_Data_App, "Audio_Type", self.Audio_Type))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_FileSize", self.Content_FileSize))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_CheckSum", self.Content_CheckSum))
	Metadata.append(App_Data_Element(self.App_Data_App, "Rating", self.Rating))

        #
	# Campos de Metadata Obligatorios pero agregados en 2009 (Algunas plataformas no lo soportan) 
	#
	if self.Resolution != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Resolution", self.Resolution))
	if self.Frame_Rate != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Frame_Rate", self.Frame_Rate))
	if self.Codec != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Codec", self.Codec))
        if self.Bit_Rate != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Bit_Rate", self.Bit_Rate))
	if self.Run_Time != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Run_Time", self.Run_Time))
	    
	Content.attrib["Value"] = self.Content_Value
        
        Asset.append(Metadata)
        Asset.append(Content)

	return Asset


class Movie(Media):
    def __init__(self, App_Data_App=None, toBuild=True):
        super(Movie,self).__init__("movie", App_Data_App, toBuild)
        self.Audio_Type             = u''
        self.Resolution             = u''
        self.Frame_Rate             = u''
        self.Codec                  = u'' 
        self.Bit_Rate               = u''
	self.Screen_Format          = u''
	self.Viewing_Can_Be_Resumed = u''
	self.Watermarking           = u''
	self.Languages              = u''
	self.Copy_Protection        = u''
	


    def AddCustomMetadata(self, Name = None, Value = None, Target_Language=u'', Target_Country=u''):
	if Name is not None and Value is not None:
	    self.Custom_Metadata.append(CustomMetadata(Name,Value, Target_Language, Target_Country))


    def AssetElement(self):
        Asset    = Element("Asset")
        Content  = Element("Content")
        Metadata = Element("Metadata")

        AMS = AMS_Element(self.AMS)
        Metadata.append(AMS)

	#
	# Campos de Metadata Obligatorios
	#

        Metadata.append(App_Data_Element(self.App_Data_App, "Type", self.Type))
	Metadata.append(App_Data_Element(self.App_Data_App, "Audio_Type", self.Audio_Type))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_FileSize", self.Content_FileSize))
        Metadata.append(App_Data_Element(self.App_Data_App, "Content_CheckSum", self.Content_CheckSum))


	#
	# Custom Metadata ??? Agregale tu campo custom al XML
	#
	for CM in self.Custom_Metadata:
	    Metadata.append(App_Data_Element(self.App_Data_App, CM.Name, CM.Value, CM.Target_Language, CM.Target_Country))


        #
	# Campos de Metadata Obligatorios pero agregados en 2009 (Algunas plataformas no lo soportan) 
	#
	if self.Resolution != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Resolution", self.Resolution))
	if self.Frame_Rate != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Frame_Rate", self.Frame_Rate))
	if self.Codec != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Codec", self.Codec))
        if self.Bit_Rate != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Bit_Rate", self.Bit_Rate))

	#
	# Campos de Metadata Opcionales
	#
	if self.Screen_Format != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Screen_Format", self.Screen_Format))
        if self.Viewing_Can_Be_Resumed != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Viewing_Can_Be_Resumed", self.Viewing_Can_Be_Resumed))
        if self.Watermarking != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Watermarking", self.Watermarking))
        if self.Languages != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Languages", self.Languages))
        if self.Copy_Protection != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Copy_Protection", self.Copy_Protection))
       


        Content.attrib["Value"] = self.Content_Value
        
        Asset.append(Metadata)
        Asset.append(Content)


        
        return Asset


def Package_fromADIFile(ADIFile=None):
    if ADIFile is not None:
        p = Package_fromElement(parse(ADIFile))
        return p

    return None

def Package_toADIFile(package=None, ADIFile=None, Version='1.1', doctype=None):
    if package is not None:
	#
	# Bug a corregir
	#
	package.AMS.Asset_Name = package.AMS.Asset_Name + '_package'
	#
	# End Bug
	#
        ADIElement = package.AdiElement()
        if ADIElement is not None:
	    indent(ADIElement)
            AdiString = tostring(ADIElement, encoding="ISO-8859-1", doctype=doctype)
	    if ADIFile is not None:
        	if Version == '1.1':
		    fd = open(ADIFile, "wb")
        	    fd.write(AdiString)
		    fd.close()
		    return True
		
	    else:
		return AdiString
            

def Package_fromElement(ADIElement=None):

    package = None

    if ADIElement is not None:
        package = Package(toBuild=False)

        #
        # Busca y Carga AMS del Package
        #
        AmsElement = ADIElement.find("Metadata/AMS")
#        dump(AmsElement)
        if AmsElement is not None:
            package.AMS = AMS_fromElement(AmsElement)
            
        App_DataElementList = ADIElement.findall("Metadata/App_Data")

        first = True
        for App_DataElement in App_DataElementList:
            if first:
                package.App_Data_App = Attrib_fromElement(App_DataElement,"App")
                first = False

            Name, Value  = NameValue_fromApp_DataElement(App_DataElement)
            
            if Name == "Metadata_Spec_Version":
                package.Metadata_Spec_Version = Value
            elif Name == "Provider_Content_Tier":
                package.Provider_Content_Tier = Value

        TitleElement = ADIElement.find("Asset")


        package.Title = Title_fromElement(TitleElement)

        AssetElementList = AssetElementList_fromTitleElement(TitleElement)
        
        for AssetElement in AssetElementList:

            Asset = AssetMedia_fromElement(AssetElement)

#            print Asset
            if Asset.AMS.Asset_Class == "movie":
                package.Movie = Asset
            else:
                package.StillImage = Asset
    

    return package                


def Title_fromElement(TitleElement=None):
    title = None

    if TitleElement is not None:

        title = Title(toBuild=False)

        AmsElement = TitleElement.find("Metadata/AMS")
        
        if AmsElement is not None:
            title.AMS = AMS_fromElement(AmsElement)

        App_DataElementList = TitleElement.findall("Metadata/App_Data")

        first = True
        for App_DataElement in App_DataElementList:

            if first == True:
                title.App_Data_App = Attrib_fromElement(App_DataElement, "App")
                first = False

            Name,Value = NameValue_fromApp_DataElement(App_DataElement)

            if Name == "Title_Sort_Name":
                title.Title_Sort_Name = Value
            if Name == "Title_Brief":
                title.Title_Brief = Value
            if Name == "Title":
                title.Title = Value
            if Name == "Type":
                title.Type = Value
            if Name == "Episode_Name":
                title.Episode_Name = Value
            if Name == "Episode_ID":
                title.Episode_ID = Value
            if Name == "Summary_Long":
                title.Summary_Long = Value
            if Name == "Summary_Medium":
                title.Summary_Medium = Value
            if Name == "Summary_Short":
                title.Summary_Short = Value
            if Name == "Rating":
                title.Rating = Value
            if Name == "Advisories":
                title.Advisories = Value
            if Name == "Closed_Captioning":
                title.Closed_Captioning = Value
            if Name == "Run_Time":
                title.Run_Time = Value
            if Name == "Display_Run_Time":
                title.Display_Run_Time = Value
            if Name == "Year":
                title.Year = Value
            if Name == "Country_of_Origin":
                title.Country_of_Origin = Value
            if Name == "Actors":
                title.Actors = Value
            if Name == "Actors_Display":
                title.Actors_Display = Value
            if Name == "Writer_Display":
                title.Writer_Display = Value
            if Name == "Director":
                title.Director = Value
            if Name == "Producers":
                title.Producers = Value
            if Name == "Studio":
                title.Studio = Value
            if Name == "Category":
                title.Category = Value
            if Name == "Genre":
                title.Genre = Value
            if Name == "Show_Type":
                title.Show_Type = Value
            if Name == "Season_Premiere":
                title.Season_Premiere = Value
            if Name == "Season_Finale":
                title.Season_Finale = Value
            if Name == "Box_Office":
                title.Box_Office = Value
            if Name == "Propagation_Priority":
                title.Propagation_Priority = Value
            if Name == "Billing_ID":
                title.Billing_ID = Value
            if Name == "Licensing_Window_Start":
                title.Licensing_Window_Start = Value
            if Name == "Licensing_Window_End":
                title.Licensing_Window_End = Value
            if Name == "Preview_Period":
                title.Preview_Period = Value
            if Name == "Home_Video_Window":
                title.Home_Video_Window = Value
            if Name == "Display_As_New":
                title.Display_As_New = Value
            if Name == "Display_As_Last_Chance":
                title.Display_As_Last_Chance = Value
            if Name == "Maximum_Viewing_Length":
                title.Maximum_Viewing_Length = Value
            if Name == "Provider_QA_Contact":
                title.Provider_QA_Contact = Value
            if Name == "Contract_Name":
                title.Contract_Name = Value
            if Name == "Suggested_Price":
                title.Suggested_Price = Value
            if Name == "Distributor_Royalty_Percent":
                title.Distributor_Royalty_Percent = Value
            if Name == "Distributor_Royalty_Minimum":
                title.Distributor_Royalty_Minimum = Value
            if Name == "Distributor_Royalty_Flat_Rate":
                title.Distributor_Royalty_Flat_Rate = Value
            if Name == "Distributor_Name":
                title.Distributor_Name = Value
            if Name == "Studio_Royalty_Percent":
                title.Studio_Royalty_Percent = Value
            if Name == "Studio_Royalty_Minimum":
                title.Studio_Royalty_Minimum = Value
            if Name == "Studio_Royalty_Flat_Rate":
                title.Studio_Royalty_Flat_Rate = Value
            if Name == "Studio_Name":
                title.Studio_Name = Value
            if Name == "Studio_Code":
                title.Studio_Code = Value
            if Name == "Subscriber_View_Limit":
                title.Subscriber_View_Limit = Value
            if Name == "Programmer_Call_Letters":
                title.Programmer_Call_Letters = Value
            if Name == "Recording_Artist":
                title.Recording_Artist = Value
            if Name == "Song_Title":
                title.Song_Tile = Value
                
    return title
                
def AssetMedia_fromElement(AssetElement=None):

    asset = None

    if AssetElement is not None:

        AmsElement = AssetElement.find("Metadata/AMS")

        if AmsElement is not None:
                Ams = AMS_fromElement(AmsElement)


#                print Ams.Asset_Class
                if Ams.Asset_Class == "movie":
                    asset = Movie(toBuild=False)
                    asset.AMS = Ams

                    App_DataElementList = AssetElement.findall("Metadata/App_Data")

                    first = True
                    for App_DataElement in App_DataElementList:
                        if first:
                            asset.App_Data_App = Attrib_fromElement(App_DataElement,"App")
                            first = False

                        Name, Value  = NameValue_fromApp_DataElement(App_DataElement)

                        if Name == "Type":
                            asset.Type = Value
                        if Name == "Content_FileSize":
                            asset.Content_FileSize = Value
                        if Name == "Content_CheckSum":
                            asset.Content_CheckSum = Value
                        if Name == "Audio_Type":
                            asset.Audio_Type = Value
                        if Name == "Resolution":
                            asset.Resolution = Value
                        if Name == "Frame_Rate":
                            asset.Frame_Rate = Value
                        if Name == "Bit_Rate":
                            asset.Bit_Rate = Value
			if Name == "Screen_Format":
			    asset.Screen_Format = Value
			if Name == "Viewing_Can_Be_Resumed":
			    asset.Viewing_Can_Be_Resumed = Value
			if Name == "Watermarking":
			    asset.Watermarking = Value
			if Name == "Languages":
			    asset.Languages = Value
			if Name == "Copy_Protection":
			    asset.Copy_Protection = Value
			



                    ContentElement = AssetElement.find("Content")
                    if ContentElement is not None:
                        asset.Content_Value = Attrib_fromElement(ContentElement, "Value")    

                      
                elif Ams.Asset_Class == "poster" or Ams.Asset_Class == "box cover":
                    asset = StillImage(toBuild=False)
                    asset.AMS = Ams

                    App_DataElementList = AssetElement.findall("Metadata/App_Data")

                    first = True
                    for App_DataElement in App_DataElementList:
                        if first:
                            asset.App_Data_App = Attrib_fromElement(App_DataElement,"App")
                            first = False

                        Name, Value  = NameValue_fromApp_DataElement(App_DataElement)

                        if Name == "Type":
                            asset.Type = Value
                        if Name == "Content_FileSize":
                            asset.Content_FileSize = Value
                        if Name == "Content_CheckSum":
                            asset.Content_CheckSum = Value


                    ContentElement = AssetElement.find("Content")
                    if ContentElement is not None:
                        asset.Content_Value = Attrib_fromElement(ContentElement, "Value")

        return asset
    
               
class Package(object):
    def __init__(self, 
                 Provider = u'',
                 Product  = u'',                
                 Asset_Name    = u'',
                 Description   = u'',
                 Creation_Date = u'',
                 Provider_ID   = u'',
                 Asset_ID      = u'',
                 App_Data_App  = None, toBuild=True):

        if toBuild == True:
            self.AMS = AMS("package")
            self.AMS.Provider      = Provider
            self.AMS.Product       = Product
            self.AMS.Asset_Name    = Asset_Name
            self.AMS.Description   = Description
            self.AMS.Creation_Date = Creation_Date
            self.AMS.Provider_ID   = Provider_ID
            self.AMS.Asset_ID      = Asset_ID

            self.App_Data_App = App_Data_App
            if self.App_Data_App is None:
                return None

        else:
            self.AMS = None

        
        self.Metadata_Spec_Version = u'CableLabsVOD1.1'
        self.Provider_Content_Tier = u''

        self.Title = None

	self.Preview = None

        self.Movie = None

        self.StillImage = None



    def AdiElement(self):
        ADI      = Element("ADI")
        Metadata = Element("Metadata")
        
        AMS = AMS_Element(self.AMS)
        Metadata.append(AMS)
        Metadata.append(App_Data_Element(self.App_Data_App, "Metadata_Spec_Version", self.Metadata_Spec_Version))
	if self.Provider_Content_Tier != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Provider_Content_Tier", self.Provider_Content_Tier))

        ADI.append(Metadata)
        if self.Title is not None:
            Asset_Title = self.Title.AssetElement()

            if self.Movie is not None:
                Asset_Movie = self.Movie.AssetElement()
                Asset_Title.append(Asset_Movie)

            if self.StillImage is not None:
                Asset_Image = self.StillImage.AssetElement()
                Asset_Title.append(Asset_Image)

	    if self.Preview is not None:
		Asset_Preview = self.Preview.AssetElement()
		Asset_Title.append(Asset_Preview)

            ADI.append(Asset_Title)
        
        
        return ADI

    
    def AddPreview(self):
	self.Preview = Preview(self.App_Data_App)

	self.Preview.AMS.Provider      = self.AMS.Provider
        self.Preview.AMS.Product       = self.AMS.Product
        self.Preview.AMS.Asset_Name    = self.AMS.Asset_Name + "_preview"
        self.Preview.AMS.Description   = self.AMS.Description
        self.Preview.AMS.Creation_Date = self.AMS.Creation_Date
        self.Preview.AMS.Provider_ID   = self.AMS.Provider_ID
        self.Preview.AMS.Asset_ID      = self.AMS.Asset_ID

        

    def AddTitle(self):
        self.Title = Title(self.App_Data_App)
        
        self.Title.AMS.Provider      = self.AMS.Provider
        self.Title.AMS.Product       = self.AMS.Product
        self.Title.AMS.Asset_Name    = self.AMS.Asset_Name + "_title"
        self.Title.AMS.Description   = self.AMS.Description
        self.Title.AMS.Creation_Date = self.AMS.Creation_Date
        self.Title.AMS.Provider_ID   = self.AMS.Provider_ID
        self.Title.AMS.Asset_ID      = self.AMS.Asset_ID

        
    def AddMovie(self):
        self.Movie = Movie(self.App_Data_App)

        self.Movie.AMS.Provider      = self.AMS.Provider
        self.Movie.AMS.Product       = self.AMS.Product
        self.Movie.AMS.Asset_Name    = self.AMS.Asset_Name + "_movie"
        self.Movie.AMS.Description   = self.AMS.Description
        self.Movie.AMS.Creation_Date = self.AMS.Creation_Date
        self.Movie.AMS.Provider_ID   = self.AMS.Provider_ID
        self.Movie.AMS.Asset_ID      = self.AMS.Asset_ID

    def AddStillImage(self, Type = None):
        if Type == "poster":
                self.StillImage = Poster(self.App_Data_App)
                self.StillImage.AMS.Asset_Name = self.AMS.Asset_Name + "_poster"

        else:
                self.StillImage = BoxCover(self.App_Data_App)
                self.StillImage.AMS.Asset_Name = self.AMS.Asset_Name + "_box_cover"

        self.StillImage.AMS.Provider      = self.AMS.Provider
        self.StillImage.AMS.Product       = self.AMS.Product
        self.StillImage.AMS.Description   = self.AMS.Description
        self.StillImage.AMS.Creation_Date = self.AMS.Creation_Date
        self.StillImage.AMS.Provider_ID   = self.AMS.Provider_ID
        self.StillImage.AMS.Asset_ID      = self.AMS.Asset_ID
        
        
    def AddPoster(self):
        self.AddStillImage("poster")


    def AddBoxCover(self):
        self.AddStillImage("box_cover")


class CustomMetadata(object):
    def __init__(self, Name = None, Value = None, Target_Language = u'', Target_Country = u''):
	self.Name  = Name
	self.Value = Value
	self.Target_Language = Target_Language
	self.Target_Country  = Target_Country	

class Title(object):
    def __init__(self,App_Data_App=None, toBuild=True):
        if toBuild == False:
            self.AMS = None
        else:
            self.AMS          = AMS("title")

        self.App_Data_App = App_Data_App

        self.Title_Sort_Name = u''
        self.Title_Brief = u''
        self.Title = u''
        self.Type = u'title'
        self.Episode_Name = u''
        self.Episode_ID = u''
        self.Summary_Long = u''
        self.Summary_Medium = u''
        self.Summary_Short = u''
        self.Rating = u''
        self.Advisories = u''
        self.Closed_Captioning = u''
        self.Run_Time = u''
        self.Display_Run_Time = u''
        self.Year = u''
        self.Country_of_Origin = u''
        self.Actors = u''
        self.Actors_Display = u''
        self.Writer_Display = u''
        self.Director = u''
        self.Producers = u''
        self.Studio = u''
        self.Category = u''
        self.Genre = u''
        self.Show_Type = u''
        self.Season_Premiere = u''
        self.Season_Finale = u''
        self.Box_Office = u''
        self.Propagation_Priority = u''
        self.Billing_ID = u''
        self.Licensing_Window_Start = u''
        self.Licensing_Window_End = u''
        self.Preview_Period = u''
        self.Home_Video_Window = u''
        self.Display_As_New = u''
        self.Display_As_Last_Chance = u''
        self.Maximum_Viewing_Length = u''
        self.Provider_QA_Contact = u''
        self.Contract_Name = u''
        self.Suggested_Price = u''
        self.Distributor_Royalty_Percent = u''
        self.Distributor_Royalty_Minimum = u''
        self.Distributor_Royalty_Flat_Rate = u''
        self.Distributor_Name = u''
        self.Studio_Royalty_Percent = u''
        self.Studio_Royalty_Minimum = u''
        self.Studio_Royalty_Flat_Rate = u''
        self.Studio_Name = u''
        self.Studio_Code = u''
        self.Subscriber_View_Limit = u''
        self.Programmer_Call_Letters = u''
        self.Recording_Artist = u''
        self.Song_Title = u''
        self.Target_Language = u''
        self.Target_Country  = u''
        

	self.Custom_Metadata = []

    #
    # Agrega Metadata que no existe en Cablelabs --- HardCode ---
    #
    def AddCustomMetadata(self, Name = None, Value = None, Target_Language =u'', Target_Country = u''):
	if Name is not None and Value is not None:
	    self.Custom_Metadata.append(CustomMetadata(Name,Value, Target_Language, Target_Country))

    def AssetElement(self):

        Asset    = Element("Asset")

        Metadata = Element("Metadata")
        AMS = AMS_Element(self.AMS)
        Metadata.append(AMS)


	#
	# Custom Metadata ??? Agregale tu campo custom al XML
	#
	for CM in self.Custom_Metadata:
	    Metadata.append(App_Data_Element(self.App_Data_App, CM.Name, CM.Value, CM.Target_Language, CM.Target_Country))


	#
	# Campos Requeridos
	# 
	Metadata.append(App_Data_Element(self.App_Data_App, "Type",self.Type))
	Metadata.append(App_Data_Element(self.App_Data_App, "Title_Brief",self.Title_Brief, self.Target_Language))
        Metadata.append(App_Data_Element(self.App_Data_App, "Title",self.Title, self.Target_Language))
	Metadata.append(App_Data_Element(self.App_Data_App, "Summary_Short",self.Summary_Short, self.Target_Language))
	Metadata.append(App_Data_Element(self.App_Data_App, "Rating",self.Rating, '', self.Target_Country))
	Metadata.append(App_Data_Element(self.App_Data_App, "Closed_Captioning",self.Closed_Captioning))
        Metadata.append(App_Data_Element(self.App_Data_App, "Run_Time",self.Run_Time))
        Metadata.append(App_Data_Element(self.App_Data_App, "Display_Run_Time",self.Display_Run_Time))
        Metadata.append(App_Data_Element(self.App_Data_App, "Year",self.Year))
	Metadata.append(App_Data_Element(self.App_Data_App, "Category",self.Category))
        Metadata.append(App_Data_Element(self.App_Data_App, "Genre",self.Genre, self.Target_Language))
	Metadata.append(App_Data_Element(self.App_Data_App, "Show_Type",self.Show_Type))
        Metadata.append(App_Data_Element(self.App_Data_App, "Licensing_Window_Start",self.Licensing_Window_Start))
        Metadata.append(App_Data_Element(self.App_Data_App, "Licensing_Window_End",self.Licensing_Window_End))
	Metadata.append(App_Data_Element(self.App_Data_App, "Preview_Period",self.Preview_Period))
	Metadata.append(App_Data_Element(self.App_Data_App, "Provider_QA_Contact",self.Provider_QA_Contact))


	#
	# Campos Opcionales
	#
	if self.Billing_ID != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Billing_ID", self.Billing_ID))
	if self.Title_Sort_Name != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Title_Sort_Name",self.Title_Sort_Name))
        if self.Episode_Name != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Episode_Name",self.Episode_Name))
        if self.Episode_ID != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Episode_ID",self.Episode_ID))
	if self.Summary_Long != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Summary_Long",self.Summary_Long, self.Target_Language))
	if self.Summary_Medium != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Summary_Medium",self.Summary_Medium, self.Target_Language))
	if self.Advisories != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Advisories",self.Advisories))
	if self.Country_of_Origin != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Country_of_Origin",self.Country_of_Origin))
	if self.Actors != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Actors",self.Actors))
	if self.Actors_Display != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Actors_Display",self.Actors_Display))
	if self.Writer_Display != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Writer_Display",self.Writer_Display))
	if self.Director != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Director",self.Director))
	if self.Producers != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Producers",self.Producers))
	if self.Studio != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio",self.Studio))
	if self.Season_Premiere != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Season_Premiere",self.Season_Premiere))
	if self.Season_Finale != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Season_Finale",self.Season_Finale))
	if self.Box_Office != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Box_Office",self.Box_Office))
	if self.Propagation_Priority != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Propagation_Priority",self.Propagation_Priority))
	if self.Home_Video_Window != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Home_Video_Window",self.Home_Video_Window))
	if self.Display_As_New != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Display_As_New",self.Display_As_New))
	if self.Display_As_Last_Chance != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Display_As_Last_Chance",self.Display_As_Last_Chance))
	if self.Maximum_Viewing_Length != '':
	    Metadata.append(App_Data_Element(self.App_Data_App, "Maximum_Viewing_Length",self.Maximum_Viewing_Length))
	if self.Contract_Name != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Contract_Name",self.Contract_Name))
        if self.Suggested_Price != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Suggested_Price",self.Suggested_Price))
        if self.Distributor_Royalty_Percent != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Distributor_Royalty_Percent",self.Distributor_Royalty_Percent))
        if self.Distributor_Royalty_Minimum != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Distributor_Royalty_Minimum",self.Distributor_Royalty_Minimum))
        if self.Distributor_Royalty_Flat_Rate != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Distributor_Royalty_Flat_Rate",self.Distributor_Royalty_Flat_Rate))
	if self.Distributor_Name != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Distributor_Name",self.Distributor_Name))
        if self.Studio_Royalty_Percent != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio_Royalty_Percent",self.Studio_Royalty_Percent))
        if self.Studio_Royalty_Minimum != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio_Royalty_Minimum",self.Studio_Royalty_Minimum))
        if self.Studio_Royalty_Flat_Rate != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio_Royalty_Flat_Rate",self.Studio_Royalty_Flat_Rate))
        if self.Studio_Name != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio_Name",self.Studio_Name))
	if self.Studio_Code != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Studio_Code",self.Studio_Code))
	if self.Subscriber_View_Limit != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Subscriber_View_Limit",self.Subscriber_View_Limit))
	if self.Programmer_Call_Letters != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Programmer_Call_Letters",self.Programmer_Call_Letters))
	if self.Recording_Artist != '':
            Metadata.append(App_Data_Element(self.App_Data_App, "Recording_Artist",self.Recording_Artist))
    	if self.Song_Title != '':
    	    Metadata.append(App_Data_Element(self.App_Data_App, "Song_Title",self.Song_Title))


        Asset.append(Metadata)
        return Asset

