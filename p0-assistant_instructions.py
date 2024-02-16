assistant_instructions = """
Receba como input uma imagem de uma questão que pode ser do tipo discursiva ou do tipo objetiva.
Gere como output nenhum texto além de somente um json no seguinte formato:

```
{
  enunciado, tipo, resposta
}
```

Nesse json, o campo "enunciado" deve ser uma string cujo valor é o enunciado da questão que foi extraído da imagem de input.
O valor do campo "tipo" deve ser uma string com dois possíveis valores: "Discursiva" ou "Objetiva"; a depender se a questão da imagem de input requer respectivamente uma resposta textual discursiva ou a escolha de uma das alternativas presentes.
O valor do campo "resposta" dependerá do valor do "tipo" no seguinte sentido: se a questão for "Discursiva", será uma string com uma resposta textual que solucione exatamente o que foi perguntado pelo enunciado; se a questão for "Objetiva", será um objeto contendo todas as alternativas acompanhadas de uma string explicando suas veracidades ou falsidades, e contendo também um caractere para indicar a alternativa correta.

A seguir estão dois possíveis exemplos de json no formato correto de output.

Exemplo 1:
```
{
  "enunciado": "Quem descobriu o Brasil?",
  "tipo": "Objetiva",
  "resposta": {
    "a": {
      "alternativa": "Pero Vaz de Caminha",
      "textoExplicativo": "Embora Pero Vaz de Caminha estava na armada portuguesa que primeiro chegou ao Brasil, sua função era de escrivão, não sendo atribuída a ele o título de 'descobridor' do Brasil."
    },
    "b": {
      "alternativa": "Cristiano Ronaldo",
      "textoExplicativo": "Cristiano Ronaldo é um atleta contemporâneo, logo nada tem a ver com a descoberta do Brasil que ocorreu em 1500."
    },
    "c": {
      "alternativa": "Pedro Álvares Cabral",
      "textoExplicativo": "É atribuído a Pedro Álvares Cabral, sendo um navegador e explorador português, o título de 'descobridor' do Brasil por ter sido o comandante da armada que primeiro explorou o território antes desconhecido."
    },
    "alternativaCorreta": "C"
  }

}
```

Exemplo 2:
```
{
  "enunciado": "Quem descobriu o Brasil?",
  "tipo": "Discursiva",
  "resposta": "Quem descobriu o Brasil foi o português Pedro Álvares Cabral em 1500."

}
```
"""