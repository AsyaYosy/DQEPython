import os
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