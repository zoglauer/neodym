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
import sys
import re

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
    self.mReplacements = {}
    

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
  
    self.addDefaultReplacements()
    if "PapersReplace" in Article.mDictionary:
      Text = Article.mDictionary["PapersReplace"]
      
      # Extract the brackets
      Text = re.findall('\(([^)]+)', Text)

      for T in Text:
        
        # Extract the strings
        S = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', T)
        
        if len(S) != 2:
          print("ERROR: Not exactly two items in replacmenet text: " + str(len(S)))
          continue

        # Remove the first and last quote and add it to the replacement texts
        self.mReplacements[S[0][1:-1]] = S[1][1:-1]
        
      print(self.mReplacements)
        
  
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


  def addDefaultReplacements(self):
    self.mReplacements["{\\\"o}"] = "oe"
    self.mReplacements["{\\\"u}"] = "oe"
    self.mReplacements["{\\\"a}"] = "ae"
    self.mReplacements["{\\\'c}"] = "c"
    self.mReplacements["{\\\'e}"] = "e"
    self.mReplacements["{\\`e}"] = "e"
    self.mReplacements["{\\v c}"] = "c"
    self.mReplacements["\\#"] = "#"
    self.mReplacements["``"] = "\""
    self.mReplacements["\'\'"] = "\""
    self.mReplacements["{$\\alpha$}"] = "alpha"
    self.mReplacements["{$\\beta$}"] = "beta"
    self.mReplacements["{$\gamma$}"] = "gamma"


  def nicen(self, Text):
        
    for k, v in self.mReplacements.items():
      if k in Text:
        Text = Text.replace(k, v)

    for s in "[]{}":
      Text = Text.replace(s, "")
    for s in "~\n":
      Text = Text.replace(s, " ")
    
    return Text

  
  def nicenJournal(self, Text):
    print("Journal: " + Text)
    
    # Replace common journal short cuts
    if Text == "\\apj":
      Text = "The Astrophysical Journal"
    if Text == "\\nat":
      Text = "Nature"
    if Text == "\\nar":
      Text = "New Astronomy Reviews"
    if Text == "\\procspie":
      Text = "Proceedings of SPIE"
    
    # Sometimes the journal contains a link: remove everything between two $\\gt$
    Text = re.sub('\$\\\\gt\$.*gt\$', '', Text)
    
    # Do a final normal nicen
    Text = self.nicen(Text)
    
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
