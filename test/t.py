import subprocess

condition = True  # Example condition

if condition:
    # Run another Python file
    subprocess.run(['python', 'test/r.py'])
else:
    print("Condition not met.")