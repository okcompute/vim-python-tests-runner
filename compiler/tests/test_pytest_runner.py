#!/usr/bin/env python
# encoding: utf-8

from runners.pytest import (
    group_lines,
    match_conftest_error,
    match_error,
    match_file_location,
    match_fixture_not_found_error,
    match_fixture_not_found_file_location,
    match_fixture_scope_mismatch,
    parse,
    parse_conftest_error,
    parse_error,
    parse_errors,
    parse_failure,
    parse_failures,
    parse_fixture_error,
    parse_sections,
    parse_session,
    parse_session_failure,
    parse_test_error,
)


class TestPytestRunner():

    """Test case for runners.pytest.py module"""

    def test_match_fixture_scope_mismatch(self):
        input_ = r"ScopeMismatch: Invalid something"
        expected = r"Invalid something"
        result = match_fixture_scope_mismatch(input_)
        assert expected == result

    def test_match_file_location(self):
        input_ = r"application/tests/__init__.py:96: in create_user"
        expected = {
            "file_path": "application/tests/__init__.py",
            "line_no": "96",
        }
        result = match_file_location(input_)
        assert expected == result

    def test_match_file_location_windows(self):
        input_ = r"my_package\tests\test_something.py:1090: in "
        "test_add_something"
        expected = {
            "file_path": r"my_package\tests\test_something.py",
            "line_no": "1090",
        }
        result = match_file_location(input_)
        assert expected == result

    def test_match_file_location_when_no_match(self):
        input_ = r"   assert goals == {'goal_2': {'contexts': [], "
        "'contribution': 2.0}}"
        result = match_file_location(input_)
        assert {} == result

    def test_match_error(self):
        input_ = r"E   NameError: name 'asdfasdf' is not defined"
        expected = "NameError: name 'asdfasdf' is not defined"
        result = match_error(input_)
        assert expected == result

    def test_match_error_when_no_match(self):
        input_ = r"application/tests/test_dal.py:19: in <module>"
        result = match_error(input_)
        assert result is None

    def test_match_conftest_error(self):
        input_ = "E   _pytest.config.ConftestImportFailure: " \
            "(local('/test/conftest.py'), (<class 'ImportError'>, " \
            "ImportError(\"No module named 'unknown'\",), <traceback object " \
            "at 0x104226f88>))"
        expected = {
            'file_path': "/test/conftest.py",
            'error': "<class 'ImportError'>, ImportError(\"No module named "
            "'unknown'\",), <traceback object at 0x104226f88>",
        }
        result = match_conftest_error(input_)
        assert result == expected

    def test_match_fixture_not_found_file_location(self):
        input_ = r"file F:\my_package\tests\test_something.py, line 1245"
        expected = {
            "file_path": r"F:\my_package\tests\test_something.py",
            "line_no": "1245",
        }
        result = match_fixture_not_found_file_location(input_)
        assert expected == result

    def test_match_fixture_not_found_error(self):
        input_ = "        fixture 'populate_database' not found"
        expected = {
            'error': "fixture 'populate_database' not found",
        }
        result = match_fixture_not_found_error(input_)
        assert result == expected

    def test_parse_fixture_error_when_fixture_not_found(self):
        input_ = [
            r"___ ERROR at setup of TestSomething.test_something ___",
            r"file F:\git\my_package\tests\test_something.py, l"
            "ine 1245",
            r"      def test_something(",
            r"        fixture 'a_fixture' not found",
            r"        available fixtures: pytestconfig, capfd, capsys",
            r"        use 'py.test --fixtures [testpath]' for help on them.",
        ]
        expected = [
            r"___ ERROR at setup of TestSomething.test_something ___",
            r"file F:\git\my_package\tests\test_something.py, l"
            "ine 1245",
            r"      def test_something(",
            r"        fixture 'a_fixture' not found",
            r"F:\git\my_package\tests\test_something.py:1245 <fixture "
            "'a_fixture' not found>",
            r"        available fixtures: pytestconfig, capfd, capsys",
            r"        use 'py.test --fixtures [testpath]' for help on them.",
        ]
        result = parse_fixture_error(r'F:\git\my_package\tests', input_)
        assert expected == result

    def test_parse_fixture_error_with_scope_mistmatch(self):
        input_ = [
            r"________________________________________________________________"
            "________ ERROR at setup of test_fixtures ________________________"
            "_________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture "
            "'function_fixture' with a 'session' scoped request object, "
            "involved factories",
            r"tests/conftest.py:26:  def session_fixture"
            "(function_fixture)",
        ]
        expected = [
            r"________________________________________________________________"
            "________ ERROR at setup of test_fixtures ________________________"
            "_________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped fixture "
            "'function_fixture' with a 'session' scoped request object, "
            "involved factories",
            r"tests/conftest.py:26:  def session_fixture"
            "(function_fixture)",
            r"tests/conftest.py:26 <You tried to access the "
            "'function' scoped fixture 'function_fixture' with a 'session' "
            "scoped request object, involved factories>",
        ]
        result = parse_fixture_error('', input_)
        assert expected == result

    def test_parse_fixture_error_no_filename_found(self):
        input_ = [
            r"================================================================",
            "===================== ERRORS ====================================",
            "=================================================",
            r"________________________________________________________________",
            "________ ERROR at setup of test_fixtures ________________________",
            "_________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped ",
            "fixture 'function_fixture' with a 'session' scoped request object"
            ", involved factories",
            r"This should not be possible but we will test it!",
        ]
        expected = [
            r"================================================================",
            "===================== ERRORS ====================================",
            "=================================================",
            r"________________________________________________________________",
            "________ ERROR at setup of test_fixtures ________________________",
            "_________________________________________________",
            r"ScopeMismatch: You tried to access the 'function' scoped ",
            "fixture 'function_fixture' with a 'session' scoped request object"
            ", involved factories",
            r"This should not be possible but we will test it!",
        ]
        result = parse_fixture_error(r'c:\root', input_)
        assert expected == result

    def test_parse_conftest_error(self):
        input_ = [
            r"________________________________________________________________"
            "_______________ ERROR collecting  _______________________________"
            "_________________________________________________",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:332: in "
            "visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            r"    dirs = self.optsort([p for p in entries",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:368: in "
            "<listcomp>",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:632: in "
            "_recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:162: in "
            "__getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:692: in "
            "_getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:521: in "
            "getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:545: in "
            "importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   _pytest.config.ConftestImportFailure: "
            "(local('/Users/user/project/tests/conftest.py'), "
            "(<class 'ImportError'>, ImportError(\"No module named "
            "'unknown'\",), <traceback object at 0x104226f88>))",
        ]
        expected = [
            r"________________________________________________________________"
            "_______________ ERROR collecting  _______________________________"
            "_________________________________________________",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:332: in "
            "visit",
            r"    for x in Visitor(fil, rec, ignore, bf, sort).gen(self):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:378: in gen",
            r"    for p in self.gen(subdir):",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:367: in gen",
            r"    dirs = self.optsort([p for p in entries",
            r"venv/lib/python3.4/site-packages/py/_path/common.py:368: in "
            "<listcomp>",
            r"    if p.check(dir=1) and (rec is None or rec(p))])",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:632: in "
            "_recurse",
            r"    ihook.pytest_collect_directory(path=path, parent=self)",
            r"venv/lib/python3.4/site-packages/_pytest/main.py:162: in "
            "__getattr__",
            r"    plugins = self.config._getmatchingplugins(self.fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:692: in "
            "_getmatchingplugins",
            r"    self._conftest.getconftestmodules(fspath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:521: in "
            "getconftestmodules",
            r"    mod = self.importconftest(conftestpath)",
            r"venv/lib/python3.4/site-packages/_pytest/config.py:545: in "
            "importconftest",
            r"    raise ConftestImportFailure(conftestpath, sys.exc_info())",
            r"E   _pytest.config.ConftestImportFailure: "
            "(local('/Users/user/project/tests/conftest.py'), "
            "(<class 'ImportError'>, ImportError(\"No module named "
            "'unknown'\",), <traceback object at 0x104226f88>))",
            r"/Users/user/project/tests/conftest.py:1 <<class 'ImportError'>, "
            "ImportError(\"No module named 'unknown'\",), "
            "<traceback object at 0x104226f88>>",
        ]
        result = parse_conftest_error(input_)
        assert expected == result

    def test_parse_test_error(self):
        input_ = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
        ]
        expected = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "tests/test_something.py:19 <NameError: name 'asdfasdf' is not "
            "defined>"
        ]
        result = parse_test_error(input_)
        assert expected == result

    def test_parse_error(self):
        input_ = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
        ]
        expected = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "tests/test_something.py:19 <NameError: name 'asdfasdf' is not "
            "defined>"
        ]
        result = parse_error(r'C:\root', input_)
        assert expected == result

    def test_parse_error_nothing_found(self):
        input_ = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "This is not understood by the parser!",
        ]
        expected = [
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "This is not understood by the parser!",
            "Unknown:Unknown <An error was found but could not be parsed. "
            "This is probably a missing error pattern. Please post an issue "
            "on GitHub.>",
        ]
        result = parse_error(r'C:\root', input_)
        assert expected == result

    def test_parse_failure(self):
        input_ = [
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"tests/test_assertion.py:283: in test_assert_false",
            r"assert False",
            r"E   assert False",
        ]
        expected = [
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"tests/test_assertion.py:283: in test_assert_false",
            r"assert False",
            r"E   assert False",
            r"tests/test_assertion.py:283 <assert False>",
        ]
        result = parse_failure(input_)
        assert expected == result

    def test_parse_failure_nothing_found(self):
        input_ = [
            r"_________________________________ test_myfunc __________________",
            "________________",
            "_____________________________________________",
            "This is not understood by the parser!",
        ]
        expected = [
            r"_________________________________ test_myfunc __________________",
            "________________",
            "_____________________________________________",
            "This is not understood by the parser!",
            "Unknown:Unknown <An error was found but could not be parsed. "
            "This is probably a missing error pattern. Please post an issue "
            "on GitHub.>",
        ]
        result = parse_failure(input_)
        assert expected == result

    def test_parse_failure_with_repeated_filenames(self):
        input_ = [
            r"self = <application.tests.test_authentication.",
            "TestAuthentication <testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestAuthentication, self).setUp()",
            r"",
            r"application/tests/test_authentication.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ",
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ ",
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", ",
            "\"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
        ]
        expected = (
            input_ + [
                "application/tests/__init__.py:96 <AssertionError: 500 != 200>"
            ]
        )
        result = parse_failure(input_)
        assert expected == result

    def test_parse_session_failure(self):
        input_ = [
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "513, in getconftestmodules",
            "    return self._path2confmods[path]",
            "KeyError: local('/tests')",
            "",
            "During handling of the above exception, another exception ",
            "occurred:",
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "537, in importconftest",
            "    return self._conftestpath2mod[conftestpath]",
            "KeyError: local('/tests/conftest.py')",
            "",
            "During handling of the above exception, another exception ",
            "occurred:",
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "543, in importconftest",
            "    mod = conftestpath.pyimport()",
            "  File \"/venv/lib/python3.4/site-packages/py/_path/local.py\", ",
            "line 650, in pyimport",
            "    __import__(modname)",
            "  File \"/tests/conftest.py\", line 1, in <module>",
            "    adfasfdasdfasd",
            "NameError: name 'adfasfdasdfasd' is not defined",
            "ERROR: could not load /tests/conftest.py",
        ]
        expected = [
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "513, in getconftestmodules",
            "    return self._path2confmods[path]",
            "KeyError: local('/tests')",
            "",
            "During handling of the above exception, another exception ",
            "occurred:",
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "537, in importconftest",
            "    return self._conftestpath2mod[conftestpath]",
            "KeyError: local('/tests/conftest.py')",
            "",
            "During handling of the above exception, another exception ",
            "occurred:",
            "Traceback (most recent call last):",
            "  File \"/venv/lib/python3.4/site-packages//config.py\", line ",
            "543, in importconftest",
            "    mod = conftestpath.pyimport()",
            "  File \"/venv/lib/python3.4/site-packages/py/_path/local.py\", ",
            "line 650, in pyimport",
            "    __import__(modname)",
            "  File \"/tests/conftest.py\", line 1, in <module>",
            "    adfasfdasdfasd",
            "NameError: name 'adfasfdasdfasd' is not defined",
            "/tests/conftest.py:1 <NameError: name 'adfasfdasdfasd' is not "
            "defined>",
            "ERROR: could not load /tests/conftest.py",
        ]
        result = parse_session_failure(input_)
        assert expected == list(result)

    def test_group_lines(self):
        input_ = [
            r"________________________________________________________________"
            "__ ERROR collecting tests/test_one.py _______________"
            "____________________________________________________",
            r"/tests/test_something.py:19: in <module>",
            r"    unknown",
            r"E   NameError: name 'unknown' is not defined",
            r"________________________________________________________________"
            "__ ERROR collecting tests/test_two.py _______________"
            "____________________________________________________",
            r"/tests/test_something.py:19: in <module>",
            r"    unknown",
            r"E   NameError: name 'unknown' is not defined",
        ]
        expected = [
            [
                r"____________________________________________________________"
                "______ ERROR collecting tests/test_one.py _____________"
                "______________________________________________________",
                r"/tests/test_something.py:19: in <module>",
                r"    unknown",
                r"E   NameError: name 'unknown' is not defined",
            ],
            [
                r"____________________________________________________________"
                "______ ERROR collecting tests/test_two.py ___________________"
                "________________________________________________",
                r"/tests/test_something.py:19: in <module>",
                r"    unknown",
                r"E   NameError: name 'unknown' is not defined",
            ],
        ]
        result = group_lines(input_, r"_{2,} .* _{2,}")
        assert expected == result

    def test_parse_sections(self):
        input_ = [
            r'==============================================================='
            '=============== test session starts ============================='
            '==================================================',
            'session lines',
            r'================================================================'
            '===================== ERRORS ===================================='
            '=================================================',
            "_ ERROR collecting testa _"
            'testa line1',
            'testa line2',
            "_ ERROR collecting testb _"
            'testb line1',
            'testb line2',
            r'___ ERROR at setup of test1  ____',
            'test1 line1',
            'test1 line2',
            r'___ ERROR at setup of test2  ____',
            'test2 line1',
            'test2 line2',
            r'___ ERROR at setup of test3  ____',
            'test3 line1',
            'test3 line2',
            r'================================================================'
            '==================== FAILURES ==================================='
            '=================================================',
            r'___ test4  ____',
            'test4 line1',
            'test4 line2',
            r'___ test5  ____',
            'test4 line1',
            'test4 line2',
        ]
        expected = {
            'session': [
                r'============================================================'
                '================== test session starts ======================'
                '=========================================================',
                'session lines',
            ],
            'errors': [
                r'============================================================'
                '========================= ERRORS ============================'
                '========'
                '=================================================',
                "_ ERROR collecting testa _"
                'testa line1',
                'testa line2',
                "_ ERROR collecting testb _"
                'testb line1',
                'testb line2',
                r'___ ERROR at setup of test1  ____',
                'test1 line1',
                'test1 line2',
                r'___ ERROR at setup of test2  ____',
                'test2 line1',
                'test2 line2',
                r'___ ERROR at setup of test3  ____',
                'test3 line1',
                'test3 line2',
            ],
            'failures': [
                r'============================================================'
                '======================== FAILURES ==========================='
                '=========================================================',
                r'___ test4  ____',
                'test4 line1',
                'test4 line2',
                r'___ test5  ____',
                'test4 line1',
                'test4 line2',
            ]
        }
        result = parse_sections(input_)
        assert expected == result

    def test_parse_sections_no_failures(self):
        input_ = [
            r'==============================================================='
            '=============== test session starts ============================='
            '==================================================',
            'session lines',
            r'================================================================'
            '===================== ERRORS ===================================='
            '=================================================',
            "_ ERROR collecting testa _"
            'testa line1',
            'testa line2',
            "_ ERROR collecting testb _"
            'testb line1',
            'testb line2',
            r'___ ERROR at setup of test1  ____',
            'test1 line1',
            'test1 line2',
            r'___ ERROR at setup of test2  ____',
            'test2 line1',
            'test2 line2',
            r'___ ERROR at setup of test3  ____',
            'test3 line1',
            'test3 line2',
        ]
        expected = {
            'session': [
                r'============================================================'
                '================== test session starts ======================'
                '=========================================================',
                'session lines',
            ],
            'errors': [
                r'============================================================'
                '========================= ERRORS ============================'
                '=========================================================',
                "_ ERROR collecting testa _"
                'testa line1',
                'testa line2',
                "_ ERROR collecting testb _"
                'testb line1',
                'testb line2',
                r'___ ERROR at setup of test1  ____',
                'test1 line1',
                'test1 line2',
                r'___ ERROR at setup of test2  ____',
                'test2 line1',
                'test2 line2',
                r'___ ERROR at setup of test3  ____',
                'test3 line1',
                'test3 line2',
            ],
        }
        result = parse_sections(input_)
        assert expected == result

    def test_parse_sections_no_errors(self):
        input_ = [
            r'==============================================================='
            '=============== test session starts ============================='
            '==================================================',
            'session lines',
            r'================================================================'
            '==================== FAILURES ==================================='
            '=================================================',
            r'___ test4  ____',
            'test4 line1',
            'test4 line2',
            r'___ test5  ____',
            'test4 line1',
            'test4 line2',
        ]
        expected = {
            'session': [
                r'============================================================'
                '================== test session starts ======================'
                '=========================================================',
                'session lines',
            ],
            'failures': [
                r'============================================================'
                '======================== FAILURES ==========================='
                '=========================================================',
                r'___ test4  ____',
                'test4 line1',
                'test4 line2',
                r'___ test5  ____',
                'test4 line1',
                'test4 line2',
            ]
        }
        result = parse_sections(input_)
        assert expected == result

    def test_parse_errors(self):
        input_ = [
            r"================================================================"
            "==================== ERRORS ==================================="
            "=================================================",
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
        ]
        expected = [
            r"================================================================"
            "==================== ERRORS ==================================="
            "=================================================",
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "tests/test_something.py:19 <NameError: name 'asdfasdf' is not "
            "defined>",
            "_________________________________________________________________"
            "_ ERROR collecting tests/test_something.py ______________________"
            "_____________________________________________",
            "tests/test_something.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
            "tests/test_something.py:19 <NameError: name 'asdfasdf' is not "
            "defined>",
        ]
        result = parse_errors('/user/tests/', input_)
        assert expected == result

    def test_parse_failures(self):
        input_ = [
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"________________________________________________________________"
            "_________ TestSystem.test_false _________________________"
            "_________________________________________________",
            r"",
            r"self = <tests.TestSystem "
            "testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestSystem, self).setUp()",
            r"",
            r"application/tests/test_system.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", "
            "\"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
            r"----------------------------------------------------------------"
            "-------------- Captured stderr call -----------------------------"
            "-------------------------------------------------",
            r"ERROR:tornado.application:Uncaught exception POST /api/signup "
            "(127.0.0.1)",
            r"Traceback (most recent call last):",
            r"  File \"/venv/lib/python3.4/site-packages/tornado/w"
            "eb.py\", line 1332, in _execute",
            r"    result = method(*self.path_args, **self.path_kwargs)",
            r"  File \"/application/rest/__init__.py\", line 135, "
            "in wrapper",
            r"    return method(self, *args, **kwargs)",
            r"  File \"/application/rest/__init__.py\", line 105, "
            "in request_wrapper",
            r"    response = request(self, arguments, *args, **kwargs)",
            r"  File \"/application/rest/authentication.py\", line "
            "105, in post",
            r"    body['email']",
            r"  File \"/application/dal.py\", line 257, in "
            "create_user",
            r"    return self._convert_to_user(user)",
            r"  File \"/application/dal.py\", line 236, in "
            "_convert_to_user",
            r"    an_error",
            r"NameError: name 'an_error' is not defined",
            r"ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"tests/test_assertion.py:283: in test_assert_false",
            r"assert False",
            r"E   assert False",

        ]
        expected = [
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"________________________________________________________________"
            "_________ TestSystem.test_false _________________________"
            "_________________________________________________",
            r"",
            r"self = <tests.TestSystem "
            "testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestSystem, self).setUp()",
            r"",
            r"application/tests/test_system.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", "
            "\"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
            r"application/tests/__init__.py:96 <AssertionError: 500 != 200>",
            r"----------------------------------------------------------------"
            "-------------- Captured stderr call -----------------------------"
            "-------------------------------------------------",
            r"ERROR:tornado.application:Uncaught exception POST /api/signup "
            "(127.0.0.1)",
            r"Traceback (most recent call last):",
            r"  File \"/venv/lib/python3.4/site-packages/tornado/w"
            "eb.py\", line 1332, in _execute",
            r"    result = method(*self.path_args, **self.path_kwargs)",
            r"  File \"/application/rest/__init__.py\", line 135, "
            "in wrapper",
            r"    return method(self, *args, **kwargs)",
            r"  File \"/application/rest/__init__.py\", line 105, "
            "in request_wrapper",
            r"    response = request(self, arguments, *args, **kwargs)",
            r"  File \"/application/rest/authentication.py\", line "
            "105, in post",
            r"    body['email']",
            r"  File \"/application/dal.py\", line 257, in "
            "create_user",
            r"    return self._convert_to_user(user)",
            r"  File \"/application/dal.py\", line 236, in "
            "_convert_to_user",
            r"    an_error",
            r"NameError: name 'an_error' is not defined",
            r"ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"tests/test_assertion.py:283: in test_assert_false",
            r"assert False",
            r"E   assert False",
            r"tests/test_assertion.py:283 <assert False>",
        ]
        result = parse_failures(input_)
        assert expected == result

    def test_parse_session(self):
        input_ = [
            r'==============================================================='
            '=============== test session starts ============================='
            '==================================================',
            r'platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2',
            r'rootdir: /Tests, inifile: setup.cfg',
            r'collected 47 items / 1 errors',
            r'',
            r'tests/test_something.py F.',
            r'',
            r'================================================================'
            '===================== ERRORS ===================================='
            '=================================================',
            r'_______________________________________________________________'
            'ERROR collecting tests/test_something.py '
            '________________________________________________________________',
            r'venv/lib/python3.4/site-packages/_pytest/python.py:488: in '
            '_importtestmodule',
            r'    mod = self.fspath.pyimport(ensuresyspath=True)',
            r'venv/lib/python3.4/site-packages/py/_path/local.py:650: in '
            'pyimport',
            r'    __import__(modname)',
            r'E     File "/tests/test_something.py", line 2',
            r'E       print error',
            r'E                 ^',
            r'E   SyntaxError: Missing parentheses in call to \'print\'',
            r'================================================================'
            '==================== FAILURES ==================================='
            '=================================================',
            r'________________________________________________________________'
            '_________ TestProject.test_this _________________________________'
            '________________________________________',
            r'',
        ]
        result = parse_session(input_)
        assert '/Tests' == result

    def test_parse(self):
        input_ = [
            r"================================================================"
            "============== test session starts =============================="
            "=================================================",
            r'platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2',
            r'rootdir: /Users/user/project, inifile: setup.cfg',
            r'collected 47 items / 1 errors',
            r'',
            r'tests/test_something.py F.',
            r'',
            r"================================================================"
            "===================== ERRORS ===================================="
            "=================================================",
            r"________________________________________________________________"
            "__ ERROR collecting tests/test_something.py _______________"
            "____________________________________________________",
            r"/tests/test_something.py:19: in <module>",
            r"    unknown",
            r"E   NameError: name 'unknown' is not defined",
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"________________________________________________________________"
            "_________ TestSystem.test_false _________________________"
            "_________________________________________________",
            r"",
            r"self = <tests.TestSystem "
            "testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestSystem, self).setUp()",
            r"",
            r"application/tests/test_system.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", "
            "\"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
            r"----------------------------------------------------------------"
            "-------------- Captured stderr call -----------------------------"
            "-------------------------------------------------",
            r"ERROR:tornado.application:Uncaught exception POST /api/signup "
            "(127.0.0.1)",
            r"Traceback (most recent call last):",
            r"  File \"/venv/lib/python3.4/site-packages/tornado/w"
            "eb.py\", line 1332, in _execute",
            r"    result = method(*self.path_args, **self.path_kwargs)",
            r"  File \"/application/rest/__init__.py\", line 135, "
            "in wrapper",
            r"    return method(self, *args, **kwargs)",
            r"  File \"/application/rest/__init__.py\", line 105, "
            "in request_wrapper",
            r"    response = request(self, arguments, *args, **kwargs)",
            r"  File \"/application/rest/authentication.py\", line "
            "105, in post",
            r"    body['email']",
            r"  File \"/application/dal.py\", line 257, in "
            "create_user",
            r"    return self._convert_to_user(user)",
            r"  File \"/application/dal.py\", line 236, in "
            "_convert_to_user",
            r"    blarg",
            r"NameError: name 'blarg' is not defined",
            r"ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",

        ]
        expected = [
            r"================================================================"
            "============== test session starts =============================="
            "=================================================",
            r'platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2',
            r'rootdir: /Users/user/project, inifile: setup.cfg',
            r'collected 47 items / 1 errors',
            r'',
            r'tests/test_something.py F.',
            r'',
            r"================================================================"
            "===================== ERRORS ===================================="
            "=================================================",
            r"________________________________________________________________"
            "__ ERROR collecting tests/test_something.py _______________"
            "____________________________________________________",
            r"/tests/test_something.py:19: in <module>",
            r"    unknown",
            r"E   NameError: name 'unknown' is not defined",
            r"/tests/test_something.py:19 <NameError: name 'unknown' is not "
            "defined>",
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"________________________________________________________________"
            "_________ TestSystem.test_false _________________________"
            "_________________________________________________",
            r"",
            r"self = <tests.TestSystem "
            "testMethod=test_false>",
            r"",
            r"    def setUp(self):",
            r">       super(TestSystem, self).setUp()",
            r"",
            r"application/tests/test_system.py:56:",
            r"_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            r"application/tests/__init__.py:46: in setUp",
            r"    self.user = self.create_user(\"test\", \"test\", "
            "\"test@test.com\")",
            r"application/tests/__init__.py:96: in create_user",
            r"    self.assertEqual(response.code, 200)",
            r"E   AssertionError: 500 != 200",
            r"application/tests/__init__.py:96 <AssertionError: 500 != 200>",
            r"----------------------------------------------------------------"
            "-------------- Captured stderr call -----------------------------"
            "-------------------------------------------------",
            r"ERROR:tornado.application:Uncaught exception POST /api/signup "
            "(127.0.0.1)",
            r"Traceback (most recent call last):",
            r"  File \"/venv/lib/python3.4/site-packages/tornado/w"
            "eb.py\", line 1332, in _execute",
            r"    result = method(*self.path_args, **self.path_kwargs)",
            r"  File \"/application/rest/__init__.py\", line 135, "
            "in wrapper",
            r"    return method(self, *args, **kwargs)",
            r"  File \"/application/rest/__init__.py\", line 105, "
            "in request_wrapper",
            r"    response = request(self, arguments, *args, **kwargs)",
            r"  File \"/application/rest/authentication.py\", line "
            "105, in post",
            r"    body['email']",
            r"  File \"/application/dal.py\", line 257, in "
            "create_user",
            r"    return self._convert_to_user(user)",
            r"  File \"/application/dal.py\", line 236, in "
            "_convert_to_user",
            r"    blarg",
            r"NameError: name 'blarg' is not defined",
            r"ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
        ]
        result = parse(input_)
        assert expected == result

    def test_parse_without_errors(self):
        input_ = [
            r"================================================================"
            "============== test session starts =============================="
            "=================================================",
            r'platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2',
            r'rootdir: /Users/user/project, inifile: setup.cfg',
            r'collected 47 items / 1 errors',
            r'',
            r'tests/test_something.py F.',
            r'',
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"/tests/test_false.py:283: in test_myfunc",
            r"assert False",
            r"E   assert False",
            r"=========================== 1 failed in 0.21 seconds ===========",

        ]
        expected = [
            r"================================================================"
            "============== test session starts =============================="
            "=================================================",
            r'platform darwin -- Python 3.4.2 -- py-1.4.30 -- pytest-2.7.2',
            r'rootdir: /Users/user/project, inifile: setup.cfg',
            r'collected 47 items / 1 errors',
            r'',
            r'tests/test_something.py F.',
            r'',
            r"================================================================"
            "==================== FAILURES ==================================="
            "=================================================",
            r"_________________________________ test_myfunc __________________",
            "________________",
            r"/tests/test_false.py:283: in test_myfunc",
            r"assert False",
            r"E   assert False",
            r"/tests/test_false.py:283 <assert False>",
            r"=========================== 1 failed in 0.21 seconds ===========",
        ]
        result = parse(input_)
        assert expected == result

    def test_parse_with_session_failure(self):
        input_ = [
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 513, '
            'in getconftestmodules',
            r'    return self._path2confmods[path]',
            r'KeyError: local(\'/tests\')',
            r'',
            r'During handling of the above exception, another exception '
            'occurred:',
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 537, '
            'in importconftest',
            r'    return self._conftestpath2mod[conftestpath]',
            r'KeyError: local(\'/tests/conftest.py\')',
            r'',
            r'During handling of the above exception, another exception '
            'occurred:',
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 543, '
            'in importconftest',
            r'    mod = conftestpath.pyimport()',
            r'  File "/venv/lib/python3.4/site-packages/py/_path/local.py", '
            'line 650, in pyimport',
            r'    __import__(modname)',
            r'  File "/tests/conftest.py", line 1, in <module>',
            r'    adfasfdasdfasd',
            r'NameError: name \'adfasfdasdfasd\' is not defined',
            r'ERROR: could not load /tests/conftest.py',
        ]
        expected = [
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 513, '
            'in getconftestmodules',
            r'    return self._path2confmods[path]',
            r'KeyError: local(\'/tests\')',
            r'',
            r'During handling of the above exception, another exception '
            'occurred:',
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 537, '
            'in importconftest',
            r'    return self._conftestpath2mod[conftestpath]',
            r'KeyError: local(\'/tests/conftest.py\')',
            r'',
            r'During handling of the above exception, another exception '
            'occurred:',
            r'Traceback (most recent call last):',
            r'  File "/venv/lib/python3.4/site-packages//config.py", line 543, '
            'in importconftest',
            r'    mod = conftestpath.pyimport()',
            r'  File "/venv/lib/python3.4/site-packages/py/_path/local.py", '
            'line 650, in pyimport',
            r'    __import__(modname)',
            r'  File "/tests/conftest.py", line 1, in <module>',
            r'    adfasfdasdfasd',
            r'NameError: name \'adfasfdasdfasd\' is not defined',
            r'/tests/conftest.py:1 <NameError: name \'adfasfdasdfasd\' is not '
            'defined>',
            r'ERROR: could not load /tests/conftest.py',
        ]
        result = parse(input_)
        assert expected == result

    def test_parse_empty_lines(self):
        assert parse([]) == []
