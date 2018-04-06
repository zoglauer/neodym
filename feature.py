#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files

# Import neodym files

# -----------------------------------------------------------------------------------

class ZFeature():
  def __init__(self):
    self.mFeatureTag = ""
  
  def apply(self, Article):
    print("Applying feature")

  def hasFeature(self, Article):
    if self.mFeatureTag == "":
      return False
    else:
      print("Count: " + str(Article.mBody.count(self.mFeatureTag)))
      if Article.mBody.count(self.mFeatureTag) == 0:
        return False
      else:
        return True
      

# -----------------------------------------------------------------------------------
