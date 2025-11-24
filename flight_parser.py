import json
import csv
from datetime import datetime

# File configuration
INPUT_FILE = 'db.csv'
OUTPUT_JSON = 'db.json'
OUTPUT_ERRORS = 'errors.txt'

def is_valid_datetime(date_str):
    """Helper to check if string is valid YYYY-MM-DD HH:MM"""
    try:
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return dt_obj
    except ValueError:
        return None

def validate_row(row):
    """
    Validates a single row of data based on the assignment rules.
    Returns: (is_valid, result_data_or_error_messages)
    """

    # 1. Check for missing fields
    if len(row) != 6:
        return False, ["missing required fields or formatting error"]

    # Unpack data
    flight_id, origin, dest, dep_str, arr_str, price_str = [x.strip() for x in row]
    error_messages = []

    # 2. Validate Flight ID (2-8 alphanumeric characters)
    if not (flight_id.isalnum() and 2 <= len(flight_id) <= 8):
        error_messages.append(f"flight_id too long or invalid chars (must be 2-8 alnum)")

    # 3. Validate Origin (3 uppercase letters)
    if not (len(origin) == 3 and origin.isupper() and origin.isalpha()):
        error_messages.append("invalid origin code")

    # 4. Validate Destination (3 uppercase letters)
    if not (len(dest) == 3 and dest.isupper() and dest.isalpha()):
        error_messages.append("invalid destination code")
        # Special case from example: check if destination is empty string handled by length check

    # 5. Validate Datetimes
    dep_dt = is_valid_datetime(dep_str)
    arr_dt = is_valid_datetime(arr_str)

    if not dep_dt:
        error_messages.append("invalid departure datetime")

    if not arr_dt:
        error_messages.append("invalid arrival datetime")

    # 6. Logical Check: Arrival must be after Departure
    if dep_dt and arr_dt:
        if arr_dt <= dep_dt:
            error_messages.append("arrival before departure")

    # 7. Validate Price (Positive float number)
    try:
        price = float(price_str)
        if price <= 0:
            error_messages.append("negative price value")
    except ValueError:
        error_messages.append("invalid price format")

    # Return result
    if error_messages:
        return False, error_messages
    else:
        # Create clean dictionary for JSON
        flight_obj = {
            "flight_id": flight_id,
            "origin": origin,
            "destination": dest,
            "departure_datetime": dep_str,
            "arrival_datetime": arr_str,
            "price": price
        }
        return True, flight_obj

def main():
    valid_flights = []
    error_logs = []

    print(f"Reading from {INPUT_FILE}...")

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Could not find {INPUT_FILE}. Please make sure the file exists.")
        return

    header_skipped = False

    for i, line in enumerate(lines):
        line_num = i + 1
        clean_line = line.strip()

        # Skip completely empty lines
        if not clean_line:
            continue

        # Handle Comment Lines
        if clean_line.startswith("#"):
            error_logs.append(f"Line {line_num}: {clean_line} -> comment line, ignored for data parsing")
            continue

        # Skip Header (Standard CSV header check)
        if not header_skipped and clean_line.startswith("flight_id"):
            header_skipped = True
            continue

        # Split the CSV line
        parts = clean_line.split(',')

        # Perform Validation
        is_valid, result = validate_row(parts)

        if is_valid:
            # result is the flight dictionary
            valid_flights.append(result)
        else:
            # result is a list of error strings
            # Join errors with commas if multiple exist
            error_reason = ", ".join(result)
            error_logs.append(f"Line {line_num}: {clean_line} -> {error_reason}")

    # --- Write Outputs ---

    # Write Valid Flights to JSON
    try:
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(valid_flights, json_file, indent=4)
        print(f"Successfully wrote {len(valid_flights)} valid flights to {OUTPUT_JSON}")
    except IOError as e:
        print(f"Error writing JSON: {e}")

    # Write Errors to TXT
    try:
        with open(OUTPUT_ERRORS, 'w', encoding='utf-8') as txt_file:
            for log in error_logs:
                txt_file.write(log + "\n")
        print(f"Successfully wrote {len(error_logs)} log lines to {OUTPUT_ERRORS}")
    except IOError as e:
        print(f"Error writing error log: {e}")

# --- Helper to Create Dummy Data (For testing) ---
def create_sample_csv():
    content = """flight_id,origin,destination,departure_datetime,arrival_datetime,price
# === Valid flights ===
BA2490,LHR,JFK,2025-11-14 10:30,2025-11-14 13:05,489.99
LH172,FRA,RIX,2025-11-12 07:15,2025-11-12 10:30,159.50
FR1234,RIX,OSL,2025-11-15 08:00,2025-11-15 08:55,99.99
BT102,RIX,HEL,2025-11-14 09:40,2025-11-14 10:25,120.00
AA9999,JFK,LHR,2025-11-15 20:15,2025-11-16 08:10,550.00
DY4501,OSL,ARN,2025-12-01 06:00,2025-12-01 07:10,75.00
AF112,CDG,DXB,2025-11-20 21:10,2025-11-21 05:45,620.00

# === Invalid flights (for testing validation) ===
BADLINE,NO_DATE,NO_TIME
BA_BAD,RIX,LON,2025-11-15 11:00,INVALID_DATE,250.00
SK404,OSL,RIX,2025-11-15 14:00,2025-11-15 12:00,120.00
W61025,XXX,RIX,2025-11-16 11:00,2025-11-16 13:00,80.00
QR1,DOH,SYD,INVALID_DATETIME,2025-11-17 23:30,980.00
KL1999,AMS,,2025-11-14 09:00,2025-11-14 11:15,180.00
AY503,HEL,RIX,2025-11-15 13:20,2025-11-15 14:15,-10.00
LH999999999,FRA,LAX,2025-11-13 09:30,2025-11-13 18:10,700.00
SN2902,BRU,LHR,2025-13-40 10:00,2025-13-40 12:00,99.99"""
    with open('db.csv', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created sample 'db.csv' file for testing.\n")

if __name__ == "__main__":
    # Check if file exists, if not create it
    try:
        with open(INPUT_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        create_sample_csv()

    main()