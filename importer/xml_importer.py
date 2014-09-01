import shutil
import json
import os
import sys, re, optparse
import xml.etree.ElementTree as ET

parser = optparse.OptionParser()
parser.set_defaults(input_path=None,project_title=None)
parser.add_option('--input-xml', action='store', dest='input_path', help='Path to your BibTeX XML export (Required)')
parser.add_option('--project-title', action='store', dest='project_title', help='Your project\'s title (Required)')
(options, args) = parser.parse_args()

# Making sure all mandatory options appeared.
mandatories = ['input_path', 'project_title']
for m in mandatories:
    if not options.__dict__[m]:
        print "mandatory option is missing\n"
        parser.print_help()
        exit(-1)


output_directory = "output"
if os.path.exists(output_directory):
  shutil.rmtree(output_directory)
shutil.copytree("html", output_directory)
os.makedirs(output_directory + "/pdf")

namespaces = {'bibtex': 'http://bibtexml.sf.net/'}
tree = ET.parse(options.input_path)

entries = []
copy_entries = ""

class Entry():
  pass

#for node_xml in entries:
for node in tree.findall('./bibtex:entry/bibtex:newspaperarticle', namespaces=namespaces):
  keys = list(node)
  author_node = node.find('bibtex:author', namespaces=namespaces)
  title_node = node.find('bibtex:title', namespaces=namespaces)
  journal_node = node.find('bibtex:journal', namespaces=namespaces)
  year_node = node.find('bibtex:year', namespaces=namespaces)
  abstract_node = node.find('bibtex:abstract', namespaces=namespaces)
  keywords_node = node.find('bibtex:keywords', namespaces=namespaces)
  comment_node = node.find('bibtex:comment', namespaces=namespaces)
  file_node = node.find('bibtex:nstandard', namespaces=namespaces)

  entry = Entry()
  entry.id = len(entries) + 1
  entry.author = "" if author_node == None else author_node.text
  entry.title = "" if title_node == None else title_node.text
  entry.journal = "" if journal_node == None else journal_node.text
  entry.year = "" if year_node == None else year_node.text
  entry.abstract = "" if abstract_node == None else abstract_node.text
  entry.keywords = "" if keywords_node == None else keywords_node.text
  entry.comment = "" if comment_node == None else comment_node.text
  entry.file = "" if file_node == None else file_node.text

  # remove the path from the file name
  head, tail = os.path.split(entry.file)
  entry.file = tail

  # remove the redundant keywords
  # TODO: add as config option
  keywords = entry.keywords.split(",")
  while "Mineral King" in keywords: keywords.remove("Mineral King")
  entry.keywords = ", ".join(keywords)

  entries.append(entry)

  if(entry.file != ""):
    copy_entries += "copy \"%s\" %%output%%\n" % entry.file
    if os.path.exists(entry.file):
      shutil.copy(entry.file, output_directory + "/pdf")


with open("output/article-json.js", "w") as output:
  output.write("project_title = '"+ options.project_title +"';")
  # TODO: add as command line option
  output.write("pdf_root = 'pdf';")
  output.write("entries = ")
  output.write(json.dumps(entries, default=lambda o: o.__dict__))
  output.write(";")


with open("output/article-copy.bat", "w") as output:
  output.write("set output=\""+ os.path.abspath(output_directory) +"/pdf\"\n")
  output.write("mkdir %output%\n")
  output.write(copy_entries)

print "\nYour package is at: "+ os.path.abspath(output_directory) + "\n"
