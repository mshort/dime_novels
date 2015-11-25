import sys, solr, csv, os

HOST = 'xxx'
fedoraUser = 'xxx'
fedoraPass = 'xxx'


def main(argv):

    s = solr.SolrConnection('%s/solr' % HOST)

    with open('C://Users/a1691506/Desktop/ocr_metadata.csv', 'w') as csvfile:

        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)

        path = "C://Users/a1691506/Desktop/dime_ocr_raw"

        for root, dirs, files in os.walk(path):
            for file in files:

                pid = file.split('.')[0].replace('_',':')
                print pid

                response = s.query('PID:"%s"' % pid)

                for hit in response.results:
                    mods_title_full_ms = hit['mods_title_full_ms'][0]
                    if 'mods_dateIssued_ms' in hit:
                        mods_dateIssued_ms = hit['mods_dateIssued_ms'][0]
                    else:
                        mods_dateIssued_ms = hit['mods_copyrightDate_ms'][0]
                    if 'mods_name_author_ms' in hit:
                        mods_name_author_ms = hit['mods_name_author_ms'][0]
                    else:
                        mods_name_author_ms = ''
                    if 'mods_name_publisher_ms' in hit:
                        mods_name_publisher_ms = hit['mods_name_publisher_ms'][0]
                    else:
                        mods_name_publisher_ms = ''
                    if 'mods_publisher_ms' in hit:
                        mods_publisher_ms = hit['mods_publisher_ms'][0]
                    else:
                        mods_publisher_ms = ''
                    if 'mods_identifier_oclc_ms' in hit:
                        mods_identifier_oclc_ms = hit['mods_identifier_oclc_ms'][0]
                    else:
                        mods_identifier_oclc_ms = ''
                    if 'mods_genre_lcsh_ms' in hit:
                        mods_genre_lcsh_ms = ''
                        for genre in hit['mods_genre_lcsh_ms'][:-1]:
                            mods_genre_lcsh_ms+=genre+"||"
                        mods_genre_lcsh_ms+=hit['mods_genre_lcsh_ms'][-1]
                    else:
                        mods_genre_lcsh_ms = ''
                    if 'mods_subject_precoordinated_lcsh_ms' in hit:
                        mods_subject_precoordinated_lcsh_ms = ''
                        for subject in hit['mods_subject_precoordinated_lcsh_ms'][:-1]:
                            mods_subject_precoordinated_lcsh_ms+=subject+"||"
                        mods_subject_precoordinated_lcsh_ms+=hit['mods_subject_precoordinated_lcsh_ms'][-1]
                    else:
                        mods_subject_precoordinated_lcsh_ms = ''
                    mods_series_title_preferred_ms = hit['mods_series_title_preferred_ms'][0]
                    mods_series_number_ms = hit['mods_series_number_ms'][0]
                    
                    

                    csvwriter.writerow([pid, mods_title_full_ms.encode('utf-8'), mods_dateIssued_ms, mods_name_author_ms,
                                        mods_publisher_ms, mods_name_publisher_ms, mods_identifier_oclc_ms, mods_genre_lcsh_ms,
                                        mods_subject_precoordinated_lcsh_ms.encode('utf-8'), mods_series_title_preferred_ms,
                                        mods_series_number_ms]) 
        
if __name__ == '__main__':
    sys.exit(main(sys.argv))
