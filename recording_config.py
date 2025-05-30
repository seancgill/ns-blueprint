# Script to calculate number of users supported for call recordings
# Assumes GSM compression at 13 kbps

def get_positive_float(prompt):
    """Helper function to get a positive float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculate_supported_users():
    # Inform user about GSM compression
    print("Note: Call recordings are archived using GSM compression (13 kbps).")

    # Prompt for inputs
    avg_call_length = get_positive_float("Enter the average call length (in minutes): ")
    avg_calls_per_day = get_positive_float("Enter the average number of calls per day per user: ")
    retention_months = get_positive_float("Enter the archival retention duration before purge (in months): ")

    # Constants
    storage_capacities_tb = [2, 3, 4, 5, 6]  # Storage capacities in TB
    gsm_bitrate_kbps = 13  # GSM bitrate in kilobits per second
    bits_per_byte = 8
    kb_per_mb = 1024
    mb_per_gb = 1024
    gb_per_tb = 1000  # Using base-10 as storage is typically marketed
    seconds_per_minute = 60
    days_per_month = 365 / 12  # Approximate days per month (30.4167)

    # Step 1: Calculate storage per call
    bitrate_bytes_per_second = gsm_bitrate_kbps * 1000 / bits_per_byte  # Convert kbps to bytes/s
    call_length_seconds = avg_call_length * seconds_per_minute
    storage_per_call_kb = bitrate_bytes_per_second * call_length_seconds / 1000  # KB per call
    storage_per_call_mb = storage_per_call_kb / kb_per_mb  # MB per call

    # Step 2: Calculate storage per user per day
    storage_per_user_day_mb = storage_per_call_mb * avg_calls_per_day

    # Step 3: Calculate storage per user for retention period
    retention_days = retention_months * days_per_month
    storage_per_user_mb = storage_per_user_day_mb * retention_days
    storage_per_user_gb = storage_per_user_mb / mb_per_gb

    # Step 4: Calculate and print users supported for each storage capacity
    print("\nNumber of users supported for different storage capacities:")
    print("-" * 50)
    for storage_tb in storage_capacities_tb:
        storage_total_gb = storage_tb * gb_per_tb
        num_users = storage_total_gb / storage_per_user_gb
        print(f"With {storage_tb}TB of storage: approximately {int(num_users):,} users")
    print(f"\nEach user averages {avg_calls_per_day:.2f} calls per day, "
          f"each {avg_call_length:.2f} minutes long, "
          f"archived for {retention_months:.2f} months.")

if __name__ == "__main__":
    print("Calculate Users Supported for Call Recording Storage")
    print("-" * 50)
    calculate_supported_users()