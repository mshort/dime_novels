import urllib2, string
from lxml import etree
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words
from nltk.stem.snowball import SnowballStemmer


HOSTURL = 'xxx'
fedoraUser = 'xxx'
fedoraPass = 'xxx'

# Create authentication handler for RI Search

passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
riSearch = "http://%s:8080/fedora/risearch" % HOSTURL
passwordManager.add_password(None, riSearch, fedoraUser, fedoraPass)
handler = urllib2.HTTPBasicAuthHandler(passwordManager)
riOpener = urllib2.build_opener(handler)

# Create authentication handler for Fedora Admin

passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
fedoraAdmin = "http://%s:8080/fedora" % HOSTURL
passwordManager.add_password(None, fedoraAdmin, fedoraUser, fedoraPass)
handler = urllib2.HTTPBasicAuthHandler(passwordManager)
fedoraOpener = urllib2.build_opener(handler)

def getBooksFromGenre(genre):

    # Query for genre pids
    
    queryString = "select $object from <#ri> where $object <dc:type> 'Adventure stories' and $object <fedora-rels-ext:isMemberOfCollection> <info:fedora/dimenovels:collection> minus $object <dc:type> 'Detective and mystery stories' minus $object <dc:type> 'Sea stories' minus $object <dc:type> 'Love stories' minus $object <dc:type> 'Western stories' minus $object <dc:type> 'Historical fiction'"
    
    try:
        url = riOpener.open('%s?type=tuples&flush=TRUE&format=Sparql&lang=itql&stream=on&query=%s' % (riSearch, urllib2.quote(queryString)))
    except:
        pass
    
    # Create the xml parser to retrieve the results
    parser = etree.XMLParser(remove_blank_text=True)
    xmlFile = etree.parse(url, parser)
    xmlFileRoot = xmlFile.getroot()

    # Create array for pids
    results = []
    pids = []
    ns = { 'results' : 'http://www.w3.org/2001/sw/DataAccess/rf1/result' }
    xmlPids = xmlFileRoot.xpath('/results:sparql/results:results/results:result/results:object', namespaces=ns)
    pids = [p.attrib['uri'] for p in xmlPids]
    return pids

def getPagesFromBook(book):

    # Format book pid for RI query
    if not (book.startswith('<') or book.endswith('>')):
        book = '<info:fedora/%s>' % book

    # Query for page pids
    
    queryString = 'select $object from <#ri> where $object <fedora-rels-ext:isMemberOf> %s' % book

    try:
        url = riOpener.open('%s?type=tuples&flush=TRUE&format=Sparql&lang=itql&stream=on&query=%s' % (riSearch, urllib2.quote(queryString)))
    except:
        pass
    
    # Create the xml parser to retrieve the results
    parser = etree.XMLParser(remove_blank_text=True)
    xmlFile = etree.parse(url, parser)
    xmlFileRoot = xmlFile.getroot()

    # Create array for pids
    results = []
    pids = []
    ns = { 'results' : 'http://www.w3.org/2001/sw/DataAccess/rf1/result' }
    xmlPids = xmlFileRoot.xpath('/results:sparql/results:results/results:result/results:object', namespaces=ns)
    pids = [p.attrib['uri'] for p in xmlPids]
    return pids

def getTextFromPages(genre):

    stopWords = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    noise = stopWords.union(punctuation)
    wordCorpus = words.words('en')
    stemmer = SnowballStemmer('english')

    # Retreive books from genre
    books = getBooksFromGenre(genre)

    for book in books:


        strippedPid = book.replace('info:fedora/', '')

        file = open ("%s.txt" % strippedPid.replace(':','_'), "w")

        #Retreive pages from book
        
        pages = getPagesFromBook(strippedPid)

        # Loop through pages and retrieve OCR, then write to file
    
        for page in pages:
        
            strippedPid = page.replace('info:fedora/', '')

            #Open OCR plain text

            try:
                ocr = fedoraOpener.open('http://%s:8080/fedora/objects/%s/datastreams/OCR/content' % (HOSTURL, strippedPid))
            

            #Decode plain text from utf-8 and convert all words to lower-case
            
                text = ocr.read().decode('utf-8').lower()

            #Tokenize words
            
                tokens = word_tokenize(text)

            #Remove stopwords and punctuation
            
                tokens = [word for word in tokens if not word in noise]

            #Remove words not in the word corpus
            
                tokens = [word for word in tokens if word in wordCorpus]

                stemmed = []
                
                for word in tokens:

                    if len(word) > 3:
                
                        #Stem word

                        stem = stemmer.stem(word)
                        stemmed.append(stem)                        

                for word in stemmed:
                    
                    if word is not stemmed[-1]:
                        file.write('%s ' % word)
                    else:
                        file.write('%s' % word)
            except:
                pass

        file.close()

getTextFromPages('Adventure stories')
