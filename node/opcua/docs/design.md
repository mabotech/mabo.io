# Design



## Road-map

- HTTP server * socket.io
- Central configuration download
- Rule based action routing
- Reconnect
- Heart beat & server recovery


#Recipes

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

    try{

        the_session.write([                
            {
                nodeId:"ns=2;s=Channel1.Device1.MT",
                attributeId:opcua.read_service.AttributeIds.Value,
                indexRange: null,
                value: {value:  { dataType: "UInt16", value: vWord1 }}                
                } ,
            {
                nodeId:"ns=2;s=Channel1.Device1.Tag2",
                attributeId:opcua.read_service.AttributeIds.Value,
                indexRange: null,
                value: {value:  { dataType: "UInt16", value: vWord1 }}                
                }                    
            ],  
            function(err, statusCodes, diagnosticInfos){
                console.log(statusCodes);
        });
    }catch(err){
        console.log(err)
    }  