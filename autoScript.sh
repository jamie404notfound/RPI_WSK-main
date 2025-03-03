# Change directory to required destination
cd ~/.config/lxsession/LXDE-pi/autostart

# Run required Desktop GUI and Login user
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
point-rpi
# Open new terminal
@lxterminal
# Execute Python script
-e sudo python readSensors.py