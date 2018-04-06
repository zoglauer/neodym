#!/usr/bin/env python3

import os
import shutil
import re
import bibtexparser
from collections import OrderedDict
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------------

class ZReader:
  def __init__(self):
    self.mFileName = ""
    self.mContent = []
    self.mDictionary = {}
    self.mFiles = []
    self.mBody = ""
    print("Reader init")
  

  def read(self, Name):
    self.mFileName = os.path.basename(Name)
    with open(Name) as File:
      self.mContent = File.readlines()
    self.mContent = [X.strip() for X in self.mContent] 
  
    InBody = False
    for Line in self.mContent:
      if InBody == True:
        self.mBody += Line
        self.mBody += "\n"  
      else: 
        if Line.startswith("<neodym-body>"):
          InBody = True
          self.mBody += Line
          self.mBody += "\n"          
        else:
          if Line.find(":") != -1:
            Split = Line.split(":", maxsplit=2)
            if len(Split) == 2 and Split[0].strip() != "" and Split[1].strip() != "":
              self.mDictionary[Split[0].strip()] = Split[1].strip()
              print("Added to dictionary: " + Split[0].strip() + ", " + Split[1].strip()) 
            #else:
            #  print("Error: Unknown keyword: ", Line)
    
    # Remove the <body> & </body> tags
    self.mBody = self.mBody.replace("<neodym-body>", "")
    self.mBody = self.mBody.replace("</neodym-body>", "")
    
    # Extract figures
    Pattern = re.compile(r'img src=\"(.*?)\"')
    self.mFiles = re.findall(Pattern, self.mBody)
    
    # Extract potential documents
    Pattern = re.compile(r'href=\"(.*?)\"')
    Docs = re.findall(Pattern, self.mBody)
    for File in Docs:
      if os.path.isfile("content" + os.sep + File) == True:
        self.mFiles.append(File)
    
    print("Files: ", self.mFiles)
    
    return True


  def assimilate(self, Reader):
    self.mDictionary = Reader.mDictionary
    self.mBody = Reader.mBody
    self.mFileName = Reader.mFileName
    self.mFiles = Reader.mFiles

    
  def has(self, Key, Value):
    if Key in self.mDictionary:
      return self.mDictionary[Key] == Value 
    else:
      return False


  def extractSingleTag(self, Name):
    
    Start = "<" + Name + ">"
    End = "</" + Name + ">"
    
    Found = False
    InTag = False
    
    Tag = ""
    
    # Extract all the lines from where the tag appearsvthe first time including the line where it ends
    for Line in self.mContent:
      if Found == True:
        if InTag == True:
          self.mBody += Line
          self.mBody += "\n"
          if End in Line:
            InTag = False
        else:
          if Start in Line:
            print("ERROR: Tag appears multiple times")
            return ""
      else: 
        if Start in Line:
          Found = True
          InTag = True
          Tag += Line 
          Tag += "\n" 
    
    if InTag == True:
      print("ERROR: Tag not closed")
      return ""
    
    # Remove everything to the Start and everything after the End
    StartIndex = Tag.index(Start) + len(Start)
    EndIndex = Tag.index(End, StartIndex)
    
    return Tag[StartIndex:EndIndex]
    

# -----------------------------------------------------------------------------------

class ZConfiguration(ZReader):
  def __init__(self):
    super(ZConfiguration, self).__init__()
    self.mTitle = "Neodym"
    self.mSubTitle = ""
    self.mDescription = ""
    self.mFooter = ""
    self.mMenu = []
    self.mLogo = ""
    self.mContentDirectory = "."
    self.mTemplateDirectory = "."
    self.mTargetDirectory = "public"
    self.mTargetPermissions = "a+rX"
    print("Config init")

  def assign(self):
    if "Title" in self.mDictionary:
      self.mTitle = self.mDictionary["Title"]
    if "SubTitle" in self.mDictionary:
      self.mSubTitle = self.mDictionary["SubTitle"]
    if "Description" in self.mDictionary:
      self.mDescription = self.mDictionary["Description"]
    if "Logo" in self.mDictionary:
      self.mLogo = self.mDictionary["Logo"]
    if "Footer" in self.mDictionary:
      self.mFooter = self.mDictionary["Footer"]
    if "self.mContentDirectory" in self.mDictionary:
      self.mself.mContentDirectory = self.mDictionary["self.mContentDirectory"]
    if "TemplateDirectory" in self.mDictionary:
      self.mTemplateDirectory = self.mDictionary["TemplateDirectory"]
    if "TargetDirectory" in self.mDictionary:
      self.mTargetDirectory = self.mDictionary["TargetDirectory"]
    if "TargetPermissions" in self.mDictionary:
      self.mTargetPermissions = self.mDictionary["TargetPermissions"]
      

  def read(self, FileName):
    super(ZConfiguration, self).read(FileName)
    self.assign()	
    return True
  
  def print(self):
    print("# Configuration of file " + self.mFileName)
    print("Logo: " + self.mLogo)
    print("Title: " + self.mTitle)
    print("SubTitle: " + self.mSubTitle)
    print("Description: " + self.mSubTitle)
    print("Footer: " + self.mFooter)
    print("ConentDirectory: " + self.mContentDirectory)
    print("TemplateDirectory: " + self.mTemplateDirectory)
    print("TargetDirectory: " + self.mTargetDirectory)
    print("TargetPermissions: " + self.mTargetPermissions)



