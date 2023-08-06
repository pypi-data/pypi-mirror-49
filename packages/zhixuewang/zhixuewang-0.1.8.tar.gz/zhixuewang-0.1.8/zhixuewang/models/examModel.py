from collections import namedtuple


class examMarkModel(list):
    def __init__(self, l: list):
        super().__init__(l)

    def __str__(self):
        m = ""
        for i in self:
            m += f"{str(i)}\n"
        return m

    def __repr__(self):
        m = ""
        for i in self:
            m += f"{str(i)}\n"
        return m


class subjectMarkModel(namedtuple("subjectMarkModel", [
    "score",
    "classRank",
    "gradeRank",
    "subjectName",
    "standardScore",
    "examName",
    "examId",
])):
    def __str__(self):
        return f"{self.subjectName}:\n分数: {self.score}\n{str(self.classRank)}\n{str(self.gradeRank)}"


class classMarkModel:
    def __init__(self, avgScore: float, highScore: float, rank: int, lowScore: float):
        self.avgScore = avgScore
        self.highScore = highScore
        self.rank = rank
        self.lowScore = lowScore

    def __repr__(self):
        return f"classMarkModel(avgScore={self.avgScore}, highScore={self.highScore}, rank={self.rank}, lowScore={self.lowScore})"

    def __str__(self):
        return f"班级平均分: {self.avgScore}\n班级最高分: {self.highScore}\n班级最低分: {self.lowScore}\n班级排名: {self.rank}"


class gradeMarkModel:
    def __init__(self, avgScore: float, highScore: float, lowScore: float):
        self.avgScore = avgScore
        self.highScore = highScore
        self.lowScore = lowScore

    def __repr__(self):
        return f"gradeMarkModel(avgScore={self.avgScore}, highScore={self.highScore}, lowScore={self.lowScore})"

    def __str__(self):
        return f"年级平均分: {self.avgScore}\n年级最高分: {self.highScore}\n年级最低分: {self.lowScore}"


class examDataModel:
    def __init__(self, examId: str, examName: str):
        self.examId: str = examId
        self.examName: str = examName

    def __repr__(self):
        return f"examDataModel(examId={self.examId}, examName={self.examName})"
