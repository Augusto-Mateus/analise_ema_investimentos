# 📈 Análise de Estratégia de Trading: EMA vs. Buy & Hold (TQQQ)

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)]() 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
### 🔗 Acesse o Relatório [Aqui](https://github.com/Augusto-Mateus/analise_ema_investimentos/blob/main/avaliacao_estrategia.ipynb)

## 💡 Sobre o Projeto

Este projeto de **Análise Quantitativa** visa testar a eficácia da **Média Móvel Exponencial (EMA)** como indicador de *timing* para investimentos. A estratégia é comparada com o investimento passivo (*Buy and Hold*) no ativo alavancado **TQQQ**, que potencializa a visualização dos resultados.

### Principais Habilidades Demonstradas:
* Análise de Séries Temporais (Financeiras)
* Backtesting de Estratégias de Trading
* Manipulação de Dados com Pandas
* Visualização de Dados para Comparação de Performance

## 📊 Resultados Chave (timeframe de 8 anos com intervalos de 1 dia)

| Estratégia | Retorno Total |
| :--- | :--- |
| **EMA** | ~ +1246,86% |
| **Buy & Hold** | ~ +1152,96% |

![Imagem output.png](https://github.com/Augusto-Mateus/analise_ema_investimentos/blob/main/grafs/output.png?raw=true)

É importante notar que este resultado é recorte de um timeframe específico com um span específico. O resultado pode variar de acordo com as configurações.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Pandas:** Manipulação e preparo dos dados.
* **yfinance:** Download dos dados históricos do TQQQ.
* **Matplotlib:** Criação de gráficos de comparação de performance.
* **NumPy:** Empregada para otimizar operações.

## 🔄 Melhorias Recentes

* **Remoção de Redundâncias:** O notebook e o módulo foram otimizados para eliminar cálculos duplicados e simplificar a lógica.
* **Ajustes nos Gráficos:** Os gráficos foram aprimorados para melhorar a clareza e a apresentação dos dados, com legendas mais informativas e escalas ajustadas.
* **Estrutura Modular:** O código foi reorganizado para facilitar a reutilização e a manutenção.
* **Remoção de lookahead:** A lógica de implementação da estratégia foi ajustada para retornar resultados menos enviesados.

## ⏭️ Próximas Etapas (Roadmap)

* **Inclusão do SQQQ:** Adicionar a lógica para operar no ativo inverso (**SQQQ**) durante tendências de baixa, buscando rentabilidade em quedas.
* **Combinação de Indicadores:** Adicionar **RSI** e **MACD** para validar os sinais e reduzir a latência e os sinais falsos da estratégia atual.