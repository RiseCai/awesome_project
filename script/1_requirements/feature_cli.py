#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import argparse
from datetime import datetime

FEATURES_DIR = os.path.join('docs', 'docs', 'features')

def get_feature_status(content):
    for line in content.split('\n'):
        if line.strip().startswith('- [x]'):
            return line.strip()[5:]
    return "To Do"

def list_features():
    print("Looking for features in: {0}".format(FEATURES_DIR))
    features = [f for f in os.listdir(FEATURES_DIR) if f.endswith('.md')]
    print("Found {0} feature files".format(len(features)))
    print("\nID                  | Status       | Title")
    print("--------------------|--------------|------------------------")
    for feature in sorted(features):
        with open(os.path.join(FEATURES_DIR, feature), 'r') as f:
            content = f.read()
            first_line = content.split('\n')[0]
            feature_id = first_line.split(':')[0].strip('# ')
            title = first_line.split(':')[1].strip()
            status = get_feature_status(content)
            print("{0:<20} | {1:<12} | {2}".format(feature_id, status, title[:30]))

def show_feature(feature_id):
    feature_file = find_feature_file(feature_id)
    if feature_file:
        with open(os.path.join(FEATURES_DIR, feature_file), 'r') as f:
            print(f.read())
    else:
        print("Feature {0} not found.".format(feature_id))

def update_feature_status(feature_id, new_status):
    feature_file = find_feature_file(feature_id)
    if not feature_file:
        print("Feature {0} not found.".format(feature_id))
        return

    file_path = os.path.join(FEATURES_DIR, feature_file)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('- ['):
            lines[i] = line.replace('x', ' ')
        if line.strip().startswith('- [ ] {0}'.format(new_status)):
            lines[i] = line.replace('[ ]', '[x]')

    with open(file_path, 'w') as f:
        f.writelines(lines)

    print("Updated status of feature {0} to {1}".format(feature_id, new_status))

def add_progress(feature_id, progress_note):
    feature_file = find_feature_file(feature_id)
    if not feature_file:
        print("Feature {0} not found.".format(feature_id))
        return

    file_path = os.path.join(FEATURES_DIR, feature_file)
    with open(file_path, 'r') as f:
        content = f.read()

    progress_entry = "- {0}: {1}\n".format(datetime.now().strftime('%Y-%m-%d'), progress_note)
    
    if "## Progress" in content:
        content = content.replace("## Progress\n", "## Progress\n{0}".format(progress_entry))
    else:
        content += "\n## Progress\n{0}".format(progress_entry)

    with open(file_path, 'w') as f:
        f.write(content)

    print("Added progress note to feature {0}".format(feature_id))

def find_feature_file(feature_id):
    for filename in os.listdir(FEATURES_DIR):
        if filename.startswith(feature_id) and filename.endswith('.md'):
            return filename
    return None

def main():
    parser = argparse.ArgumentParser(description="Feature CLI for managing features")
    parser.add_argument("action", choices=["list", "show", "update", "add-progress"], help="Action to perform")
    parser.add_argument("--id", help="Feature ID for show, update, and add-progress actions")
    parser.add_argument("--status", choices=["To Do", "In Progress", "Done"], help="New status for update action")
    parser.add_argument("--note", help="Progress note for add-progress action")

    args = parser.parse_args()

    if args.action == "list":
        list_features()
    elif args.action == "show":
        if not args.id:
            print("Error: --id is required for show action")
            sys.exit(1)
        show_feature(args.id)
    elif args.action == "update":
        if not args.id or not args.status:
            print("Error: --id and --status are required for update action")
            sys.exit(1)
        update_feature_status(args.id, args.status)
    elif args.action == "add-progress":
        if not args.id or