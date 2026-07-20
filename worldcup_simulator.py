# ================================
# دانشجو: [zahrazarini]
# شماره دانشجویی: [404990353]
# عنوان پروژه: شبیه ساز جام جهانی
#[ تاریخ تحویل:[1405.4.31
# ================================

import csv
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

        group_name = chr(ord('A') + i)
            
class WorldCupSimulator:
    """
    کلاس اصلی شبیه‌ساز جام جهانی.
    مسئولیت: مدیریت کل فرآیند جام (بارگذاری، قرعه‌کشی، گروهی، حذفی، شبیه‌سازی‌های متعدد).
    """

    def __init__(self):
        """سازنده کلاس WorldCupSimulator."""
        self.teams: List[Team] = []
        self.groups: List[Group] = []
        self.round_of_16: Optional[KnockoutStage] = None
        self.quarterfinals: Optional[KnockoutStage] = None
        self.semifinals: Optional[KnockoutStage] = None
        self.final: Optional[KnockoutStage] = None
        self.champion: Optional[Team] = None

    def load_teams_from_csv(self, filepath: str = "worldcup_2026_teams.csv") -> None:
      try:
          with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.teams = []
            for row in reader:
                team = Team(
                    name=row['name'],
                    attack=int(row['attack']),
                    defense=int(row['defense']),
                    rank=int(row['rank'])
                )
                self.teams.append(team)
          print(f"✅ {len(self.teams)} تیم با موفقیت بارگذاری شد!")
      except FileNotFoundError:
          print("⚠️ فایل CSV پیدا نشد! از داده‌های داخلی استفاده می‌شود.")
          teams_data = [
            ("Argentina", 95, 92, 1), ("France", 94, 89, 2),
            ("Brazil", 93, 91, 3), ("England", 91, 87, 4),
            ("Belgium", 89, 86, 5), ("Croatia", 88, 84, 6),
            ("Netherlands", 87, 85, 7), ("Portugal", 86, 83, 8),
            ("Spain", 85, 88, 9), ("Italy", 84, 82, 10),
            ("Uruguay", 83, 80, 11), ("Morocco", 82, 81, 12),
            ("Germany", 81, 86, 13), ("USA", 80, 79, 14),
            ("Mexico", 79, 78, 15), ("Japan", 78, 77, 16),
            ("Senegal", 77, 75, 17), ("Switzerland", 76, 76, 18),
            ("Iran", 75, 74, 19), ("Denmark", 74, 73, 20),
            ("South Korea", 73, 72, 21), ("Australia", 72, 71, 22),
            ("Peru", 71, 70, 23), ("Sweden", 70, 69, 24),
            ("Poland", 69, 68, 25), ("Ukraine", 68, 67, 26),
            ("Wales", 67, 66, 27), ("Egypt", 66, 65, 28),
            ("Nigeria", 65, 64, 29), ("Canada", 64, 63, 30),
            ("Ecuador", 63, 62, 31), ("Saudi Arabia", 62, 61, 32)
         ]
          self.teams = []
          for name, attack, defense, rank in teams_data:
             self.teams.append(Team(name, attack, defense, rank))
          print(f"✅ {len(self.teams)} تیم از داده‌های داخلی بارگذاری شد!")
    def seed_and_draw_groups(self) -> None:
        """سیدبندی و قرعه‌کشی گروه‌ها"""
        if len(self.teams) != 32:
            print("❌ خطا: تعداد تیم‌ها باید ۳۲ باشد!")
            return
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)
        seeds = [
            sorted_teams[0:8],
            sorted_teams[8:16],
            sorted_teams[16:24],
            sorted_teams[24:32]
        ]
        for seed in seeds:
            random.shuffle(seed)
        self.groups = []
        for i in range(8):
            group_name = chr(ord('A') + i)
            self.groups.append(Group(group_name))
        for seed_index, seed in enumerate(seeds):
            for group_index, team in enumerate(seed):
                self.groups[group_index].add_team(team)
        print("✅ قرعه‌کشی گروه‌ها با موفقیت انجام شد!")
        for group in self.groups:
            print(f"   گروه {group.name}: {', '.join([t.name for t in group.teams])}")

    def run_group_stage(self) -> None:
        """اجرای مرحله گروهی و نمایش جدول هر گروه"""
        if not self.groups:
            print("❌ خطا: ابتدا قرعه‌کشی گروه‌ها را انجام دهید!")
            return
        print("\n===== مرحله گروهی =====")
        for group in self.groups:
            group.play_all_matches()
            group.display_table()

    def setup_knockout_bracket(self) -> None:
        """ساخت براکت حذفی بر اساس قانون فیفا"""
        if not self.groups:
            print("❌ خطا: ابتدا مرحله گروهی را اجرا کنید!")
            return
        group_winners = []
        for group in self.groups:
            first, second = group.advance_teams()
            group_winners.append((first, second))
        pairs = [
            (group_winners[0][0], group_winners[1][1]),
            (group_winners[2][0], group_winners[3][1]),
            (group_winners[4][0], group_winners[5][1]),
            (group_winners[6][0], group_winners[7][1]),
            (group_winners[1][0], group_winners[0][1]),
            (group_winners[3][0], group_winners[2][1]),
            (group_winners[5][0], group_winners[4][1]),
            (group_winners[7][0], group_winners[6][1])
        ]
        self.round_of_16 = KnockoutStage("Round of 16", pairs)
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        print("✅ براکت حذفی با موفقیت ساخته شد!")

    def run_knockout_stage(self) -> None:
        """اجرای تمام مراحل حذفی"""
        if not self.round_of_16:
            print("❌ خطا: ابتدا براکت حذفی را بسازید!")
            return
        print("\n===== مرحله یک‌هشتم نهایی =====")
        self.round_of_16.play_round()
        self.round_of_16.display_results()
        qf_winners = self.round_of_16.get_winners()
        qf_pairs = []
        for i in range(0, len(qf_winners), 2):
            qf_pairs.append((qf_winners[i], qf_winners[i+1]))
        self.quarterfinals = KnockoutStage("Quarterfinals", qf_pairs)
        print("\n===== مرحله یک‌چهارم نهایی =====")
        self.quarterfinals.play_round()
        self.quarterfinals.display_results()
        sf_winners = self.quarterfinals.get_winners()
        sf_pairs = [
            (sf_winners[0], sf_winners[1]),
            (sf_winners[2], sf_winners[3])
        ]
        self.semifinals = KnockoutStage("Semifinals", sf_pairs)
        print("\n===== مرحله نیمه‌نهایی =====")
        self.semifinals.play_round()
        self.semifinals.display_results()
        final_winners = self.semifinals.get_winners()
        final_pairs = [(final_winners[0], final_winners[1])]
        self.final = KnockoutStage("Final", final_pairs)
        print("\n===== فینال =====")
        self.final.play_round()
        self.final.display_results()
        self.champion = self.final.get_winners()[0]
        print(f"\n🏆 قهرمان جام جهانی: {self.champion.name} 🏆")

    def run_full_simulation(self) -> Team:
        """اجرای کامل جام (گروهی + حذفی) و برگرداندن قهرمان"""
        for team in self.teams:
            team.reset_stats()
        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()
        return self.champion

    def most_likely_champion(self, num_simulations: int = 1000) -> Dict[str, float]:
        """شبیه‌سازی چندباره و محاسبه درصد قهرمانی"""
        if num_simulations <= 0:
            print("❌ خطا: تعداد شبیه‌سازی‌ها باید مثبت باشد!")
            return {}
        print(f"\n===== شبیه‌سازی {num_simulations} باره =====")
        champion_counts = {team.name: 0 for team in self.teams}
        for i in range(num_simulations):
            if (i + 1) % 100 == 0:
                print(f"   در حال اجرای شبیه‌سازی {i+1}/{num_simulations}...")
            champion = self.run_full_simulation()
            champion_counts[champion.name] += 1
        percentages = {}
        for name, count in champion_counts.items():
            percentages[name] = (count / num_simulations) * 100
        print("\n===== درصد قهرمانی هر تیم =====")
        sorted_teams = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
        for name, percent in sorted_teams:
            if percent > 0:
                print(f"{name}: {percent:.2f}%")
        return percentages

    def display_bracket(self) -> None:
        """نمایش براکت حذفی آخرین شبیه‌سازی"""
        if not self.round_of_16:
            print("❌ خطا: هنوز براکت حذفی ساخته نشده است!")
            return
        print("\n===== براکت حذفی =====")
        if self.round_of_16:
            self.round_of_16.display_results()
        if self.quarterfinals:
            self.quarterfinals.display_results()
        if self.semifinals:
            self.semifinals.display_results()
        if self.final:
            self.final.display_results()
        if self.champion:
            print(f"\n🏆 قهرمان: {self.champion.name}")

    def __repr__(self) -> str:
        return f"WorldCupSimulator({len(self.teams)} teams, {len(self.groups)} groups)"
