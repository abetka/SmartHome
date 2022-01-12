################################################################################
### Update from older versions containig client and server together:
################################################################################

# Remove old installation from /opt/imm
rm -r /opt/imm/

# !!! IMPORTANT: Keep settings in /etc/imm untouched

# Rest is the same as fresh install

################################################################################
### Fresh installation of imm server:
################################################################################

# Unpack archive
tar -xzf [archive].tar.gz
# change directory to [archive]
cd [archive]
# Run install script
sudo bash install.sh

# restart server


################################################################################
### Update from previous version of imm server:
################################################################################

# stop running imm_server
/etc/init.d/imm_server stop

#install according previous step

# if there were any custom settings in imm_server.cfg or supervisord.cfg
# move them from /opt/imm/imm_server.cfg.old and /opt/imm/supervisord.cfg.old to newly installed files

# start imm_server
/etc/init.d/imm_server start

