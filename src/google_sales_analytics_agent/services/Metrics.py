import logging
import pandas as pd

class Metrics:

    def __init__(
        self,
        df: pd.DataFrame
    ) -> None:

        self.logger = logging.getLogger(
            __name__
        )

        self.df = df.copy()

    def total_invoicing(
        self
    ) -> float:

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

    def total_cost(
        self
    ) -> float:

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

    def total_profit(
        self
    ) -> float:

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

    def percentage_margin(
        self
    ) -> float:

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

    def sales_month(
        self
    ) -> pd.DataFrame:

        try:

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

    def top_sellers(
        self,
        n: int = 5
    ) -> pd.DataFrame:

        try:

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