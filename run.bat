pip install -r .\requirements.txt
start python .\BV.py 127.0.0.1 5000
start python .\Robo_N.py 127.0.0.1 3000 127.0.0.1:5000
start python .\Banco_N_HB.py 127.0.0.1 3500 127.0.0.1:3000
start python .\Robo_N.py 127.0.0.1 4000 127.0.0.1:5000
start python .\Banco_N_HB.py 127.0.0.1 4500 127.0.0.1:4000