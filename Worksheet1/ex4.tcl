#Creates new simulation
set ns [new Simulator]

#Creates file to store the results of the simulation
#Dump of the simutalation goes in the file
set nf [open out.nam w]
$ns namtrace-all $nf

#Sequence of commands so that at the end of the simulation the result file is closed and NAM is called
#This basically "cleans the house" in the end of the simulation
proc fim {} {
    global ns nf
    $ns flush-trace
    close $nf
    exec nam out.nam
    exit 0
}

#Nodes
set n0 [$ns node]
set n1 [$ns node]

#Links
#When the queue loses packages SFQ is a more fair way to lose packages
$ns duplex-link $n0 $n1 1Mb 10ms DropTail

#Creates a UDP agent and connects it to node 0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#Creates a source of traffic CBR(constant bit rate) and connects it to udp0
#This CBR generates 1 packet of 500 Bytes. At 200 packages per second (1 in 0.005)
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

#Data receiver. Define a NULL agent that will act as receiver
#NULL agent linked to node n1
set null0 [new Agent/Null]
$ns attach-agent $n1 $null0

#Connect the 2 agents
$ns connect $udp0 $null0

#Defines when to start and end data transmission
$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"

#Terminates the simulation after 5s
$ns at 5.0 "fim"
#Iniciates simulation
$ns run
