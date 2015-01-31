import os, subprocess, traceback, atexit
import debug_cron_common

def main():
    if set_up():
        atexit.register(clean_up)
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
    f = open(debug_cron_common.LOG_PATH, "a")
    f.write(log_msg + "\n")
    f.close()

def quit_signal():
    return os.path.exists(debug_cron_common.QUIT_SIGNAL_PATH)

def process_command():
    log("Listening for command")
    insock = open(debug_cron_common.SOCKET_IN_PATH, "r")
    outsock = open(debug_cron_common.SOCKET_OUT_PATH, "w")
    subprocess.call("sh", stdout=outsock, stderr=outsock, stdin=insock)

def set_up():
    # A crude lock. There are nice lockfile libraries, but we don't want
    # to deal with virtualenv under cron.
    try:
        os.mkfifo(debug_cron_common.LOCKFILE_PATH)
    except os.error:
        msg = (
            "Already running. Likely from a previous cron run. If not, try cleaning up files."
        )
        log(msg)
        return False

    for path in [debug_cron_common.SOCKET_IN_PATH, debug_cron_common.SOCKET_OUT_PATH]:
        os.mkfifo(path, 0600)
    return True

def clean_up():
    log("Cleaning Up")
    for path in [debug_cron_common.SOCKET_IN_PATH,
                 debug_cron_common.SOCKET_OUT_PATH,
                 debug_cron_common.QUIT_SIGNAL_PATH,
                 debug_cron_common.LOCKFILE_PATH]:
        if os.path.exists(path):
            os.remove(path)

if __name__ == "__main__":
    main()
