# service level running for data collection ( ottoMicroLogger.py )

In this case, ottoMicroLogger.py which to be executed on startup, is located in
~/foocars/cars/services/

the services file, ottMicroLogger.service, also located in ~/foocars/cars/services/
looks like this:


[Unit]
Description=Data logging for ottoMicro car

[Service]
Type=simple
ExecStart=/usr/local/bin/ottoMicroLogger.py
Restart=always
StandardOutput=journal

[Install]
WantedBy=multi-user.target
Alias=ottoMicroLogger.service


while in directory /usr/local/bin, create a symlink thusly:
ln -s ~/foocars/cars/services/ottoMicroLogger.py

while in directory /lib/systemd/system, create a another symlink thusly:
ln -s ~/foocars/cars/services/ottoMicroLogger.service

To enable the service:
sudo systemctl enable ~/foocars/cars/services/ottoMicroLogger.service
once on the system. This will cause the service to be started when the system is started.

To manually start the service:
sudo systemctl start ottoMicroLogger.service

To manually stop:
sudo systemctl stop ottoMicroLogger.service

To check status of ottoMicroLogger.py:
sudo systemctl status ottoMicroLogger.service

To see output of ottoMicroLogger.py for debugging:
sudo journalctl -u ottoMicroLogger.service
