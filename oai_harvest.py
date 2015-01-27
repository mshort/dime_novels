from sickle import Sickle
from lxml import etree, objectify

series = input('Enter series name keywords: ')

sickle = Sickle("http://localhost/oai-request.do")

records = sickle.ListRecords(**{'metadataPrefix': 'marc21', 'set':'bib', 'from':'2014-01-01T00:00:00Z', 'ignore_deleted':True})

for record in records:

    root = record.xml

    for elem in root.getiterator():
        if not hasattr(elem.tag, 'find'): continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

    objectify.deannotate(root, cleanup_namespaces=True)

    id = root.xpath("metadata/record/controlfield[@tag='001']/text()")[0]
    
    print 'Processing %s' % id

    if root.xpath("metadata/record/datafield[@tag='490']/subfield[@code='a']/text()[contains(.,'%s')]" % series):

	print etree.tostring(root.find('metadata/record'), pretty_print=True)
	f = open ('G:/carter/%s.xml' % id, 'w')
        f.write(etree.tostring(root.find('metadata/record'), pretty_print=True))
        f.close()
