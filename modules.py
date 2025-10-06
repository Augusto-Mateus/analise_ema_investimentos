import pandas as pd
import yfinance as yf

#####################################################################################
############################### OBTER DADOS #########################################
#####################################################################################


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
    return ticker.history(period=periodo, interval=intervalo).reset_index()


#####################################################################################
############################### CALCULAR EMAS #######################################
#####################################################################################


def adicionar_ema(df, spans=[20, 50, 100, 200]):
    """
    Cria colunas de EMAs no dataframe para os spans fornecidos.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        spans (list): Lista de períodos para os quais as EMAs serão calculadas.(padrão é [20, 50, 100, 200])
    Returns:
        pd.DataFrame: DataFrame com colunas adicionais para cada EMA calculada.
    """

    df_ema = df.copy()

    for span in spans:
        df_ema[f"EMA_{span}"] = df["Close"].ewm(span=span, adjust=False).mean()

    return df_ema


#####################################################################################
############################### CALCULAR PROGRESSO ##################################
#####################################################################################


def adicionar_pctg(df):
    """
    Calcula o progresso do investimento ao longo do tempo.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): Valor inicial do investimento.
    Returns:
    """

    df_progresso = df.copy()
    df_progresso["Pctg_Variação"] = df["Close"].pct_change()

    df_progresso["Pctg_Variação"] = df_progresso["Pctg_Variação"].fillna(0)

    return df_progresso


#####################################################################################
############################### CALCULAR INVESTIMENTO ###############################
#####################################################################################


def calc_investimento(df, investimento):
    """
    Calcula o valor do investimento ao longo do tempo.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): Valor inicial do investimento.
    Returns:
        pd.DataFrame: DataFrame com a coluna adicional "Valor_Investimento" representando o valor do investimento sem a aplicação da estratégia com o EMA.
    """

    df_investimento = df.copy()

    df_investimento["Valor_Investimento"] = round(
        investimento * (1 + df["Pctg_Variação"]).cumprod(), 2
    )

    return df_investimento


#####################################################################################
#################################### ESTRATÉGIA #####################################
#####################################################################################


def aplicar_estrategia(df, investimento, reverso=False):
    """
    Aplica a estratégia de investimento ao DataFrame.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): Valor inicial do investimento.
    Returns:
        pd.DataFrame: DataFrame com a coluna adicional "Investimento_Estrategia" representando o valor do investimento ao longo do tempo com a aplicação da estratégia com o EMA.
    """

    df_estrategia = df.copy()

    df_estrategia["Investimento_Estrategia"] = investimento

    for i in range(1, len(df_estrategia)):
        if (
            df_estrategia.loc[i, "EMA_20"]
            > df_estrategia.loc[i, "EMA_50"]
            > df_estrategia.loc[i, "EMA_100"]
            > df_estrategia.loc[i, "EMA_200"]
        ):
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"]
                * (1 + df_estrategia.loc[i, "Pctg_Variação"]),
                2,
            )

        elif (
            df_estrategia.loc[i, "EMA_20"]
            < df_estrategia.loc[i, "EMA_50"]
            < df_estrategia.loc[i, "EMA_100"]
            < df_estrategia.loc[i, "EMA_200"]
        ):
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"], 2
            )

        else:
            df_estrategia.loc[i, "Investimento_Estrategia"] = round(
                df_estrategia.loc[i - 1, "Investimento_Estrategia"]
                * (1 + df_estrategia.loc[i, "Pctg_Variação"]),
                2,
            )

    return df_estrategia