# -----------------------------------------------------------------------------------

class ZPage(ZReader):
  def __init__(self):
    super(ZPage, self).__init__()
    self.mMenuLevel = 0
    self.mMenuEntry = 0
    self.mMenuTitle = ""
    self.mBody = ""
  

  def assign(self):
    print("Assign Page")
    if "MenuLevel" in self.mDictionary:
      self.mMenuLevel = int(self.mDictionary["MenuLevel"])
    if "MenuEntry" in self.mDictionary:
      self.mMenuEntry = int(self.mDictionary["MenuEntry"])
    if "MenuTitle" in self.mDictionary:
      self.mMenuTitle = self.mDictionary["MenuTitle"]
  
  
  def read(self, FileName):
    print("Read Page")
    super(ZPage, self).read(FileName)
    ZPage.assign(self)
    
    # Parse neody-body
    InBody = False
    for Line in self.mContent:
      if InBody == True:
        self.mBody += Line
        self.mBody += "\n"  
      else: 
        if Line.startswith("<neodym-body>"):
          InBody = True
          self.mBody += Line
          self.mBody += "\n"          
        else:
          if Line.find(":") != -1:
            Split = Line.split(":", maxsplit=2)
            if len(Split) == 2 and Split[0].strip() != "" and Split[1].strip() != "":
              self.mDictionary[Split[0].strip()] = Split[1].strip()
              print("Added to dictionary: " + Split[0].strip() + ", " + Split[1].strip()) 
            #else:
            #  print("Error: Unknown keyword: ", Line)
    
    # Remove the <body> & </body> tags
    self.mBody = self.mBody.replace("<neodym-body>", "")
    self.mBody = self.mBody.replace("</neodym-body>", "")
    
    return True
  
  
  def assimilate(self, Reader):
    print("Assim Article")
    super(ZPage, self).assimilate(Reader)
    ZPage.assign(self)	
    return True



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
      if Key == A.mMenuEntry:
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

class ZBlog(ZPage):
  def __init__(self):
    super(ZBlog, self).__init__()
    self.mDate = ""
    self.mBlogTitle = []
    self.mBlogSummary = []
    self.mBlogBody = []


  def assign(self):
    print("Assign ")
    if "Date" in self.mDictionary:
      self.mDate = self.mDictionary["Date"]  
  
  
  def read(self, FileName):
    print("Read Blog")
    super(ZBlog, self).read(FileName)
    ZBlog.assign(self)
    return True
  
  
  def assimilate(self, Reader):
    print("Assim Blog")
    super(ZBlog, self).assimilate(Reader)
    ZBlog.assign(self)	
    return True


# -----------------------------------------------------------------------------------

class ZFeature():
  def __init__(self):
    self.mFeatureTag = ""
  
  def apply(self, Article):
    print("Applying feature")

  def hasFeature(self, Article):
    if self.mFeatureTag == "":
      return False
    else:
      print("Count: " + str(Article.mBody.count(self.mFeatureTag)))
      if Article.mBody.count(self.mFeatureTag) == 0:
        return False
      else:
        return True
      

# -----------------------------------------------------------------------------------

