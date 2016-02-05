

function fun_diff( t )
    print("===========================")
    --print("maxn: ", table.maxn( t ))
    print("   #: ", # t )
    -- print("getn: ", table.getn( t ))
end


fun_diff({3,8,9})
fun_diff({[1]=3,[3]=9})
fun_diff({[3]=9})