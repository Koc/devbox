import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='ssh')
@click.argument('service', required=False)
@click.pass_context
def execute(ctx, service):
    """
    Connect by ssh to the given service
    """
    from subprocess import call
    from ..utils.docker import DockerHelper, get_default_service, get_env
    from ..utils.cwd import CwdHelper

    if not service:
        service = get_default_service(CwdHelper().get_compose_path())

    # call('ssh-keygen -R %s' % service)
    # pass password https://gist.github.com/virtuald/54c8657a9ea834fb7fdd
    docker_helper = DockerHelper()
    container = docker_helper.get_container(service)
    user = get_env(container, 'CONTAINER_USER') or 'dev'

    # ssh_exec_pass('112233', ['ssh', 'root@1.2.3.4', 'echo hi!'])
    # ssh(service, '', user, '112233')

    cmd = 'ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" {0}@{1}'.format(user, service)
    call(cmd, shell=True)
