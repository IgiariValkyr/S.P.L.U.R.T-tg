import os
import re
import sys

define_regex = re.compile(r"(\s+)?#define\s?([A-Z0-9_]+)\(?(.+)\)?")

def green(text):
	return "\033[32m" + str(text) + "\033[0m"

def red(text):
	return "\033[31m" + str(text) + "\033[0m"

# simple way to check if we're running on github actions, or on a local machine
on_github = os.getenv("GITHUB_ACTIONS") == "true"

defines_file = "code/__DEFINES/traits/declarations.dm"
skyrat_defines_file = "code/__DEFINES/~skyrat_defines/traits/declarations.dm" # SKYRAT EDIT ADDITION
bubber_defines_file = "code/__DEFINES/~~bubber_defines/traits/declarations.dm" # BUBBER EDIT ADDITION
splurt_defines_file = "code/__DEFINES/~~~splurt_defines/traits/declarations.dm" # SPLURT EDIT ADDITION
globalvars_file = "code/_globalvars/traits/_traits.dm"

how_to_fix_message = f"Please ensure that all traits in the {defines_file} file are added in the {globalvars_file} file."

def post_error(define_name):
	if on_github:
		print(f"::error file={defines_file},title=Define Sanity::{define_name} is defined in {defines_file} but not added to {globalvars_file}!")
	else:
		print(red(f"- Failure: {define_name} is defined in {defines_file} but not added to {globalvars_file}!"))

number_of_defines = 0

if not os.path.isfile(defines_file):
	print(red(f"Could not find the defines file '{defines_file}'!"))
	sys.exit(1)

# SKYRAT EDIT ADDITION START
if not os.path.isfile(skyrat_defines_file):
	print(red(f"Could not find the skyrat defines file '{skyrat_defines_file}'!"))
	sys.exit(1)
# SKYRAT EDIT ADDITION END

# BUBBER EDIT ADDITION START
if not os.path.isfile(bubber_defines_file):
	print(red(f"Could not find the bubber defines file '{bubber_defines_file}'!"))
	sys.exit(1)
# BUBBER EDIT ADDITION END

# SPLURT EDIT ADDITION START
if not os.path.isfile(splurt_defines_file):
	print(red(f"Could not find the splurt defines file '{splurt_defines_file}'!"))
	sys.exit(1)
# SPLURT EDIT ADDITION END

if not os.path.isfile(globalvars_file):
	print(red(f"Could not find the globalvars file '{globalvars_file}'!"))
	sys.exit(1)

defines_to_search_for = []
missing_defines = []
scannable_lines = []

with open(defines_file, 'r') as file:
	reading = False

	for line in file:
		line = line.strip()

		if line == "// BEGIN TRAIT DEFINES":
			reading = True
			continue
		elif line == "// END TRAIT DEFINES":
			break
		elif not reading:
			continue

		scannable_lines.append(line)

for potential_define in scannable_lines:
	match = define_regex.match(potential_define)
	if not match:
		continue

	number_of_defines += 1
	defines_to_search_for.append(match.group(2))

# SKYRAT EDIT ADDITION START
scannable_lines = []
with open(skyrat_defines_file, 'r') as file:
	reading = False

	for line in file:
		line = line.strip()

		if line == "// BEGIN TRAIT DEFINES":
			reading = True
			continue
		elif line == "// END TRAIT DEFINES":
			break
		elif not reading:
			continue

		scannable_lines.append(line)

for potential_define in scannable_lines:
	match = define_regex.match(potential_define)
	if not match:
		continue

	number_of_defines += 1
	defines_to_search_for.append(match.group(2))
# SKYRAT EDIT ADDITION END

# BUBBER EDIT ADDITION START
scannable_lines = []
with open(bubber_defines_file, 'r') as file:
	reading = False

	for line in file:
		line = line.strip()

		if line == "// BEGIN TRAIT DEFINES":
			reading = True
			continue
		elif line == "// END TRAIT DEFINES":
			break
		elif "//" in line or "#define" not in line:
			continue
		elif not reading:
			continue

		scannable_lines.append(line)

for potential_define in scannable_lines:
	match = define_regex.match(potential_define)
	if not match:
		continue

	number_of_defines += 1
	defines_to_search_for.append(match.group(2))
# BUBBER EDIT ADDITION END

# SPLURT EDIT ADDITION START
scannable_lines = []
with open(splurt_defines_file, 'r') as file:
	reading = False

	for line in file:
		line = line.strip()

		if line == "// BEGIN TRAIT DEFINES":
			reading = True
			continue
		elif line == "// END TRAIT DEFINES":
			break
		elif not reading:
			continue

		scannable_lines.append(line)

for potential_define in scannable_lines:
	match = define_regex.match(potential_define)
	if not match:
		continue

	number_of_defines += 1
	defines_to_search_for.append(match.group(2))
# SPLURT EDIT ADDITION END

if number_of_defines == 0:
	print(red("No defines found! This is likely an error."))
	sys.exit(1)

if number_of_defines <= 450:
	print(red(f"Only found {number_of_defines} defines! Something has likely gone wrong as the number of global traits should not be this low."))
	sys.exit(1)

with open(globalvars_file, "r") as file:
	globalvars_file_contents = file.read()
	for define_name in defines_to_search_for:
		searchable_string = "\"" + define_name + "\" = " + define_name
		if not re.search(searchable_string, globalvars_file_contents):
			missing_defines.append(define_name)

if len(missing_defines):
	for missing_define in missing_defines:
		post_error(missing_define)

	print(red(how_to_fix_message))
	sys.exit(1)

else:
	print(green(f"All traits were found in both files! (found {number_of_defines} defines)"))
