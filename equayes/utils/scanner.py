import argparse
import os
import re
import sys
from collections import defaultdict

import requests

# Global error log
error_log = defaultdict(list)


def clean_requirements(file_path):
    """
    Liest die requirements.txt-Datei, entfernt Header-Zeilen und gibt eine Liste von Paketen mit ihren Versionen zurück.
    """
    packages = []
    with open(file_path, "r") as file:
        for line in file:
            # Überspringe Header-Zeilen
            if line.startswith("Package") or line.startswith("---"):
                continue
            # Extrahiere Paketname und -version
            match = re.match(r"(\S+)\s+(\S+)", line)
            if match:
                package_name = match.group(1)
                package_version = match.group(2)
                packages.append(f"{package_name} {package_version}")
    return packages


ca_bundle_path = "/usr/local/share/ca-certificates/ca.crt"
import requests


def fetch_package_info(package_name, package_version):
    try:
        base_url = "https://api.deps.dev/v3/systems/pypi/packages/"
        url = f"{base_url}{package_name}/versions/{package_version}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        error_log["HTTPError"].append(f"HTTP-Fehler bei {package_name} {package_version}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        error_log["ConnectionError"].append(f"Verbindungsfehler bei {package_name} {package_version}: {conn_err}")
    except Exception as err:
        error_log["GeneralError"].append(f"Fehler bei {package_name} {package_version}: {err}")
    return None


def fetch_dependencies(package_name, package_version):
    try:
        base_url = "https://api.deps.dev/v3/systems/pypi/packages/"
        url = f"{base_url}{package_name}/versions/{package_version}:dependencies"
        response = requests.get(url)
        response.raise_for_status()
        dependencies = response.json().get("dependencies", [])

        # Filter out dependencies that start with an underscore
        # These are most likely packages that are needet for the OS
        # have not much to do with our packages or code
        filtered_dependencies = [dep for dep in dependencies if not dep["package"].get("name", "").startswith("_")]

        return filtered_dependencies
    except requests.exceptions.HTTPError as http_err:
        error_log["HTTPError"].append(
            f"HTTP error occurred when fetching dependencies for {package_name} {package_version}: {http_err}"
        )
    except requests.exceptions.ConnectionError as conn_err:
        error_log["ConnectionError"].append(
            f"Connection error occurred when fetching dependencies for {package_name} {package_version}: {conn_err}"
        )
    except Exception as err:
        error_log["GeneralError"].append(
            f"Error occurred when fetching dependencies for {package_name} {package_version}: {err}"
        )
    return []


def extract_licenses(package_info):
    try:
        licenses = package_info.get("licenses", [])
        return licenses if licenses else ["unknown"]
    except Exception as err:
        error_log["GeneralError"].append(f"Error occurred when extracting licenses: {err}")
        return ["unknown"]


def fetch_advisory_details(advisory_id):
    try:
        url = f"https://api.deps.dev/v3/advisories/{advisory_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        error_log["HTTPError"].append(f"HTTP error occurred when fetching advisory details for {advisory_id}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        error_log["ConnectionError"].append(
            f"Connection error occurred when fetching advisory details for {advisory_id}: {conn_err}"
        )
    except Exception as err:
        error_log["GeneralError"].append(f"Error occurred when fetching advisory details for {advisory_id}: {err}")
    return None


def process_packages(package_list):
    all_licenses = {}
    all_advisories = {}
    max = len(package_list)
    tmp = 0
    for package in package_list:
        tmp += 1
        try:
            package_name, package_version = package.split()

            package_info = fetch_package_info(package_name, package_version)
            if package_info:
                licenses = extract_licenses(package_info)
                all_licenses[(package_name, package_version)] = licenses

                # Extract the actual advisory IDs
                advisory_keys = package_info.get("advisoryKeys", [])
                for advisory in advisory_keys:
                    advisory_id = advisory.get("id")  # Only the 'id' value is extracted here
                    advisory_info = fetch_advisory_details(advisory_id)
                    if advisory_info:
                        # Add relevant information to the advisory
                        advisory_data = {
                            "package_name": package_name,
                            "description": advisory_info.get("title", "No description"),
                            "severity": advisory_info.get("cvss3Score", "Unknown"),
                            "url": advisory_info.get("url", f"https://api.deps.dev/v3/advisories/{advisory_id}"),
                        }
                        all_advisories[advisory_id] = advisory_data

                # Also process the dependencies
                dependencies = fetch_dependencies(package_name, package_version)
                for dep in dependencies:
                    if dep.get("advisoryKeys"):
                        for advisory in dep["advisoryKeys"]:
                            advisory_id = advisory.get("id")  # Only the 'id' value is extracted here
                            advisory_info = fetch_advisory_details(advisory_id)
                            if advisory_info:
                                # Add relevant information to the advisory
                                advisory_data = {
                                    "package_name": dep["package"]["name"],
                                    "description": advisory_info.get("title", "No description"),
                                    "severity": advisory_info.get("cvss3Score", "Unknown"),
                                    "url": advisory_info.get("url", f"https://api.deps.dev/v3/advisories/{advisory_id}"),
                                }
                                all_advisories[advisory_id] = advisory_data
            else:
                error_log["NoDataFound"].append(f"No data found for package: {package_name} {package_version}")
        except ValueError:
            error_log["ValueError"].append(f"Error processing package: {package}. Ensure it is in 'name version' format.")
        except Exception as err:
            error_log["GeneralError"].append(f"An unexpected error occurred: {err}")
        print(f"({tmp}/{max})")

    return all_licenses, all_advisories


