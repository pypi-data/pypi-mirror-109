"""REST definitions for the 'model' entity of the 'byoml' service."""

from zipfile import ZipFile
from io import BytesIO
from functools import wraps
from typing import Callable, List, Any, Union, Tuple, Dict, Optional
import os
import tempfile

import joblib
import pandas as pd
import numpy as np

from .._base import WaylayResource
from .._decorators import (
    return_body_decorator,
    return_path_decorator,
    suppress_header_decorator
)
from ._decorators import (
    byoml_exception_decorator,
    byoml_retry_decorator
)
from ...exceptions import (
    RestRequestError,
)
from ._exceptions import (
    ByomlValidationError,
)


def _input_data_as_list(input_data):
    if isinstance(input_data, list):
        if not input_data:
            # empty list
            return input_data

        if hasattr(input_data[0], 'tolist'):
            # list of numpy arrays
            return [d.tolist() for d in input_data]

        if isinstance(input_data[0], (pd.DataFrame, pd.Series)):
            # list of pandas
            return [d.values.tolist() for d in input_data]

        # list of (list of ...) value types?
        return input_data

    # pandas
    if isinstance(input_data, (pd.DataFrame, pd.Series)):
        return input_data.values.tolist()

    # numpy arrays
    if hasattr(input_data, 'tolist'):
        return input_data.tolist()

    raise RestRequestError(
        f'input data of unsupported type {type(input_data)}'
    )


def model_execution_request_decorator(action_method):
    """Decorate an action to prepare the execution of the model.

    Transforms any input data into a list, and provides it
    as `instances` in the request body.
    """
    @wraps(action_method)
    def wrapped(model_name, input_data, **kwargs):
        body = kwargs.pop('body', {})
        if 'instances' not in body:
            body = {
                'instances': _input_data_as_list(input_data),
                **body
            }
        return action_method(
            model_name,
            body=body,
            **kwargs
        )
    return wrapped


DEFAULT_DECORATORS = [
    byoml_exception_decorator,
    return_body_decorator,
]


def _get_model_decorator() -> List[Callable]:
    return [
        byoml_retry_decorator,
        byoml_exception_decorator,
        return_body_decorator,
    ]


def _execute_model_decorators(response_key: str) -> List[Callable]:
    return [
        byoml_retry_decorator,
        byoml_exception_decorator,
        model_execution_request_decorator,
        return_path_decorator(
            [response_key],
            default_response_constructor=np.array
        )
    ]


DEFAULT_BYOML_MODEL_TIMEOUT = 60

# type aliases for documentation purpose
PathLike = Union[str, os.PathLike]
PytorchModel = Any
TensorflowModel = Any
XgboostModel = Any
SklearnModel = Any
ByomlModel = Union[PytorchModel, TensorflowModel, XgboostModel, SklearnModel]
ModelSerializer = Callable[[PathLike, ByomlModel], PathLike]


def _serialize_torch(work_dir: PathLike, trained_model: PytorchModel) -> PathLike:
    """Serialize a pytorch model to a `model.pt` file."""
    # assuming a TorchScript model
    import torch  # pylint: disable=import-error

    model_file = f'{work_dir}/model.pt'
    model_script = torch.jit.script(trained_model)
    model_script.save(model_file)
    return model_file


def _serialize_joblib(work_dir: PathLike, trained_model: SklearnModel) -> PathLike:
    """Serialize a sklearn model to a `model.joblib` file."""
    model_file = f'{work_dir}/model.joblib'
    joblib.dump(trained_model, model_file)
    return model_file


def _serialize_tf(work_dir: PathLike, trained_model: TensorflowModel) -> PathLike:
    """Serialize a tensorflow model to a model folder."""
    import tensorflow as tf  # pylint: disable=import-error

    tf.saved_model.save(trained_model, work_dir)
    return work_dir


def _serialize_bst(work_dir: PathLike, trained_model: XgboostModel) -> PathLike:
    """Serialize a xgboost model to a `model.bst` file."""
    if hasattr(trained_model, 'save_model'):
        model_file = f'{work_dir}/model.bst'
        trained_model.save_model(model_file)
        return model_file
    raise ByomlValidationError('Could not serialise this model: missing `save_model` method.')


