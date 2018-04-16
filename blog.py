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

# -----------------------------------------------------------------------------------

class ZBlog(ZFeature):
  def __init__(self):
    super(ZBlog, self).__init__()
    self.mFeatureTag = "neodym-blog"
    self.mBlogEntries = []

  def apply(self, Article):
    #
    Body = BeautifulSoup(Article.mBody, 'html.parser')
    Tag = Body.find_all(self.mFeatureTag)
    
    if len(Tag) == 0:
      return
    if len(Tag) > 1: 
      print("Error: Only one <" + self.mFeatureTag + "> allowed")
      return

    # Find the directory where all blog entries are stored
    Directory = "blog"
    if "BlogDirectory" in Article.mDictionary:
      Directory = Article.mDictionary["BlogDirectory"]

    # Read all blog enetries
    self.readBlogs(Directory)
    
    # 
    

  def readBlogs(self, Directory):
    # Read all files (html)
    for SubDir, Dirs, Files in os.walk(Directory):
      for File in Files:
    
        if File.endswith(".html") == False: continue
  
        FilePath = SubDir + os.sep + File
        print ("Reading %s..." % (FilePath))
        Reader = ZReader()
        Reader.read(FilePath)
        if Reader.has("Type", "BlogEntry"):
          BlogEntry = ZBlogEntry()
          BlogEntry.assimilate(Reader) 
          self.mBlogEntries.append(BlogEntry)



# -----------------------------------------------------------------------------------
