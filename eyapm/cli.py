
import os
import pkg_resources
import click
import eyapm
import pyalpm

# aptitude 的参数选项
# https://wiki.debian.org/Aptitude
# pacman 与 其他包管理器的参数对比
# https://wiki.archlinux.org/index.php/Pacman/Rosetta

CMD_DIR = pkg_resources.resource_filename(__name__, 'commands')


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--version', 'show_version', is_flag=True, default=False)
def eyapmcli(ctx, show_version):
    ctx.ensure_object(dict)

    if show_version:
        msg_list = []
        msg_list.append('eyapm   version is %s' % eyapm.__version__)
        msg_list.append('pyalpm  version is %s' % pyalpm.version())
        msg_list.append('libalpm version is %s' % pyalpm.alpmversion())
        print('\n'.join(msg_list))


def list_command(cmd_dir):
    rv = []
    for filename in os.listdir(cmd_dir):
        if filename.endswith('.py') and \
                filename.startswith('cmd_'):
            rv.append(filename[4:-3])

    rv.sort()
    return rv


def find_and_import_commands():
    rv = list_command(CMD_DIR)
    for name in rv:
        mod = __import__(
            'eyapm.commands.cmd_%s' % name,
            None, None, ['cli', 'default_config']
            )
        eyapmcli.add_command(mod.cli)


def main():
    find_and_import_commands()
    eyapmcli(obj={})


if __name__ == '__main__':
    main()
