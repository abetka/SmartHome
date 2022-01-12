#!/bin/bash

INSTALL_DIR=/opt/updater
APP_DIR=$INSTALL_DIR/updater
UPDATE_DIR=$INSTALL_DIR/temp
VIRTUALENV_DIR=$INSTALL_DIR/.venv


function create_dir {
    if ls $1 &> /dev/null ;
    then
        echo "$1 directory already exists"
    else
        mkdir $1
    fi
}

function check_update {
    file_version_old="/opt/updater/updater/version"
    file_version_new="/opt/updater/temp/version"
    version_old=""
    version_new=""

    while read line; do
        version_old="$line"
        break
    done < "$file_version_old"

    while read line; do
        version_new="$line"
        break
    done < "$file_version_new"

    MEGA="1000"
    version_old=$(awk '{print $1*$2}' <<<"${version_old} ${MEGA}")
    version_new=$(awk '{print $1*$2}' <<<"${version_new} ${MEGA}")

    echo -e "Update server OLD version: $version_old"
    echo -e "\nUpdate server NEW version: $version_new"

    if (( version_new > version_old )); then
        return 0
    else
        return 1
    fi
}

# create /opt/imm/
echo -e "\n********** CREATE DIR ...\n"
create_dir $INSTALL_DIR
chmod 777 $INSTALL_DIR
create_dir $APP_DIR
create_dir $VIRTUALENV_DIR


# create the virtual environment if not exist
if [ -z "$(ls -A $VIRTUALENV_DIR)" ];
then
    echo -e "\n********** CREATE VIRTUALENV ...\n"
    virtualenv -p /usr/bin/python2.7 $VIRTUALENV_DIR --no-site-packages --distribute
fi


# install requirements(new ones)
echo -e "\n********** INSTALL PACKAGES\n"
source $VIRTUALENV_DIR/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install Flask
pip install flask-login
pip install requests psutil



if [ -z "$(ls -A /opt/updater/updater)" ];
then
    echo -e "\n***** INSTALL UPDATE SERVER ..."
    
    # copy new files
    echo -e "\n********** COPY FILES"
    rm -r $APP_DIR/*
    cp -r static $APP_DIR
    cp -r templates $APP_DIR
    cp -r install $APP_DIR
    cp -r log $APP_DIR
    cp -r updater.py $APP_DIR
    cp -r update.sh $APP_DIR
    cp -r version $APP_DIR

    # change permissions
    chown -R imm $INSTALL_DIR
    chgrp -R imm $INSTALL_DIR

    chmod 777 $APP_DIR/install
    chmod 777 $APP_DIR/log

    #install init scripts
    echo -e "\n********** SET SERVICE"
    cp updater.service /etc/init.d/updater_server
    chmod u+x /etc/init.d/updater_server
    chown imm /etc/init.d/updater_server
    update-rc.d updater_server defaults

    #start server
    echo -e "\n********** START UPDATE SERVER\n"
    /etc/init.d/updater_server start
    
else
    echo -e "\n***** UPDATE UPDATE SERVER ..."

    # overwrite old version
    echo -e "\n********** COPY FILES\n"
    create_dir $UPDATE_DIR
    rm -r $UPDATE_DIR/*
    cp -r static $UPDATE_DIR
    cp -r templates $UPDATE_DIR
    cp -r install $UPDATE_DIR
    cp -r log $UPDATE_DIR
    cp -r updater.py $UPDATE_DIR
    cp -r update.sh $UPDATE_DIR
    cp -r version $UPDATE_DIR

    # change permissions
    chown -R imm $INSTALL_DIR
    chgrp -R imm $INSTALL_DIR

    chmod 777 $UPDATE_DIR/install
    chmod 777 $UPDATE_DIR/log

    #install init scripts
    if check_update ; then
        echo -e "\n********** SET SERVICE\n"
        cp updater.service /etc/init.d/updater_server
        chmod u+x /etc/init.d/updater_server
        chown imm /etc/init.d/updater_server
        update-rc.d updater_server defaults
    else
        echo -e "\n********** REMOVING FILES\n"
        rm -r $UPDATE_DIR
    fi
    
fi
