```python
from flask_srd import Consul,ConsulService
from flask import Flask

app = Flask(__name__)
consul = Consul(app,consul_host='10.1.1.7',consul_port=8500)
consul.apply_remote_config('my_kv_folder')
consul.register_service(
    name='app-server',
    service_id='app-server-sprint1',
    tag=['flask','service'],
    interval='5s',
    port=5000,
    address='10.1.1.1',
    http_check='http://10.1.1.1:500/healthcheck'
)

@app.route('/healthcheck')
def health_check():
    return '',200


@app.route('/another/<service>')
def communicate(service):
    client = ConsulService(service_name=service,nameservers=['10.1.1.7'],port=8600)
    return client.get('/').text

if __name__ == '__main__':
        app.run(debug=True,port=5000,host='0.0.0.0')

```

