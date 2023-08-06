"""Integration tests that validates the BYOML story.

See https://github.com/waylayio/waylay-py/issues/3
"""
from typing import Any, Tuple
import time
import random
import tempfile
import os

import numpy as np
import pandas as pd

from waylay import (
    WaylayClient,
    RestResponseError
)

from waylay.service.byoml import ByomlActionError, ByomlValidationError

from fixtures import (
    sklearn_model_and_test_data,
    tensorflow_model_and_test_data,
    pytorch_model_and_test_data,
    pytorch_custom_model_and_test_data,
    xgboost_model_and_test_data,
    generate_dataset,
    generate_labels,
)
import pytest


class ModelUpload():
    """Object to upload a trained model for any supported framework."""

    def __init__(
        self,
        client,
        model,
        framework,
        model_name,
        input_data,
        predictions,
        work_dir=None
    ):
        """Create the ModelUpload object."""
        self.client = client
        self.model = model
        self.framework = framework
        self.model_name = model_name
        self.input_data = input_data
        self.predictions = predictions
        self.work_dir = work_dir

    def upload_test_model(self) -> Any:
        """Delete any test model before uploading a new one."""
        try:
            self.client.byoml.model.remove(self.model_name)
            # removed, await (see )
            time.sleep(10)
        except RestResponseError as exc:
            # not found, OK
            pass

        return self.client.byoml.model.upload(
            self.model_name, self.model, framework=self.framework,
            description=f"integration test {__name__}.test_byoml_create_{self.framework}_model",
            work_dir=self.work_dir
        )

    def validate_uploaded_model(self):
        """Validate if the model has been uploaded correctly."""
        model_repr = self.client.byoml.model.get(self.model_name)
        assert 'name' in model_repr
        assert f'integration test {__name__}' in model_repr['description']

    def validate_updated_model(self):
        """Validate if the model has been correctly updated."""
        model_repr = self.client.byoml.model.get(self.model_name)
        assert 'updated' in model_repr['description']

    def predict_model(self, **kwargs):
        """Create a prediction with a model."""
        # test model on byoml, wait until ready
        predictions = self.client.byoml.model.predict(self.model_name, self.input_data, **kwargs)

        assert predictions is not None
        assert len(predictions) == len(self.input_data.index)

        # Floating points can be imprecise, don't assert equality
        np.testing.assert_allclose(self.predictions, predictions, atol=1e-05)

    def replace_test_model(self):
        """Replace the current model."""
        self.client.byoml.model.replace(
            self.model_name, self.model, framework=self.framework,
            description=f"updated integration test {__name__}.test_byoml_create_{self.framework}_model"
        )

    def remove_test_model(self):
        """Remove the model used in the test case."""
        self.client.byoml.model.remove(self.model_name)

    def execute_model_upload(self):
        """
        Upload a model using the following steps.

        Upload model, validate the upload, create a prediction,
        replace the test model and validate the replacement.
        Finally remove the test model.
        """
        self.upload_test_model()
        self.validate_uploaded_model()
        self.predict_model()
        self.replace_test_model()
        self.validate_updated_model()
        self.remove_test_model()


class SklearnModelUpload(ModelUpload):
    """Sklearn upload support."""


class PytorchModelUpload(ModelUpload):
    """Pytorch upload support."""

    def predict_model(self):
        """Create a prediction with a PyTorch model."""
        # test model on byoml, wait until ready
        predictions = self.client.byoml.model.predict(self.model_name, self.input_data)

        assert predictions is not None
        assert len(predictions) == self.input_data.size()[0]

        # Floating points can be imprecise, don't assert equality
        np.testing.assert_allclose(self.predictions, predictions, atol=1e-05)


class XGBoostModelUpload(ModelUpload):
    """XGBoost upload support."""


class TensorflowModelUpload(ModelUpload):
    """Tensorflow upload support."""


