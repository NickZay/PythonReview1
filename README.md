# PythonReview1

Я выбрал тему "Генерация текста".

Ссылка на выбранныЕ мною текстЫ:
https://royallib.com/book/London_Jack/White_Fang.html
https://www.gutenberg.org/files/11/11.txt
Это "London Jack - White Fang" и "Alice in Wonderland".

Примеры генерации текста:

1) Work and a tidy little creature when she had been, it 
uneasily, shaking among the copyright notice this time. 
“I don’t think, Alice as hard as it to comply with.”

2) A timid and finish your Majesty, he said Alice. “That’s 
nothing but it to whisper a shrill, passionate voice.” 
“Now, I should like the individual work can reach it: there.”


3) The sands are accepted in their simple rules in a 
complaining tone, going to guard him; and very much under 
the end. “If you take this pool?” I meant, the.



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

