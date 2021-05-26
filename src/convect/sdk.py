import io
import dill
import codecs
import requests
import json
from typing import List, Dict, Any, Union
from convect.helpers import is_iterable, list_large_vars, exclude_ignores_and_redump

ROOT_DOMAIN = "convect.ml"
CREATE_HOST = f"https://app.{ROOT_DOMAIN}/api"
PREDICT_HOST = f"https://api.{ROOT_DOMAIN}/predict-v0"


class Sdk:
    def __init__(self, api_token, create_host=CREATE_HOST, predict_host=PREDICT_HOST):
        self.api_token = api_token
        self.create_host = create_host
        self.predict_host = predict_host

    def deploy(self, model, sample_inputs=[], ignore=[]):
        assert is_iterable(sample_inputs)
        pickled_model = codecs.encode(
            dill.dumps(model), "base64_codec").decode()
        with io.BytesIO() as buffer:
            dill.dump_session(buffer)
            pickled_session = codecs.encode(
                buffer.getvalue(), "base64_codec").decode()

        pickled_session = exclude_ignores_and_redump(pickled_session, ignore)

        large_vars = list_large_vars(pickled_session)
        if len(large_vars) > 0:
            error_msg = f'''
Convect cannot deploy a session containing variables holding more than 0.5MB of data.
If these variables are not required to host the model, you can use the "ignore" argument
to exclude them from the deployment. E.g.

convect_sdk.deploy(model, sample_inputs={sample_inputs}, ignore=[{", ".join([f'"{v}"' for v in (ignore + large_vars)])}])
            '''
            print(error_msg)
            return

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
        if response.status_code != 201:
            response.raise_for_status()
        else:
            response_json = response.json()
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
            f"Your model ({response_json['pk'][:6]}...) is now deployed! Try it out with this shell command:\n\n" +
            f"curl -H 'Content-Type: application/json' -d '{json.dumps(sample_inputs)}' -X POST {self.predict_host}/{response_json['pk']}/"
        )
        return submission_data

    def predict(self, model_id: str, inputs: List[Dict[str, Any]]) -> Union[dict, list]:
        assert is_iterable(inputs)
        response = requests.post(
            f"{self.predict_host}/{model_id}/",
            json=inputs
        )
        try:
            return response.json()
        except:
            response.raise_for_status()

    def ready(self):
        print("Welcome to Convect!\n")
        print("Head to https://app.convect.ml to start deploying models.")
