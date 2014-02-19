import taskrun
import os

POWER = 15
RUNS = 10
PACKETS_PER_RUN = 100000

manager = taskrun.Task.Manager(
    numProcs = 1,
    showCommands = True,
    runTasks = True,
    showProgress = True)

DIR = "sims"
mkdir = manager.task_new('dir', 'rm -rI ' + DIR + '; mkdir ' + DIR)

def makeName(stype, size, run):
    return stype + '_size' + str(size) + '_run' + str(run)

def makeCommand(port_or_path, size, name):
    return 'node client.js ' + port_or_path + ' ' + str(size) + ' ' + str(PACKETS_PER_RUN) + \
        ' | grep millis | awk \'{printf "%s, ", $2}\' > ' + os.path.join(DIR, name)

barrier1 = manager.task_new('barrier1', 'sleep 0')
for exp in range(0, POWER):
    size = pow(2, exp)
    for run in range(0, RUNS):
        # Unix domain socket test
        name = makeName('uds', size, run)
        task = manager.task_new(name, makeCommand('/tmp/uds', size, name))
        task.dependency_is(mkdir)
        barrier1.dependency_is(task)

        # TCP socket test
        name = makeName('tcp', size, run)
        task = manager.task_new(name, makeCommand('5555', size, name))
        task.dependency_is(mkdir)
        barrier1.dependency_is(task)

# create CSV header
filename = os.path.join(DIR, 'uds_vs_tcp.csv')
header = 'NAME, '
for run in range(0, RUNS):
    header += 'RUN ' + str(run) + ', '
hdr_task = manager.task_new('CSV header', 'echo \'' + header + '\' > ' + filename)
hdr_task.dependency_is(barrier1)

# UDS to CSV
cmd = ''
for exp in range(0,POWER):
    size = pow(2, exp)
    cmd += 'echo -n \'UDS Size ' + str(size) + ', \' >> ' + filename + '; '
    for run in range(0, RUNS):
        name = makeName('uds', size, run)
        cmd += 'cat ' + os.path.join(DIR, name) + ' >> ' + filename + '; '
    cmd += 'echo \'\' >> ' + filename + '; '
uds_task = manager.task_new('UDS to CSV', cmd)
uds_task.dependency_is(hdr_task)

# TCP to CSV
cmd = ''
for exp in range(0,POWER):
    size = pow(2, exp)
    cmd += 'echo -n \'TCP Size ' + str(size) + ', \' >> ' + filename + '; '
    for run in range(0, RUNS):
        name = makeName('tcp', size, run)
        cmd += 'cat ' + os.path.join(DIR, name) + ' >> ' + filename + '; '
    cmd += 'echo \'\' >> ' + filename + '; '
tcp_task = manager.task_new('TCP to CSV', cmd)
tcp_task.dependency_is(uds_task)

manager.run_request_is()
