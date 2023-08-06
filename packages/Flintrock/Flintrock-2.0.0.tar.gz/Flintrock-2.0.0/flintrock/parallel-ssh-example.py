from pssh.clients import ParallelSSHClient
from pssh.utils import enable_host_logger

enable_host_logger()

client = ParallelSSHClient(hosts=['localhost', 'localhost'])
cmd = 'uname && sleep 100'
output = client.run_command(cmd)
client.join(output, consume_output=True)

for host_out in output:
    for line in host_out.stdout:
        print(line)
