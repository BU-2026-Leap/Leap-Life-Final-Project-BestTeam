from common.contracts import DataFetcher, ExamScore

import csv

class LocalCSVDataFetcher(DataFetcher):
    def __init__(self, file_path:str):
        self.file_path = file_path

    def fetch(self) -> [ExamScore]:
        scores = []

        # TODO: implement here
        with open(self.file_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                scores.append(
                    ExamScore(
                        student_id = row['student_id'],
                        exam_name = row['exam_name'],
                        score = float(row['score'])
                    )
                )

        return scores