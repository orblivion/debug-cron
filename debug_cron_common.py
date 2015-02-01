import os

def get_working_path():
    # Get *real* uid. TODO - is this safest?
    return "/var/debug_cron/users/%s" % os.getuid()

def confirm_dir(path):
    dir_stat = os.stat(path)
    if dir_stat.st_mode != 040700:
        return False, "Wrong working directory permissions. Got: %s" % dir_stat.st_mode
    if dir_stat.st_uid != os.getuid():
        return False, "Wrong working directory owner uid. Got: %s" % dir_stat.st_uid
    return True, None

def set_up_dir():
    path = get_working_path()
    if not os.path.exists(path):
        os.mkdir(path, 0700)
    return confirm_dir(path)

def get_path_for_file(fname):
    return os.path.join(get_working_path(), fname)

get_lockfile_path = lambda : get_path_for_file("debug_cron_server.lock")
get_socket_in_path = lambda : get_path_for_file("debug_cron.in")
get_socket_out_path = lambda : get_path_for_file("debug_cron.out")
get_run_signal_path = lambda : get_path_for_file("debug_cron_server.runsignal")
get_log_path = lambda : get_path_for_file("debug_cron_server.log")
