#!/bin/bash

pip install -r requirements.txt
python BV.py 192.168.15.67 5000 &
python Robo_B.py 192.168.15.67 3000 192.168.15.67:5000 &
python Banco_B_HB1.py 192.168.15.67 3500 192.168.15.67:3000 &
python Robo_A.py 192.168.15.67 4000 192.168.15.67:5000 &
python Banco_A_HB2.py 192.168.15.67 4500 192.168.15.67:4000 &