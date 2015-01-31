import os, subprocess, traceback

LOCKFILE_PATH = "/tmp/debug_cron_server.lock"
SOCKET_IN_PATH = "/tmp/debug_cron.in"
SOCKET_OUT_PATH = "/tmp/debug_cron.out"
LOG_PATH = "/tmp/debug_cron_server.log"

def main():
    if not set_up():
        return
    while 1:
        process_command()

def log(log_msg):
    print log_msg
    f = open(LOG_PATH, "a")
    f.write(log_msg + "\n")
    f.close()

def process_command():
    log("Starting")
    insock = open(SOCKET_IN_PATH, "r")
    outsock = open(SOCKET_OUT_PATH, "w")
    subprocess.call("sh", stdout=outsock, stderr=outsock, stdin=insock)

def set_up():
    # A crude lock. There are nice lockfile libraries, but we don't want
    # to deal with pip environment under cron.
    try:
        os.mkfifo(LOCKFILE_PATH)
    except os.error:
        msg = (
            "Already running. Likely from a previous cron run. If not, try cleaning up files."
        )
        log(msg)
        return False

    for path in [SOCKET_IN_PATH, SOCKET_OUT_PATH]:
        os.mkfifo(path, 0600)
    return True

def clean_up():
    log("Cleaning Up")
    for path in [SOCKET_IN_PATH, SOCKET_OUT_PATH, LOCKFILE_PATH]:
        os.remove(path)

if __name__ == "__main__":
    if set_up():
        try:
            process_command()
        except BaseException as e:
            # Particularly useful for keyboard
            clean_up()
            log("Exception:")
            log(traceback.format_exc())
            raise
        clean_up()
