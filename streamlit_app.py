import subprocess

def run_gunicorn():
    command = [
        "gunicorn",            # Gunicorn command             # Number of worker processes
        "-b", "0.0.0.0:8000",  # Bind address and port
        "app:app"             # Name of your Flask app object
    ]
    subprocess.run(command)

if __name__ == "__main__":
    run_gunicorn()
