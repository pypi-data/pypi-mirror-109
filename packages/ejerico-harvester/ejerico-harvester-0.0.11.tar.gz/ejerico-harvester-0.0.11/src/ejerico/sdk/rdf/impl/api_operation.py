"""TODO doc"""

import sys 

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import RDF, FOAF, XSD, SDO
from rdflib.store import Store, VALID_STORE

class ApiOperationImpl(object):

    def __init__(self):
        object.__init__(self)
        self.default_value = None
        self.label = None
        self.max_value = None
        self.method = None
        self.min_value = None
        self.param_value = None
        self.property = None
        self.required = None
        self.range = None
        self.returns = None
        self.template = None
        self.variable = None
        self.value_pattern = None