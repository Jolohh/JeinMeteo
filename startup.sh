#!/bin/sh
# startup.sh
# start python script from venv

while ! ip route | grep -oP 'default via .+ dev eth0'; do
  echo "interface not up, will try again in 1 second";
  sleep 1;
done


sudo /home/unix/project/.venv/bin/python /home/unix/project/mqttPublisher.py



