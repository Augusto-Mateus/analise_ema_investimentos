# 📈 Análise de Estratégia de Trading: EMA vs. Buy & Hold (TQQQ)

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)]() 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
### 🔗 Acesse o Relatório / Notebook Online [Link AQUI]

## 💡 Sobre o Projeto

Este projeto de **Análise Quantitativa** visa testar a eficácia da **Média Móvel Exponencial (EMA)** como indicador de *timing* para investimentos. A estratégia é comparada com o investimento passivo (*Buy and Hold*) no ativo alavancado **TQQQ**, que potencializa a visualização dos resultados.

### Principais Habilidades Demonstradas:
* Análise de Séries Temporais (Financeiras)
* Backtesting de Estratégias de Trading
* Manipulação de Dados com Pandas
* Visualização de Dados para Comparação de Performance

## 📊 Resultados Chave (1 ano)

| Estratégia | Retorno Total |
| :--- | :--- |
| **EMA** | ~ +131,76% |
| **Buy & Hold** | ~ 49,93% |

![Imagem output.png](https://github.com/Augusto-Mateus/analise_ema_investimentos/blob/main/grafs/output.png?raw=true)

É importante notar que este resultado é recorte de um timeframe específico com um span específico. O resultado pode variar de acordo com as variáveis.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas:** Manipulação e preparo dos dados.
* **yfinance:** Download dos dados históricos do TQQQ.
* **Matplotlib:** Criação de gráficos de comparação de performance.

## ⏭️ Próximas Etapas (Roadmap)

* **Inclusão do SQQQ:** Adicionar a lógica para operar no ativo inverso (**SQQQ**) durante tendências de baixa, buscando rentabilidade em quedas.
* **Otimização do EMA:** Implementar um módulo de backtesting para analisar e encontrar o *span* ideal do EMA para diferentes *timeframes*.
* **Combinação de Indicadores:** Adicionar **RSI** e **MACD** para validar os sinais e reduzir a latência e os sinais falsos da estratégia atual.