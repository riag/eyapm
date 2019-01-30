
import click
import sys
from pycman import config
from pycman import pkginfo
import eyapm

print_fmt = '{:<40}\t{}'


def list_installed_packages(handle, pkgnames, show_detail):
    db = handle.get_localdb()
    pkglist = []
    if not pkgnames:
        pkglist = db.pkgcache
    else:
        for name in pkgnames:
            pkg = db.get_pkg(name)
            if not pkg:
                print('error: package %s was not found' % name)
                sys.exit(-1)

            pkglist.append(pkg)

    if not show_detail:
        for pkg in pkglist:
            s = print_fmt.format(
                pkg.name, pkg.version
            )
            print(s)
    else:
        for pkg in pkglist:
            pkginfo.display_pkginfo(pkg, 2)


def find_remote_package(name, syncdbs):
    if '/' in name:
        repo, pkgname = name.spit('/', 1)
        db = syncdbs.get(repo)
        if db is None:
            print("repository '%s' does not exist" % repo)
            sys.exit(-1)
        pkg = db.get_pkg(name)
        if pkg is None:
            print("error: package %s was not found in repository %s" % (
                name, repo
            ))
        return pkg

    for db in syncdbs:
        pkg = db.get_pkg(name)
        if pkg is not None:
            return pkg

    return None


def list_remote_packages(handle, pkgnames, show_detail):
    repos = handle.get_syncdbs()
    pkglist = []
    if not pkgnames:
        for repo in repos:
            pkglist.extend(repo.pkgcache)
    else:
        for name in pkgnames:
            pkg = find_remote_package(name, repos)
            if pkg is None:
                print('error: package %s was not found' % name)
                sys.exit(-1)

            pkglist.append(pkg)

    if not show_detail:
        for pkg in pkglist:
            s = print_fmt.format(
                pkg.name, pkg.version
            )
            print(s)
    else:
        for pkg in pkglist:
            pkginfo.display_pkginfo(pkg, 2, 'sync')


@click.command('list')
@click.pass_context
@click.option(
            '--config-file', 'config_file',
            default=eyapm.default.config_file
        )
@click.option(
    '-i', '--installed', 'list_installed',
    is_flag=True, default=False)
@click.option('--detail', 'show_detail', is_flag=True, default=False)
@click.argument('pkgnames', nargs=-1)
def cli(ctx, config_file, list_installed, show_detail, pkgnames):
    handle = config.init_with_config(config_file)

    if list_installed:
        return list_installed_packages(handle, pkgnames, show_detail)

    return list_remote_packages(handle, pkgnames, show_detail)
