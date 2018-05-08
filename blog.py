#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
from bs4 import BeautifulSoup
import os

# Import neodym files
from feature import ZFeature
from reader import ZReader
from blogentry import ZBlogEntry

# -----------------------------------------------------------------------------------

class ZBlog(ZFeature):
  def __init__(self):
    super(ZBlog, self).__init__()
    self.mFeatureTag = "neodym-blog"
    self.mBlogEntries = []

  def apply(self, Article):
    #
    Body = BeautifulSoup(Article.mBody, 'html.parser')
    Tags = Body.find_all(self.mFeatureTag)
    
    if len(Tags) == 0:
      return
    if len(Tags) > 1: 
      print("Error: Only one <" + self.mFeatureTag + "> allowed")
      return

    # Find the directory where all blog entries are stored
    Directory = "blog"
    if "BlogDirectory" in Article.mDictionary:
      Directory = Article.mDictionary["BlogDirectory"]

    Directory = Article.mFilePath + os.sep + Directory
    print("A:" + Article.mFilePath)
    print("D:" + Directory)

    # Read all blog entries
    self.readBlogs(Directory)
    
    print("Number of Blogs: " + str(len(self.mBlogEntries)))
    
    # 
    ReplacementText = ""
    for B in self.mBlogEntries:
      ReplacementText += B.createPage()
    
    print("ReplacementText:")
    print(ReplacementText)
    
    PS = BeautifulSoup(ReplacementText, 'html.parser')
    Tags[0].replace_with(PS)
      
    Article.mBody = Body.prettify();


  def readBlogs(self, Directory):
    print("1")
    # Read all files (html)
    for SubDir, Dirs, Files in os.walk(Directory):
      print("1")
      for File in Files:
        print("1")
    
        if File.endswith(".html") == False: continue
        print("1")
  
        FilePath = SubDir + os.sep + File
        print ("Reading %s..." % (FilePath))
        Entry = ZBlogEntry()
        Entry.read(FilePath)
        if Entry.has("Type", "BlogEntry"):
          print("1")
          self.mBlogEntries.append(Entry)

    # Final sort by date
    self.mBlogEntries.sort(key=lambda x: x.mDate, reverse=True)


# -----------------------------------------------------------------------------------
