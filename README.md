lint183
=======

Trivially simple web-based service for running Google's cpplint on uploaded code. We made some changes to the cpplint script (eg, errors to stderr) and a very simple HTML formatter that marks areas for improvement.

This web service is set up to run its components as plugins. To run a plugin, add a line with the command to run to cpplint/plugins.conf. Plugins should accept the C++ code on stdin and output
comments to stdout one per line. Each line either blank or FILENAME:LINENO:Comment. Plugins are
executed in a bash shell with the project root directory as the working directory. Pipes and such are allowed; as are simple bash commands.

To change cpplint flags: edit `  lint183/CPPLINT_COMMANDLINE `
