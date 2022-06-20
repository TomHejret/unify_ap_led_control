# Ubiquiti Unify AP LED control script
Script to control your Ubiquiti Unify AP LED status light. It can only turn on and off "AP location" LED blinking.

## Prerequisites
The script requires running Unify Controller where AP, you want to control, has been adopted.

## Limitations
If you want to control LED without Unify Controller, set light color or pattern have a look at the
[Home Assistant forum](https://community.home-assistant.io/t/control-unifi-ap-status-led/188063) or feel free to 
improve the script and help others.

**Just, please, pay attention to backwards compatibility and never commit any secrets, keys, passwords or any other 
sensitive data!**

## How to use
- fill 4 default variables at the beginning of the script according to your setup
- run the script like:
  - ./unify_ap_led_control.py
  - ./unify_ap_led_control.py --off
  - ./unify_ap_led_control.py --mac aa:bb:cc:dd:ee:ff
  - ./unify_ap_led_control.py --mac aa:bb:cc:dd:ee:ff --off
- profit!

## Versions
Tested with:
- Unify Controller: 6.5.55
- UAP-AC-Lite, Firmware Version: 6.0.21

## Disclaimer
Use at your own risk and responsibility.