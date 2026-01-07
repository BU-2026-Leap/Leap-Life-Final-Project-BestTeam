from contracts import DataFetcher, ExamScore

import csv

class LocalCSVDataFetcher(DataFetcher):
    def __init__(self, file_path:str):
        self.file_path = file_path

    def fetch(self) -> [ExamScore]:
        scores = []

        # TODO: implement here

        return scores