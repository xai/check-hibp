#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Olaf Lessenich <xai@linux.com>
#
# Distributed under terms of the MIT license.


import argparse
import hashlib
import getpass
import io
import re
import sys
import mmap


def grep(pattern, filename):
    with io.open(filename, "r", encoding="utf-8") as f:
        return re.search(pattern, mmap.mmap(f.fileno(), 0,
                                            access=mmap.ACCESS_READ))


def query(filename, passwords, quiet):
    found = 0

    for p in passwords:
        h = hashlib.sha1(p.encode()).hexdigest().upper()
        if not quiet:
            print("sha1(%s) = %s" % (len(p) * '*', h))
        if grep(h.encode("utf-8"), filename):
            print('Password found: %s (%s)' % (p, h))
            found += 1

    print()
    print("%d out of %d passwords found." % (found, len(passwords)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file",
                        help="File containing hashes "
                        "that will be used for searching. "
                        "This can be retrieved from "
                        "https://haveibeenpwned.com.",
                        type=str,
                        required=True)
    parser.add_argument("-i",
                        "--interactive",
                        help="Interactive mode. "
                        "You will be prompted to enter a password.",
                        action="store_true")
    parser.add_argument("-q",
                        "--quiet",
                        help="Quiet mode. "
                        "Print only found passwords and summary.",
                        action="store_true")
    args = parser.parse_args()

    passwords = []
    if not args.interactive:
        for line in iter(sys.stdin.readline, ''):
            passwords.append(line.strip())

    if not passwords:
        print("Enter password that you want to check (won't be shown)!")
        passwords = (getpass.getpass(),)

    query(args.file, passwords, args.quiet)


if __name__ == "__main__":
    main()
