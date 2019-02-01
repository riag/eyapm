
import click
from pycman import config

import sys

import eyapm
from eyapm import transaction


# pamac 工具里，会在 prepare 之前
# 查看 pkg 是否有 opt dept，如果有，会询问用户是否安装 opt dept
# 参见 https://gitlab.manjaro.org/applications/pamac/blob/master/src/transaction.vala

def install_pkgnames(handle, syncdbs, quiet, force_install, pkgnames):
    targets = []
    for name in pkgnames:
        pkg = eyapm.util.find_remote_package(syncdbs, name)
        if pkg is None:
            print("package '%s' was not found" % name)
            sys.exit(-1)

        targets.append(pkg)

    t = transaction.create_transaction(
        handle,
        {'needed': not force_install}
    )

    with eyapm.util.work_with_transaction(t):
        print('')
        print('Preparing...')
        for pkg in targets:
            t.add_pkg(pkg)

        transaction.prepare(t)
        if len(t.to_add) == 0:
            print('Nothing to do.')
            return

        total_install_size = 0
        total_download_size = 0
        for x in t.to_add:
            total_install_size += x.isize
            total_download_size += x.download_size

        print('')
        package_name_list = [x.name for x in t.to_add]
        print('Packages (%d) %s\n' % (
            len(t.to_add), ' '.join(package_name_list)
        ))
        size_str = '{:.2f}'.format(
                total_install_size/1024/1024
        )
        s = 'Total Installed Size: {:>8} MiB'.format(
            size_str
        )
        print(s)
        size_str = '{:.2f}'.format(
                total_download_size/1024/1024
        )
        s = 'Net Upgrade Size:     {:>8} MiB'.format(
            size_str
        )
        print(s)
        print('')

        answer = 'y'
        if not quiet:
            answer = input(':: Proceed with installation? [Y/n] ')
            if not answer:
                answer = 'y'
            else:
                answer = answer.lower()

        if answer in ('y', 'yes'):
            t.commit()
            return


@click.command('install')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.option(
    '-y', '--yes', 'quiet', is_flag=True, default=False
)
@click.option(
    '--force', 'force_install', is_flag=True, default=False
)
@click.argument('pkgnames', nargs=-1, required=True)
def cli(ctx, config_file, quiet, force_install, pkgnames):
    handle = config.init_with_config(config_file)
    syncdbs = handle.get_syncdbs()

    eyapm.util.sync_dbs(handle, syncdbs)

    install_pkgnames(
        handle, syncdbs, quiet,
        force_install, pkgnames
        )
