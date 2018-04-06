#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
import os
import re

# Import neodym files

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
