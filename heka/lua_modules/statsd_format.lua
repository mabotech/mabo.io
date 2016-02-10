
-- statsd parser

local l = require("lpeg")

local pretty = require("pl.pretty")

l.locale(l)

function parse(msg)

    local sep = l.P("\n")
    local space = l.P(" ")
    local name = l.Cg((1-(sep+space))^0,"name")

    function maybe(p) return p^-1 end
    
    local digits = l.R'09'^1
    local mpm = maybe(l.S'+-')
    local dot = '.'
    local exp = l.S'eE'
    
    local value = l.Cg(mpm * digits * maybe(dot*digits)* maybe(exp*mpm*digits)/tonumber,"value" )

    local timestamp = l.Cg(l.R'09'^1/tonumber,"timestamp")

    local c = l.Ct(name*space*value*space*timestamp*sep)

    local grammar = l.Ct(c^0)

    local list = grammar:match(msg)

    return list    

end

local msg = "stats.counters.foo.rate 0.00 1455112442\nstats.counters.foo.count 0 1455112442\nstats.gauges.mabo.io 39.000000 1455112442\nstats.gauges.test -6.2166e1 1455112442\nstats.gauges.foo +22.8760 1455112442\nstats.statsd.numStats 4 1455112442\n"

local list = parse(msg)

pretty.dump(list)