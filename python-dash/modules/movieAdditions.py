
import pandas as pd
import calendar

class movieAdditions:
    def __init__(self, netflix_df):
        """
        Inicializa a classe movieAdditions com um DataFrame contendo informações de filmes do Netflix.
        
        Args:
            netflix_df (pandas.DataFrame): DataFrame contendo informações dos filmes no Netflix.
        """
        self.netflix_df = netflix_df
    
    def mostCommonMonth(self):
        """
        Calcula o mês com mais adições de filmes no Netflix.
        
        Returns:
            str: O nome do mês com mais adições de filmes.
        """
        netflix_films = self.netflix_df.loc[self.netflix_df['type'] == 'Movie']
        netflix_films['date_added'] = pd.to_datetime(netflix_films['date_added'], errors='coerce')
        netflix_films_monthly_counts = netflix_films['date_added'].dt.month.value_counts()
        most_common_month = calendar.month_name[netflix_films_monthly_counts.idxmax()]
        return most_common_month

    def getMonthlyAdditions(self):
        """
        Calcula a contagem mensal de adições de filmes no Netflix.
        
        Returns:
            pandas.Series: Uma série contendo a contagem mensal de adições de filmes.
        """
        netflix_films = self.netflix_df.loc[self.netflix_df['type'] == 'Movie']
        netflix_films['date_added'] = pd.to_datetime(netflix_films['date_added'], errors='coerce')
        netflix_films_monthly_counts = netflix_films['date_added'].dt.month.value_counts()
        return netflix_films_monthly_counts.reindex(range(1, 13), fill_value=0)