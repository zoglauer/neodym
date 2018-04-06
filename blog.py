#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files

# Import neodym files
from page import ZPage

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
