


-module(timer01).

-export([timer/0]).


timer() ->

    receive
    
    after 100 ->
    
        io:format("hi"),
        
        timer()
        
    end.
    
    

main(_) ->

    spawn(timer).