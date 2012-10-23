#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module is the OpenTrep binding main script.
'''

from OpenTrepWrapper import main_trep, index_trep
from OpenTrepWrapper import DEFAULT_LOG, DEFAULT_FMT, DEFAULT_DB



def main():
    '''
    Main function.
    '''

    import argparse

    parser = argparse.ArgumentParser(description='Python OpenTrep binding.')

    parser.epilog = 'Example: python %s rio de janero lso angles reykyavki' % \
            parser.prog

    parser.add_argument('keys',
        help='Main argument, free text.',
        nargs='*'
    )

    parser.add_argument('-f', '--format',
        help = '''Choose a different format.
                        Must be either F, S, J, I.
                        Default is "%s"''' % DEFAULT_FMT,
        default = DEFAULT_FMT
    )

    parser.add_argument('-x', '--xapiandb',
        help = '''Specify the xapian db location.
                        Default is "%s"''' % DEFAULT_DB,
        default = DEFAULT_DB
    )

    parser.add_argument('-l', '--log',
        help = '''Specify a log file. 
                        Default is "%s"''' % DEFAULT_LOG,
        default = DEFAULT_LOG
    )

    parser.add_argument('-q', '--quiet',
        help = '''Turn off verbose output.''',
        action='store_true'
    )

    parser.add_argument('-i', '--index',
        help = '''Index the base then exit.''',
        action='store_true'
    )

    args = vars(parser.parse_args())

    if args['index']:

        index_trep(xapianDBPath=args['xapiandb'],
                   logFilePath=args['log'],
                   verbose=not(args['quiet']))

        exit()

    main_trep(searchString=' '.join(args['keys']),
              outputFormat=args['format'],
              xapianDBPath=args['xapiandb'],
              logFilePath=args['log'],
              verbose=not(args['quiet']))



if __name__ == '__main__':

    main()

