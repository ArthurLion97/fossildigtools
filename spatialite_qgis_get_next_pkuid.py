l = iface.activeLayer()
dp = l.dataProvider()
ds = QgsDataSourceURI(dp.dataSourceUri())

from pyspatialite import dbapi2 as db
conn = db.connect(ds.database())
cur = conn.cursor()

sql = 'SELECT "seq" FROM "sqlite_sequence" WHERE name = "{0}"'.format(ds.table())
rs = cur.execute(sql)
pkuid = list(rs)[0][0]
print "pkuid: {0}".format(pkuid)

eb = l.editBuffer()
addedf = len(l.editBuffer().addedFeatures()) if l.isEditable() else 0
print "addedf: {0}".format(addedf)

print "pkuid + addedf + 1: {0}".format((pkuid + addedf + 1))