@pytest.mark.sklearn
def test_byoml_create_model(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f"test-sklearn-{int(random.random()*1000)}"

    model_upload = SklearnModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.sklearn
def test_byoml_create_model_in_local_dir(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f"test-sklearn-local-{int(random.random()*1000)}"

    with tempfile.TemporaryDirectory() as work_dir:

        model_upload = SklearnModelUpload(
            client=waylay_test_client,
            model=model,
            framework=framework,
            model_name=model_name,
            input_data=df_validate,
            predictions=predictions,
            work_dir=work_dir
        )

        model_upload.execute_model_upload()

        assert os.path.exists(os.path.join(work_dir, 'model.joblib'))


@pytest.mark.sklearn
def test_byoml_create_model_in_unexisting_local_dir(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f"test-sklearn-unex-dir-{int(random.random()*1000)}"

    dir_name = "dir_does_not_exist"

    model_upload = SklearnModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions,
        work_dir=dir_name
    )

    with pytest.raises(ByomlValidationError) as exc_info:
        model_upload.execute_model_upload()

    assert 'does not exist' in format(exc_info)


@pytest.mark.sklearn
def test_byoml_get_model_without_retry(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f"test-sklearn-no-retry-{int(random.random()*1000)}"
    model_upload = SklearnModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.upload_test_model()
    with pytest.raises(ByomlActionError):
        model_upload.predict_model(retry_attempts=-1)
    model_upload.remove_test_model()


@pytest.mark.sklearn
def test_byoml_create_dill_model(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f"test-sklearn-dill-{int(random.random()*1000)}"

    import dill  # pylint: disable=import-error

    with tempfile.TemporaryDirectory() as tmp_dir:
        model_file = f'{tmp_dir}/model.joblib'

        with open(model_file, 'wb') as f:
            dill.settings['recurse'] = True
            dill.dump(model, f)

        model_upload = SklearnModelUpload(
            client=waylay_test_client,
            model=model_file,
            framework=framework,
            model_name=model_name,
            input_data=df_validate,
            predictions=predictions
        )

        model_upload.execute_model_upload()


@pytest.mark.tensorflow
def test_byoml_create_tf_model(
    tensorflow_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a tensorflow model."""
    model, df_validate, predictions = tensorflow_model_and_test_data

    framework = "tensorflow"
    model_name = f"test-tensorflow-{int(random.random()*1000)}"

    model_upload = TensorflowModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
def test_byoml_create_pytorch_model(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a pytorch model."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f"test-pytorch-{int(random.random()*1000)}"

    model_upload = PytorchModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
def test_byoml_create_pytorch_script(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a pytorch script."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f"test-pytorch-script-{int(random.random()*1000)}"

    import torch  # pylint: disable=import-error
    model_script = torch.jit.script(model)
    model_upload = PytorchModelUpload(
        client=waylay_test_client,
        model=model_script,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
def test_byoml_create_pytorch_trace(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a pytorch trace."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f"test-pytorch-trace-{int(random.random()*1000)}"

    import torch  # pylint: disable=import-error
    model_trace = torch.jit.trace(model, torch.randn(5, 1))  # pylint: disable=no-member
    model_upload = PytorchModelUpload(
        client=waylay_test_client,
        model=model_trace,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.skip(reason="PyTorch 1.5 does not support this")
@pytest.mark.pytorch
def test_byoml_create_pytorch_custom(
    pytorch_custom_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test a custom pytorch function."""
    model, validation_tensor, predictions = pytorch_custom_model_and_test_data
    framework = "pytorch"
    model_name = f"test-pytorch-custom-{int(random.random()*1000)}"

    model_upload = PytorchModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.xgboost
def test_byoml_create_xgboost_model(
    xgboost_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient
):
    """Create, upload, and test an xgboost model."""
    model, df_validate, predictions = xgboost_model_and_test_data

    framework = "xgboost"
    model_name = f"test-xgboost-{int(random.random()*1000)}"

    model_upload = XGBoostModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()
