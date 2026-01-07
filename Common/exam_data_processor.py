from common.contracts import DataProcessor, ExamScore

class ExamDataProcessor(DataProcessor):
    def compute_number_of_unique_students(self, scores: [ExamScore]) -> int:
        """
        Given a list of ExamScore's, computes the number of unique students in the data set
        """

        # TODO: implement here
        unique_students = set()
        for score in scores:
            unique_students.add(score.student_id)
        unique_student_count = len(unique_students)

        return unique_student_count

    def compute_average_final(self, scores: [ExamScore]) -> float:
        """
        Given a list of ExamScore's, computes the average of all final scores
        """

        # TODO: implement here
        finals_list = []
        for score in scores:
            if score.exam_name == "final":
                finals_list.append(int(score.score))
        #check that there's something in the list before computing average
        if finals_list:
            final_average = sum(finals_list) / len(finals_list)
        else:
            final_average = 0

        return final_average