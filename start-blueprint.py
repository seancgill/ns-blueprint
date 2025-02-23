import subprocess
import sys

def start_blueprint():
    # Prompt user for environment
    env_choice = input("Is this build for Eval (e) or Prod (p)? ").strip().lower()

    # Check input and call appropriate script
    if env_choice == 'e':
        print("\n=== Starting Eval Build ===")
        subprocess.call([sys.executable, 'eval-main.py'])
    elif env_choice == 'p':
        print("\n=== Starting Prod Build ===")
        subprocess.call([sys.executable, 'prod-main.py'])
    else:
        print("Invalid input. Please enter 'e' for Eval or 'p' for Prod.")
        start_blueprint()  # Restart prompt if invalid input

if __name__ == "__main__":
    start_blueprint()
