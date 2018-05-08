#
# Neodym
#
# Copyright (C) by Andreas Zoglauer and contributors
# Please see the license file for more details.
#

# -----------------------------------------------------------------------------------

# Import external files
import bibtexparser
import os

# Import neodym files
from feature import ZFeature

# -----------------------------------------------------------------------------------

class ZBibliography(ZFeature):
  def __init__(self):
    super(ZBibliography, self).__init__()
    self.mFeatureTag = "<neodym-papers />"
    self.mPapersDB = []
    self.mHighlightNames = []
    self.mPapersDBFileNames = ""
    

  def apply(self, Article):
    print("Checking to apply feature " + self.mFeatureTag + " to " + Article.mMenuTitle)
    
    if self.hasFeature(Article) == False:
      print("   --> no")
      return
    
    self.mHighlightAuthor = ""
    if "HighlightAuthor" in Article.mDictionary:
      self.mHighlightAuthor = Article.mDictionary["HighlightAuthor"]
      
    print("HN (1): " + self.mHighlightAuthor)  
      
    self.mPapersDBFileNames = ""
    if "PapersBibtexFiles" in Article.mDictionary:
      self.mPapersDBFileNames = Article.mDictionary["PapersBibtexFiles"]
    if self.mPapersDBFileNames == "":
      print("ERROR: No bib-tex file name found")
      return
  
  
  
    SplitAuthor = self.mHighlightAuthor.split(",")
    LastName = ""
    FirstNames = ""
    if len(SplitAuthor) >= 1:
      LastName = SplitAuthor[0]
    if len(SplitAuthor) > 1:
      FirstNames = SplitAuthor[1]

    # Now add all abbrevations of the first name
    SplitFirstName = FirstNames.split(" ")
    SplitFirstName = list(filter(None, SplitFirstName))
    
    if len(SplitFirstName) == 1:
      self.mHighlightNames.append(SplitFirstName[0] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + LastName)
    elif len(SplitFirstName) == 2:
      self.mHighlightNames.append(SplitFirstName[0] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + LastName)
      self.mHighlightNames.append(SplitFirstName[0] + " " + SplitFirstName[1] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + SplitFirstName[1] + " " + LastName)
      self.mHighlightNames.append(SplitFirstName[0] + " " + SplitFirstName[1][0] + ". " + LastName)
      self.mHighlightNames.append(SplitFirstName[0][0] + ". " + SplitFirstName[1][0] + ". " + LastName)
    
    #print("HN: " + self.mHighlightAuthor + "  L:" + LastName + "  F:" + FirstNames + "  split=" + str(len(SplitFirstName)))
    #for s in SplitFirstName: print(">>" + s + "<<")
    #print("HN:")
    #for s in self.mHighlightNames: print(s)
    
    self.readDBs(Article.mFilePath)
    
    ReplacementHTML = self.createHTML()
    
    Article.mBody = Article.mBody.replace(self.mFeatureTag, ReplacementHTML)
  
    
  
  def readDBs(self, Directory):

    with open(Directory + os.sep + self.mPapersDBFileNames) as bibtex_file:
      bibtex_str = bibtex_file.read()
      
    self.mPapersDB = bibtexparser.loads(bibtex_str)
    #print(self.mPapersDB.entries)



  def createHTML(self):
    HTML = ""
    HTML += "<h2>Papers</h2>\n"
    HTML += "  <ul>\n"

    
    for Article in self.mPapersDB.entries:
      
      if "title" in Article: Title = Article["title"]
      
      HTML += "    <li>"
      
      # 1. Nicen authors:
      if "author" in Article: AllAuthors = Article["author"]
      AllAuthors = self.nicen(AllAuthors)
      Authors = AllAuthors.split(" and")
      
      First = True
      for A in Authors:
        SplitAuthor = A.split(",")

        FirstNames = ""
        LastName = ""
        if len(SplitAuthor) >= 1:
          LastName = SplitAuthor[0].strip()
        if len(SplitAuthor) > 1:
          FirstNames = SplitAuthor[1].strip()
        
        if First == False:
          HTML += ", ";
        else:
          First = False
          
        AuthorName = ""
        if FirstNames != "":
          AuthorName += FirstNames + " ";
        if LastName != "":
          AuthorName += LastName;
          
        FoundName = False
        for Name in self.mHighlightNames:
          #print("Testing: " + Name + " vs " + AuthorName)
          if Name == AuthorName:
            #print("Found: " + Name)
            FoundName = True
            break
          
        if FoundName == False:
          HTML += AuthorName
        else:
          HTML += "<b>" + AuthorName + "</b>"
      
      # 2. Title
      Title = self.nicen(Title)
      HTML += ", <i>\"" + Title + "\"</i>"
      
      # 3. Journal
      Journal = ""
      if "journal" in Article: Journal = Article["journal"]
      Journal = self.nicenJournal(Journal)
      
      if Journal == "":
        if "booktitle" in Article: Journal = Article["booktitle"]
        if Journal != "":
          Journal = self.nicenJournal(Journal)
          Series = ""
          if "series" in Article: Series = Article["series"]
          if Series != "":
            Series = self.nicenJournal(Series)
            HTML += ", " + Series + ": " + Journal
          else:
            HTML += ", " + Journal

      else:
        HTML += ", " + Journal
        if "volume" in Article: Volume = Article["volume"]
        if Volume != "":
          HTML += " <b>" + Volume + "</b>"
          if "pages" in Article: Pages = Article["pages"]
          if Pages != "":
            HTML += ": " + Pages

      if "year" in Article: Year = Article["year"]
      if "month" in Article: Month = Article["month"]
      Month = self.nicenMonth(Month)
      
      if Month != "" and Year != "":
        HTML += ", " + Month + "/" + Year
      elif Year != "":
        HTML += ", " + Year
      
      HTML += "</li>\n"
    HTML += "  </ul>\n"
    
    return HTML


  def nicen(self, Text):
    Text = Text.replace("{\\\"o}", "oe")
    Text = Text.replace("{\\\"u}", "ue")
    Text = Text.replace("{\\\"a}", "ae")
    Text = Text.replace("{\\'c}", "c")
    Text = Text.replace("{\\`e}", "e")
    Text = Text.replace("{\\'e}", "e")
    Text = Text.replace("{$\\alpha$}", "alpha")
    Text = Text.replace("{$\\beta$}", "beta")
    Text = Text.replace("{$\\gamma$}", "gamma")
    Text = Text.replace("{$^{44}$}", "44-")

    for s in "[]{}":
      Text = Text.replace(s, "")
    for s in "~\n":
      Text = Text.replace(s, " ")
    
    return Text

  
  def nicenJournal(self, Text):
    print("Journal: " + Text)
    if Text == "\\apj":
      return "The Astrophysical Journal"
    if Text == "\\nat":
      return "Nature"
    if Text == "\\nar":
      return "New Astronomy Reviews"
    if Text == "\\procspie":
      return "Proceedings of SPIE"
    return Text

  
  def nicenMonth(self, Text):
    if Text == "jan":
      return "1"
    if Text == "feb":
      return "2"
    if Text == "mar":
      return "3"
    if Text == "apr":
      return "4"
    if Text == "mai":
      return "5"
    if Text == "jun":
      return "6"
    if Text == "jul":
      return "7"
    if Text == "aug":
      return "8"
    if Text == "sep":
      return "9"
    if Text == "oct":
      return "10"
    if Text == "nov":
      return "11"
    if Text == "dec":
      return "12"
    
    return ""


# -----------------------------------------------------------------------------------
