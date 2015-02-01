#!/bin/bash
BASE_DIR=/var/debug_cron
USER_DIR=$BASE_DIR/users

mkdir $BASE_DIR | chown root:root $BASE_DIR
chmod 777 $BASE_DIR

mkdir $USER_DIR | chown root:root $USER_DIR
chmod 777 $USER_DIR
