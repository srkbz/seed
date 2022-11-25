#!/usr/bin/env python3
import subprocess
import xml.etree.ElementTree as ET

def main():
    data = get_data("example/db.kdbx", "1234")
    print(get_value(data, "Key A", "attribute"))

def get_data(database, password):
    args = ["keepassxc-cli", "export", "--format", "xml", database]
    cmd = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = cmd.communicate(input=password)
    code = cmd.wait()
    if code != 0:
        print(f"Command finished with exit code {code}:")
        print(stderr)
        exit(code)
    return ET.fromstring(stdout)

def get_value(data, entry, attribute):
    return data.find(f'./Root/Group/Entry/String[Key="Title"][Value="{entry}"]/../String[Key="{attribute}"]/Value').text

main()
