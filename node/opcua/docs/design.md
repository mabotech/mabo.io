# Design



## Road-map

- HTTP server * socket.io
- Central configuration download
- Rule based action routing
- Reconnect
- Heart beat & server recovery


## Read


## Write

**writeSingleNode**

	try{
	    the_session.writeSingleNode("ns=2;s=Channel1.Device1.Tag1",
	        { dataType: "UInt16", value: vWord1 },   // UInt16 - Word (Kepware)
	        function(err, statusCodes, diagnosticInfos){
	            console.log(statusCodes);
	    });
	}catch(err){
	    
	}
      
**write**

  