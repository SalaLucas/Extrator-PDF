# Problemas Mapeados

- Como deixar a requisição de API para a OpenAI mais rápida.  
- Como diminuir a quantidade de informação que a IA deve processar.  
- Como aprender com as respostas de uma mesma *label*.  
- Como lidar com informações que podem ser repetidas.  
- Como diminuir a quantidade de chamadas para a IA.  

---

# Problemas Escolhidos e Soluções Propostas

Tentei diminuir a quantidade de informações que a IA precisa processar utilizando algumas heurísticas básicas. É possível buscar palavras no texto que já são campos do nosso *extraction_schema* e procurar, em volta desse texto, possíveis valores para esses campos — já que, muitas vezes, temos um campo e o seu valor logo à direita ou abaixo.

Busquei deixar a requisição para a API mais rápida fazendo apenas **uma chamada** em vez de várias, ou então executando **várias requisições em paralelo**, uma para cada campo sem resposta. A abordagem com múltiplas *threads* se mostrou um pouco mais eficiente, porém com um custo maior.

Também é possível salvar as posições de onde as informações foram extraídas anteriormente pela IA e tentar reutilizá-las, verificando se continuam no mesmo local em outros documentos com a mesma *label*.

Para lidar com informações repetidas, tentei sempre pegar a **primeira ocorrência** encontrada pela heurística e, depois, apagar essa parte do texto para evitar duplicações. No entanto, alguns campos realmente se repetiam no exemplo. Não consegui pensar em uma solução puramente heurística para isso, mas, utilizando a IA, é possível compreender em quais situações devemos pegar cada ocorrência do campo. Assim, a heurística pode se tornar mais precisa após algumas execuções assistidas pela IA.

---

# Observação

A data coincidiu com a final da maratona de programação, então não tive muito tempo disponível. Ainda assim, o teste foi bem interessante e me fez pensar em várias ideias legais. Obrigado pela oportunidade!

---

# Como Utilizar a Solução

Para rodar a solução, é necessário ter o **Python 3** (testado apenas na versão **3.12.3**).

1. Instale as dependências executando:

   ```bash
   pip install -r requirements.txt
   ```
2. Rode o programa com Python 3, passando o parâmetro --dataset com o caminho para o dataset que será utilizado na aplicação.

É importante que o caminho para o PDF esteja correto dentro do arquivo de dataset.
```bash
  python main.py --dataset caminho/para/dataset.json
```
