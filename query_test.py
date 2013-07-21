from query import *
import timeit


index = None
bindex = None

def build1():
    global index
    index = buildindex(layer, 'postcode')
    
def build2():
    global bindex
    bindex = buildBIndex(layer, 'postcode')
    
qstring = "postcode = 6164"
qstring2 = "subdivided = 'Y'"
   
def withindex():
    layer = iface.activeLayer()
    q = query(layer).where(qstring).top(10000).with_index(index)
    results = q().next()
        
def withbindex():
    layer = iface.activeLayer()
    q = query(layer).where(qstring).top(10000).with_index(bindex)
    results = q().next()
    
def without():
    def checkassessment(feature):
        return int(feature['assessment']) <> 4315968
    
    layer = iface.activeLayer()
    q = (query(layer).where(qstring)
                    .where(qstring2)
                    .where(checkassessment)
                    .top(100))
    results = q()
    for f in results:
        print f['assessment'], f['postcode'], f['subdivided']
        
def with_select():
    def checkassessment(feature):
        return int(feature['assessment']) <> 4315968
    
    
    layer = iface.activeLayer()
    q = (query(layer).where(qstring)
                    .where(qstring2)
                    .where(checkassessment)
                    .top(10)
                    .select('assessment', 
                            'address', 
                            'lot',
                            geom = lambda f: f.geometry(),
                            mylot = lambda f: int(f['house_numb']) * 100)
        )
    results = q()
    for f in results:
        print f
        
def with_select_mapview():
    def checkassessment(feature):
        return int(feature['assessment']) <> 4315968
    
    
    layer = iface.activeLayer()
    q = (query(layer).restict_to(Query.MapView())
                    .top(10)
                    .select('assessment', 
                            'address', 
                            'lot',
                            geom = lambda f: f.geometry(),
                            mylot = lambda f: int(f['house_numb']) * 100)
        )
    results = q()
    for f in results:
        print f

    
#print "Dict Index Build"
#print timeit.timeit(build1, number=1), '(1 run)'
#print "BPlusTree Index Build"
#print timeit.timeit(build2, number=1), '(1 run)'
#
#print "With dict index:"
#print timeit.timeit(withindex, number=1), '(1 run)'
#print timeit.timeit(withindex, number=4), '(4 runs)'
#print timeit.timeit(withindex, number=10), '(10 runs)'
#print "With BPlusTree index:"
#print timeit.timeit(withbindex, number=1), '(1 run)'
#print timeit.timeit(withbindex, number=4), '(4 runs)'
#print timeit.timeit(withbindex, number=10), '(10 runs)'
print "No Index:"
print timeit.timeit(without, number=1), '(1 run)'
print timeit.timeit(with_select, number=1), '(1 run)'
print timeit.timeit(with_select_mapview, number=1), '(1 run)'
#print timeit.timeit(without, number=4), '(4 runs)'
#print timeit.timeit(without, number=10), '(10 runs)'
