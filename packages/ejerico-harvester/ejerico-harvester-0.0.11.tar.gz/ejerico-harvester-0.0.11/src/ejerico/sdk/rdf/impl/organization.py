"""TODO doc"""

import sys 

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import RDF, FOAF, XSD, SDO
from rdflib.store import Store, VALID_STORE

class OrganizationImpl(object):

    def __init__(self):
        object.__init__(self)
        self.address = None
        self.email = None
        self.lei_code = None
        self.name = None
        self.spatial = None
        self.phone = None
        self.url = None
        self.vcard = None