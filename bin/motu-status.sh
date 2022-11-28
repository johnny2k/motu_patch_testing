# Enable telnet
# POST http://MOTU_IP/start_telnet

MOTU_IP=""

echo "Mode: $(curl -s $MOTU_IP/datastore/host/mode)"

# Get sample rate
# TODO: This isn't the right way but it's visible on the display so I'm not concerned.
#echo "Sample rate $(curl -s $MOTU_IP/cfg/0/current_sampling_rate)"

# Get current buffer size
echo "Buffer size: $(curl -s $MOTU_IP/datastore/host/win/current_buffer_size_1x)"
# Get max usb channels to host

echo "Max USB channel: $(curl -s $MOTU_IP/datastore/host/maxUSBToHost)"

# Get "Safety Offset"
echo "Safety Offset: $(curl -s $MOTU_IP/datastore/host/win/current_safety_offset_1x)"
