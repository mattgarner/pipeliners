

import subprocess

verbose_level = 0

VERBOSE_LEVELS = {'DEBUG' : 0,
                  'INFO'  : 1,
                  'WARN'  : 2,
                  'ERROR' : 3,
                  'FATAL' : 4}
REV_VERBOSE_LEVELS = { 0 : 'DEBUG',
                       1 : 'INFO',
                       2 : 'WARN',
                       3 : 'ERROR',
                       4 : 'FATAL' };



def set_verbose_level( new_level ):

    new_level = new_level.upper()

    if ( new_level in VERBOSE_LEVELS ):
        verbose_level = new_level
    else:
        print "Unknown verbosity level: " + new_level


    

def verbose_print( message, level ):

    if (VERBOSE_LEVELS[ level ] > verbose_level):
        return

    print REV_VERBOSE_LEVELS[ verbose_level ] + " :: " + message


    

#------------------------------------------------------------
# Make system call fucntion that checks if the function exited correctly

def system_call( step_name, cmd ):

    verbose_print(cmd, 'DEBUG')

    try:
        subprocess.check_call(cmd, shell=True)

    except subprocess.CalledProcessError as scall:

        verbose_print("Script failed at %s stage - exit code was %s, ouput = %s" % (step_name, scall.returncode, scall.output), 'DEBUG')
        verbose_print("Script failed at %s stage - exit code was %s" % (step_name, scall.returncode), 'INFO')
