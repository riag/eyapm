
# 见 libalpm/alpm.h

# /** Dependencies will be computed for a package. */
ALPM_EVENT_CHECKDEPS_START = 1
# /** Dependencies were computed for a package. */
ALPM_EVENT_CHECKDEPS_DONE = 2
# /** File conflicts will be computed for a package. */
ALPM_EVENT_FILECONFLICTS_START = 3
# /** File conflicts were computed for a package. */
ALPM_EVENT_FILECONFLICTS_DONE = 4
# /** Dependencies will be resolved for target package. */
ALPM_EVENT_RESOLVEDEPS_START = 5
# /** Dependencies were resolved for target package. */
ALPM_EVENT_RESOLVEDEPS_DONE = 6
# /** Inter-conflicts will be checked for target package. */
ALPM_EVENT_INTERCONFLICTS_START = 7
# /** Inter-conflicts were checked for target package. */
ALPM_EVENT_INTERCONFLICTS_DONE = 8
# /** Processing the package transaction is starting. */
ALPM_EVENT_TRANSACTION_START = 9
# /** Processing the package transaction is finished. */
ALPM_EVENT_TRANSACTION_DONE = 10
# /** Package will be installed/upgraded/downgraded/re-installed/removed; See
# * alpm_event_package_operation_t for arguments. */
ALPM_EVENT_PACKAGE_OPERATION_START = 11
# /** Package was installed/upgraded/downgraded/re-installed/removed; See
# * alpm_event_package_operation_t for arguments. */
ALPM_EVENT_PACKAGE_OPERATION_DONE = 12
# /** Target package's integrity will be checked. */
ALPM_EVENT_INTEGRITY_START = 13
# /** Target package's integrity was checked. */
ALPM_EVENT_INTEGRITY_DONE = 14
# /** Target package will be loaded. */
ALPM_EVENT_LOAD_START = 15
# /** Target package is finished loading. */
ALPM_EVENT_LOAD_DONE = 16
# /** Target delta's integrity will be checked. */
ALPM_EVENT_DELTA_INTEGRITY_START = 17
# /** Target delta's integrity was checked. */
ALPM_EVENT_DELTA_INTEGRITY_DONE = 18
# /** Deltas will be applied to packages. */
ALPM_EVENT_DELTA_PATCHES_START = 19
# /** Deltas were applied to packages. */
ALPM_EVENT_DELTA_PATCHES_DONE = 20
# /** Delta patch will be applied to target package; See
# * alpm_event_delta_patch_t for arguments.. */
ALPM_EVENT_DELTA_PATCH_START = 21
# /** Delta patch was applied to target package. */
ALPM_EVENT_DELTA_PATCH_DONE = 22
# /** Delta patch failed to apply to target package. */
ALPM_EVENT_DELTA_PATCH_FAILED = 23
# /** Scriptlet has printed information; See alpm_event_scriptlet_info_t for
# * arguments. */
ALPM_EVENT_SCRIPTLET_INFO = 24
# /** Files will be downloaded from a repository. */
ALPM_EVENT_RETRIEVE_START = 25
# /** Files were downloaded from a repository. */
ALPM_EVENT_RETRIEVE_DONE = 26
# /** Not all files were successfully downloaded from a repository. */
ALPM_EVENT_RETRIEVE_FAILED = 27
# /** A file will be downloaded from a repository; See alpm_event_pkgdownload_t
# * for arguments */
ALPM_EVENT_PKGDOWNLOAD_START = 28
# /** A file was downloaded from a repository; See alpm_event_pkgdownload_t
# * for arguments */
ALPM_EVENT_PKGDOWNLOAD_DONE = 29
# /** A file failed to be downloaded from a repository; See
# * alpm_event_pkgdownload_t for arguments */
ALPM_EVENT_PKGDOWNLOAD_FAILED = 30
# /** Disk space usage will be computed for a package. */
ALPM_EVENT_DISKSPACE_START = 31
# /** Disk space usage was computed for a package. */
ALPM_EVENT_DISKSPACE_DONE = 32
# /** An optdepend for another package is being removed; See
# * alpm_event_optdep_removal_t for arguments. */
ALPM_EVENT_OPTDEP_REMOVAL = 33
# /** A configured repository database is missing; See
# * alpm_event_database_missing_t for arguments. */
ALPM_EVENT_DATABASE_MISSING = 34
# /** Checking keys used to create signatures are in keyring. */
ALPM_EVENT_KEYRING_START = 35
# /** Keyring checking is finished. */
ALPM_EVENT_KEYRING_DONE = 36
# /** Downloading missing keys into keyring. */
ALPM_EVENT_KEY_DOWNLOAD_START = 37
# /** Key downloading is finished. */
ALPM_EVENT_KEY_DOWNLOAD_DONE = 38
# /** A .pacnew file was created; See alpm_event_pacnew_created_t for arguments. */
ALPM_EVENT_PACNEW_CREATED = 39
# /** A .pacsave file was created; See alpm_event_pacsave_created_t for
# * arguments */
ALPM_EVENT_PACSAVE_CREATED = 40
# /** Processing hooks will be started. */
ALPM_EVENT_HOOK_START = 41
# /** Processing hooks is finished. */
ALPM_EVENT_HOOK_DONE = 42
# /** A hook is starting */
ALPM_EVENT_HOOK_RUN_START = 43
# /** A hook has finished running */
ALPM_EVENT_HOOK_RUN_DONE = 44

event_msg_map = {
    ALPM_EVENT_RESOLVEDEPS_START: 'resolving dependencies...',
    ALPM_EVENT_INTERCONFLICTS_START: 'looking for conflicting packages...',
    ALPM_EVENT_KEYRING_START: 'checking keys in keyring',
    ALPM_EVENT_INTEGRITY_START: 'checking package integrity',
    ALPM_EVENT_LOAD_START: 'loading package files',
    ALPM_EVENT_FILECONFLICTS_START: 'checking for file conflicts',
    ALPM_EVENT_TRANSACTION_START: ':: Processing package changes...',
    ALPM_EVENT_HOOK_START: ':: Running post-transaction hooks...',
}
