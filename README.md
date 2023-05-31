# Integrantes

1 - Amanda de Sousa Martins           R.A: 22.120.004-1<br><br>
2 - Kawê Vinicius Barboza de Carvalho R.A: 22.120.018-1<br><br>
3 - Nicolas Moretti Trevizam          R.A: 22.120.011-6<br><br>
4 - Rafael Carraro Martins            R.A: 22.120.025-6<br><br>

# Testes realizados em ambiente *Windows*

Como demonstrado nas logs de compra, o ip das solicitações é diferente<br>
Maneira como foi ajustada:<br>
Máquina 1 (Winodws):
```
pip install -r .\requirements.txt
start python .\BV.py 192.168.15.40 5000
start python .\Robo_N.py 192.168.15.40 3500 192.168.15.40:5000
start python .\Banco_N_HB.py 192.168.15.40 3000 192.168.15.40:3500
```

Máquina 2 (Winodws):
```
start python .\Robo_N.py 192.168.15.168 2500 192.168.15.40:5000
start python .\Banco_N_HB.py 192.168.15.168 2000 192.168.15.168:2500
```

# Simulação de uma Bolsa de Valores com Home Brokers

Este projeto tem como objetivo simular uma bolsa de valores, fornecendo uma interface de usuário através de um sistema de home brokers.<br>


## Instalação

>Python superior ou igual à 3.7

1. Clone este repositório para o seu ambiente local.

```
git clone https://github.com/rcarraro/Sistemas-Distribuidos.git
```
2. Acesse o diretório do projeto.

```
cd Sistemas-Distribuidos
```

3. Instale as dependências do projeto.

```
pip install -r requirements.txt
```

## Uso

1. Inicie a aplicação.

Windows:
```
Execute o run.bat
```
<br>
Linux:

```
Execute o run.sh
```

Ou vá até o diretório correto
```
Ex: cd /etc/systemd/system
```

Crie o serviço:
```
nano nome_serviço.service
```

Preencha ele para o robo, banco e BV:
```
Ex:
Description=Run
StartLimitIntervalSec=0
[Service]
User=root
ExecStart=python /caminho/Robo_N.py *ip* *porta* *ip:porta(BV)*

[Install]
WantedBy=multi-user.target
```
>Seguindo os padrões:<br>
>python /caminho/BV.py *ip* *porta*<br>
>python /caminho/Robo_N.py *ip* *porta* *ip:porta(BV)*<br>
>python /caminho/Banco_N_HB.py *ip* *porta* *ip:porta(Robo)*<br>
>lembre-se de rodar antes a BV, depois o Robo e por fim o Banco.


Adicione o seu serviço:
```
sudo systemctl daemon-reload
```

Dê um enable no seu serviço:
```
sudo systemctl enable nome_serviço.service
```

Basta dar o start agora:
```
sudo systemctl start nome_serviço.service
```

### Mudanças possíveis

Acesse o código .bat ou .bash e altere seguindo o padrão:
```
start python .\BV.py *ip* *porta*
start python .\Robo_N.py *ip* *porta* *ip:porta(BV)*
start python .\Banco_N_HB.py *ip* *porta* *ip:porta(Robo)*
```

>Vale lembrar que o número de robôs e homebrokers, pode ser aumentado infinitamente, basta seguir o padrão de ip e, não repetir nenhuma porta.<br>
>não é necessário abrir outra Bolsa de valores, apenas Robos e Bancos

Ex:

```
start python .\BV.py 192.168.15.67 5000
start python .\Robo_N.py 192.168.15.67 3000 192.168.15.67:5000
start python .\Banco_N_HB1.py 192.168.15.67 3500 192.168.15.67:3000
```
## Visualização

1 -O uso do código gera arquivos de logs. Estes demonstram as compras e vendas realizadas, bem como as solicitações de mudanças de horários.

2 - Para visualizar a mudança de preço nas ações, basta executar o graphs.bat
