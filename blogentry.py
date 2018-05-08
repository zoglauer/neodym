#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
from datetime import datetime

# Import neodym files
from page import ZPage

# -----------------------------------------------------------------------------------


# The basic information of a blog entry: title, summary, main text blog
class ZBlogEntry(ZPage):
  def __init__(self):
    super(ZBlogEntry, self).__init__()
    self.mDate = ""
    self.mTitle = ""
    self.mSummary = ""
    self.mMain = ""


  def assign(self):
    print("Assign ZBlogEntry")  

    if "Date" in self.mDictionary:
      self.mDate = datetime.strptime(self.mDictionary["Date"], '%Y-%m-%d')

    self.mTitle = self.extractSingleTag("neodym-blog-title") 
    if self.mTitle == "":
      print("ERROR: <neodym-blog-title>...</neodym-blog-title> tag not found in blog entry")
    
    self.mSummary = self.extractSingleTag("neodym-blog-summary") 
    if self.mSummary == "":
      print("ERROR: <neodym-blog-summary>...</neodym-blog-summary> tag not found in blog entry")
    
    self.mMain = self.extractSingleTag("neodym-blog-body") 
    if self.mMain == "":
      print("ERROR: <neodym-blog-body>...</neodym-blog-body> tag not found in blog entry")
    
    
  def read(self, FileName):
    print("Read ZBlogEntry")
    super(ZBlogEntry, self).read(FileName)
    ZBlogEntry.assign(self)
    return True

  
  def assimilate(self, Reader):
    print("Assimilate ZBlogEntry")
    super(ZBlogEntry, self).assimilate(Reader)
    ZBlogEntry.assign(self)	
    return True
      
      
  def createPage(self):
    Out = "\n"
    
    Out += "  <div class=\"nd-blog-date\">\n"
    Out += self.mDate.strftime('%A, %B %d, %Y')
    Out += "  </div>\n"
    
    Out += "  <div class=\"nd-blog-title\">\n"
    Out += self.mTitle
    Out += "  </div>\n"

    Out += "  <div class=\"nd-blog-summary\">\n"
    Out += self.mSummary
    Out += "  </div>\n"

    Out += "  <div class=\"nd-blog-body\">\n"
    Out += self.mMain
    Out += "  </div>\n"

    return Out



# -----------------------------------------------------------------------------------
