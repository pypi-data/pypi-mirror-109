# AD-Logger

### Example
```python
from ad_logger import logger,KafkaHandler

kafka_producer = {
    'bootstrap_servers': ["localhost:9094"],
    # 'sasl_plain_username': USERNAME,
    # 'sasl_plain_password': PASSWORD,
}

logger.add(KafkaHandler('ad_logger', 'log_center.dev', use_queue=False, kafka_producer=kafka_producer),
           format="{message}", level="INFO")


def test_logger():
    logger.debug("this is debug")
    logger.info("this is info")
```