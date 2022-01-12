#!/bin/bash

#DEPENDIENCE
#sudo apt-get install nfs-common
#sudo apt-get install nfs-kernel-server


#Type:
#SYNOLOGY_NFS
#SYNOLOGY_SMBCIFS
#QNAP_NFS
#QNAP_SMBCIFS
#SYNOLOGY_MANUAL
#QNAP_MANUAL

PREFIX_TYPE=( "SYNOLOGY_NFS:${1}:/volume1/${3} /mnt/nfs nfs nouser,atime,auto,rw,dev,exec,suid 0 0"
          "SYNOLOGY_SMBCIFS://${1}/${3} /mnt/smb cifs username=$4,password=$5,nofail,x-systemd.automount,x-systemd.requires=network-online.target,x-systemd.device-timeout=1  0"
          "QNAP_NFS:${1}:/${3} /mnt/nfs nfs nouser,atime,auto,rw,dev,exec,suid 0 0"
          "QNAP_SMBCIFS://${1}/${3} /mnt/smb cifs username=$4,password=$5,nofail,x-systemd.automount,x-systemd.requires=network-online.target,x-systemd.device-timeout=1  0"
          "MANUAL_SYNOLOGY_NFS:${1}"
          #"MANUAL_SYNOLOGY_NFS:IP_ADDRESS:/volume1/Storage /mnt/nfs nfs nouser,atime,auto,rw,dev,exec,suid 0 0
          "MANUAL_SYNOLOGY_SMBCIFS:${1}"
          #//IP_ADDRESS/Storage /mnt/smb cifs username=$3,password=$4,nofail,x-systemd.automount,x-systemd.requires=network-online.target,x-systemd.device-timeout=1  0"
          "MANUAL_QNAP_NFS:${1}"
          #"MANUAL_QNAP:IP_ADDRESS:/Storage /mnt/nfs nfs nouser,atime,auto,rw,dev,exec,suid 0 0"
          "MANUAL_QNAP_SMBCIFS:${1}"
          #MANUAL_QNAP_SMBCIFS://${1}/Storage /mnt/smb cifs username=,password=,nofail,x-systemd.automount,x-systemd.requires=network-online.target,x-systemd.device-timeout=1  0"
          "MANUAL_NFS:${1}"
          #"MANUAL_NFS:IP_ADDRESS:/Storage /mnt/nfs add parameters"
          "MANUAL_SMB:${1}"
          #"MANUAL_SMB://IP_ADDRESS/Storage /mnt/smb add parameters"
           );

MANUAL=( "MANUAL_SYNOLOGY_NFS"
		 "MANUAL_SYNOLOGY_SMBCIFS"
		 "MANUAL_QNAP_NFS"
		 "MANUAL_QNAP_SMBCIFS"
		 "MANUAL_NFS"
		 "MANUAL_SMB"
		   );

 
CONFIG_DIR="/etc/imm/"
HOME="/home/imm/"
AUDIT="/opt/imm/imm_server/log/immControlCenter.log"
FSTAB="/etc/fstab"
MOUNT_OUTPUT="/tmp/mount_output.log"

#DEBUG 
date >> /home/imm/mount.txt
echo "$1 $2 $3 $4 $5" >> /home/imm/mount.txt


#Variable alias for function 
count_arg="$#"

#Timestamp
timestamp=$(date +'%Y-%m-%d %T%M')

#Argument control if less 
arg_check() {
if [ "$count_arg" == "2" ] || [ "$count_arg" -gt 2 ]; then
	:
else 
	echo -e "ERROR Missing parameters \\n"
	exit 1
fi
}

arg_check

