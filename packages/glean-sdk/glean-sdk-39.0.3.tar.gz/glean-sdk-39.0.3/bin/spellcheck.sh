#!/bin/bash
# Copied, and modified, from the Rust Cookbook.
# https://github.com/rust-lang-nursery/rust-cookbook/blob/HEAD/ci/spellcheck.sh

# Copyright 2016 The Rust Project Developers. See the COPYRIGHT
# file at the top-level directory of this distribution and at
# http://rust-lang.org/COPYRIGHT.
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

aspell --version

# Checks project markdown files for spell errors

# Notes:

# This script needs dictionary file ($dict_filename) with project-specific
# valid words. If this file is missing, first invocation of a script generates
# a file of words considered typos at the moment. User should remove real typos
# from this file and leave only valid words. When script generates false
# positive after source modification, new valid word should be added
# to dictionary file.

# Default mode of this script is interactive. Each source file is scanned for
# typos. aspell opens window, suggesting fixes for each found typo. Original
# files with errors will be backed up to files with format "filename.md.bak".

# When running in CI, this script should be run in "list" mode (pass "list"
# as first argument). In this mode script scans all files and reports found
# errors. Exit code in this case depends on scan result:
# 1 if any errors found,
# 0 if all is clear.

# Script skips words with length less than or equal to 3. This helps to avoid
# some false positives.

# We can consider skipping source code in markdown files (```code```) to reduce
# rate of false positives, but then we lose ability to detect typos in code
# comments/strings etc.

shopt -s nullglob

dict_filename=./.dictionary
markdown_sources="$(git ls-files | grep -v 'DEPENDENCIES\.md' | grep '\.md$')"
mode="check"
aspell_args="--lang en_US --mode=markdown"

# aspell repeatedly modifies personal dictionary for some purpose,
# so we should use a copy of our dictionary
mkdir -p "/tmp/ci"
dict_path="/tmp/$dict_filename"

if [[ "$1" == "list" ]]; then
    mode="list"
fi

if [[ ! -f "$dict_filename" ]]; then
    # Pre-check mode: generates dictionary of words aspell consider typos.
    # After user validates that this file contains only valid words, we can
    # look for typos using this dictionary and some default aspell dictionary.
    echo "Scanning files to generate dictionary file '$dict_filename'."
    echo "Please check that it doesn't contain any misspellings."

    echo "personal_ws-1.1 en 0 utf-8" > "$dict_filename"
    cat "${markdown_sources}" | aspell ${aspell_args} list | sort -u >> "$dict_filename"
elif [[ "$mode" == "list" ]]; then
    # List (default) mode: scan all files, report errors
    declare -i retval=0

    cp "$dict_filename" "$dict_path"

    if [ ! -f $dict_path ]; then
        retval=1
        exit "$retval"
    fi

    for fname in $markdown_sources; do
        command=$(aspell ${aspell_args} --personal="$dict_path" "$mode" < "$fname")
        if [[ -n "$command" ]]; then
            for error in $command; do
                # FIXME: Find more correct way to get line number
                # (ideally from aspell). Now it can make some false positives,
                # because it is just a grep
                grep --with-filename --line-number -o --color=always "$error" "$fname"
            done
            retval=1
        fi
    done
    exit "$retval"
elif [[ "$mode" == "check" ]]; then
    for fname in $markdown_sources; do
        aspell --mode=markdown ${aspell_args} --dont-backup --personal="$dict_filename" "$mode" "$fname"
    done
fi
