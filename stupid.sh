while [[ 1 ]]; do
	sport=$(( ( RANDOM % 10000 )  + 1000 ))
	dport=$(( ( RANDOM % 10000 )  + 1000 ))
	traceroute 10.2.10.2 --sport=$sport -U -p $dport | tr '\n' ' ' | grep -o "leaf.*spine1.*core1.*spine4.*leaf";
	#traceroute 10.2.10.2 --sport=$sport -U -p $dport | tr '\n' ' ' | grep "traceroute to.*core1-spine2.*spine3-core1.*";
	if [[ $? -eq 0 ]]; then
		echo "$sport $dport"
	fi
done
