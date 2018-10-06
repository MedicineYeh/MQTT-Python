
# This class is just a named structure to wrap the variables for a topic
class Topic():
    def __init__(self, topic = '', qos = 0):
        self.topic = topic
        self.qos = qos

class mqttTopics():
    def myTopic(id = ''):
        return Topic('/my/topic/{0}/cmd'.format(id), 1)

