# Neodym - a static website creator

## Overview




## Installation & Setup

### Download

Start with creating a directory where neodym and your raw websites will reside and switch into it, e.g.

```
mkdir MyWebpage
cd MyWebpage
```

There, download the the latest version of neodym from github.com

```
git clone https://github.com/zoglauer/neodym.git neodym
```

Now create two more directories, content & templates

```
mkdir content
mkdir templates
```

In content you place all your html and associates files (e.g. images, pdfs, etc.).
Into template you copy some of the template files which determine the layout of your website, start with neodym.js, neodym-fill.css and nedym-mobile.css from the template directory in the neodym directory.

### Creating the python environment

Neodym is a python program which requires the following addition python libraries (besides all the default stuff)

* bs (BeautifulSoup)
* bibtexparser

While you are of course free to use whatever way you want to install them, here is the way I would do it:


```
python3 -m venv python-env
. python-env/bin/activate
pip3 install -r Requirements.txt
```

### Creating a configuration file

A configuration file looks like this:

```
Title:             MEGAlib
SubTitle:          The Medium-Energy Gamma-ray Astronomy library
Logo:              img/Icon.png
Footer:            (C) by Andreas Zoglauer &ndash; All rights reserved
ContentDirectory:  content
TemplateDirectory: neodym/templates

TargetDirectory:   public_html
TargetPermissions: a+rX
```

### Creating the webpages

First, make sure you are in your python environment (assuming use setup python the way I suggested). You will see that you command prompt is preceeded by something like "(python-env)",

The just run neodym:

```
python3 neodym/neodym.py
```

# Implementation notes

## The pages

### ZReader

* Reads the file and stores t
* 




