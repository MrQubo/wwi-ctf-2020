#!/bin/bash

set -o errexit -o pipefail -o nounset


mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL

declare -ra args=(
	-Ml --port 9000
	--user app --group app
	--cwd /opt
	-R /bin -R /usr -R /lib -R /lib64
	-R /opt
	--time_limit 0
	--cgroup_cpu_ms_per_sec 1000
	--cgroup_mem_max "$((1024 * 1024))"
	--cgroup_pids_max 1
	-- "$@"
)
exec nsjail "${args[@]}"
