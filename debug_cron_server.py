LOCKFILE_PATH = "/tmp/debug_cron_server.lock"
from lockfile import LockFile
lock = LockFile(LOCKFILE_PATH)
if lock.is_locked():
    print "Locked. Try again. If there was a horrible crash, maybe delete the lock file at %s" % LOCKFILE_PATH
else:
    with lock:
        print lock.path, 'is locked.'
        while 1:
            pass
