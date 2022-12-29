# Liner

### Usage: 
liner [-options] [file...]

### Description:
  **Liner** - Lines counter. Counts amount lines in files and their size

### Options:
    -e   Will only shows files with the specified extensions
    -x   Exclude the specified files and dirs
    -r   Recursive scan dirs
    -f   File size in human-readable format
    -h   Help

### Examples:
  ```liner -e ".py .js" -x "venv/ node_modules/" -rf example_dir/``` - Will show all javascript and python files exclude dir node_modules and venv <br>
  ```liner -r example_dir/``` - Will show all files in the example_dir<br>
  ```liner -rf example_dir/``` - You can add -f flag for human-readable format<br>

### Noticed:
  _If you used flags -x[exclude] or -e[extensions] your should specify a value!<br>_
  _If it is list of values you must used quotes!'<br>_