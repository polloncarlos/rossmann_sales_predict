![Rossmann Logo](img/rossmann_logo.jpg)

<h1>📈 Rossmann Sales Forecast — Projeto End-to-End de Ciência de Dados</h1>

<p>
<strong>Previsão de vendas para 1.115 lojas da Rossmann (horizonte de 6 semanas)</strong>, 
desenvolvida a partir de um pipeline completo de Ciência de Dados baseado no 
<strong>CRISP-DM</strong>, com foco em <em>valor de negócio</em>, <em>tomada de decisão executiva</em> 
e <em>deploy</em>.
</p>

<hr/>

<h2>🎯 Problema de Negócio</h2>

<p>
O CFO da Rossmann decidiu iniciar reformas estruturais em parte das lojas da rede. 
Para viabilizar esse planejamento financeiro, foi solicitado aos gerentes que estimassem 
o faturamento das próximas <strong>6 semanas</strong>, permitindo provisionar corretamente 
o capital necessário para cada reforma.
</p>

<p>
O problema é que, até então, essas previsões eram feitas de forma <strong>manual e descentralizada</strong>, 
onde cada gerente utilizava critérios próprios, sem padronização e sem considerar de forma 
estruturada fatores como promoções, concorrência, sazonalidade e feriados.
</p>

<p>
Diante desse cenário, este projeto tem como objetivo <strong>automatizar e padronizar</strong> 
as previsões de faturamento, entregando os resultados de forma simples e acessível 
via <strong>aplicativo Telegram</strong>, permitindo:
</p>

<ul>
  <li>Consulta rápida por loja</li>
  <li>Comparação entre múltiplas lojas</li>
  <li>Identificação da loja com maior faturamento previsto</li>
  <li>Visualização da diferença de faturamento entre as melhores lojas</li>
</ul>

<hr/>

<h2>📌 Premissas do Negócio</h2>
<ul>
  <li>As previsões estão disponíveis <strong>24/7</strong> via Telegram, bastando informar o código da loja.</li>
  <li>Apenas lojas com histórico de vendas maior que zero foram consideradas para previsão.</li>
  <li>Dias em que as lojas estavam fechadas foram removidos da modelagem.</li>
  <li>Caso o usuário consulte uma loja fechada ou inexistente, o sistema retorna uma mensagem informativa.</li>
</ul>

<hr/>

<h2>🧩 Metodologia — CRISP-DM</h2>
<ol>
  <li>Entendimento do Problema de Negócio</li>
  <li>Coleta e Descrição dos Dados</li>
  <li>Limpeza e Tratamento de Dados</li>
  <li>Análise Exploratória de Dados (EDA)</li>
  <li>Preparação dos Dados</li>
  <li>Engenharia e Seleção de Features (Boruta + ExtraTrees)</li>
  <li>Modelagem (Baseline → XGBoost)</li>
  <li>Cross-Validation Temporal</li>
  <li>Fine-Tuning com Optuna</li>
  <li>Avaliação e Tradução para Negócio</li>
  <li>Deploy em Produção</li>
</ol>

<hr/>

<h2>📊 Avaliação do Modelo</h2>

<p>
O modelo foi avaliado utilizando <strong>validação temporal</strong>, simulando o comportamento real 
de previsões futuras. A métrica principal utilizada foi o <strong>RMSE</strong>, interpretado também 
sob a ótica de impacto financeiro.
</p>

<!-- Gráfico Real vs Predito -->
<strong>Vendas Reais vs Previsões</strong>
<p>
Este gráfico demonstra a capacidade do modelo em acompanhar o comportamento real das vendas 
ao longo do tempo, evidenciando boa aderência às variações sazonais.
</p>

![Sales x Predictions](img/sales_vs_predictions_timeseries.png)

<!-- Gráfico Distribuição do Erro -->
<strong>Distribuição do Erro</strong>
<p>
A distribuição do erro mostra uma concentração próxima de zero, indicando estabilidade do modelo 
e menor risco de erros extremos, o que é fundamental para decisões financeiras.
</p>

![Error Distribution](img/error_distribution.png)

<hr/>

<h2>📈 Evolução do Modelo</h2>

<table border="1" cellpadding="6">
  <tr>
    <th>Versão</th>
    <th>Modelo</th>
    <th>Seleção de features</th>
    <th>Tuning</th>
    <th>RMSE</th>
    <th>Observação</th>
  </tr>
  <tr>
    <td>Baseline</td>
    <td>Média (Average Model)</td>
    <td>-</td>
    <td>-</td>
    <td>1835</td>
    <td>Referência: prevê a média de vendas</td>
  </tr>
  <tr>
    <td>v1</td>
    <td>XGBoost</td>
    <td>Boruta + RandomForest</td>
    <td>Random Search</td>
    <td>1120</td>
    <td>Primeira versão do XGBoost</td>
  </tr>
  <tr>
    <td>v2</td>
    <td>XGBoost</td>
    <td>Boruta + ExtraTrees</td>
    <td>Optuna</td>
    <td>895</td>
    <td>Melhor performance offline</td>
  </tr>
  <tr>
    <td>v3</td>
    <td>XGBoost</td>
    <td>Reutilização das features</td>
    <td>Optuna</td>
    <td>912</td>
    <td>Versão final compatível com Render (512MB)</td>
  </tr>
