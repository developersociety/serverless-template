from fabric.api import local as fab_local, task
from fabric.context_managers import prefix, quiet


# We need bash as our local shell to execute commands in (as we're using source)
def local(command, capture=False, shell='/bin/bash'):
    return fab_local(command, capture=capture, shell=shell)


@task
def deploy():
    """
    Deploy to AWS.
    """
    local('virtualenv .zappaenv')

    with prefix('source .zappaenv/bin/activate'):
        local('pip install -r requirements/production.txt')

        with quiet():
            status = local('zappa status production', capture=True)

        if status.succeeded:
            # Already deployed - just update
            local('zappa update production')
        else:
            # First time - full deploy
            local('zappa deploy production')

    local('rm -rf .zappaenv')
