# PythonReview1

Я выбрал тему "Генерация текста".

Ссылка на выбранный мною текст:
https://www.gutenberg.org/files/11/11.txt
Это "Alice in Wonderland".

Примеры генерации текста:

1) Very politely: 'Did you can--' 'Swim after thinking 
a soldier on growing, and, just as herself, the way 
I have to begin.' For, you derive from a poor Alice, in.

2) The soldiers shouted Alice. 'Why, Mary Ann, and then 
silence, and she had peeped over me see--how IS a candle'. 
I know! The King was going up into the arch.

3) And then she spoke, but tea. 'I kept from the Project 
Gutenberg-tm electronic works provided you to do,' Alice 
kept shifting from one of Mercia and rightly too, that it.

Пример команды для запуска программы в режиме подсчета:
python3 main.py calculate --input_file <path_1> 
--probabilities_file <path_2> --depth <depth>

Пример команды для запуска программы в режиме генерации:
python3 main.py calculate --output_file <path_1> 
--probabilities_file <path_2> --depth <depth> --count <count>

(Если глубина больше, чем было подсчитано раньше,
бросается исключение IndexError)

usage: main.py [-h] [-i INPUT_FILE] [-p PROBABILITIES_FILE] 
[-d DEPTH] [-c COUNT] [-o OUTPUT_FILE] mode

positional arguments:
  mode                  calculate or generate

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE file to calculate from
  -p PROBABILITIES_FILE, --probabilities_file | file to write to
  -d DEPTH, --depth DEPTH depth of calculation
  -c COUNT, --count COUNT number of words to generate
  -o OUTPUT_FILE, --output_file OUTPUT_FILE file to generate to

