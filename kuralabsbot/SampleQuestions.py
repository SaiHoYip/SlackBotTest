class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer
question_prompt = [
    """Why is AWS more economical than traditional data centers for applications with varying compute workloads?
    (a)Amazon EC2 costs are billed on a monthly basis. 
    (b)Users retain full administrative access to their Amazon EC2 instances.
    (c)Amazon EC2 instances can be launched on demand when needed.
    (d)Users can permanently run enough instances to handle peak workloads.
    """,
    """Which AWS service would simplify the migration of a database to AWS?
    (a)AWS Storage Gateway
    (b)AWS Database Migration Service (AWS DMS)
    (c)Amazon EC2
    (d)Amazon AppStream 2.0
    """,
    """Which AWS offering enables users to find, buy, and immediately start using software solutions in their AWS environment? 
    (a)AWS Config
    (b)AWS OpsWorks
    (c)AWS SDK
    (d)AWS Marketplace
    """
]

questions = [
    Question(question_prompt[0], "C"),
    Question(question_prompt[1], "B"),
    Question(question_prompt[2], "D")
]

def run_test(questions):
    for question in questions:
        answer = input(question.prompt)

def run_quiz(questions):
    score = 0
    for question in questions:
        answer = input(question.prompt).upper()
        if answer == question.answer:
            score += 1
    print("You got " + str(score) + '/' + str(len(questions)) + "correct")

def runQ():
    return run_quiz(questions)

runQ()