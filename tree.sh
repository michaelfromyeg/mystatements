# A helper function to generate the tree from the README
# It ignores .gitignore'd files, but it doesn't handle globs (e.g., .pdf, .csv)
# See more https://unix.stackexchange.com/questions/291282/have-tree-hide-gitignored-files

ignored=$(git ls-files -ci --others --directory --exclude-standard)
ignored_filter=$(echo "$ignored" \
                | egrep -v "^#.*$|^[[:space:]]*$" \
                | sed 's~^/~~' \
                | sed 's~/$~~' \
                | tr "\\n" "|")
tree --prune -I ".git|${ignored_filter: : -1}" "$@"