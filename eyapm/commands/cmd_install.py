
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
            if not db.update(True):
                print(' %s is up to date' % db.name)


def install_pkgnames(handle, syncdbs, pkgnames):
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
            r = t.prepare()
            print(dir(t))
            print(r)
            for x in t.to_add:
                print(x)
            t.commit()
        except pyalpm.error as e:
            print("")
            print(e)
            sys.exit(-1)
        except Exception as e:
            print(e)
            t.interrupt()


@click.command('install')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.argument('pkgnames', nargs=-1, required=True)
def cli(ctx, config_file, pkgnames):
    handle = config.init_with_config(config_file)
    print(dir(handle))
    print(handle.lockfile)
    syncdbs = handle.get_syncdbs()

    sync_dbs(handle, syncdbs)
    return

    install_pkgnames(handle, syncdbs, pkgnames)
