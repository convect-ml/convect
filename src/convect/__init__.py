import io
import dill
import codecs
import requests

class Sdk:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    def submit(self, model, sample_inputs=[]):
        pickled_model = codecs.encode(dill.dumps(model), "base64_codec").decode()
        with io.BytesIO() as buffer:
            dill.dump_session(buffer)
            pickled_session = codecs.encode(buffer.getvalue(), "base64_codec").decode()
        model_submission_data = {
            "pickled_model": pickled_model,
            "pickled_session": pickled_session,
            "enable_endpoint": False
        }
        response = requests.post(
            "https://app.convect.ml/api/submitted-models/",
            json=model_submission_data,
            headers={'Authorization': f'Token {self.auth_token}'}
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
            "https://app.convect.ml/api/sample-inputs/",
            json=sample_input_data,
            headers={'Authorization': f'Token {self.auth_token}'}
        )
        submission_data = {
            "model_id": response_json['pk'],
        }
        print("Your model is deployed!")
        return submission_data

    @staticmethod
    def predict(model_id, inputs):
        response = requests.post(
            f"https://api.convect.ml/predict-v0/{model_id}/",
            json=inputs
        )
        try:
            return response.json()
        except:
            response.raise_for_status()