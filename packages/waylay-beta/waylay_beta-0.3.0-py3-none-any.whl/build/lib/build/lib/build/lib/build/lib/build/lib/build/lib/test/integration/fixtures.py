"""Reusable test fixtures."""
import os
from typing import Any, Tuple

import pytest
import pandas as pd
import numpy as np

from waylay import ClientCredentials, WaylayClient
from waylay.auth import WaylayTokenAuth
from waylay.service import ApiService, StorageService, DataService


def get_test_env(key: str, default: str = None) -> str:
    """Get an environment variable."""
    test_var = os.getenv(key, default)
    if not test_var:
        raise AttributeError(f'{key} environment variable not configured, while test requires it.')
    return test_var


@pytest.fixture(scope='session')
def waylay_test_profile():
    """Get environment variable WAYLAY_TEST_PROFILE."""
    return get_test_env('WAYLAY_TEST_PROFILE')


@pytest.fixture(scope='session')
def waylay_test_user_id():
    """Get environment variable WAYLAY_TEST_USER_ID."""
    return get_test_env('WAYLAY_TEST_USER_ID')


@pytest.fixture(scope='session')
def waylay_test_user_secret():
    """Get environment variable WAYLAY_TEST_USER_SECRET."""
    return get_test_env('WAYLAY_TEST_USER_SECRET')


@pytest.fixture(scope='session')
def waylay_test_accounts_url():
    """Get environment variable WAYLAY_TEST_ACCOUNTS_URL or 'https://accounts-api-staging.waylay.io'."""
    return get_test_env('WAYLAY_TEST_ACCOUNTS_URL', 'https://accounts-api-staging.waylay.io')


@pytest.fixture(scope='session')
def waylay_test_client_credentials(waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url):
    """Get client credentials.

    As specified in the environment variables
    WAYLAY_TEST_USER_ID, WAYLAY_TEST_USER_SECRET, WAYLAY_TEST_ACCOUNTS_URL
    """
    return ClientCredentials(
        waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url
    )


@pytest.fixture(scope='session')
def waylay_test_token_string(waylay_test_client_credentials):
    """Get a valid token string."""
    token = WaylayTokenAuth(waylay_test_client_credentials).assure_valid_token()
    return token.token_string


@pytest.fixture(scope='session')
def waylay_session_test_client(waylay_test_client_credentials):
    """Get a test waylay SDK client (same for whole session)."""
    waylay_client = WaylayClient.from_credentials(waylay_test_client_credentials)
    return waylay_client


@pytest.fixture
def waylay_test_client(waylay_test_client_credentials):
    """Get a test waylay SDK client."""
    waylay_client = WaylayClient.from_credentials(waylay_test_client_credentials)
    return waylay_client


@pytest.fixture
def waylay_storage(waylay_test_client: WaylayClient) -> StorageService:
    """Get the storage service."""
    return waylay_test_client.storage  # type: ignore


@pytest.fixture
def waylay_api(waylay_test_client: WaylayClient) -> ApiService:
    """Get the storage service."""
    return waylay_test_client.api  # type: ignore


@pytest.fixture
def waylay_data(waylay_test_client: WaylayClient) -> DataService:
    """Get the storage service."""
    return waylay_test_client.data  # type: ignore


@pytest.fixture
def sklearn_model_and_test_data(
    waylay_test_client: WaylayClient,
    generate_dataset
) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """Get a trained sklearn model and test data."""
    df = generate_dataset

    df_train, df_validate = get_train_validation_set(df)

    # train model
    from sklearn.covariance import EllipticEnvelope   # pylint: disable=import-error
    cov_model = EllipticEnvelope(random_state=0, contamination=0.05).fit(df_train)

    predictions = cov_model.predict(df_validate)
    df_prediction = pd.DataFrame(
        predictions,
        index=df_validate.index
    )
    assert len(df_prediction.index) == len(df_validate.index)
    return cov_model, df_validate, predictions


@pytest.fixture
def generate_dataset():
    """Generate a random dataset consisting of timestamps and temperatures."""
    amount_of_samples = 2500

    data = np.random.randint(0, 25, size=(amount_of_samples, 1))
    index = pd.date_range(name='timestamp', start="2019-01-01", end="2020-12-31", periods=amount_of_samples)
    return pd.DataFrame(data, index=index, columns=['temperature'])


@pytest.fixture
def generate_labels():
    """Generate a random dataset consisting of timestamps and temperatures."""
    amount_of_samples = 2500

    data = np.random.randint(0, 5, size=(amount_of_samples, 1))
    return pd.DataFrame(data, columns=['labels'])


