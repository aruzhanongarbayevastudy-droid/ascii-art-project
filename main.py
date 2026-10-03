import sys # чтобы работать с командой, которую мы вводим в терминале
import shutil # для ширины терминала

# 1 потому что main.py - 0
arguments = sys.argv[1:] 

allowed_banners = ["standard", "shadow", "thinkertoy"] # тип текста
allowed_alignments = ["left", "right", "center"] # выравнивание

colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

color = None
colored_letters = None
output_file = None
align = None


# параметры программы
while arguments and arguments[0].startswith("--"):

    option = arguments.pop(0)

    if option.startswith("--color="):
        color = option.split("=", 1)[1]

        if color not in colors:
            print("Unknown color")
            sys.exit()

    elif option.startswith("--output="):
        output_file = option.split("=", 1)[1]

    elif option.startswith("--align="):
        align = option.split("=", 1)[1]

        if align not in allowed_alignments:
            print("Available alignments: left, right, center")
            sys.exit()

    else:
        print("Unknown option:", option)
        sys.exit()


# проверяем наличие текста
if len(arguments) < 1 or len(arguments) > 3:
    print("Usage: py main.py [OPTION] [STRING] [BANNER]")
    sys.exit()


# если после цвета указаны буквы, красим только их
if color is not None and len(arguments) >= 2:
    if arguments[1] not in allowed_banners:
        colored_letters = arguments.pop(0)


text = arguments[0]

# шрифт
banner = arguments[1] if len(arguments) >= 2 else "standard"

if banner not in allowed_banners:
    print("Available banners: standard, shadow, thinkertoy")
    sys.exit()


# перенос строки
text = text.replace("\\n", "\n")


# файл шрифта
with open(banner + ".txt", "r", encoding="utf-8") as file:
    lines = file.read().splitlines()


height = 8
result_lines = []


# ASCII-art
for text_line in text.split("\n"):

    if text_line == "":
        result_lines.append("")
        continue

    for row in range(height):
        result = ""

        for character in text_line:
            start = (ord(character) - 32) * 9 + 1
            piece = lines[start + row]

            # Красим весь текст или выбранные буквы
            if color is not None:
                if colored_letters is None or character in colored_letters:
                    piece = colors[color] + piece + "\033[0m"

            result += piece

        result_lines.append(result)


# выравнивание
if align is not None:
    terminal_width = shutil.get_terminal_size().columns
    aligned_lines = []

    for line in result_lines:

        if align == "left":
            aligned_line = line

        elif align == "right":
            spaces = terminal_width - len(line)
            aligned_line = " " * max(spaces, 0) + line

        else:  # center
            spaces = (terminal_width - len(line)) // 2
            aligned_line = " " * max(spaces, 0) + line

        aligned_lines.append(aligned_line)

    result_lines = aligned_lines


final_result = "\n".join(result_lines)


# сохраняем в файл/выводим в терминал
if output_file is not None:
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(final_result)
else:
    print(final_result)