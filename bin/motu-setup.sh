#!/bin/bash


MOTU_IP="192.168.178.100"
buffer_size=512

# Set to Vendor mode (USB2)
#
echo "Setting to vendor mode USB2"
curl --data 'json={"value":"UAC"}' $MOTU_IP/datastore/host/mode
exit

# Set buffer size
#
# You can also check your current buffer size and set the device to the same.
# buffer_size=$(cat /proc/asound/card0/pcm0p/sub0/hw_params | grep buffer_size | awk '{print $2 }')
echo "Setting buffer size to $buffer_size"
curl --data 'json={"value":'"$buffer_size"'}' $MOTU_IP/datastore/host/win/current_buffer_size_1x


# Set channel count to 32 (24, 32, 64)
#
echo "Setting max channels to 32"
curl --data 'json={"value":32}' $MOTU_IP/datastore/host/maxUSBToHost


# Set sample rate to 48000
#
echo "Setting sample rate to 48000"
curl -X POST -F 'json={"avb/0001f2fffe01542c/cfg/0/current_sampling_rate":48000}' http://$MOTU_IP/datastore


# Set "Safety Offset"
#
#safety_offset=1024
#echo "Setting safety offset to $safety_offset"
#curl --data 'json={"value":'"$safety_offset"'}' $MOTU_IP/datastore/host/win/current_safety_offset_1x
