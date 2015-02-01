import os, subprocess, traceback, atexit, time, calendar
import debug_cron_common

def main():
    if set_up():
        try:
            while not quit_signal():
                process_command()
        except BaseException:
            # Particularly useful for keyboard
            log("Exception:")
            log(traceback.format_exc())
            raise
        else:
            log("Normal Exit")

def log(log_msg):
    print log_msg
    f = open(debug_cron_common.get_log_path(), "a")
    timestamp = calendar.timegm(time.gmtime())
    if len(log_msg.split("\n")) > 1:
        # multi line
        f.write("{timestamp}:\n{log_msg}".format(timestamp=timestamp, log_msg=log_msg) + "\n")
    else:
        # one line
        f.write("{timestamp}: {log_msg}".format(timestamp=timestamp, log_msg=log_msg) + "\n")
    f.close()

def quit_signal():
    return not os.path.exists(debug_cron_common.get_run_signal_path())

def process_command():
    log("Listening for command")
    insock = open(debug_cron_common.get_socket_in_path(), "r")
    outsock = open(debug_cron_common.get_socket_out_path(), "w")
    subprocess.call("sh", stdout=outsock, stderr=outsock, stdin=insock)

def set_up():
    success, error_msg = debug_cron_common.set_up_dir()
    if not success:
        # Probably shouldn't log since the dir isn't established.
        print error_msg
        return

    # A crude lock. There are nice lockfile libraries, but we don't want
    # to deal with virtualenv under cron.
    try:
        os.mkfifo(debug_cron_common.get_lockfile_path())
    except os.error:
        log(
            "Already running. Likely from a previous cron run. If not, try cleaning up files."
        )
        return False

    atexit.register(clean_up)

    for path in [debug_cron_common.get_socket_in_path(), debug_cron_common.get_socket_out_path()]:
        os.mkfifo(path, 0600)
    return True

def clean_up():
    log("Cleaning Up")
    for path in [debug_cron_common.get_socket_in_path(),
                 debug_cron_common.get_socket_out_path(),
                 debug_cron_common.get_lockfile_path()]:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    main()
