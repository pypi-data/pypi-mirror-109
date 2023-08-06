# rabbitmq-tool
A RabbitMQ CLI

**Features**:
- manage bindings
- inspect exchanges and queues
- show all exchanges and queues
- create and delete exchanges and queues


## Installation
```
pip install rabbitmq-tool
```

## Usage Examples
See `--help` for more information.

### Create exchange
```
$ rabbitmq-tool --url http://localhost:15672 --username guest create-exchange myexchange

```

### Create queue
```
$ rabbitmq-tool --url http://localhost:15672 --username guest create-queue myqueue
```

### Bind exchange and queue
```
$ rabbitmq-tool --url http://localhost:15672 --username guest bind --exchange myexchange --queue myqueue --routing '#'
```