check_dir()
{
if [ "$1" == "NFS" ] || [ "$1" == "SMBCIFS" ] ; then 
	#echo "Argument rights $1" 

	if [ $1  == "NFS" ] ; then
		echo "NFS"

		if  [ -d /mnt/nfs ] ; then
			:
			#echo "Directory /mnt/nfs exist"
		else 
			#echo "Creating /mnt/nfs"
		sudo mkdir /mnt/nfs
		sudo chown imm:imm /mnt/nfs
		fi
	fi


	if [ $1 == "SMBCIFS" ] ; then 
		echo "SMBCIFS"

		if [ -d /mnt/smb ]; then
			:
			#echo "Directory /mnt/smb exist"
		else
			#echo "Creating /mnt/smb"
			sudo mkdir /mnt/smb
			sudo chown imm:imm /mnt/smb
		fi
		
	fi
 
else 
	echo -e "ERROR: check_dir Wrong argument \\n"

fi
}

function argsa () {
echo "$1"
}  	


type_share()
{
# SYNOLOGY="/volume1/Place /mnt/nfs nfs nouser,atime,auto,rw,dev,exec,suid 0 0"
# SYNOLOGY_MANUAL=""
# QNAP=""
# QNAP_MANUAL=""

if [ "$1" == "SYNOLOGY_NFS" ];
		then
		arg="NFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "SYNOLOGY_SMBCIFS" ];
		then
		#echo "OK SYNOLOGY_SMBCIFS"
		arg="SMBCIFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "QNAP_NFS" ];
		then
		#echo "OK QNAP_NFS"
		arg="NFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "QNAP_SMBCIFS" ];
		then
		#echo "OK QNAP_SMBCIFS"
		arg="SMBCIFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_SYNOLOGY_NFS" ];
		then
		#echo "OK SYNOLOGY_MANUAL"
		arg="NFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_SYNOLOGY_SMBCIFS" ];
		then
		#echo "OK SYNOLOGY_MANUAL"
		arg="SMBCIFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_QNAP_NFS" ];
		then
		#echo "OK QNAP_MANUAL"
		arg="NFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_QNAP_SMBCIFS" ];
		then
		#echo "OK QNAP_MANUAL"
		arg="SMBCIFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_NFS" ];
		then
		#echo "OK Manual NFS"
		arg="NFS"
		echo "$args"
		check_dir $arg

elif [ "$1" == "MANUAL_SMB" ];
		then
		#echo "OK Manual SMB"
		arg="SMBCIFS"
		echo "$args"
		check_dir $arg

		else
		echo "Other or nothing"
		echo "$1"
fi
}

#Test mount and unmount  
manual_mount()
{
echo "check_mount()"
}

# Music
# Pictures
# Television
# Video
check_simlink()
{   
if [ $share == "NFS" ]; then
	path="mnt/nfs"
	#echo $path

elif [ $share == "SMBCIFS" ]; then
	path="mnt/smb"
	#echo $path

else 
	echo="Unknown $1"
fi

for dir in Music Pictures Television Video
do

fullpath="/$path/$dir"
mediapath="/home/imm/$dir"

if [ -d "$fullpath" ]; then
	:
	echo "$timestamp INFO Directory $fullpath exist" >> "$AUDIT"

else
	echo "Warning: directory not found $fullpath"
	echo "$timestamp ERROR: $fullpath not found symbolic link will not be created " >> "$AUDIT"
	echo "$timestamp $dir directory is missing on your Network Attached Storage " >> "$AUDIT"

fi
# Clean directory or links
if [ -d "/home/imm/$dir" ] || [ -h "/home/imm/$dir" ]; then
	sudo unlink /home/imm/$dir
	sudo rm -dr /home/imm/$dir
	sudo rm /home/imm/$dir
	create_symlink="sudo ln -s $fullpath $HOME$dir"
	#echo -e "$create_symlink \\n"
	echo -e "Symlink $dir created. \\n"
	$create_symlink

#If directory noexist create symlink
 elif [ ! -d "/home/imm/$dir" ]; then 
	create_symlink="sudo ln -s $fullpath $HOME$dir"
	#echo -e "$create_symlink \\n"
	echo -e "Symlink $dir created. \\n"
	$create_symlink



else
	echo -e "Symlink $dir can not be created. check Audit. \\n"
	echo "$timestamp Unknown directory or can not be created." >> "$AUDIT"
fi

done

}


