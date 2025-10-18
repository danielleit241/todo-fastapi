import subprocess
import sys

def run_alembic_upgrade():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Alembic migration successful.")
    else:
        print("Alembic migration failed:")
        print(result.stderr)
        sys.exit(1)

def run_seed():
    result = subprocess.run(
        [sys.executable, "-m", "app.seed"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Seeding completed.")
    else:
        print("Seeding failed:")
        print(result.stderr)
        sys.exit(1)

def run():
    run_alembic_upgrade()
    run_seed()

if __name__ == "__main__":
    run()
