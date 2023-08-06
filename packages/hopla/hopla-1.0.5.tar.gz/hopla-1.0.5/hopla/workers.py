##########################################################################
# Hopla - Copyright (C) AGrigis, 2015 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module proposes a local worker and a distant TORQUE worker. The two
proposed workers are able to follow a '__hopla__' list of parameter
names to keep trace on. All specified parameters values are stored in the
execution status.
"""  # pragma: no cover

# System import
from __future__ import print_function  # pragma: no cover
import os  # pragma: no cover
import copy  # pragma: no cover
import subprocess  # pragma: no cover
import traceback  # pragma: no cover
from socket import getfqdn  # pragma: no cover
import sys  # pragma: no cover
import glob  # pragma: no cover
import time  # pragma: no cover
import json  # pragma: no cover
import random  # pragma: no cover

# Hopla import
from .signals import FLAG_ALL_DONE  # pragma: no cover
from .signals import FLAG_WORKER_FINISHED_PROCESSING  # pragma: no cover


def worker(tasks, returncodes, python_cmd="python", delay_upto=0,
           use_subprocess=False):
    """ The worker function for a script.

    If the script contains a '__hopla__' list of parameter names to keep
    trace on, all the specified parameters values are stored in the return
    code.

    Parameters
    ----------
    tasks, returncodes: multiprocessing.Queue
        the input (commands) and output (results) queues.
    python_cmd: str (optional, default 'python')
        the path to the python binary. Only usefull in the subprocess mode.
    delay_upto: int (optional, default 0)
        the process execution will be delayed randomly by [0, <delay_upto>[
        seconds.
    use_subprocess: bool, default False
        use a subprocess (for instance in case of memory leak). In this
        particular case the __hopla__ setting is deactivated.
    """
    while True:
        signal = tasks.get()
        if signal == FLAG_ALL_DONE:
            returncodes.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        job_name, command = signal
        returncode = {}
        returncode[job_name] = {}
        returncode[job_name]["info"] = {}
        returncode[job_name]["debug"] = {}
        returncode[job_name]["info"]["cmd"] = command
        returncode[job_name]["debug"]["hostname"] = getfqdn()

        # COMPATIBILITY: dict in python 2 becomes structure in pyton 3
        python_version = sys.version_info
        if python_version[0] < 3:
            environ = copy.deepcopy(os.environ.__dict__)
        else:
            environ = copy.deepcopy(os.environ._data)
        returncode[job_name]["debug"]["environ"] = environ

        # Execution with a random delay expressed in seconds
        try:
            time.sleep(random.random() * abs(delay_upto))
            sys.argv = command
            job_status = {}
            if use_subprocess:
                if python_cmd is not None:
                    subprocess.check_call([python_cmd] + command)
                else:
                    subprocess.check_call(command)
            else:
                with open(command[0]) as ofile:
                    exec(ofile.read(), job_status)
            returncode[job_name]["info"]["exitcode"] = "0"
        # Error
        except:
            returncode[job_name]["info"]["exitcode"] = (
                "1 - '{0}'".format(traceback.format_exc().rstrip("\n")))
        # Follow '__hopla__' script parameters
        finally:
            if "__hopla__" in job_status:
                for parameter_name in job_status["__hopla__"]:
                    if parameter_name in job_status:
                        returncode[job_name]["info"][
                            parameter_name] = job_status[parameter_name]
        returncodes.put(returncode)


PBS_TEMPLATE = """
#!/bin/bash
#PBS -l mem={memory}gb,nodes=1:ppn={threads},walltime={hwalltime}:00:00
#PBS -N {name}
#PBS -e {errfile}
#PBS -o {logfile}
echo $PBS_JOBID
{command}
"""  # pragma: no cover


PY_TEMPLATE = """
from __future__ import print_function
import sys
import json


# Execute the command line in the 'job_status' environment
try:
    command = {cmd}
    sys.argv = command
    job_status = dict()
    with open(command[0]) as ofile:
        exec(ofile.read(), job_status)
# Error
except:
    raise
# Follow '__hopla__' script parameters: print the parameters to keep trace on
# in '<hopla>...</hopla>' div in order to communicate with the scheduler and
# in order to generate a complete log
finally:
    parameters = dict()
    if "__hopla__" in job_status:
        for parameter_name in job_status["__hopla__"]:
            if parameter_name in job_status:
                parameters[parameter_name] = job_status[parameter_name]
    print("<hopla>")
    print(json.dumps(parameters))
    print("</hopla>")
"""  # pragma: no cover


def qsub_worker(tasks, returncodes, logdir, queue,
                memory=1, walltime=24, nb_threads=1, python_cmd="python",
                delay_upto=0, sleep=4):
    """ A cluster worker function for a script.

    Use the TORQUE resource manager provides control over batch jobs and
    distributed computing resources. It is an advanced open-source product
    based on the original PBS project.

    Use a double script strategy in order to manage the '__hopla__' list of
    parameter names to keep trace on: a '.pbs' script calling another '.py'
    script that print the '__hopla__' parameters. All the specified parameters
    values are stored in the return code.

    Parameters
    ----------
    tasks, returncodes: multiprocessing.Queue
        the input (commands) and output (results) queues.
    logdir: str
        a path where the qsub error and output files will be stored.
    queue: str
        the name of the queue where the jobs will be submited.
    memory: float (optional, default 1)
        the memory allocated to each qsub (in GB).
    walltime: int (optional, default 24)
        the walltime used for each job submitted on the cluster (in hours).
    nb_threads: int (optional, default 1)
        the number of cores allocated for each node.
    python_cmd: str (optional, default 'python')
        the path to the python binary. If None consider the command directly in
        the PBS batch.
    delay_upto: int (optional, default 0)
        the process execution will be delayed randomly by [0, <delay_upto>[
        seconds.
    sleep: float (optional, default 4)
        time rate to check the termination of the submited jobs.
    """
    while True:
        signal = tasks.get()
        if signal == FLAG_ALL_DONE:
            returncodes.put(FLAG_WORKER_FINISHED_PROCESSING)
            break
        job_name, command = signal
        returncode = {}
        returncode[job_name] = {}
        returncode[job_name]["info"] = {}
        returncode[job_name]["debug"] = {}
        returncode[job_name]["info"]["cmd"] = command
        returncode[job_name]["debug"]["hostname"] = getfqdn()

        # COMPATIBILITY: dict in python 2 becomes structure in python 3
        python_version = sys.version_info
        if python_version[0] < 3:
            environ = copy.deepcopy(os.environ.__dict__)
        else:
            environ = copy.deepcopy(os.environ._data)
        returncode[job_name]["debug"]["environ"] = environ

        # Torque-PBS execution
        fname_pbs = os.path.join(logdir, job_name + ".pbs")
        fname_py = os.path.join(logdir, job_name + ".py")
        errfile = os.path.join(logdir, "error." + job_name)
        logfile = os.path.join(logdir, "output." + job_name)
        try:
            # Random delay expressed in seconds
            time.sleep(random.random() * abs(delay_upto))

            # Edit the job to be submitted
            if python_cmd is not None:
                with open(fname_py, "w") as open_file:
                    open_file.write(PY_TEMPLATE.format(cmd=command))
                with open(fname_pbs, "w") as open_file:
                    pbs_cmd = " ".join([python_cmd, fname_py])
                    open_file.write(PBS_TEMPLATE.format(
                        memory=memory,
                        hwalltime=walltime,
                        threads=nb_threads,
                        name=job_name,
                        errfile=errfile,
                        logfile=logfile,
                        command=pbs_cmd))
            else:
                with open(fname_pbs, "w") as open_file:
                    open_file.write(PBS_TEMPLATE.format(
                        memory=memory,
                        hwalltime=walltime,
                        threads=nb_threads,
                        name=job_name,
                        errfile=errfile,
                        logfile=logfile,
                        command=" ".join(command)))

            # Submit the job
            # subprocess.check_call(["qsub", "-q", queue, fname_pbs])
            process = subprocess.Popen(["qsub", "-q", queue, fname_pbs],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            job_id = stdout.rstrip("\n")
            print(job_id)
            exitcode = process.returncode
            if exitcode != 0:
                raise Exception(stderr)

            # Lock everything until the submitted command has not terminated
            while True:
                terminated = (len(glob.glob(errfile + ".*")) > 0 or
                              len(glob.glob(logfile + ".*")) > 0)
                with_log = terminated
                process = subprocess.Popen("qstat | grep {0}".format(job_id),
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           shell=True)
                stdout, stderr = process.communicate()
                exitcode = process.returncode
                terminated = terminated or (exitcode == 1)
                if terminated:
                    break
                time.sleep(sleep)

            # Check that no error was produced during the submission
            if with_log:
                with open(glob.glob(errfile + ".*")[0]) as open_file:
                    stderr = open_file.readlines()
                if len(stderr) > 0:
                    raise Exception("\n".join(stderr))

            # Update the return code
            if with_log:
                returncode[job_name]["info"]["exitcode"] = "0"
            else:
                returncode[job_name]["info"]["exitcode"] = "-1"
        # Error
        except:
            if os.path.isfile(errfile):
                with open(errfile) as openfile:
                    error_message = openfile.readlines()
            else:
                error_message = traceback.format_exc()
            returncode[job_name]["info"]["exitcode"] = (
                "1 - '{0}'".format(error_message))
        # Follow '__hopla__' script parameters in pbs '<hopla>...</hopla>'
        # output
        finally:
            pbs_logfiles = glob.glob(logfile + ".*")
            if len(pbs_logfiles) == 1:
                with open(pbs_logfiles[0]) as open_file:
                    stdout = open_file.read()
                hopla_start = stdout.rfind("<hopla>")
                hopla_end = stdout.rfind("</hopla>")
                parameters_repr = stdout[
                    hopla_start + len("<hopla>"): hopla_end]
                try:
                    parameters = json.loads(parameters_repr)
                except:
                    parameters = {}
                for name, value in parameters.items():
                    returncode[job_name]["info"][name] = value

        returncodes.put(returncode)
