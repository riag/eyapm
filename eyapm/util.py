
import contextlib
import pyalpm
from eyapm import transaction
import os
import sys


@contextlib.contextmanager
def work_with_transaction(t):
    try:
        yield
    finally:
        t.release()


def find_remote_package(syncdbs, name):
    if '/' in name:
        repo, pkgname = name.spit('/', 1)
        db = syncdbs.get(repo)
        if db is None:
            print("repository '%s' does not exist" % repo)
            return None
        pkg = db.get_pkg(name)
        #if pkg is None:
            #print("error: package %s was not found in repository %s" % (
            #    name, repo
            #))
        return pkg

    for db in syncdbs:
        pkg = db.get_pkg(name)
        if pkg is not None:
            return pkg

    return None


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

        with work_with_transaction(t):
            if not db.update(False):
                print(' %s is up to date' % db.name)
