#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    sv.py: Simple VIVO

    Uses the VIVO Pump to provide data management services for VIVO.  Tabular data is mapped by the pump in and out
    of VIVO.  Simple VIVO can be used from the command line to get data from VIVO into speadsheets (delimited text
    files).  Spreadsheets can be edited using any text editor or spreadsheet program.  The resulting imporved data
    can be used to update VIVO.

    Inputs:  spreadsheet containing updates and additions.  Definition file containing maps to/from columns to
        VIVO objects.  Enumeration tables for translating spreadsheet values to VIVO values and back.  VIVO for
        current state. Config file with parameters describing VIVO and the pump actions.
    Outputs:  spreadsheet with current state.  RDF files (add and sub) to create VIVO state changes.
        stdout with timestamped messages. logger output.

    See CHANGELOG.md for history
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2016 Michael Conlon"
__license__ = "New BSD License"
__version__ = "0.8.7"

#   Simple VIVO uses three sources for parameters to control its actions.  The _last_ value found is the value that
#   is used
#
#   1. Defaults in the code.  These defaults are coded for each parameter in the add_argument calls below
#   2. Values in the config file.  sv.py will read a config file and set the values of the parameters
#   3. Command line parameters
#
#   Program defaults are overwritten by config file values which are overwritten by command line parameters.  Each
#   parameter is handled independently of the others.  So one parameter might be set by the command line, another
#   by program defaults (because it was unspecified on the command line and was not specified in the config file)
#   and a third parameter's value might come from the config file, overwriting the program default and left unspecified
#   on the command line

import sys
from datetime import datetime
from pump.vivopump import get_args, DefNotFoundException, InvalidDefException
from pump.pump import Pump
from pump.vivopump import make_inverse_subs


def main():
    """
    The main function.  Does the work of Simple VIVO
    :return: None
    """
    return_code = 0
    print datetime.now(), "Start"
    args = get_args()

    #   Create a Pump and use it to perform the requested actions based on arguments

    try:
        p = Pump(args.defn, args.src)
    except DefNotFoundException:
        print args.defn, "definition file not found"
        sys.exit(1)
    except InvalidDefException as invalid:
        print "Invalid definition file", args.defn, "\n", invalid
        sys.exit(1)

    p.filter = not args.nofilters
    p.inter = args.inter
    p.intra = args.intra
    p.rdfprefix = args.rdfprefix
    p.uriprefix = args.uriprefix
    p.queryuri = args.queryuri
    p.username = args.username
    p.password = args.password
    p.prefix = args.prefix

    if args.action == 'get':
        n_rows = p.get()
        print datetime.now(), n_rows, "rows in", args.src
    elif args.action == 'update':

        try:
            [add_graph, sub_graph] = p.update()
        except IOError:
            print args.src, "file not found"
            return_code = 1
        else:
            add_file = open(args.rdfprefix + '_add.rdf', 'w')
            print >>add_file, add_graph.serialize(format='nt')
            add_file.close()
            sub_file = open(args.rdfprefix + '_sub.rdf', 'w')
            print >>sub_file, sub_graph.serialize(format='nt')
            sub_file.close()
            make_inverse_subs(args.rdfprefix + '_sub.rdf', p.query_parms)
            print datetime.now(), len(add_graph), 'triples to add', len(sub_graph), 'triples to sub'
    elif args.action == 'summarize':
        print p.summarize()
    elif args.action == 'serialize':
        print p.serialize()
    elif args.action == 'test':
        test_result = p.test()
        print test_result
        if 'Check' in test_result:
            return_code = 1
    else:
        print datetime.now(), "Unknown action.  Try sv -h for help"
    print datetime.now(), "Finish"
    sys.exit(return_code)

if __name__ == "__main__":
    main()
