<xsl:stylesheet xmlns="http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:vod30="http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1" xmlns:core="http://www.cablelabs.com/namespaces/metadata/xsd/core/1" xmlns:offer="http://www.cablelabs.com/namespaces/metadata/xsd/offer/1" xmlns:title="http://www.cablelabs.com/namespaces/metadata/xsd/title/1" xmlns:terms="http://www.cablelabs.com/namespaces/metadata/xsd/terms/1" xmlns:content="http://www.cablelabs.com/namespaces/metadata/xsd/content/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  version="2.0">
<!--
Translate from CL1.1 (ADI 20091229) to CL3.
-->
	<xsl:output method="xml" indent="yes"/>
	<xsl:variable name="PackageProviderId" select="/ADI/Metadata/AMS/@Provider_ID"/>
	<xsl:variable name="PackageAssetId" select="/ADI/Metadata/AMS/@Asset_ID"/>
	<xsl:variable name="Title" select="/ADI/Asset/Metadata/AMS[@Asset_Class='title'][1]"/>
	<xsl:variable name="TitleProviderId" select="$Title/@Provider_ID"/>
	<xsl:variable name="TitleAssetId" select="$Title/@Asset_ID"/>
	<xsl:variable name="TermsUriId" select="concat($TitleProviderId, '/Terms/', $TitleAssetId )"/>
	<xsl:variable name="TitleUriId" select="concat($TitleProviderId, '/Title/', $TitleAssetId )"/>
	<xsl:variable name="ContentGroupUriId" select="concat($TitleProviderId, '/ContentGroup/', $TitleAssetId )"/>

	<xsl:variable name="TitleProviderVersionNum" select="/ADI/Asset/Metadata/AMS/@Version_Major"/>
	<xsl:variable name="TitleInternalVersionNum" select="/ADI/Asset/Metadata/AMS/@Version_Minor"/>
	<xsl:variable name="TitleCreationDateTime"><xsl:choose><xsl:when test="string-length(/ADI/Asset/Metadata/AMS/@Creation_Date) = 10"><xsl:value-of select="concat(/ADI/Asset/Metadata/AMS/@Creation_Date,'T00:00:00Z')"/></xsl:when><xsl:otherwise><xsl:value-of select="/ADI/Asset/Metadata/AMS/@Creation_Date"/></xsl:otherwise></xsl:choose></xsl:variable>	
	
	<xsl:template match="/ADI">
		<ADI3 xmlns="http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1"  xmlns:vod30="http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1" xmlns:core="http://www.cablelabs.com/namespaces/metadata/xsd/core/1" xmlns:offer="http://www.cablelabs.com/namespaces/metadata/xsd/offer/1" xmlns:title="http://www.cablelabs.com/namespaces/metadata/xsd/title/1" xmlns:terms="http://www.cablelabs.com/namespaces/metadata/xsd/terms/1" xmlns:content="http://www.cablelabs.com/namespaces/metadata/xsd/content/1"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1 MD-SP-VODContainer-D04.xsd">
			<xsl:if test="empty(Metadata/AMS/@Verb) or Metadata/AMS[@Verb != 'DELETE']">
				<xsl:call-template name="Offer" />
			</xsl:if>
			<xsl:apply-templates select="//Asset[empty(Metadata/AMS/@Verb) or Metadata/AMS/@Verb != 'DELETE']"/>
		</ADI3>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='title']">
		<!-- Every ADI1.1 title maps to a Title, ContentGroup, Terms and one or more Categories -->
		<xsl:call-template name="Title"/>
		<xsl:call-template name="ContentGroup"/>
		<xsl:call-template name="Terms"/>
		<xsl:call-template name="Category"/>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='box cover']">
		<BoxCover>
			<xsl:call-template name="StillImage"/>
		</BoxCover>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='poster']">
		<Poster>
			<xsl:call-template name="StillImage"/>
		</Poster>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='movie']">
		<Movie>
			<xsl:call-template name="AudioVideo" ><xsl:with-param name="previewOrTitle" select=".."/></xsl:call-template>
		</Movie>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='encrypted']">
		<Movie>
			<xsl:call-template name="AudioVideo">
				<xsl:with-param name="masterSourceRef">
					<xsl:if test="Metadata/App_Data[@Name='Asset_Encrypted']">
						<xsl:value-of select="concat( Metadata/AMS/@Provider_ID, '/Asset/',Metadata/App_Data[@Name='Asset_Encrypted']/@Value)"/>
					</xsl:if>
				</xsl:with-param>
				<xsl:with-param name="previewOrTitle" select=".."/>
			</xsl:call-template>
		</Movie>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='preview']">
		<Preview>
			<xsl:call-template name="AudioVideo"><xsl:with-param name="previewOrTitle" select="."/></xsl:call-template>
		</Preview>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='trickfile']">
		<Trick>
			<xsl:call-template name="ContentAsset"><xsl:with-param name="masterSourceRef">$TitleUriId</xsl:with-param></xsl:call-template>
			<xsl:if test="Metadata/App_Data[@Name='Bit_Rate']">
				<content:BitRate>
					<xsl:value-of select="Metadata/App_Data[@Name='Bit_Rate']/@Value"/>
				</content:BitRate>	
			</xsl:if>	
			<xsl:if test="Metadata/App_Data[@Name='Vendor_Name']">
				<content:VendorName>
					<xsl:value-of select="Metadata/App_Data[@Name='Vendor_Name']/@Value"/>
				</content:VendorName>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Vendor_Product']">
				<content:VendorProduct>
					<xsl:value-of select="Metadata/App_Data[@Name='Vendor_Product']/@Value"/>
				</content:VendorProduct>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='For_Version']">
				<content:ForVersion>
					<xsl:value-of select="Metadata/App_Data[@Name='For_Version']/@Value"/>
				</content:ForVersion>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Trick_Mode']">
				<content:TrickMode>
					<xsl:value-of select="Metadata/App_Data[@Name='Trick_Mode']/@Value"/>
				</content:TrickMode>
			</xsl:if>		
		</Trick>
	</xsl:template>
	<xsl:template match="Asset[Metadata/AMS/@Asset_Class='barker']">
		<Barker>
			<xsl:call-template name="AudioVideo"><xsl:with-param name="previewOrTitle" select=".."/></xsl:call-template>
		</Barker>
	</xsl:template>
	
	<xsl:template name="Offer">
		<Offer>
			<xsl:attribute name="uriId"><xsl:value-of select="concat( $PackageProviderId, '/Offer/', $PackageAssetId )"/></xsl:attribute>
			<xsl:call-template name="AMS_1"/>
			<xsl:call-template name="AMS_2"/>
			<xsl:for-each select="//App_Data[@Name='Category'] ">
				<offer:Presentation>
					<offer:CategoryRef>
						<xsl:attribute name="uriId"><xsl:value-of select="concat( $PackageProviderId, '/Category/',@Value )"/></xsl:attribute>
					</offer:CategoryRef>
					<xsl:if test="//App_Data[@Name='Display_As_Last_Chance']">
						<offer:DisplayAsNew>
							<xsl:value-of select="concat('P',//App_Data[@Name='Display_As_Last_Chance']/@Value,'D')"/>
						</offer:DisplayAsNew>
					</xsl:if>
					<xsl:if test="//App_Data[@Name='Display_As_New']">
						<offer:DisplayAsLastChance>
							<xsl:value-of select="concat('P',//App_Data[@Name='Display_As_New']/@Value,'D')"/>
						</offer:DisplayAsLastChance>
					</xsl:if>
				</offer:Presentation>
			</xsl:for-each>
			<offer:PromotionalContentGroupRef uriId="{$ContentGroupUriId}"/>
			<xsl:for-each select="Metadata/App_Data[@Name='Provider_Content_Tier'] ">
				<offer:ProviderContentTier>
					<xsl:value-of select="@Value"/>
				</offer:ProviderContentTier>
			</xsl:for-each>
			<xsl:if test="Metatdata/App_Data[@Name='Metadata_Spec_Version'] ">
				<offer:SourceMetadataSpecVersion deprecated="true">
					<xsl:value-of select="Metadata/App_Data[@Name='Metadata_Spec_Version']/@Value"/>
				</offer:SourceMetadataSpecVersion>
			</xsl:if>
 			<offer:BillingId>
				<xsl:choose>
					<xsl:when test="//App_Data[@Name='Billing_ID']"><xsl:value-of select="//App_Data[@Name='Billing_ID']/@Value"/></xsl:when>
					<!--TODO  what is default value? This introduces default Suggested_Price after round trip-->
					<xsl:otherwise>00000</xsl:otherwise>
				</xsl:choose>
			</offer:BillingId>
			<offer:TermsRef uriId="{$TermsUriId}"/>
			<offer:ContentGroupRef uriId="{$ContentGroupUriId}"/>
		</Offer>
	</xsl:template>
	<xsl:template name="Title">
		<Title>
			<xsl:attribute name="uriId"><xsl:value-of select="$TitleUriId"/></xsl:attribute>
			<xsl:call-template name="AMS_1"/>
			<xsl:if test="Metadata/App_Data[@Name='ISAN']">
				<core:AlternateId identifierSystem="ISAN">
					<xsl:value-of select="Metadata/App_Data[@Name='ISAN']/@Value"/>
				</core:AlternateId>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Provider_QA_Contact']">
				<core:ProviderQAContact>
					<xsl:value-of select="Metadata/App_Data[@Name='Provider_QA_Contact']/@Value"/>
				</core:ProviderQAContact>
			</xsl:if>
			<xsl:call-template name="AMS_2"/>
			<title:LocalizableTitle>
				<xsl:if test="Metadata/App_Data[@Name='Title_Sort_Name']">
					<title:TitleSortName>
						<xsl:value-of select="Metadata/App_Data[@Name='Title_Sort_Name']/@Value"/>
					</title:TitleSortName>
				</xsl:if>
				<xsl:choose>
					<xsl:when test="Metadata/App_Data[@Name='Title_Brief']">
						<title:TitleBrief>
							<xsl:value-of select="Metadata/App_Data[@Name='Title_Brief']/@Value"/>
						</title:TitleBrief>
						<title:TitleMedium>
							<xsl:value-of select="Metadata/App_Data[@Name='Title_Brief']/@Value"/>
						</title:TitleMedium>
					</xsl:when>		
					<xsl:otherwise>
						<title:TitleBrief>
							<xsl:value-of select="substring(Metadata/App_Data[@Name='Title']/@Value,1,19)"/>
						</title:TitleBrief>
						<title:TitleMedium>
							<xsl:value-of select="substring(Metadata/App_Data[@Name='Title']/@Value,1,35)"/>
						</title:TitleMedium>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:if test="Metadata/App_Data[@Name='Title']">
					<title:TitleLong>
						<xsl:value-of select="Metadata/App_Data[@Name='Title']/@Value"/>
					</title:TitleLong>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Summary_Short']">
					<title:SummaryShort>
						<xsl:value-of select="Metadata/App_Data[@Name='Summary_Short']/@Value"/>
					</title:SummaryShort>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Summary_Medium']">
					<title:SummaryMedium>
						<xsl:value-of select="Metadata/App_Data[@Name='Summary_Medium']/@Value"/>
					</title:SummaryMedium>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Summary_Long']">
					<title:SummaryLong>
						<xsl:value-of select="Metadata/App_Data[@Name='Summary_Long']/@Value"/>
					</title:SummaryLong>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Actors_Display']">
					<title:ActorDisplay>
						<xsl:value-of select="Metadata/App_Data[@Name='Actors_Display']/@Value"/>
					</title:ActorDisplay>
				</xsl:if>
				<xsl:apply-templates select="Metadata/App_Data[@Name='Actors']" mode="person" />
				<xsl:if test="Metadata/App_Data[@Name='Writer_Display']">
					<title:WriterDisplay>
						<xsl:value-of select="Metadata/App_Data[@Name='Writer_Display']/@Value"/>
					</title:WriterDisplay>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Director_Display']">
					<title:DirectorDisplay>
						<xsl:value-of select="Metadata/App_Data[@Name='Director_Display']/@Value"/>
					</title:DirectorDisplay>
				</xsl:if>
				<xsl:apply-templates select="Metadata/App_Data[@Name='Director']" mode="person"/>
				<xsl:if test="Metadata/App_Data[@Name='Producer_Display']">
						<title:ProducerDisplay>
							<xsl:value-of select="Metadata/App_Data[@Name='Producer_Display']/@Value"/>
						</title:ProducerDisplay>
				</xsl:if>
				<xsl:apply-templates select="Metadata/App_Data[@Name='Producers']" mode="person"/>
				<xsl:if test="Metadata/App_Data[@Name='Studio']">
						<title:StudioDisplay>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio']/@Value"/>
						</title:StudioDisplay>
				</xsl:if>
				<xsl:for-each select="Metadata/App_Data[@Name='Recording_Artist']">
					<title:RecordingArtist>
						<xsl:value-of select="@Value"/>
					</title:RecordingArtist>
				</xsl:for-each>
				<xsl:for-each select="Metadata/App_Data[@Name='Song_Title']">
					<title:SongTitle>
						<xsl:value-of select="@Value"/>
					</title:SongTitle>
				</xsl:for-each>
				<xsl:if test="Metadata/App_Data[@Name='Episode_Name']">
					<title:EpisodeName deprecated="true">
						<xsl:value-of select="Metadata/App_Data[@Name='Episode_Name']/@Value"/>
					</title:EpisodeName>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Episode_ID']">
					<title:EpisodeID deprecated="true">
						<xsl:value-of select="Metadata/App_Data[@Name='Episode_ID']/@Value"/>
					</title:EpisodeID>
				</xsl:if>
				<xsl:for-each select="Metadata/App_Data[@Name='Chapter']">
					<title:Chapter>
						<xsl:attribute name="heading"><xsl:value-of select="substring-after(@Value, ',')"/></xsl:attribute>	
						<xsl:attribute name="timeCode"><xsl:value-of select="substring-before(@Value, ',')"/></xsl:attribute>
					</title:Chapter>
				</xsl:for-each>
			</title:LocalizableTitle>
			<xsl:for-each select="Metadata/App_Data[@Name='Rating']">
				<title:Rating>
					<xsl:choose>
						<xsl:when test="exists(index-of(('G','PG','PG-13','R','NC-17'),@Value))"><xsl:attribute name="ratingSystem">MPAA</xsl:attribute></xsl:when>
						<xsl:when test="starts-with(@Value,'TV')"><xsl:attribute name="ratingSystem">TV</xsl:attribute></xsl:when>
					</xsl:choose>
					<xsl:value-of select="@Value"/>
				</title:Rating>
			</xsl:for-each>
			<xsl:for-each select="Metadata/App_Data[@Name='MSORating']">
				<title:Rating ratingSystem="MSO">
					<xsl:value-of select="@Value"/>
				</title:Rating>
			</xsl:for-each>
			<xsl:for-each select="Metadata/App_Data[@Name='Audience']">
				<title:Audience>
					<xsl:value-of select="@Value"/>
				</title:Audience>
			</xsl:for-each>
			<xsl:for-each select="Metadata/App_Data[@Name='Advisories']">
				<title:Advisory>
					<xsl:value-of select="@Value"/>
				</title:Advisory>
			</xsl:for-each>
			<xsl:if test="Metadata/App_Data[@Name='Closed_Captioning']/@Value='Y'">
				<title:IsClosedCaptioning>true</title:IsClosedCaptioning>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Closed_Captioning']/@Value='N'">
				<title:IsClosedCaptioning>false</title:IsClosedCaptioning>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Display_Run_Time']">
				<title:DisplayRunTime>
					<xsl:value-of select="Metadata/App_Data[@Name='Display_Run_Time']/@Value"/>
				</title:DisplayRunTime>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Year']">
				<title:Year>
					<xsl:value-of select="Metadata/App_Data[@Name='Year']/@Value"/>
				</title:Year>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Country_of_Origin']">
				<title:CountryOfOrigin>
					<xsl:choose>
						<xsl:when test="Metadata/App_Data[@Name='Country_of_Origin']/@Value = 'United States'">US</xsl:when>
						<xsl:otherwise><xsl:value-of select="Metadata/App_Data[@Name='Country_of_Origin']/@Value"/></xsl:otherwise>
					</xsl:choose>
				</title:CountryOfOrigin>
			</xsl:if>
			<xsl:for-each select="Metadata/App_Data[@Name='Genre']">
				<title:Genre>
					<xsl:value-of select="@Value"/>
				</title:Genre>
			</xsl:for-each>
			<xsl:if test="count(Metadata/App_Data[@Name='Genre'])=0">
				<title:Genre>private:UNKNOWN</title:Genre>
			</xsl:if>
			<title:ShowType>
				<xsl:choose>
					<xsl:when test="Metadata/App_Data[@Name='Show_Type']"><xsl:value-of select="Metadata/App_Data[@Name='Show_Type']/@Value"/></xsl:when>
					<xsl:otherwise>private:UNKNOWN</xsl:otherwise>
				</xsl:choose>
			</title:ShowType>
			<xsl:if test="Metadata/App_Data[@Name='Season_Premiere']/@Value='Y'">
				<title:IsSeasonPremier deprecated="true">true</title:IsSeasonPremier>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Season_Premiere']/@Value='N'">
				<title:IsSeasonPremier deprecated="true">false</title:IsSeasonPremier>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Season_Finale']/@Value='Y'">
				<title:IsSeasonFinale deprecated="true">true</title:IsSeasonFinale>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Season_Finale']/@Value='N'">
				<title:IsSeasonFinale deprecated="true">false</title:IsSeasonFinale>
			</xsl:if>
			<!-- TODO:  a bit weird as this is per movie in ADI1.1, should be deprecated? we are lazy and just find it any Encryption="Y" -->
			<xsl:if test="//App_Data[@Name='Encryption']/@Value='Y'">
				<title:IsEncryptionRequired>true</title:IsEncryptionRequired>
			</xsl:if>
			<xsl:if test="//App_Data[@Name='Encryption']/@Value='N'">
				<title:IsEncryptionRequired>false</title:IsEncryptionRequired>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Box_Office']">
				<title:BoxOffice>
					<xsl:value-of select="Metadata/App_Data[@Name='Box_Office']/@Value"/>
				</title:BoxOffice>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Programmer_Call_Letters']">
				<title:ProgrammerCallLetters>
					<xsl:value-of select="Metadata/App_Data[@Name='Programmer_Call_Letters']/@Value"/>
				</title:ProgrammerCallLetters>
			</xsl:if>
		</Title>
	</xsl:template>
	<xsl:template name="ContentGroup">
		<ContentGroup>
			<xsl:attribute name="uriId"><xsl:value-of select="$ContentGroupUriId"/></xsl:attribute>
			<xsl:call-template name="AMS_1"/>
			<offer:TitleRef>
				<xsl:attribute name="uriId"><xsl:value-of select="$TitleUriId"/></xsl:attribute>
			</offer:TitleRef>
			<xsl:for-each select="Asset/Metadata/AMS">
				<xsl:variable name="uriId"><xsl:value-of select="concat( @Provider_ID, '/Asset/', @Asset_ID)"/></xsl:variable>
				<xsl:choose>
					<xsl:when test="@Asset_Class='movie' or @Asset_Class='encrypted'"><offer:MovieRef uriId="{$uriId}"/></xsl:when>
					<xsl:when test="@Asset_Class='barker'"><offer:BarkerRef uriId="{$uriId}"/></xsl:when>
					<xsl:when test="@Asset_Class='preview'"><offer:PreviewRef uriId="{$uriId}"/></xsl:when>
					<xsl:when test="@Asset_Class='box cover'"><offer:BoxCoverRef uriId="{$uriId}"/></xsl:when>
					<xsl:when test="@Asset_Class='poster'"><offer:PosterRef uriId="{$uriId}"/></xsl:when>
					<xsl:when test="@Asset_Class='trickfile'"><offer:TrickRef uriId="{$uriId}"/></xsl:when>
				</xsl:choose>
			</xsl:for-each>
		</ContentGroup>
	</xsl:template>
	<xsl:template name="Terms">
		<xsl:variable name="MaxViewingLength" select="Metadata/App_Data[@Name='Maximum_Viewing_Length']/@Value"/>
		<xsl:variable name="days" select="concat('P',substring-before($MaxViewingLength, ':'),'DT')"/>
		<xsl:variable name="remaining" select="substring-after($MaxViewingLength, ':')"/>
		<xsl:variable name="hours" select="concat(substring-before($remaining, ':'),'H')"/>
		<xsl:variable name="minutes" select="concat(substring-after($remaining, ':'),'M')"/>
		<xsl:variable name="FormattedMaxViewingLength" select="concat($days,$hours,$minutes)"/>
		<Terms>
			<xsl:attribute name="uriId"><xsl:value-of select="$TermsUriId"/></xsl:attribute>
			<xsl:call-template name="AMS_1"/>
			<xsl:if test="Metadata/App_Data[@Name='Contract_Name']">
				<terms:ContractName>
					<xsl:value-of select="Metadata/App_Data[@Name='Contract_Name']/@Value"/>
				</terms:ContractName>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Preview_Period']">
				<terms:BillingGracePeriod>
					<xsl:value-of select="concat('PT',Metadata/App_Data[@Name='Preview_Period']/@Value,'S')"/>
				</terms:BillingGracePeriod>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Maximum_Viewing_Length']">
				<terms:RentalPeriod>
					<xsl:value-of select="$FormattedMaxViewingLength"/>
				</terms:RentalPeriod>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Home_Video_Window']">
				<terms:HomeVideoWindow>
					<xsl:value-of select="concat('P',Metadata/App_Data[@Name='Home_Video_Window']/@Value,'D') "/>
				</terms:HomeVideoWindow>
			</xsl:if>
			
			<xsl:for-each select="//App_Data[@Name='Subscriber_View_Limit']">
				<xsl:variable name="subscriberViewLimit" select="tokenize(@Value, ',')"/>
				<terms:SubscriberViewLimit>
					<xsl:attribute name="startDateTime">
						<xsl:call-template name="startDateTime">
							<xsl:with-param name="dateString" select="$subscriberViewLimit[1]" />
						</xsl:call-template>
					</xsl:attribute>
					<xsl:attribute name="endDateTime">
						<xsl:call-template name="endDateTime">
							<xsl:with-param name="dateString" select="$subscriberViewLimit[2]" />
						</xsl:call-template>
					</xsl:attribute>				
					<xsl:attribute name="maximumViews"><xsl:value-of select="$subscriberViewLimit[3]"/></xsl:attribute>	
				</terms:SubscriberViewLimit>
			</xsl:for-each>

			<terms:SuggestedPrice>
				<xsl:choose>
					<xsl:when test="Metadata/App_Data[@Name='Suggested_Price']">
						<xsl:value-of select="Metadata/App_Data[@Name='Suggested_Price']/@Value"/>
					</xsl:when>
					<!-- TODO:  no price, must be free but this introduces default Suggested_Price after round trip -->
					<xsl:otherwise>0.00</xsl:otherwise>
				</xsl:choose>
			</terms:SuggestedPrice>

			<xsl:if test="Metadata/App_Data[@Name='Distributor_Name'] or Metadata/App_Data[@Name='Distributor_Code'] or Metadata/App_Data[@Name='Distributor_Royalty_Percent'] or Metadata/App_Data[@Name='Distributor_Royalty_Minimum'] or Metadata/App_Data[@Name='Distributor_Royalty_Flat_Rate']">
				<terms:DistributorRoyaltyInfo>
					<xsl:if test="Metadata/App_Data[@Name='Distributor_Name']">
						<terms:OrganizationName>
							<xsl:value-of select="Metadata/App_Data[@Name='Distributor_Name']/@Value"/>
						</terms:OrganizationName>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Distributor_Code']">
						<terms:OrganizationCode>
							<xsl:value-of select="Metadata/App_Data[@Name='Distributor_Code']/@Value"/>
						</terms:OrganizationCode>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Distributor_Royalty_Percent']">
						<terms:RoyaltyPercent>
							<xsl:value-of select="Metadata/App_Data[@Name='Distributor_Royalty_Percent']/@Value"/>
						</terms:RoyaltyPercent>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Distributor_Royalty_Minimum']">
						<terms:RoyaltyMinimum>
							<xsl:value-of select="Metadata/App_Data[@Name='Distributor_Royalty_Minimum']/@Value"/>
						</terms:RoyaltyMinimum>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Distributor_Royalty_Flat_Rate']">
						<terms:RoyaltyFlatRate>
							<xsl:value-of select="Metadata/App_Data[@Name='Distributor_Royalty_Flat_Rate']/@Value"/>
						</terms:RoyaltyFlatRate>
					</xsl:if>
				</terms:DistributorRoyaltyInfo>
			</xsl:if>
			<xsl:if test="Metadata/App_Data[@Name='Studio_Name'] or Metadata/App_Data[@Name='Studio_Code'] or Metadata/App_Data[@Name='Studio_Royalty_Percent'] or Metadata/App_Data[@Name='Studio_Royalty_Minimum'] or  Metadata/App_Data[@Name='Studio_Royalty_Flat_Rate']">
				<terms:StudioRoyaltyInfo>
					<xsl:if test="Metadata/App_Data[@Name='Studio_Name']">
						<terms:OrganizationName>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio_Name']/@Value"/>
						</terms:OrganizationName>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Studio_Code']">
						<terms:OrganizationCode>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio_Code']/@Value"/>
						</terms:OrganizationCode>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Studio_Royalty_Percent']">
						<terms:RoyaltyPercent>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio_Royalty_Percent']/@Value"/>
						</terms:RoyaltyPercent>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Studio_Royalty_Minimum']">
						<terms:RoyaltyMinimum>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio_Royalty_Minimum']/@Value"/>
						</terms:RoyaltyMinimum>
					</xsl:if>
					<xsl:if test="Metadata/App_Data[@Name='Studio_Royalty_Flat_Rate']">
						<terms:RoyaltyFlatRate>
							<xsl:value-of select="Metadata/App_Data[@Name='Studio_Royalty_Flat_Rate']/@Value"/>
						</terms:RoyaltyFlatRate>
					</xsl:if>
				</terms:StudioRoyaltyInfo>
			</xsl:if>
		</Terms>
	</xsl:template>
	<xsl:template name="Category">
		<xsl:for-each select="Metadata/App_Data[@Name='Category']">
			<Category>
				<xsl:attribute name="uriId"><xsl:value-of select="concat( $PackageProviderId, '/Category/',@Value )"/></xsl:attribute>
				<xsl:for-each select="../..[1]">
					<xsl:call-template name="AMS_1"/>
				</xsl:for-each>
				<offer:CategoryPath>
					<xsl:value-of select="@Value"/>
				</offer:CategoryPath>
			</Category>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="ContentAsset">
		<xsl:param name="masterSourceRef"/>
		<xsl:attribute name="uriId"><xsl:value-of select="concat( Metadata/AMS/@Provider_ID, '/Asset/', Metadata/AMS/@Asset_ID )"/></xsl:attribute>
		<xsl:call-template name="AMS_1"/>
		<xsl:call-template name="AMS_2"/>
		<xsl:if test="$masterSourceRef">
			<content:MasterSourceRef>
				<xsl:attribute name="uriId"><xsl:value-of select="$masterSourceRef"/></xsl:attribute>
			</content:MasterSourceRef>
		</xsl:if>	
		<xsl:if test="Content/@Value">
			<content:SourceUrl>
				<xsl:value-of select="Content/@Value"/>
			</content:SourceUrl>
		</xsl:if>
		<xsl:if test="Metadata/App_Data[@Name='Content_FileSize']">
			<content:ContentFileSize>
				<xsl:value-of select="Metadata/App_Data[@Name='Content_FileSize']/@Value"/>
			</content:ContentFileSize>
		</xsl:if>
		<xsl:if test="Metadata/App_Data[@Name='Content_CheckSum']">
			<content:ContentCheckSum>
				<xsl:value-of select="Metadata/App_Data[@Name='Content_CheckSum']/@Value"/>
			</content:ContentCheckSum>
		</xsl:if>
		<xsl:if test="//Asset/Metadata/App_Data[@Name='Propagation_Priority']" >
			<content:PropagationPriority>
				<!-- grab any one (max??) -->
				<xsl:value-of select="//Asset/Metadata/App_Data[@Name='Propagation_Priority']/@Value"/>
			</content:PropagationPriority>
		</xsl:if>
	</xsl:template>
	<xsl:template name="StillImage">
		<xsl:call-template name="ContentAsset"/>
		<xsl:variable name="ImageAspect" select="Metadata/App_Data[@Name='Image_Aspect_Ratio']/@Value"/>
		<xsl:variable name="x" select="substring-before($ImageAspect, 'x')"/>
		<xsl:variable name="y" select="substring-after($ImageAspect, 'x')"/>
		<xsl:if test="$x">
			<content:X_Resolution>
				<xsl:value-of select="$x"/>
			</content:X_Resolution>
		</xsl:if>
		<xsl:if test="$y">
			<content:Y_Resolution>
				<xsl:value-of select="$y"/>
			</content:Y_Resolution>
		</xsl:if>
	</xsl:template>
	<xsl:template name="AudioVideo">
		<xsl:param name="masterSourceRef"/>
		<xsl:param name="previewOrTitle"/>
		<xsl:call-template name="ContentAsset"><xsl:with-param name="masterSourceRef" select="$masterSourceRef"/></xsl:call-template>
		
		<!-- For an asset with asset_class="encrypted" the values on the "movie" with Asset_ID of the Asset_Encrypted are copied over -->
		<xsl:variable name="assetEncrypted" select="Metadata/App_Data[@Name='Asset_Encrypted']/@Value" />
		<xsl:variable name="sourceNode" select="//Asset[Metadata/AMS/@Asset_ID=$assetEncrypted] | current()" />
				
		<xsl:for-each select="$sourceNode/Metadata/App_Data[@Name='Audio_Type']">
			<content:AudioType>
				<xsl:value-of select="@Value"/>
			</content:AudioType>
		</xsl:for-each>
		<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Screen_Format']">
			<content:ScreenFormat>
				<xsl:value-of select="$sourceNode/Metadata/App_Data[@Name='Screen_Format']/@Value"/>
			</content:ScreenFormat>
		</xsl:if>
		<xsl:if test="Metadata/App_Data[@Name='Resolution']">
			<content:Resolution><xsl:value-of select="Metadata/App_Data[@Name='Resolution']/@Value"/></content:Resolution>
		</xsl:if>
		<xsl:if test="Metadata/App_Data[@Name='Frame_Rate']">
			<content:FrameRate><xsl:value-of select="Metadata/App_Data[@Name='Frame_Rate']/@Value"/></content:FrameRate>
		</xsl:if>		
		<xsl:if test="Metadata/App_Data[@Name='Codec']">
			<content:Codec><xsl:value-of select="Metadata/App_Data[@Name='Codec']/@Value"/></content:Codec>
		</xsl:if>
		<xsl:if test="Metadata/App_Data[@Name='Bit_Rate']">
			<content:BitRate><xsl:value-of select="Metadata/App_Data[@Name='Bit_Rate']/@Value"/></content:BitRate>
		</xsl:if>
		<xsl:if test="$previewOrTitle/Metadata/App_Data[@Name='Run_Time']">			
			<content:Duration>
				<xsl:apply-templates select="$previewOrTitle/Metadata/App_Data[@Name='Run_Time']/@Value" mode="stringToDuration"/>
			</content:Duration>
		</xsl:if>
		<xsl:for-each select="$sourceNode/Metadata/App_Data[@Name='Languages'] ">
			<content:Language>
				<xsl:value-of select="@Value"/>
			</content:Language>
		</xsl:for-each>
		<xsl:for-each select="$sourceNode/Metadata/App_Data[@Name='Subtitle_Languages'] ">
			<content:SubtitleLanguage>
				<xsl:value-of select="@Value"/>
			</content:SubtitleLanguage>
		</xsl:for-each>
		<xsl:for-each select="$sourceNode/Metadata/App_Data[@Name='Dubbed_Languages'] ">
			<content:DubbedLanguage>
				<xsl:value-of select="@Value"/>
			</content:DubbedLanguage>
		</xsl:for-each>	
		<xsl:for-each select="$previewOrTitle/Metadata/App_Data[@Name='Rating']">
			<content:Rating>
				<xsl:choose>
					<xsl:when test="exists(index-of(('G','PG','PG-13','R','NC-17'),@Value))"><xsl:attribute name="ratingSystem">MPAA</xsl:attribute></xsl:when>
					<xsl:when test="starts-with(@Value,'TV')"><xsl:attribute name="ratingSystem">TV</xsl:attribute></xsl:when>
				</xsl:choose>
				<xsl:value-of select="@Value"/>
			</content:Rating>
		</xsl:for-each>
		<xsl:for-each select="$previewOrTitle/Metadata/App_Data[@Name='MSORating']">
			<content:Rating ratingSystem="MSO">
				<xsl:value-of select="@Value"/>
			</content:Rating>
		</xsl:for-each>
		<xsl:for-each select="$previewOrTitle/Metadata/App_Data[@Name='Audience']">
			<content:Audience>
				<xsl:value-of select="@Value"/>
			</content:Audience>
		</xsl:for-each>
			
		<xsl:if test="Metadata/App_Data[@Name='Vendor_Name' or @Name='Receiver_Type' or @Name='Receiver_Version' or @Name='Encryption_Type' or @Name='Encryption_Algorithm' or @Name='Encryption_Date' or @Name='Encryption_Time'  or @Name='Encryption_System_Info'  or @Name='Encryption_Key_Block' ]">
			<content:EncryptionInfo>
				<xsl:if test="Metadata/App_Data[@Name='Vendor_Name']">
					<content:VendorName>
						<xsl:value-of select="Metadata/App_Data[@Name='Vendor_Name']/@Value"/>
					</content:VendorName>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Receiver_Type']">
					<content:ReceiverType>
						<xsl:value-of select="Metadata/App_Data[@Name='Receiver_Type']/@Value"/>
					</content:ReceiverType>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Receiver_Version']">
					<content:ReceiverVersion>
						<xsl:value-of select="Metadata/App_Data[@Name='Receiver_Version']/@Value"/>
					</content:ReceiverVersion>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Encryption_Type']">
					<content:Encryption>
						<xsl:value-of select="Metadata/App_Data[@Name='Encryption_Type']/@Value"/>
					</content:Encryption>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Encryption_Algorithm']">
					<content:EncryptionAlgorithm>
						<xsl:value-of select="Metadata/App_Data[@Name='Encryption_Algorithm']/@Value"/>
					</content:EncryptionAlgorithm>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Encryption_Date']">
					<content:EncryptionDateTime>
						<xsl:value-of select="concat(Metadata/App_Data[@Name='Encryption_Date']/@Value,'T',Metadata/App_Data[@Name='Encryption_Time']/@Value,'Z')"/>
					</content:EncryptionDateTime>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Encryption_System_Info']">
					<content:EncryptionSystemInfo>
						<xsl:value-of select="Metadata/App_Data[@Name='Encryption_System_Info']/@Value"/>
					</content:EncryptionSystemInfo>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Encryption_Key_Block']">
					<content:EncryptionKeyBlock>
						<xsl:value-of select="Metadata/App_Data[@Name='Encryption_Key_Block']/@Value"/>
					</content:EncryptionKeyBlock>
				</xsl:if>
			</content:EncryptionInfo>
		</xsl:if>

		<xsl:if test="Metadata/App_Data[@Name='Copy_Protection' or @Name='Copy_Protection_Verbose' or @Name='Analog_Protection_System' or @Name='Encryption_Mode_Indicator' or @Name='Constrained_Image_Trigger' or @Name='CGMS_A' ]">		
			<content:CopyControlInfo>
				<xsl:if test="Metadata/App_Data[@Name='Copy_Protection']/@Value='Y'">
					<content:IsCopyProtection>true</content:IsCopyProtection>
				</xsl:if>
				<xsl:if test="Metadata/App_Data[@Name='Copy_Protection']/@Value='N'">
					<content:IsCopyProtection>false</content:IsCopyProtection>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Copy_Protection_Verbose']/@Value='Y'">
					<content:IsCopyProtectionVerbose>true</content:IsCopyProtectionVerbose>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Copy_Protection_Verbose']/@Value='N'">
					<content:IsCopyProtectionVerbose>false</content:IsCopyProtectionVerbose>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Analog_Protection_System']">
					<content:AnalogProtectionSystem>
						<xsl:value-of select="$sourceNode/Metadata/App_Data[@Name='Analog_Protection_System']/@Value"/>
					</content:AnalogProtectionSystem>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Encryption_Mode_Indicator']">
					<content:EncryptionModeIndicator>
						<xsl:value-of select="$sourceNode/Metadata/App_Data[@Name='Encryption_Mode_Indicator']/@Value"/>
					</content:EncryptionModeIndicator>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Constrained_Image_Trigger']">
					<content:ConstrainedImageTrigger>
						<xsl:value-of select="$sourceNode/Metadata/App_Data[@Name='Constrained_Image_Trigger']/@Value"/>
					</content:ConstrainedImageTrigger>
				</xsl:if>
				<xsl:if test="$sourceNode/Metadata/App_Data[@Name='CGMS_A']">
					<content:CGMS_A>
						<xsl:value-of select="$sourceNode/Metadata/App_Data[@Name='Constrained_Image_Trigger']/@Value"/>
					</content:CGMS_A>
				</xsl:if>
			</content:CopyControlInfo>
		</xsl:if>
		<!-- really should be on Terms -->
		<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Viewing_Can_Be_Resumed']/@Value='Y'">
			<content:IsResumeEnabled>true</content:IsResumeEnabled>
		</xsl:if>
		<xsl:if test="$sourceNode/Metadata/App_Data[@Name='Viewing_Can_Be_Resumed']/@Value='N'">
			<content:IsResumeEnabled>false</content:IsResumeEnabled>
		</xsl:if>
		<!-- really should be on Terms -->
		<xsl:for-each select="$sourceNode/Metadata/App_Data[@Name='trickModesRestricted']">
			<xsl:for-each select="tokenize(@Value, ',')">
				<content:TrickModesRestricted><xsl:value-of select="normalize-space(.)"/></content:TrickModesRestricted>
			</xsl:for-each>
		</xsl:for-each>
		<!-- Ext -->
	</xsl:template>

	<!-- Reusable Templates -->
	<xsl:template name="AMS_1">
		<xsl:attribute name="providerVersionNum"><xsl:value-of select="Metadata/AMS/@Version_Major"/></xsl:attribute>
		<xsl:attribute name="internalVersionNum"><xsl:value-of select="Metadata/AMS/@Version_Minor"/></xsl:attribute>
		<xsl:attribute name="creationDateTime">
			<xsl:call-template name="startDateTime">
				<xsl:with-param name="dateString"><xsl:value-of select="Metadata/AMS/@Creation_Date"/></xsl:with-param>
			</xsl:call-template>
		</xsl:attribute>
		<xsl:if test="//App_Data[@Name='Licensing_Window_Start']">
			<xsl:attribute name="startDateTime">
				<xsl:call-template name="startDateTime">
					<xsl:with-param name="dateString"><xsl:value-of select="(//App_Data[@Name='Licensing_Window_Start'])[1]/@Value"/></xsl:with-param>
				</xsl:call-template>
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="//App_Data[@Name='Licensing_Window_End']">
			<xsl:attribute name="endDateTime">
				<xsl:call-template name="endDateTime">
					<xsl:with-param name="dateString"><xsl:value-of select="(//App_Data[@Name='Licensing_Window_End'])[1]/@Value"/></xsl:with-param>
				</xsl:call-template>
			</xsl:attribute>
		</xsl:if>
		<xsl:if test="Metadata/AMS/@Provider_ID and Metadata/AMS/@Asset_ID">
			<core:AlternateId identifierSystem="VOD1.1">
				<xsl:value-of select="concat('vod://',Metadata/AMS/@Provider_ID,'/',Metadata/AMS/@Asset_ID)"/>
			</core:AlternateId>
		</xsl:if>
	</xsl:template>
	<xsl:template name="AMS_2">
		<xsl:if test="Metadata/AMS/@Asset_Name">
			<core:AssetName deprecated="true"><xsl:value-of select="Metadata/AMS/@Asset_Name"/></core:AssetName>
		</xsl:if>
		<xsl:if test="Metadata/AMS/@Product">
			<core:Product deprecated="true"><xsl:value-of select="Metadata/AMS/@Product"/></core:Product>
		</xsl:if>		
		<xsl:if test="Metadata/AMS/@Provider">
			<core:Provider deprecated="true"><xsl:value-of select="Metadata/AMS/@Provider"/></core:Provider>
		</xsl:if>
		<xsl:if test="Metadata/AMS/@Description">
			<core:Description deprecated="true"><xsl:value-of select="Metadata/AMS/@Description"/></core:Description>
		</xsl:if>
		<core:Ext>
			<xsl:apply-templates select="Metadata/App_Data" />
		</core:Ext>
	</xsl:template>

	<xsl:template name="startDateTime">
		<xsl:param name="dateString" />
		<xsl:choose>
			<xsl:when test="string-length($dateString) = 10"><xsl:value-of select="concat($dateString,'T00:00:00Z')"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="concat($dateString,'Z')"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="endDateTime">
		<xsl:param name="dateString" />
		<xsl:choose>
			<xsl:when test="string-length($dateString) = 10"><xsl:value-of select="concat($dateString,'T23:59:59Z')"/></xsl:when>
			<xsl:otherwise><xsl:value-of select="concat($dateString,'Z')"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="*" mode="person">
		<xsl:variable name="elementName" select="concat('title:', replace(@Name, 's$', ''))" />
		<xsl:variable name="name" select="reverse(tokenize(@Value,','))"/>
		<xsl:element name="{$elementName}">
			<xsl:attribute name="fullName"><xsl:value-of select="string-join($name, ' ')"/></xsl:attribute>
			<xsl:attribute name="firstName"><xsl:value-of select="$name[1]"/></xsl:attribute>
			<xsl:attribute name="lastName"><xsl:value-of select="$name[2]"/></xsl:attribute>
			<xsl:attribute name="sortableName"><xsl:value-of select="@Value"/></xsl:attribute>
		</xsl:element>
	</xsl:template>
	<xsl:template match="*|@*" mode="stringToDuration">
		<xsl:variable name="hours" select="concat('PT',substring-before(., ':'),'H')"/>
		<xsl:variable name="remaining" select="substring-after(., ':')"/>
		<xsl:variable name="minutes" select="concat(substring-before($remaining, ':'),'M')"/>
		<xsl:variable name="seconds" select="concat(substring-after($remaining, ':'),'S')"/>
		<xsl:value-of select="concat($hours,$minutes,$seconds)"/>
	</xsl:template>
	
	<!-- Templates to convert trial use fields -->
	<xsl:template match="App_Data[../AMS/@Asset_Class='package']">
		<xsl:if test="empty(index-of(('Provider_Content_Tier','Metadata_Spec_Version'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='title']">
		<xsl:choose>
			<xsl:when test="//AMS[@Asset_Class='barker']">
				<xsl:if test="empty(index-of(('Type','Title','Summary_Short','Rating','Display_Run_Time','Run_Time','Category','Licensing_Window_Start','Licensing_Window_End','Year','Studio','Closed_Captioning'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="empty(index-of(('Type','Title_Sort_Name','Subscriber_View_Limit','Title_Brief','Title','ISAN','Episode_Name','Episode_ID','Summary_Long','Summary_Medium','Summary_Short','Rating','MSORating','Advisories','Audience','Closed_Captioning','Run_Time','Display_Run_Time','Year','Country_of_Origin','Actors','Actors_Display','Writer_Display','Director','Producers','Studio','Category','Season_Premiere','Season_Finale','Genre','Show_Type','Chapter','Box_Office','Propagation_Priority','Billing_ID','Licensing_Window_Start','Licensing_Window_End','Preview_Period','Home_Video_Window','Display_As_New','Display_As_Last_Chance','Maximum_Viewing_Length','Provider_QA_Contact','Contract_Name','Suggested_Price','Distributor_Royalty_Percent','Distributor_Royalty_Minimum','Distributor_Royalty_Flat_Rate','Distributor_Name','Studio_Royalty_Percent','Studio_Royalty_Minimum','Studio_Royalty_Flat_Rate','Studio_Name','Studio_Code','Programmer_Call_Letters','Recording_Artist','Song_Title'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='movie']">
		<xsl:if test="empty(index-of(('Encryption','Type','Audio_Type','Screen_Format','Resolution','Frame_Rate','Codec','Languages','Subtitle_Languages','Dubbed_Languages','Copy_Protection','Copy_Protection_Verbose','Analog_Protection_System','Encryption_Mode_Indicator','Constrained_Image_Trigger','CGMS_A','Viewing_Can_Be_Resumed','Bit_Rate','Content_FileSize','Content_CheckSum','trickModesRestricted'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='box cover' or ../AMS/@Asset_Class='poster']">
		<xsl:if test="empty(index-of(('Type','Image_Aspect_Ratio','Content_FileSize','Content_CheckSum'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='preview']">
		<xsl:if test="empty(index-of(('Rating','MSORating','Audience','Run_Time','Type','Audio_Type','Screen_Format','Resolution','Frame_Rate','Codec','Languages','Subtitle_Languages','Dubbed_Languages','Bit_Rate','Content_FileSize','Content_CheckSum','trickModesRestricted'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='trickfile']">
		<xsl:if test="empty(index-of(('Vendor_Name','Vendor_Product','For_Version','Trick_Mode','Bit_Rate','Content_FileSize','Content_CheckSum'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='encrypted']">
		<xsl:if test="empty(index-of(('Asset_Encrypted','Vendor_Name','Receiver_Type','Receiver_Version','Encryption_Type','Encryption_Algorithm','Encryption_Date','Encryption_Time','Encryption_System_Info','Encryption_Key_Block','Resolution','Frame_Rate','Codec','Bit_Rate','Content_FileSize','Content_CheckSum'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>
	<xsl:template match="App_Data[../AMS/@Asset_Class='barker']">
		<xsl:if test="empty(index-of(('Type','Audio_Type','Languages','Subtitle_Languages','Dubbed_Languages','Content_FileSize','Content_CheckSum','Resolution','Frame_Rate','Codec','Bit_Rate'),@Name))">
			<App_Data>
			<xsl:attribute name="App"><xsl:value-of select="@App"/></xsl:attribute>
			<xsl:attribute name="Name"><xsl:value-of select="@Name"/></xsl:attribute>
			<xsl:attribute name="Value"><xsl:value-of select="@Value"/></xsl:attribute>
			</App_Data>
		</xsl:if>	
	</xsl:template>

</xsl:stylesheet>