#Iterative parsing through OSM to find uniques tags




# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import pprint
import xml.etree.cElementTree as ET
from collections import defaultdict

def count_tags(filename):
    tags = defaultdict(int)
    for event, element in ET.iterparse(filename):
        tags[element.tag] += 1
    return tags



def test():
    tags = count_tags('sample1.osm')
    pprint.pprint(tags)


if __name__ == "__main__":
    test()


#Checking K values in tags and searching for potential problems

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint


"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.
We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""
import re
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#matching the keys with regex patterns
def key_type(element, keys):
    if element.tag == "tag":
        print element.attrib['k']
        if lower.match(element.attrib['k']) != None:
            keys['lower'] += 1
        elif problemchars.match(element.attrib['k']) != None:
            keys['problemchars'] += 1
        elif lower_colon.match(element.attrib['k']) != None:
            keys['lower_colon'] += 1
        else:
            keys['other'] += 1

    return keys

#Adding the keys to the dictionary we made in python
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('sample1.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    test()


#Exploring unique contributors

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return

#Parsing through the File and adding unique users to the Python set called 'users'
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'user' in element.attrib:
            users.update([element.attrib['user']])

    return users


def test():

    users = process_map('sample1.osm')
    pprint.pprint(users)



if __name__ == "__main__":
    test()

#Changing unexpected street names

from collections import defaultdict
import re
import pprint

OSMFILE = "sample1.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Ridge","Galleine", "Heights","Airport","Alley","Bayside","Beach","Bowery","Ridgewood",
            "Turnpike","Americas","Broadway","Circle","Camp","Center","Chestnut","Close","Concourse","Course","Cove",
            "Crescent","Douglaston","Driveway","East","Esplanade","Estate","Expressway","Extension","Floor","Floor)","Gardens",
            "Gate","Green","Hamilton","Hempsead","Highway","Hill","Island","John","Knolls","Loop","Malba","Mall","Mews","NY","North",
            "Oval","Plaza","Park","Path","Promenade","Point","Reservation","Roadbed","Rockaways","Row","Run","Slip","South",
            "Southwest","Terrace","Throughway","Village","Way","Walk","West","Yards","1","10","109","17","207","21G","22","25A",
            "2A","2R","3","35","36","426","46","A","B","C","D","E","F","H","I","J","K","L","M","N","O","P","R","S","T","U","V",
            "W","X","Y","Z"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Ave.": "Avenue",
           "Avenue,#392": "Avenue",
           "Rd.": "Road",
           "AVENUE": "Avenue",
           "Blvd": "Boulevard",
           "Cir": "Circle",
           "CIRCLE": "Circle",
           "Concrs": "Concourse",
           "Cres": "Crescent",
           "Ct": "Court",
           "Ctr": "Center",
           "Cv": "Cove",
           "DRIVE": "Drive",
           "Grn": "Green",
           "Hl": "Hill",
           "Knls": "Knolls",
           "LANE": "Lane",
           "Ln": "Lane",
           "PLAZA": "Plaza",
           "Pkwy": "Parkway",
           "Pl": "Plaza",
           "Plz": "Plaza",
           "Prom": "Promenade",
           "Pt": "Point",
           "ROAD": "Road",
           "Rd": "Road",
           "Rdg": "Ridge",
           "STREET": "Street",
           "Ter": "Terrace",
           "Thruway": "Throughway",
           "Tirnpike": "Turnpike",
           "Tpke": "Turnpike",
           "WAY":"Way",
           "avenue": "Avenue",
           "lane": "Lane",
           "street": "Street"
           }

#Grouping the street types which follow the regex pattern and if not found in expected list, add to the defaultdict
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#Check to return the format of street in the form 'addr:street' for the key 'k'
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#Main function which is called first to parse the OSM XML file and extract the "Street" from either 'node' or 'way' element
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


st_types = audit(OSMFILE)
assert len(st_types) == 3
pprint.pprint(dict(st_types))



