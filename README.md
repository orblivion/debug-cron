# Warning

This **HAS NOT** been carefully vetted or tested, including for security concerns (particularly with other users injecting commands). Use at your own risk.

Requires (and should only be relevant for) a Unix environment. To the extent it has been tested, it was tested on Ubuntu Utropic.

Please see [Issues](https://github.com/orblivion/debug-cron/issues/) if you want to help review or fix or report bugs.

# Why

There's no reason I should be writing this package, but there's *still* no reasonable way to test commands under cron. There's always some nonsense in the environment, you have to have it pipe stdout to a file and wait around for another minute like an idiot. And of course nothing happens for no apparent reason, so you try piping stderr...

So, here's a hacked up way to do it more conveniently:

# How To

## Install

    sudo ./install.sh

This just creates the directories in /var/ for us use for communicating between the processes.

## Use

In your crontab, add the following line:

    * * * * * python /path/to/package/debug_cron_server.py

Now wait until the next minute comes along. Yes this command will repeat every minute, but it should immediately exit if it's already running. Once it starts, it stays in a command loop so you don't have to keep waiting.

Now from within the package directory run:

    ./debug_cron_client.py ls /

Initially, the cron job probably won't have kicked in:

    Waiting for server (may take up to a minute)...

Once it does, you should get the output as cron sees it:

    bin
    boot
    cdrom
    dev
    etc
    home
    initrd.img
    initrd.img.old
    lib
    lib64
    lost+found
    media
    mnt
    opt
    proc
    root
    run
    sbin
    srv
    sys
    tmp
    usr
    var
    vmlinuz
    vmlinuz.old

Now that it's started, subsequent commands should go through right away. Here, try this:

    ./debug_cron_client.py env

You'll see the elusive cron env that's giving us all this grief:

    HOME=/home/keyboard_kowboy
    LOGNAME=keyboard_kowboy
    PATH=/usr/bin:/bin
    LANG=en_US.UTF-8
    SHELL=/bin/sh
    PWD=/home/keyboard_kowboy

So now you'll see what's really going on. Both `stdout` and `stderr` should now come out here, for now both as stdout.

Since the thing is running in cron land, you may want to stop it:

    ./debug_cron_client.py --quit

This will tell it to stop listening for new commands. If you run the client again with a normal command, it will have to wait for cron to kick it off on the next minute mark, like it did the first time you ran it. This way you can conceivably leave it in your cron and it won't be waiting around, or really do anything when you don't need it. Just make sure to remember to run with `--quit` when you're done, even if you remove it from cron, otherwise it'll be hanging around listening. I know this is a bit inelegant, I'm open to better ideas.

## Annoying things

If you use a shell variable, you have to escape the `$`

    ./debug_cron_client.py echo \$PWD

If you need to change your directory first, you should put that in quotes:

    ./debug_cron_client.py "(cd /tmp/; ls)"
