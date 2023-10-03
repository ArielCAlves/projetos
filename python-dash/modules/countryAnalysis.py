import matplotlib.pyplot as plt

class countryAnalysis:
    def __init__(self, amazon_df, netflix_df):        
        """
        Inicializa a classe StreamingDataAnalyzer com DataFrames das plataformas Amazon e Netflix.
        
        Args:
            amazon_df (pandas.DataFrame): DataFrame contendo informações dos filmes na Amazon.
            netflix_df (pandas.DataFrame): DataFrame contendo informações dos filmes na Netflix.
        """
        self.amazon_df = amazon_df
        self.netflix_df = netflix_df
    
    def topCountriesPlot(self, df, platform, column, n=5):
        """
        Calcula e exibe o top países produtores para uma plataforma específica.
        
        Args:
            df (pandas.DataFrame): DataFrame contendo informações dos filmes de uma plataforma.
            platform (str): Nome da plataforma (por exemplo, 'Amazon', 'Netflix').
            column (str): Nome da coluna contendo informações dos países.
            n (int, optional): Número de principais países a serem exibidos. Padrão é 5.
        """
        country_counts = df[column].str.split(', ').explode().value_counts().head(n)
        plt.figure(figsize=(10, 6))
        country_counts.plot(kind='bar')
        plt.title(f'Frequency of Producing Countries in {platform}')
        plt.xlabel('Country')
        plt.ylabel('Frequency')
        plt.show()


    def topCountries(self, df, plataform, column, n=5):
        """
        Exibe os primeiros 5 registros do DataFrame.
        
        Args:
            df (pandas.DataFrame): DataFrame contendo informações dos filmes de uma plataforma.
            platform (str): Nome da plataforma (por exemplo, 'Amazon', 'Netflix').
            column (str): Nome da coluna contendo informações dos países.
            n (int, optional): Número de principais países a serem exibidos. Padrão é 5.
        """
        country_counts = df[column].str.split(', ').explode().value_counts().head(n)
        # print(f'Top 5 países produtores da: {plataform}')        
        return f'Top {n} countries: {plataform}', country_counts