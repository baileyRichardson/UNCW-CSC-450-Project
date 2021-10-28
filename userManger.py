import Database
class userManager:
    total_user_id = 1

    def __init__(self,email: str):
        self.email = email
        Database.create_user(email.replace(".com", ""), email)
        self.total_user_id = self.total_user_id + 1


