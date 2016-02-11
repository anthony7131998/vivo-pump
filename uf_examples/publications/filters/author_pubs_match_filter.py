#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pub_columns_filter.py -- add needed columns, remove unused columns
"""

__author__ = "Alex Loiacono and Nicholas Rejack"
__copyright__ = "Copyright 2016 (c) Alex Loiacono and Nicholas Rejack"
__license__ = "New BSD License"
__version__ = "0.01"

from vivopump import read_csv_fp, write_csv_fp, get_parms, vivo_query
import sys
import utils
import time

def get_vivo_academic_articles(parms):
    """
    Query VIVO and return a list of all the academic articles.
    @see uf_examples/publications/filters/pub_match_filter.py
    @see https://wiki.duraspace.org/display/VIVO/VIVO-ISF+1.6+relationship+diagrams%3A+Authorship

    :param: parms: vivo_query params
    :return: dictionary of uri keyed by DOI
    """
    query = """
    SELECT
    ?uri ?doi
    WHERE {
        ?uri a vivo:InformationResource .
        ?uri bibo:doi ?doi .
    }
    """
    results = vivo_query(query, parms)
    bindings = results['results']['bindings']
    doi_list = [b['doi']['value'] for b in bindings]
    uri_list = [b['uri']['value'] for b in bindings]
    return dict(zip(doi_list, uri_list))

date = time.strftime("%Y_%m_%d")

file_name = 'vivo_author_list.csv'
utils.print_err("Using static disambiguation file: {}".format(file_name))

disamb_file = open('data_out/disambiguation_'+date+'.txt', 'w+')

authors_missing_pubs_file = open('data_out/authors_missing_pubs_'+date+'.txt', 'w+')

authors_missing_pubs_dict = {}

# get dictionaries of authors keyed by name parts
vivo_auth_disambig_data = utils.get_vivo_disambiguation_data_from_csv(
    file_name)

parms = get_parms()
data_in = read_csv_fp(sys.stdin)
utils.print_err("{} rows in the input".format(len(data_in)))

data_out = {}
# get dictionary of pub uri keyed by doi
vivo_pubs = get_vivo_academic_articles(parms)

utils.print_err('{} publications found in VIVO'.format(len(vivo_pubs)))
# print >>sys.stderr, vivo_pubs

row_out = 1

disamb_dict = []

for row, data in data_in.items():

    if data['doi'] not in vivo_pubs:
        #data_out[row]['pub_uri'] = ''
        authors_missing_pubs_dict[row] = data
        continue

    data_out[row] = data

    utils.print_err("data is: \n{}".format(data))
    utils.print_err("row_out: {} ||| row: {}".format(row_out,row))

    data_out[row]['pub_uri'] = vivo_pubs[data['doi']]

    if data['uf'] == 'false':
        # Always put in the non-UF author as new
        #row_out += 1
        data_out[row] = data
        data_out[row]['uri'] = ''
        #utils.print_err("UF entry is false {}".format(row_index))
    else:
        author_uris = utils.get_author_disambiguation_data(
            vivo_auth_disambig_data,
            data['last'],
            data['first'],
            data['middle'])

        count = len(author_uris)
        utils.print_err("author_uris: {}".format(author_uris))
        if count == 0:
            # There is no match in the current VIVO ==> add a new UF author
            #row_out += 1
            data_out[row] = data
            data_out[row]['uri'] = ''
        elif count == 1:
            data_out[row]['uri'] = author_uris[0]
        else:
            utils.print_err("Disamb: {}".format(author_uris))
            data_out[row]['uri'] = author_uris[0]
            disamb_dict.append("Paper: {} -- written by {} has uris  : \n{}\n\n".format(data['pub_uri'], data['display_name'], author_uris))
    row_out += 1

utils.print_err('{} rows in the output'.format(len(data_out)))

for line in disamb_dict:
    disamb_file.write(line)

disamb_file.close()

write_csv_fp(authors_missing_pubs_file, authors_missing_pubs_dict)
write_csv_fp(sys.stdout, data_out)