SUPPORTED_FRAMEWORKS: Dict[str, ModelSerializer] = {
    "pytorch": _serialize_torch,
    "sklearn": _serialize_joblib,
    "tensorflow": _serialize_tf,
    "xgboost": _serialize_bst,
}


def assert_dir_exists(dir_name: PathLike):
    """Raise error if the input directory does not exist."""
    if not os.path.exists(str(dir_name)):
        raise ByomlValidationError(f"The directory '{dir_name}' does not exist.")


class ModelResource(WaylayResource):
    """REST Resource for the 'model' entity of the 'byoml' service."""

    link_roots = {
        'doc': '${doc_url}/api/byoml/',
        'iodoc': '${iodoc_url}/api/byoml/?id='
    }

    actions = {
        'list': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models'])
            ],
            'description': 'List the metadata of the deployed <em>BYOML Models</em>',
            'links': {
                'doc': '#overview-of-the-api',
                'iodoc': 'overview-of-the-api'
            },
        },
        'list_names': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models', 'name'])
            ],
            'description': 'List the names of deployed <em>BYOML Models</em>',
            'links': {
                'doc': '#overview-of-the-api',
                'iodoc': 'overview-of-the-api'
            },
        },
        '_create': {
            'method': 'POST',
            'url': '/models',
            'decorators': DEFAULT_DECORATORS,
            'description': (
                'Build and create a new <em>BYOML Model</em> as specified in the request'
            ),
            'name': 'upload',
            'links': {
                'doc': '#how-to-upload-your-model',
                'iodoc': 'how-to-upload-your-model'
            },
        },
        '_replace': {
            'method': 'PUT',
            'url': '/models/{}',
            'name': 'replace',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Build and replace the named <em>BYOML Model</em>',
            'links': {
                'doc': '#overwriting-a-model',
                'iodoc': 'overwriting-a-model'
            },
        },
        'get': {
            'method': 'GET',
            'url': '/models/{}',
            'decorators': _get_model_decorator(),
            'description': 'Fetch the metadata of the named <em>BYOML Model</em>',
            'links': {
                'doc': '#checking-out-your-model',
                'iodoc': 'checking-out-your-model'
            },
        },
        'get_content': {
            'method': 'GET',
            'url': '/models/{}/content',
            'decorators': [byoml_exception_decorator],
            'description': 'Fetch the content of the named <em>BYOML Model</em>',
            'links': {
                'doc': '#checking-out-your-model',
                'iodoc': 'checking-out-your-model'
            },
        },
        'examples': {
            'method': 'GET',
            'url': '/models/{}/examples',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['example_payloads'])
            ],
            'description': (
                'Fetch the <em>example request input</em> of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#example-input',
                'iodoc': 'example-input'
            },
        },
        'predict': {
            'method': 'POST',
            'url': '/models/{}/predict',
            'decorators': _execute_model_decorators('predictions'),
            'description': (
                'Execute the <em>predict</em> capability of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'regress': {
            'method': 'POST',
            'url': '/models/{}/regress',
            'decorators': _execute_model_decorators('result'),
            'description': (
                'Execute the <em>regress</em> capability of the named  <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'classify': {
            'method': 'POST',
            'url': '/models/{}/classify',
            'decorators': _execute_model_decorators('result'),
            'description': (
                'Execute the <em>classification</em> capability of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'remove': {
            'method': 'DELETE',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Remove the named <em>BYOML Model</em>',
            'links': {
                'doc': '#deleting-a-model',
                'iodoc': 'deleting-a-model'
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """Create a ModelResource."""
        kwargs.pop('timeout', None)
        super().__init__(*args, timeout=DEFAULT_BYOML_MODEL_TIMEOUT, **kwargs)

    def _get_files_to_zip(self, file_or_dir: PathLike) -> List[Tuple[str, str]]:
        """Get the filenames to zip and the name it should have in the zipfile."""
        file_or_dir = str(file_or_dir)
        if not os.path.isdir(file_or_dir):
            # single file
            zip_file_name = os.path.basename(file_or_dir)
            return [(file_or_dir, zip_file_name)]

        file_names: List[Tuple[str, str]] = []
        for root, _, files in os.walk(file_or_dir):
            for file_name in files:
                # the root will always contain the same suffix, which should not end up in the zip
                zip_root = root[len(file_or_dir):]
                zip_file_name = os.path.join(zip_root, file_name)

                file_path = os.path.join(root, file_name)

                file_names.append((file_path, zip_file_name))

        return file_names

    def _send_model_arguments(
        self, model_name: str, trained_model: Union[PathLike, ByomlModel],
        framework: str = "sklearn", description: str = "",
        work_dir: Optional[PathLike] = None
    ):
        """Upload a binary model with given name, framework and description."""
        if work_dir:
            model_zip_buffer = self._save_model_in_dir(trained_model, work_dir, framework)
        else:
            with tempfile.TemporaryDirectory() as work_dir:
                model_zip_buffer = self._save_model_in_dir(trained_model, work_dir, framework)
        return {
            'body': {
                "name": model_name,
                "framework": framework,
                "description": description
            },
            'files': {
                "file": ('model.zip', model_zip_buffer.getvalue())
            },
        }

    def _save_model_in_dir(
        self, trained_model: Union[PathLike, ByomlModel], work_dir: PathLike, framework: str
    ):
        if not isinstance(trained_model, (str, os.PathLike)):
            file_name = self._serialize_model(trained_model, work_dir, framework)
            files = self._get_files_to_zip(file_name)
        else:
            files = self._get_files_to_zip(trained_model)

        model_zip_buffer = BytesIO()
        with ZipFile(model_zip_buffer, 'w') as zipper:
            for file_name, zip_file_name in files:
                zipper.write(file_name, zip_file_name)

        return model_zip_buffer

    def _serialize_model(
        self, trained_model: ByomlModel, work_dir: PathLike, framework: str
    ) -> PathLike:
        assert_dir_exists(work_dir)

        framework_function = SUPPORTED_FRAMEWORKS.get(framework, None)
        if framework_function is not None:
            return framework_function(work_dir, trained_model)

        raise ByomlValidationError(
            f'Passing a model instance is not supported for this `{framework}` model, '
            'please provide the path to the saved model instead.'
        )

    @suppress_header_decorator('Content-Type')
    def upload(
        self,
        model_name: str,
        trained_model: Union[PathLike, ByomlModel],
        framework: str = "sklearn",
        description: str = "",
        work_dir: Optional[PathLike] = None,
        **kwargs
    ) -> Any:
        """Upload a new machine learning model with given name, framework and description.

        Parameters:
            model_name      The name of the model.
            trained_model   The model object (will be serialised to an zip archive before upload),
                            or a file path to the serialized model file or folder.
            framework       One of the supported frameworks (default 'sklearn').
            description     Description of the model.
            work_dir        Optional location of the working directory used to serialize the model.
                            If not specified, a temporary directory is used.
            (other args)    Passed onto the underlying 'POST /model/{name}' request
        """
        return self._create(  # pylint: disable=no-member
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework,
                description=description,
                work_dir=work_dir,
            ),
            **kwargs
        )

    @suppress_header_decorator('Content-Type')
    def replace(
        self,
        model_name: str,
        trained_model: Union[PathLike, ByomlModel],
        framework: str = "sklearn",
        description: str = "",
        work_dir: Optional[PathLike] = None,
        **kwargs
    ) -> Any:
        """Replace a machine learning model with given name, framework and description.

        Parameters:
            model_name      The name of the model.
            trained_model   The model object (will be serialised to an zip archive before upload).
            framework       One of the supported frameworks (default 'sklearn').
            description     Description of the model.
            work_dir        Optional location of the working directory used to serialize the model.
                            If not specified, a temporary directory is used.
            (other)         Passed onto the underlying 'PUT /model/{name}' request.
        """
        return self._replace(   # pylint: disable=no-member
            model_name,
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework,
                description=description,
                work_dir=work_dir,
            ),
            **kwargs
        )
