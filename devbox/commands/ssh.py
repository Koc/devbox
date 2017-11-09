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
    import docker
    from devbox.utils.docker import get_default_service, get_env
    from devbox.utils.cwd import ensure_docker_compose_dir
    from devbox.utils.sshpass import ssh

    cwd = ensure_docker_compose_dir()
    service = service or get_default_service()

    #call('ssh-keygen -R %s' % service)
    # pass password https://gist.github.com/virtuald/54c8657a9ea834fb7fdd
    container = docker.from_env().containers.get(service)
    user = get_env(container, 'CONTAINER_USER') or 'dev'

    # ssh_exec_pass('112233', ['ssh', 'root@1.2.3.4', 'echo hi!'])
    # ssh(service, '', user, '112233')

    call('ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" {0}@{1}'
         .format(user, service))