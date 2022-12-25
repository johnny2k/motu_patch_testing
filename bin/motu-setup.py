#!/usr/bin/env python3

import json
import os, typing
import urllib.request as request
import argparse
import readline #Import readline for enabling it in the input() calls.


MOTU_CONFIG_FILE="~/.config/motu_patch_setup.json"

cfg_dict={}

#---------------------------------------------------------------------------------
def getValue(subtreeString:str) -> str :
    global cfg_dict
    with request.urlopen(f"http://{cfg_dict['IP']}/datastore/{subtreeString}") as req:
        if ( req.getcode() != 200 ):
            print('An error occurred while attempting to retrieve data from the API.')
            exit(1)
        _json = json.loads( req.read() )
        return str( _json['value'] )

def setValue(subtreeString:str, data:str):
    import requests
    global cfg_dict
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return requests.post(f"http://{cfg_dict['IP']}/datastore/{subtreeString}", headers=headers, data=data)
#---------------------------------------------------------------------------------
def printSetting(settingName:str):
    print(f"{settingName} = {cfg_dict[settingName]}")

def updateSetting(settingName:str, promptText:str, reconfig:bool=False):
    if reconfig:
        if settingName in cfg_dict.keys():
            curValue = cfg_dict[settingName]
        else:
            curValue = ""
    
    if settingName not in cfg_dict.keys() or reconfig:
        userVal = input(promptText + f" (ENTER for current value {curValue}) : ")
        if userVal:
            cfg_dict[settingName] = userVal
        else:
            cfg_dict[settingName] = curValue
    return cfg_dict[settingName]


def updateConfig(reconfig:bool=False):
    _MOTU_CONFIG_FILE_exp=os.path.expandvars(os.path.expanduser(MOTU_CONFIG_FILE))
    print(f"Using configuration file: {_MOTU_CONFIG_FILE_exp}")
    os.makedirs( os.path.dirname(_MOTU_CONFIG_FILE_exp), exist_ok=True )

    global cfg_dict

    if ( os.path.isfile(_MOTU_CONFIG_FILE_exp) ):
        with open( _MOTU_CONFIG_FILE_exp, 'r') as f:
            cfg = f.read()
            cfg_dict=json.loads(cfg)

    #---------------------------
    val = updateSetting('IP', "Please enter the IP-number or resolvable network name for your MOTU device", reconfig)
    #---------------------------
    val = updateSetting('NumChannels', f"Please enter number of channels [24, 32, 64]", reconfig)
    #---------------------------
    valid_sample_rates=[ v for v in getValue('avb/0001f2fffe012e8a/cfg/0/sample_rates').split(':') ]
    valid_sample_rates_str = ','.join(valid_sample_rates)
    val = updateSetting('SampleRate', f"Please enter sample rate ({valid_sample_rates_str})", reconfig)
    if val not in valid_sample_rates:
        print(f"Desired sample-rate ({val}) is not valid. Choose from {valid_sample_rates_str}.")
        exit(1)
    #---------------------------
    valid_buffer_sizes=[ v for v in getValue('host/win/buffer_sizes_1x').split(':') ]
    valid_buffer_sizes_str = ','.join(valid_buffer_sizes)
    val = updateSetting('BufferSize', f"Please enter the desired buffer-size ({valid_buffer_sizes_str})", reconfig)
    if val not in valid_buffer_sizes:
        print(f"Desired buffer-size ({val}) is not valid. Choose from {valid_buffer_sizes_str}.")
        exit(1)
    #---------------------------


    cfg = json.dumps(cfg_dict, sort_keys=True, indent=4)
    with open( _MOTU_CONFIG_FILE_exp, 'w') as f:
        f.write(cfg)
    
    print()
    print("------------------------")
    print(f"MOTU Configuration:")
    printSetting('IP')
    printSetting('SampleRate')
    printSetting('NumChannels')
    printSetting('BufferSize')
    print("------------------------")


#------------------------------
def toJsonPayloadStr(value:str,):
    return 'json={"value":' + f'"{value}"' + '}'
def toJsonPayloadInt(value:int):
    return 'json={"value":' + f'"{str(value)}"' + '}'
#------------------------------
def configureMOTUDevice():
    print()
    print("Sending settings to device....")
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
   
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reconfig", help="reconfigure settings (with new values)", action="store_true")
    args = parser.parse_args()
   
    updateConfig(reconfig=args.reconfig)
    configureMOTUDevice()
