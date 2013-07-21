import sys
import os
import itertools
from qgis.utils import iface
from qgis.core import QgsExpression, QgsFeatureRequest
from btree import BPlusTree
from collections import defaultdict

def buildindex(layer, field):
    d = defaultdict(list)
    for f in layer.getFeatures():
        try:
            d[int(f[field])].append(f)
        except TypeError:
            continue
    return d

def buildBIndex(layer, field):
    bt = BPlusTree(20)
    for f in layer.getFeatures():
        try:
            bt.insert(int(f[field]), f)
        except TypeError:
            continue
    return bt
    
class Select(object):
    def __init__(self, layer, *cols, **namedcols):
        self.layer = layer
        self.cols = cols
        self.namedcols = namedcols
        
    def __call__(self, f):
        result = {}
        # Loop each feature
        # Get each column
        # Insert named columns
        def _getValue(col):
            if hasattr(col, '__call__'):
                value = col(f)
            else:
                value = f[col]
            return value
            
        for col in self.cols:
            result[str(col)] = _getValue(col)
            
        for name, col in self.namedcols.iteritems():
            result[name] = _getValue(col)
        
        print result
        return result
        
class Where(object):
    def __init__(self, layer, filterfunc):
        """
            Object to filter result set by a where expression or function
            
            filterfunc : A QgsExpression string, or Python callable.
        """
        self.filterfunc = filterfunc
        self.layer = layer
        
    def __call__(self, features):
        func = self.filterfunc
        if not hasattr(self.filterfunc, '__call__'):
            exp = QgsExpression(self.filterfunc)
            fields = self.layer.pendingFields()
            exp.prepare(fields)
            func = exp.evaluate
        # Return a generator of features that match the given where check.
        for f in features:
            if func(f):
                yield f

def query(*args, **kwargs):
    return Query(*args, **kwargs)

class Query(object):
    MapView = iface.mapCanvas().extent
    def __init__(self, layer, DEBUG=False):
        self.layer = layer
        self.wheres = []
        self.rect = None
        self.index = None
        self.limit = None
        self.selectstatment = None
        self.DEBUG = DEBUG
        
    def where(self, filterexp ):
        self.wheres.append(Where(self.layer, filterexp))
        return self
        
    def restict_to(self, rect):
        self.rect = rect
        return self
        
    def top(self, limit):
        self.limit = limit
        return self
    
    def with_index(self, index):
        self.index = index
        return self
        
    def select(self, *cols, **namedcols):
        self.selectstatment = Select(self.layer, *cols, **namedcols)
        return self
        
    def __call__(self):
        if self.rect:
            rq = QgsFeatureRequest()
            rq.setFilterRect(self.rect)
            features = self.layer.getFeatures(rq)
        else:
            features = self.layer.getFeatures()
        
        for where in self.wheres:
            if self.DEBUG: "Has filter"
            #TODO Index lookup
#            if self.index:
#                if self.DEBUG: print "Has index"
#                min = 6163
#                max = 6164
#                iters = [iter(self.index[code]) for code in xrange(min, max + 1)]
#                features = itertools.chain(*iters)
            features = where(features)
        
        # TODO Clean up
        if self.limit:
            if self.DEBUG: print "Has Limit"
            for count in xrange(self.limit):
                if self.selectstatment:
                    yield self.selectstatment(features.next())
                else:
                    yield features.next()
        else:
            for f in features:
                if self.selectstatment:
                    yield self.selectstatment(f)
                else:
                    yield f
            

if __name__ == "__main__":
    pass    