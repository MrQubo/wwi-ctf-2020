#!/bin/bash

set -o errexit -o pipefail -o nounset


mkdir /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL

declare -ra args=(
	-Ml --port 9000
	--user app --group app
	--cwd /home
	-R /bin -R /usr -R /lib -R /lib64
	-R /home/app
	--time_limit 0
	--cgroup_cpu_ms_per_sec 8
	--cgroup_mem_max "$((2 * 1024 * 1024))"
	--cgroup_pids_max 4
	-- "$@"
)
exec nsjail "${args[@]}"
