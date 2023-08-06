"""TODO doc"""

import sys 

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import RDF, FOAF, XSD, SDO
from rdflib.store import Store, VALID_STORE

class SpatialImpl(object):

    def __init__(self):
        object.__init__(self)
        self.name = None
        self.address = None
        self.geometry = None
        self.location = None
        self.latitude = None
        self.longitude = None
        self.max_latitude = None
        self.max_longitude = None
        self.min_latitude = None
        self.min_longitude = None
        self.reference_system = None
        self.unit_latitude = None
        self.unit_longitude = None
