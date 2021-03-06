from rdflib import Graph, URIRef
from rdflib.namespace import RDF
import re

class Model:

    def __init__(self):
        self.graph = Graph()
        self.loaded = set()

    def load(self, source, format=None):
        if source not in self.loaded:
            self.loaded.add(source)
            try:
                self.graph.parse(source, format=format)
            except Exception as e:
                print e
                return False
        return True

    def size(self):
        return len(self.graph)

    def pred(self, subj):
        return list(set(self.graph.predicates(subj)))

    def types(self):
        return set(self.graph.objects(predicate=RDF.type))

    def contains_resource(self, ref):
        resources = filter(lambda x: type(x) == URIRef, self.graph.all_nodes())
        return ref in resources

    def get_resource_objects(self, subj, pred):
        return filter(lambda x: type(x) == URIRef, self.graph.objects(subj, pred))

    def get_objects(self, subj, pred):
        return list(self.graph.objects(subj, pred))

    def get_subjects(self, pred, obj):
        return list(self.graph.subjects(pred, obj))

    def get_properties(self, subj):
        properties = {}
        for pred, obj in self.graph.predicate_objects(subj):
            if pred in properties:
                properties[pred].append(obj)
            else:
                properties[pred] = [obj]
        return properties

    def get_reverse_properties(self, obj):
        properties = {}
        for subj, pred in self.graph.subject_predicates(obj):
            if pred in properties:
                properties[pred].append(subj)
            else:
                properties[pred] = [subj]
        return properties

    def norm(self, ref):
        if ref is None:
            return None
        elif isinstance(ref, URIRef):
            return self.graph.namespace_manager.normalizeUri(ref)
        else:
            return unicode(ref)

    def to_uriref(self, string):
        """Expand QName to UriRef based on existing namespaces."""
        if not string:
            return None
        elif re.match('[^:/]*:[^:/]+', string):
            prefix, name = string.split(':')
            try:
                namespace = dict(self.graph.namespaces())[prefix]
                return namespace + name
            except:
                return None
        else:
            return URIRef(string)

    def select(self, query):
        return self.graph.query(query)
