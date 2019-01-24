
import click
from pycman import config
import eyapm


def search_pkgname(handle, pkgname):

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


def search_filenames(handle, filenames):
    localpkgs = handle.get_localdb().pkgcache

    for name in filenames:
        for pkg in localpkgs:
            files = pkg.files
            for fp in files:
                if name in fp[0]:
                    print("/%s is owned by %s" % (
                        fp[0], pkg.name
                    ))


@click.command('search')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.option(
    '--files', 'search_files', is_flag=True, default=False
)
@click.argument('pkgname_or_filename', nargs=-1, required=True)
def cli(ctx, config_file, search_files, pkgname_or_filename):
    handle = config.init_with_config(config_file)

    if not search_files:
        search_pkgname(handle, pkgname_or_filename[0])
        return

    search_filenames(handle, pkgname_or_filename)
