pip install -r .\requirements.txt
start python .\BV.py 192.168.15.67 5000
start python .\Robo_N.py 192.168.15.67 3000 192.168.15.67:5000
start python .\Banco_N_HB.py 192.168.15.67 3500 192.168.15.67:3000
start python .\Robo_N.py 192.168.15.67 4000 192.168.15.67:5000
start python .\Banco_N_HB.py 192.168.15.67 4500 192.168.15.67:4000