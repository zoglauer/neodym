#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
from bs4 import BeautifulSoup

# Import neodym files
from feature import ZFeature

# -----------------------------------------------------------------------------------


class ZPictureShow(ZFeature):
  def __init__(self):
    super(ZPictureShow, self).__init__()
    self.mFeatureTag = "<neodym-pictureshow />"
  

  def apply(self, Article):
    Body = BeautifulSoup(Article.mBody, 'html.parser')
    PictureShowTag = Body.find_all('neodym-pictureshow')
    
    if len(PictureShowTag) == 0:
      return
    if len(PictureShowTag) > 1: 
      print("Error: Only one <neodym-pictureshow> allowed")
      return
    
    for Tag in PictureShowTag:
      ReplacementText = ""
      PictureTags = Tag.find_all('neodym-picture')
      if len(PictureTags) > 0:
        ReplacementText += "<div class=\"nd-ps-main\">\n"
        ReplacementText += "  <div class=\"nd-ps-backwardsbutton\" onclick='ImageSwitchBackward();'>\n"
        ReplacementText += "    <div class=\"nd-ps-backwardstext\" onclick='ImageSwitchBackward();'>«</div>\n"
        ReplacementText += "  </div>\n"
        ReplacementText += "  <div class=\"nd-ps-figures\">\n"
        
        for PTag in PictureTags:
          SourceTag = PTag.find('neodym-picture-source')
          #print(type(SourceTag))
          TitleTag = PTag.find('neodym-picture-title')
          #print(TitleTag)
          CaptionTag = PTag.find('neodym-picture-caption')
          #print(CaptionTag)
          if SourceTag:
            Source = ""
            for S in SourceTag.stripped_strings:
              Source += S
              
              Title = ""
              if TitleTag:
                Title = TitleTag.prettify()
                Title = Title.replace("<neodym-picture-title>", "")
                Title = Title.replace("</neodym-picture-title>", "")
                Title = Title.replace("\n", "")
              
              Caption = ""
              if CaptionTag:
                Caption = CaptionTag.prettify()
                Caption = Caption.replace("<neodym-picture-caption>", "")
                Caption = Caption.replace("</neodym-picture-caption>", "")
                Caption = Caption.replace("\n", "")
              
              ReplacementText += "    <figure class=\"nd-ps-figure\">\n"
              ReplacementText += "      <img class=\"nd-ps-image\" src=\"" + Source + "\"/>\n"
              ReplacementText += "      <figcaption class=\"nd-ps-figure-caption\">\n"
              ReplacementText += "        <div class=\"nd-ps-title\">\n"
              ReplacementText += "          " + Title + "\n"
              ReplacementText += "        </div>\n"
              ReplacementText += "        <div class=\"nd-ps-caption\">\n"
              ReplacementText += "          " + Caption + "\n"
              ReplacementText += "        </div>\n"
              ReplacementText += "      </figcaption>\n"
              ReplacementText += "    </figure>\n"
              
              Article.mFiles.append(Source)
              
        ReplacementText += "  </div>\n"
        ReplacementText += "  <div class=\"nd-ps-forwardsbutton\" onclick='ImageSwitchForward();'>\n"
        ReplacementText += "    <div class=\"nd-ps-forwardstext\" onclick='ImageSwitchForward();'>»</div>\n"
        ReplacementText += "  </div>\n"
        ReplacementText += "</div>\n"
              
        #print("Replacement: " + ReplacementText)
              
        PS = BeautifulSoup(ReplacementText, 'html.parser')
        Tag.replace_with(PS)
      
      Article.mBody = Body.prettify();
              
      Article.mJavaScriptFileNames.append("neodym-pictureshow.js")

      if "PictureShowMode" in Article.mDictionary:
        if Article.mDictionary["PictureShowMode"] == "Dual" or Article.mDictionary["PictureShowMode"] == "dual": 
          Article.mCSSFileNames.append("neodym-pictureshow-dual.css")
        else:
          Article.mCSSFileNames.append("neodym-pictureshow.css")
      else:
        Article.mCSSFileNames.append("neodym-pictureshow.css")

  
# -----------------------------------------------------------------------------------
