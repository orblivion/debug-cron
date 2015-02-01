# Warning

This **HAS NOT** been carefully vetted or tested, including for security concerns (particularly with other users injecting commands). Use at your own risk.

Requires (and should only be relevant for) a Unix environment. To the extent it has been tested, it was tested on Ubuntu Utropic.

# Why

There's no reason I should be writing this package, but there's *still* no reasonable way to test commands under cron. There's always some nonsense in the environment, you have to have it pipe stdout to a file and wait around for another minute like an idiot. And of course nothing happens for no apparent reason, so you try piping stderr...

So, here's a hacked up way to do it more conveniently:

# How To

In your crontab, add the following line:

    * * * * * python /path/to/package/debug_cron_server.py

Now wait until the next minute comes along. Yes this command will repeat every minute, but it should immediately exit if it's already running. Once it starts, it stays in a command loop so you don't have to keep waiting.

Now from within the package directory run:

    python debug_cron_client.py ls /tmp/somefile

You should get the output as cron sees it. Here, try this:

    python debug_cron_client.py env

Now you'll see what's really going on. `stdout` and `stderr` should now come out here.
