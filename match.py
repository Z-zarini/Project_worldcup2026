
from typing import Optional
from team import Team


class Match:
    """
    کلاس مسابقه بین دو تیم.
    مسئولیت: شبیه‌سازی یک بازی، ثبت نتیجه، به‌روزرسانی آمار تیم‌ها و تعیین برنده (در مراحل حذفی).
    """

    def __init__(self, team1: Team, team2: Team, is_knockout: bool = False):
        
        self.team1 = team1
        self.team2 = team2
        self.goals1: int = 0
        self.goals2: int = 0
        self.is_knockout = is_knockout
        self.winner: Optional[Team] = None

    def play(self) -> None:
        """
        اجرای مسابقه:
        - با فراخوانی simulate_match روی تیم اول، نتیجه را محاسبه می‌کند.
        - گل‌ها را ذخیره می‌کند.
        - آمار تیم‌ها را به‌روز می‌کند (گل زده، گل خورده، و در مرحله گروهی امتیاز).
        - در صورت حذفی، برنده را مشخص می‌کند.
        """
        # شبیه‌سازی بازی (متد simulate_match در کلاس Team)
        goals1, goals2, winner = self.team1.simulate_match(self.team2, self.is_knockout)
        self.goals1 = goals1
        self.goals2 = goals2
        self.winner = winner  # در مرحله گروهی، winner = None است

        # به‌روزرسانی آمار تیم‌ها (گل زده و خورده)
        self.team1.goals_for += goals1
        self.team1.goals_against += goals2
        self.team2.goals_for += goals2
        self.team2.goals_against += goals1

        # اگر بازی مرحله گروهی است، امتیاز را محاسبه و اضافه کن
        if not self.is_knockout:
            if goals1 > goals2:
                self.team1.points += 3
            elif goals1 < goals2:
                self.team2.points += 3
            else:  # مساوی
                self.team1.points += 1
                self.team2.points += 1

    def __repr__(self) -> str:
        """
        نمایش متن نتیجه مسابقه.
        """
        if self.is_knockout and self.winner:
            return f"{self.team1.name} {self.goals1} - {self.goals2} {self.team2.name} -> برنده: {self.winner.name}"
        else:
            return f"{self.team1.name} {self.goals1} - {self.goals2} {self.team2.name}"