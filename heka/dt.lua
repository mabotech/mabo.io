
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
        + l.P"emerg"   / "0")
        / tonumber, "severity")
        
    local BEGIN_LOGGER = l.P("[")
    local END_LOGGER = l.P("]")
    ---local NOT_BEGIN = (1 - BEGIN_COMMENT)^0
    local LOGGER = (1 - END_LOGGER)^0
    local FULL_LOGGER = BEGIN_LOGGER * l.Cg(LOGGER,"logger_name") * END_LOGGER
    

    local Q = l.P('"')
    local MSG = l.Cg((1-Q)^0, "msg")
    local full_msg = Q*MSG*Q
    
    local time = "("*date_month *"/"* date_mday*"/"*date_fullyear  *" "* time_hour *":"* time_minute*":" * time_second*")"

    local t1 = l.Ct( time * " " * levels * " " * FULL_LOGGER * " " * full_msg)
    local t2 =  l.Ct( time * " " * levels)
    
    local t3 = l.Ct(t1+t2)
    local v = t3:match(line)
   
    -- pretty.dump(v)
    
    timestamp =os.time(v[1])
    
    if v[1].logger_name then
        print(timestamp .. " " .. v[1].severity .. " " .. v[1].logger_name .. " " .. v[1].msg)
    else
        print(timestamp .. " " .. v[1].severity)
    end      

end

function run()

    print("log parser")

    local fh = io.open("Rear Spindle_Direct_Test.log")

    local i = 0

    local t = os.date('*t'); -- get current date and time
    --[[
    print(os.date("%Y-%m-%d %H:%m:%S", os.time(t)));
    t.min = t.min - 9000; -- subtract 9000 minutes
    print(os.date("%Y-%m-%d %H:%m:%S", os.time(t)));
    print(t)
    ]]
    print(os.time(t))
    print("========================================")



    while true do
        i = i +1
        
        if i > 5 then
            break
        end
        
        local line = fh:read("*line")
        dt_parse(line)
        
        local s = string.gmatch(line, "\((.*)\) (.*)")
        for j in s do
            print(j)
        end
        
        if line == nil then
            break
        end
    end

end

-- run

run()