from functools import wraps
import json
import os

from fabric.api import env, execute, local, task
from fabric.context_managers import prefix, quiet

env.appname = env.get('appname', '{{ cookiecutter.project_slug }}')
env.profile = env.get('profile', 'devsoc-serverless')
env.stage = env.get('stage', 'production')


@task
def demo():
    """
    Load demo environment settings.
    """
    env.stage = 'demo'


def aws_vault(func):
    """
    Wrapper to load environment variables from aws-vault
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.environ.get('AWS_SECRET_ACCESS_KEY') is None:
            aws_json = local('aws-vault exec {} --json'.format(env.profile), capture=True)
            aws_dict = json.loads(aws_json)

            os.environ['AWS_ACCESS_KEY_ID'] = aws_dict['AccessKeyId']
            os.environ['AWS_SECRET_ACCESS_KEY'] = aws_dict['SecretAccessKey']
            os.environ['AWS_SESSION_TOKEN'] = aws_dict['SessionToken']

        func(*args, **kwargs)

    return wrapper


@task
@aws_vault
def deploy():
    """
    Deploy to AWS.
    """
    local('npm run serverless -- deploy --stage {}'.format(env.stage))


@task
@aws_vault
def lambda_env(name=None, value=None):
    """
    Update SSM environment variables.

    Setting a variable:

      fab lambda_env:name=ENV_VAR_NAME,value=env_var_value

    Getting a single variable:

      fab lambda_env:name=ENV_VAR_NAME

    Listing all variables:

      fab lambda_env
    """
    stack_name = '{}-{}'.format(env.appname, env.stage)

    if name is None and value is None:
        # List parameters
        local(
            'aws ssm get-parameters-by-path '
            '--region eu-west-2 '
            '--path "/serverless/{}/" '
            '--with-decryption'.format(stack_name)
        )
    elif value is None:
        # Get parameter
        local(
            'aws ssm get-parameter '
            '--region eu-west-2 '
            '--name "/serverless/{}/{}" '
            '--with-decryption'.format(stack_name, name)
        )
    else:
        # Set parameter
        local(
            'aws ssm put-parameter '
            '--region eu-west-2 '
            '--name "/serverless/{}/{}" '
            '--type SecureString '
            '--value "{}" '
            '--overwrite'.format(stack_name, name, value)
        )


@task
@aws_vault
def invoke(name):
    """
    Invoke a lambda function.

    Examples:

      fab invoke:function_name

      fab invoke:name=function_name
    """
    local('npm run serverless -- invoke --stage {} --function {}'.format(env.stage, name))
