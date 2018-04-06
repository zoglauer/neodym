#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
import os
import shutil
from collections import OrderedDict

# Import neodym files
from configuration import ZConfiguration
from reader import ZReader
from article import ZArticle
from pictureshow import ZPictureShow
from bibliography import ZBibliography

# -----------------------------------------------------------------------------------

def CopyFiles(Article):

  for FileName in Article.mFiles:
    CopyFile(FileName)
  for Name in Article.mCSSFileNames:
    CopyFile(Name)
  for Name in Article.mJavaScriptFileNames:
    CopyFile(Name)
  
# -----------------------------------------------------------------------------------
  
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

# -----------------------------------------------------------------------------------

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



# -----------------------------------------------------------------------------------

