#!/bin/bash

function test_return_value {
	if [ $? -ne 0 ]
	then
		echo "ERROR: $1"
		exit 1
	fi
}

# check root access
sudo echo -e "\n***** SUDO ACCESS IS OK\n"
test_return_value "Permission denied. You need sudo password!"

RASPI_MODEL=`cat /sys/firmware/devicetree/base/model`

echo -e "\n***** Model: $RASPI_MODEL\n"

if [[ $RASPI_MODEL == *" 4 "* ]]; then
    sudo bash suinstall_cs_rpi4.sh
else
    sudo bash suinstall12.04.sh
fi

read -p "Press any key..."
