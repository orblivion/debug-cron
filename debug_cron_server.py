import os, subprocess

LOCKFILE_PATH = "/tmp/debug_cron_server.lock"
SOCKET_IN_PATH = "/tmp/debug_cron.in"
SOCKET_OUT_PATH = "/tmp/debug_cron.out"
LOG_PATH = "/tmp/debug_cron_server.log"

def main():
    if not set_up():
        return
    while 1:
        process_command()

def process_command():
    insock = open(SOCKET_IN_PATH, "r")
    outsock = open(SOCKET_OUT_PATH, "w")
    subprocess.call("sh", stdout=outsock, stderr=outsock, stdin=insock)

def set_up():
    # A crude lock. There are nice lockfile libraries, but we don't want
    # to deal with pip environment under cron.
    try:
        os.mkfifo(LOCKFILE_PATH)
    except os.error:
        error_msg = (
            "Alread running, maybe try again in a minute."
            " If there was a horrible crash, maybe delete the lock file at %s" % LOCKFILE_PATH
        )
        print error_msg
        f = open(LOG_PATH, "a")
        f.write(error_msg + "\n")
        f.close()
        return False

    for path in [SOCKET_IN_PATH, SOCKET_OUT_PATH]:
        os.mkfifo(path, 0600)
    return True

def clean_up():
    for path in [SOCKET_IN_PATH, SOCKET_OUT_PATH, LOCKFILE_PATH]:
        os.remove(path)

if __name__ == "__main__":
    if set_up():
        process_command()
        clean_up()
