import io
import dill
import codecs
import requests
import json
from typing import List, Tuple

ROOT_DOMAIN = "convect.ml"
CREATE_HOST = f"https://app.{ROOT_DOMAIN}/api"
PREDICT_HOST = f"https://api.{ROOT_DOMAIN}/predict-v0"


def is_iterable(value):
    return isinstance(value, List) or isinstance(value, Tuple)


class Sdk:
    def __init__(self, api_token, create_host=CREATE_HOST, predict_host=PREDICT_HOST):
        self.api_token = api_token
        self.create_host = create_host
        self.predict_host = predict_host

    def deploy(self, model, sample_inputs=[]):
        assert is_iterable(sample_inputs)
        pickled_model = codecs.encode(
            dill.dumps(model), "base64_codec").decode()
        with io.BytesIO() as buffer:
            dill.dump_session(buffer)
            pickled_session = codecs.encode(
                buffer.getvalue(), "base64_codec").decode()
        model_submission_data = {
            "pickled_model": pickled_model,
            "pickled_session": pickled_session,
            "enable_endpoint": False
        }
        response = requests.post(
            f"{self.create_host}/submitted-models/",
            json=model_submission_data,
            headers={'Authorization': f'Token {self.api_token}'}
        )
        response_json = response.json()
        if not response.ok:
            print(response_json)
            response.raise_for_status()
        sample_input_data = [{
            "submitted_model": response_json['pk'],
            "json_payload": sample_input,
        } for sample_input in sample_inputs]
        requests.post(
            f"{self.create_host}/sample-inputs/",
            json=sample_input_data,
            headers={'Authorization': f'Token {self.api_token}'}
        )
        submission_data = {
            "model_id": response_json['pk'],
        }
        print(
            "Your model is now deployed! Try it out with this shell command:\n\n" +
            f"curl -H 'Content-Type: application/json' -d '{json.dumps(sample_inputs)}' -X POST {self.predict_host}/{response_json['pk']}/"
        )
        return submission_data

    def predict(self, model_id, inputs):
        assert is_iterable(inputs)
        response = requests.post(
            f"{self.predict_host}/{model_id}/",
            json=inputs
        )
        try:
            return response.json()
        except:
            response.raise_for_status()
