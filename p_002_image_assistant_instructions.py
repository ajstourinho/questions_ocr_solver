assistant_instructions = """
Receba como input um arquivo de uma imagem, que consiste numa questão.
Tal questão contém figuras embutidas.
Gere como output um JSON contendo o seguinte:
- um campo de largura em pixels da imagem input, do tipo int;
- um campo de altura em pixels da imagem input, do tipo int;
- um campo de figuras, cujo valor é um Array listando, para cada figura, os quatro pontos (X,Y) do arquivo que descrevem os cantos da figura.

Não gere mais nenhum texto.
Um exemplo de output está a seguir:
```
{
altura: 1250,
largura: 900
figuras: [[(0,0), (0,100), (100, 100), (100, 0)]]
}
```
"""