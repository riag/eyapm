
import pyalpm
import sys
import os
from tqdm import tqdm
from tqdm._utils import _environ_cols_wrapper
from eyapm import event

cols = _environ_cols_wrapper()(sys.stdout)

_last_operation_action = None

_current_operate_pkg_map = {}


def _start_operation_action(*args):
    event_str = args[1]
    global _last_operation_action
    if event_str.startswith('Adding'):
        _last_operation_action = 'installing'
    elif event_str.startswith('Upgrading'):
        _last_operation_action = 'upgrading'
    elif event_str.startswith('Reinstalling'):
        _last_operation_action = 'reinstalling'
    elif event_str.startswith('Downgrading'):
        _last_operation_action = 'downgrading'
    elif event_str.startswith('Removing'):
        _last_operation_action = 'removing'


def _start_check_keyring(*args):
    global _last_pg_desc
    _last_pg_desc = 'checking keys in keyring'


def _start_check_package_integrity(*args):
    global _last_pg_desc
    _last_pg_desc = 'checking package integrity'


def _start_load_package_files(*args):
    global _last_pg_desc
    _last_pg_desc = 'loading package files'


def _start_check_file_conflicts(*args):
    global _last_pg_desc
    _last_pg_desc = 'checking for file conflicts'


event_action_map = {
    event.ALPM_EVENT_PACKAGE_OPERATION_START: _start_operation_action,
    event.ALPM_EVENT_KEYRING_START: _start_check_keyring,
    event.ALPM_EVENT_INTEGRITY_START: _start_check_package_integrity,
    event.ALPM_EVENT_LOAD_START: _start_load_package_files,
    event.ALPM_EVENT_FILECONFLICTS_START: _start_check_file_conflicts,
}


def cb_event(*args):
    event_id = args[0]

    func = event_action_map.get(event_id, None)
    if func:
        return func(*args)

    msg = event.event_msg_map.get(event_id, '')
    if msg:
        print(msg)
    #else:
    #    print('event ', args)


def cb_conv(*args):
    print('conversation ', args)


bar_install_format_list = ['{desc}', ' '*int(cols/2), '[{bar}]']
bar_install_format_list.append('{percentage:3.0f}%')
bar_intall_format = ''.join(bar_install_format_list)

_last_pg_target = None
_last_pg_progressbar = None
_last_pg_percent = None
_last_pg_desc = None

_finish_target_set = []


def cb_progress(target, percent, n, i):
    global _last_pg_target, _last_pg_progressbar
    global _last_pg_percent, _last_pg_desc
    global _last_operation_action, _finish_target_set

    if target and percent == 100 and target in _finish_target_set:
        return

    if _last_pg_target is not None and _last_pg_target != target:
        return

    if _last_pg_target is None:
        _last_pg_target = target
        _last_pg_progressbar = tqdm(
            total=100, ascii=True,
            dynamic_ncols=True,
            bar_format=bar_intall_format
        )

        _last_pg_progressbar.update(percent)
        _last_pg_percent = percent
        return

    if target:
        desc = '(%d/%d) %s %s' % (
            i, n,
            _last_operation_action,
            target
        )
        _last_pg_progressbar.set_description(desc)
    else:
        desc = '(%d/%d) %s' % (
            i, n, _last_pg_desc
        )
        _last_pg_progressbar.set_description(desc)

    d = percent - _last_pg_percent
    _last_pg_percent = percent
    if d > 0:
        _last_pg_progressbar.update(d)

    if percent == 100:
        if target:
            _finish_target_set.append(target)

        _last_pg_target = None
        _last_pg_progressbar = None
        _last_pg_percent = None
        _last_pg_desc = None

        if _last_operation_action == 'installing':
            global _current_operate_pkg_map
            pkg = _current_operate_pkg_map.get(target, None)
            if pkg and len(pkg.optdepends) > 0:
                print('Optional dependencies for %s' % target)
                for x in pkg.optdepends:
                    print('    %s' % x)

        _last_operation_action = None


bar_dl_format_list = ['{desc:<30}', ' '*int(cols/3), ]
bar_dl_format_list.append('{n_fmt}/{total_fmt}')
bar_dl_format_list.append('  {rate_fmt}{postfix}')
bar_dl_format_list.append('  {elapsed} [{bar}]')
bar_dl_format_list.append('{percentage:3.0f}%')
bar_dl_format = ''.join(bar_dl_format_list)


_last_dl_filename = None
_last_dl_progressbar = None
_last_dl_tx = None


def cb_dl(filename, tx, total):

    if total <= 0 or tx <= 0:
        return

    global _last_dl_filename, _last_dl_progressbar, _last_dl_tx
    if _last_dl_filename is not None and _last_dl_filename != filename:
        return

    if _last_dl_filename is None:
        _last_dl_filename = filename
        _last_dl_progressbar = tqdm(
            total=total, unit='B', ascii=True,
            dynamic_ncols=True,
            bar_format=bar_dl_format,
            unit_scale=True, unit_divisor=1024, miniters=1
            )
        _last_dl_progressbar.set_description('%s ' % filename)
        _last_dl_tx = tx
        _last_dl_progressbar.update(tx)
        return

    d = tx - _last_dl_tx
    _last_dl_tx = tx
    if d > 0:
        _last_dl_progressbar.update(d)

    if tx == total:
        _last_dl_filename = None
        _last_dl_progressbar = None
        _last_dl_tx = None


