#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
import re
import os

# Import neodym files
from reader import ZReader

# -----------------------------------------------------------------------------------

# A page whcih is part og the menu structure
class ZPage(ZReader):
  
  # Constructor
  def __init__(self):
    super(ZPage, self).__init__()
    
    # All the files referenced by this page
    self.mFiles = []

  
  # Read the file
  def read(self, FileName):
    print("Read Page")
    super(ZPage, self).read(FileName)
    ZPage.assign(self)

    return True
  
  
  # Assimilate a reader into this page
  def assimilate(self, Reader):
    print("Assimilate Reader into Page")
    super(ZPage, self).assimilate(Reader)
    ZPage.assign(self)	
    
    return True


  # Extract all additional information from the content into this page
  def assign(self):
    print("Assign Page")

    # Extract figures
    Pattern = re.compile(r'img src=\"(.*?)\"')
    self.mFiles = re.findall(Pattern, self.mMainContent)
    
    # Extract potential documents
    Pattern = re.compile(r'href=\"(.*?)\"')
    Docs = re.findall(Pattern, self.mMainContent)
    for File in Docs:
      if os.path.isfile("content" + os.sep + File) == True:
        self.mFiles.append(File)
    
    print("Files: ", self.mFiles)  


# -----------------------------------------------------------------------------------
