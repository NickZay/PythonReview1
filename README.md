# PythonReview1

Я выбрал тему "Генерация текста".

Ссылка на выбранный мною текст:
https://www.gutenberg.org/files/11/11-h/11-h.htm
Это "Alice in Wonderland".

Примеры генерации текста:

Текст курильщика:
it’s no pleasing them!” “I don’t like the Mock Turtle sighed deeply, and got to?” (Alice began thinking while the United States with all the Englis
h coast you usually see it may demand a steam-engine when the table, with you,” (she was quite silent for it, even spoke to her. “Poor little creat
ure, but now had not solicit donations are tarts on again:— “You are you?” “Not quite understand English,” thought Alice; “I must be off, and the G
ryphon, and tremulous sound.] “That’s right, so suddenly: you what to have made another snatch in an end? “I won’t indeed!” said

Текст здорового человека:
It’s no pleasing them! “I don’t like the Mock Turtle sighed deeply, and got to?” (Alice began thinking while the United States with all the English
 coast you usually see it may demand a steam-engine when the table, with you, (she was quite silent for it, even spoke to her.)) “Poor little creat
ure, but now had not solicit donations are tarts on again:- “You are you?”” “Not quite understand English,” thought Alice; “I must be off, and the
Gryphon, and tremulous sound.” “That’s right, so suddenly: you what to have made another snatch in an end?” “I won’t indeed!” said.




Пример команды для запуска программы в режиме подсчета:
python3 main.py calculate --input_file <path_1> 
--probabilities_file <path_2> --depth <depth>

Пример команды для запуска программы в режиме генерации:
python3 main.py calculate --output_file <path_1> 
--probabilities_file <path_2> --depth <depth> --count <count_of_words> --verbosity <0 or 1>



usage: main.py [-h] {calculate,generate} ...

Program which can make text itself

positional arguments:
  {calculate,generate}
    calculate           calculate probabilities
    generate            generate text from database

optional arguments:
  -h, --help            show this help message and exit



usage: main.py calculate [-h] [-i INPUT_FILE] [-p PROBABILITIES_FILE] [-d DEPTH]

optional arguments:
  -h, 			--help						show this help message and exit
  -i INPUT_FILE, 	--input_file INPUT_FILE				file to calculate from
  -p PROBABILITIES_FILE,--probabilities_file PROBABILITIES_FILE		file to write to
  -d DEPTH, 		--depth DEPTH					depth of calculation


usage: main.py generate [-h] [-p PROBABILITIES_FILE] [-o OUTPUT_FILE] [-d DEPTH] [-c COUNT] [-v VERBOSITY]

optional arguments:
  -h, 			--help       					show this help message and exit
  -p PROBABILITIES_FILE, --probabilities_file PROBABILITIES_FILE	file to learn info from
  -o OUTPUT_FILE, 	--output_file OUTPUT_FILE			file to generate to
  -d DEPTH, 		--depth DEPTH					depth of finding words
  -c COUNT, 		--count COUNT					number of words to generate
  -v VERBOSITY, 	--verbosity VERBOSITY				0 is just text, and 1 is with original
	



