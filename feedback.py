class Feedback:
    def __init__(self, user_experience: str, feedback: str):
        self.user_experience = user_experience
        self.feedback = feedback

    def feedback_to_dict(self):
        return {
            '_id': None,
            'user_experience': self.user_experience,
            'feedback': self.feedback
        }