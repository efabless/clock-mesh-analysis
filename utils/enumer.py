#!/usr/bin/python3 -B
"""
enumer:
"""

# from __future__ import print_function
# from functools import cmp_to_key
import sys
import os
import shutil
import tempfile
import getopt
import signal
import subprocess

def sigterm_handler(signal, frame):
    print( 'Abnormal EXIT (SIGTERM)' )
    sys.exit(1)
 
def usage(msg=None):
    if msg: print( msg )
    print( """Usage:
  enumer [-v] [-R] [-J <parallelJobs>] [-r <templateRunScript>] [-o <outName>] [-n <firstN>] [-d <runDir>] <templateFile> <configFile>
    -v : verbose
    -R : run all jobs (using xargs -P), requires -r templateRunScript
          Even without this, the base runDir will get a run_all.sh script that can be run to run all jobs.
    -J <N> : run N jobs in parallel, default: count CPUs, 'grep -c ^processeor /proc/cpuinfo'; 0 or 1 to disable
    -r  : optional, customize also this file as executable 'run.sh' in each case-dir
    -o  : override default 'tb.spi' output filename, customized from templateFile, in each case-dir
    -n  : optional, limit to just the first-N enumeratations to create (and run if -R), for quick testing
    -d  : base dir below which to create each numbered case-subdir: 00001, 00002, ...
    <templateFile> : mandatory, path of main netlist input template to specialize for each case
    <configFile>   : mandatory, path of config file declaring placeholder strings and their values to enumerate
          Both templateFile & templateRunScript participate in placeholder substitutions by enumerated values,
          so the script for example can embed (some of them) in per-case raw or log file names, etc.
          The config-file is executable python, but only function one should use is of the form:
              dim("<placeHolder>", ["<value1>", ... , "valueN" ])

          Example configFile line: replace ${CORNER} by three corner string variations in turn:
              dim("${CORNER}", ["tm", "wp", "ws"])

""" )
    sys.exit(1)

verbose = False
allDims = []
cases = []

if (verbose):
    print( "verbose1" )

# config file calls this function directly.
def dim(placeh, values):
    global allDims
    allDims += [ [ placeh, values ] ]

def dimDump():
    for x in allDims:
        print( "dim: placeholder: '%s' and values: '%s'" % (x[0], "' '".join( x[1] )))

def flushStdOutErr():
    sys.stdout.flush()
    sys.stderr.flush()

def perr(msg):
    sys.stdout.flush()
    print(msg, flush=True, file=sys.stderr)

