#!/usr/bin/env python
# encoding: utf-8

import unittest

from runners.pytest import (
    match_conftest_error,
    match_error,
    match_file_location,
    match_fixture_not_found_error,
    match_fixture_not_found_file_location,
    match_fixture_scope_mismatch,
    parse,
    parse_failure,
    parse_fixture_error,
    parse_session_failure,
)


class TestPytestRunner(unittest.TestCase):

    """Test case for runners.pytest.py module"""

    def test_match_fixture_scope_mismatch(self):
        input = r"ScopeMismatch: Invalid something"
        expected = r"Invalid something"
        result = match_fixture_scope_mismatch(input)
        self.assertEqual(expected, result)

    def test_match_file_location(self):
        input = r"application/tests/__init__.py:96: in create_user"
        expected = {"file_path": "application/tests/__init__.py", "line_no": "96"}
        result = match_file_location(input)
        self.assertEqual(expected, result)

    def test_match_file_location_windows(self):
        input = r"my_package\tests\test_something.py:1090: in test_add_something"
        expected = {"file_path": r"my_package\tests\test_something.py", "line_no": "1090"}
        result = match_file_location(input)
        self.assertEqual(expected, result)

    def test_match_file_location_when_no_match(self):
        input = r"   assert goals == {'goal_2': {'contexts': [], 'contribution': 2.0}}"
        result = match_file_location(input)
        self.assertEqual({}, result)

    def test_match_error(self):
        input = r"E   NameError: name 'asdfasdf' is not defined"
        expected = {"error": "NameError: name 'asdfasdf' is not defined"}
        result = match_error(input)
        self.assertEqual(expected, result)

    def test_match_error_when_no_match(self):
        input = r"application/tests/test_dal.py:19: in <module>"
        result = match_error(input)
        self.assertEqual({}, result)

    def test_match_conftest_error(self):
        input = "E   _pytest.config.ConftestImportFailure: (local('/test/conftest.py'), (<class 'ImportError'>, ImportError(\"No module named 'unknown'\",), <traceback object at 0x104226f88>))"
        expected = {
            'file_path': "/test/conftest.py",
            'error': "<class 'ImportError'>, ImportError(\"No module named 'unknown'\",), <traceback object at 0x104226f88>",
        }
        result = match_conftest_error(input)
        self.assertEqual(result, expected)

    def test_match_fixture_not_found_file_location(self):
        input = r"file F:\git\my_package\my_package\tests\dal\test_something.py, line 1245"
        expected = {"file_path": r"F:\git\my_package\my_package\tests\dal\test_something.py", "line_no": "1245"}
        result = match_fixture_not_found_file_location(input)
        self.assertEqual(expected, result)

    def test_match_fixture_not_found_error(self):
        input = "        fixture 'populate_redis_with_progression' not found"
        expected = {
            'error': "fixture 'populate_redis_with_progression' not found",
        }
        result = match_fixture_not_found_error(input)
        self.assertEqual(result, expected)

    def test_parse_fixture_error(self):
        input = [
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
        ]
        expected = [
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            r"okbudget/tests/conftest.py:26 <You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories>",
        ]
        result = parse_fixture_error('', iter(input))
        self.assertEqual(expected, result)

    def test_parse_fixture_error_no_filename_found(self):
        input = [
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"This should not be possible but we will test it!",
        ]
        expected = [
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"This should not be possible but we will test it!",
        ]
        result = parse_fixture_error('', iter(input))
        self.assertEqual(expected, result)

    def test_parse_session_failure(self):
        input = [
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 513, in getconftestmodules",
            "    return self._path2confmods[path]",
            "KeyError: local('/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests')",
            "",
            "During handling of the above exception, another exception occurred:",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 537, in importconftest",
            "    return self._conftestpath2mod[conftestpath]",
            "KeyError: local('/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py')",
            "",
            "During handling of the above exception, another exception occurred:",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 543, in importconftest",
            "    mod = conftestpath.pyimport()",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages/py/_path/local.py\", line 650, in pyimport",
            "    __import__(modname)",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py\", line 1, in <module>",
            "    adfasfdasdfasd",
            "NameError: name 'adfasfdasdfasd' is not defined",
            "ERROR: could not load /Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py",
        ]
        expected = [
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 513, in getconftestmodules",
            "    return self._path2confmods[path]",
            "KeyError: local('/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests')",
            "",
            "During handling of the above exception, another exception occurred:",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 537, in importconftest",
            "    return self._conftestpath2mod[conftestpath]",
            "KeyError: local('/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py')",
            "",
            "During handling of the above exception, another exception occurred:",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py\", line 543, in importconftest",
            "    mod = conftestpath.pyimport()",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages/py/_path/local.py\", line 650, in pyimport",
            "    __import__(modname)",
            "  File \"/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py\", line 1, in <module>",
            "    adfasfdasdfasd",
            "NameError: name 'adfasfdasdfasd' is not defined",
            "/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py:1 <NameError: name 'adfasfdasdfasd' is not defined>",
            "ERROR: could not load /Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py",
        ]
        result = parse_session_failure(iter(input))
        self.assertEqual(expected, list(result))

    def test_parse_failure_with_repeated_filenames(self):
        input = [
            r"self = <application.tests.test_authentication.TestAuthentication testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestAuthentication, self).setUp()",
            r"",
            r"application/tests/test_authentication.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
        ]
        expected = input + ["application/tests/__init__.py:96 <AssertionError: 500 != 200>"]
        result = parse_failure(iter(input))
        self.assertEqual(expected, result)

    def test_parse(self):
        input = [
            "============================================================================== test session starts ===============================================================================",
            "===================================================================================== ERRORS =====================================================================================",
            "__________________________________________________________________ ERROR collecting application/tests/test_dal.py ___________________________________________________________________",
            "application/tests/test_dal.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "==================================================================================== FAILURES ====================================================================================",
            "_________________________________________________________________________ TestAuthentication.test_false __________________________________________________________________________",
            "",
            "self = <application.tests.test_authentication.TestAuthentication testMethod=test_false>",
            "",
            "    def setUp(self):",
            ">       super(TestAuthentication, self).setUp()",
            "",
            "application/tests/test_authentication.py:56:",
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            "application/tests/__init__.py:46: in setUp",
            "    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
            "application/tests/__init__.py:96: in create_user",
            "    self.assertEqual(response.code, 200)",
            "E   AssertionError: 500 != 200",
            "------------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------------",
            "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
            "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
            "Traceback (most recent call last):",
            "  File \"/Git/Backend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
            "    result = method(*self.path_args, **self.path_kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 135, in wrapper",
            "    return method(self, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 105, in request_wrapper",
            "    response = request(self, arguments, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/authentication.py\", line 105, in post",
            "    body['email']",
            "  File \"/Git/Backend/application/dal.py\", line 257, in create_user",
            "    return self._convert_to_user(user)",
            "  File \"/Git/Backend/application/dal.py\", line 236, in _convert_to_user",
            "    blarg",
            "NameError: name 'blarg' is not defined",
            "ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
        ]
        expected = [
            "============================================================================== test session starts ===============================================================================",
            "===================================================================================== ERRORS =====================================================================================",
            "__________________________________________________________________ ERROR collecting application/tests/test_dal.py ___________________________________________________________________",
            "application/tests/test_dal.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "application/tests/test_dal.py:19 <NameError: name 'asdfasdf' is not defined>",
            "==================================================================================== FAILURES ====================================================================================",
            "_________________________________________________________________________ TestAuthentication.test_false __________________________________________________________________________",
            "",
            "self = <application.tests.test_authentication.TestAuthentication testMethod=test_false>",
            "",
            "    def setUp(self):",
            ">       super(TestAuthentication, self).setUp()",
            "",
            "application/tests/test_authentication.py:56:",
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            "application/tests/__init__.py:46: in setUp",
            "    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
            "application/tests/__init__.py:96: in create_user",
            "    self.assertEqual(response.code, 200)",
            "E   AssertionError: 500 != 200",
            "application/tests/__init__.py:96 <AssertionError: 500 != 200>",
            "------------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------------",
            "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
            "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
            "Traceback (most recent call last):",
            "  File \"/Git/Backend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
            "    result = method(*self.path_args, **self.path_kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 135, in wrapper",
            "    return method(self, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 105, in request_wrapper",
            "    response = request(self, arguments, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/authentication.py\", line 105, in post",
            "    body['email']",
            "  File \"/Git/Backend/application/dal.py\", line 257, in create_user",
            "    return self._convert_to_user(user)",
            "  File \"/Git/Backend/application/dal.py\", line 236, in _convert_to_user",
            "    blarg",
            "NameError: name 'blarg' is not defined",
            "/Git/Backend/application/dal.py:236 <NameError: name 'blarg' is not defined>",
            "ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_error_in_module_function(self):
        input = [
            r"============================================================================== test session starts ===============================================================================",
            r"=================================== FAILURES ===================================",
            r"_________________________________ test_myfunc __________________________________",
            r"okbudget/tests/test_authentication.py:283: in test_myfunc",
            r"assert False",
            r"E   assert False",
            r"None <assert False>",
            r"=========================== 1 failed in 0.21 seconds ===========================",
        ]
        expected = [
            r"============================================================================== test session starts ===============================================================================",
            r"=================================== FAILURES ===================================",
            r"_________________________________ test_myfunc __________________________________",
            r"okbudget/tests/test_authentication.py:283: in test_myfunc",
            r"assert False",
            r"E   assert False",
            r"okbudget/tests/test_authentication.py:283 <assert False>",
            r"None <assert False>",
            r"=========================== 1 failed in 0.21 seconds ===========================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_conftest_import_failure(self):
        input = [
            r"============================================================================== test session starts ===============================================================================",
            r"===================================================================================== ERRORS =====================================================================================",
            r"_______________________________________________________________________________ ERROR collecting  ________________________________________________________________________________",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:332: in visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            r"    dirs = self.optsort([p for p in entries",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:368: in <listcomp>",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:632: in _recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:162: in __getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:692: in _getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:521: in getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:545: in importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   _pytest.config.ConftestImportFailure: (local('/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py'), (<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>))",
            r"============================================================================ 1 error in 0.56 seconds =============================================================================",
        ]
        expected = [
            r"============================================================================== test session starts ===============================================================================",
            r"===================================================================================== ERRORS =====================================================================================",
            r"_______________________________________________________________________________ ERROR collecting  ________________________________________________________________________________",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:332: in visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            r"    dirs = self.optsort([p for p in entries",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:368: in <listcomp>",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:632: in _recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:162: in __getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:692: in _getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:521: in getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:545: in importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   _pytest.config.ConftestImportFailure: (local('/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py'), (<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>))",
            r"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py:1 <<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>>",
            r"============================================================================ 1 error in 0.56 seconds =============================================================================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_fixture_error(self):
        input = [
            r"============================================================================== test session starts ===============================================================================",
            r"platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: /Users/okcompute/Developer/Git/OkBudgetBackend, inifile: setup.cfg",
            r"collected 48 items",
            r"",
            r"okbudget/tests/test_authentication.py ......",
            r"okbudget/tests/test_dal.py ......................",
            r"okbudget/tests/test_envelope.py ................",
            r"okbudget/tests/test_fixtures.py E",
            r"okbudget/tests/test_users.py ...",
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            r"okbudget/tests/conftest.py:21:  def function_fixture()",
        ]
        expected = [
            r"============================================================================== test session starts ===============================================================================",
            r"platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: /Users/okcompute/Developer/Git/OkBudgetBackend, inifile: setup.cfg",
            r"collected 48 items",
            r"",
            r"okbudget/tests/test_authentication.py ......",
            r"okbudget/tests/test_dal.py ......................",
            r"okbudget/tests/test_envelope.py ................",
            r"okbudget/tests/test_fixtures.py E",
            r"okbudget/tests/test_users.py ...",
            r"===================================================================================== ERRORS =====================================================================================",
            r"________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            r"okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            r"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py:26 <You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories>",
            r"okbudget/tests/conftest.py:21:  def function_fixture()",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_session_failure(self):
        input = [
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 513, in getconftestmodules',
            r'    return self._path2confmods[path]',
            r'KeyError: local(\'/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests\')',
            r'',
            r'During handling of the above exception, another exception occurred:',
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 537, in importconftest',
            r'    return self._conftestpath2mod[conftestpath]',
            r'KeyError: local(\'/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py\')',
            r'',
            r'During handling of the above exception, another exception occurred:',
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 543, in importconftest',
            r'    mod = conftestpath.pyimport()',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages/py/_path/local.py", line 650, in pyimport',
            r'    __import__(modname)',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py", line 1, in <module>',
            r'    adfasfdasdfasd',
            r'NameError: name \'adfasfdasdfasd\' is not defined',
            r'ERROR: could not load /Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py',
        ]
        expected = [
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 513, in getconftestmodules',
            r'    return self._path2confmods[path]',
            r'KeyError: local(\'/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests\')',
            r'',
            r'During handling of the above exception, another exception occurred:',
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 537, in importconftest',
            r'    return self._conftestpath2mod[conftestpath]',
            r'KeyError: local(\'/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py\')',
            r'',
            r'During handling of the above exception, another exception occurred:',
            r'Traceback (most recent call last):',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages//config.py", line 543, in importconftest',
            r'    mod = conftestpath.pyimport()',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/venv/lib/python3.4/site-packages/py/_path/local.py", line 650, in pyimport',
            r'    __import__(modname)',
            r'  File "/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py", line 1, in <module>',
            r'    adfasfdasdfasd',
            r'NameError: name \'adfasfdasdfasd\' is not defined',
            r'/Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py:1 <NameError: name \'adfasfdasdfasd\' is not defined>',
            r'ERROR: could not load /Users/okcompute/Developer/Git/okbudgetbackend/okbudget/tests/conftest.py',
        ]
        self.maxDiff = None
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_empty_lines(self):
        self.assertEqual(parse([]), [])

    def test_parse_when_short_is_not_set(self):
        """
        Test the parser behaviour if the pytest command was not run with the
        --short option set. The error will not be found but the script won't
        crash.
        """
        input = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 274 items",
            r" ",
            r"my_package\tests\test_module.py ......F........",
            r" ",
            r"================================== FAILURES ===================================",
            r"_____________ TestRedisInterface.test_somethings_progression_key ______________",
            r" ",
            r"self = <test_redis_interface.TestRedisInterface instance at 0x06CA4170>",
            r"redis = <my_package.dal.redis_interface.RedisInterface object at 0x06AFB650>",
            r" ",
            r"    def test_somethings_progression_key(self, redis):",
            r">       assert 'Something:somethings:instances:progression:123' == str(",
            r"            redis.get_something_progression_key(123),",
            r"        )",
            r"E       AttributeError: 'RedisInterface' object has no attribute 'get_something_progression_key'",
            r" ",
            r"my_package\tests\dal\test_redis_interface.py:45: AttributeError",
            r"==================== 1 failed, 273 passed in 5.10 seconds =====================",
        ]
        expected = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 274 items",
            r" ",
            r"my_package\tests\test_module.py ......F........",
            r" ",
            r"================================== FAILURES ===================================",
            r"_____________ TestRedisInterface.test_somethings_progression_key ______________",
            r" ",
            r"self = <test_redis_interface.TestRedisInterface instance at 0x06CA4170>",
            r"redis = <my_package.dal.redis_interface.RedisInterface object at 0x06AFB650>",
            r" ",
            r"    def test_somethings_progression_key(self, redis):",
            r">       assert 'Something:somethings:instances:progression:123' == str(",
            r"            redis.get_something_progression_key(123),",
            r"        )",
            r"E       AttributeError: 'RedisInterface' object has no attribute 'get_something_progression_key'",
            r" ",
            r"my_package\tests\dal\test_redis_interface.py:45: AttributeError",
            r"==================== 1 failed, 273 passed in 5.10 seconds =====================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_conftest_type_error(self):
        input = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 0 items / 1 errors",
            r" ",
            r"=================================== ERRORS ====================================",
            r"______________________________ ERROR collecting  ______________________________",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:332: in visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:368: in gen",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:632: in _recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:162: in __getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:692: in _getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:521: in getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:545: in importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   ConftestImportFailure: (local('F:\git\my_package\my_package\tests\service\conftest.py'), (<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>))",
            r"=========================== 1 error in 1.69 seconds ===========================",
        ]
        expected = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 0 items / 1 errors",
            r" ",
            r"=================================== ERRORS ====================================",
            r"______________________________ ERROR collecting  ______________________________",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:332: in visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:368: in gen",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:632: in _recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:162: in __getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:692: in _getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:521: in getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:545: in importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   ConftestImportFailure: (local('F:\git\my_package\my_package\tests\service\conftest.py'), (<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>))",
            r"F:\git\my_package\my_package\tests\service\conftest.py:1 <<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>>",
            r"=========================== 1 error in 1.69 seconds ===========================",
        ]
        self.maxDiff = None
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_on_windows(self):
        input = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 81 items",
            r"",
            r"my_package\tests\test_module.py .....................................F.....................",
            r"",
            r"================================== FAILURES ===================================",
            r"___________ TestSomethingDAL.test_add_player_contribution_to_goals ____________",
            r"my_package\tests\dal\test_something.py:1090: in test_add_player_contribution_to_goals",
            r"    assert goals == {'goal_2': {'contexts': [], 'contribution': 2.0}}",
            r"E   assert {'goal_2': {'...ribution': 0}} == {'goal_2': {'c...bution': 2.0}}",
            r"E     Differing items:",
            r"E     {'goal_2': {'contexts': [], 'contribution': 0}} != {'goal_2': {'contexts': [], 'contribution': 2.0}}",
            r"E     Use -v to get the full diff",
            r"===================== 1 failed, 80 passed in 1.73 seconds =====================",
        ]

        expected = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 81 items",
            r"",
            r"my_package\tests\test_module.py .....................................F.....................",
            r"",
            r"================================== FAILURES ===================================",
            r"___________ TestSomethingDAL.test_add_player_contribution_to_goals ____________",
            r"my_package\tests\dal\test_something.py:1090: in test_add_player_contribution_to_goals",
            r"    assert goals == {'goal_2': {'contexts': [], 'contribution': 2.0}}",
            r"E   assert {'goal_2': {'...ribution': 0}} == {'goal_2': {'c...bution': 2.0}}",
            r"my_package\tests\dal\test_something.py:1090 <assert {'goal_2': {'...ribution': 0}} == {'goal_2': {'c...bution': 2.0}}>",
            r"E     Differing items:",
            r"E     {'goal_2': {'contexts': [], 'contribution': 0}} != {'goal_2': {'contexts': [], 'contribution': 2.0}}",
            r"E     Use -v to get the full diff",
            r"===================== 1 failed, 80 passed in 1.73 seconds =====================",
        ]
        self.maxDiff = None
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_fixture_not_found(self):
        input = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 88 items",
            r" ",
            r"my_package\tests\dal\test_something.py ....................................F....FFF...................F.E.F.F.......F.FF.......",
            r" ",
            r"=================================== ERRORS ====================================",
            r"___ ERROR at setup of TestSomethingDAL.test_get_goals_player_contributions ____",
            r"file F:\git\my_package\my_package\tests\dal\test_something.py, line 1245",
            r"      def test_get_goals_player_contributions(",
            r"        fixture 'populate_redis_with_progression' not found",
            r"        available fixtures: pytestconfig, goals_configuration, mutable_service, force_default_settings, somethings, tmpdir, registered_somethings, populate_redis, redis, completed_somethings, service, something_dictionaries, mock_utcnow, registered_somethings_with_progression, load_service, submissions, goal_instances, somethings_with_registration, use_redis, use_mongo, dal, recwarn, monkeypatch, invalid_something_instances, registered_populations_context, registered_principal_ids, flush_redis, cov, something_instances, reward_instances, somethings_with_progression, capfd, capsys",
            r"        use 'py.test --fixtures [testpath]' for help on them.",
        ]
        expected = [
            r"============================= test session starts =============================",
            r"platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            r"rootdir: F:\git\my_package, inifile: setup.cfg",
            r"plugins: cache, cov, flake8",
            r"collected 88 items",
            r" ",
            r"my_package\tests\dal\test_something.py ....................................F....FFF...................F.E.F.F.......F.FF.......",
            r" ",
            r"=================================== ERRORS ====================================",
            r"___ ERROR at setup of TestSomethingDAL.test_get_goals_player_contributions ____",
            r"file F:\git\my_package\my_package\tests\dal\test_something.py, line 1245",
            r"      def test_get_goals_player_contributions(",
            r"        fixture 'populate_redis_with_progression' not found",
            r"F:\git\my_package\my_package\tests\dal\test_something.py:1245 <fixture 'populate_redis_with_progression' not found>",
            r"        available fixtures: pytestconfig, goals_configuration, mutable_service, force_default_settings, somethings, tmpdir, registered_somethings, populate_redis, redis, completed_somethings, service, something_dictionaries, mock_utcnow, registered_somethings_with_progression, load_service, submissions, goal_instances, somethings_with_registration, use_redis, use_mongo, dal, recwarn, monkeypatch, invalid_something_instances, registered_populations_context, registered_principal_ids, flush_redis, cov, something_instances, reward_instances, somethings_with_progression, capfd, capsys",
            r"        use 'py.test --fixtures [testpath]' for help on them.",
        ]
        self.maxDiff = None
        result = parse(input)
        self.assertEqual(expected, result)