write_simlink() 
{
# for dir in Music Pictures Television Video
# do
# fullpath="/home/imm/$dir"

# if [ ! -e $mda ]; then

echo ""
# fi
# done
}


test_mnt()
{
for dir in Music Pictures Television Video
do
path="/mnt/nfs/"
fullpath=$path"/"$dir
#cd $fullpath
        if [ -d $fullpath ]; then
                echo "Exist"
        else
                echo "No find directory $fullpath"
        fi

done
}

# Check mounting point link must be include : or //
write_fstab()
{

for manual_type in "${MANUAL[@]}" ; do
    if [ "$manual_type" == "$arg2" ]; then
		VALUE=${VALUE//_/ }
	else
     	:
   	fi
done

sudo sed -i "$ a ${VALUE}" "$FSTAB"

echo -e "write successfully \\n"
}

check_mount()
{
share=$(type_share $arg2)

if [ "$share" == "NFS" ]; then
	echo "Unmount NFS"
	sudo umount /mnt/nfs
elif [ "$share" == "SMBCIFS" ] ; then
	echo "Unmount SMB"
	sudo umount /mnt/smb

else
	#echo "MANUAL umount all"
	sudo umount /mnt/nfs
	sudo umount /mnt/smb	
fi
}

mount_test()
{

sudo mount -av > "$MOUNT_OUTPUT"
# Zero true; One fail remove line from fstab 
#echo "$?"
 if [ "$?" == 0 ]; then
 	:
 else
 	remove_mounting_point
 	echo "ERROR could not mount."
	exit 1
 fi
}

fstab_output(){
if [ $share == "NFS" ]; then
	#DEBUG or see $MOUNT_OUTPUT
	#mounting_point=`grep 'nfs' < "$MOUNT_OUTPUT"`
	mounting_point=`grep '/mnt/nfs' < "$MOUNT_OUTPUT"`
	echo -e "Mount $mounting_point \\n"

elif [ $share == "SMBCIFS" ]; then
	mounting_point=`grep '/mnt/smb' < "$MOUNT_OUTPUT"`
	echo -e "Mount $mounting_point \\n"

elif [ ! -f "$MOUNT_OUTPUT" ]; then 
	echo -e "Mounting point file $MOUNT_OUTPUT not found. \\n"

else
	echo "$timestamp Mounting point NFS or SMBCIFS not found." >> "$AUDIT"
fi
}


remove_mounting_point()
{

lines=$(sudo grep -rn '/etc/fstab' -e ':' || sudo grep -rn '/etc/fstab' -e '//')
line="${lines%%:*}"
if [ -n "$line" ]; then 
	sudo cp /etc/fstab /etc/imm/fstab.bak
	sudo sed -i.bak -e "${line}d" /etc/fstab   
	#echo "Remove mountingpoint"

else
	:
	#echo "Mounting point not found"
fi 

}

check_media_dir()
{
for dir in Music Pictures Television Video
do
fullpath="/home/imm/$dir"

if [ ! -h $fullpath ] && [ ! -d $fullpath  ]; then
	mkdir $fullpath
fi
done	

}



TESTPOINT="sudo mount -t nfs $1"
arg1=$1
arg2=$2
type_share $arg2
remove_mounting_point
check_mount



# Dictionary hack

for val in "${PREFIX_TYPE[@]}" ; do
    KEY="${val%%:*}"
    VALUE="${val#*:}"

    if [[ "$KEY"  ==  "$arg2" ]]; then
    	write_fstab
    	mount_test
    	fstab_output
    	check_simlink
    	check_media_dir

    else
    	:

    fi
done