# count number of CPUs available. On error, report error, but survive and return -1.
def countCPU():
    try:
        p = subprocess.run(['/bin/grep', '-c', '^processor', '/proc/cpuinfo'],
			   stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = None, check = True,
                           universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print('enumer: ERROR: running /bin/grep -c /proc/cpuinfo: ' + e.output.decode('utf-8'), flush=True, file=sys.stderr)
        return -1

    if p.stderr: print(p.stderr, flush=True, file=sys.stderr)
    lines = p.stdout.splitlines()
    return int(lines[0])

# chmod a file to add execute perm., only to the extent it is already readable
def chmodPlusX(fname):
    mask = os.stat(fname).st_mode
    # bit-wise And to isolate read-bits; shift-right 2 to exec-bits; Or back onto mask
    mask2 = mask | ((0o444 & mask) >> 2)
    # print( "mode: %o -> %o" % (mask, mask2))
    os.chmod(fname, mask2)
    
def caseDump():
    # headers, the placeholders of each dimension:
    vals = []
    for y in allDims:
        vals += [ y[0] ]
    print("%5s: %s" % ("#", ", ".join(vals)))

    ndx = 0
    for x in cases:
        # print("%5d# %s" % (ndx, ", ".join( map(str, x))))
        vals = []
        for i in range(nbrDim):
            vals += [ allDims[i][1][ x[i] ]]
        print("%5d: %s" % (ndx, ", ".join( map(str, vals))))
        ndx += 1

def dimReplace( lines, digits, nbr, auxMap ):
    tmp = []
    for line in lines:
        for i in range(nbrDim):
            trg = allDims[i][0]
            val = allDims[i][1][ digits[i] ]
            line = line.replace(trg, val)
            # line = line.replace(placeHoldCaseNbr, str(nbr))
        for key in auxMap:
            line = line.replace(key, auxMap[key])

        tmp += [ line ]
    return tmp

# increment the current enumeration set, starting from last/least-significant "digit"
# modifies curDigits in-place. Does not add digits to cases.
# Uses several globals, modifies globals: ...
# If we roll-over most-significant "digit": return False, else True.
def incr():
    global digMax, nbrDim, curDigits
    for i in range(nbrDim-1,-1,-1):
        val = curDigits[i]
        maxv = digMax[i]
        if val == maxv:
            # at max: roll-over to zero AND carry to next more significant digit
            curDigits[i] = 0
            continue
        # increment this digit
        val += 1
        curDigits[i] = val

        # return success
        return True

    # if got here: we carried from most-significant digit: enumeration is done.
    return False

# emulate 'source file' to directly execute code of a config file, that can reference our dim() function
def exec_full(filepath):
    import os
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'))

# main starts here:
def main(argv):

    signal.signal(signal.SIGTERM, sigterm_handler)
	       
    global verbose, allDims, nbrDim
    
    debug = 0
    # debug = 1 # extra print statements, not relevant to the user.
    err = 0
    warn = 0

    # command line args
    runDir = "/tmp"
    outName = "tb.spi"
    outName2 = "run.sh"
    templateFile = ""
    templateScript = ""
    configFile = ""
    firstN = 0
    runAll = False
    nbrJobs = -1

    try:
        myopts, args = getopt.getopt(argv[1:], "hvRJ:n:r:d:o:")
    except getopt.GetoptError as e:
        print (str(e))
        usage()

    for o, a in myopts:
        if o == '-v':
            verbose = True
            print( "mode: verbose")
        elif o == '-R':
            runAll = True
            print( "mode: runAll")
        elif o == '-J':
            nbrJobs = int(a)
            if verbose: print( "nbrJobs: %d" % (nbrJobs))
        elif o == '-d':
            runDir = a
            if verbose: print( "runDir: %s" % (runDir))
        elif o == '-n':
            firstN = int(a)
            if verbose: print( "first-N: %d" % (firstN))
        elif o == '-o':
            outName = a
            if verbose: print( "output-file: %s" % (outName))
        elif o == '-r':
            templateScript = a
            if verbose: print( "template-script: %s" % (templateScript))
        elif o == '-h':
            usage("help:")
        else:
            usage("unknown option: %s" %(o))

    argv = args
    ndx = 0
    argc = len(argv)
    if ndx < argc:
        templateFile = str(argv[ndx])
        ndx += 1
        if verbose: print( "template-file: %s" % (templateFile))

    if ndx < argc:
        configFile = str(argv[ndx])
        ndx += 1
        if verbose: print( "config-file: %s" % (configFile))

    if not configFile:
        usage( 'enumer: ERROR: less than the two mandatory arguments: <templateFile> <configFile>' )

    if ndx < argc:
        usage( 'enumer: ERROR: extra unsupported arguments: ' + " ".join( argv[ndx:]) )

    # read template-file
    try :
        with open(templateFile,'r') as inFile:
            srcLines = inFile.read().splitlines()
    except :
        perr( '%s %s' % ('enumer: ERROR, failed open:', templateFile))
        err += 1

    # verify templateDir exists as a dir (or symlink to a dir)
    # if templateDir and not os.path.isdir( os.path.join( templateDir, ".")):
    #     print( '%s %s' % ('enumer: INFO, not a dir:', templateDir))

    # read optional templateScript
    if templateScript:
        try :
            with open(templateScript,'r') as inFile:
                runLines = inFile.read().splitlines()
        except :
            perr( '%s %s' % ('enumer: ERROR, failed open:', templateScript))
            err += 1

    # read dimensions from config file.
    # let an exception kill the program, and report its own error messages:
    if not os.path.isfile( configFile ):
        perr( '%s %s' % ('enumer: ERROR, file not found:', configFile))
        err += 1
    else:
        exec_full( configFile )

    nbrDim = len( allDims )
    if verbose: print( "number of dims: %d" % (nbrDim))
    if verbose: dimDump()

    # if non-zero errors till now: exit early.
    if err > 0:
        sys.exit(1)

    # enumerate cases from dimensions
    global cases, digMax, nbrCases, curDigits
    cases = []
    curDigits = []
    digMax = []
    nbrCases = 1
    # initialize case 0, all digits at 0
    for x in allDims:
        vals = x[1]
        digMax += [ len(vals) - 1 ]
        nbrCases *= len(vals)
        curDigits += [ 0 ]
    cases += [ curDigits ]
    print( "enumer: number of cases: %d" % (nbrCases))
    
    # enumerate all digits. incr returns FALSE when most-siginificant digit overflows.
    while incr():
        cases += [ curDigits[:] ]    # copy the list
    if verbose: caseDump()

    tmpfRunAll = ""
    if templateScript:
        tmpfRunAll = tempfile.NamedTemporaryFile(delete=False)

    if tmpfRunAll:
        chmodPlusX(tmpfRunAll.name)
        runAllf=open(tmpfRunAll.name,'w')
        print("""#!/bin/bash
rund=$(readlink -f $(dirname $0))
logp=$rund/run-all.log

echo log: $logp
echo in dir: $rund
echo
cd           $rund
exec </dev/null >& $logp
{ cat <<_EOF""", file=runAllf)

    # walk the cases, make runDirs, do substitutions in template, do subs in optional template-script
    ndx = 0
    for x in cases:
        dirName = "%05d" % (ndx)
        caseDir = os.path.join( runDir, dirName )
        trg     = os.path.join( runDir, dirName, outName )
        os.makedirs(os.path.dirname(trg), exist_ok=True)

        # do string replacements in copy of srcLines
        auxMap = { "${ENUMER_CASE_NBR}": dirName,
                   "${ENUMER_CASE_DIR}": caseDir }
        lines = dimReplace( srcLines, x, ndx, auxMap )
        if templateScript:
            trg2   = os.path.join( runDir, dirName, outName2 )
            lines2 = dimReplace( runLines, x, ndx, auxMap )
        if tmpfRunAll:
            relCaseRun = os.path.join( ".", dirName, outName2 )
            print(relCaseRun, file=runAllf)

        tmpf1 = tempfile.NamedTemporaryFile(delete=False)
        with open(tmpf1.name, 'w') as f:
            for i in lines: print(i, file=f)
        # if verbose: print( "wrote: %s" % tmpf1.name )
        if trg:
            shutil.move(tmpf1.name, trg)
            if verbose: print( "wrote: %s" % trg )
        
        if templateScript:
            # We reuse same tempfile name as just used for outFile,
            # but since it was moved, we're recreating it from scratch here, which
            # uses existing umask; unlike tempfile.NamedTemporaryFile() which creates
            # the file to be user-readable only.
            # TODO: Should make these consistent. Possibly just not ruese old tempfile name?
            with open(tmpf1.name, 'w') as f:
                for i in lines2: print(i, file=f)
            chmodPlusX(tmpf1.name)
            # if verbose: print( "wrote: %s" % tmpf1.name )
            if trg2:
                shutil.move(tmpf1.name, trg2)
                if verbose: print( "wrote: %s" % trg2 )

        ndx += 1
        if firstN > 0 and ndx >= firstN:
            break

    flushStdOutErr()
    if nbrJobs < 0: nbrJobs = countCPU()
    if nbrJobs < 1: nbrJobs = 1

    if tmpfRunAll:
        print("_EOF\n} | xargs -n 1 -P %d /bin/bash" % (nbrJobs), file=runAllf)
        runAllf.close()

        trg = os.path.join( runDir, "run-all.sh")
        shutil.move(tmpfRunAll.name, trg)
        if verbose: print( "wrote: %s" % trg )

        if runAll:
            runAllLog = os.path.join( runDir, "run-all2.log")
            with open(tmpf1.name, 'w') as f:
                try:
                    print( "enumer: running run-all.sh ..." )
                    flushStdOutErr()
                    p = subprocess.run(trg, stdout = f, stderr = f, stdin = None, check = True,
                                       universal_newlines=True)
                except subprocess.CalledProcessError as e:
                    print('enumer: ERROR: running run-all.sh: ' + str(e.output), flush=True, file=sys.stderr)
                    err += 1

    # exit status: indicates if there were errors.
    flushStdOutErr()
    print( "enumer: %d errors, %d warning" % (err, warn))
    sys.exit(err)

if __name__ == '__main__': main(sys.argv)

# for emacs syntax-mode:
# Local Variables:
# mode:python
# End:
