import subprocess
import sys

# Command to run the Node.js script
# Make sure 'node' is in your system's PATH (which it should be after installation)
# Arguments are passed as elements in the list
command = ["node", "test1.js", "an_argument_value"]

try:
    # Run the command and capture the output
    # 'text=True' ensures output is a string, not bytes
    # 'capture_output=True' captures stdout and stderr
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print the output from the Node.js script
    print("Output from Node.js script:")
    print(result.stdout)
    
    # Check for any errors
    if result.stderr:
        print("Errors from Node.js script:")
        print(result.stderr)

except subprocess.CalledProcessError as e:
    print(f"Node.js script failed with exit code {e.returncode}")
    print(e.stderr)
except FileNotFoundError:
    print("Error: 'node' command not found. Make sure Node.js is installed and in your system's PATH.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")