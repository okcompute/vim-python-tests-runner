#!/usr/bin/env python
# encoding: utf-8

import unittest

from runners.pytest import (
    match_conftest_error,
    match_error,
    match_file_location,
    match_scope_mismatch,
    parse,
    parse_failure,
    parse_fixture_error,
    parse_session_failure,
)


class TestPytestRunner(unittest.TestCase):

    """Test case for runners.pytest.py module"""

    def test_match_scope_mismatch(self):
        input = "ScopeMismatch: Invalid something"
        expected = "Invalid something"
        result = match_scope_mismatch(input)
        self.assertEqual(expected, result)

    def test_match_file_location(self):
        input = "application/tests/__init__.py:96: in create_user"
        expected = {"file_path": "application/tests/__init__.py", "line_no": "96"}
        result = match_file_location(input)
        self.assertEqual(expected, result)

    def test_match_file_location_when_no_match(self):
        input = "Traceback (most recent call last):"
        result = match_file_location(input)
        self.assertEqual({}, result)

    def test_match_error(self):
        input = "E   NameError: name 'asdfasdf' is not defined"
        expected = {"error": "NameError: name 'asdfasdf' is not defined"}
        result = match_error(input)
        self.assertEqual(expected, result)

    def test_match_error_when_no_match(self):
        input = "application/tests/test_dal.py:19: in <module>"
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

    def test_parse_fixture_error(self):
        input = [
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
        ]
        expected = [
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            "okbudget/tests/conftest.py:26 <You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories>",
        ]
        result = parse_fixture_error('', iter(input))
        self.assertEqual(expected, result)

    def test_parse_fixture_error_no_filename_found(self):
        input = [
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "This should not be possible but we will test it!",
        ]
        expected = [
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "This should not be possible but we will test it!",
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
            "============================================================================== test session starts ===============================================================================",
            "=================================== FAILURES ===================================",
            "_________________________________ test_myfunc __________________________________",
            "okbudget/tests/test_authentication.py:283: in test_myfunc",
            "assert False",
            "E   assert False",
            "None <assert False>",
            "=========================== 1 failed in 0.21 seconds ===========================",
        ]
        expected = [
            "============================================================================== test session starts ===============================================================================",
            "=================================== FAILURES ===================================",
            "_________________________________ test_myfunc __________________________________",
            "okbudget/tests/test_authentication.py:283: in test_myfunc",
            "assert False",
            "E   assert False",
            "okbudget/tests/test_authentication.py:283 <assert False>",
            "None <assert False>",
            "=========================== 1 failed in 0.21 seconds ===========================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_conftest_import_failure(self):
        input = [
            "============================================================================== test session starts ===============================================================================",
            "===================================================================================== ERRORS =====================================================================================",
            "_______________________________________________________________________________ ERROR collecting  ________________________________________________________________________________",
            "venv/lib/python3.4/site-packages/py/_path/common.py:332: in visit",
            "    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            "venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            "    for p in self.gen(subdir):",
            "venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            "    dirs = self.optsort([p for p in entries",
            "venv/lib/python3.4/site-packages/py/_path/common.py:368: in <listcomp>",
            "    if p.check(dir=1) and (rec is None or rec(p))])",
            "venv/lib/python3.4/site-packages/_pytest/main.py:632: in _recurse",
            "    ihook.pytest_collect_directory(path=path, parent=self)",
            "venv/lib/python3.4/site-packages/_pytest/main.py:162: in __getattr__",
            "    plugins = self.config._getmatchingplugins(self.fspath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:692: in _getmatchingplugins",
            "    self._conftest.getconftestmodules(fspath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:521: in getconftestmodules",
            "    mod = self.importconftest(conftestpath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:545: in importconftest",
            "    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            "E   _pytest.config.ConftestImportFailure: (local('/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py'), (<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>))",
            "============================================================================ 1 error in 0.56 seconds =============================================================================",
        ]
        expected = [
            "============================================================================== test session starts ===============================================================================",
            "===================================================================================== ERRORS =====================================================================================",
            "_______________________________________________________________________________ ERROR collecting  ________________________________________________________________________________",
            "venv/lib/python3.4/site-packages/py/_path/common.py:332: in visit",
            "    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            "venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            "    for p in self.gen(subdir):",
            "venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            "    dirs = self.optsort([p for p in entries",
            "venv/lib/python3.4/site-packages/py/_path/common.py:368: in <listcomp>",
            "    if p.check(dir=1) and (rec is None or rec(p))])",
            "venv/lib/python3.4/site-packages/_pytest/main.py:632: in _recurse",
            "    ihook.pytest_collect_directory(path=path, parent=self)",
            "venv/lib/python3.4/site-packages/_pytest/main.py:162: in __getattr__",
            "    plugins = self.config._getmatchingplugins(self.fspath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:692: in _getmatchingplugins",
            "    self._conftest.getconftestmodules(fspath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:521: in getconftestmodules",
            "    mod = self.importconftest(conftestpath)",
            "venv/lib/python3.4/site-packages/_pytest/config.py:545: in importconftest",
            "    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            "E   _pytest.config.ConftestImportFailure: (local('/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py'), (<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>))",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py:1 <<class 'ImportError'>, ImportError(\"No module named 'tata'\",), <traceback object at 0x104226f88>>",
            "============================================================================ 1 error in 0.56 seconds =============================================================================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_fixture_error(self):
        input = [
            "============================================================================== test session starts ===============================================================================",
            "platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: /Users/okcompute/Developer/Git/OkBudgetBackend, inifile: setup.cfg",
            "collected 48 items",
            "",
            "okbudget/tests/test_authentication.py ......",
            "okbudget/tests/test_dal.py ......................",
            "okbudget/tests/test_envelope.py ................",
            "okbudget/tests/test_fixtures.py E",
            "okbudget/tests/test_users.py ...",
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            "okbudget/tests/conftest.py:21:  def function_fixture()",
        ]
        expected = [
            "============================================================================== test session starts ===============================================================================",
            "platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: /Users/okcompute/Developer/Git/OkBudgetBackend, inifile: setup.cfg",
            "collected 48 items",
            "",
            "okbudget/tests/test_authentication.py ......",
            "okbudget/tests/test_dal.py ......................",
            "okbudget/tests/test_envelope.py ................",
            "okbudget/tests/test_fixtures.py E",
            "okbudget/tests/test_users.py ...",
            "===================================================================================== ERRORS =====================================================================================",
            "________________________________________________________________________ ERROR at setup of test_fixtures _________________________________________________________________________",
            "ScopeMismatch: You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories",
            "okbudget/tests/conftest.py:26:  def session_fixture(function_fixture)",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/conftest.py:26 <You tried to access the 'function' scoped fixture 'function_fixture' with a 'session' scoped request object, involved factories>",
            "okbudget/tests/conftest.py:21:  def function_fixture()",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_session_failure(self):
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
            "============================= test session starts =============================",
            "platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: F:\git\rdv_challenge, inifile: setup.cfg",
            "plugins: cache, cov, flake8",
            "collected 274 items",
            " ",
            "rdv_challenge\tests\test_configuration.py ...................................................................",
            "rdv_challenge\tests\bindings\prudp\test_prudp.py ...",
            "rdv_challenge\tests\bindings\rest\test_private.py ................................................",
            "rdv_challenge\tests\dal\test_challenge.py ...........................................................",
            "rdv_challenge\tests\dal\test_redis_interface.py ......F........",
            "rdv_challenge\tests\dal\test_stages.py .......",
            "rdv_challenge\tests\rvmc\test_rvmc.py ..",
            "rdv_challenge\tests\service\test_service.py .........................................................................",
            " ",
            "================================== FAILURES ===================================",
            "_____________ TestRedisInterface.test_challenges_progression_key ______________",
            " ",
            "self = <test_redis_interface.TestRedisInterface instance at 0x06CA4170>",
            "redis = <rdv_challenge.dal.redis_interface.RedisInterface object at 0x06AFB650>",
            " ",
            "    def test_challenges_progression_key(self, redis):",
            ">       assert 'Challenge:challenges:instances:progression:123' == str(",
            "            redis.get_challenge_progression_key(123),",
            "        )",
            "E       AttributeError: 'RedisInterface' object has no attribute 'get_challenge_progression_key'",
            " ",
            "rdv_challenge\tests\dal\test_redis_interface.py:45: AttributeError",
            "==================== 1 failed, 273 passed in 5.10 seconds =====================",
        ]
        expected = [
            "============================= test session starts =============================",
            "platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: F:\git\rdv_challenge, inifile: setup.cfg",
            "plugins: cache, cov, flake8",
            "collected 274 items",
            " ",
            "rdv_challenge\tests\test_configuration.py ...................................................................",
            "rdv_challenge\tests\bindings\prudp\test_prudp.py ...",
            "rdv_challenge\tests\bindings\rest\test_private.py ................................................",
            "rdv_challenge\tests\dal\test_challenge.py ...........................................................",
            "rdv_challenge\tests\dal\test_redis_interface.py ......F........",
            "rdv_challenge\tests\dal\test_stages.py .......",
            "rdv_challenge\tests\rvmc\test_rvmc.py ..",
            "rdv_challenge\tests\service\test_service.py .........................................................................",
            " ",
            "================================== FAILURES ===================================",
            "_____________ TestRedisInterface.test_challenges_progression_key ______________",
            " ",
            "self = <test_redis_interface.TestRedisInterface instance at 0x06CA4170>",
            "redis = <rdv_challenge.dal.redis_interface.RedisInterface object at 0x06AFB650>",
            " ",
            "    def test_challenges_progression_key(self, redis):",
            ">       assert 'Challenge:challenges:instances:progression:123' == str(",
            "            redis.get_challenge_progression_key(123),",
            "        )",
            "E       AttributeError: 'RedisInterface' object has no attribute 'get_challenge_progression_key'",
            " ",
            "rdv_challenge\tests\dal\test_redis_interface.py:45: AttributeError",
            "==================== 1 failed, 273 passed in 5.10 seconds =====================",
        ]
        result = parse(input)
        self.assertEqual(expected, result)

    def test_parse_with_conftest_type_error(self):
        input = [
            "============================= test session starts =============================",
            "platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: F:\git\rdv_challenge, inifile: setup.cfg",
            "plugins: cache, cov, flake8",
            "collected 0 items / 1 errors",
            " ",
            "=================================== ERRORS ====================================",
            "______________________________ ERROR collecting  ______________________________",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:332: in visit",
            "    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            "    for p in self.gen(subdir):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            "    for p in self.gen(subdir):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:368: in gen",
            "    if p.check(dir=1) and (rec is None or rec(p))])",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:632: in _recurse",
            "    ihook.pytest_collect_directory(path=path, parent=self)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:162: in __getattr__",
            "    plugins = self.config._getmatchingplugins(self.fspath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:692: in _getmatchingplugins",
            "    self._conftest.getconftestmodules(fspath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:521: in getconftestmodules",
            "    mod = self.importconftest(conftestpath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:545: in importconftest",
            "    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            "E   ConftestImportFailure: (local('F:\\git\\rdv_challenge\\rdv_challenge\\tests\\service\\conftest.py'), (<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>))",
            "=========================== 1 error in 1.69 seconds ===========================",
        ]
        expected = [
            "============================= test session starts =============================",
            "platform win32 -- Python 2.7.8 -- py-1.4.30 -- pytest-2.7.2",
            "rootdir: F:\git\rdv_challenge, inifile: setup.cfg",
            "plugins: cache, cov, flake8",
            "collected 0 items / 1 errors",
            " ",
            "=================================== ERRORS ====================================",
            "______________________________ ERROR collecting  ______________________________",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:332: in visit",
            "    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            "    for p in self.gen(subdir):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:378: in gen",
            "    for p in self.gen(subdir):",
            ".tox\rdv3.0.5\lib\site-packages\py\_path\common.py:368: in gen",
            "    if p.check(dir=1) and (rec is None or rec(p))])",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:632: in _recurse",
            "    ihook.pytest_collect_directory(path=path, parent=self)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\main.py:162: in __getattr__",
            "    plugins = self.config._getmatchingplugins(self.fspath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:692: in _getmatchingplugins",
            "    self._conftest.getconftestmodules(fspath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:521: in getconftestmodules",
            "    mod = self.importconftest(conftestpath)",
            ".tox\rdv3.0.5\lib\site-packages\_pytest\config.py:545: in importconftest",
            "    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            "E   ConftestImportFailure: (local('F:\\git\\rdv_challenge\\rdv_challenge\\tests\\service\\conftest.py'), (<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>))",
            "F:\\git\\rdv_challenge\\rdv_challenge\\tests\\service\\conftest.py:1 <<type 'exceptions.TypeError'>, TypeError(\"fixture() got an unexpected keyword argument 'score'\",), <traceback object at 0x060958A0>>",
            "=========================== 1 error in 1.69 seconds ===========================",
        ]
        self.maxDiff = None
        result = parse(input)
        self.assertEqual(expected, result)
