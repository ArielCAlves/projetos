import matplotlib.pyplot as plt

class actorAnalysis:
    def __init__(self, df):

        """
        Inicializa a classe actorAnalysis com um DataFrame contendo informações de filmes.
        
        Args:
            df (pandas.DataFrame): O DataFrame contendo os dados dos filmes.
        """

        self.df = df
    
    def topActors(self, column_name, n=10):
        """
        Calcula os principais valores dessa coluna.
        
        Args:
            column_name (str): O nome da coluna para análise.
            n (int, optional): O número de principais valores a serem calculados. Padrão é 10.
            
        Returns:
            pandas.Series: Uma série contendo os principais valores da coluna.
        """
        top_values = self.df[column_name].str.split(', ').explode().value_counts().head(n)
        return top_values
    
    def plotBar(self, data, title, xlabel, ylabel):
        """
        Cria um gráfico de barras a partir dos dados fornecidos.
        
        Args:
            data (pandas.Series): Os dados para criar o gráfico.
            title (str): O título do gráfico.
            xlabel (str): Rótulo do eixo x.
            ylabel (str): Rótulo do eixo y.
        """               
        plt.figure(figsize=(10, 6))
        data.plot(kind='bar')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()