
import click
from pycman import config
import pyalpm

import sys
import os

import eyapm
from eyapm import transaction


def sync_dbs(handle, syncdbs):
    print(':: Synchronizing package databases...')
    for db in syncdbs:
        t = None
        try:
            t = transaction.init_from_options(handle)
        except pyalpm.error as e:
            print('')
            print(e)
            if os.path.exists(handle.lockfile):
                print('%s is exist' % handle.lockfile)
            sys.exit(-1)

        with eyapm.util.work_with_transaction(t):
            if not db.update(False):
                print(' %s is up to date' % db.name)


def install_pkgnames(handle, syncdbs, quiet, pkgnames):
    targets = []
    for name in pkgnames:
        pkg = eyapm.util.find_remote_package(syncdbs, name)
        if pkg is None:
            print("package '%s' was not found" % name)
            sys.exit(-1)

        targets.append(pkg)

    t = transaction.create_transaction(handle)

    # :: Proceed with installation? [Y/n]
    with eyapm.util.work_with_transaction(t):
        for pkg in targets:
            t.add_pkg(pkg)
        try:
            transaction.prepare(t)
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

            answer = answer.lower()

            if answer in ('y', 'yes'):
                t.commit()
                return

        except pyalpm.error as e:
            print("")
            print(e)
            sys.exit(-1)
        except Exception as e:
            print(e)


@click.command('install')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.option(
    '-y', '--yes', 'quiet', is_flag=True, default=False
)
@click.argument('pkgnames', nargs=-1, required=True)
def cli(ctx, config_file, quiet, pkgnames):
    handle = config.init_with_config(config_file)
    print(handle.lockfile)
    syncdbs = handle.get_syncdbs()

    sync_dbs(handle, syncdbs)

    install_pkgnames(handle, syncdbs, quiet, pkgnames)
