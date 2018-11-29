# Experimento 4 y 5
En este experimento se uso tf-idf para sacar los vectores que describiran los documentos.

## Experimento 4 

En este experimento se obtienen los vectores de los documentos, cada vector tiene n número de dimensiones, las cuales represantan la importancia de la palabra, cuyo valor viene dado por el conteo de la palabra evaluador por una función sigmoidal, multiplicado por su valor de tf-idf de la palabra máximo en todas las palabras, esto garantiza que el valor estará entre 0 y 1 un que dependerá de la importancia de la palabra con respecto al documento donde es más importante esta palabra, esto se dará uniformemente, por lo que no estará sesgado hacia ningún resultado.

## Experimento 5

Este experimento se hizo vecotorizando de forma tradicional los documentos, asignando directamente el valor tf-idf de la palabra, en la dimensión que lo representa.