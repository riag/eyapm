
import click
import eyapm
from pycman import config
from pycman import pkginfo


@click.command('info')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.argument('pkgnames', nargs=-1, required=True)
def cli(ctx, config_file, pkgnames):

    handle = config.init_with_config(config_file)
    syncdbs = handle.get_syncdbs()
    db = handle.get_localdb()

    for name in pkgnames:
        pkg = eyapm.util.find_remote_package(syncdbs, name)
        if pkg is None:
            print('Error: target not found: %s' % name)
            continue

        local_pkg = db.get_pkg(name)
        if local_pkg:
            pkginfo.display_pkginfo(pkg, 2, 'local')
        else:
            pkginfo.display_pkginfo(pkg, 2, 'sync')

        print('')
