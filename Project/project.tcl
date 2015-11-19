if {$argc == 5} {
    set cenario [lindex $argv 0]
    set protocolo [lindex $argv 1]
    set tcp_window [lindex $argv 2]
    set quebra [lindex $argv 3]
    set velocidade [lindex $argv 4]
} else {
    puts "Insira cenário(default= cenario 1; 2 = cenario 2), protocolo(udp ou tcp; default da erro),
    janela, quebra(1-quebra; default nao quebra) e velocidade da ligacao 0-4"
    exit 1
}
#awk -f trace_analyzer.awk type=cbr src=0 dest=2 flow=1 trace.tr
set ns [new Simulator]

set nf [open out.nam w]
$ns namtrace-all $nf

set nt [open trace.tr w]
$ns trace-all $nt

#Algorithm for dynamic forwarding
$ns rtproto DV

proc fim {} {
    global ns nf
    $ns flush-trace
    close $nf
    exec nam out.nam
    exit 0
}

#Creation of nodes
for {set i 0} {$i < 7} {incr i} {
    set n$i [$ns node]
}

#Links
$ns duplex-link $n0 $n4 $velocidade 10ms DropTail
$ns duplex-link $n1 $n5 0.1Gb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n5 200Mb 10ms DropTail
$ns duplex-link $n4 $n6 1Gb 10ms DropTail
$ns duplex-link $n5 $n6 100Mb 10ms DropTail
$ns duplex-link $n6 $n2 40Mb 3ms DropTail

#Position of queue
$ns duplex-link-op $n0 $n4 queuePos 0.5
$ns duplex-link-op $n1 $n5 queuePos 0.5
$ns duplex-link-op $n4 $n3 queuePos 0.5
$ns duplex-link-op $n4 $n5 queuePos 0.5
$ns duplex-link-op $n4 $n6 queuePos 0.5
$ns duplex-link-op $n2 $n6 queuePos 0.5

#Layout of nodes
$ns duplex-link-op $n0 $n4 orient down
$ns duplex-link-op $n1 $n5 orient down
$ns duplex-link-op $n4 $n6 orient right-down
$ns duplex-link-op $n4 $n5 orient right
$ns duplex-link-op $n4 $n3 orient down
$ns duplex-link-op $n5 $n6 orient down
$ns duplex-link-op $n6 $n2 orient right

#Shapes, colors and labels
$n0 shape "hexagon"
$n1 shape "hexagon"
$n2 shape "square"
$n3 shape "square"

$n0 color Red
$n1 color Red
$n2 color Blue
$n3 color Blue

#(cor dos pacotes)
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Green
$ns color 4 Black

$ns duplex-link-op $n0 $n4 label "v=$velocidade"
$ns duplex-link-op $n1 $n5 label "v=0,1Gb"
$ns duplex-link-op $n4 $n3 label "v=10Mb"
$ns duplex-link-op $n4 $n5 label "v=200Mb"
$ns duplex-link-op $n6 $n5 label "v=100Mb"
$ns duplex-link-op $n4 $n6 label "v=1Gb"
$ns duplex-link-op $n6 $n2 label "v=40Mb"

$n0 label "Servidor 1"
$n1 label "Servidor 2"
$n2 label "Receptor 1"
$n3 label "Receptor 2"
$n4 label "R4"
$n5 label "R5"
$n6 label "R6"


set queue0_4 [[$ns link $n0 $n4] queue]
$queue0_4 set limit_ 2098

if {$protocolo == "UDP"} {
    set udp0 [new Agent/UDP]
    $ns attach-agent $n0 $udp0

    set cbr0 [new Application/Traffic/CBR]
    $cbr0 set packetSize_ 2097152
    #2MB * 1024 * 1024
    $cbr0 set maxpkts_ 1
    $cbr0 attach-agent $udp0

    set null0 [new Agent/Null]
    $ns attach-agent $n2 $null0
    $ns connect $udp0 $null0

    $udp0 set class_ 1

    $ns at 0.5 "$cbr0 start"
    $ns at 9.0 "$cbr0 stop"
}
if {$protocolo == "TCP"} {
    set tcp0 [$ns create-connection TCP $n0 TCPSink $n2 2]
    $tcp0 set window_ $tcp_window

    set cbr0  [new Application/Traffic/CBR]
    $cbr0 set packetSize_ 2097152
    $cbr0 set maxpkts_ 1

    $ns attach-agent $n0 $tcp0
    $cbr0 attach-agent $tcp0

    $tcp0 set class_ 2

    $ns at 0.5 "$cbr0 start"
    $ns at 9.0 "$cbr0 stop"
}

if {$cenario == 2} {
	set udp1 [new Agent/UDP]
	$ns attach-agent $n1 $udp1

	set cbr1 [new Application/Traffic/CBR]
	$cbr1 set rate_ 3Mb
	$cbr1 attach-agent $udp1

	set null1 [new Agent/Null]
	$ns attach-agent $n2 $null1
	$ns connect $udp1 $null1

    $udp1 set class_ 3

	$ns at 0.5 "$cbr1 start"
	$ns at 9.0 "$cbr1 stop"

	set udp2 [new Agent/UDP]
	$ns attach-agent $n1 $udp2

	set cbr2 [new Application/Traffic/CBR]
	$cbr2 set rate_ 3Mb
	$cbr2 attach-agent $udp2

	set null2 [new Agent/Null]
	$ns attach-agent $n3 $null2
	$ns connect $udp2 $null2

    $udp2 set class_ 4

	$ns at 0.5 "$cbr2 start"
	$ns at 9.0 "$cbr2 stop"
}

if {$quebra == 1} {
    $ns rtmodel-at 0.6 down $n4 $n6
    $ns rtmodel-at 0.7 up $n4 $n6
}

$ns at 10.0 "fim"
$ns run
