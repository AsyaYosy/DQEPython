from file_parser.file_parser import FileParse, CsvProcessor, JsonProcessor

if __name__ == "__main__":
    #FileParse.process_file()
    JsonProcessor.process_json()
    CsvProcessor.csv_word_count()
    CsvProcessor.csv_letter_count()