def write_to_html(all_licenses, all_advisories, error_log=None, output_file="reports/deps.html"):
    try:
        with open(output_file, "w") as f:
            f.write("<html><body>")
            f.write("<h1>License and Vulnerability Report</h1>")

            # License table (sorted alphabetically by license names)
            f.write("<h2>Licenses</h2>")
            if all_licenses:
                sorted_licenses = sorted(all_licenses.items(), key=lambda x: x[1])
                f.write('<table border="1" cellpadding="5" cellspacing="0">')
                f.write("<tr><th>#</th><th>Package</th><th>Version</th><th>Licenses</th></tr>")
                for i, ((package, version), licenses) in enumerate(sorted_licenses, start=1):
                    f.write(f"<tr><td>{i}</td><td>{package}</td><td>{version}</td><td>{', '.join(licenses)}</td></tr>")
                f.write("</table>")
            else:
                f.write("<p>No licenses found.</p>")

            # Advisory table (including corresponding package name)
            f.write("<h2>Vulnerability</h2>")
            if all_advisories:
                f.write('<table border="1" cellpadding="5" cellspacing="0">')
                f.write(
                    "<tr><th>#</th><th>Advisory ID</th><th>Package</th><th>Description</th><th>Severity</th><th>Link</th></tr>"
                )
                for i, (advisory_id, details) in enumerate(all_advisories.items(), start=1):
                    description = details.get("description", "No description")
                    severity = details.get("severity", "Unknown")
                    link = details.get("url", f"https://api.deps.dev/v3/advisories/{advisory_id}")
                    package_name = details.get("package_name", "Unknown")
                    f.write(
                        f"<tr><td>{i}</td><td>{advisory_id}</td><td>{package_name}</td><td>{description}</td><td>{severity}</td><td><a href='{link}'>Link</a></td></tr>"
                    )
                f.write("</table>")
            else:
                f.write("<p>No vulnerability found.</p>")

            # Errors and warnings table
            f.write("<h2>Errors and Warnings</h2>")
            if error_log:
                for error_type, messages in error_log.items():
                    f.write(f"<h3>{error_type}</h3>")
                    f.write('<table border="1" cellpadding="5" cellspacing="0">')
                    f.write("<tr><th>#</th><th>Message</th></tr>")
                    for i, message in enumerate(messages, start=1):
                        f.write(f"<tr><td>{i}</td><td>{message}</td></tr>")
                    f.write("</table>")
            else:
                f.write("<p>No errors or warnings.</p>")

            f.write("</body></html>")
        print(f"Output written to {output_file}")
    except Exception as err:
        print(f"Error occurred while writing to HTML file: {err}")


def write_to_markdown(all_licenses, all_advisories, error_log=None, output_file="reports/deps.md"):
    try:
        with open(output_file, "w") as f:
            f.write("# License and Vulnerability Report\n\n")

            # License section (sorted alphabetically by license names)
            f.write("## Licenses\n")
            if all_licenses:
                sorted_licenses = sorted(all_licenses.items(), key=lambda x: x[1])
                f.write("| # | Package | Version | Licenses |\n")
                f.write("|---|---------|---------|----------|\n")
                for i, ((package, version), licenses) in enumerate(sorted_licenses, start=1):
                    f.write(f"| {i} | {package} | {version} | {', '.join(licenses)} |\n")
            else:
                f.write("No licenses found.\n\n")

            # Advisory section (including corresponding package name)
            f.write("## Vulnerabilities\n")
            if all_advisories:
                f.write("| # | Advisory ID | Package | Description | Severity | Link |\n")
                f.write("|---|-------------|---------|-------------|----------|------|\n")
                for i, (advisory_id, details) in enumerate(all_advisories.items(), start=1):
                    description = details.get("description", "No description")
                    severity = details.get("severity", "Unknown")
                    link = details.get("url", f"https://api.deps.dev/v3/advisories/{advisory_id}")
                    package_name = details.get("package_name", "Unknown")
                    f.write(f"| {i} | {advisory_id} | {package_name} | {description} | {severity} | [Link]({link}) |\n")
            else:
                f.write("No vulnerabilities found.\n\n")

            # Errors and warnings section
            f.write("## Errors and Warnings\n")
            if error_log:
                for error_type, messages in error_log.items():
                    f.write(f"### {error_type}\n")
                    f.write("| # | Message |\n")
                    f.write("|---|---------|\n")
                    for i, message in enumerate(messages, start=1):
                        f.write(f"| {i} | {message} |\n")
            else:
                f.write("No errors or warnings.\n")

        print(f"Output written to {output_file}")
    except Exception as err:
        print(f"Error occurred while writing to Markdown file: {err}")


def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Überprüft die erforderlichen Pakete und verarbeitet die requirements.txt-Datei."
    )
    parser.add_argument(
        "requirements",
        type=str,
        nargs="?",
        default="requirements.txt",
        help="Pfad zur requirements.txt-Datei (Standard: 'requirements.txt')",
    )
    args = parser.parse_args()

    required_packages = ["requests", "collections", "sys", "re", "os"]
    missing_packages = [pkg for pkg in required_packages if not is_package_installed(pkg)]

    if missing_packages:
        print(f"Fehlende Pakete: {', '.join(missing_packages)}")
        print("Bitte installieren Sie die fehlenden Pakete mit:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)

    requirements_file = args.requirements
    # Weitere Verarbeitung der requirements_file

    package_list = clean_requirements(requirements_file)
    all_licenses, all_advisories = process_packages(package_list)
    write_to_html(all_licenses, all_advisories, error_log)
    write_to_markdown(all_licenses, all_advisories, error_log)


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