class ZBibliography(ZFeature):
  def __init__(self):
    super(ZBibliography, self).__init__()
    self.mFeatureTag = "<neodym-papers />"
    self.mPapersDB = []
    self.mHighlightNames = []
    self.mPapersDBFileNames = ""
    

  def apply(self, Article):
    print("Checking to apply feature " + self.mFeatureTag + " to " + Article.mMenuTitle)
    
    if self.hasFeature(Article) == False:
      print("   --> no")
      return
    
    self.mHighlightAuthor = ""
    if "HighlightAuthor" in Article.mDictionary:
      self.mHighlightAuthor = Article.mDictionary["HighlightAuthor"]
      
    print("HN (1): " + self.mHighlightAuthor)  
      
    self.mPapersDBFileNames = ""
    if "PapersBibtexFiles" in Article.mDictionary:
      self.mPapersDBFileNames = Article.mDictionary["PapersBibtexFiles"]
    if self.mPapersDBFileNames == "":
      print("ERROR: No bib-tex file name found")
      return
  
  
  
    SplitAuthor = self.mHighlightAuthor.split(",")
    LastName = ""
    FirstNames = ""
    if len(SplitAuthor) >= 1:
      LastName = SplitAuthor[0]
    if len(SplitAuthor) > 1:
      FirstNames = SplitAuthor[1]

    # Now add all abbrevations of the first name
    SplitFirstName = FirstNames.split(" ")
    SplitFirstName = list(filter(None, SplitFirstName))
    
    if len(SplitFirstName) == 1:
      self.mHighlightNames.append(SplitFirstName[0] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + LastName)
    elif len(SplitFirstName) == 2:
      self.mHighlightNames.append(SplitFirstName[0] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + LastName)
      self.mHighlightNames.append(SplitFirstName[0] + " " + SplitFirstName[1] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + SplitFirstName[1] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0] + " " + SplitFirstName[1][0] + ". " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + SplitFirstName[1][0] + ". " + LastName)
    
    #print("HN: " + self.mHighlightAuthor + "  L:" + LastName + "  F:" + FirstNames + "  split=" + str(len(SplitFirstName)))
    #for s in SplitFirstName: print(">>" + s + "<<")
    #print("HN:")
    #for s in self.mHighlightNames: print(s)
    
    self.readDBs(Config.mContentDirectory)
    
    ReplacementHTML = self.createHTML()
    
    Article.mBody = Article.mBody.replace(self.mFeatureTag, ReplacementHTML)
  
    
  
  def readDBs(self, Directory):

    with open(Directory + os.sep + self.mPapersDBFileNames) as bibtex_file:
      bibtex_str = bibtex_file.read()
      
    self.mPapersDB = bibtexparser.loads(bibtex_str)
    #print(self.mPapersDB.entries)



  def createHTML(self):
    HTML = ""
    HTML += "<h2>Papers</h2>\n"
    HTML += "  <ul>\n"

    
    for Article in self.mPapersDB.entries:
      
      if "title" in Article: Title = Article["title"]
      
      HTML += "    <li>"
      
      # 1. Nicen authors:
      if "author" in Article: AllAuthors = Article["author"]
      AllAuthors = self.nicen(AllAuthors)
      Authors = AllAuthors.split(" and")
      
      First = True
      for A in Authors:
        SplitAuthor = A.split(",")

        FirstNames = ""
        LastName = ""
        if len(SplitAuthor) >= 1:
          LastName = SplitAuthor[0].strip()
        if len(SplitAuthor) > 1:
          FirstNames = SplitAuthor[1].strip()
        
        if First == False:
          HTML += ", ";
        else:
          First = False
          
        AuthorName = ""
        if FirstNames != "":
          AuthorName += FirstNames + " ";
        if LastName != "":
          AuthorName += LastName;
          
        FoundName = False
        for Name in self.mHighlightNames:
          #print("Testing: " + Name + " vs " + AuthorName)
          if Name == AuthorName:
            #print("Found: " + Name)
            FoundName = True
            break
          
        if FoundName == False:
          HTML += AuthorName
        else:
          HTML += "<b>" + AuthorName + "</b>"
      
      # 2. Title
      Title = self.nicen(Title)
      HTML += ", <i>\"" + Title + "\"</i>"
      
      # 3. Journal
      Journal = ""
      if "journal" in Article: Journal = Article["journal"]
      Journal = self.nicenJournal(Journal)
      
      if Journal == "":
        if "booktitle" in Article: Journal = Article["booktitle"]
        if Journal != "":
          Journal = self.nicenJournal(Journal)
          Series = ""
          if "series" in Article: Series = Article["series"]
          if Series != "":
            Series = self.nicenJournal(Series)
            HTML += ", " + Series + ": " + Journal
          else:
            HTML += ", " + Journal

      else:
        HTML += ", " + Journal
        if "volume" in Article: Volume = Article["volume"]
        if Volume != "":
          HTML += " <b>" + Volume + "</b>"
          if "pages" in Article: Pages = Article["pages"]
          if Pages != "":
            HTML += ": " + Pages

      if "year" in Article: Year = Article["year"]
      if "month" in Article: Month = Article["month"]
      Month = self.nicenMonth(Month)
      
      if Month != "" and Year != "":
        HTML += ", " + Month + "/" + Year
      elif Year != "":
        HTML += ", " + Year
      
      HTML += "</li>\n"
    HTML += "  </ul>\n"
    
    return HTML


  def nicen(self, Text):
    Text = Text.replace("{\\\"o}", "oe")
    Text = Text.replace("{\\\"u}", "ue")
    Text = Text.replace("{\\\"a}", "ae")
    Text = Text.replace("{\\'c}", "c")
    Text = Text.replace("{\\`e}", "e")
    Text = Text.replace("{\\'e}", "e")
    Text = Text.replace("{$\\alpha$}", "alpha")
    Text = Text.replace("{$\\beta$}", "beta")
    Text = Text.replace("{$\\gamma$}", "gamma")
    Text = Text.replace("{$^{44}$}", "44-")

    for s in "[]{}":
      Text = Text.replace(s, "")
    for s in "~\n":
      Text = Text.replace(s, " ")
    
    return Text

  
  def nicenJournal(self, Text):
    print("Journal: " + Text)
    if Text == "\\apj":
      return "The Astrophysical Journal"
    if Text == "\\nat":
      return "Nature"
    if Text == "\\nar":
      return "New Astronomy Reviews"
    if Text == "\\procspie":
      return "Proceedings of SPIE"
    return Text

  
  def nicenMonth(self, Text):
    if Text == "jan":
      return "1"
    if Text == "feb":
      return "2"
    if Text == "mar":
      return "3"
    if Text == "apr":
      return "4"
    if Text == "mai":
      return "5"
    if Text == "jun":
      return "6"
    if Text == "jul":
      return "7"
    if Text == "aug":
      return "8"
    if Text == "sep":
      return "9"
    if Text == "oct":
      return "10"
    if Text == "nov":
      return "11"
    if Text == "dec":
      return "12"
    
    return ""



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
# -----------------------------------------------------------------------------------

