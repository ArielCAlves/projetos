
### # Mercado Imobiliario
 - Projeto voltado para analisar dados de imóveis localizados na região de Itapema-SC (maior parte referente ao mês de dezembro/2022).
 - Foram coletados dados do Airbnb e do VivaReal para identificar os perfis que geraram a maior rentabilidade na gestão de alugueis e também para poder prever preços de venda/locação e analisar se é viável investir ou não.
 - Foi um projeto real e por isso deixei o relatório em inglês mesmo para modificar o mínimo possível.
 - Mantive os códigos em Python porque precisei utilizar o VSCode para testar num ambiente virtual e disponibilizar o modelo para um futura integração CI/CD (pode utilizar o Jupyter sem problemas). 
 - Para rodar os scripts precisa instalar as bibliotecas do requirements (depois de clonar o repositório execute no terminal: pip install -r requirements.txt): 

   [Requirements](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/libraries.png)
 
 - Importante: os scripts precisam ser executados na seguinte ordem:
    - scripts/etl.py
    - scripts/ml.py
    - scripts/clustering.py
    - scripts/viva_real_etl.py
    - Link dos scripts: [scripts](https://github.com/ArielCAlves/projetos/tree/main/mercado-imobiliario/scripts)
    
    
 - Datasets: alguns arquivos estavam muito grandes no formato csv e precisei fazer modificações/compactações para poder colocá-los no repositório, escolhi salvar em formato parquet (o código já está adaptado para ler e só precisa instalar o requirements para não ter complicações).
    - exemplo: 
    
    ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/print_dataset.png)
       
  
 - Algumas perguntas de negócios foram feitas para conseguir tirar as minhas conclusões (aliás, segui a metodologia CRISP-DM partindo do problema de negócio para depois ir atrás dos dados):
  1) Qual é o melhor perfil de imóveis para investir?
      - Precisei segmentar os perfis seguindo algumas técnicas de redução de dimensionalidade, clusterização com algoritmo k-means, distância euclidiana e métrica silhouette para testar se a quantidade de clusters (grupos) estava adequada.
      - Exemplo de transformações para chegar ao resultado final:
      
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/cluster.png)
      
      - A partir disso criei uma coluna para identificar a qual cluster pertence cada imóvel disponível no dataset (última coluna; varia de 0 a 3):
      
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/cluster2.png)
      
      
      - Resultado final desse agrupamento (ainda faltam tratamentos para melhorar, mas até o momento foi suficiente para tomar decisões mais assertivas):
      
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/profiles.png)
  
  2) Qual é a melhor localização da cidade pensando na perspectiva de receita?  
      - Além de fazer alguns tratamentos removendo valores extremos (outliers), precisei fazer um feature engineering para calcular o preço do metro quadrado de acordo com características dos imóveis (dentro de determinadas categorias me baseando em conceitos de centroides), entre outros tratamentos verificando mais detalhes sobre localização com a API do viacep.
    
      - Exemplo de um dos gráficos gerados durante a exploração:    
    
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/viva_real.png)    
    
  

  3) Quais são as características e principais fatores que ocasionaram essa melhor receita?
      - Utilizei 3 algoritmos de Regressão para estimar os preços e comparei a performance deles com o R² (coeficiente de determinação) e RMSE (raiz quadrada do erro médio). Idenfique um alto overfitting nos resultados e precisei fazer diversas modificações envolvendo um aumento da aleatoriedade da amostra selecionada (amostra representativa que fosse suficiente para avaliar um bom modelo sem estourar memória do pc).
      - Resultado final dos modelos (sem modificar muitos hiperparâmetros):
      
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/without_overfitting.png)
      
      - Modelo Treinado para disponibilizar em forma de API: [ModeloTreinado](https://github.com/ArielCAlves/projetos/tree/main/mercado-imobiliario/model)
      
      - Para identificar as principais variáveis responsáveis por essa estimativa de preços utilizei o feature importances, conforme gráfico abaixo:
      ![link](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/images/ml_feature_importance.png)
      
      
      - É importante sempre desconfiar de alguns resultados e retreinar o modelo mais vezes modificando a seleção de variáveis entre outras modificações, no entanto, se fosse investir em alguma reforma desses imóveis daria mais ênfase aos cômodos que estão relacionados ao top 5, por exemplo.
      
      
  
  - Para ter acesso ao relatório "final" pode acessar [report](https://github.com/ArielCAlves/projetos/blob/main/mercado-imobiliario/report.pdf)