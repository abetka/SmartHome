#!/bin/bash

if mkdir /var/lock/.uexports.lock 2>/dev/null
then
    IP=`python getMyIPmod0.pyc`
    MASK=`python getMyNetMaskmod0.pyc`
    if [[ ! -z "$IP" ]] && [[ ! -z "$MASK" ]]
    then
        grep -v '^/home/imm\s' /etc/exports >.exports.new
        echo "/home/imm $IP/$MASK(rw,sync,no_subtree_check)" >>.exports.new
        sudo cp -f .exports.new /etc/exports && rm .exports.new
        sudo /etc/init.d/portmap restart
        sudo /etc/init.d/nfs-kernel-server restart
        sudo exportfs -ra
    fi
    rmdir /var/lock/.uexports.lock
else
    echo "WARNING: Export file cannot be set up"
fi

