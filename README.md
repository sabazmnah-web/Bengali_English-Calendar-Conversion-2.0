# Bengali_English-Calendar-Conversion-2.0 (Bengali-English Universal Calendar System)

A comprehensive Python-based calendar conversion engine designed to handle complex conversions, date arithmetic, seasonal metadata, and full-year grid generations across multiple historical and regional calendar systems.

## Features

### 1. Date Conversion Matrix (Gregorian ↔ Bangla)
Input any standard Gregorian date or Bangla date to view its exact equivalent across multiple localized systems simultaneously:
* **Julian Date** (Accurately calculates the historical astronomical day gap)
* **Bangla (Bangladesh 1987–2018 Standard)**
* **Bangla (Bangladesh 2019–Present Standard)** — incorporating updated reforms where the first 6 months have 31 days (including Ashshin)[cite: 1]
* **Bangla (India Traditional Standard)**
* **Bangla (India Saha Committee / National Standard)**
* **Day of the week calculation** (Powered by Zeller's Congruence)

### 2. Date Arithmetic & Metadata
* **Age / Date Difference Calculator:** Calculate the exact difference between two Gregorian dates in Years, Months, and Days, as well as the total number of days.
* **Add / Subtract Days:** Input a starting date and a number of days (e.g., `+45` or `-30`). The system uses Julian Day Numbers to calculate the exact future or past date across Gregorian and Bangla calendars.
* **Seasonal Tracking:** Automatically maps months to traditional Bengali seasons (`Grishshô`, `Bôrsha`, `Shôrôd`, `Hemonto`, `Sheet`, and `Bôsôntô`).

### 3. Full-Year Calendar Generator
Generates clean, properly aligned ASCII monthly calendar grids for a chosen year across four modes:
* **Bangla Year ➔ Bangla Grid** (Using Modern Bangladesh 2019 standards with seasonal breakdowns)
* **English Year ➔ Bangla Grid** (Finds the intersecting primary Bangla year)
* **Bangla Year ➔ English Grid** 
* **English Year ➔ English Grid**

## Technical Highlights

* **Absolute Julian Day Number (JDN) Bridge:** All date arithmetic and conversions are routed through the JDN, eliminating floating-point errors and complex leap-year edge cases.
* **Zero External Dependencies:** Built entirely using Python's standard library requiring zero external package installations.
* **Mathematical Regional Models:** The India Traditional and Saha standards are handled using precise mathematical year-length models to ensure zero drift.
* **Robust Input Validation:** Safely handles invalid dates and prevents crashes from unexpected text inputs.

## How to Run

Execute the script directly via your terminal to access the interactive CLI menu:

```bash
python Bengali_English-Calendar-Conversion.py
