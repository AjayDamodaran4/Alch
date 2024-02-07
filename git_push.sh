#!/bin/bash

# GitHub username
USERNAME="AjayDamodaran4"

# Personal access token
TOKEN="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"

# Add all changes
git add .

# Commit with a message provided as an argument
git commit -m "m"

# Push changes to the remote repository using HTTPS with personal access token
git push https://$USERNAME:$TOKEN@github.com/AjayDamodaran4/Alch.git main

