import sys, os, time
import debug_cron_common

def get_command(args):
    return " ".join(args[1:]).strip()

def dispatch_command(command):
    f = open(debug_cron_common.get_socket_in_path(), "w")
    f.write(command)
    f.close()

def print_output():
    # TODO Output is more complicated, since it's hard to say when it's done.
    # May need signals and locks, and this: http://stackoverflow.com/a/12523302/475877
    with open(debug_cron_common.get_socket_out_path(), 'r') as out_f:
        print out_f.read()

def flush_output():
    # TODO Output is more complicated, since it's hard to say when it's done.
    # May need signals and locks, and this: http://stackoverflow.com/a/12523302/475877
    with open(debug_cron_common.get_socket_out_path(), 'r') as out_f:
        out_f.read()

def signal_quit():
    os.remove(debug_cron_common.get_run_signal_path())

def signal_run():
    if not os.path.exists(debug_cron_common.get_run_signal_path()):
        os.mkfifo(debug_cron_common.get_run_signal_path())

def is_running():
    return os.path.exists(debug_cron_common.get_lockfile_path())

def wait_until_running():
    if is_running():
        return True
    else:
        print "Waiting for server (may take up to a minute)..."

    for x in range(61):
        time.sleep(1)
        if is_running():
            print "Server found. Running command."
            print
            return True
    else:
        print "Server not found. Doublecheck that it's set up correctly in cron. Exiting client."

    return False

def main():
    success, error_msg = debug_cron_common.set_up_dir()
    if not success:
        print error_msg
        return

    cron_command = get_command(sys.argv)

    if not cron_command:
        print "Please give a command"
        return

    signal_run()

    if cron_command == "quit":
        signal_quit()
        time.sleep(.2) # mitigate race conditions
        if is_running(): 
            dispatch_command("ls") # something to get it to read from the fifo
            flush_output() # necessary to get it to process the above command
        return

    if wait_until_running():
        dispatch_command(cron_command)
        print_output()

if __name__ == "__main__":
    main()
