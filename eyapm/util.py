
import contextlib


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
