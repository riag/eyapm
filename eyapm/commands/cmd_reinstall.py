

import click
from pycman import config

import eyapm
from eyapm import transaction


def reinstall_pkgs(handle, quiet, pkgnames):
    local_db = handle.get_localdb()
    syncdbs = handle.get_syncdbs()

    targets = []
    for name in pkgnames:
        local_pkg = local_db.get_pkg(name)
        if local_pkg is None:
            print('error: target not found: %s' % name)
            return

        sync_pkg = eyapm.util.find_remote_package(syncdbs, local_pkg.name)
        if sync_pkg is None:
            print('error: target not found: %s' % name)
            return

        if sync_pkg.version != local_pkg.version:
            print('error: target not found: %s-%s' % (
                name, local_pkg.version
            ))
            return

        targets.append(sync_pkg)

    if not targets:
        print('Nothing to do.')
        return

    t = transaction.create_transaction(
        handle,
        {'needed': False}
    )

    with eyapm.util.work_with_transaction(t):
        print('')
        print('Preparing...')

        for pkg in targets:
            t.add_pkg(pkg)

        t.prepare()
        if len(t.to_add) == 0:
            print('Nothing to do.')
            return

        max_pkg_name_len = 0
        for pkg in t.to_add:
            l = len(pkg.name)
            if l > max_pkg_name_len:
                max_pkg_name_len = l

        print('To reinstall (%d) :' % len(t.to_add))
        fmt = '  {:<%d}  {:<10}  {}' % max_pkg_name_len
        for pkg in t.to_add:
            s = fmt.format(
                pkg.name,
                pkg.version,
                pkg.db.name
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


@click.command('reinstall')
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
    syncdbs = handle.get_syncdbs()

    eyapm.util.sync_dbs(handle, syncdbs)

    reinstall_pkgs(handle, quiet, pkgnames)
