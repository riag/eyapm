
import click
from pycman import config

import eyapm
from eyapm import transaction


@click.command('upgrade')
@click.pass_context
@click.option(
    '--config-file', 'config_file',
    default=eyapm.default.config_file)
@click.option(
    '-y', '--yes', 'quiet', is_flag=True, default=False
)
def cli(ctx, config_file, quiet):
    handle = config.init_with_config(config_file)
    syncdbs = handle.get_syncdbs()

    eyapm.util.sync_dbs(handle, syncdbs)
    print('')

    t = transaction.create_transaction(
        handle, {}
    )
    with eyapm.util.work_with_transaction(t):
        t.sysupgrade(True)
        t.prepare()
        #print(dir(t))
        #print(len(t.to_remove))
        if len(t.to_add) == 0:
            print(' Nothing to do.')
            return

        total_install_size = 0
        total_download_size = 0
        total_size = 0
        for x in t.to_add:
            #print(dir(x))
            total_install_size += x.isize
            total_download_size += x.download_size
            total_size += x.size

        print('')
        package_name_list = [x.name for x in t.to_add]
        print('Packages (%d) %s\n' % (
            len(t.to_add), ' '.join(package_name_list)
        ))
        size_str = '{:.2f}'.format(
                total_download_size/1024/1024
        )
        s = 'Total Download Size:     {:>8} MiB'.format(
            size_str
        )
        print(s)
        size_str = '{:.2f}'.format(
                total_install_size/1024/1024
        )
        s = 'Total Installed Size:    {:>8} MiB'.format(
            size_str
        )
        print(s)
        #print(total_size/1024/1024)
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
