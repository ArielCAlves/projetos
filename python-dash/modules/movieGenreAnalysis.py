from nltk.stem import PorterStemmer
import pandas as pd

class movieGenreAnalysis:
    def __init__(self, df):
        """
        Inicializa a classe movieGenreAnalysis com um DataFrame contendo informações de filmes.
        
        Args:
            df (pandas.DataFrame): DataFrame contendo informações dos filmes.
        """
        self.df = df
        self.stemmer = PorterStemmer()
    
    def stem_word(self, word):
        """
        Realiza stemming em uma palavra usando o PorterStemmer.
        
        Args:
            word (str): Palavra a ser stemmizada.
        
        Returns:
            str: Radical da palavra stemmizada.
        """
        return self.stemmer.stem(word)
    
    def countComedyMovies(self):
        """
        Calcula a quantidade de filmes listados como comédia.
        
        Returns:
            int: A quantidade de filmes listados como comédia.
        """
        movies_df = self.df[self.df['type'] == 'Movie']
        comedy_count = 0
        
        for listed_in in movies_df['listed_in']:
            genres = listed_in.split(', ')
            stemmed_genres = [self.stem_word(genre) for genre in genres]
            if 'comedi' in stemmed_genres:
                comedy_count += 1
        
        return comedy_count
        
    def allGenres(self):
        """
        Lista todos os gêneros de filmes.
        """
        movies_df = self.df[self.df['type'] == 'Movie']
        all_genres = movies_df['listed_in'].str.split(', ').explode().unique()
        stemmed_genres = [self.stem_word(genre).title() for genre in all_genres]
        
        print('Todos os gêneros:\n')
        unique = []    
        for genre in stemmed_genres:
            if genre not in unique:
                unique.append(genre)
        for item in unique:
            print(item)

    def allGenresQuantity(self):
        """
        Lista todos os gêneros de filmes com suas contagens, formatados em título.
        
        Returns:
            pandas.Series: Contagem de gêneros de filmes em formato Series.
        """
        movies_df = self.df[self.df['type'] == 'Movie']
        all_genres = movies_df['listed_in'].str.split(', ').explode()

        genre_stems = all_genres.apply(self.stem_word)
        formatted_genre_stems = [genre.title() for genre in genre_stems]
        genre_series = pd.Series(formatted_genre_stems)
        genre_counts = genre_series.value_counts()
        return genre_counts
