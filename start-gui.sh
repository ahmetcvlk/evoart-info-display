#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/evoart/.Xauthority
export QT_QPA_PLATFORM=xcb
source /home/evoart/miniforge3/etc/profile.d/conda.sh
conda activate pyqt-env

python /home/evoart/Desktop/evoart-info-display/mainWindow.py


