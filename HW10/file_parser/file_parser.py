import json
import sqlite3
from pydoc import text
import os, csv, re
from classes.classes import News, Private, Funny
from pathlib import Path
import xml.etree.ElementTree as ET


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
    def process_json():

        file_path = input("Enter JSON file path or press Enter for default: ")

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
                DatabaseProcessor.save_news(new)

                i += 3

            elif record_type == "2":

                text = FileParse.normalize(lines[i+1])
                date = lines[i+2]

                private = Private(date, "Private Ad", text)

                with open(FileParse.board_path, "a", encoding="utf-8") as f:
                    f.write(private.publish_datatype())
                    f.write(private.publish_something())
                    f.write(private.count_exp())
                DatabaseProcessor.save_private_ad(private)

                i += 3

            elif record_type == "3":

                text = FileParse.normalize(lines[i+1])

                funny = Funny(text, "Entertainment")
                lucky_day_str = funny.random_lucky_day()

                with open(FileParse.board_path, "a", encoding="utf-8") as f:
                    f.write(funny.publish_datatype())
                    f.write(funny.publish_something())
                    f.write(lucky_day_str)
                DatabaseProcessor.save_funny(funny, lucky_day_str.strip().split(": ")[-1])

                i += 2

        print("\n--Result--\n")

        with open(FileParse.board_path, "r", encoding="utf-8") as f:
            print(f.read())

        os.remove(file_path)


class JsonProcessor:
    announcement_path = Path(__file__).parent.parent / "data" / "announcements.json"
    board_path = Path(__file__).parent.parent / "data" / "board.txt"

    @staticmethod
    def normalize_json(text):
        return TextNormalization(text).fix_misspelling()

    @staticmethod
    def process_json():

        file_path = input("Enter JSON file path or press Enter for default: ")

        if file_path == "":
            file_path = JsonProcessor.announcement_path
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for record in data:
            record_type = record.get("type")
            title = JsonProcessor.normalize_json(record.get("title"))

            if record_type == "1":

                new = News(record.get("location"), "News", title)

                with open(JsonProcessor.board_path, "a", encoding="utf-8") as f:
                    f.write(new.publish_datatype())
                    f.write(new.publish_something())
                    f.write(new.publish_city())
                DatabaseProcessor.save_news(new)

            elif record_type == "2":
                private = Private(record.get("date"), "Private Ad", title)

                with open(JsonProcessor.board_path, "a", encoding="utf-8") as f:
                    f.write(private.publish_datatype())
                    f.write(private.publish_something())
                    f.write(private.count_exp())
                DatabaseProcessor.save_private_ad(private)

            elif record_type == "3":
                funny = Funny(title, "Entertainment")
                lucky_day_str = funny.random_lucky_day()

                with open(JsonProcessor.board_path, "a", encoding="utf-8") as f:
                    f.write(funny.publish_datatype())
                    f.write(funny.publish_something())
                    f.write(lucky_day_str)
                DatabaseProcessor.save_funny(funny, lucky_day_str.strip().split(": ")[-1])
            
        with open(JsonProcessor.board_path, "r", encoding="utf-8") as f:
                print(f.read())

        os.remove(file_path)

