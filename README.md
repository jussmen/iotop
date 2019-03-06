# iotop
iotop command that can run on F5 BigIP. It lists the top 10 processes of Read and Write in the interval.
The data sorce is, read_bytes and write_bytes in /proc/PID/io and /proc/PID/task/io.

man PROC(5)
http://man7.org/linux/man-pages/man5/proc.5.html

# Problem
F5 BigIP does not have useful linux commands that make difficult to understand which process is writing/reading most

# Options
You do not need any argument or you can specify an interval

-i / --interval : Specify interval in seconds. Default is 2 seconds

# How to use
1. Copy iotop to your BigIP, such as /shared/
2. Give permission 

chmod +x /shared/iotop

3. Run

/shared/iotop

# Output Sample
```
----------------------------------------------------------------------------------------------------
2019/03/06 10:33:53

Readers                                                Delta Bytes     Source File         
/usr/bin/chmand                                            2048.0     /proc/8844/io       

Writers                                                Delta Bytes     Source File         
/usr/share/dosl7/bin/dosl7d                               12288.0     /proc/25501/io      
----------------------------------------------------------------------------------------------------
2019/03/06 10:33:55

Readers                                                Delta Bytes     Source File         
/usr/bin/chmand                                            4096.0     /proc/8844/io       

Writers                                                Delta Bytes     Source File         
/usr/share/dosl7/bin/dosl7d                               12288.0     /proc/25501/io      
/usr/lib/jvm/jre/bin/java                                  8192.0     /proc/25827/io      
asm_config_server_rpc_handler_async.pl                     4096.0     /proc/10260/io      
----------------------------------------------------------------------------------------------------
2019/03/06 10:33:58

Readers                                                Delta Bytes     Source File         
/usr/bin/chmand                                            7168.0     /proc/8844/io       

Writers                                                Delta Bytes     Source File         
/usr/sbin/mysqld                                         106496.0     /proc/30542/io      
/usr/share/dosl7/bin/dosl7d                               12288.0     /proc/25501/io      
/usr/lib/jvm/jre/bin/java                                  8192.0     /proc/25827/io      
asm_config_server_rpc_handler_async.pl                     4096.0     /proc/10260/io      
/usr/bin/perl                                              4096.0     /proc/9952/io       
/usr/bin/perl                                              4096.0     /proc/10188/io      
----------------------------------------------------------------------------------------------------
```
