# Bengali_English-Calendar-Conversion-2.0 (Bengali-English Universal Calendar System)

A comprehensive Python-based calendar conversion engine designed to handle complex conversions, date arithmetic, and full-year grid generations across multiple historical and regional calendar systems.

## Features

### 1. Date Conversion Matrix (Gregorian ↔ Bangla)
Input any standard Gregorian date or Bangla date to view its exact equivalent across multiple localized systems simultaneously:
* **Julian Date** (Accurately calculates the historical astronomical day gap)
* **Bangla (Bangladesh 1987–2018 Standard)**
* **Bangla (Bangladesh 2019–Present Standard)**
* **Bangla (India Traditional Standard)**
* **Bangla (India Saha Committee / National Standard)**
* **Day of the week calculation** (Powered by Zeller's Congruence)

### 2. Date Arithmetic (Time Machine)
* **Age / Date Difference Calculator:** Calculate the exact difference between two Gregorian dates in Years, Months, and Days, as well as the total number of days.
* **Add / Subtract Days:** Input a starting date and a number of days (e.g., `+45` or `-30`). The system uses Julian Day Numbers to calculate the exact future or past date across Gregorian and Bangla calendars.

### 3. Full-Year Calendar Generator
Generates clean, properly aligned ASCII monthly calendar grids for a chosen year across four modes:
* **Bangla Year ➔ Bangla Grid** (Using Modern Bangladesh 2019 standards)
* **English Year ➔ Bangla Grid** (Finds the intersecting primary Bangla year)
* **Bangla Year ➔ English Grid** 
* **English Year ➔ English Grid**

## Technical Highlights

* **Absolute Julian Day Number (JDN) Bridge:** All date arithmetic and conversions are routed through the JDN, eliminating floating-point errors and complex leap-year edge cases.
* **Zero External Dependencies:** The core engine uses only Python's standard library (no `pip install` required for the core logic).
* **Mathematical Regional Models:** The India Traditional and Saha standards are handled using precise mathematical year-length models (5 months of 31 days, 7 months of 30 days) to ensure zero drift.
* **Robust Input Validation:** Safely handles invalid dates (like February 30th) and prevents crashes from unexpected text inputs.

## How to Run

1. Ensure you have a modern version of Python installed (Python 3.11 or newer is recommended, as older versions like 3.8 and 3.9 have reached End of Life).
2. Clone the repository or download the `calendar.py` file.
3. Open your terminal or command prompt and run:
```bash
python calendar.py
