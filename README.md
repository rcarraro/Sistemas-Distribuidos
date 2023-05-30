# Integrantes

Amanda de Sousa Martins           R.A: 22.120.004-1
Kawê Vinicius Barboza de Carvalho R.A: 22.120.018-1
Nicolas Moretti Trevizam          R.A: 22.120.011-6
Rafael Carraro Martins            R.A: 22.120.025-6

# Simulação de uma Bolsa de Valores com Home Brokers

Este projeto tem como objetivo simular uma bolsa de valores, fornecendo uma interface de usuário através de um sistema de home brokers.

## Instalação

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

```
Execute o run.bat ou run.sh
```

### Mudanças possíveis

Acesse o código .bat ou .bash e altere seguindo o padrão:
```
start python .\BV.py *ip* *porta*
start python .\Robo_B.py *ip* *porta* *ip:porta(BV)*
start python .\Banco_B_HB1.py *ip* *porta* *ip:porta(Robo)*
```

>Vale lembrar que o número de robôs e homebrokers, pode ser aumentado infinitamente, basta seguir o padrão de ip e, não repetir nenhuma porta.

Ex:

```
start python .\BV.py 192.168.15.67 5000
start python .\Robo_B.py 192.168.15.67 3000 192.168.15.67:5000
start python .\Banco_B_HB1.py 192.168.15.67 3500 192.168.15.67:3000
```
## Visualização

1 -O uso do código gera arquivos de logs. Estes demonstram as compras e vendas realizadas, bem como as solicitações de mudanças de horários.

2 - Para visuzliar a mudança de preço nas ações, basta executar o graphs.bat ou o graphs.sh
