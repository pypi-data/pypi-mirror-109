import base64
import os
import json
import io
import time
import csv
import threading
import itertools
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from yaspin import yaspin


class AutomateMissingCredentialsException(Exception):
    pass


class AutomateAuthException(Exception):
    pass


class InvalidResponseException(Exception):
    status_code = None

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class AutomateClient:

    __USERNAME = None
    __PASSWORD = None

    __DEBUG = False
    __ACCESS_TOKEN = None

    API_URL = "https://auto.primer.ai/api/v1/automate"

    def __init__(self, username=None, password=None, access_token=None, debug=True):
        self.SESSION = requests.Session()

        self.__USERNAME = username
        self.__PASSWORD = password
        self.__ACCESS_TOKEN = access_token

        self.__DEBUG = debug

        if not access_token and not username and not password:
            raise AutomateMissingCredentialsException(
                "Missing authentication mechanism, you need to provide either an access_token or username and password combination"
            )

        if username and not password:
            raise AutomateMissingCredentialsException(
                "Password is required for authentication"
            )

        if password and not username:
            raise AutomateMissingCredentialsException(
                "Username is required for authentication"
            )

        if access_token is not None:
            self.set_access_token(access_token)
        else:
            self.refresh_token(username, password)

    def __log(self, msg):
        if self.__DEBUG:
            print(msg)

    def __handle_json_response(self, resp):
        """Ensure a valid JSON response

        Args:
            resp: A `requests` Response object

        Raises:
            AutomateAuthException: If a 401 is returned by an endpoint
            InvalidResponseException: If an invalid status code is returned (not a 200 or 201)

        Returns:
            object: the deserialized json
        """
        if resp.status_code == 401:
            raise AutomateAuthException

        if resp.status_code == 204:
            return None

        if (
            resp.status_code != 200
            and resp.status_code != 201
            and resp.status_code != 202
        ):
            raise InvalidResponseException(resp.status_code, resp.text)

        return resp.json()

    def set_access_token(self, access_token):
        self.__ACCESS_TOKEN = access_token
        self.SESSION.headers.update({"Authorization": f"JWT {access_token}"})

    def refresh_token(self, username, password, retries=1):
        """Refreshes the __ACCESS_TOKEN given using a provided username and password

        Args:
            retries (int, optional): number of times to retry refreshing. Defaults to 1.

        Raises:
            Exception: If authorization wasn't successful, an Exception is rasied
        """

        for i in range(retries):
            maybe_exception = None
            try:
                self.__log("Getting access token...")
                session_information = self.verify_credentials(
                    self.__USERNAME, self.__PASSWORD
                )
                self.__log("Access token retrieved...")
                self.set_access_token(session_information["access_token"])
                time.sleep(1)
            except Exception as e:
                self.__log(e)
                maybe_exception = e

        if maybe_exception is not None:
            raise maybe_exception

    def verify_credentials(self, username, password):
        """Makes a POST request to Primer's authorization service and returns session information.
        Uses USERNAME and PASSWORD when making the POST request

        Returns:
        string:An access token
        """
        credentials_request = requests.post(
            "https://sso.primer.ai/api/v1/auth/login",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            data=json.dumps(
                {
                    "password": password,
                    "username": username,
                }
            ),
        )

        if credentials_request.status_code != 200:
            raise Exception(
                f"Received bad status code from authorization service while attempting to refresh credentials: {credentials_request.status_code}, message: {credentials_request.text}"
            )

        resp = credentials_request.json()
        return resp

    def get_models(self, order="desc", page=0, page_size=0, is_published=False):
        """Returns dict summary of models, and counts of models available to account.

        Args:
            order (str, optional): Defaults to "desc".
            page (int, optional): Defaults to 0.
            page_size (int, optional): Defaults to 0, which returns all models in account.
            is_published (bool, optional): Defaults to False.

        Returns:
            dict: Returns dict_keys(['filters', 'models', 'pagination']), where
                `filters` contains a list of system model statuses,
                `models` contains a list of model summaries, and
                `pagination` contains a brief summary of the model counts available to account.
        """
        method_url = f"{self.API_URL}/models?order={order}&page={page}&page_size={page_size}&is_published={is_published}&org_models=true"

        try:
            r = self.SESSION.get(method_url)
            resp = self.__handle_json_response(r)
        except AutomateAuthException as e:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.get(method_url)
            return self.__handle_json_response(r)

        return resp

    def get_datasets(self, order="desc", page=0, page_size=0):
        """Returns list of datasets available to account.

        Args:
            order (str, optional): Defaults to "desc".
            page (int, optional): Defaults to 0.
            page_size (int, optional): Defaults to 0, which returns all datasets in account.

        Raises:
            e: Authentication error

        Returns:
            dict: Returns dict_keys(['filters', 'pagination', 'datasets']), where
                `filters` contains a list of system dataset statuses,
                `pagination` contains a summary of dataset counts available to account, and
                `datasets` contains a list of dataset summaries -- includes dataset id.

        """
        method_url = (
            f"{self.API_URL}/datasets?order={order}&page={page}&page_size={page_size}"
        )

        try:
            r = self.SESSION.get(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.get(method_url)
            return self.__handle_json_response(r)

    def get_training_jobs(self):
        """Returns list of training jobs with associated dataset id, job id, creation data, and model id.

        Returns:
            dict: Returns list of training summaries with associated dataset id, job id, creation data, and model id.
        """
        method_url = f"{self.API_URL}/training-jobs:all"

        try:
            r = self.SESSION.get(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.get(method_url)
            return self.__handle_json_response(r)

    def upload_dataset(self, dataset_data, dataset_name, dataset_type="Reports"):
        request_args = {
            "url": f"{self.API_URL}/datasets:upload-csv?dataset_meta_display_name={dataset_name}&dataset_meta_document_type={dataset_type}",
            "data": dataset_data.encode("utf-8"),
            "headers": {"content-type": "text/csv", "charset": "UTF-8"},
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def duplicate_dataset(self, dataset_id, new_dataset_name):
        """Duplicates the dataset. Also needs a new name for the dataset.

        Args:
            dataset_id (str): Dataset unique id
            new_dataset_name (str): New dataset display name

        Returns:
            dict: JSON summary of dataset
        """
        request_args = {
            "url": f"{self.API_URL}/datasets/{dataset_id}/duplicate",
            "json": {"display_name": new_dataset_name},
            "headers": {"content-type": "application/json"},
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def rename_dataset(self, dataset_id, new_dataset_name):
        """Renames the display name of dataset.

        Args:
            dataset_id (str): Dataset unique id
            new_dataset_name (str): New dataset display name

        Returns:
            dict: JSON summary of dataset
        """
        request_args = {
            "url": f"{self.API_URL}/datasets/{dataset_id}",
            "json": {"display_name": new_dataset_name},
            "headers": {"content-type": "application/json"},
        }

        try:
            r = self.SESSION.patch(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.patch(**request_args)
            return self.__handle_json_response(r)

    def delete_dataset(self, dataset_id):
        """Deletes dataset.

        Args:
            dataset_id (str): dataset_id unique id

        Returns:
            None
        """

        method_url = f"{self.API_URL}/datasets/{dataset_id}"

        try:
            r = self.SESSION.delete(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.delete(method_url)
            return self.__handle_json_response(r)

    def create_model(self, model_name, dataset_id, labels, model_type="CLF_MULTILABEL"):
        request_args = {
            "url": f"{self.API_URL}/models",
            "json": {
                "name": model_name,
                "description": model_name,
                "display_name": model_name,
                "dataset_id": dataset_id,
                "labels": labels,
                "type": model_type,
                "published_status": "private",
                "is_archived": False,
                "is_trainable": True,
                "status": "Has Dataset",
            },
            "headers": {"content-type": "application/json"},
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def rename_model(self, model_id, new_model_name):
        """Renames the display name of model.

        Args:
            model_id (str): Model unique id
            new_model_name (str): New model display name

        Returns:
            dict: JSON summary of model
        """
        request_args = {
            "url": f"{self.API_URL}/models/{model_id}",
            "json": {"display_name": new_model_name, "base_model_id": model_id},
            "headers": {"content-type": "application/json"},
        }

        try:
            r = self.SESSION.patch(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.patch(**request_args)
            return self.__handle_json_response(r)

    def delete_model(self, model_id):
        """Deletes model.

        Args:
            model_id (str): Model unique id

        Returns:
            None
        """

        method_url = f"{self.API_URL}/models/{model_id}"

        try:
            r = self.SESSION.delete(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.delete(method_url)
            return self.__handle_json_response(r)

    def get_unlabled_data(self, dataset_id, model_id, batch_size=20):
        method_url = f"{self.API_URL}/datasets:unlabeled?dataset_id={dataset_id}&model_id={model_id}&batch_size={batch_size}&new_batch=true"

        try:
            r = self.SESSION.get(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.get(method_url)
            return self.__handle_json_response(r)

    def get_documents(self, dataset_id):
        method_url = f"{self.API_URL}/documents?dataset_id={dataset_id}"

        try:
            r = self.SESSION.get(method_url)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.get(method_url)
            return self.__handle_json_response(r)

    def label_document(self, dataset_id, doc_id, model_id, label_id, label_value):
        request_args = {
            "url": f"{self.API_URL}/labels?return_all_labels=true",
            "json": {
                "dataset_id": dataset_id,
                "document_id": doc_id,
                "model_id": model_id,
                "label": {"label_meta_id": label_id, "label_value": label_value},
            },
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def train_model(self, model_id, dataset_id):
        request_args = {
            "url": f"{self.API_URL}/training-jobs",
            "json": {"model_id": model_id, "dataset_id": dataset_id},
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def get_model_prediction(self, model_id, text):
        request_args = {
            "url": f"{self.API_URL}/models/{model_id}/predictions",
            "json": {"text": text},
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        }

        try:
            r = self.SESSION.post(**request_args)
            resp = self.__handle_json_response(r)
            return resp
        except AutomateAuthException:
            if not self.__USERNAME and not self.__PASSWORD:
                raise e

            self.refresh_token(self.__USERNAME, self.__PASSWORD)
            r = self.SESSION.post(**request_args)
            return self.__handle_json_response(r)

    def make_classifier(self, model_name, data):
        """Create, label and train a model

        Args:
            model_name (str): The name of the model
            data (AutomateClassifierDatasetRow): A list of AutomateClassifierDatasetRow objects
        """

        ## first, get the data in a csv like format
        csv_rows = [["text", "title"]]

        is_multilabel = False
        unique_labels = set()

        # Get all the unique labels
        for row in data:
            if len(row.labels) > 1:
                is_multilabel = True

            unique_labels.update(row.labels)

            # We'll store the labels along with the text, so they're always paired together
            # and this dataset can be reused to build other models without the origin data
            csv_row = [row.text, json.dumps(row.labels)]

            csv_rows.append(csv_row)

        # make an in-memory csv of text + labels
        s = io.StringIO()
        csv.writer(s).writerows(csv_rows)
        s.seek(0)
        csv_text = s.getvalue()

        self.__log("Uploading training data...")

        with yaspin():
            dataset = self.upload_dataset(csv_text, model_name + "_dataset")

        self.__log("dataset id: " + dataset["dataset_id"])
        self.__log("Upload complete...")

        labels = []

        ## If there's only one label across the entire list of AutomateClassifierDatasetRow objects? It's binary
        if len(unique_labels) == 1:
            model_type = "CLF_BINARY"
        elif not is_multilabel:
            model_type = "CLF_MULTICLASS"
        else:
            model_type = "CLF_MULTILABEL"

        # Convert all the new labels to dict's, which are needed for creating the model
        for unique_label in unique_labels:
            labels.append(
                {
                    "name": unique_label,
                    "description": unique_label,
                    "color": "",  ## todo: do we need colors for multiclass?
                }
            )

        self.__log("Creating model...")
        with yaspin():
            model = self.create_model(
                model_name, dataset["dataset_id"], labels, model_type=model_type
            )

        self.__log("model id: " + model["id"])
        self.__log("Model created...")

        ## Fetch the dataset again, as we need the actual numerical ID's that are attached to
        ## each document of the dataset by Automate after uploading a dataset
        self.__log("Fetching labeling data...")
        documents = []
        with yaspin():
            documents = self.get_documents(dataset["dataset_id"])

        self.__log("Labeling data fetched...")

        with yaspin():
            ## fist, do a quick calculation to get total labels
            processes = []
            # total_labels = len(documents["documents"]) * len(model["labels"])
            # labels_pending = 0

            self.__log(
                "Starting to label, this could take a while, please don't exit this script..."
            )

            def label_document(datset_id, document_id, model_id, label_id, value):
                try:
                    self.label_document(
                        datset_id, document_id, model_id, label_id, value
                    )
                except InvalidResponseException as e:
                    ## If there was a bad status code, sleep for 2 seconds and then try again
                    time.sleep(3)
                    try:
                        self.label_document(
                            datset_id, document_id, model_id, label_id, value
                        )
                    except InvalidResponseException as e:
                        self.__log(
                            f"An invalid response with status code {e.status_code} was received from the server when trying to label a document: {document_id}"
                        )
                        self.__log(
                            f"We attempted to label this document a few times, but continued to receive this status code. We'll proceed without this labeled document, but if it's critical you can restart the model creation process by restarting this script after a short pause."
                        )
                        time.sleep(3)
                        pass

            with ThreadPoolExecutor(max_workers=10) as executor:
                completed_labels = 0
                for document in documents["documents"]:
                    labels = json.loads(document["title"])
                    leftover_labels = model["labels"]

                    true_labels = []
                    for label in labels:
                        # Match the label from the dataset to the labels attached to the model
                        existing_label = next(
                            l for l in leftover_labels if l["name"] == label
                        )
                        if existing_label:
                            true_labels.append(existing_label)

                        # Remove the found label and the remaining these will end up being set to False
                        leftover_labels = list(
                            filter(
                                lambda l: l["name"] != existing_label["name"],
                                leftover_labels,
                            )
                        )

                        for true_label in true_labels:
                            processes.append(
                                executor.submit(
                                    label_document,
                                    dataset["dataset_id"],
                                    document["id"],
                                    model["id"],
                                    true_label["id"],
                                    True,
                                )
                            )

                        # Don't need to mark False for multiclass
                        if model_type == "CLF_MULTICLASS":
                            continue

                        for false_label in leftover_labels:
                            processes.append(
                                executor.submit(
                                    label_document,
                                    dataset["dataset_id"],
                                    document["id"],
                                    model["id"],
                                    false_label["id"],
                                    False,
                                )
                            )

                for task in as_completed(processes):
                    # pass
                    completed_labels += 1

                    if completed_labels % 100 == 0:
                        self.__log(f"{completed_labels} labeling actions completed...")

        self.__log("Thanks for waiting, labeling complete...")
        self.__log("Sending model for training...")
        training_job = self.train_model(model["id"], dataset["dataset_id"])
        self.__log(
            f"Model is being trained, training id: {training_job['training_job_id']}"
        )
        self.__log(
            "At this point, you can exit this script as model training is done asynchronously. It'll take between 5-20 mintues to train and then the model will automatically deploy."
        )
        self.__log(
            f"Once deployed, you can get predictions from the model by calling the method in this client: get_model_prediction('{model['id']}', 'Some text')"
        )
        self.__log(
            f"If you let this script continue to run, we'll poll the training status of the model and let you know when it's completed."
        )

        with yaspin():
            is_model_training = True
            consecutive_training_job_fetch_failures = 0
            while is_model_training:
                time.sleep(30)
                try:
                    training_jobs = self.get_training_jobs()
                    consecutive_training_job_fetch_failures = 0
                except Exception as e:
                    if consecutive_training_job_fetch_failures > 3:
                        self.__log(
                            "We continued to have difficulty getting the training jobs, we're going to stop attempting now..."
                        )
                        raise e
                    self.__log(
                        "We weren't able to get the training jobs, going to try again shortly..."
                    )
                    consecutive_training_job_fetch_failures += 1

                statuses = training_jobs["statuses"]
                training_job = next(
                    job
                    for job in statuses
                    if job["training_job_id"] == training_job["training_job_id"]
                )

                if training_job["training_job_status"] == "completed":
                    is_model_training = False
                else:
                    self.__log("Model is still training...")

        self.__log(
            f"Model as completed training, feel free to call the client method get_model_prediction('{model['id']}', 'Some text') to get a prediction"
        )


class AutomateClassifierDatasetRow:
    text = None
    labels = []

    def __init__(self, text, labels):
        """[summary]

        Args:
            text (str): The text of the training data
            labels (list): A list of strings representing the labels of the training data
        """
        self.text = text
        self.labels = labels