def prepare(t):
    t.prepare()


def set_operate_pkgs(pkgs):
    global _current_operate_pkg_map
    _current_operate_pkg_map.clear()
    for pkg in pkgs:
        _current_operate_pkg_map[pkg.name] = pkg


'''
/** Transaction flags */
typedef enum _alpm_transflag_t {
	/** Ignore dependency checks. */
	ALPM_TRANS_FLAG_NODEPS = 1,
	/* (1 << 1) flag can go here */
	/** Delete files even if they are tagged as backup. */
	ALPM_TRANS_FLAG_NOSAVE = (1 << 2),
	/** Ignore version numbers when checking dependencies. */
	ALPM_TRANS_FLAG_NODEPVERSION = (1 << 3),
	/** Remove also any packages depending on a package being removed. */
	ALPM_TRANS_FLAG_CASCADE = (1 << 4),
	/** Remove packages and their unneeded deps (not explicitly installed). */
	ALPM_TRANS_FLAG_RECURSE = (1 << 5),
	/** Modify database but do not commit changes to the filesystem. */
	ALPM_TRANS_FLAG_DBONLY = (1 << 6),
	/* (1 << 7) flag can go here */
	/** Use ALPM_PKG_REASON_DEPEND when installing packages. */
	ALPM_TRANS_FLAG_ALLDEPS = (1 << 8),
	/** Only download packages and do not actually install. */
	ALPM_TRANS_FLAG_DOWNLOADONLY = (1 << 9),
	/** Do not execute install scriptlets after installing. */
	ALPM_TRANS_FLAG_NOSCRIPTLET = (1 << 10),
	/** Ignore dependency conflicts. */
	ALPM_TRANS_FLAG_NOCONFLICTS = (1 << 11),
	/* (1 << 12) flag can go here */
	/** Do not install a package if it is already installed and up to date. */
	ALPM_TRANS_FLAG_NEEDED = (1 << 13),
	/** Use ALPM_PKG_REASON_EXPLICIT when installing packages. */
	ALPM_TRANS_FLAG_ALLEXPLICIT = (1 << 14),
	/** Do not remove a package if it is needed by another one. */
	ALPM_TRANS_FLAG_UNNEEDED = (1 << 15),
	/** Remove also explicitly installed unneeded deps (use with ALPM_TRANS_FLAG_RECURSE). */
	ALPM_TRANS_FLAG_RECURSEALL = (1 << 16),
	/** Do not lock the database during the operation. */
	ALPM_TRANS_FLAG_NOLOCK = (1 << 17)
} alpm_transflag_t;
'''


def init_from_options(handle, config={}):
    '''
    "Initializes a transaction.\n"
    "Arguments:\n"
    "  nodeps, force, nosave, nodepversion, cascade, recurse,\n"
    "  dbonly, alldeps, downloadonly, noscriptlet, noconflicts,\n"
    "  needed, allexplicit, inneeded, recurseall, nolock\n"
    "    -- the transaction options (booleans)\n"
    "  event_callback -- a function called when an event occurs\n"
    "  conv_callback -- a function called to get user input\n"
    "  progress_callback -- a function called to indicate progress\n"
    '''
    t = handle.init_transaction(
        # nodeps
        config.get('nodeps', False),
        # "force",
        config.get('force', False),
        # "nosave",
        config.get('nosave', False),
        # "nodepversion",
        config.get('nodepversion', False),
        # "cascade",
        config.get('cascade', False),
        # "recurse",
        (config.get('recurse', 0) > 0),
        # "dbonly",
        config.get('dbonly', False),
        # "alldeps",
        config.get('alldeps', False),
        # "downloadonly",
        config.get('downloadonly', False),
        # "noscriptlet",
        config.get('noscriptlet', False),
        # "noconflicts",
        config.get('noconflicts', False),
        # "needed",
        config.get('needed', True),
        # "allexplicit",
        config.get('allexplicit', False),
        # "unneeded",
        config.get('unneeded', False),
        # "recurseall",
        (config.get('recurse', 0) > 1),
        # "nolock",
        #config.get('nolock', False)
    )

    cb_event_func = cb_event
    handle.dlcb = cb_dl
    handle.eventcb = cb_event_func
    handle.questioncb = cb_conv
    handle.progresscb = cb_progress
    return t


def create_transaction(handle, config={}):
    try:
        return init_from_options(handle, config)
    except pyalpm.error as e:
        print('')
        print(e)
        if os.path.exists(handle.lockfile):
            print('%s is exist' % handle.lockfile)
        sys.exit(-1)
