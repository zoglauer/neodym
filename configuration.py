#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files

# Import neodym files
from reader import ZReader

# -----------------------------------------------------------------------------------

# Parses all the global configuration parameters
class ZConfiguration(ZReader):
  
  # Constructor
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
    if "ContentDirectory" in self.mDictionary:
      self.mContentDirectory = self.mDictionary["ContentDirectory"]
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
    print("Configuration of file " + self.mFileName)
    print("Logo:              " + self.mLogo)
    print("Title:             " + self.mTitle)
    print("SubTitle:          " + self.mSubTitle)
    print("Description:       " + self.mSubTitle)
    print("Footer:            " + self.mFooter)
    print("ContentDirectory:  " + self.mContentDirectory)
    print("TemplateDirectory: " + self.mTemplateDirectory)
    print("TargetDirectory:   " + self.mTargetDirectory)
    print("TargetPermissions: " + self.mTargetPermissions)

# -----------------------------------------------------------------------------------
