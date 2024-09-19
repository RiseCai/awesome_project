#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import re
from datetime import datetime

def generate_feature_id(project_code, branch_code):
    features_dir = os.path.join('docs', 'docs', 'features')
    if not os.path.exists(features_dir):
        os.makedirs(features_dir)
    
    existing_features = [f for f in os.listdir(features_dir) if f.endswith('.md')]
    
    year = datetime.now().strftime('%y')
    
    # Find the maximum sequence number for the current year
    max_sequence = 0
    pattern = r"{0}-{1}-F{2}(\d{{5}})".format(re.escape(project_code), re.escape(branch_code), year)
    for feature in existing_features:
        match = re.match(pattern, feature)
        if match:
            sequence = int(match.group(1))
            max_sequence = max(max_sequence, sequence)
    
    new_sequence = max_sequence + 1
    return "{0}-{1}-F{2}{3:05d}".format(project_code, branch_code, year, new_sequence)

def create_feature(project_code, branch_code, title, description):
    features_dir = os.path.join('docs', 'docs', 'features')
    if not os.path.exists(features_dir):
        os.makedirs(features_dir)

    new_id = generate_feature_id(project_code, branch_code)

    content = """# {0}: {1}

## Description
{2}

## Status
- [ ] To Do
- [ ] In Progress
- [ ] Done

## Created
{3}

## Updated
{3}

## Progress
- {4}: Feature created
""".format(new_id, title, description, 
           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
           datetime.now().strftime('%Y-%m-%d'))

    file_name = "{0}_{1}.md".format(new_id, title.lower().replace(' ', '_'))
    file_path = os.path.join(features_dir, file_name)

    with open(file_path, 'w') as f:
        f.write(content)

    print("Created new feature: {0}".format(file_path))

if __name__ == "__main__":
    if len(sys.argv) < 6 or sys.argv[1] != "create" or sys.argv[2] != "feature":
        print("Usage: python doc_manager.py create feature <project_code> <branch_code> <title> <description>")
        sys.exit(1)

    _, _, _, project_code, branch_code, title = sys.argv[:6]
    description = " ".join(sys.argv[6:])
    create_feature(project_code, branch_code, title, description)