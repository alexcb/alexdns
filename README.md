# alexdns
python-based dns server as an alternative to dnsmasq for those who want to hack python code rather than config software

# running locally against port 53
sudo bash -c "PYTHONPATH=`pwd` ./bin/alexdns"

# install
sudo rm -rf build/ dist/ alexdns.egg-info/;
find . -name *.pyc | xargs -r sudo rm
find . -name __pycache__ | xargs -r sudo rm -rf
sudo pip3 uninstall -y alexdns
sudo rm -rf /usr/local/lib/python3.6/dist-packages/alexdns/

sudo sh -c "HOME=/ ./setup.py install"
sudo cp etc/systemd/system/alexdns.service /etc/systemd/system/alexdns.service
sudo cp bin/alexdns /usr/local/bin/.

# disabling systemd-resolve
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

sudo systemctl enable alexdns
echo 'nameserver 127.0.0.1' | sudo tee /etc/resolv.conf

# wtf python

