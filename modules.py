from pandas import DataFrame, Series
from yfinance import Ticker
import yfinance as yf
import numpy as np

## OBTER DADOS DE TICKER ##


def get_ticker(
    simbolo_ticker: str, periodo: str = "5y", intervalo: str = "1d"
) -> DataFrame:
    """
    Obtém o objeto Ticker do yfinance para o símbolo fornecido.

    Args:
        simbolo_ticker (str): Símbolo do ativo (ex: 'AAPL', 'MSFT').
        periodo (str): Período para o qual os dados são obtidos (padrão é '5y' para 5 anos).
        intervalo (str): Intervalo dos dados (padrão é '1d' para diário).
    Returns:
        pd.DataFrame: DataFrame contendo os dados históricos do ativo.
    """

    ticker: Ticker = yf.Ticker(simbolo_ticker)

    df: DataFrame = ticker.history(
        period=periodo, interval=intervalo
    ).reset_index()

    # Coluna renomeada para "Datetime" para evitar conflitos de timeframe
    nome_original_coluna: str = df.columns[0]
    novo_nome_coluna: str = "Datetime"

    df.rename(columns={nome_original_coluna: novo_nome_coluna}, inplace=True)

    # Remoção de colunas desnecessárias
    df: DataFrame = df.drop(
        columns=["Dividends", "Stock Splits", "Capital Gains"]
    )

    return df


## CALCULAR EMAS ##


def adicionar_cols_ema(
    df: DataFrame, periodos: list[int] = [20, 50, 100, 200]
) -> DataFrame:
    """
    Cria colunas de EMAs no dataframe para os spans fornecidos.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        periodos (list): Lista de períodos para os quais as EMAs serão calculadas (padrão é [20, 50, 100, 200])
    Returns:
        pd.DataFrame: DataFrame com colunas adicionais para cada EMA calculada.
    Nota:
        - Valores ausentes na coluna 'Close' serão ignorados.
        - Spans inválidos (ex.: negativos ou zero) não serão processados.
    """

    df_ema: DataFrame = df.copy()

    # Cria 4 colunas EMA para os spans fornecidos
    for span in periodos:
        df_ema[f"EMA_{span}"] = df["Close"].ewm(span=span, adjust=False).mean()

    return df_ema


## PLOTAR GRÁFICO ##


def plotar_EMA(df: DataFrame) -> None: ...


## CALCULAR RAZÃO ##


def adicionar_col_razao(
    df: DataFrame, col_ref: str, col_result: str
) -> DataFrame:
    """
    Calcula a razão(ratio) do progresso do investimento.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        col_ref (str): String contendo o nome da coluna de referencia do calculo.
        col_result (str): String contendo o nome da coluna resultante do calculo.
    Returns:
        pd.DataFrame: DataFrame com a coluna razão calculada.
    """

    df_razao: DataFrame = df.copy()

    # Calcula a variação percentual diária
    df_razao[col_result] = df[col_ref].pct_change()

    return df_razao


## ESTRATÉGIA ##


def adicionar_col_razao_estrategia(
    df: DataFrame, col_razao: str, col_result: str
) -> DataFrame:
    """
    Determina quando a estrategia está ativa.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        col_ref (str): String contendo o nome da coluna de referencia do calculo.
        col_result (str): String contendo o nome da coluna resultante do calculo.
    Returns:
        pd.DataFrame: DataFrame com a coluna razão para a estratégia.
    """

    df_progresso_estr: DataFrame = df.copy()

    sinal: Series = (
        (
            df_progresso_estr.iloc[:, 6].shift(1)
            <= df_progresso_estr.iloc[:, 7].shift(1)
        )
        & (
            df_progresso_estr.iloc[:, 7].shift(1)
            <= df_progresso_estr.iloc[:, 8].shift(1)
        )
        & (
            df_progresso_estr.iloc[:, 8].shift(1)
            <= df_progresso_estr.iloc[:, 9].shift(1)
        )
    )

    df_progresso_estr[col_result] = np.where(
        sinal, 0.0, df_progresso_estr[col_razao]
    )

    return df_progresso_estr


## PROJEÇÃO INVESTIMENTO ##


def adicionar_col_investimento(
    df: DataFrame, investimento: float, col_ref: str, col_result: str
) -> DataFrame:
    """
    Calcula o progresso do valor absoluto do investimento ao longo do tempo.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados históricos do ativo.
        investimento (float): O valor usado para simular o investimento.
        col_ref (str): String contendo o nome da coluna de referencia do calculo.
        col_result (str): String contendo o nome da coluna resultante do calculo.
    Returns:
        pd.DataFrame: DataFrame com a coluna de investimento calculada.
    """

    df_retorno_estr: DataFrame = df.copy()

    df_retorno_estr[col_result] = round(
        investimento * (1 + df_retorno_estr[col_ref]).cumprod(), 2
    )

    return df_retorno_estr


## PRODUTO CUMULATIVO ##


def produto_cumulativo(x: Series) -> Series:
    """
    Retorna o produto cumulativo da variação percentual de x, para plotagem de graficos.
    Args:
        x (Series): Serie de valores absolutos a serem convertidos em porcentagem cumulativa.
    """

    return ((1 + x).cumprod()) - 1


"""
TODO:
[X] adicionar ajuste ao nome das colunas para evitar conflitos de timeframes
[X] ajustar o uso do EMA e suas colunas nos DF's para evitar reescrever código
[X] remover colunas desnecessárias: Dividends, Stock Splits, Capital Gains
[X] remover funções redundantes
[X] ajustar os textos do notebook
[X] ajustar vizualização dos gráficos para apresentar a variação percentual do investimento ao invés do valor absoluto
[ ] criar função para plotar gráficos
[ ] adicionar SQQQ ao notebook de avaliação da estratégia
[ ] criar ou adaptar a função de estratégia para contemplar os dois investimentos
"""
