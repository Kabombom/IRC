set ns [new Simulator]

set nf [open out.nam w]
$ns namtrace-all $nf

proc fim {} {
	global ns nf
	$ns flush-trace
	close $nf
	exec nam out.nam
	exit 0
}

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

#A->B Tp=5ms e C = 3Mb
$ns duplex-link $n0 $n1 3Mb 5ms DropTail

#B->C Tp=233.3ms e C=1Gb==1000Mb
$ns duplex-link $n1 $n2 1000Mb 233ms DropTail

#C->D Tp=0.05ms e C=9.97Mb
$ns duplex-link $n2 $n3 9.97Mb 0.05ms DropTail

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

set cbr0 [new Application/Traffic/CBR]
#Faltou adicionar chars adicionais
$cbr0 set packetSize_ 20485
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

$ns connect $udp0 $null0

$ns at 0.1 "$cbr0 start"
$ns at 4.0 "$cbr0 stop"

$ns at 5.0 "fim"

$ns run
