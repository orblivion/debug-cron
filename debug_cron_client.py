import sys, os, time
import debug_cron_common

def get_command(args):
    return " ".join(args[1:]).strip()

def dispatch_command(command):
    f = open(debug_cron_common.SOCKET_IN_PATH, "w")
    f.write(command)
    f.close()

def print_output():
    # TODO Output is more complicated, since it's hard to say when it's done.
    # May need signals and locks, and this: http://stackoverflow.com/a/12523302/475877
    with open(debug_cron_common.SOCKET_OUT_PATH, 'r') as out_f:
        print out_f.read()

def signal_quit():
    os.remove(debug_cron_common.RUN_SIGNAL_PATH)

def signal_run():
    if not os.path.exists(debug_cron_common.RUN_SIGNAL_PATH):
        os.mkfifo(debug_cron_common.RUN_SIGNAL_PATH)

def wait_until_running():
    if not os.path.exists(debug_cron_common.LOCKFILE_PATH):
        print "Waiting for server..."
    else:
        return
    for x in range(61):
        time.sleep(1)
        if os.path.exists(debug_cron_common.LOCKFILE_PATH):
            print "Server found. Running command."
            print
            return True
    else:
        print "Server not found. Doublecheck that it's set up correctly in cron. Exiting client."

def main():
    signal_run()
    cron_command = get_command(sys.argv)

    if not cron_command:
        print "Please give a command"
        return

    wait_until_running()
    if cron_command == "quit":
        signal_quit()
        dispatch_command("ls") # something to get it to read from the fifo
    else:
        dispatch_command(cron_command)
        print_output()

if __name__ == "__main__":
    main()
