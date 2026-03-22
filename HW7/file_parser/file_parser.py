import os, csv, re
from classes.classes import News, Private, Funny
from pathlib import Path


class TextNormalization:

    def __init__(self, text):
        self.text = text

    def normalize_case(self):
        text = self.text.lower()
        sentences = text.replace("\n", " ").split(".")
        sentences = [s.strip().capitalize() for s in sentences if s.strip()]

        normalized_text = ". ".join(sentences) + "."
        return normalized_text, sentences

    def fix_misspelling(self):
        normalized_text, sentences = self.normalize_case()

        fixed_sentences = []
        for sentence in sentences:
            words = sentence.split()
            words = ["is" if w.lower() == "iz" else w for w in words]
            fixed_sentences.append(" ".join(words))

        fixed_text = ". ".join(fixed_sentences) + "."
        return fixed_text


class FileParse:
    announcement_path = Path(__file__).parent.parent / "data" / "announcements.txt"
    board_path = Path(__file__).parent.parent / "data" / "board.txt"

    @staticmethod
    def normalize(text):
        return TextNormalization(text).fix_misspelling()

    @staticmethod
    def process_file():

        file_path = input("Enter file path or press Enter for default: ")

        if file_path == "":
            file_path = FileParse.announcement_path

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        i = 0

        while i < len(lines):

            record_type = lines[i]

            if record_type == "1":

                text = FileParse.normalize(lines[i+1])
                city = lines[i+2]

                new = News(city, "News", text)

                with open(FileParse.board_path, "a", encoding="utf-8") as f:
                    f.write(new.publish_datatype())
                    f.write(new.publish_something())
                    f.write(new.publish_city())

                i += 3

            elif record_type == "2":

                text = FileParse.normalize(lines[i+1])
                date = lines[i+2]

                private = Private(date, "Private Ad", text)

                with open(FileParse.board_path, "a", encoding="utf-8") as f:
                    f.write(private.publish_datatype())
                    f.write(private.publish_something())
                    f.write(private.count_exp())

                i += 3

            elif record_type == "3":

                text = FileParse.normalize(lines[i+1])

                funny = Funny(text, "Entertainment")

                with open(FileParse.board_path, "a", encoding="utf-8") as f:
                    f.write(funny.publish_datatype())
                    f.write(funny.publish_something())
                    f.write(funny.random_lucky_day())

                i += 2

        print("\n--Result--\n")

        with open(FileParse.board_path, "r", encoding="utf-8") as f:
            print(f.read())

        os.remove(file_path)

class CsvProcessor:
    @staticmethod
    def word_count():
        board_path = Path(__file__).parent.parent / "data" / "board.txt"
        
        with open(board_path, "r", encoding="utf-8") as f:
            text = f.read().lower()

        words = re.findall(r"[a-zA-Z]+", text)

        dict_word_count = {}

        for word in words:
            if word in dict_word_count:
                dict_word_count[word] += 1
            else:
                dict_word_count[word] = 1

        return dict_word_count
        
    @staticmethod
    def csv_word_count():
        csv_path = Path(__file__).parent.parent / "csv_proccesed" / "csv_word_count.csv"
        
        count = CsvProcessor.word_count()
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["word", "count"])  
            for word, freq in count.items():
                writer.writerow([word, freq])

    @staticmethod
    def letter_count():
        board_path = Path(__file__).parent.parent / "data" / "board.txt"

        with open(board_path, "r", encoding="utf-8") as f:
            text = f.read()

        letters = [char for char in text if char.isalpha()]
        total_letters = len(letters)

        dict_letter_count = {}

        for char in letters:
            letter_lower = char.lower()

            if letter_lower not in dict_letter_count:
                dict_letter_count[letter_lower] = [0, 0, 0]

            dict_letter_count[letter_lower][0] += 1

            if char.isupper():
                dict_letter_count[letter_lower][1] += 1

        for letter in dict_letter_count:
            count_all = dict_letter_count[letter][0]
            percentage = (count_all / total_letters) * 100
            dict_letter_count[letter][2] = percentage

        return dict_letter_count

    @staticmethod
    def csv_letter_count():
        csv_path = Path(__file__).parent.parent / "csv_proccesed" / "csv_letter_count.csv"
        letter_count = CsvProcessor.letter_count()

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])  
            for letter, data in letter_count.items():
                writer.writerow([letter, data[0], data[1], f"{data[2]:.2f}%"])