def CopyFiles(Article):

  for FileName in Article.mFiles:
    CopyFile(FileName)
  for Name in Article.mCSSFileNames:
    CopyFile(Name)
  for Name in Article.mJavaScriptFileNames:
    CopyFile(Name)
  
  
def CopyFile(FileName):
  NewFileName = Config.mTargetDirectory + os.sep + FileName
  OldFileName = "content" + os.sep + FileName
  
  # Check if the fike exists:
  if os.path.isfile(OldFileName) == False:
    OldFileName = Config.mTemplateDirectory + os.sep + FileName
    if os.path.isfile(OldFileName) == False:
      print("ERROR: Unable to find file: " + FileName)
    
  Dirs = []
  path = os.path.dirname(NewFileName)
  while True:
    path, folder = os.path.split(path)
      
    if folder != "":
      Dirs.append(folder)
    else:
      break
  Dirs.reverse()
   
  if len(Dirs) > 0 and Config.mTargetDirectory[0] == "/":
    Dirs[0] = "/" + Dirs[0] 
 
  FullPath = ""
  for Dir in Dirs:
    if FullPath != "":
      FullPath += os.sep + Dir
    else:
      FullPath += Dir
    print("Checking to create path: ", FullPath)
    if os.path.isdir(FullPath) == False:
      os.makedirs(FullPath)
  
  print("Copying: ", OldFileName, " --> ", NewFileName)
  shutil.copy(OldFileName, NewFileName)



# -----------------------------

