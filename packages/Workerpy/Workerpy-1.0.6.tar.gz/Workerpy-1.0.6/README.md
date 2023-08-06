# Worker

Libreria la implementacion de workes basados en kafka.


### Ejemplo

```python
from Workerpy import Manager, Worker, Options

@Manager.Define(
    Options(
        'DemoWorker', # Nombre del worker
        'gitlab_push', # Topico que escucha
        ['kafka:9092'] # Kafka Hosts
    )
)
class demo(Worker):
    def process(self, data):
        print(data)
```

> Los workes solo escuchan, no tienen posibilidad de responder