class DatabaseProcessor:
    """Saves News, Private Ad and Funny records to an SQLite database.
    Each record type is stored in its own table.
    Duplicate records]are skipped.
    """

    db_path = Path(__file__).parent.parent / "data" / "announcements.db"

    @classmethod
    def _get_connection(cls):
        return sqlite3.connect(cls.db_path)

    @classmethod
    def initialize_db(cls):
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    text         TEXT    NOT NULL,
                    city         TEXT    NOT NULL,
                    published_at TEXT    NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS private_ads (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    text         TEXT    NOT NULL,
                    expiry_date  TEXT    NOT NULL,
                    days_left    INTEGER NOT NULL,
                    published_at TEXT    NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funny (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    text         TEXT NOT NULL,
                    lucky_day    TEXT NOT NULL,
                    published_at TEXT NOT NULL
                )
            """)
            conn.commit()

    @classmethod
    def save_news(cls, news_obj):
        import datetime
        cls.initialize_db()
        now = datetime.datetime.now()
        published_at = f"{now.strftime('%x')} {now.strftime('%X')}"

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM news WHERE text = ? AND city = ?",
                (news_obj.text, news_obj.city)
            )
            if cursor.fetchone():
                print(f"[DB] Duplicate News skipped: '{news_obj.text[:60]}'")
                return False
            cursor.execute(
                "INSERT INTO news (text, city, published_at) VALUES (?, ?, ?)",
                (news_obj.text, news_obj.city, published_at)
            )
            conn.commit()
            print(f"[DB] News saved: '{news_obj.text[:60]}'")
            return True

    @classmethod
    def save_private_ad(cls, private_obj):
        import datetime
        cls.initialize_db()
        now_date = datetime.datetime.now().date()
        expiry_date = datetime.datetime.strptime(private_obj.date, "%Y-%m-%d").date()
        days_left = (expiry_date - now_date).days
        published_at = str(now_date)

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM private_ads WHERE text = ? AND expiry_date = ?",
                (private_obj.text, private_obj.date)
            )
            if cursor.fetchone():
                print(f"[DB] Duplicate Private Ad skipped: '{private_obj.text[:60]}'")
                return False
            cursor.execute(
                "INSERT INTO private_ads (text, expiry_date, days_left, published_at)"
                " VALUES (?, ?, ?, ?)",
                (private_obj.text, private_obj.date, days_left, published_at)
            )
            conn.commit()
            print(f"[DB] Private Ad saved: '{private_obj.text[:60]}'")
            return True

    @classmethod
    def save_funny(cls, funny_obj, lucky_day):
        import datetime
        cls.initialize_db()
        published_at = str(datetime.datetime.now().date())

        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM funny WHERE text = ?",
                (funny_obj.text,)
            )
            if cursor.fetchone():
                print(f"[DB] Duplicate Funny skipped: '{funny_obj.text[:60]}'")
                return False
            cursor.execute(
                "INSERT INTO funny (text, lucky_day, published_at) VALUES (?, ?, ?)",
                (funny_obj.text, lucky_day, published_at)
            )
            conn.commit()
            print(f"[DB] Funny saved: '{funny_obj.text[:60]}'")
            return True

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


class XmlProcessor:
    announcement_path = Path(__file__).parent.parent / "data" / "announcements.xml"
    board_path = Path(__file__).parent.parent / "data" / "board.txt"

    @staticmethod
    def normalize_xml(text):
        return TextNormalization(text).fix_misspelling()

    @staticmethod
    def process_xml():

        file_path = input("Enter XML file path or press Enter for default: ")

        if file_path == "":
            file_path = XmlProcessor.announcement_path

        tree = ET.parse(file_path)
        root = tree.getroot()

        with open(XmlProcessor.board_path, "a", encoding="utf-8") as f:

            for record in root.findall("type"):
                record_type = record.get("name")

                title = record.findtext("title", default="")
                title = XmlProcessor.normalize_xml(title)

                if record_type == "1":
                    location = record.findtext("location", default="")

                    new = News(location, "News", title)
                    f.write(new.publish_datatype())
                    f.write(new.publish_something())
                    f.write(new.publish_city())
                    DatabaseProcessor.save_news(new)

                elif record_type == "2":
                    date = record.findtext("date", default="")

                    private = Private(date, "Private Ad", title)
                    f.write(private.publish_datatype())
                    f.write(private.publish_something())
                    f.write(private.count_exp())
                    DatabaseProcessor.save_private_ad(private)

                elif record_type == "3":
                    funny = Funny(title, "Entertainment")
                    lucky_day_str = funny.random_lucky_day()
                    f.write(funny.publish_datatype())
                    f.write(funny.publish_something())
                    f.write(lucky_day_str)
                    DatabaseProcessor.save_funny(funny, lucky_day_str.strip().split(": ")[-1])

        with open(XmlProcessor.board_path, "r", encoding="utf-8") as f:
            print(f.read())

        os.remove(file_path)