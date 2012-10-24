
CPPLINT_ARGUMENTS = ''.join([
    '--filter=-legal,',
    '-readability/streams,',
    '-whitespace/newline,',
    '-readability/constructors,',
    '-runtime/arrays,',
    '-build/namespaces,',
    '-runtime/string,',
    '-readability/casting,',
    '-runtime/references,',
    '-readability/streams,',
    '-whitespace/labels,',
    '-readability/todo,',
    '-runtime/threadsafe_fn,',
    '-readability/header_guard,',
    '-whitespace/braces_google,',
    '-build/include_directory -',
])

BRACE_VERIFY_ENABLED = False