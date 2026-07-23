
import random
from typing import List, Tuple
from match import Match
from team import Team

class Group:
    """
    کلاس گروه مرحله گروهی.
    مسئولیت: نگهداری تیم‌های گروه، اجرای بازی‌ها، رتبه‌بندی و انتخاب تیم‌های صعودکننده.
    """

    def __init__(self, name: str):
        
        self.name = name
        self.teams: List[Team] = []

    def add_team(self, team: Team) -> None:
        """اضافه کردن یک تیم به گروه"""
        self.teams.append(team)
        team.group = self.name  # نام گروه را در تیم نیز ثبت می‌کنیم

    def play_all_matches(self) -> None:
        """
        انجام تمام مسابقات گروه به صورت دور رفت (هر تیم با ۳ تیم دیگر یک بار بازی می‌کند).
        """
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()

    def get_ranking(self) -> List[Team]:
        """
        رتبه‌بندی تیم‌های گروه بر اساس:
        ۱. امتیاز بیشتر
        ۲. تفاضل گل بیشتر
        ۳. گل زده بیشتر
        ۴. قرعه‌کشی تصادفی (در صورت تساوی کامل)

        Returns:
            List[Team]: لیست تیم‌ها به ترتیب (اول تا چهارم)
        """
        # کپی از لیست تیم‌ها برای مرتب‌سازی (تا به ترتیب اصلی دست نزنیم)
        sorted_teams = self.teams.copy()

        # مرتب‌سازی با کلیدهای .. همه نزولی
        sorted_teams.sort(
            key=lambda t: (t.points, t.goal_difference(), t.goals_for),
            reverse=True
        )

        # اگر دو یا چند تیم در همه موارد مساوی بودند، قرعه‌کشی تصادفی انجام می‌شود
      
        i = 0
        while i < len(sorted_teams):
            j = i + 1
            # پیدا کردن محدوده تیم‌های مساوی
            while j < len(sorted_teams):
                t1 = sorted_teams[i]
                t2 = sorted_teams[j]
                if (t1.points == t2.points and
                    t1.goal_difference() == t2.goal_difference() and
                    t1.goals_for == t2.goals_for):
                    j += 1
                else:
                    break

            # اگر بیش از یک تیم مساوی بود، تصادفی shuffle کن
            if j - i > 1:
                segment = sorted_teams[i:j]
                random.shuffle(segment)
                sorted_teams[i:j] = segment

            i = j

        return sorted_teams

    def advance_teams(self) -> Tuple[Team, Team]:
        """
        انتخاب دو تیم اول گروه برای صعود به مرحله حذفی
        """
        ranking = self.get_ranking()
        return ranking[0], ranking[1]

    def display_table(self) -> None:
        """
        نمایش جدول گروه به صورت مرتب‌شده.
        """
        ranking = self.get_ranking()
        print(f"\n===== Group {self.name} =====")
        print(f"{'رتبه':<4} {'تیم':<20} {'امتیاز':<6} {'تفاضل':<6} {'گل زده':<6}")
        print("-" * 50)
        for idx, team in enumerate(ranking, 1):
            print(f"{idx:<4} {team.name:<20} {team.points:<6} {team.goal_difference():<6} {team.goals_for:<6}")

    def __repr__(self) -> str:
        return f"Group({self.name}, {len(self.teams)} teams)"       
        