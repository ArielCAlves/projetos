import matplotlib.pyplot as plt

class catalogAnalysis:
    def __init__(self, amazon_df, netflix_df):
        """
        Inicializa a classe catalogAnalysis com DataFrames das plataformas Amazon e Netflix.
        
        Args:
            amazon_df (pandas.DataFrame): DataFrame contendo informações do catálogo da Amazon.
            netflix_df (pandas.DataFrame): DataFrame contendo informações do catálogo da Netflix.
        """
        self.amazon_df = amazon_df
        self.netflix_df = netflix_df
    
    def calculateFrequency(self, df, platform):
        """
        Calcula a frequência de TV Shows e Movies para uma plataforma específica e cria os gráficos.
        
        Args:
            df (pandas.DataFrame): DataFrame contendo informações do catálogo de uma plataforma.
            platform (str): Nome da plataforma (por exemplo, 'Amazon', 'Netflix').
        """
        type_counts = df['type'].value_counts()
        print(type_counts)
        plt.figure(figsize=(8, 6))
        type_counts.plot(kind='bar')
        plt.title(f"Frequency of content types in {platform}")
        plt.xlabel("Content")
        plt.ylabel("Frequency")
        plt.show()

        
    def calculateFrequencyQuantity(self, df):
            """
            Calcula a frequência de TV Shows e Movies  uma plataforma específica.
            
            Args:
                df (pandas.DataFrame): DataFrame contendo informações do catálogo de uma plataforma.
            """
            type_counts = df['type'].value_counts()
            return type_counts