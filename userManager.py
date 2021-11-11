import Database
class userManager:
    total_user_id = 1

    def __init__(self,email: str):
        self.email = email
        Database.create_user(email.replace(".", ""), email)
        self.total_user_id = self.total_user_id + 1

    def get_email(self):
        return self.email


