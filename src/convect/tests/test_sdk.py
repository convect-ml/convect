from unittest.mock import Mock, patch, call
import __main__ as _main_module
import dill
import codecs

from requests.exceptions import HTTPError
from nose.tools import with_setup, assert_equal, assert_raises, assert_is_none, assert_true

from convect.sdk import Sdk
from convect.tests import captured_output, setup_newsgroups_func, teardown_newsgroups_func, raise_, reg


@patch('convect.sdk.requests.post')
def test_deploy(mocked_post):
    mocked_post.side_effect = [
        Mock(
            status_code=201,
            json=lambda: {"pk": "123"}
        ),
        Mock()
    ]

    pickled_model = codecs.encode(
        dill.dumps(reg), "base64_codec"
    ).decode()
    pickled_session = codecs.encode(
        dill.dumps(_main_module), "base64_codec"
    ).decode()
    result = Sdk("apikey").deploy(
        model=reg,
        sample_inputs=[{'a': 0, 'b': 1}, {'a': 1, 'b': 2}]
    )
    mocked_post.assert_has_calls([
        call(
            "https://app.convect.ml/api/submitted-models/",
            json={
                "pickled_model": pickled_model,
                "pickled_session": pickled_session,
                "enable_endpoint": False
            },
            headers={'Authorization': 'Token apikey'},
        ),
        call(
            "https://app.convect.ml/api/sample-inputs/",
            json=[{
                "submitted_model": "123",
                "json_payload": {'a': 0, 'b': 1}
            }, {
                "submitted_model": "123",
                "json_payload": {'a': 1, 'b': 2}
            }],
            headers={'Authorization': 'Token apikey'}
        )
    ])
    assert_equal(result, {'model_id': "123"})


def test_deploy_bad_sample_inputs():
    assert_raises(
        AssertionError,
        Sdk("apikey").deploy,
        model=reg,
        sample_inputs='abc'
    )


@with_setup(setup_newsgroups_func, teardown_newsgroups_func)
def test_deploy_bad_session():
    with captured_output() as (out, err):
        deploy_result = Sdk("apikey").deploy(
            model=reg,
            sample_inputs=[{'a': 0, 'b': 1}, {'a': 1, 'b': 2}]
        )
    output = out.getvalue().strip()
    assert_true(output.startswith('"newsgroups" is'))
    assert_is_none(deploy_result)


@patch('convect.sdk.requests.post')
def test_deploy_bad_response(mocked_post):
    mocked_post.return_value = Mock(
        status_code=400,
        raise_for_status=lambda: (raise_(HTTPError('error')))
    )
    with captured_output() as (out, err):
        assert_raises(
            HTTPError,
            Sdk("apikey").deploy,
            model=reg,
            sample_inputs=[{'a': 0, 'b': 1}, {'a': 1, 'b': 2}]
        )
    output = out.getvalue().strip()


@patch('convect.sdk.requests.post')
def test_predict(mocked_post):
    mocked_post.return_value = Mock(
        json=lambda: {"data": {"id": "test"}}
    )
    result = Sdk("apikey").predict(model_id="123", inputs=[{'a': 1, 'b': 2}])
    mocked_post.assert_called_once_with(
        "https://api.convect.ml/predict-v0/123/",
        json=[{'a': 1, 'b': 2}]
    )
    assert_equal(result, {"data": {"id": "test"}})


@patch('convect.sdk.requests.post')
def test_predict_bad_response(mocked_post):
    mocked_post.return_value = Mock(
        status_code=400,
        raise_for_status=lambda: (raise_(HTTPError('error')))
    )
    del mocked_post.return_value.json  # Remove json attribute to 
    assert_raises(
        HTTPError,
        Sdk("apikey").predict,
        model_id="123",
        inputs=[{'a': 1, 'b': 2}]
    )


def test_ready():
    with captured_output() as (out, err):
        Sdk("apikey").ready()
    output = out.getvalue().strip()
    assert_equal(
        output,
        "Welcome to Convect!\n\nHead to https://app.convect.ml to start deploying models."
    )
