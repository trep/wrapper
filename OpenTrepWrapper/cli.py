# -*- coding: utf-8 -*-

'''
This module is the OpenTrep binding main script.
'''

import OpenTrepWrapper

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
                        Default is "%s"''' % OpenTrepWrapper.DEFAULT_FMT,
        default = OpenTrepWrapper.DEFAULT_FMT
    )

    parser.add_argument('-x', '--xapiandb',
        help = '''Specify the xapian db location.
                        Default is "%s"''' % OpenTrepWrapper.DEFAULT_DB,
        default = OpenTrepWrapper.DEFAULT_DB
    )

    parser.add_argument('-l', '--log',
        help = '''Specify a log file. 
                        Default is "%s"''' % OpenTrepWrapper.DEFAULT_LOG,
        default = OpenTrepWrapper.DEFAULT_LOG
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

    ot = OpenTrepWrapper()

    if args['index']:

        ot.index_trep(xapianDBPath=args['xapiandb'],
                      logFilePath=args['log'],
                      verbose=not(args['quiet']))

        exit()

    ot.main_trep(searchString=' '.join(args['keys']),
                 outputFormat=args['format'],
                 xapianDBPath=args['xapiandb'],
                 logFilePath=args['log'],
                 verbose=not(args['quiet']))


if __name__ == '__main__':

    main()

