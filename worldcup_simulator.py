import csv
import random
from typing import List, Optional, Tuple, Dict
from team import Team
from group import Group
from knockout_stage import KnockoutStage



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
