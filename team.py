import random
import numpy as np
from typing import List, Optional, Tuple, Dict



class Team:
    """
    کلاس تیم ملی فوتبال.
    مسئولیت: نگهداری اطلاعات تیم، آمار مسابقات و شبیه‌سازی نتیجه بازی مقابل حریف.
    """

    def __init__(self, name: str, attack: int, defense: int, rank: int):
        

       
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None  # نام گروه (اختیاری)

    def goal_difference(self) -> int:
        """برگرداندن تفاضل گل (گل زده منهای گل خورده)"""
        return self.goals_for - self.goals_against

    def reset_stats(self) -> None:
        """صفر کردن آمار (گل‌ها و امتیاز) برای شروع یک شبیه‌سازی جدید"""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def _simulate_penalty_shootout(self, opponent: 'Team') -> 'Team':
        """
        شبیه‌سازی ضربات پنالتی (داخلی).
        احتمال گل بر اساس حمله خودی و دفاع حریف محاسبه می‌شود.
""" 
     
        # احتمال گل برای خودی و حریف (محدود به بازه ۰.۶ تا ۰.۹)
        prob_self = 0.75 + (self.attack - opponent.defense) / 250
        prob_self = max(0.6, min(0.9, prob_self))

        prob_opp = 0.75 + (opponent.attack - self.defense) / 250
        prob_opp = max(0.6, min(0.9, prob_opp))

        # مرحله ۵ ضربه اول
        self_goals = sum(1 for _ in range(5) if random.random() < prob_self)
        opp_goals = sum(1 for _ in range(5) if random.random() < prob_opp)

        # اگر مساوی شد، ضربات ناگهانی (Sudden Death)
        while self_goals == opp_goals:
            self_score = 1 if random.random() < prob_self else 0
            opp_score = 1 if random.random() < prob_opp else 0
            self_goals += self_score
            opp_goals += opp_score

            # اگر در همین دور نتیجه مشخص شد (یکی گل زد و دیگری نه)
            if self_goals != opp_goals:
                break

        return self if self_goals > opp_goals else opponent

    def simulate_match(self, opponent: 'Team', is_knockout: bool = False) -> Tuple[int, int, Optional['Team']]:
        """
        شبیه‌سازی نتیجه بازی با تیم حریف

        Returns:
            tuple: (گل_تیم_خودی, گل_تیم_حریف, برنده_مسابقه)
                   در مرحله گروهی، برنده همیشه None است.
                   در مرحله حذفی، برنده یک شیء Team یا None (در صورت بروز خطا) است.
        """
        # --- ۱. شبیه‌سازی ۹۰ دقیقه با توزیع پواسون ---
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opp = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        # تولید تعداد گل (مقادیر ورودی باید غیرمنفی باشند، پواسون این تضمین را دارد)
        goals_self = np.random.poisson(lam=max(0, lambda_self))
        goals_opp = np.random.poisson(lam=max(0, lambda_opp))

        # --- ۲. اگر مرحله گروهی است، بدون وقت اضافه و پنالتی برگردان ---
        if not is_knockout:
            return goals_self, goals_opp, None

        # --- ۳. مرحله حذفی و تساوی در ۹۰ دقیقه ---
        if goals_self == goals_opp:
            # شبیه‌سازی وقت اضافه ۳۰ دقیقه (lambda * 0.33)
            et_self = np.random.poisson(lam=max(0, lambda_self * 0.33))
            et_opp = np.random.poisson(lam=max(0, lambda_opp * 0.33))

            goals_self += et_self
            goals_opp += et_opp

        # --- ۴. اگر در وقت اضافه نتیجه مشخص شد ---
        if goals_self != goals_opp:
            winner = self if goals_self > goals_opp else opponent
            return goals_self, goals_opp, winner

        # --- ۵. اگر باز هم مساوی شد -> پنالتی ---
        # توجه: گل‌های پنالتی به آمار گل‌های بازی اضافه نمی‌شوند، فقط برنده مشخص می‌شود.
        winner = self._simulate_penalty_shootout(opponent)
        return goals_self, goals_opp, winner

    def __repr__(self) -> str:
        return f"Team({self.name}, rank={self.rank}, attack={self.attack}, defense={self.defense})"

