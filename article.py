#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files

# Import neodym files
from page import ZPage

# -----------------------------------------------------------------------------------

class ZArticle(ZPage):
  def __init__(self):
    super(ZArticle, self).__init__()
    self.mCSSFileNames = []
    self.mJavaScriptFileNames = []


  def assign(self):
    print("Assign Article")
    if "CSS" in self.mDictionary:
      self.mCSSFileNames.append(self.mDictionary["CSS"])
      print("Found CSS " + self.mDictionary["CSS"] + " in " + self.mDictionary["MenuTitle"])
    if "JS" in self.mDictionary:
      self.mJavaScriptFileNames.append(self.mDictionary["JS"])
  
  
  def read(self, FileName):
    print("Read Article")
    super(ZArticle, self).read(FileName)
    ZArticle.assign(self)
    return True
  
  
  def assimilate(self, Reader):
    print("Assim Article")
    super(ZArticle, self).assimilate(Reader)
    ZArticle.assign(self)	
    return True
      
  
  def createPage(self, Title, SubTitle, Description, Logo, Footer, Menus):
    Out  = "<!DOCTYPE html>\n"
    Out += "<html>\n"
    Out += "\n"
    Out += "<head>\n"
    Out += "  <meta charset=\"UTF-8\">\n"
    Out += "  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
    if Description != "":
      Out += "  <meta name=\"description\" content=\"" + Description + "\">\n"
    Out += "  <title>" + Title + "</title>\n"
    Out += "  <script type=\"text/javascript\" src=\"neodym.js\"></script>\n"
    Out += "  <link rel=\"stylesheet\" type=\"text/css\" href=\"neodym.css\">\n"
    Out += "  <link rel=\"stylesheet\" type=\"text/css\" href=\"neodym-user.css\">\n"

    for Name in self.mCSSFileNames:
      Out += "  <link rel=\"stylesheet\" type=\"text/css\" href=\"" + Name + "\">\n"

    for Name in self.mJavaScriptFileNames:
      Out += "  <script type=\"text/javascript\" src=\"" + Name + "\"></script>\n"

    Out += "</head>\n"
    Out += "\n"
    Out += "<body>\n"
    Out += "  <div id=\"nd-master\">\n"
    Out += "    <div id=\"nd-header\">\n"
    Out += "      <div id=\"nd-upper-header-container\">\n"

    if Logo != "":
      Out += "        <div id=\"nd-logo-container\">\n"
      Out += "          <img id=\"nd-logo\" src=\"" + Logo + "\" alt=\"MEGAlib Logo\">\n"
      Out += "        </div>\n"
    
    Out += "        <div id=\"nd-title-container\">\n"
    Out += "          <div id=\"nd-title\">" + Title + "</div>\n"
  
    if SubTitle != "":
      Out += "          <div id=\"nd-subtitle\">" + SubTitle + "</div>\n"

    Out += "        </div>\n"
    Out += "        <div id=\"nd-menubutton\" onclick='ToggleSubMenu();'>\n"
    Out += "          <div id=\"nd-menubutton-text\">&equiv;</div>\n"
    Out += "        </div>\n"
    Out += "      </div>\n"
    Out += "      <div id=\"nd-mainmenu\">\n"
    Out += "        <ul id=\"nd-mainmenu-list\">\n"

    for Key in Menus:
      if Key == self.mMenuEntry:
        Out += "          <li class=\"nd-mainmenu-element nd-mainmenu-element-activated\"><a class=\"nd-mainmenu-element-link\" href=\"" + Menus[Key].mFileName + "\">" + Menus[Key].mMenuTitle + "</a></li>\n"
      else:
        Out += "          <li class=\"nd-mainmenu-element\"><a class=\"nd-mainmenu-element-link\" href=\"" + Menus[Key].mFileName + "\">" + Menus[Key].mMenuTitle + "</a></li>\n"

    Out += "        </ul>\n"
    Out += "      </div>\n"
    Out += "    </div>\n"
    Out += "    \n"
    Out += "    <div id=\"nd-content\" onclick=\"DeactivateSubMenu()\">\n"
    Out += "\n"
    Out += "<!-- --- body start --- -->\n"
    Out += "\n"
    Out += self.mBody
    Out += "\n"
    Out += "<!-- --- body end --- -->\n"
    Out += "\n"
    Out += "    </div>\n"

  
    if Footer != "":
      Out += "    <div id=\"nd-footer\">\n"
      Out += "      " + Footer + "<br>\n"
      Out += "      Powered by <a href=\"https://github.com/zoglauer/neodym\">Neodym</a>\n"
      Out += "    </div>\n"
    
    Out += "  </div>\n"
    Out += "</body>\n"
    Out += "\n"
    Out += "</html>\n"

    return Out

# -----------------------------------------------------------------------------------
