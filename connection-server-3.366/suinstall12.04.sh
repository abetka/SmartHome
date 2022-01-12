INSTALL_DIR=/opt/imm/
APP_DIR=$INSTALL_DIR/imm_server/
VIRTUALENV_DIR=$INSTALL_DIR/.virtualenvs
VIRTUALENV=imm_server
CONFIG_DIR=/etc/imm/
DEBVERSION=$(cat /etc/*-release |awk '{ print $3 }')
SPOTIFY_DIR=/opt/spotify/

CONFIG_FILES="imm_server.cfg supervisord.cfg"

function create_dir {
    if ls $1 &> /dev/null ;
    then
        echo "$1 directory already exists"
    else
        mkdir $1
    fi
}

#install dependencies
sudo apt-get install ssh -y libxml2 libxml2-dev libxslt1-dev build-essential python-dev libjpeg62-turbo-dev python-pip python-virtualenv python-setuptools sysstat asterisk python-imaging  zlib1g-dev libfreetype6-dev nfs-kernel-server portmap nfs-common libav-tools ssmtp python-suds libssl-dev


#INSTALL LMS RASPI3+ ONLY
sudo bash ./install_lms.sh


#INSTALL UPDATE SERVER
cd updater
sudo bash ./install_updater.sh
cd ..


# Spotify files
create_dir $SPOTIFY_DIR
cp -r ./spotify/* $SPOTIFY_DIR
chown -R imm $SPOTIFY_DIR
chgrp -R imm $SPOTIFY_DIR
chmod 777 $SPOTIFY_DIR/*


# create /opt/imm/
create_dir $INSTALL_DIR
create_dir $VIRTUALENV_DIR

# if instalation archive contains virtualenv, replace old
if ls .virtualenvs/$VIRTUALENV &> /dev/null;
then
    if ls $VIRTUALENV_DIR/$VIRTUALENV &> /dev/null ;
    then
        rm -r  $VIRTUALENV_DIR/$VIRTUALENV
    fi
    cp -r .virtualenvs/$VIRTUALENV $VIRTUALENV_DIR/
else
    echo "Virtualenv binaries not present in install package"
fi

# create the virtual environment if not exist
if ! ls $VIRTUALENV_DIR/$VIRTUALENV/ &> /dev/null ;
then
    virtualenv -p /usr/bin/python2.7 /opt/imm/.virtualenvs/imm_server --no-site-packages --distribute
    source /opt/imm/.virtualenvs/imm_server/bin/activate

    wd=`pwd`
    wget ftp://xmlsoft.org/libxml2/libxml2-2.7.2.tar.gz
    tar -xzvf libxml2-2.7.2.tar.gz
    cd libxml2-2.7.2/
    ./configure
    make
    cd python/
    CFLAGS=-I./include /opt/imm/.virtualenvs/imm_server/bin/python2.7 setup.py build
    CFLAGS=-I./include /opt/imm/.virtualenvs/imm_server/bin/python2.7 setup.py install
    cd $wd
    sudo rm -r libxml2-2.7.2/

    curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
    python get-pip.py
    pip install -r requirements12.04.txt
fi

# install requirements(new ones)
source /opt/imm/.virtualenvs/imm_server/bin/activate
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python get-pip.py
pip install -r requirements12.04.txt

# fix issue with decoder jpeg not available
isMissing=false
for lib in libz libjpeg libfreetype
do
    if [ ! -f /usr/lib/$lib.so ] ;
    then
        rm /usr/lib/$lib.so
        ln -s /usr/lib/arm-linux-gnueabihf/$lib.so /usr/lib
        isMissing=true
    fi
done

if $isMissing ;
then
    yes | pip uninstall Pillow
    pip install Pillow==2.6.0
fi

# remove daemons
DAEMONS=( 'air'
          'coolMaster'
          'ELAN'
          'ELAN_SCN'
          'em'
          'epg'
          'epsnet'
          'identMovies'
          'imm-webadmin'
          'immXMLRPCServer'
          'imm_server'
          'miele'
          'svisord'
          'videoScreenshots' );

for (( i=0; i<"${#DAEMONS[@]}"; i++ )) ; do
    if [ -f /etc/init.d/${DAEMONS[$i]} ]
    then
        /etc/init.d/${DAEMONS[$i]} stop 1>/dev/null
        sudo update-rc.d -f ${DAEMONS[$i]} remove &>/dev/null
        sudo rm /etc/init.d/${DAEMONS[$i]}
        echo  ${DAEMONS[$i]}
    fi
done

# create basic config directory
if ls $CONFIG_DIR &> /dev/null ;
then
    echo "$CONFIG_DIR already exists"
else
    mkdir $CONFIG_DIR
    cp -r ./config/* $CONFIG_DIR
fi

cp config/manual_en.pdf /etc/imm/
cp config/manual_cz.pdf /etc/imm/
cp config/Cams.json /etc/imm/
cp -R config/scripts /etc/imm/
cp -R config/spotify /etc/imm/

CFG_FLS=( 'AiRPohoda.cfg'
          'control.cfg'
          'coolMaster.cfg'
          'elan.cfg'
          'export.pub'
          'heating.dat'
          'chart.cfg'
          'imm.cfg'
          'irwebcontrol.ini'
          'irweblog.conf'
          'layout.xml'
          'rf.pub'
          'rooms.cfg'
          'screenlet.cfg'
          'subtitles.cfg'
          'nilan.cfg'
          'intercoms.json'
          'network.json'
          'clims.json'
          'asterisk'
          'lara.json'
          'cu3_update_timeout.ini'
          'settings_templates'
          'log' );

for (( i=0; i<"${#CFG_FLS[@]}"; i++ )) ; do
    [ ! -f /etc/imm/${CFG_FLS[$i]} ] && cp -r config/${CFG_FLS[$i]} /etc/imm/
done

OVERWRITE_DIRECTORIES=('asterisk'
        'settings_templates');

for (( i=0; i<"${#OVERWRITE_DIRECTORIES[@]}"; i++ )) ; do
    cp -r config/${OVERWRITE_DIRECTORIES[$i]} /etc/imm/
done

# scene
ED=/etc/imm/events
mkdir $ED 2>/dev/null
touch $ED/enterHouse.py  $ED/exitHouse.py

# if there is older version of imm_server
# store them in imm_server.cfg.old and supervisord.cfg.old

if ls $APP_DIR &> /dev/null ;
then
    for file in $CONFIG_FILES;
    do
        cp $APP_DIR/$file $APP_DIR/$file.old
    done
else
    mkdir  $APP_DIR
fi
for file in $CONFIG_FILES;
do
    cp imm_server/$file $APP_DIR/$file
done

# overwrite old version
DIRS=`ls -d imm_server/*/`
for dir in $DIRS;
do
    rm -r $APP_DIR/`basename $dir`
    cp -r $dir $APP_DIR/`basename $dir`
done


# change permissions

chown -R imm $INSTALL_DIR
chgrp -R imm $INSTALL_DIR


chown -R imm $CONFIG_DIR
chgrp -R imm $CONFIG_DIR


#version-check for right init format
if ((  $DEBVERSION > 7 )) ; then
    echo "Debian $DEBVERSION"
    cp imm_server.init.LSB /etc/init.d/imm_server
else
    echo "Debian 7"
    cp imm_server.init /etc/init.d/imm_server
fi

#install init scripts
for script in imm_server
do
    chmod u+x /etc/init.d/$script
    chown imm /etc/init.d/$script
    update-rc.d $script defaults
done

# fix abs path
cd /opt/imm/imm_server/web && python ./fixAbsPath.pyc &> /dev/null

# crontab
(crontab -l 2>/dev/null | grep -Fv "eMan_opt.pyc" ; printf  "30 2 * * * /usr/bin/python /opt/imm/imm_server/epsnet/eMan_opt.pyc\n") | crontab

# convert old chart.cfg to new one
FILE=/etc/imm/chart.cfg
for LINE in "electric_z1_impulses"\
            "electric_z2_impulses"\
            "electric_z3_impulses"\
            "electric_z4_impulses"\
            "electric_z5_impulses"\
            "electric_z1_per"\
            "electric_z2_per"\
            "electric_z3_per"\
            "electric_z4_per"\
            "electric_z5_per"
do
    grep -q "$LINE" "$FILE" || echo "$LINE = 1" >> "$FILE"
done

for LINE in "electric_impulses" "electric_per"
do
    grep -v "$LINE" "$FILE" > temp && mv temp "$FILE"
done

chown imm $FILE
chmod 666 $FILE

# sudo without password
echo "imm ALL=(ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/imm
chmod 0440 /etc/sudoers.d/imm
