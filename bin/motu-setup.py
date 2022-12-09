#!/usr/bin/env python3

import json
import os, typing
import urllib.request as request

MOTU_CONFIG_FILE="~/.config/motu_patch_setup.json"

cfg_dict={}

def updateConfig():
    _MOTU_CONFIG_FILE_exp=os.path.expandvars(os.path.expanduser(MOTU_CONFIG_FILE))
    print(f"Using configuration file: {_MOTU_CONFIG_FILE_exp}")
    os.makedirs( os.path.dirname(_MOTU_CONFIG_FILE_exp), exist_ok=True )

    global cfg_dict

    if ( os.path.isfile(_MOTU_CONFIG_FILE_exp) ):
        with open( _MOTU_CONFIG_FILE_exp, 'r') as f:
            cfg = f.read()
            cfg_dict=json.loads(cfg)

    if 'IP' not in cfg_dict.keys():
        cfg_dict['IP'] = input("Please enter the IP-number or resolvable network name for your MOTU device: ")
    if 'SampleRate' not in cfg_dict.keys():
        cfg_dict['SampleRate'] = input("Please enter sample rate: ")
    if 'NumChannels' not in cfg_dict.keys():
        cfg_dict['NumChannels'] = input("Please enter number of channels (24, 32, 64): ")
    if 'BufferSize' not in cfg_dict.keys():
        cfg_dict['BufferSize'] = input("Please enter the Idesired buffer-size (16,32,64,128,256,512,1024): ")

    cfg = json.dumps(cfg_dict, sort_keys=True, indent=4)
    with open( _MOTU_CONFIG_FILE_exp, 'w') as f:
        f.write(cfg)
    print(f"MOTU Configuration: IP = {cfg_dict['IP']}, SAMP_RATE = {cfg_dict['SampleRate']}, NUM_CHAN = {cfg_dict['NumChannels']}, buffer_size = {cfg_dict['BufferSize']}")


#------------------------------
def toJsonPayloadStr(value:str,):
    return 'json={"value":' + f'"{value}"' + '}'
def toJsonPayloadInt(value:int):
    return 'json={"value":' + f'"{str(value)}"' + '}'
#------------------------------

def getValue(subtreeString:str):
    global cfg_dict
    with request.urlopen(f"http://{cfg_dict['IP']}/datastore/{subtreeString}") as req:
        if ( req.getcode() != 200 ):
            print('An error occurred while attempting to retrieve data from the API.')
            exit(1)
        _json = json.loads( req.read() )
        return _json['value']

def setValue(subtreeString:str, data:str):
    import requests
    global cfg_dict
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return requests.post(f"http://{cfg_dict['IP']}/datastore/{subtreeString}", headers=headers, data=data)

def configureMOTUDevice():
    motu_uid=getValue('uid')
    print(f"UID for this device = {motu_uid}")

    # Set to UAC mode (USB Audio Class)
    #
    print(f"Setting to UAC mode (USB Audio Class)", end=': ')
    data = toJsonPayloadStr("UAC")
    response = setValue("host/mode", data=data)
    print(response)

    # Set buffer size
    #
    # You can also check your current buffer size and set the device to the same.
    # buffer_size=$(cat /proc/asound/card0/pcm0p/sub0/hw_params | grep buffer_size | awk '{print $2 }')
    print(f"Setting buffer size to {cfg_dict['BufferSize']}", end=': ')
    data = toJsonPayloadInt(cfg_dict['BufferSize'])
    response = setValue("host/win/current_buffer_size_1x", data=data)
    print(response)

    # Set channel count
    #
    print(f"Setting max channels to {cfg_dict['NumChannels']}", end=': ')
    data = toJsonPayloadInt(cfg_dict['NumChannels'])
    response = setValue("host/maxUSBToHost", data=data)
    print(response)


    # Set sample rate
    print(f"Setting sample rate to {cfg_dict['SampleRate']}", end=': ')
    data = toJsonPayloadInt(cfg_dict['SampleRate'])
    response = setValue(f"avb/{motu_uid}/cfg/0/current_sampling_rate", data=data)
    print(response)

    # Set "Safety Offset"
    #
    #safety_offset=1024
    #echo "Setting safety offset to $safety_offset"
    #curl --data 'json={"value":'"$safety_offset"'}' ${MOTU_IP}/datastore/host/win/current_safety_offset_1x


if __name__ == "__main__":
   updateConfig()
   configureMOTUDevice()
