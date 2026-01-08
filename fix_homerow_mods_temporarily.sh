#!/bin/bash

sudo chgrp uinput /dev/uinput
sudo chmod g+w /dev/uinput
sudo chmod g+r /dev/uinput
systemctl --user start kanata.service
