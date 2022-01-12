sudo apt-get install net-snmp
sudo cp snmpd.conf /etc/snmp/
mkdir /home/imm/monitoring
cp snmp.py /home/imm/monitoring/
source /opt/imm/.virtualenvs/imm_server/bin/activate
pip install snmp-passpersist
