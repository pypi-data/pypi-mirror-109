"""TODO doc"""

import datetime
import inspect
import sys 
import re
import time
import traceback
import logging

from validator_collection import checkers, errors

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import namespace 
from rdflib.namespace import Namespace, ClosedNamespace
from rdflib.store import Store, VALID_STORE

from ejerico.sdk.exceptions import GraphError
from ejerico.sdk.utils import isPrimitive, tokenize_name, parseDatetime, roundTime
from ejerico.sdk.rdf.entity import Entity, EntityMetaclass, EntityMapper, Person

class GraphExtension:

    def __init__(self): pass

    def toTurtle(self):
        self._register_namespaces()
        rep_turtle = self.serialize(format="turtle")
        return rep_turtle.decode("utf-8") if  hasattr(rep_turtle, "decode") else rep_turtle

    def toJSONLD(self): 
        self._register_namespaces()
        rep_jsonld = self.serialize(format="json-ld")
        return rep_jsonld.decode("utf-8") if  hasattr(rep_jsonld, "decode") else rep_jsonld

    def toXML(self):
        self._register_namespaces() 
        rep_xml = self.serialize(format="xml")
        return rep_xml.decode("utf-8") if  hasattr(rep_xml, "decode") else rep_xml
    
    def toN3(self):
        self._register_namespaces() 
        rep_n3 = self.serialize(format="n3")
        return rep_n3.decode("utf-8") if  hasattr(rep_n3, "decode") else rep_n3

    def findByURI(self, uri, kind=None):
        logging.debug("[Graph::findByURI] entering method")

        if not isinstance(uri,str):
            logging.info("[find_URI] uri is not a 'str' instance {}")
            return None

        rst = self.findByURIs([uri])
        rst = rst if rst is not None else []
        if 1 < len(rst):
            logging.info("[Graph::findByURI] warnning -multiple entities are binded to uri {} ({})".format(uri, rst))

        return rst[0] if 0 != len(rst) else None

    def findByURIs(self, uris, kind=None):
        #logging.debug("[Graph::findByURIs] entering method")
        
        if not isinstance(uris,list):
            logging.info("[Graph::findByURIs] uris is not a 'list' instance {}")
            return None

        uri = next((self.findByURIs.cache_URI[str(u)] for u in uris if str(u) in self.findByURIs.cache_URI), None)
        if uri is not None:
            logging.info("[Graph::findByURIs] found in cache: {}".format(uri)) 
            return uri

        rst = None

        if kind is not None:
            logging.debug("[Graph::findByURIs] entering method with param '{}'".format(_get_RDFType(kind)))
        for uri in uris:
            rst = self._findByURIsOneByOne(uri, kind)
            if rst is not None:
                rst = [rst] 
                break
            
        # try:
        #     if kind is None:
        #         query = _SPARQL_QUERY_FIND_ENTITY_BY_URI
        #         query = query.replace("###prefixes###", self.prefixes) 
        #     else:
        #         kind = kind() if isinstance(kind,EntityMetaclass) else kind
        #         if not isinstance(kind,Entity):
        #             logging.info("[Graph::findByURIs] 'kind' parameter must be a Entity class")
        #             raise GraphError("'kind' parameter must be a Entity class")
                
        #         base = _get_RDFType(kind)
        #         query = _SPARQL_QUERY_FIND_ENTITY_BY_URI_KIND
        #         query = query.replace("###prefixes###", self.prefixes)
        #         query = query.replace("###kind###",base)
        #         logging.debug("[Graph::findByURIs] entering method with param '{}'".format(base))
        
        #     query = query.replace("###values###", " ".join(['(<{}>)'.format(URIRef(u)) for u in uris]))
        #     #logging.info("\t Query: -> {}".format(query))
        #     rows = self.query(query, initNs=self.registered_namespaces)
        #     for row in rows:
        #         if rst is None: rst = [] 
        #         rst.append(str(row[0]))
        # except Exception as e:
        #     logging.error("[Graph::findByURIs] error processing sparql ({})".format(e))
        #     logging.error("\t\tQuery: '{}'".format(query))
        #     raise GraphError(e)
        
        if rst is not None and len(rst) != 0:
            for uri in uris: self.findByURIs.cache_URI[str(uri)] = str(rst[0])
        return rst
    findByURIs.cache_URI = {}

    def _findByURIsOneByOne(self, uri, kind=None):
        try:
            rst = None

            if kind is None:
                query = _SPARQL_QUERY_FIND_ENTITY_BY_URI_KIND_ONE_BY_ONE
            else:
                kind = kind() if isinstance(kind,EntityMetaclass) else kind
                if not isinstance(kind,Entity):
                    logging.info("[Graph::findByURIs] 'kind' parameter must be a Entity class")
                    raise GraphError("'kind' parameter must be a Entity class")
                
                base = _get_RDFType(kind)
                query = _SPARQL_QUERY_FIND_ENTITY_BY_URI_KIND_ONE_BY_ONE
                query = query.replace("###kind###",base)
        
            query = query.replace("###value###", '<{}>'.format(URIRef(uri)))
            query = query.replace("###prefixes###", self.prefixes)
    
            rows = self.query(query, initNs=self.registered_namespaces)
            for row in rows:
                if rst is None: rst = [] 
                rst.append(str(row[0]))
        except Exception as e:
            logging.error("[Graph::_findByURIsOneByOne] error processing sparql ({})".format(e))
            logging.error("\t\tQuery: '{}'".format(query))
            logging.error(traceback.format_exc())
            #raise GraphError(e)
            return None
        
        return rst[0] if rst is not None and len(rst) > 0 else None

    def findRelatedURIsByURI(self, uri):
        #logging.debug("[Graph::findRelatedURIsByURI] entering method")
        uris = None
        try:
            my_uri = uri if isinstance(uri, URIRef) else URIRef(uri)
            query = _SPARQL_QUERY_FIND_RELATED_ENTITY_BY_URI.replace("###uri###", my_uri)
            query = query.replace("###prefixes###", self.prefixes)
            data = self.query(query, initNs=self.registered_namespaces)
            for d in data:
                if uris is None: uris = []
                uris.append(d[0])
        except Exception as e:
            logging.error("[Graph::getEntityByURI] error getting entity by uri ({})".format(e))
            raise GraphError(e)
        return uris

    def getEntityByURI(self, uri):
        #logging.debug("[Graph::getEntityByURI] entering method")
        try:
            my_uri = uri if isinstance(uri, URIRef) else URIRef(uri)
            graph = Graph()
            query = _SPARQL_QUERY_GET_ENTITY_BY_URI.replace("###uri###", my_uri)
            data = self.query(query, initNs=self.registered_namespaces)
            for d in data:
                graph.add((my_uri, d[0], d[1]))
            return Entity.load(graph)
        except Exception as e:
            logging.error("[Graph::getEntityByURI] error getting entity by uri ({})".format(e))
            raise GraphError(e)

    def save(self, entity):
        logging.debug("[Graph::save] entering method ")

        if not isinstance(entity,Entity):
            logging.info("[save] parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity'")
            raise GraphError("parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity' (found type:{})".format(type(entity)))

        self.do_before_save(entity)
        
        if self._validate(entity):
            tiplets = entity.toGraph()
            self.__iadd__(tiplets)

    def delete(self, entity):
        if not isinstance(entity,Entity):
            logging.info("[delete] parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity'")
            raise GraphError("parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity' (found type:{})".format(type(entity)))
        
        self._prepare(entity)
        self._fixEntityID(entity)

        tiplets = entity.toGraph()
        self.remove_graph(tiplets)

    def find(self, entity):
        if not isinstance(entity,Entity):
            logging.info("[find] parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity'")
            raise GraphError("parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity' (found type:{})".format(type(entity)))
        
        tiplets = entity.toDict()
        logging.info(tiplets)

    @property
    def prefixes(self):
        rst = []
        for k,v in sorted(self.registered_namespaces.items(), key=lambda item: item[1]):
            #rst.append("@prefix {}: <{}>.".format(k,v))
            rst.append("PREFIX {}: <{}>".format(k,v))
        return "\n".join(rst)

    @property
    def registered_namespaces(self):
        import rdflib as my_rdflib
        self.bind("EJERICO".lower(), my_rdflib.EJERICO)
        self.bind("ADMS".lower(), my_rdflib.ADMS)
        self.bind("BODC".lower(), my_rdflib.BODC)
        self.bind("EJERICO".lower(), my_rdflib.EJERICO)
        self.bind("EPOS".lower(), my_rdflib.EPOS)
        self.bind("HTTP".lower(), my_rdflib.HTTP)
        self.bind("HYDRA".lower(), my_rdflib.HYDRA)
        self.bind("LOCN".lower(), my_rdflib.LOCN)
        self.bind("SOCIB".lower(), my_rdflib.SOCIB)
        self.bind("SPDX".lower(), my_rdflib.SPDX)
        self.bind("VCARD".lower(), my_rdflib.VCARD)
        return {k:str(v) for k,v in self.namespaces()}

    def _register_namespaces(self):
        entity = Entity()
        entity._register_namespaces(self)

    def _prepare(self,entity):
        if hasattr(entity,"prepare"): entity.prepare()

        # if hasattr(entity,"name") and entity.name is not None:
        #     tokenized_name = tokenize_name(entity.name)
        #     if tokenized_name is not None:
        #         uri_for_name = "{}:{}".format(entity._scope, tokenized_name)
        #         entity.alias.append(uri_for_name)

        if entity.alias is None: entity.alias = []
        if not isinstance(entity.alias, list): entity.alias = [entity.alias]
        #self.alias = [entity.buildURI(a) for a in entity.alias if not checkers.is_url(a) and not checkers.is_email(a)]
        for i in range(len(entity.alias)):
            if not checkers.is_url(entity.alias[i]) and not checkers.is_email(entity.alias[i]):
                entity.alias[i] = entity.buildURI(entity.alias[i])

        if isinstance(entity, Person) and entity.name is not None:
            match = re.match(self._prepare.RE_NAME_EMAIL_PATTERN, entity.name)
            if match:
                entity.name = match.group("name")
                entity.alias.append(match.group("email"))
        
        for entity_child in entity.__dict__:
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                    if isinstance(entity.__dict__[entity_child],list):
                        for list_entity in entity.__dict__[entity_child]:
                            if isinstance(list_entity, Entity): self._prepare(list_entity)

                    if isinstance(entity.__dict__[entity_child], Entity): 
                        self._prepare(entity.__dict__[entity_child])

        #fix organizations acting as persons
        #if isinstance(entity,Person): pass
    _prepare.RE_NAME_EMAIL_PATTERN = re.compile("^(?P<name>[áàéèíìóòúùäöü\w\d.-_ ]+){1}([\W])+(<)(?P<email>[\w\d\W]+)+(>)$", re.UNICODE)

    def _fixEntityID(self,entity):   
        
        if not entity.first_born:
            entity.alias.append(entity.id)
            my_ID = self.findByURIs(entity.alias, kind=entity)

            if my_ID is not None:
                entity.alias.remove(entity.id) 
                if entity.id != my_ID: entity.id = my_ID[0] if isinstance(my_ID, list) else my_ID

        for entity_child in entity.__dict__:
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                if isinstance(entity.__dict__[entity_child],list):
                    for list_entity in entity.__dict__[entity_child]:
                        if isinstance(list_entity, Entity):
                            self._fixEntityID(list_entity)

                if isinstance(entity.__dict__[entity_child], Entity): 
                    self._fixEntityID(entity.__dict__[entity_child])
    
    def _delete_on_save(self, entity):
        for entity_child in entity.__dict__: 
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                if isinstance(entity.__dict__[entity_child],list):
                    for list_entity in entity.__dict__[entity_child]:
                        if isinstance(list_entity, Entity):
                            self._delete_on_save(list_entity)
                elif isinstance(entity.__dict__[entity_child], Entity): 
                    self._delete_on_save(entity.__dict__[entity_child])

        if entity.delete_on_save:
            try:
                logging.info("[Graph::_delete_on_save] deleting entities binded to <{}> as subject".format(entity.id))
                query = _SPARQL_DELETE_ENTITY_BY_URI_AS_SUBJECT.replace("###uri###", entity.id)
                query = query.replace("###prefixes###", self.prefixes)
                data = self.update(query, initNs=self.registered_namespaces)

                logging.info("[Graph::_delete_on_save] deleting entities binded to <{}> as object".format(entity.id))
                query = query.replace("###prefixes###", self.prefixes)
                query = _SPARQL_DELETE_ENTITY_BY_URI_AS_OBJECT.replace("###uri###", entity.id)
                query = query.replace("###prefixes###", self.prefixes)
                data = self.update(query, initNs=self.registered_namespaces)
            except Exception as e: pass

    def _setSource(self,entity, source=None):
        if entity.source is None:
            if source is None:
                for alias in entity.alias:
                    if alias.startswith(entity.entity_domain):
                        alias = alias.replace(entity.entity_domain,"")
                        alias = alias.split("/")
                        if 4 == len(alias): 
                            entity.source = alias[2]
                else:
                    entity.alias = "ejerico" if entity.alias is None else entity.alias
            else:
                entity.source = source
                
        for entity_child in entity.__dict__:
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                if isinstance(entity.__dict__[entity_child],list):
                    for list_entity in entity.__dict__[entity_child]:
                        if isinstance(list_entity, Entity):
                            self._setSource(list_entity, source=source)

                if isinstance(entity.__dict__[entity_child], Entity): 
                    self._setSource(entity.__dict__[entity_child], source=source)

    def _entity_timestamp(self,entity): 
        entity.modified = datetime.datetime.now() if entity.modified is None else entity.modified
        entity.modified = entity.modified.replace(hour=0, minute=0, second=0, microsecond=0)

        entity.created = entity.modified if entity.created is None else entity.created
        entity.created = entity.created.replace(hour=0, minute=0, second=0, microsecond=0)

        for entity_child in entity.__dict__:
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                if isinstance(entity.__dict__[entity_child],list):
                    for list_entity in entity.__dict__[entity_child]:
                        if isinstance(list_entity, Entity):
                            self._entity_timestamp(list_entity)

                if isinstance(entity.__dict__[entity_child], Entity): 
                    self._entity_timestamp(entity.__dict__[entity_child])

    def _validate(self, entity):
        is_valid = True
        if hasattr(entity,"validate"): is_valid = entity.validate()
        
        for entity_child in entity.__dict__:
            if re.match(r"^[a-zA-Z]+\W*", entity_child):
                    if isinstance(entity.__dict__[entity_child],list):
                        for list_entity in entity.__dict__[entity_child]:
                            if isinstance(list_entity, Entity): 
                                is_valid = is_valid and self._validate(list_entity)

                    if isinstance(entity.__dict__[entity_child], Entity): 
                        is_valid = is_valid and self._validate(entity.__dict__[entity_child])
        return is_valid

    def do_before_save(self, entity):
        logging.debug("[Graph::do_before_save] entering method ")

        if not isinstance(entity,Entity):
            logging.info("[save] parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity'")
            raise GraphError("parameter entity must be a instance of 'ejerico.sdk.rdf.entity.Entity' (found type:{})".format(type(entity)))

        self._prepare(entity)
        self._fixEntityID(entity)
        self._setSource(entity, entity.source)
        self._entity_timestamp(entity)

        

