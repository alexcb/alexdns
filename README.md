# alexdns
python-based dns server as an alternative to dnsmasq for those who want to hack python code rather than config software

# setup
pip3 install dnslib dnspython

# disabling systemd-resolve
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

sudo systemctl enable alexdns
echo 'nameserver 127.0.0.1' | sudo tee /etc/resolv.conf
