
# ================================
# دانشجو: [zahrazarini]
# شماره دانشجویی: [404990353]
# عنوان پروژه: شبیه ساز جام جهانی
#[ تاریخ تحویل:[1405.4.31
# ================================


from worldcup_simulator import WorldCupSimulator

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
    