def _getBaseClass(obj,return_class=False):
        rst = obj.__class__ if return_class else obj.__class__.__name__
        for cls in inspect.getmro(obj.__class__):
            if cls.__name__ == "Entity": break
            rst = cls if return_class else cls.__name__
        return rst

def _get_RDFType(kind):
    mapper = EntityMapper.instance()
    base = mapper.map_class(scope=_getBaseClass(kind))
    base = str(base)

    import rdflib as my_rdflib

    custom_namespaces = [
        ("EJERICO".lower(), str(my_rdflib.EJERICO)),
        ("ADMS".lower(), str(my_rdflib.ADMS)),
        ("SPDX".lower(), str(my_rdflib.SPDX)),
        ("LOCN".lower(), str(my_rdflib.LOCN)),
    ]
    for a in namespace.__dict__:
        if isinstance(namespace.__dict__[a],Namespace) or isinstance(namespace.__dict__[a],ClosedNamespace):
            custom_namespaces.append((a.lower(), str(namespace.__dict__[a])))

    for key,val in custom_namespaces:
        if val in base:
            base = "{}:{}".format(key, base.replace(val,"")) 

    return base

_SPARQL_QUERY_FIND_ENTITY_BY_URI_KIND = """
    ###prefixes###

    SELECT DISTINCT ?s
    WHERE {
        VALUES (?o) { ###values### }
        ?s adms:identifier ?o.
        ?s rdf:type ###kind###.
    }
"""

