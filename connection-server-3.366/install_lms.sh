#!/bin/bash
HWR=`cat /proc/cmdline | awk -v RS=" " -F= '/boardrev/ { print $2 }'`
HWR2='0x'`cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}'`
RASPI_MODEL=`cat /sys/firmware/devicetree/base/model`

echo $VARS
CHANGE_CFG=`sudo grep -q '/var/log/squeezeboxserver' '/usr/lib/tmpfiles.d/systemd.conf' && echo $?`

#RASPI B 2 0xa01040, 0xa01041, 0xa21041
#RASPI B 3 0xa02082, 0xa020d3, 0xa22082, 0xa32082, 0xa52082, 0xa22083
#RASPI B 4 0xa03111, 0xb03111, 0xc03111
#https://github.com/mholling/rpirtscts/blob/master/rpirtscts.c

##
#RASPI HW REVISION ADD NEXT 3+
RSPI_TYPE=( '0xa02082'
            '0xa020d3'
            '0xa22082'
            '0xa32082'
            '0xa52082'
            '0xa22083'
            '0xa03111'
            '0xb03111'
            '0xc03111' );
#LIB
sudo apt-get install -y libsox-fmt-all libflac-dev libfaad2 libmad0

if [ -f /etc/init.d/logitechmediaserver ]
then 
echo "LMS is instaled"
else
echo "LMS not found - Downloading"
for (( i=0; i<"${#RSPI_TYPE[@]}"; i++ )); do  
if [ "${RSPI_TYPE[$i]}" == "$HWR" ]
then
echo "Compatible HW Revision $HWR (${RSPI_TYPE[$i]} required)"
echo "Model: $RASPI_MODEL"
echo "Installing Logitechmedia server"
#wget http://downloads.slimdevices.com/nightly/7.9/sc/5e54c18/logitechmediaserver_7.9.1~1501791870_arm.deb
#sudo dpkg -i logitechmediaserver_7.9.1~1501791870_arm.deb
wget -O logitechmediaserver_all.deb $(wget -q -O - "http://www.mysqueezebox.com/update/?version=7.9.0&revision=1&geturl=1&os=deb")
sudo dpkg -i logitechmediaserver_all.deb

#Copy Preset
sudo cp -R config/settings_templates/server.prefs /var/lib/squeezeboxserver/prefs/

break

elif [ "${RSPI_TYPE[$i]}" == "$HWR2" ]
then
echo "Compatible HW Revision $HWR2 (${RSPI_TYPE[$i]} required)"
echo "Model: $RASPI_MODEL"
echo "Installing Logitechmedia server"
#wget http://downloads.slimdevices.com/nightly/7.9/sc/5e54c18/logitechmediaserver_7.9.1~1501791870_arm.deb
#sudo dpkg -i logitechmediaserver_7.9.1~1501791870_arm.deb
wget -O logitechmediaserver_all.deb $(wget -q -O - "http://www.mysqueezebox.com/update/?version=7.9.0&revision=1&geturl=1&os=deb")
sudo dpkg -i logitechmediaserver_all.deb

#Copy Preset
sudo cp -R config/settings_templates/server.prefs /var/lib/squeezeboxserver/prefs/

break

fi
done
fi

if [ -f /usr/lib/tmpfiles.d/systemd.conf ] ; then 
sudo chmod 750 /usr/lib/tmpfiles.d/systemd.conf
CHANGE_CFG=`sudo grep -q '/var/log/squeezeboxserver' '/usr/lib/tmpfiles.d/systemd.conf' && echo $?`
echo "$CHANGE_CFG"
if [ -z $CHANGE_CFG ] ; then
sudo echo 'd /var/log/squeezeboxserver 0755 squeezeboxserver nogroup - -' >> /usr/lib/tmpfiles.d/systemd.conf
sudo chmod 755 /usr/lib/tmpfiles.d/systemd.conf
sudo chmod a-x /usr/lib/tmpfiles.d/systemd.conf
else
sudo chmod 755 /usr/lib/tmpfiles.d/systemd.conf
fi
else
sudo chmod 755 /usr/lib/tmpfiles.d/systemd.conf
fi

exit 0

