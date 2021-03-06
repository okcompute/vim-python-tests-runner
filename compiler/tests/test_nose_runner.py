#!/usr/bin/env python
# encoding: utf-8

import unittest

from runners.nose import (
    parse,
)


class TestNoseRunner(unittest.TestCase):

    """Test case for runners.nose.py module"""

    def test_parse_lines(self):
        input = [
            "FF...E..F.........................................",
            "======================================================================",
            "ERROR: Test authentication handler cannot be accessed if user sign in and",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 240, in test_signout",
            "    caca",
            "nose.proxy.NameError: name 'caca' is not defined",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.general: WARNING: tornado.autoreload started more than once in the same process",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.43ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 2.72ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.18ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: test_false (okbudget.tests.test_authentication.TestAuthentication)",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 276, in test_false",
            "    assert False",
            "nose.proxy.AssertionError:",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 3.07ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 3.15ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.16ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: test_false2 (okbudget.tests.test_authentication.TestAuthentication)",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 279, in test_false2",
            "    assert False",
            "nose.proxy.AssertionError:",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.general: WARNING: tornado.autoreload started more than once in the same process",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.33ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 2.27ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.20ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: okbudget.tests.test_authentication.test_myfunc",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/nose/case.py\", line 198, in runTest",
            "    self.test(*self.arg)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 283, in test_myfunc",
            "    assert False",
            "AssertionError",
            "",
            "----------------------------------------------------------------------",
            "Ran 50 tests in 1.684s",
            "",
            "FAILED (errors=1, failures=3)",
        ]
        expected = [
            "FF...E..F.........................................",
            "======================================================================",
            "ERROR: Test authentication handler cannot be accessed if user sign in and",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 240, in test_signout",
            "    caca",
            "nose.proxy.NameError: name 'caca' is not defined",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py:240 <nose.proxy.NameError: name 'caca' is not defined>",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.general: WARNING: tornado.autoreload started more than once in the same process",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.43ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 2.72ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.18ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: test_false (okbudget.tests.test_authentication.TestAuthentication)",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 276, in test_false",
            "    assert False",
            "nose.proxy.AssertionError:",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py:276 <nose.proxy.AssertionError:>",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 3.07ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 3.15ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.16ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: test_false2 (okbudget.tests.test_authentication.TestAuthentication)",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/testing.py\", line 118, in __call__",
            "    result = self.orig_method(*args, **kwargs)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 279, in test_false2",
            "    assert False",
            "nose.proxy.AssertionError:",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py:279 <nose.proxy.AssertionError:>",
            "-------------------- >> begin captured logging << --------------------",
            "tornado.general: WARNING: tornado.autoreload started more than once in the same process",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.33ms",
            "tornado.access: INFO: 200 POST /api/signup (127.0.0.1) 2.27ms",
            "tornado.access: INFO: 200 PUT /private/reset_db (127.0.0.1) 2.20ms",
            "--------------------- >> end captured logging << ---------------------",
            "",
            "======================================================================",
            "FAIL: okbudget.tests.test_authentication.test_myfunc",
            "----------------------------------------------------------------------",
            "Traceback (most recent call last):",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/nose/case.py\", line 198, in runTest",
            "    self.test(*self.arg)",
            "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py\", line 283, in test_myfunc",
            "    assert False",
            "AssertionError",
            "/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_authentication.py:283 <AssertionError>",
            "",
            "----------------------------------------------------------------------",
            "Ran 50 tests in 1.684s",
            "",
            "FAILED (errors=1, failures=3)",
        ]
        result = parse(input)
        self.assertEqual(expected, result)
