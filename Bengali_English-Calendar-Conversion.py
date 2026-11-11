import sys

def gregorian_to_jdn(y, m, d):
    return (1461 * (y + 4800 + (m - 14) // 12)) // 4 \
         + (367 * (m - 2 - 12 * ((m - 14) // 12))) // 12 \
         - (3 * ((y + 4900 + (m - 14) // 12) // 100)) // 4 \
         + d - 32075

def jdn_to_gregorian(jdn):
    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    d = l - (2447 * j) // 80
    l = j // 11
    m = j + 2 - 12 * l
    y = 100 * (n - 49) + i + l
    return y, m, d

def is_gregorian_leap(year):
    if year % 400 == 0: return True
    if year % 100 == 0: return False
    return year % 4 == 0

def is_julian_leap(year):
    return year % 4 == 0

def get_day_of_week(d, m, y):
    if m < 3: 
        m += 12
        y -= 1
    q, k, j = d, y % 100, y // 100
    h = (q + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return days[h]

def get_day_of_week_num(d, m, y):
    if m < 3: 
        m += 12
        y -= 1
    q, k, j = d, y % 100, y // 100
    return (q + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7

def get_day_of_year(d, m, y):
    m_len = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_gregorian_leap(y): m_len[2] = 29
    return sum(m_len[1:m]) + d

def get_gregorian_from_day_of_year(doy, y):
    m_len = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_gregorian_leap(y): m_len[2] = 29
    m = 1
    while doy > m_len[m]:
        doy -= m_len[m]
        m += 1
    return doy, m

def is_valid_gregorian_date(d, m, y):
    if y < 1 or m < 1 or m > 12 or d < 1: return False
    m_len = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_gregorian_leap(y): m_len[2] = 29
    return d <= m_len[m]

def get_bangla_month_lengths(by, version):
    b_lens = [0] * 12
    if version == 3: # Traditional India
        base = [31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30]
        for i in range(12): b_lens[i] = base[i]
        if is_gregorian_leap(by + 594): b_lens[11] = 31
    else:
        is_leap = is_gregorian_leap(by + 594)
        if version in (1, 4): # BD old & India Saha
            base = [31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30]
            for i in range(12): b_lens[i] = base[i]
            if is_leap: b_lens[10] = 31
        else: # BD modern 2019+
            base = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 29, 30]
            for i in range(12): b_lens[i] = base[i]
            if is_leap: b_lens[10] = 30
    return b_lens

def get_bangla_date_details(d, m, y, ver):
    b_months = ["Boishakh", "Jyoishtho", "Asharh", "Shrabon", "Bhadro", "Ashshin",
                "Kartik", "Ogrohayon", "Poush", "Magh", "Falgun", "Choitro"]
    doy = get_day_of_year(d, m, y)

    start_offset = 104
    if ver == 3: start_offset = 105
    if is_gregorian_leap(y): start_offset += 1

    by = (y - 593) if (doy >= start_offset) else (y - 594)

    if doy >= start_offset:
        rel_days = doy - start_offset + 1
    else:
        prev_year_days = 366 if is_gregorian_leap(y - 1) else 365
        prev_start_offset = (106 if is_gregorian_leap(y - 1) else 105) if ver == 3 else (105 if is_gregorian_leap(y - 1) else 104)
        rel_days = (prev_year_days - prev_start_offset + 1) + doy

    b_lens = get_bangla_month_lengths(by, ver)

    idx = 0
    while rel_days > b_lens[idx] and idx < 11:
        rel_days -= b_lens[idx]
        idx += 1
        
    return rel_days, b_months[idx], by

def bangla_to_gregorian(bd, bm_idx, by, ver):
    b_lens = get_bangla_month_lengths(by, ver)
    accumulated = sum(b_lens[:bm_idx]) + (bd - 1)

    start_offset = 105 if ver == 3 else 104
    gy = by + 593
    if is_gregorian_leap(gy): start_offset += 1

    doy = start_offset + accumulated
    total_days = 366 if is_gregorian_leap(gy) else 365

    if doy > total_days:
        doy -= total_days
        gy += 1

    gd, gm = get_gregorian_from_day_of_year(doy, gy)
    return gd, gm, gy

def add_days_to_date(d, m, y, delta):
    jdn = gregorian_to_jdn(y, m, d) + delta
    return jdn_to_gregorian(jdn)

def date_difference(d1, m1, y1, d2, m2, y2):
    j1 = gregorian_to_jdn(y1, m1, d1)
    j2 = gregorian_to_jdn(y2, m2, d2)
    
    if j1 > j2:
        j1, j2 = j2, j1
        d1, d2 = d2, d1
        m1, m2 = m2, m1
        y1, y2 = y2, y1

    years = y2 - y1
    months = m2 - m1
    days = d2 - d1

    if days < 0:
        months -= 1
        prev_m = m2 - 1
        prev_y = y2
        if prev_m < 1: 
            prev_m = 12
            prev_y -= 1
        m_len = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if is_gregorian_leap(prev_y): m_len[2] = 29
        days += m_len[prev_m]
        
    if months < 0:
        years -= 1
        months += 12

    return years, months, days

def print_julian_date(d, m, y):
    julian_days = gregorian_to_jdn(y, m, d) - 1721423

    julian_year = 1
    while True:
        diy = 366 if is_julian_leap(julian_year) else 365
        if julian_days <= diy: break
        julian_days -= diy
        julian_year += 1

    julian_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_julian_leap(julian_year): julian_months[2] = 29

    julian_month = 1
    while julian_days > julian_months[julian_month]:
        julian_days -= julian_months[julian_month]
        julian_month += 1

    month_names = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    print(f"{'Julian Date':<23}: {julian_days} {month_names[julian_month]} {julian_year}")

def print_english_month_grid(month, year):
    months = ["", "January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    m_len = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_gregorian_leap(year): m_len[2] = 29

    print(f"\n      {months[month]} {year}")
    print("  S   M   T   W   T   F   S")

    start_day = get_day_of_week_num(1, month, year)
    spaces = (start_day + 6) % 7

    print("    " * spaces, end="")
    for day in range(1, m_len[month] + 1):
        print(f"{day:>3} ", end="")
        if (day + spaces) % 7 == 0: print()
    print()

def print_bangla_month_grid(b_month_idx, b_year, version):
    b_months = ["Boishakh", "Jyoishtho", "Asharh", "Shrabon", "Bhadro", "Ashshin",
                "Kartik", "Ogrohayon", "Poush", "Magh", "Falgun", "Choitro"]
    print(f"\n      {b_months[b_month_idx]} {b_year} BS")
    print("  S   M   T   W   T   F   S")

    greg_year = b_year + 593
    base_doy = 105 if version == 3 else 104
    if is_gregorian_leap(greg_year): base_doy += 1

    b_lens = get_bangla_month_lengths(b_year, version)
    accumulated_days = sum(b_lens[:b_month_idx])

    target_doy = base_doy + accumulated_days
    total_greg_days = 366 if is_gregorian_leap(greg_year) else 365
    if target_doy > total_greg_days:
        target_doy -= total_greg_days
        greg_year += 1

    gd, gm = get_gregorian_from_day_of_year(target_doy, greg_year)
    start_day = get_day_of_week_num(gd, gm, greg_year)
    spaces = (start_day + 6) % 7

    print("    " * spaces, end="")
    for day in range(1, b_lens[b_month_idx] + 1):
        print(f"{day:>3} ", end="")
        if (day + spaces) % 7 == 0: print()
    print()

def convert_gregorian_to_bangla():
    try:
        print("\nEnter Gregorian Date (DD MM YYYY): ", end="")
        d, m, y = map(int, input().split())
        if not is_valid_gregorian_date(d, m, y):
            print("Invalid Date.")
            return
    except ValueError:
        print("Invalid input format.")
        return

    m_names = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
               
    print("\n================ DATE CONVERSION RESULTS ================")
    print(f"{'Gregorian Date':<23}: {d} {m_names[m]} {y}")
    print_julian_date(d, m, y)
    print(f"{'Day of the Week':<23}: {get_day_of_week(d, m, y)}")
    print("---------------------------------------------------------")

    bd, bm, by = get_bangla_date_details(d, m, y, 1)
    print(f"{'Bangla (BD 1987-2018)':<23}: {bd} {bm} {by} BS")
    bd, bm, by = get_bangla_date_details(d, m, y, 2)
    print(f"{'Bangla (BD 2019-Pres)':<23}: {bd} {bm} {by} BS")
    bd, bm, by = get_bangla_date_details(d, m, y, 3)
    print(f"{'Bangla (India Trad)':<23}: {bd} {bm} {by} BS")
    bd, bm, by = get_bangla_date_details(d, m, y, 4)
    print(f"{'Bangla (India Saha)':<23}: {bd} {bm} {by} BS")
    print("=========================================================")

def convert_bangla_to_gregorian():
    print("\nEnter Bangla Date & Version (Day Month Year [Version 1-4]):")
    print("(e.g., 23 2 1480 2) > ", end="")
    
    try:
        parts = input().split()
        bd = int(parts[0])
        bm = int(parts[1])
        by = int(parts[2])
        ver = int(parts[3]) if len(parts) > 3 else 2
    except (ValueError, IndexError):
        print("Invalid input format.")
        return

    if bm < 1 or bm > 12 or bd < 1 or by < 1 or ver < 1 or ver > 4:
        print("Invalid input (Check date bounds and Version 1-4).")
        return

    gd, gm, gy = bangla_to_gregorian(bd, bm - 1, by, ver)
    m_names = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

    print("\n================ DATE CONVERSION RESULTS ================")
    print(f"{'Gregorian Date':<23}: {gd} {m_names[gm]} {gy}")
    print(f"{'Day of Week':<23}: {get_day_of_week(gd, gm, gy)}")
    print("=========================================================")

def run_merged_conversion_menu():
    print("\n--- Date Conversion Options ---")
    print("2.1 Gregorian -> Bangla")
    print("2.2 Bangla -> Gregorian")
    sub_opt = input("Select Direction (2.1 or 2.2): ").strip()

    if sub_opt in ("2.1", "1"):
        convert_gregorian_to_bangla()
    elif sub_opt in ("2.2", "2"):
        convert_bangla_to_gregorian()
    else:
        print("Invalid Selection.")

def run_age_calculator_option():
    print("\n--- Age / Date Difference Calculator ---")
    try:
        print("Enter first date  (DD MM YYYY) [e.g. birth]: ", end="")
        d1, m1, y1 = map(int, input().split())
        print("Enter second date (DD MM YYYY) [e.g. today]: ", end="")
        d2, m2, y2 = map(int, input().split())
        
        if not is_valid_gregorian_date(d1, m1, y1) or not is_valid_gregorian_date(d2, m2, y2):
            print("Invalid date.")
            return
    except ValueError:
        print("Invalid input format.")
        return

    years, months, days = date_difference(d1, m1, y1, d2, m2, y2)
    j1 = gregorian_to_jdn(y1, m1, d1)
    j2 = gregorian_to_jdn(y2, m2, d2)
    total_days = abs(j2 - j1)

    print(f"\nExact difference: {years} years, {months} months, {days} days")
    print(f"Total days      : {total_days} days")

def run_add_subtract_days_option():
    print("\n--- Add / Subtract Days ---")
    try:
        print("Enter starting Gregorian date (DD MM YYYY): ", end="")
        d, m, y = map(int, input().split())
        if not is_valid_gregorian_date(d, m, y):
            print("Invalid date.")
            return
        print("Enter number of days to add (negative to subtract): ", end="")
        delta = int(input())
    except ValueError:
        print("Invalid input format.")
        return

    nd, nm, ny = add_days_to_date(d, m, y, delta)
    m_names = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

    print(f"\nResult Gregorian : {nd} {m_names[nm]} {ny}")
    print(f"Day of Week      : {get_day_of_week(nd, nm, ny)}")

    bd, bm, by = get_bangla_date_details(nd, nm, ny, 2)
    print(f"Bangla (BD 2019+): {bd} {bm} {by} BS")

def run_year_calendar_option():
    print("\n--- Year-Calendar Options ---")
    print("1.1 Enter Bangla Year  -> Show Bangla Year Calendar")
    print("1.2 Enter English Year -> Show Bangla Year Calendar")
    print("1.3 Enter Bangla Year  -> Show English Year Calendar")
    print("1.4 Enter English Year -> Show English Year Calendar")
    sub_opt = input("Select Sub-option (1.1 - 1.4): ").strip()

    try:
        input_year = int(input("Enter Year: "))
    except ValueError:
        print("Invalid input format.")
        return

    if sub_opt == "1.1":
        print(f"\nGenerating Bangla Calendar for {input_year} BS (Bangladesh Modern 2019 Rules):")
        for m in range(12): print_bangla_month_grid(m, input_year, 2)
    elif sub_opt == "1.2":
        converted_bangla_year = input_year - 593
        print(f"\nEnglish Year {input_year} maps primarily to Bangla Year {converted_bangla_year} BS.")
        for m in range(12): print_bangla_month_grid(m, converted_bangla_year, 2)
    elif sub_opt == "1.3":
        converted_gregorian_year = input_year + 593
        print(f"\nBangla Year {input_year} BS intersects heavily with English Year {converted_gregorian_year}.")
        for m in range(1, 13): print_english_month_grid(m, converted_gregorian_year)
    elif sub_opt == "1.4":
        print(f"\nGenerating English Year Calendar for {input_year}:")
        for m in range(1, 13): print_english_month_grid(m, input_year)
    else:
        print("Invalid Sub-option choice.")


if __name__ == "__main__":
    while True:
        print("\n=========================================================")
        print("         Bengali - English Calendar Conversion System")
        print("=========================================================")
        print("1. Year-Calendar Generator")
        print("2. Date Conversion (Gregorian <-> Bangla)")
        print("3. Age / Date Difference Calculator")
        print("4. Add / Subtract Days from a Date")
        print("5. Exit System")
        
        try:
            choice = int(input("Choose Option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            run_year_calendar_option()
        elif choice == 2:
            run_merged_conversion_menu()
        elif choice == 3:
            run_age_calculator_option()
        elif choice == 4:
            run_add_subtract_days_option()
        elif choice == 5:
            break
        else:
            print("Invalid Option. Try again.")
