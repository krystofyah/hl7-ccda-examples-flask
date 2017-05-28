import os, ipdb, re, pandoc

folder = '../C-CDA-Examples'

import git
repo = git.Repo(folder)
VALIDATOR_LOOKUP = {
    "https://sitenv.org/c-cda-validator": "SITE C-CDA Validator"
}

from app.db import db

def get_name(section):
    lines = section.split("\n\n")
    name = lines[0].strip()
    try:
        colon = name.index(':')
        name = name[:colon]
    except:
        pass
    return name


def process_section(doc, name, section):
    #name_criteria = name if name == 'Approval Status' else "#{}".format(name)
    if section.startswith(name): # not clear what this section maps to in the front end
        lines = section.split("\n")
        #   ipdb.set_trace()
        lines = [ l.replace('* ', '') for l in lines if l.startswith("*") ]
        #   get rid of remaining #
        name = name[1:] if name.startswith("#") else name
        # make name safe for mongo
        name = name.replace(".", ' ')

        #   update Permalink field to just be the id, otherwise list of bulleted items
        isStr = name in ['Permalink', 'Comments', 'Custodian', 'Reference to full CDA sample']
        if name == 'Approval Status':
            doc['approval']  = lines[0].split(":")[1].strip()
        if name == 'Validation location':
            link = lines[0][lines[0].index('(')+1 : lines[0].index(')')]
            doc['validator'] = {
                                "link": link,
                                "name": VALIDATOR_LOOKUP[link]
                                }
        doc[name] = lines[0] if isStr else lines


def process_sections(sections):
    doc = {}
    for section in sections:
        if section != '':
            name = get_name(section)
            process_section(doc,name, section)

            #   ipdb.set_trace()
            """
            if section.startswith("Approval Status"):
                lines = section.split("\n")
                lines = [ l for l in lines if l.startswith("*")]
                doc['Approval Status'] = lines
            if section.startswith("#C-CDA 2.1 Example"): # not clear what this section maps to in the front end
                lines = section.split("\n")
                lines = [ l for l in lines if l.startswith("*")]
                doc['C-CDA 2.1 Example'] = lines
            """
    return doc


def process_readme(section_name, example_name, data, example_xml, xml_filename):
    sections = data.split('##')
    doc = process_sections(sections)
    doc['section'] = section_name
    doc['name'] = example_name
    doc['xml'] = example_xml
    doc['xml_filename'] = xml_filename
    if 'Permalink' in doc:
        result = db.examples.replace_one({"Permalink": doc['Permalink']}, doc, upsert=True)
        #   ipdb.set_trace()
    else:
        #   add permalink to readme
        pass
        #   commit change to readme

        #   push change to GitHub repo


#   loop through each section folder
def parse(folder):
    for path,dirs,files in os.walk(folder):
        #   print "path: {} dir: {} "
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            #   section folder
            if filename.lower() == "readme.md" and len(dirs) != 0:
                print os.path.join(path,filename)
                pth = os.path.join(re.sub(folder, '', path), filename)
                pth = pth.lstrip('/')
                with open(os.path.join(path,filename), 'rb') as readme:
                    description = readme.read()
                    description = description.replace("##", "")
                    section_name = path.split(os.path.sep)[-1]
                    #   ipdb.set_trace()
                    if section_name != 'C-CDA-Examples':
                        db.sections.replace_one(
                            {"name": section_name},
                            {
                                "name": section_name,
                                "description": description
                            },
                            upsert=True
                        )

            #   actual example folder
            if filename.lower() == "readme.md" and dirs == []:
                #   get the xml file for the example
                xml_filename =  [ _file for _file in files if _file.lower() != "readme.md" ][0]
                print os.path.join(path,filename)
                pth = os.path.join(re.sub(folder, '', path), filename)
                pth = pth.lstrip('/')
                example_name = path.split(os.path.sep)[-1]
                example_xml = ''
                with open(os.path.join(path,xml_filename), 'rU') as xml:
                    example_xml = xml.read()

                with open(os.path.join(path,filename), 'rU') as readme:
                    data = readme.read()
                    process_readme(section_name, example_name, data, example_xml, xml_filename)
