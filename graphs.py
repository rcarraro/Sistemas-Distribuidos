import math
import plotly.graph_objects as go
import pandas as pd
data = []
valores = {}
with open('valores_acao.txt', "r") as arquivo:
    for item in arquivo:
        data_app = item.split(" ")[2]+" "+ item.split(" ")[3].replace("\n", "")
        try:
            valores[item.split(" ")[0]]["datas"].append(data_app)
            valores[item.split(" ")[0]]["valores"].append((math.ceil(float(item.split(" ")[1])*100)/100))
        except:
            valores[item.split(" ")[0]] = {'valores':[],'datas':[]}
            valores[item.split(" ")[0]]["valores"] = [(math.ceil(float(item.split(" ")[1])*100)/100)]
            valores[item.split(" ")[0]]["datas"] = [data_app]

fig = go.Figure()

for item in valores:
    fig.add_trace(
        go.Scatter(x=valores[item]["datas"], y=valores[item]["valores"],name=item,
        ))
    

fig.update_layout(
    title_text="Valores das ações"
)

fig.show()