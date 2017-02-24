from logger_cjl.Logger import Logger
import sys

# All of the configuration below can optionally be
# added as arguments to the Logger constructor
logger = Logger()

print 'This should be displayed normally'
sys.stderr.write("This is a message to stderr\n")

# Write stdout and stderr to file
logger.file_for_stdout = 'stdout.txt'
logger.file_for_stderr = 'stderr.txt'

# Don't append stdout to a file (i.e. replace the file if it already exists)
logger.append_to_stdout_file = False

# don't display stdout to the screen
logger.echo_stdout = False

# do display stderr to the screen.  (Default behavior)
logger.echo_stderr= True

# capture stdout and put it in a buffer
logger.store_stdout = True

print 'Still printing normally, about to activate the Logger'

logger.begin_capture()

print 'This should end up in stdout.txt but should not be displayed to the screen'
sys.stderr.write('This should end up in stderr.txt as well as on the screen\n')

logger.end_capture()

print 'The following things were written to stdout and stored in a buffer.  Here is what is in that buffer:'

# this is not possible without the line 'logger.store_stdout = True'
for line in logger.stdout_data:
    print line