</table>

<p>
Em todas as versões o modelo de previsão é o XGBoost. RandomForest e ExtraTrees aparecem só
como estimadores internos do Boruta, na etapa de seleção de features. Contra o baseline pela
média (RMSE 1.835), a versão final reduz o erro em 50% (MAPE de 9,2%).
</p>

<p>
Apesar de uma leve perda de performance em relação à v2, a versão final foi escolhida 
por garantir <strong>estabilidade, menor consumo de memória e viabilidade de deploy</strong> 
no plano gratuito do Render (512 MB).
</p>

<hr/>

<h2>💡 Principais Insights de Negócio</h2>

<strong>Competição e Distância</strong>
<p>
Foi identificado que lojas com competidores mais próximos apresentam, em média, 
<strong>maior volume de vendas</strong>, contrariando o senso comum. Esse comportamento sugere 
que regiões com maior competitividade tendem a concentrar maior fluxo de consumo.
</p>

![Sales by Competition Distance](img/sales_by_competition_distance.png)

<p>
Por outro lado, ao longo do tempo, a presença contínua de competidores tende a reduzir 
gradualmente as vendas, indicando possível saturação do mercado local.
</p>

![Sales by Competition Time](img/sales_by_competition_time.png)

<hr/>

<strong>Promoções Regulares vs Estendidas</strong>
<p>
Promoções iniciadas após períodos sem descontos apresentam crescimento significativo de vendas, 
mostrando-se eficazes para alavancagem de faturamento.
</p>

![Regular Promotion](img/regular_promo_analysis.png)

<p>
Entretanto, promoções consecutivas (promoções estendidas) demonstraram queda de performance, 
indicando possível desgaste do estímulo ao consumidor.
</p>

![Extended Promotion](img/extended_promo_analysis.png)

<p>
Esse insight abre espaço para decisões estratégicas sobre <strong>frequência e duração de campanhas promocionais</strong>.
</p>

<hr/>

<strong>Sazonalidade Mensal</strong>
<p>
Observou-se que o maior volume de vendas ocorre após o dia 10 de cada mês, possivelmente associado 
a ciclos de pagamento da população. Esse padrão pode orientar decisões de estoque e campanhas direcionadas.
</p>

![Sales by Day of Month](img/sales_by_day_of_month.png)

<hr/>

<h2>🚀 Produto de Dados (deploy)</h2>
<ul>
  <li>API Flask para previsões de vendas</li>
  <li>Bot Telegram para interação em tempo real</li>
  <li>Deploy no Render (plano gratuito)</li>
</ul>

<p><strong>Repositórios relacionados:</strong></p>
<ul>
  <li><a href="https://github.com/polloncarlos/rossmann_api">Rossmann API</a></li>
  <li><a href="https://github.com/polloncarlos/rossmann_telegram_bot">Rossmann Telegram Bot</a></li>
</ul>

<hr/>

<h3>🤖 Interface de Consumo — Bot Telegram</h3>
<hr/>
<p>
Para garantir que as previsões fossem realmente utilizadas na prática, 
foi desenvolvido um <strong>bot no Telegram</strong> como camada de interface 
entre o modelo e os decisores do negócio.
</p>

<p>
Essa abordagem elimina a necessidade de dashboards complexos ou acesso técnico, 
permitindo que executivos e gestores consultem previsões de forma 
<strong>rápida, intuitiva e em tempo real</strong>.
</p>

<ul>
  <li>Consulta individual por código da loja</li>
  <li>Consulta de múltiplas lojas em uma única mensagem</li>
  <li>Ranking automático por faturamento previsto</li>
  <li>Identificação da loja com maior e segunda maior previsão</li>
  <li>Cálculo da diferença de faturamento entre as lojas líderes</li>
</ul>

<p>
A resposta do bot retorna valores formatados, feedback de processamento 
e mensagens claras em casos de erro ou indisponibilidade do serviço, 
reforçando a experiência do usuário.
</p>

<!-- Imagem do funcionamento do bot -->
<p align="center">
  <img src="img/rossmann_telegram_bot.png"/>
</p>

<p>
Essa solução aproxima o modelo do contexto real de tomada de decisão, 
transformando previsões estatísticas em <strong>informação acionável</strong>.
</p>

<hr/>

<h2>🛠️ Stack Tecnológica</h2>
<ul>
  <li>Python 3.10</li>
  <li>Pandas, NumPy, Scikit-learn</li>
  <li>XGBoost</li>
  <li>Optuna</li>
  <li>Flask</li>
  <li>Render</li>
</ul>

<hr/>

<h2>📌 Conclusão</h2>
<p>
Este projeto representa a construção de uma solução completa de Ciência de Dados,
indo da compreensão do problema de negócio até a entrega de um produto funcional publicado.
Ao longo do processo, foram aplicadas boas práticas de análise, modelagem e deploy,
sempre com foco em gerar valor real para o negócio.
</p>

<p>
O trabalho demonstra capacidade de estruturar problemas, tomar decisões técnicas conscientes
(dados, modelo e infraestrutura) e transformar análises em informações acionáveis,
mesmo sob restrição real de infraestrutura (512 MB).
</p>