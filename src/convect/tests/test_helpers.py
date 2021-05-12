import dill
import codecs
import __main__ as _main_module

from nose.tools import with_setup, assert_equal, assert_in, assert_not_in, assert_true, assert_false

from convect.tests import setup_newsgroups_func, teardown_newsgroups_func, setup_ipython_module_func, teardown_ipython_module_func
from convect.helpers import is_iterable, list_large_vars, exclude_ignores_and_redump


def test_is_iterable():
    assert_true(is_iterable(['a', 'b', 'c']))
    assert_true(is_iterable(('a', 'b', 'c',)))
    assert_false(is_iterable('abc'))


def test_list_large_vars_zero_large_vars():
    pickled_session = codecs.encode(
        dill.dumps(_main_module), "base64_codec"
    ).decode()
    assert_equal(list_large_vars(pickled_session), [])


@with_setup(setup_newsgroups_func, teardown_newsgroups_func)
def test_list_large_vars_one_large_var():
    pickled_session = codecs.encode(
        dill.dumps(_main_module), "base64_codec"
    ).decode()
    assert_in('newsgroups', list_large_vars(pickled_session))


@with_setup(setup_ipython_module_func, teardown_ipython_module_func)
def test_list_large_vars_skip_ipython_var():
    assert_true(hasattr(_main_module, "ipython_module"))
    pickled_module = codecs.encode(
        dill.dumps(_main_module), "base64_codec"
    ).decode()
    assert_not_in('ipython_module', list_large_vars(pickled_module))


def test_exclude_ignores_and_redump():
    setattr(_main_module, 'test_ignores', 1)
    assert_in('test_ignores', dir(_main_module))
    assert_equal(_main_module.test_ignores, 1)
    pickled_session = codecs.encode(
        dill.dumps(_main_module), "base64_codec"
    ).decode()
    new_pickled_session = exclude_ignores_and_redump(
        pickled_session, ['test_ignores']
    )
    new_session = dill.loads(
        codecs.decode(
            new_pickled_session.encode(), "base64_codec"
        )
    )
    assert_not_in('test_ignores', dir(new_session))