_SPARQL_QUERY_FIND_ENTITY_BY_URI = """
    ###prefixes###

    SELECT DISTINCT ?s
    WHERE {
        VALUES (?o) { #values# }
        ?s adms:identifier ?o.
    }
"""
_SPARQL_QUERY_FIND_ENTITY_BY_URI_KIND_ONE_BY_ONE = """
    ###prefixes###

    SELECT DISTINCT ?s
    WHERE {
        ?s adms:identifier ###value###.
        ?s rdf:type ###kind###.
    }
"""

_SPARQL_QUERY_FIND_ENTITY_BY_URI_ONE_BY_ONE = """
    ###prefixes###

    SELECT DISTINCT ?s
    WHERE {
        ?s adms:identifier ###value###.
    }
"""
_SPARQL_QUERY_FIND_RELATED_ENTITY_BY_URI = """
    ###prefixes###

    SELECT DISTINCT ?s
    WHERE {
        ?s ?p <###uri###>.
    }
"""

_SPARQL_QUERY_GET_ENTITY_BY_URI = """
    ###prefixes###

    SELECT ?p ?o
    WHERE {
        <###uri###> ?p ?o.
    }
"""

_SPARQL_DELETE_ENTITY_BY_URI_AS_SUBJECT = """
    ###prefixes###

    DELETE
    WHERE {
        <###uri###> ?p ?o.
    }
"""
_SPARQL_DELETE_ENTITY_BY_URI_AS_OBJECT = """
    ###prefixes###

    DELETE
    WHERE {
        ?s ?p <###uri###>.
    }
"""