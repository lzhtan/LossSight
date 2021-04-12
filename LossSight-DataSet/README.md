# LossSight-Dataset

A dataset on in-band network telemetry packet loss, tracking the long-term statistical results of two edge switches in Fat-Tree Network, including random loss (0.1%, 0.5%, and 1% three different random packet loss probabilities), congestion loss and blackhole loss.

Most file contains 100,000 pieces of INT Telemetry data. However, due to packet loss, the actual data volume is less than 100,000 rows, and the missing is the packet loss. each row contains 1 telemetry data, and contains two hops of telemetry results. The telemetry packet loss marking scheme uses MCM=8.

The file format of each line is:[INT Report TimeStamp] [Loss Bit] [SwitchID #1] [Qdepth #1] [SwitchID #2] [Qdepth #2]


# LossSight-Dataset

一个带内网络遥测丢包数据集，在Fat-Tree网络中跟踪两个边缘交换机的长时间的统计结果，包含随机缺失（0.1%、0.5%、1%三种不同的随机丢包概率）、拥塞缺失、黑洞缺失等多种丢包类型。

大多数文件应包含100000条数据，但由于丢包原因，实际数据量小于100000行，缺失数据即为丢包数据。每一行为1个遥测数据，包含两跳的遥测结果。遥测丢包标记方案采用MCM=8。

每行的文件格式为：[INT Report时间戳] [Loss Bit] [SwitchID #1] [队列长度 #1] [SwitchID #2] [队列长度 #2]
