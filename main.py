from datetime import datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
from playsound import playsound
import requests
import argparse

appointments_url = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=2&locationId={}&minimum=1"

def check_appointments(loc_id):
    url = appointments_url.format(loc_id)
    appointments = requests.get(url).json()
    return appointments


def parse_timeframe(value):
    """Convert timeframe string (like '24h', '7d', or '3m') to timedelta or relativedelta"""
    try:
        number = int(value[:-1])
        unit = value[-1].lower()
        
        if unit == 'h':
            return timedelta(hours=number)
        elif unit == 'd':
            return timedelta(days=number)
        elif unit == 'm':
            return relativedelta(months=number)
        else:
            raise argparse.ArgumentTypeError("Timeframe must end with 'h' for hours, 'd' for days, or 'm' for months")
    except (ValueError, IndexError):
        raise argparse.ArgumentTypeError("Timeframe must be a number followed by 'h', 'd', or 'm' (e.g., '24h', '7d', or '3m')")

def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD")



def appointment_in_timeframe(now, future_date, appt_datetime):
    if (now <= appt_datetime <= future_date):
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description='Check appointments for nexus')
    parser.add_argument('--locations', '-l', 
                       nargs='+',  # This allows for one or more arguments
                       type=int,   # Convert inputs to integers
                       help='List of location IDs to check',
                       default=[5020])
    parser.add_argument('--sound', '-s',
                       type=str,
                       default='alarm.mp3',
                       help='Path to sound file to play when appointment is found (default: alert.mp3)')
    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument('--timeframe', '-t',
                           type=parse_timeframe,
                           default='6m',
                           help='Timeframe to check appointments (e.g., "24h" for 24 hours, "7d" for 7 days, "3m" for 3 months)')
    
    time_group.add_argument('--date-range', '-d', 
                           nargs=2,
                           type=parse_date,
                           metavar=('START_DATE', 'END_DATE'),
                           help='Specific date range to check (format: YYYY-MM-DD YYYY-MM-DD)')
    parser.add_argument('--interval', '-i',
                       type=int,
                       default=3,
                       help='Check interval in seconds (default: 3)')
    args = parser.parse_args()

    
    now = datetime.now()
    
    if args.date_range:
        start_date = args.date_range[0]
        end_date = args.date_range[1]
        if start_date > end_date:
            print("Start date must be before end date")
            return
        print(f"Using date range: {start_date.date()} to {end_date.date()}")
    else:
        start_date = now
        end_date = now + args.timeframe
        print(f"Using timeframe: {args.timeframe}")
    try:
        while True:
            for location in args.locations:
                appointments = check_appointments(location)
                appt_found = False
                if appointments:
                    appt_datetime = datetime.strptime(appointments[0]['startTimestamp'], '%Y-%m-%dT%H:%M')
                    if start_date <= appt_datetime <= end_date:
                        print(f"""
✨ APPOINTMENT FOUND
Location ID: {location:>6}
Date & Time: {appt_datetime.strftime('%Y-%m-%d %H:%M:%S')}
{'-' * 50}
""")
                        appt_found = True
                        playsound(args.sound)
                if not appt_found:
                    print(f"""
Location ID: {location:>6}
Start Time: {start_date.strftime('%Y-%m-%d %H:%M:%S')}
End Time:   {end_date.strftime('%Y-%m-%d %H:%M:%S')}
Status:     No appointments found
{'-' * 50}
""")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopping appointment checker...")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()