import logging
import pandas as pd

class Metrics:
    """
    Classe responsável pelo cálculo de métricas
    analíticas relacionadas às vendas.

    Parameters
    ----------
    df : pd.DataFrame
        Base de vendas padronizada contendo
        informações comerciais.
    """

    def __init__(self, df: pd.DataFrame) -> None:

        self.logger = logging.getLogger(
            __name__
        )

        self.df = df.copy()

    def total_invoicing(self) -> float:
        """
        Calcula faturamento total.

        Returns
        -------
        float
            Soma total do faturamento.
        """
        try:
            self.logger.info(
                "Calculando faturamento."
            )

            return float(
                (
                    self.df["quantidade_vendida"]
                    *
                    self.df["valor_venda"]
                ).sum()
            )

        except Exception:
            self.logger.exception(
                "Erro ao calcular faturamento."
            )

            raise

    def total_cost(self) -> float:
        """
        Calcula custo agregado.

        Returns
        -------
        float
            Soma total dos custos.
        """
        try:
            self.logger.info(
                "Calculando custo."
            )

            return float(
                (
                    self.df["quantidade_vendida"]
                    *
                    self.df["valor_compra"]
                ).sum()
            )

        except Exception:
            self.logger.exception(
                "Erro ao calcular custo."
            )

            raise

    def total_profit(self) -> float:
        """
        Calcula lucro bruto.

        Returns
        -------
        float
            Diferença entre faturamento
            e custo.
        """
        try:

            self.logger.info(
                "Calculando lucro."
            )

            return (
                (self.df["quantidade_vendida"]
                * 
                self.df["valor_venda"])
                -
                (self.df["quantidade_vendida"]
                * 
                self.df["valor_compra"])
            ).sum()

        except Exception:
            self.logger.exception(
                "Erro ao calcular lucro."
            )

            raise

    def percentage_margin(self) -> float:
        """
        Calcula lucro bruto.

        Returns
        -------
        float
            Diferença entre faturamento
            e custo.
        """
        try:
            self.logger.info(
                "Calculando margem percentual."
            )
            faturamento = (
                float(
                    (
                    self.df["quantidade_vendida"]
                    *
                    self.df["valor_venda"]
                    ).sum()
                )   
            )
            
            lucro_total = (
                (self.df["quantidade_vendida"]
                * 
                self.df["valor_venda"]
                )
                -
                (self.df["quantidade_vendida"]
                * 
                self.df["valor_compra"]
            )
            ).sum()

            if faturamento == 0:

                raise ZeroDivisionError(
                    "Faturamento zero."
                )

            return (lucro_total / faturamento) * 100

        except Exception:
            self.logger.exception(
                "Erro ao calcular margem."
            )

            raise

    def sales_month(self) -> pd.DataFrame:
        """
        Consolida faturamento mensal.

        Returns
        -------
        pd.DataFrame
            Série temporal mensal.
        """
        try:
            self.logger.info(
                "Calculando margem faturamento mensal."
            )

            base = self.df.copy()

            # Cria coluna temporal
            # agregadora.
            base["mes"] = (
                pd.to_datetime(
                    base["data_venda"]
                )
                .dt.to_period("M")
            )

            base["faturamento"] = (
                base["quantidade_vendida"]
                *
                base["valor_venda"]
            )

            return (
                base
                .groupby("mes")
                ["faturamento"]
                .sum()
                .reset_index()
            )

        except Exception:
            self.logger.exception(
                "Erro em vendas mensais."
            )

            raise

    def top_sellers(self, n: int = 5) -> pd.DataFrame:
        """
        Retorna ranking de vendedores.

        Parameters
        ----------
        n : int
            Quantidade de posições.

        Returns
        -------
        pd.DataFrame
            Ranking de vendedores.
        """
        try:
            self.logger.info(
                "Calculando margem ranking de vendedores."
            )

            base = self.df.copy()

            base["faturamento"] = (
                base["quantidade_vendida"]
                *
                base["valor_venda"]
            )

            return (
                base
                .groupby("vendedor")
                ["faturamento"]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(n)
                .reset_index()
            )

        except Exception:
            self.logger.exception(
                "Erro no ranking."
            )

            raise

    def top_products(self, n: int = 10) -> pd.DataFrame:
        """
        Retorna ranking dos produtos
        com melhor desempenho financeiro.

        Parameters
        ----------
        n : int, default=10
            Quantidade de produtos
            retornados.

        Returns
        -------
        pd.DataFrame
            Ranking consolidado
            por produto.

        Raises
        ------
        Exception
            Quando ocorre erro
            durante cálculo.
        """

        try:

            self.logger.info(
                "Calculando ranking de produtos."
            )

            # Evita modificar
            # DataFrame original.
            base = self.df.copy()

            # Calcula métricas
            # por registro.
            base["faturamento"] = (
                base["quantidade_vendida"]
                *
                base["valor_venda"]
            )

            base["custo"] = (
                base["quantidade_vendida"]
                *
                base["valor_compra"]
            )

            base["lucro"] = (
                base["faturamento"]
                -
                base["custo"]
            )

            result = (
                base
                .groupby("produto")
                .agg(
                    faturamento=(
                        "faturamento",
                        "sum"
                    ),

                    quantidade_vendida=(
                        "quantidade_vendida",
                        "sum"
                    ),

                    lucro=(
                        "lucro",
                        "sum"
                    )
                )

                .reset_index()
            )

            # Calcula margem
            # percentual.
            result["margem_pct"] = (
                result["lucro"] / result["faturamento"]
            ) * 100

            result = (
                result
                .sort_values(
                    "faturamento",
                    ascending=False
                )
                .head(n)
                .reset_index(
                    drop=True
                )
            )

            self.logger.info(
                f"{len(result)} produtos retornados."
            )

            return result

        except Exception:
            self.logger.exception(
                "Erro ao calcular top produtos."
            )

            raise    