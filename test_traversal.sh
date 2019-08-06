#!/usr/bin/expect --
set fd [open "node_list" r]
while {[gets $fd line] >= 0 } {puts "$line"}
close $fd
