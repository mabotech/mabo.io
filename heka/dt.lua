
--[[

lpeg exercise

]]

local l = require("lpeg")

local pretty = require("pl.pretty")

lpeg.locale(l)  

function dt_parse(line)

    local date_fullyear = l.Cg(l.digit * l.digit * l.digit * l.digit, "year")

    local date_month = l.Cg(l.P"0" * l.R"19"
                         + "1" * l.R"02", "month")

    local date_mday = l.Cg(l.P"0" * l.R"19"
                        + l.R"12" * l.R"09"
                        + "3" * l.R"01", "day")
    --[[
    date_mday_sp = l.Cg(l.P" " * l.R"19"
                        + l.S"12" * l.digit
                        + "3" * l.S"01", "day")
    ]]
    
    local time_hour = l.Cg(l.R"01" * l.digit
                        + "2" * l.R"03", "hour")

    local time_minute = l.Cg(l.R"05" * l.digit, "min")

    local time_second = l.Cg(l.R"05" * l.digit
                               + "60", "sec")
                               
    local t = l.Ct("("*date_month *"/"* date_mday*"/"*date_fullyear  *" "* time_hour *":"* time_minute*":" * time_second*")")

    local v = t:match(line)

    pretty.dump(v)

end

dt_parse("(01/20/2016 16:09:21)")

dt_parse("(01/20/2016 16:29:51)")