def update_name(name, mapping):
    for search_error in mapping:
        if search_error in name:
            name = re.sub(r'\b' + search_error + r'\b\.?', mapping[search_error], name)



    #m = street_type_re.search(name)
    #if m:
        #street_type = m.group()
        #if street_type not in expected:
            #name = re.sub(street_type_re, mapping[street_type], name)



    #target = None
    #for key in mapping.keys():
        #if key in name:
            #target = key

    #name = name.replace(target, mapping[target])

    return name



def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            #if name == "Utica avenue":
                #assert better_name == "Utica Avenue"
            #if name == "Jericho Tpke":
                #assert better_name == "Jericho Turnpike"


#if __name__ == '__main__':
test()

st_types = audit(OSMFILE)

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name

# Audit Postal Code ######################################################

def audit_postal_code(error_codes, postal_codes, this_postal_code):
    # Append incorrect zip codes to list
    if this_postal_code.isdigit() == False:
        error_codes.append(this_postal_code)
    elif len(this_postal_code) != 5:
        error_codes.append(this_postal_code)
    else:
        postal_codes.update([this_postal_code])

def is_postal_code(elem):
    # Identify element tag as postal code
    return (elem.attrib['k'] == "addr:postcode")

def audit_post(osmfile):
    # Parse osm file for incorrect postal codes
    osm_file = open(osmfile, "r")
    error_codes = []
    postal_codes = set([])
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(error_codes, postal_codes, tag.attrib["v"])
    return error_codes, postal_codes

bad_list, good_list = audit_post(OSMFILE)

bad_list

mapping = {'NY 11572': '11572',
           'NY 10026': '10026',
           '11201-2483': '11201',
           '10012-3332': '10012',
           '115422': '11542',
           'NY 10001': '10001',
           '08901-1904': '08901',
           '11201;11231':'11201',
           'NY 10533':'10533',
           '08901-1281':'08901',
           '08854-8010':'08854',
           '08901-8524':'08901',
           '08854-8006': '08854',
           '08854-8029': '08854',
           '08901-8531': '08901',
           '08901-2867': '08901',
           '08901-1101': '08901',
           '08901-1414': '08901',
           '08854-8020': '08854',
           '08854-8007': '08854',
           '08901-8539': '08901',
           '08854-8008': '08854',
           '08901-8529': '08901',
           '08901-8528': '08901',
           '08901-8554': '08901',
           '08854-8054': '08854',
           '08854-8040': '08854',
           '08901-1411': '08901',
           '08854-8047': '08854',
           '08854-8040': '08854',
           '08901-8521': '08901',
           '08901-1866': '08901',
           '08854-8000': '08854',
           '08901-8505': '08901',
           '08901-8508': '08901',
           '08901-1801': '08901',
           '08901-8500': '08901',
           '08901-8513': '08901',
           '08854-8012': '08854',
           '08901-8557': '08901',
           '08901-1061': '08901',
           '08854-8048': '08854',
           '08901-2885': '08901',
           '08901-8520': '08901',
           'NY 10533': '10533',
           '07054-1396': '07054',
           'NJ 07001': '07001',
           '115422': '11542'
           }

def update_name_postcode(name, mapping):
    for search_error in mapping:
        if search_error in name:
            name = re.sub(r'\b' + search_error + r'\b\.?', mapping[search_error], name)
    return name


for name in bad_list:
    better_name = update_name_postcode(name, mapping)
    print name, "=>", better_name

