#Creates new simulation
set ns [new Simulator]

#Traffic colors
$ns color 1 Blue
$ns color 2 Red

#Creates file to store the results of the simulation
set nf [open out.nam w]
$ns namtrace-all $nf

#Sequence of commands so that at the end of the simulation the result file is closed and NAM is called
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
set n2 [$ns node]
set n3 [$ns node]

#Links
#When teh queue loses packages SFQ is a more fair way to lose packages
$ns duplex-link $n0 $n2 1Mb 10ms DropTail
$ns duplex-link $n1 $n2 1Mb 10ms DropTail
$ns duplex-link $n2 $n3 1Mb 10ms SFQ

#Disposition of Nodes
$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right

#Creates a UDP agent and connects it to node 0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

#Creates a source of traffic CBR(constant bit rate) and connects it to udp0
#This CBR generates packets of 500 Bytes. At 200 packages per second (1 in 0.005)
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

#Creates a UDP agent and connects it to node 1
set udp1 [new Agent/UDP]
$ns attach-agent $n1 $udp1

#Creates a source of traffic CBR(constant bit rate) and connects it to udp0
#This CBR generates packets of 500 Bytes. At 200 packages per second (1 in 0.005)
set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 500
$cbr1 set interval_ 0.005
$cbr1 attach-agent $udp1

#Data receiver. Define a NULL agent that will act as receiver
#NULL agent linked to node n1
set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

#Connections of agents
$ns connect $udp0 $null0
$ns connect $udp1 $null0

#Defines when to start and end data transmission of the agents
$ns at 0.5 "$cbr0 start"
$ns at 1.0 "$cbr1 start"
$ns at 4.0 "$cbr1 stop"
$ns at 4.5 "$cbr0 stop"

#Distinguish different traffic fluxes
$udp0 set class_ 1
$udp1 set class_ 2

#Observes the queue out for the link n2 to n3
$ns duplex-link-op $n2 $n3 queuePos 0.5

#Terminates the simulation after 5s
$ns at 5.0 "fim"
#Iniciates simulation
$ns run
