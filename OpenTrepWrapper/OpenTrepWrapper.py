# -*- coding: utf-8 -*-
#
# Source: https://github.com/trep/wrapper/tree/master/OpenTrepWrapper/OpenTrepWrapper.py
#
# Authors: Alex Prengere, Denis Arnaud
#

'''
This module is an OpenTrep binding.

 >>> import OpenTrepWrapper

 >>> otp = OpenTrepWrapper.OpenTrepLib()

 >>> otp.init_cpp_extension(por_path=None,
                           xapian_index_path="/tmp/opentrep/xapian_traveldb",
                           sql_db_type="nodb",
                           sql_db_conn_str=None,
                           deployment_nb=0,
                           log_path="test_OpenTrepWrapper.log",
                           log_level=5)

 >>> otp.index()

 >>> otp.search(search_string="nce sfo", outputFormat="S")
 ([(89.8466, 'NCE'), (357.45599999999996, 'SFO')], '')
 ------------------

 >>> otp.finalize()

'''

from __future__ import with_statement

import os
import sys
import inspect
import errno
import pathlib
import json

class Error(Exception):
   """
   Base class for other OpenTrep (OTP) exceptions
   """
   pass

class OPTInitError(Error):
   """
   Raised when there is an issue initializing OenTrep Python eztension
   """
   pass

class PathCreationError(Error):
   """
   Raised when there is an issue creating a directory structure
   """
   pass

class OutputFormatError(Error):
   """
   Raised when the given output format is not in the list
   """
   pass

class SQLDBTypeError(Error):
   """
   Raised when the given SQL database type is not in the list
   """
   pass

