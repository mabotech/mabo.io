
-- mts_log_format

local l = require("lpeg")
l.locale(l)

local M = {}
setfenv(1, M) 

    local date_fullyear = l.Cg(l.digit * l.digit * l.digit * l.digit, "year")

    local date_month = l.Cg(l.P"0" * l.R"19"
                         + "1" * l.R"02", "month")

    local date_mday = l.Cg(l.P"0" * l.R"19"
                        + l.R"12" * l.R"09"
                        + "3" * l.R"01", "day")
    
    local time_hour = l.Cg(l.R"01" * l.digit
                        + "2" * l.R"03", "hour")

    local time_minute = l.Cg(l.R"05" * l.digit, "min")

    local time_second = l.Cg(l.R"05" * l.digit
                               + "60", "sec")
                               
    local levels = l.Cg((
          l.P"debug"   / "7"
        + l.P"Information"    / "6"
        + l.P"notice"  / "5"
        + l.P"Warning"    / "4"
        + l.P"error"   / "3"
        + l.P"crit"    / "2"
        + l.P"alert"   / "1"
        + l.P"emerg"   / "0"), "severity")
        
    local BEGIN_LOGGER = l.P("[")
    local END_LOGGER = l.P("]")
    ---local NOT_BEGIN = (1 - BEGIN_COMMENT)^0
    local LOGGER = (1 - END_LOGGER)^0
    local FULL_LOGGER = BEGIN_LOGGER * l.Cg(LOGGER,"logger") * END_LOGGER
    

    local Quote = l.P('"')
    local MSG = l.Cg((1-Quote)^0, "msg")
    local full_msg = Quote * MSG * Quote
    
    local time = "("*date_month * "/" * date_mday * "/" *date_fullyear  
        * " " * time_hour * ":" * time_minute * ":" * time_second * ")"

    local t1 = l.Ct( time * " " * levels * " " * FULL_LOGGER * " " * full_msg)
    local t2 = l.Ct( time * " " * levels * " " * FULL_LOGGER)
    
function build_mts_grammar()    

    return l.Ct(t1+t2)
end

return M