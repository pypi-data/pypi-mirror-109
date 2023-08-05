import importlib
import os
import sys


def context():
    class FakeContext:
        function_name = "FUNCTION_NAME"
        memory_limit_in_mb = 1024
        invoked_function_arn = "INVOKED_FUNCTION_ARN"
        aws_request_id = "AWS_REQUEST_ID"
        log_group_name = "LOG_GROUP_NAME"
        log_stream_name = "LOG_STREAM_NAME"

        def get_remaining_time_in_millis(self):
            # 5 minutes
            return 300000

    return FakeContext()


def load_lambda_module(request):
    # Inject environment variables
    backup_environ = {}
    for key, value in request.param.get("environ", {}).items():
        if key in os.environ:
            backup_environ[key] = os.environ[key]
        os.environ[key] = value

    # Add path for Lambda function
    sys.path.insert(
        0, os.path.dirname(os.path.abspath(request.param["module_name"]))
    )

    # Save the list of previously loaded modules
    prev_modules = list(sys.modules.keys())

    # Return the function module
    module = importlib.import_module(request.param["module_name"])
    yield module

    # Delete newly loaded modules
    new_keys = list(sys.modules.keys())
    for key in new_keys:
        if key not in prev_modules:
            del sys.modules[key]

    # Delete function module
    del module

    # Remove the Lambda function from path
    sys.path.pop(0)

    # Restore environment variables
    for key in request.param.get("environ", {}).keys():
        if key in backup_environ:
            os.environ[key] = backup_environ[key]
        else:
            del os.environ[key]
