#!/bin/bash


HOME="/home/imm/"
AUDIT="/opt/imm/imm_server/log/immControlCenter.log"
FSTAB="/etc/fstab"


#DEBUG 
date >> /home/imm/mount.txt
echo "Umount $1" >> /home/imm/mount.txt


#Variable alias for function 
count_arg="$#"

dev_type="$1"

#Timestamp
timestamp=$(date +'%Y-%m-%d %T%M')


#Argument control if less 
arg_check() {
if [ "$count_arg" == "1" ]; then
	:
else 
	echo -e "ERROR Missing parameter \\n"
	exit 0
fi
}

arg_check


# Music
# Pictures
# Television
# Video
check_simlink()
{   
if [ "$dev_type" == "NFS" ]; then
	sudo umount /mnt/nfs
	echo -e "NFS unmout successfully \\n"

elif [ "$dev_type" == "SMB" ]; then
    sudo umount /mnt/smb
    echo -e "SMB unmout successfully \\n"

else 
	echo "$dev_type"
	echo "Unknown parameter"
	exit 0
fi

for dir in Music Pictures Television Video
do

mediapath="/home/imm/$dir"

# Clean directory or links
if [ -d "/home/imm/$dir" ] || [ -h "/home/imm/$dir" ]; then
	sudo unlink /home/imm/$dir
	sudo rm -dr /home/imm/$dir
    sudo mkdir /home/imm/$dir
    sudo chown imm:imm /home/imm/$dir

else
	echo "$timestamp Unknown directory or can not be created." >> "$AUDIT"
fi

done

echo -e "All done successfully \\n"

}

check_simlink $1