import shutil
import sys
import os

def check_disk_usage(disk, threshold=80):
    """Checks if the disk usage is above a certain percentage threshold."""
    # Get total, used, and free bytes
    total, used, free = shutil.disk_usage(disk)
    
    # Calculate percentage
    used_percentage = (used / total) * 100
    
    print(f"Current disk usage for '{disk}': {used_percentage:.2f}%")
    
    if used_percentage > threshold:
        print(f"⚠️ ALERT: Disk usage has crossed the {threshold}% threshold!")
        # Trigger an alert action here (e.g., call a Slack Webhook or send an email)
        return False
        
    print("✅ Disk usage is within safe limits.")
    return True

if __name__ == "__main__":
    # Monitor the root directory (adjust for Windows, e.g., 'C:\\')
    target_disk = "/"
    
    # Exit with code 1 if the disk is dangerously full (useful for CI/CD gates or cron jobs)
    if not check_disk_usage(target_disk, threshold=85):
        sys.exit(1)
