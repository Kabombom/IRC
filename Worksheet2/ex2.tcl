set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

$ns color 1 Blue
$ns color 2 Red
$ns color 3 Black

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
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]
set n7 [$ns node]

#C = 800Mb e Tp = 2.5ms
$ns duplex-link $n0 $n1 800Mb 2.5ms DropTail #A
#C = 500Mb e Tp = 234ms
$ns duplex-link $n2 $n3 500Mb 234ms DropTail #B
#C = 33.5Mb e Tp = 0.05ms
$ns duplex-link $n4 $n5 33.5Mb 0.05ms DropTail #C
#C = 8000Mb e Tp = 1ms
$ns duplex-link $n6 $n7 8000Mb 1ms DropTail #D

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#30KB = 30720B
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 30720
$cbr0 set interval_ 1
$cbr0 set maxpkts_ 1
$cbr0 attach-agent $udp0

set udp2 [new Agent/UDP]
$ns attach-agent $n2 $udp2

#30KB = 30720B
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetSize_ 30720
$cbr2 set interval_ 1
$cbr2 set maxpkts_ 1
$cbr2 attach-agent $udp2

set udp4 [new Agent/UDP]
$ns attach-agent $n4 $udp4

#30KB = 30720B
set cbr4 [new Application/Traffic/CBR]
$cbr4 set packetsize_ 30720
$cbr4 set interval_ 1
$cbr4 set maxpkts_ 1
$cbr4 attach-agent $udp4

set udp6 [new Agent/UDP]
$ns attach-agent $n6 $udp6

#30KB = 30720B
set cbr6 [new Application/Traffic/CBR]
$cbr6 set packetSize_ 30720
$cbr6 set interval_ 1
$cbr6 set maxpkts_ 1
$cbr6 attach-agent $udp6

set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

set null2 [new Agent/Null]
$ns attach-agent $n3 $null2

set null4 [new Agent/Null]
$ns attach-agent $n5 $null4

set null6 [new Agent/Null]
$ns attach-agent $n7 $null6

$ns connect $udp0 $null0
$ns connect $udp2 $null2
$ns connect $udp4 $null4
$ns connect $udp6 $null6

$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr2 start"
$ns at 0.1 "$cbr4 start"
$ns at 0.1 "$cbr6 start"
$ns at 4.0 "$cbr0 stop"
$ns at 4.0 "$cbr2 stop"
$ns at 4.0 "$cbr4 stop"
$ns at 4.0 "$cbr6 stop"

$udp0 set class_ 1
$udp2 set class_ 2
$udp4 set class_ 3

$ns at 5.0 "fim"

$ns run
