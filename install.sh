#!/usr/bin/bash

# Install the package in editable mode
pipx install --editable .

# Initialize a variable to track the current section (prod or dev)
current_section="prod"

# Read through the requirements.txt file
while read -r line; do
  # Skip comment lines and empty lines
  if [[ $line =~ ^# ]]; then
    # Check for section headers and update the current section
    if [[ $line =~ "# Production dependencies" ]]; then
      current_section="prod"
    elif [[ $line =~ "# Development dependencies" ]]; then
      current_section="dev"
    fi
    continue
  fi

  # If the line is not a comment or empty, inject the dependency based on the section
  if [[ -n $line ]]; then
    if [[ $current_section == "prod" ]]; then
      pipx inject pyscaffold "$line"
    elif [[ $current_section == "dev" ]]; then
      pipx inject pyscaffold "$line"
    fi
  fi
done < requirements.txt