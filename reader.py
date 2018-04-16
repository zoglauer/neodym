#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
import os

# Import neodym files

# -----------------------------------------------------------------------------------


# This class reads the file line-by-line and stores it in mFileContent.
# if finds the configuration and reads it into the dictionary
class ZReader:
  def __init__(self):
    # The file name without path for href's in the webpage
    self.mFileName = ""
    # The complete file content - line by line
    self.mFileContent = []
    # The main content without the configurations
    self.mMainContent = ""
    # The dictionary con
    self.mDictionary = {}
  
  
  # Read the file
  def read(self, FileName):
    self.mFileName = os.path.basename(FileName)
    with open(FileName) as File:
      self.mFileContent = File.readlines()
    self.mFileContent = [X.strip() for X in self.mFileContent] 
  
    InConfig = False
    for Line in self.mFileContent:
      if "<!-- neodym-config" in Line:
        InConfig = True
        continue
      if InConfig == True and "-->" in Line:
        InConfig = False
        continue
      if InConfig == True:
        if Line.find(":") != -1:
          Split = Line.split(":", maxsplit=2)
          if len(Split) == 2 and Split[0].strip() != "" and Split[1].strip() != "":
            self.mDictionary[Split[0].strip()] = Split[1].strip()
            print("Added to dictionary: " + Split[0].strip() + ", " + Split[1].strip()) 
      else:
        self.mMainContent += Line
        self.mMainContent += "\n"
    
    return True


  # Copy data into this reader
  def assimilate(self, Reader):
    self.mFileName = Reader.mFileName
    self.mFileContent = Reader.mFileContent
    self.mMainContent = Reader.mMainContent
    self.mDictionary = Reader.mDictionary


  
  # Check if the configuration has a key
  def has(self, Key, Value):
    if Key in self.mDictionary:
      return self.mDictionary[Key] == Value 
    else:
      return False


  # Extract a single Tag from the file content
  def extractSingleTag(self, Name):
    
    print("Extract")
    
    Start = "<" + Name + ">"
    End = "</" + Name + ">"
    
    Found = False
    InTag = False
    
    Tag = ""
    
    # Extract all the lines from where the tag appears, the first time including the line where it ends
    for Line in self.mFileContent:
      if Found == True:
        if InTag == True:
          Tag += Line 
          Tag += "\n" 
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
    
    if Found == False:
      print("Nothing found")
      return ""
    
    # Remove everything to the Start and everything after the End
    StartIndex = Tag.index(Start) + len(Start)
    EndIndex = Tag.index(End, StartIndex)
    
    print("Tag: " + Tag)
    print("Tag: " + str(StartIndex))
    print("Tag: " + str(EndIndex))
    
    return Tag[StartIndex:EndIndex]
    

# -----------------------------------------------------------------------------------
