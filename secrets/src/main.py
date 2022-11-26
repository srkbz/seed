#!/usr/bin/env python3
import os
import csv
import subprocess
import xml.etree.ElementTree as ET
import urllib.request


def main():
    download_database()
    tree = export_database()
    with open("/servitor/secrets/input") as input_file:
        input_tsv = csv.reader(input_file, delimiter='\t')
        for line in input_tsv:
            if len(line) == 0: continue

            key, path = line
            entry, attribute = path.split(':')

            value = get_value(tree, entry, attribute)
            with open("/servitor/secrets/output/" + key, "w") as output_file:
                output_file.write(value)


def download_database():
    print("=== Downloading database... ", end='')
    urllib.request.urlretrieve(os.environ['DATABASE_URL'], "db.kdbx")
    print("OK")


def export_database():
    print("=== Exporting database... ", end='')
    args = ["keepassxc-cli", "export", "--format", "xml", "db.kdbx"]
    cmd = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)
    stdout, stderr = cmd.communicate(input=os.environ['DATABASE_PASSWORD'])
    code = cmd.wait()
    if code != 0:
        print(f"Command finished with exit code {code}:")
        print(stderr)
        exit(code)
    print("OK")
    return ET.fromstring(stdout)


def get_value(data, entry, attribute):
    return data.find(f'./Root/Group/Entry/String[Key="Title"][Value="{entry}"]/../String[Key="{attribute}"]/Value').text


main()
