"""TODO doc"""

import sys 

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import RDF, FOAF, XSD, SDO
from rdflib.store import Store, VALID_STORE

class PersonImpl(object):

    def __init__(self):
        object.__init__(self)
        self.address = None
        self.email = None
        self.familyName = None
        self.givenName = None
        self.name = None
        self.nationality = None
        self.phone = None
        self.qualification = None
        self.url = None
        