def get_train_validation_set(df: pd.DataFrame, split_percentage=0.8, labels: pd.DataFrame = None):
    """Split the complete dataframe in two parts."""
    train_size = int(len(df.index) * split_percentage)
    df_train = df.iloc[:train_size]
    df_validate = df.iloc[train_size:]

    if labels is not None:
        labels_train = labels.iloc[:train_size]
        labels_validate = labels.iloc[:train_size]
        return df_train, df_validate, labels_train, labels_validate

    return df_train, df_validate


@pytest.fixture
def tensorflow_model_and_test_data(
    waylay_test_client: WaylayClient,
    generate_dataset,
    generate_labels
) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """Get a trained TensorFlow model and test data."""
    df = generate_dataset
    labels = generate_labels

    df_train, df_validate, labels_train, _ = get_train_validation_set(df, labels=labels)

    # Tensorflow has a lot of DeprecationWarnings, we don't want these in our test
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)

    import tensorflow as tf  # pylint: disable=import-error

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(1, 1)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(5),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    X_train = np.expand_dims(df_train, axis=2)
    X_val = np.expand_dims(df_validate, axis=2)

    model.fit(X_train, labels_train, epochs=1)

    predictions = model.predict(X_val)
    df_prediction = pd.DataFrame(
        predictions,
        index=df_validate.index
    )
    assert len(df_prediction.index) == len(df_validate.index)

    return model, df_validate, predictions


@pytest.fixture
def pytorch_model_and_test_data(
    waylay_test_client: WaylayClient,
    generate_dataset,
    generate_labels
) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """Get a trained XGBoost model and test data."""
    df = generate_dataset
    labels = generate_labels

    df_train, df_validate, labels_train, _ = get_train_validation_set(df, labels=labels)

    import torch  # pylint: disable=import-error

    train_tensor = torch.tensor(df_train.values)  # pylint: disable=not-callable
    labels_tensor = torch.tensor(labels_train.values)  # pylint: disable=not-callable
    validation_tensor = torch.tensor(df_validate.values)  # pylint: disable=not-callable

    model = torch.nn.Sequential(
        torch.nn.Linear(1, 1),
        torch.nn.Flatten(1, 1)
    )

    loss_fn = torch.nn.MSELoss(reduction='sum')
    learning_rate = 1e-3
    optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)

    for t in range(1):
        y_pred = model(train_tensor.float())

        loss = loss_fn(y_pred, labels_tensor.float())

        optimizer.zero_grad()

        loss.backward()
        optimizer.step()

    predictions = model(validation_tensor.float())
    assert predictions.size() == validation_tensor.size()

    return model, validation_tensor, predictions.detach().numpy()


@pytest.fixture
def pytorch_custom_model_and_test_data(
    waylay_test_client: WaylayClient
) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """Get a trained PyTorch model and test data."""
    import torch  # pylint: disable=import-error

    class CustomReLu(torch.autograd.Function):
        """Implement a custom autograd Function."""

        @staticmethod
        def forward(context, input: torch.Tensor) -> torch.Tensor:
            context.save_for_backward(input)
            return input.clamp(min=0)

        @staticmethod
        def backward(context, grad_output: torch.Tensor) -> torch.Tensor:
            input, = context.saved_tensors
            grad_input = grad_output.clone()
            grad_input[input < 0] = 0
            return grad_input

    batch_size, input_dim = 32, 1
    dtype = torch.float  # pylint: disable=no-member

    x = torch.randn(batch_size, input_dim, dtype=dtype)  # pylint: disable=no-member

    relu = CustomReLu.apply
    script = torch.jit.trace(relu, torch.randn(batch_size, input_dim, dtype=dtype))  # pylint: disable=no-member
    local_output = relu(x)

    return relu, x, local_output.detach().numpy()


@pytest.fixture
def xgboost_model_and_test_data(
    waylay_test_client: WaylayClient,
    generate_dataset,
    generate_labels
) -> Tuple[Any, pd.DataFrame, np.ndarray]:
    """Get a trained sklearn model and test data."""
    df = generate_dataset
    labels = generate_labels

    df_train, df_validate, labels_train, labels_validate = get_train_validation_set(df, labels=labels)

    # train model
    import xgboost as xgb  # pylint: disable=import-error

    dtrain = xgb.DMatrix(df_train, label=labels_train)
    dtest = xgb.DMatrix(df_validate, label=labels_validate)

    param = {
        'max_depth': 3,
        'learning_rate': 0.1,
        'colsample_bytree': 0.3,
        'objective': 'binary:hinge'
    }
    num_round = 100
    bst = xgb.train(param, dtrain, num_round)

    predictions = bst.predict(dtest)

    assert len(predictions) == len(df_validate.index)

    return bst, df_validate, predictions
