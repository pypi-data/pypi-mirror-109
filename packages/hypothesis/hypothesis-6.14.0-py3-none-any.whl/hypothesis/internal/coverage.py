# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2021 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

import json
import os
import sys
from contextlib import contextmanager
from typing import Dict, Set, Tuple

from hypothesis.internal.reflection import proxies

"""
This module implements a custom coverage system that records conditions and
then validates that every condition has been seen to be both True and False
during the execution of our tests.

The only thing we use it for at present is our argument validation functions,
where we assert that every validation function has been seen to both pass and
fail in the course of testing.

When not running with a magic environment variable set, this module disables
itself and has essentially no overhead.
"""

pretty_file_name_cache: Dict[str, str] = {}


def pretty_file_name(f):
    try:
        return pretty_file_name_cache[f]
    except KeyError:
        pass

    parts = f.split(os.path.sep)
    if "hypothesis" in parts:  # pragma: no branch
        parts = parts[-parts[::-1].index("hypothesis") :]
    result = os.path.sep.join(parts)
    pretty_file_name_cache[f] = result
    return result


IN_COVERAGE_TESTS = os.getenv("HYPOTHESIS_INTERNAL_COVERAGE") == "true"


if IN_COVERAGE_TESTS:
    # By this point, "branch-check" should have already been deleted by the
    # tox config. We can't delete it here because of #1718.

    written: Set[Tuple[str, bool]] = set()

    def record_branch(name, value):
        key = (name, value)
        if key in written:
            return
        written.add(key)
        with open("branch-check", "a") as log:
            log.write(json.dumps({"name": name, "value": value}) + "\n")

    description_stack = []

    @contextmanager
    def check_block(name, depth):
        # We add an extra two callers to the stack: One for the contextmanager
        # function, one for our actual caller, so we want to go two extra
        # stack frames up.
        caller = sys._getframe(depth + 2)
        local_description = "%s at %s:%d" % (
            name,
            pretty_file_name(caller.f_code.co_filename),
            caller.f_lineno,
        )
        try:
            description_stack.append(local_description)
            description = " in ".join(reversed(description_stack)) + " passed"
            yield
            record_branch(description, True)
        except BaseException:
            record_branch(description, False)
            raise
        finally:
            description_stack.pop()

    @contextmanager
    def check(name):
        with check_block(name, 2):
            yield

    def check_function(f):
        @proxies(f)
        def accept(*args, **kwargs):
            # depth of 2 because of the proxy function calling us.
            with check_block(f.__name__, 2):
                return f(*args, **kwargs)

        return accept


else:  # pragma: no cover

    def check_function(f):
        return f

    @contextmanager
    def check(name):
        yield
