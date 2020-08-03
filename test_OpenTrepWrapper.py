# -*- coding: utf-8 -*-
#
# Source: https://github.com/trep/wrapper/tree/master/test_OpenTrepWrapper.py
#
# Authors: Denis Arnaud, Alex Prengere
#

import unittest
import OpenTrepWrapper


class OpenTrepWrapperTest(unittest.TestCase):

    def test_initOpenTrepLib(self):
        # DEBUG
        print("[OTP][test_initOpenTrepLib] - Initializing OpenTrepLib...")

        otp = OpenTrepWrapper.OpenTrepLib()
        self.assertIsNotNone(otp)

        #
        otp.init_cpp_extension()
        
    def test_get_paths(self):
        # DEBUG
        print("[OTP][test_get_paths] - Get the file-paths...")
        
        otp = OpenTrepWrapper.OpenTrepLib()
        self.assertIsNotNone(otp)

        #
        otp.init_cpp_extension(por_path=None,
                               xapian_index_path="/tmp/opentrep/xapian_traveldb",
                               sql_db_type="nodb",
                               sql_db_conn_str=None,
                               deployment_nb=0,
                               log_path="test_OpenTrepWrapper.log",
                               log_level=5)

        file_path_list = otp.getPaths()

        # DEBUG
        print(f"[OTP][test_get_paths] - File-path list: {file_path_list}")
        self.assertEqual(file_path_list, None)
        
    def test_index_test_por_file(self):
        # DEBUG
        print("[OTP][test_index_test_por_file] - Index with the test file...")
        
        otp = OpenTrepWrapper.OpenTrepLib()
        self.assertIsNotNone(otp)

        #
        otp.init_cpp_extension(por_path=None,
                               xapian_index_path="/tmp/opentrep/xapian_traveldb",
                               sql_db_type="nodb",
                               sql_db_conn_str=None,
                               deployment_nb=0,
                               log_path="test_OpenTrepWrapper.log",
                               log_level=5)

        # Index the POR test file
        otp.index()

        # Search
        otp.search(search_string="nce sfo", outputFormat="F")

