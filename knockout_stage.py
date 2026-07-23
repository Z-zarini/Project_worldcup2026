from typing import List, Tuple
from match import Match
from team import Team


class KnockoutStage:
    """
    کلاس مدیریت یک مرحله از مراحل حذفی (یک‌هشتم، یک‌چهارم، نیمه‌نهایی، فینال).
    مسئولیت: دریافت جفت تیم‌ها، ساخت مسابقات، اجرای آنها و برگرداندن برنده‌ها.
    """

    def __init__(self, round_name: str, team_pairs: List[Tuple[Team, Team]]):
        """
        
        Args:
            round_name (str): نام مرحله (مثلاً 'Round of 16', 'Quarterfinals')
            team_pairs (List[Tuple[Team, Team]]): لیست جفت‌های تیم (هر جفت یک مسابقه)
        """
        self.round_name = round_name
        self.matches: List[Match] = []

        # برای هر جفت تیم، یک مسابقه حذفی می‌سازیم
        for team1, team2 in team_pairs:
            match = Match(team1, team2, is_knockout=True)
            self.matches.append(match)

    def play_round(self) -> None:
        """
        اجرای تمام مسابقات این مرحله.
        برای هر مسابقه، متد play() را صدا می‌زند تا نتیجه مشخص شود.
        """
        for match in self.matches:
            match.play()

    def get_winners(self) -> List[Team]:
        """
        دریافت لیست برنده‌های تمام مسابقات به ترتیب مسابقات.

        Returns:
            List[Team]: لیست برنده‌ها
        """
        winners = []
        for match in self.matches:
            if match.winner is not None:
                winners.append(match.winner)
            else:
                # اگر به هر دلیلی برنده مشخص نشده بود، خطا بده
                raise ValueError(f"برنده مسابقه {match.team1.name} vs {match.team2.name} مشخص نشده است!")
        return winners

    def display_results(self) -> None:
        """
        نمایش نتایج تمام مسابقات این مرحله به صورت خوانا.
        """
        print(f"\n===== {self.round_name} =====")
        for match in self.matches:
            print(match)  # از متد __repr__ کلاس Match استفاده می‌کند

    def __repr__(self) -> str:
        return f"KnockoutStage({self.round_name}, {len(self.matches)} matches)"
