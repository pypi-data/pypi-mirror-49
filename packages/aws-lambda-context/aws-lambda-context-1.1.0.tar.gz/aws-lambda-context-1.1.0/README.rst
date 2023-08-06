Python Lambda Context
=====================

A micro library that provides the AWS Lambda Context class for type checking and testing.

Installing
----------

.. code-block::

    pip install aws-lambda-context

Usage
-----

Import the LambdaContext on your handler file and type hint the lambda function with it:

.. code-block:: python

    from aws_lambda_context import LambdaContext

    def my_lambda_handler(event: Any, context: LambdaContext) -> None:
        ...

The type hint should enables type checking with mypy_ and editor auto-completion

The class is also useful as a mock during tests:

.. code-block:: python

    from aws_lambda_context import (
        LambdaClientContext,
        LambdaClientContextMobileClient,
        LambdaCognitoIdentity,
        LambdaContext
    )

    def test_handler():
        lambda_cognito_identity = LambdaCognitoIdentity()
        lambda_cognito_identity.cognito_identity_id = 'cognito_identity_id'
        lambda_cognito_identity.cognito_identity_pool_id = 'cognito_identity_pool_id'

        lambda_client_context_mobile_client = LambdaClientContextMobileClient()
        lambda_client_context_mobile_client.installation_id = 'installation_id'
        lambda_client_context_mobile_client.app_title = 'app_title'
        lambda_client_context_mobile_client.app_version_name = 'app_version_name'
        lambda_client_context_mobile_client.app_version_code = 'app_version_code'
        lambda_client_context_mobile_client.app_package_name = 'app_package_name'

        lambda_client_context = LambdaClientContext()
        lambda_client_context.client = lambda_client_context_mobile_client
        lambda_client_context.custom = {'custom': True}
        lambda_client_context.env = {'env': 'test'}

        lambda_context = LambdaContext()
        lambda_context.function_name = 'function_name'
        lambda_context.function_version = 'function_version'
        lambda_context.invoked_function_arn = 'invoked_function_arn'
        lambda_context.memory_limit_in_mb = 'memory_limit_in_mb'
        lambda_context.aws_request_id = 'aws_request_id'
        lambda_context.log_group_name = 'log_group_name'
        lambda_context.log_stream_name = 'log_stream_name'
        lambda_context.identity = lambda_cognito_identity
        lambda_context.client_context = lambda_client_context

        assert handler({}, lambda_context) == 'something'

References
----------

- https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

.. _mypy: http://mypy-lang.org/