def getMainIndex(Title, Menus):
  Out="<!DOCTYPE html>\n"
  Out += "<html>\n"
  Out += "\n"
  Out += "<head>\n"
  Out += "\n"
  Out += "  <meta charset=\"UTF-8\">\n"
  Out += "  <title>" + Title + "</title>\n"
  Out += "\n"
  Out += "  <script language=\"javascript\" type=\"text/javascript\">\n"
  Out += "    console.log('Width: %d', screen.width);\n"
  Out += "    window.location=\"" + list(Menus.values())[0].mFileName + "\";\n"
  Out += "  </script>\n"
  Out += "\n"
  Out += "</head>\n"
  Out += "\n"
  Out += "<body>\n"
  Out += "\n"
  Out += "  <h1>You seem to have disabled Javascript. But unfortunately, this website's main engine is written in Javascript! Thus please, please enable it.</h1>\n"
  Out += "\n"
  Out += "</body>\n"
  Out += "\n"
  Out += "</html>\n"

  return Out





# MAIN ------------------------------------------------------------------------------------------


Config = ZConfiguration()
Pages = []
Articles = []
Bibliographies = []
MenuTitles = []


# (1) Read the configuration file
if Config.read("neodym.conf") == False:
  print("Error: Unable to read configuation file")
  sys.exit(1)
 
Config.print()

# (2) Read all the content files (html)
for SubDir, Dirs, Files in os.walk(Config.mContentDirectory):
  for File in Files:
    
    if File.endswith(".html") == False: continue
  
    FilePath = SubDir + os.sep + File
    print ("Reading %s..." % (FilePath))
    Reader = ZReader()
    Reader.read(FilePath)
    if Reader.has("Type", "Article"):
      Article = ZArticle()
      Article.assimilate(Reader)
      Articles.append(Article)
      Pages.append(Article)
    if Reader.has("Type", "Bibliography"):
      Bibliography = ZBibliography()
      Bibliography.assimilate(Reader)
      Bibliography.readDBs(Config.mContentDirectory)
      Bibliographies.append(Bibliography)
      Pages.append(Bibliography)

if len(Pages) == 0:
  print("Error: No pages found")
  sys.exit(1)

for P in Pages:
  print("Found page with menu title: %s" % (P.mMenuTitle))


# (3) Creating the main menu based on the articles
mMenu = {}
for P in Pages:
  mMenu[P.mMenuEntry] = P
  
mMenu = OrderedDict(sorted(mMenu.items()))

if len(mMenu) == 0:
  print("Error: No menu entries found")
  sys.exit(1)

print(mMenu)


# (4) Handle all neodym features
for A in Articles:
  # (4a) Pictureshow
  P = ZPictureShow()
  P.apply(A)

  # (4b) Bibliography
  B = ZBibliography()
  B.apply(A)


# (5) Start putting it all together and copy all files

# (5a) Create the target directory if it does not exit
if os.path.isdir(Config.mTargetDirectory) == False:
  os.makedirs(Config.mTargetDirectory)

# (5b) Copy template files
shutil.copy(Config.mTemplateDirectory + os.sep + "neodym.js", Config.mTargetDirectory + os.sep + "neodym.js")
shutil.copy(Config.mTemplateDirectory + os.sep + "neodym.css", Config.mTargetDirectory + os.sep + "neodym.css")
if os.path.isfile(Config.mTemplateDirectory + os.sep + "neodym-user.css"):
  shutil.copy(Config.mTemplateDirectory + os.sep + "neodym-user.css", Config.mTargetDirectory + os.sep + "neodym-user.css")

# (5c) Copy logo
if Config.mLogo != "":
  CopyFile(Config.mLogo)
  
# (5d) Create index file 
File = open(Config.mTargetDirectory + os.sep + "index.html","w")
File.write(getMainIndex(Config.mTitle, mMenu))
File.close()

# (5e) Create articles, add all features and copy all files associated with the article
for A in Articles:
  
  # Create the articles  
  PageText = A.createPage(Config.mTitle, Config.mSubTitle, Config.mDescription, Config.mLogo, Config.mFooter, mMenu)

  FileName = Config.mTargetDirectory + os.sep + os.path.basename(A.mFileName)
  print(FileName)
  File = open(FileName, "w")
  File.write(PageText)
  File.close()
  
  # Copy all associated files:
  CopyFiles(A)

  
# (5f) Set the correct permissions
os.system("chmod -R " + Config.mTargetPermissions + " " + Config.mTargetDirectory)
  

# ... and we are done!
print("DONE!")













