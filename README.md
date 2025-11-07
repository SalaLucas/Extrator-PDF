# Problemas Mapeados

Como deixar a requisição de api para a openAI mais rápida
Como diminuir a quantidade de informção que a IA deve processar
Como aprender com as respostas de uma mesma label
Como lidar com informações que podem ser repetidas
Como diminuir a quantidade de chamadas para a IA

# Problemas escolhidos e como tentei resolver

Tentei diminuir a quantdade de informações que a IA deve processar com algumas heuristicas básicas. É possível buscar palavras no texto que já são campos do nosso extraction_schema e buscar em volta desse texto possíveis valores para esse campo já que muitas vezes temos um campo e o seu valor a direita ou a baixo.
Tentei deixar a requisição da API mais rápida fazendo só 1 requisição em vez de várias ou com várias requisições uma para cada campo que ainda não possui resposta. Várias threads pareceu pouco mais eficiente porém com um custo maior.
É possível salvar posição de onde foram tiradas informações anteriormente quando encontradas pela IA e tentar utilizar para ver se elas se encontram no mesmo local.
Informações repetidas eu tentei pegar sempre a primeira informação que encaixava quando encontrada por heuristica e após isso apagar essa parte do texto. Porém existia campos repetidos no exemplo, não consgui pensar em uma solução que contornasse isso apenas com heuristica porém utilizando a IA é possível entender em qual situação temos que pegar qual ocorrencia do campo podendo assim utilizar a huristica após algumas utilizações da IA.
