import Database


class DashReport():
    def __init__(self, user_email: str):
        self.user_email = user_email
        self.doughnut_chart_data = []
        self.bar_chart_data = []
        self.steam_accounts = Database.list_of_steam_accounts(user_email)
        self.num_accounts = len(self.steam_accounts)
        for account in self.steam_accounts:
            limit_length = Database.get_limit_duration(user_email, account)
            if limit_length == "week":
                lim = 1
            else:
                lim = 2
            limit = Database.get_playtime_limit(user_email, account)
            if limit == 0:
                self.doughnut_chart_data.append((-1, -1))
            else:
                limit *= 60
                time_elapsed = (Database.get_playtime_sums(user_email, account))[lim]
                self.doughnut_chart_data.append((time_elapsed, limit, limit_length))
            self.bar_chart_data.append(Database.get_top_five_games(user_email, account))
