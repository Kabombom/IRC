#Creates new simulation
set ns [new Simulator]

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

#Terminates the simulation after 5s
$ns at 5.0 "fim"
#Iniciates simulation
$ns run
