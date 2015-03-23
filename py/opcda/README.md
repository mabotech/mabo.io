


## 原有设计

创建多个group，每个group单独轮询OPC Server。

当某一个轮询发现OPC Server connection断开后，需要加锁、重连、解锁。

对于单个设备点。无需枷锁？


