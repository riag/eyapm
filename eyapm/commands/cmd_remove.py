
import click
from pycman import config

import eyapm
from eyapm import transaction


def remove_pkgs(handle, quiet, pkgnames):
    db = handle.get_localdb()
    targets = []

    for name in pkgnames:
        pkg = db.get_pkg(name)
        if pkg is None:
            print('error: target not found: %s' % name)
            return

        targets.append(pkg)

    t = transaction.create_transaction(
        handle,
        {}
    )

    with eyapm.util.work_with_transaction(t):
        print('')

        for pkg in targets:
            t.remove_pkg(pkg)

        t.prepare()

        if len(t.to_remove) == 0:
            print('Nothing to do.')
            return

        total_remove_size = 0
        for pkg in t.to_remove:
            total_remove_size += pkg.isize

        print('')
        package_name_list = [x.name for x in t.to_remove]
        print('Packages (%d) %s\n' % (
            len(t.to_remove), ' '.join(package_name_list)
        ))
        print('')

        size_str = '{:.2f}'.format(
                total_remove_size/1024/1024
        )
        print('Total Removed Size:   %s MiB' % size_str)

        answer = 'y'
        if not quiet:
            print('')
            answer = input(':: Do you want to remove these packages? [Y/n] ')
            if not answer:
                answer = 'y'
            else:
                answer = answer.lower()

        if answer in ('y', 'yes'):
            t.commit()
            return


@click.command('remove')
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

    remove_pkgs(handle, quiet, pkgnames)