# منوی اصلی

def show_menu():
    """نمایش منوی اصلی ستا"""
    print("\n" + "=" * 55)
    print("         شبیه‌ساز جام جهانی ۲۰۲۶")
    print("=" * 55)
    print()
    print("   1.  بارگذاری تیم‌ها از فایل CSV")
    print("  2.  انجام قرعه‌کشی گروه‌ها (سیدبندی خودکار)")
    print("   3.  اجرای مرحله گروهی و نمایش جدول هر گروه")
    print("  4.  اجرای کامل جام (گروهی + حذفی) و نمایش قهرمان")
    print("  5.  شبیه‌سازی ۱۰۰۰ بارگزارش درصد قهرمانی")
    print("    6.  نمایش براکت حذفی آخرین شبیه‌سازی")
    print("      7.  خروج از برنامه")
    print()
    print("=" * 55)

def main():
    """تابع اصلی برنامه با منوی تعاملی"""
    simulator = WorldCupSimulator()

    while True:
        show_menu()
        choice = input("✨ لطفاً یک گزینه را انتخاب کنید (۱-۷): ").strip()

        if choice == "1":
            simulator.load_teams_from_csv()

        elif choice == "2":
            if not simulator.teams:
                print("❌ ابتدا تیم‌ها را بارگذاری کنید! (گزینه ۱) 📂")
            else:
                simulator.seed_and_draw_groups()

        elif choice == "3":
            if not simulator.groups:
                print("❌ ابتدا قرعه‌کشی گروه‌ها را انجام دهید! (گزینه ۲) 🎲")
            else:
                simulator.run_group_stage()

        elif choice == "4":
            if not simulator.teams:
                print("❌ ابتدا تیم‌ها را بارگذاری کنید! (گزینه ۱) 📂")
            else:
                simulator.run_full_simulation()

        elif choice == "5":
            if not simulator.teams:
                print("❌ ابتدا تیم‌ها را بارگذاری کنید! (گزینه ۱) 📂")
            else:
                try:
                    num = input("🔢 تعداد شبیه‌سازی‌ها (پیش‌فرض ۱۰۰۰): ").strip()
                    if num == "":
                        num = 1000
                    else:
                        num = int(num)
                    simulator.most_likely_champion(num)
                except ValueError:
                    print("❌ خطا: لطفاً یک عدد صحیح وارد کنید! 🔢")

        elif choice == "6":
            if not simulator.round_of_16:
                print("❌ ابتدا یک شبیه‌سازی کامل اجرا کنید! (گزینه ۴) 🏆")
            else:
                simulator.display_bracket()

        elif choice == "7":
            print("\n👋 خداحافظ! موفق باشید! 🏆⚽")
            break

        else:
            print("❌ گزینه نامعتبر! لطفاً بین ۱ تا ۷ انتخاب کنید. ⚠️")

        input("\n🔄 برای ادامه، کلید Enter را بزنید...")
#اجرا برنامه
if __name__ == "__main__":
    main()