#Data wrangling and bringing it to correct shape to insert into Mongo DB

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node["created"] = {}
    node["address"] = {}
    node["pos"] = []
    refs = []

    # we only process the node and way tags
    if element.tag == "node" or element.tag == "way":
        if "id" in element.attrib:
            node["id"] = element.attrib["id"]
        node["type"] = element.tag

        if "visible" in element.attrib.keys():
            node["visible"] = element.attrib["visible"]

        # the key-value pairs with attributes in the CREATED list are
        # added under key "created"
        for elem in CREATED:
            if elem in element.attrib:
                node["created"][elem] = element.attrib[elem]

        # attributes for latitude and longitude are added to a "pos" array
        # include latitude value
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        # include longitude value
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))

        for tag in element.iter("tag"):
            if not (problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"] = tag.attrib['v']

                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"] = tag.attrib['v']
                    node["address"]["postcode"] = update_name_postcode(node["address"]["postcode"],mapping)

                # handling the street attribute, update incorrect names using
                # the strategy developed before
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"] = tag.attrib['v']
                    node["address"]["street"] = update_name(node["address"]["street"], mapping)

                if tag.attrib['k'].find("addr") == -1:
                    node[tag.attrib['k']] = tag.attrib['v']

        for nd in element.iter("nd"):
            refs.append(nd.attrib["ref"])

        if node["address"] == {}:
            node.pop("address", None)

        if refs != []:
            node["node_refs"] = refs

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # Process to JSON. Used start, end objects to improve performance
    # Depending upon file size... this may take a few minutes
    #file_out = "{0}.json".format(file_in)
    file_out = "sample4_new.json"
    data = []
    with codecs.open(file_out, "w") as fo:
        context = ET.iterparse(file_in,events=('start','end'))
        context = iter(context)
        event, root = context.next()
        for event, element in context:
            if event == 'end':
                el = shape_element(element)
                if el:
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
            root.clear()
    return data

data = process_map('sample1.osm', True)

#mongo db

#mongoimport --db osm --collection newyorkosm2 --type json --file sample4_new.json
import pprint
from pymongo import MongoClient

#Universities
client = MongoClient('localhost:27017')
db = client.osm

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "university", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)

#Most popular cuisines

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant", "cuisine":{"$exists":1}}},
            {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":10}]

result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)


#Top 10 amenities
pipeline = [{"$match":{"amenity":{"$exists":1}}},
            {"$group":{"_id":"$amenity","count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":10}]


result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)


#Sort cities by count

pipeline = ([{"$match":{"address.city":{"$exists":1}}},
                   {"$group":{"_id":"$address.city", "count":{"$sum":1}}},
                   {"$sort":{"count":-1}}])



result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)

#Top 10 Postcodes
pipeline = [{"$match":{"address.postcode":{"$exists":1}}},
            {"$group":{"_id":"$address.postcode",
                       "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit": 10}]

result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)

#Number of Documents
db.newyorkosm2.find().count()

#Number of Nodes
db.newyorkosm2.find({"type":"node"}).count()

#Number of Ways:

db.newyorkosm2.find({"type":"way"}).count()

#Number of Unique users
print len(db.newyorkosm2.distinct("created.user"))

#Top 10 contributing user

pipeline = [{"$group":{"_id":"$created.user",
                              "count":{"$sum":1}}},
                   {"$sort":{"count":-1}},
                   {"$limit":10}]

result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)


#Proportion of top users contribution

pipeline = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$project": {"proportion": {"$divide" :["$count",db.newyorkosm.find().count()]}}},
            {"$sort": {"proportion": -1}},
            {"$limit": 10}]

result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)

#The Number of Methods Used to Create Data Entry
pipeline = [{"$group":{"_id": "$created_by",
                       "count": {"$sum": 1}}}]
result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)


#Top 10 popular street

pipeline = [{"$match":{"address.street":{"$exists":1}}},
            {"$group":{"_id":"$address.street",
                       "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":10}]

result = db.newyorkosm2.aggregate(pipeline)

for a in result:
    pprint.pprint(a)


result = db.newyorkosm2.find({"address.postcode": {"$regex": "/^[A-Z][a-z]+/"}})

for a in result:
    pprint.pprint(a)

result = db.newyorkosm2.find({"address.postcode": {"$regex": "/^\w+$"}})

for a in result:
    pprint.pprint(a)


result = db.newyorkosm2.find({"address.housenumber": {"$regex":"/[a-zA-Z]/"}})


for a in result:
    pprint.pprint(a)

result = db.newyorkosm2.find({"address.housenumber": {"$regex":"/\s/"}})


for a in result:
    pprint.pprint(a)

