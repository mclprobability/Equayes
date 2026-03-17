import os
import shutil
import subprocess
import sys


def main():
    required_packages = ["setuptools", "build", "twine"]
    missing_packages = [pkg for pkg in required_packages if not is_package_installed(pkg)]

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Please install the missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)

    clean_dist_directory()

    try:
        subprocess.run([sys.executable, "-m", "build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error on building the package: {e}")
        sys.exit(1)

    print("Package built successfully.")


def clean_dist_directory():
    dist_path = os.path.join(os.getcwd(), "dist")

    if os.path.exists(dist_path):
        print("Cleaning dist/ folder...")
        shutil.rmtree(dist_path)

    os.makedirs(dist_path, exist_ok=True)


def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    main()
