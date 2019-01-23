
import click
from pycman import config
import eyapm


@click.command('search')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.argument('pkgname', nargs=1, required=True)
def cli(ctx, config_file, pkgname):
    handle = config.init_with_config(config_file)
    local_db = handle.get_localdb()
    repos = handle.get_syncdbs()
    pkglist = []
    for repo in repos:
        result = repo.search(pkgname)
        if result:
            pkglist.extend(result)

    for pkg in pkglist:
        name = pkg.name
        if local_db.get_pkg(name):
            name = '%s(installed)' % name
        print('%s \t\t %s \t\t %s \t\t %s' % (
            name, pkg.version,
            pkg.db.name, pkg.desc
        ))
