#!/bin/bash

if [ "$1" != "" ] && [ "$2" != "" ]
then
    echo ""
else
    echo "Update script - bad arguments"
    exit 1
fi

DIR='/opt/updater/updater/install'

if [ "$2" == "1" ]
then
    IMM_PROCESS_CMD="$(ps -eo args | grep -m1 'imm_server/supervisord')"
    echo "Stop processes ..."
    echo $IMM_PROCESS_CMD
    echo ""
    pkill -f "$IMM_PROCESS_CMD"
    
elif [ "$2" == "2" ]
then

    sudo rm -r /etc/imm.old
    sudo cp -a /etc/imm /etc/imm.old
    sudo rm -r /etc/imm.old/network.json
    sudo rm -r /etc/imm.old/settings_templates

    sudo rm -r /opt/imm.old
    sudo cp -a /opt/imm /opt/imm.old
    
elif [ "$2" == "3" ]
then

    if [ -z "$(ls -A /opt/imm.old)" ];
    then
        echo "No backup files found"
        exit 1
    fi

    echo "Backup files found"
    
    sudo umount /opt/imm/imm_server/log
    sudo rm -r /opt/imm
    sudo cp -a /opt/imm.old /opt/imm
    sudo mount -t tmpfs -o defaults,noatime,nosuid,mode=0777,size=120m tmpfs /opt/imm/imm_server/log
    
    sudo cp -a /etc/imm.old/* /etc/imm/
    
elif [ "$2" == "4" ]
then
    cd $DIR
    tar -zxvf $1.tar.gz 
    #&> out.log
    
elif [ "$2" == "5" ]
then
    cd $DIR/$1
    ./install12.04.sh
    
elif [ "$2" == "6" ]
then
    sudo rm -r $DIR/*
    
elif [ "$2" == "7" ]
then
    #sudo /etc/init.d/imm_server start
    sudo reboot

else
    echo "Update script - bad arguments"
    exit 1
fi

exit 0

