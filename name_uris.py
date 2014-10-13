import urllib, requests, re, json, csv
#from BeautifulSoup import BeautifulSoup
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

def getNames():

    names = {}

    #Read names from text files

    with open ('G:/scripts/voyager_names.txt', 'r') as text:
        count = 1
        for line in text:
            name = line.rstrip('\n')
            l = []
            l.append(name)
            names[count]=l
            count += 1

    # Scrape names from dimenovels.org    
     
#    soup = BeautifulSoup(urllib.urlopen('http://dimenovels.org/People'))

#    for a in soup.findAll('a'):
#	if a.has_key('href'):
#		if re.match(r'\/([A-Z])\w+\/[0-9]+', a['href'], re.UNICODE):
#			href = a['href']
#			name = a.contents[0].lstrip().rstrip().encode('utf-8')
#			l = []
#			l.append(name)
#			names[href] = l

    return names

def getURIs():

    names = getNames()

    for key, value in names.iteritems():

        # Escape special characters in name label for URL
        
        name = urllib.quote(value[0])
        print name
        
        # Use name to get LC, VIAF, and WKP URIs
        
        try:

            # Get LCNAF using Linked Data Service label redirect
                   
            response = requests.get('http://id.loc.gov/authorities/label/%s' % name)
            link = response.url
            pattern = re.compile(r'(.+)\.html$')
            lcnaf = pattern.findall(link)[0].encode('utf-8')

            names[key].append(lcnaf)
            print "Found LC %s for %s" % (lcnaf, key)

            # Prepare LCNAF for VIAF request
            
            r = re.search('([a-z]+)([0-9]+)$', lcnaf)
            lcnaf_viaf = r.group(1).split()[0] + ' ' + r.group(2).split()[0]

        # Get VIAF using LCNAF

            try:

                response = requests.get('http://viaf.org/viaf/sourceID/' + urllib.quote('LC| ' + lcnaf_viaf))
                viaf = response.url.encode('utf-8')
                
                names[key].append(viaf)
                print "Found VIAF %s for %s" % (viaf, key)

                # Get WKP from VIAF JSON
                # JSON seems to be easier and more reliable than HTML or cluster XML
                j = viaf + 'justlinks.json' 
                response = requests.get(j)
                data = json.loads(response.text)

                try:

                    wkp = data['WKP'][0].encode('utf-8')
                    names[key].append(wkp)

                    # Fetch Wikipedia abstract
                    # Similar functions can be written to fetch any data from LCNAF or VIAF

                    try:
                        abstract = getAbstract(wkp)
                        names[key].append(abstract)
                    
                    except:
                        names[key].append('NoAbstract')
                                
                except:
                    print "No WKP found for %s" % key
                    names[key].append('NoWKP')
                    names[key].append('NoAbstract')

            except:
                print "No VIAF found for %s" % key
                names[key].append('NoVIAF')
                names[key].append('NoWKP')
                names[key].append('NoAbstract')
                        
        except:
            print "No LC found for %s" % key
            names[key].append('NoLC')
            names[key].append('NoVIAF')
            names[key].append('NoWKP')
            names[key].append('NoAbstract')

    return names

def getAbstract(wkp):

    wkp urllib.quote(wkp)

    url = 'http://dbpedia.org/data/%s.ntriples' % wkp
    
    g = Graph()
    g.parse(url, format='nt')

    query = g.query(
        """SELECT ?abstract
            WHERE {
                <http://dbpedia.org/resource/%s> <http://dbpedia.org/ontology/abstract> ?abstract .
                FILTER(langMatches(lang(?abstract), "EN"))
            }""" % wkp)

    abstract = ''.join(query.result[0]).encode('utf-8')

    return abstract


names = getURIs()

with open('G:/scripts/dime_names.csv', 'wb') as f:
	writer = csv.writer(f)
	for key, value in names.items():
		writer.writerow([key] + value)
