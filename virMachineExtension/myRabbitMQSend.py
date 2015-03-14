# coding: utf-8
'''
Created on 2014年11月7日

@author: cuimingwen
'''
import json, pika
import libvirtUtil

class MyRabbitMQ(object):
    '''
    classdocs
    '''
    def __init__(self, host='10.66.32.18', username='guest', password='incito'):
        '''
        Constructor, Initiate a connection to the RabbitMQ server
        
        @param host RabbitMQ server host
        @param username RabbitMQ server username
        @param password RabbitMQ server user's password
        @param exchange  name of exchange
        @param routingKey binding key
        @param qname Name of the queue to create
        '''
        self.host = host
        self.username=username
        self.password = password
        self.qname = 'myceilometerExt'
        self.routingKey= self.qname
        self.exchange = 'myceilometer_exchange'
        self.conn = self.connection()
    
    def connection(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
            conn = pika.BlockingConnection(parameters)
        except Exception as  e:
            print "connect  rabbitMQ failed", e
            return  -1
        else:
            return conn
        
    def getChannel(self):
        " get a channel"
        if self.conn == -1:
            return None
        else:
            return self.conn.channel()

    def sendMsg(self, msgBody):
        """ send  message  body
        
        @param msgBody  msgbody
        @param durable will the server survive a server restart
        @param auto_delete should the server delete the exchange when it is 
        no longer in use
        """
        if self.getChannel() is None:
            return None
        print "now  send msg start, msgBody:", msgBody
        sendChannel = self.getChannel()
        sendChannel.exchange_declare(exchange=self.exchange, 
                                 exchange_type="direct", 
                                 passive=False, 
                                 durable=True, 
                                 auto_delete=False)
        sendChannel.queue_declare(queue=self.qname)
        sendChannel.queue_bind(queue=self.qname, 
                           exchange=self.exchange, 
                           routing_key=self.routingKey)
        sendChannel.basic_publish(exchange=self.exchange, 
                              routing_key=self.routingKey,
                              properties=pika.BasicProperties(
                                content_type='application/json'),
                               body=msgBody)
        
    
    def callback(self, method, mproperty, queue, msgBody):
        data = json.loads(msgBody)
        print "[x] Received %r"%(data,)


            
    def start_consuming(self,callback, queue=None, no_ack=False):
        """
        Start a consumer and register a function to be called when a message is consumed
        @param callback function to call
        @param queue_name name of the queue
        @param consumer_tag a client-generated consumer tag to establish context
        @param no_ack Tell the broker to not expect a response
        """
        consumeChannel = self.getChannel()
        if consumeChannel is None:
            return None
        try:
            print "start  receive  msg  !!!"
            consumeChannel.basic_consume(callback, 
                                         queue=self.qname,
                                #consumer_tag="myCeilometerExtTag", 
                                         no_ack=True) 
        except Exception as e:
            print "errcode :", e
            
    def receiveMsg(self):
        self.start_consuming(self.callback)
        #self.wait()
        
    #cut it        
    def stop_consumer(self, consumer_tag="myCeilometerExtTag"):
        """
            Cancel a consumer.
            @param consumer_tag a client-generated consumer tag to establish context
        """
        consumeChannel = self.getChannel()
        consumeChannel.basic_cancel(consumer_tag)
        
    #cut it   
    def wait(self):
        """
        Wait for activity on the channel
        """
        while True:
            consumeChannel = self.getChannel()
            consumeChannel.wait()
        
    def __del__(self):
        if self.conn is not -1:
            self.getChannel().close()
            self.conn.close()
            
if  __name__=='__main__':
    r = MyRabbitMQ()
    c = libvirtUtil.MyLibvirt()
    meminfo = c.get_memory()
    diskinfo = c.get_disk_info()
    interfacePath = c.get_disk_path()
    #interfaceinfo = c.get_interface_bandwidth()
    for myL in [meminfo, diskinfo, interfacePath]:
        for conte in myL:
            msgStr = json.dumps({'myceilometerExt':conte})
            r.sendMsg(msgStr)
    
