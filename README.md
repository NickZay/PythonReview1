# PythonReview1

Я выбрал тему "Генерация текста".

Ссылка на выбранный мною текст:
https://www.gutenberg.org/files/11/11.txt
Это "Alice in Wonderland".

Примеры генерации текста:

1) Lory, with the King sharply. "Do cats if you did, old 
fellow! Don't let me help of swimming away in hand, it saw 
one, or a wretched height to a.

2) She walked up and any minute, trying to the executioner 
myself, said "What a large she knows it was snorting like 
the muscular strength, which was all quarrel so Alice".

3) The court. All the beginning to herself, you have lived 
on which you indicate that he dipped it saw that, as you to 
herself "Now we needn't be interpreted to".


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

