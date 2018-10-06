import ssl

from logzero import logger
import paho.mqtt.client as mqtt

from MqttDecorator import MqttDecorator
from Common.EventEngine import Scheduler

class EdgeAgent(MqttDecorator):
    def __init__(self, name = 'MQTT'):
        self.name = name
        self._connect_handler = None  # type: Optional[Callable]
        self._disconnect_handler = None  # type: Optional[Callable]
        self.topics = {}  # type: Dict[str, TopicQos]
        self.connected = False
        self.client = mqtt.Client()
        self.config = {}

        self.gui = None

    def _init_app(self):
        self.client.on_connect = self._handle_connect
        self.client.on_disconnect = self._handle_disconnect
        self.username = self.config.get("MQTT_USERNAME")
        self.password = self.config.get("MQTT_PASSWORD")
        self.broker_url = self.config.get("MQTT_BROKER_URL", "localhost")
        self.broker_port = self.config.get("MQTT_BROKER_PORT", 1883)
        self.tls_enabled = self.config.get("MQTT_TLS_ENABLED", False)
        self.keepalive = self.config.get("MQTT_KEEPALIVE", 60)
        self.last_will_topic = self.config.get("MQTT_LAST_WILL_TOPIC")
        self.last_will_message = self.config.get("MQTT_LAST_WILL_MESSAGE")
        self.last_will_qos = self.config.get("MQTT_LAST_WILL_QOS", 0)
        self.last_will_retain = self.config.get("MQTT_LAST_WILL_RETAIN", False)

        if self.tls_enabled:
            self.tls_ca_certs = self.config["MQTT_TLS_CA_CERTS"]
            self.tls_certfile = self.config.get("MQTT_TLS_CERTFILE")
            self.tls_keyfile = self.config.get("MQTT_TLS_KEYFILE")
            self.tls_cert_reqs = self.config.get("MQTT_TLS_CERT_REQS",
                                                ssl.CERT_REQUIRED)
            self.tls_version = self.config.get("MQTT_TLS_VERSION",
                                              ssl.PROTOCOL_TLSv1)
            self.tls_ciphers = self.config.get("MQTT_TLS_CIPHERS")
            self.tls_insecure = self.config.get("MQTT_TLS_INSECURE", False)

        # set last will message
        if self.last_will_topic is not None:
            self.client.will_set(
                self.last_will_topic,
                self.last_will_message,
                self.last_will_qos,
                self.last_will_retain,
            )

    def run(self):
        self._init_app()
        if self.username is not None:
            self.client.username_pw_set(self.username, self.password)

        # security
        if self.tls_enabled:
            self.client.tls_set(
                ca_certs=self.tls_ca_certs,
                certfile=self.tls_certfile,
                keyfile=self.tls_keyfile,
                cert_reqs=self.tls_cert_reqs,
                tls_version=self.tls_version,
                ciphers=self.tls_ciphers,
            )

            if self.tls_insecure:
                self.client.tls_insecure_set(self.tls_insecure)

        # Call mqtt client with another thread
        self.client.loop_start()

        res = self.client.connect(
            self.broker_url, self.broker_port, keepalive=self.keepalive
        )
        if res == 0:
            logger.debug(
                "Connected to broker {0}:{1}"
                .format(self.broker_url, self.broker_port)
            )
        else:
            logger.error(
                "Could not connect to MQTT Broker, Error Code: {0}".format(res)
            )

        if self.gui is not None:
            self.gui.init()
        # Run the event scheduler. This will block and run forever
        Scheduler(self.events, self.gui).run()


    def stop(self):
        # type: () -> None
        self.client.loop_stop()
        self.client.disconnect()
        logger.debug('Disconnected from Broker')

