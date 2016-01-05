# tkill

This script (and MacOS app based on this script) allows uTorrent to run only if VPN is active

Every second script's logic checks two things:
1. If 'ppp' interface is in the output of 'ifconfig -lu'
2. Is uTorrent.app running ('ps -ax')

If uTorrent.app is running but 'ppp' interface is not active - it kills uTorrent.app with SIGTERM (15).


To run from Terminal:<br>
sudo chmod +x tkill.py<br>
./tkill.py<br>
