# ruff: noqa
from fabric.api import env, local, task
from fabric.context_managers import quiet

env.appname = env.get("appname", "{{ cookiecutter.project_slug }}")
env.arch = env.get("arch", "linux/{% if cookiecutter.arch == 'arm64' %}arm64{% else %}amd64{% endif %}")
env.profile = env.get("profile", "devsoc-serverless")
env.stage = env.get("stage", "production")


@task
def demo():
    """
    Load demo environment settings.
    """
    env.stage = "demo"


def aws_vault(command, capture=False, shell=None):
    """
    Run aws-vault locally with the given profile.
    """
    vault_command = "aws-vault exec {} -- {}".format(env.profile, command)
    return local(vault_command, capture=capture, shell=shell)


@task
def deploy():
    """
    Deploy to AWS.
    """
    service_name = "{}-{}".format(env.appname, env.stage)

    with quiet():
        aws_vault(
            "aws ecr create-repository --repository-name {}".format(service_name),
        )

    image_url = aws_vault(
        "aws ecr describe-repositories "
        "--repository-name {} "
        "--output=text "
        "--query=repositories[0].repositoryUri".format(service_name),
        capture=True,
    )
    repository_hostname = image_url.split("/")[0]

    aws_vault(
        "aws ecr get-login-password | docker login --username AWS --password-stdin {}".format(
            repository_hostname,
        )
    )

    # Build with a fresh environment to avoid uncommitted files or cruft
    sentry_release = local("git rev-parse HEAD", capture=True)
    local(
        "git archive HEAD | "
        "docker buildx build --build-arg SENTRY_RELEASE={} --push --platform={} --tag={} -".format(
            sentry_release,
            env.arch,
            image_url,
        )
    )

    aws_vault("npm run serverless -- deploy --stage {}".format(env.stage))
    aws_vault("npm run serverless -- info --verbose --stage {}".format(env.stage))


@task
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
    service_name = "{}-{}".format(env.appname, env.stage)

    if name is None and value is None:
        # List parameters
        aws_vault(
            "aws ssm get-parameters-by-path "
            "--region eu-west-2 "
            '--path "/serverless/{}/" '
            "--with-decryption".format(service_name)
        )
    elif value is None:
        # Get parameter
        aws_vault(
            "aws ssm get-parameter "
            "--region eu-west-2 "
            '--name "/serverless/{}/{}" '
            "--with-decryption".format(service_name, name)
        )
    else:
        # Set parameter
        aws_vault(
            "aws ssm put-parameter "
            "--region eu-west-2 "
            '--name "/serverless/{}/{}" '
            "--type SecureString "
            '--value "{}" '
            "--overwrite".format(service_name, name, value)
        )


@task
def invoke(name):
    """
    Invoke a lambda function.

    Examples:

      fab invoke:function_name

      fab invoke:name=function_name
    """
    aws_vault("npm run serverless -- invoke --stage {} --function {}".format(env.stage, name))
