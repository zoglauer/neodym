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
