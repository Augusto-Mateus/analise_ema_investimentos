import yfinance as yf

## OBTER DADOS DE TICKER ##


def get_ticker(simbolo_ticker, periodo="5y", intervalo="1d"):
    """
    Obtém o objeto Ticker do yfinance para o símbolo fornecido.

    Args:
        simbolo_ticker (str): Símbolo do ativo (ex: 'AAPL', 'MSFT').
        periodo (str): Período para o qual os dados são obtidos (padrão é '5y' para 5 anos).
        intervalo (str): Intervalo dos dados (padrão é '1d' para diário).
    Returns:
        pd.DataFrame: DataFrame contendo os dados históricos do ativo.
    """

    ticker = yf.Ticker(simbolo_ticker)

    # Coluna renomeada para "Datetime" para evitar conflitos de timeframe
    df = ticker.history(period=periodo, interval=intervalo).reset_index()
    column_old_name = df.columns[0]
    column_new_name = "Datetime"

    df.rename(columns={column_old_name: column_new_name}, inplace=True)

    # Remoção de colunas desnecessárias
    df = df.drop(columns=["Dividends", "Stock Splits", "Capital Gains"])

    return df


## CALCULAR EMAS ##


def adicionar_ema(df, periodos=[20, 50, 100, 200]):
    """
    Cria colunas de EMAs no dataframe para os spans fornecidos.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        periodos (list): Lista de períodos para os quais as EMAs serão calculadas (padrão é [20, 50, 100, 200])
    Returns:
        pd.DataFrame: DataFrame com colunas adicionais para cada EMA calculada.
    """

    df_ema = df.copy()

    # Cria 4 colunas EMA para os spans fornecidos
    for span in periodos:
        df_ema[f"EMA_{span}"] = df["Close"].ewm(span=span, adjust=False).mean()

    return df_ema


## Plotar Gráfico ##


def plotar_EMA(df): ...


## CALCULAR PROGRESSO ##


def adicionar_pctg(df):
    """
    Calcula o progresso do investimento ao longo do tempo.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): Valor inicial do investimento.
    Returns:
    """

    df_progresso = df.copy()

    # Calcula a variação percentual diária
    df_progresso["Pctg_Variação"] = df["Close"].pct_change()

    # Preenche valores NaN com 0 para evitar problemas em cálculos
    df_progresso["Pctg_Variação"] = df_progresso["Pctg_Variação"].fillna(0)

    return df_progresso


## ESTRATÉGIA ##


def aplicar_estrategia(df, investimento):
    """
    Aplica a estratégia de investimento ao DataFrame.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): Valor inicial do investimento.
    Returns:
        pd.DataFrame: DataFrame com a coluna adicional "Investimento_Estrategia" representando o valor do investimento ao longo do tempo com a aplicação da estratégia com o EMA.
    """

    df_estrategia = df.copy()

    # Inicializa a coluna de investimento com o valor inicial
    df_estrategia["Investimento_Estrategia"] = investimento

    # Aplica a estratégia de investimento com base nas EMAs (colunas: 6, 7, 8 e 9)
    for i in range(1, len(df_estrategia)):
        if (
            df_estrategia.iloc[i, 6]
            > df_estrategia.iloc[i, 7]
            > df_estrategia.iloc[i, 8]
            > df_estrategia.iloc[i, 9]
        ):
            # Aplica variação percentual ao investimento anterior
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"]
                * (1 + df_estrategia.loc[i, "Pctg_Variação"]),
                2,
            )

        elif (
            df_estrategia.iloc[i, 6]
            < df_estrategia.iloc[i, 7]
            < df_estrategia.iloc[i, 8]
            < df_estrategia.iloc[i, 9]
        ):
            # Interrompe o investimento, mantendo o valor anterior
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"], 2
            )

        else:
            # Aplica variação percentual ao investimento anterior
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"]
                * (1 + df_estrategia.loc[i, "Pctg_Variação"]),
                2,
            )

    return df_estrategia


"""
TODO:
[X] adicionar ajuste ao nome das colunas para evitar conflitos de timeframes
[X] ajustar o uso do EMA e suas colunas nos DF's para evitar reescrever código
[X] remover colunas desnecessárias: Dividends, Stock Splits, Capital Gains
[X] remover funções redundantes
[X] ajustar os textos do notebook
[ ] ajustar vizualização dos gráficos para apresentar a variação percentual do investimento ao invés do valor absoluto
[ ] criar função para plotar gráficos
[ ] adicionar SQQQ ao notebook de avaliação da estratégia
[ ] criar ou adaptar a função de estratégia para contemplar os dois investimentos
"""