class OpenTrepLib():
    """
    This class wraps the methods of the OpenTrep Python extension
    and a few utilities.

    Log levels: 1. Critical; 2. Errors; 3: Warnings; 4: Info; 5: Verbose
    """

    def __init__(self):
        # Default settings
        self.por_filepath = '/tmp/opentraveldata/optd_por_public_all.csv'
        self.xapian_index_filepath = '/tmp/opentrep/xapian_traveldb'
        self.sql_db_type_list = set(['nodb', 'sqlite', 'mysql'])
        self.sql_db_type = 'nodb'
        self.sql_db_conn_str = ''
        self.deployment_nb = 0
        self.output_available_formats = set(['I', 'J', 'F', 'S'])
        self.output_format = 'S'
        self.log_filepath = '/tmp/opentrep/opentrepwrapper.log'
        self.log_level = 2
        self.flag_index_non_iata_por = False
        self.flag_init_xapian = True
        self.flag_add_por_to_db = False
        self._trep_lib = None

    def __str__(self):
        """
        Description of the OpenTrepLib instance
        """
        desc = f"Xapian index: {self.xapian_index_filepath}; " \
            f"SQL DB type: {self.sql_db_type}; " \
            f"Deployment: {self.deployment_nb}; " \
            f"log file: {self.log_filepath}"
        return desc

    def get_log_pfx(self):
        """
        Derive a prefix for logging purpose
        """
        # 0 represents this line
        # 1 represents line at caller
        callerframerecord = inspect.stack()[1]

        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        filename = os.path.basename(info.filename)
        log_pfx = f"[TREP][{filename}][{info.function}][{info.lineno}] -"
        return log_pfx

    def derive_optd_por_test_filepath(self, pyotp_path=None):
        otp_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pyotp_path)))))
        optd_por_test_filepath = f"{otp_dir}/share/opentrep/data/por/test_optd_por_public.csv"
        return optd_por_test_filepath

    def init_cpp_extension(self, por_path=None, xapian_index_path=None,
                           sql_db_type=None, sql_db_conn_str=None,
                           deployment_nb=None,
                           log_path=None, log_level=None):
        if por_path:
            self.por_filepath = por_path

        if xapian_index_path:
            self.xapian_index_filepath = xapian_index_path

        if sql_db_type:
            if sql_db_type in self.sql_db_type_list:
                self.sql_db_type = sql_db_type
            else:
                #
                log_pfx = self.get_log_pfx()
                err_msg = f"{log_pfx} Error - The given SQL database type is " \
                    f"not in the list of possible types: {self.sql_db_type_list}"
                raise SQLDBTypeError(err_msg)

        if sql_db_conn_str:
            self.sql_db_conn_str = sql_db_conn_str

        if deployment_nb:
            self.deployment_nb = deployment_nb

        if log_path:
            self.log_filepath = log_path

        if log_level:
            self.log_level = log_level

        #
        does_xapian_dir_exist = os.path.isdir(self.xapian_index_filepath)
        if not does_xapian_dir_exist:
            # If the directory hosting the Xapian index is not existing, it
            # probably means that the Xapian index has not been created yet.
            # First, the directory has to be created.
            if self.log_level >= 4:
                log_pfx = self.get_log_pfx()
                print(f"{log_pfx} Directory {self.xapian_index_path} did not" \
                      " exist, creating it")
            self.mkdir_p(self.xapian_index_filepath)

        #
        try:
            # Initialise the OpenTrep Python extension
            import pyopentrep

        except ImportError:
            #
            log_pfx = self.get_log_pfx()
            pypi_url = "https://pypi.org/project/opentrep/"
            err_msg = f"{log_pfx} Error - The OpenTrep Python externsion " \
                "cannot be properly initialized. See {pypi_url}"
            raise ImportError(err_msg)

        self._trep_lib = pyopentrep.OpenTrepSearcher()

        # Derive the path to the test POR file
        otpso_fp = inspect.getfile(pyopentrep)
        optd_por_test_filepath = self.derive_optd_por_test_filepath(otpso_fp)

        if not por_path:
            self.por_filepath = optd_por_test_filepath
        
        # sqlDBType = 'sqlite'
        # sqlDBConnStr = '/tmp/opentrep/sqlite_travel.db'
        xapianDBActualPath = f"{self.xapian_index_filepath}{self.deployment_nb}"
        initOK = self._trep_lib.init (self.por_filepath,
                                      self.xapian_index_filepath,
                                      self.sql_db_type,
                                      self.sql_db_conn_str,
                                      self.deployment_nb,
                                      self.flag_index_non_iata_por,
                                      self.flag_init_xapian,
                                      self.flag_add_por_to_db,
                                      self.log_filepath)

        if not initOK:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The OpenTrep Python extension " \
                f"cannot be initialized - OpenTrepLib object: {self}"
            raise OPTInitError(err_msg)

    def finalize(self):
        """
        Free the OpenTREP library resource
        """
        if self._trep_lib:
            self._trep_lib.finalize()

    def __enter__(self):
        """
        To be used in with statements.
        """
        return self

    def __exit__(self, type_, value, traceback):
        """
        On de-indent inside with statement.
        """
        if self._trep_lib:
            self.finalize()

    def getPaths(self):
        """
        File-paths details
        """

        # Check that the OpenTrep Python extension has been initialized
        if not self._trep_lib:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The OpenTrep Python extension has " \
                "not been initialized properly - OpenTrepLib: {self}"
            raise OPTInitError(err_msg)
        
        # Calls the underlying OpenTrep library service
        filePathStr = self._trep_lib.getPaths()
        filePathList = filePathStr.split(';')

        # Report the results
        optd_filepath = filePathList[0]
        xapian_filepath = filePathList[1]
        log_pfx = self.get_log_pfx()
        print(f"{log_pfx} OPTD-maintained list of POR (points of reference): " \
              f"'{optd_filepath}'")
        print(f"{log_pfx} Xapian-based travel database/index: " \
              f"'{xapian_filepath}'")

    def index(self):
        '''
        Indexation
        '''

        # Check that the OpenTrep Python extension has been initialized
        if not self._trep_lib:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The OpenTrep Python extension has " \
                "not been initialized properly - OpenTrepLib: {self}"
            raise OPTInitError(err_msg)

        if self.log_level >= 4:
            print("Perform the indexation of the (Xapian-based) travel database.")
            print("That operation may take several minutes on some slow machines.")
            print("It takes less than 20 seconds on fast ones...")

        # Calls the underlying OpenTrep library service
        result = self._trep_lib.index()

        if self.log_level >= 4:
            # Report the results
            print(f"Done. Indexed {result} POR (points of reference)")

    ##
    # JSON interpreter. The JSON structure contains a list with the main matches,
    # along with their associated fields (weights, coordinates, etc).
    # For every main match:
    #  - There is a potential list of extra matches (i.e., matches with the same
    #    matching percentage).
    #  - There is a potential list of alternate matches (i.e., matches with lower
    #    matching percentages).
    #
    # Samples of result string to be parsed:
    #  - pyopentrep -fJ "nice sna francisco"
    #    - {'locations':[
    #         {'names':[
    #            {'name': 'Nice Airport'}, {'name': 'Nice Côte d'Azur International Airport'}],
    #          'cities': { 'city_details': { 'iata_code': 'NCE' } },
    #         {'names':[
    #            {'name': 'San Francisco Apt'}, {'name': 'San Francisco Intl. Airport'}],
    #          'cities': { 'city_details': { 'iata_code': 'SFO' } },
    #      ]}
    #
    def interpretFromJSON(self, jsonFormattedResult):
        parsedStruct = json.loads(jsonFormattedResult)
        interpretedString = ""
        for location in parsedStruct["locations"]:
            interpretedString += location["iata_code"] + "-"
            interpretedString += location["icao_code"] + "-"
            interpretedString += location["geonames_id"] + " "
            interpretedString += "(" + location["page_rank"] + "%) / "
            interpretedString += location["cities"]["city_details"]["iata_code"] + ": "
            interpretedString += location["lat"] + " "
            interpretedString += location["lon"] + "; "

        #
        return interpretedString

    ##
    # Protobuf interpreter. The Protobuf structure contains a list with the
    # main matches, along with their associated fields (weights, coordinates,
    # etc).
    def interpretFromProtobuf(self, protobufFormattedResult):
        unmatchedKeywordString, interpretedString = "", ""

        # DEBUG
        # print (f"DEBUG - Protobuf (array of bytes): {protobufFormattedResult}")

        # Protobuf
        import google.protobuf.message
        
        try:
            import Travel_pb2

        except ImportError:
            #
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The Travel Protobuf part of the " \
                "OpenTrep Python externsion cannot be properly initialized. " \
                "See https://pypi.org/project/opentrep/"
            raise ImportError(err_msg)

        queryAnswer = Travel_pb2.QueryAnswer()
        try:
            queryAnswer.ParseFromString(protobufFormattedResult)

        except google.protobuf.message.DecodeError as err:
            #
            log_pfx = self.get_log_pfx()
            print(f"{log_pfx} Error - Issue with the decoding. Will continue " \
                  "though")
            print(f"{log_pfx} Protobuf QueryAnswer object: {queryAnswer}")

        # List of recognised places
        placeList = queryAnswer.place_list

        # DEBUG
        if self.log_level >= 5:
            print (f"DEBUG - Result: {placeList}")

        for place in placeList.place:
            airport_code = place.tvl_code
            interpretedString += airport_code.code + "-"
            icao_code = place.icao_code
            interpretedString += icao_code.code + "-"
            geoname_id = place.geonames_id
            interpretedString += str(geoname_id.id) + " "
            page_rank = place.page_rank
            interpretedString += "(" + str(page_rank.rank) + "%) / "
            city_list = place.city_list.city
            city = Travel_pb2.City()
            for svd_city in city_list:
                city = svd_city
            interpretedString += str(city.code.code) + ": "
            geo_point = place.coord
            interpretedString += str(geo_point.latitude) + " "
            interpretedString += str(geo_point.longitude) + "; "

        # List of un-matched keywords
        unmatchedKeywords = queryAnswer.unmatched_keyword_list

        for keyword in unmatchedKeywords.word:
            unmatchedKeywordString += keyword

        #
        return unmatchedKeywordString, interpretedString
    
    def search(self, search_string=None, outputFormat=None):
        """
        Search

        If no search string was supplied as arguments of the command-line,
        ask the user for some

        Call the OpenTrep C++ library.

        The 'I' (Interpretation from JSON) output format is just an example
        of how to use the output generated by the OpenTrep library. Hence,
        that latter does not support that "output format". So, the raw JSON
        format is required, and the JSON string will then be parsed and
        interpreted by the jsonResultParser() method, just to show how it
        works
        """

        # Check that the OpenTrep Python extension has been initialized
        if not self._trep_lib:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The OpenTrep Python extension has " \
                "not been initialized properly - OpenTrepLib: {self}"
            raise OPTInitError(err_msg)

        if not outputFormat:
            outputFormat = self.output_format
            
        if outputFormat not in self.output_available_formats:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The given output format " \
                f"('{outputFormat}') is invalid. It should be one of " \
                f"{self.output_available_formats}."
            raise OutputFormatError(err_msg)
        
        # If no search string was supplied as arguments of the command-line,
        # ask the user for some
        if not search_string:
            # Ask for the user input
            search_string = raw_input(
                "Enter a search string, e.g., 'rio de janero sna francisco'"
            )
        if search_string == "":
            search_string = "nce sfo"

        # DEBUG
        if self.log_level >= 4:
            print(f"search_string: {search_string}")

        ##
        # Call the OpenTrep C++ library.
        #
        opentrepOutputFormat = outputFormat
        result = None

        # The 'I' (Interpretation from JSON) output format is just an example
        # of how to use the output generated by the OpenTrep library. Hence,
        # that latter does not support that "output format". So, the raw JSON
        # format is required, and the JSON string will then be parsed and
        # interpreted by the interpretFromJSON() method, just to show how it
        # works
        if opentrepOutputFormat == "I":
            opentrepOutputFormat = "J"

        #
        if opentrepOutputFormat != "P":
            result = self._trep_lib.search(opentrepOutputFormat, search_string)

        # When the compact format is selected, the result string has to be
        # parsed accordingly.
        if outputFormat == "S":
            parsedStruct = self.compactResultParser(result)
            print("Compact format => recognised place (city/airport) codes:")
            print(parsedStruct)
            print("------------------")

        # When the full details have been requested, the result string is
        # potentially big and complex, and is not aimed to be
        # parsed. So, the result string is just displayed/dumped as is.
        elif outputFormat == "F":
            print("Raw result from the OpenTrep library:")
            print(result)
            print("------------------")

        # When the raw JSON format has been requested, no handling is necessary.
        elif outputFormat == "J":
            print("Raw (JSON) result from the OpenTrep library:")
            print(result)
            print("------------------")

        # The interpreted JSON format is an example of how to extract relevant
        # information from the corresponding Python structure. That code can be
        # copied/pasted by clients to the OpenTREP library.
        elif outputFormat == "I":
            interpretedString = self.interpretFromJSON(result)
            print("JSON format => recognised place (city/airport) codes:")
            print(interpretedString)
            print("------------------")

        # The interpreted Protobuf format is an example of how to extract
        # relevant information from the corresponding Python structure.
        # That code can be copied/pasted by clients to the OpenTREP library.
        elif outputFormat == "P":
            result = self._trep_lib.searchToPB(search_string)
            unmatchedKeywords, interpretedString = interpretFromProtobuf(result)
            print("Protobuf format => recognised place (city/airport) codes:")
            print(interpretedString)
            print("Unmatched keywords:")
            print(unmatchedKeywords)
            print("------------------")

    def compactResultParser(self, resultString):
        """
        Compact result parser. The result string contains the main matches,
        separated by commas (','), along with their associated weights, given
        as percentage numbers. For every main match:

        - Columns (':') separate potential extra matches (i.e., matches with the same
        matching percentage).
        - Dashes ('-') separate potential alternate matches (i.e., matches with lower
        matching percentages).

        Samples of result string to be parsed:

        % python3 pyopentrep.py -f S nice sna francisco vancouver niznayou
        'nce/100,sfo/100-emb/98-jcc/97,yvr/100-cxh/83-xea/83-ydt/83;niznayou'
        % python3 pyopentrep.py -f S fr
        'aur:avf:bae:bou:chr:cmf:cqf:csf:cvf:dij/100'

        >>> test_1 = 'nce/100,sfo/100-emb/98-jcc/97,yvr/100-cxh/83-xea/83-ydt/83;niznayou'
        >>> compactResultParser(test_1)
        ([(1.0, 'NCE'), (1.0, 'SFO'), (1.0, 'YVR')], 'niznayou')

        >>> test_2 = 'aur:avf:bae:bou:chr:cmf:cqf:csf:cvf:dij/100'
        >>> compactResultParser(test_2)
        ([(1.0, 'AUR')], '')

        >>> test_3 = ';eeee'
        >>> compactResultParser(test_3)
        ([], 'eeee')
        """

        # Strip out the unrecognised keywords
        if ';' in resultString:
            str_matches, unrecognized = resultString.split(';', 1)
        else:
            str_matches, unrecognized = resultString, ''

        if not str_matches:
            return [], unrecognized

        codes = []

        for alter_loc in str_matches.split(','):

            for extra_loc in alter_loc.split('-'):

                extra_loc, score = extra_loc.split('/', 1)

                for code in extra_loc.split(':'):

                    codes.append((float(score) / 100.0, code.upper()))

                    # We break because we only want to first
                    break

                # We break because we only want to first
                break

        return codes, unrecognized

    def jsonResultParser(self, resultString):
        '''
        JSON interpreter. The JSON structure contains a list with the main matches,
        along with their associated fields (weights, coordinates, etc).
        For every main match:

        - There is a potential list of extra matches (i.e., matches with the same
        matching percentage).
        - There is a potential list of alternate matches (i.e., matches with lower
        matching percentages).

        Samples of result string to be parsed:

        - python3 pyopentrep.py -f J nice sna francisco
        - {'locations':[
            {'names':[
               {'name': 'nice'}, {'name': 'nice/fr:cote d azur'}],
             'city_code': 'nce'},
            {'names':[
               {'name': 'san francisco'}, {'name': 'san francisco/ca/us:intl'}],
             'city_code': 'sfo',
             'alternates':[
                  {'names':[
                      {'name': 'san francisco emb'},
                      {'name': 'san francisco/ca/us:embarkader'}],
                      'city_code': 'sfo'},
                  {'names':[
                      {'name': 'san francisco jcc'},
                      {'name': 'san francisco/ca/us:china hpt'}],
                      'city_code': 'sfo'}
            ]}
         ]}

        - python3 pyopentrep.py -f J fr
        - {'locations':[
            {'names':[
               {'name': 'aurillac'}, {'name': 'aurillac/fr'}],
                'extras':[
                {'names':[
                  {'name': 'avoriaz'}, {'name': 'avoriaz/fr'}],
                'city_code': 'avf'},
               {'names':[
                  {'name': 'barcelonnette'}, {'name': 'barcelonnette/fr'}],
                'city_code': 'bae'}
            ]}
         ]}

        >>> res = """{ "locations":[{
        ...                 "iata_code": "ORY",
        ...                 "icao_code": "LFPO",
        ...                 "city_code": "PAR",
        ...                 "geonames_id": "2988500",
        ...                 "lon": "2.359444",
        ...                 "lat": "48.725278",
        ...                 "page_rank": "23.53"
        ...             }, {
        ...                 "iata_code": "CDG",
        ...                 "icao_code": "LFPG",
        ...                 "city_code": "PAR",
        ...                 "geonames_id": "6269554",
        ...                 "lon": "2.55",
        ...                 "lat": "49.012779",
        ...                 "page_rank": "64.70"
        ...             }]
        ... }"""
        >>> print(jsonResultParser(res))
        ORY-LFPO-2988500-23.53%-PAR-48.73-2.36; CDG-LFPG-6269554-64.70%-PAR-49.01-2.55
        '''

        return '; '.join(
            '-'.join([
                loc['iata_code'],
                loc['icao_code'],
                loc['geonames_id'],
                '%.2f%%' % float(loc['page_rank']),
                loc['cities']['city_details']['iata_code'],
                '%.2f' % float(loc['lat']),
                '%.2f' % float(loc['lon'])
            ])
            for loc in json.loads(resultString)['locations']
        )

    def mkdir_p(self, path):
        """
        mkdir -p behavior.
        """
        
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        does_path_exist = os.path.isdir(path)
        
        if not does_path_exist:
            log_pfx = self.get_log_pfx()
            err_msg = f"{log_pfx} Error - The {path} directory structure " \
                f"cannot be created. It may come from an issue with permissions."
            raise PathCreationError(err_msg)

