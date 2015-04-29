

import subprocess

verbose_level = 0

VERBOSE_LEVELS = {'DEBUG' : 1,
                  'INFO'  : 2,
                  'WARN'  : 3,
                  'ERROR' : 4,
                  'FATAL' : 5}


def verbose_level( new_level ):

    new_level = new_level.upper()

    if ( new_level in VERBOSE_LEVELS ):
        verbose_level = new_level
    else:
        print "Unknown verbosity level: " new_level


    

#------------------------------------------------------------
# Make system call fucntion that checks if the function exited correctly

def system_call( step_name, cmd ):

    try:
        subprocess.check_call(cmd, shell=True)

    except subprocess.CalledProcessError as scall:
        if ( VERBOSE == "DEBUG"):
            print "Script failed at %s stage - exit code was %s, ouput = %s" % (step_name, scall.returncode, scall.output) 

        if ( VERBOSE == "INFO"):
            print "Script failed at %s stage - exit code was %s" % (step_name, scall.returncode)
        exit()
