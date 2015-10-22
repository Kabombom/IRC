#Creates new simulation
set ns [new Simulator]

$ns color 1 Blue

#Creates file to store the results of the simulation
#Dump of the simulation goes in the file
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
for {set i 0} {$i < 7} {incr i} {
    set n($i) [$ns node]
}

#Links
#When the queue loses packages SFQ is a more fair way to lose packages
for {set i 0} {$i < 7} {incr i} {
    $ns duplex-link $n($i) $n([expr ($i+1)%7]) 1Mb 10ms DropTail
}

#Creates a UDP agent and connects it to node 0
set udp0 [new Agent/UDP]
$ns attach-agent $n(0) $udp0

#Creates a source of traffic CBR(constant bit rate) and connects it to udp0
#This CBR generates packets of 500 Bytes. At 200 packages per second (1 in 0.005)
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0

#Data receiver. Define a NULL agent that will act as receiver
#NULL agent linked to node n1
set null0 [new Agent/Null]
$ns attach-agent $n(3) $null0

#Connections of agents
$ns connect $udp0 $null0

#Defines when to start and end data transmission of the agents
$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"

#The traffic has blue color
$udp0 set class_ 1

#Inserts a flaw at the link between nodes 1 and 2
$ns rtmodel-at 1.0 down $n(1) $n(2)
$ns rtmodel-at 2.0 up $n(1) $n(2)

#Dynamic forwarding algo
#When the flaw between 1 and 2 occurs this algo sets an alternative route
$ns rtproto DV

#Terminates the simulation after 5s
$ns at 5.0 "fim"
#Iniciates simulation
$ns run
