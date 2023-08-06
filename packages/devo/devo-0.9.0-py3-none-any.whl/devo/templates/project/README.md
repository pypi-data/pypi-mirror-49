# {{ project_name }}


## Local Development

### Setup Environment
Install the following tools:
* [Python 3.6+](https://www.python.org/)
* [skaffold 0.31](https://skaffold.dev/)
* [minikube 1.1.1](https://kubernetes.io/docs/tasks/tools/install-minikube/)
* [kubectl 1.14](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [kustomize 2.0.3](https://github.com/kubernetes-sigs/kustomize/releases)
* [devo](https://pypi.org/project/devo/)

Setup local k8s cluster
```bash
$> minikube start
```

Verify its availability
```bash
$> kubectl get nodes
```

### Run local instance of {{ project_name }}
```bash
$> skaffold dev --port-forward
# visit http://localhost:8000
```

### Run tests in local cluster
Make sure the local instance is running first (see above). 
```bash
$> devo kube test
```

{% if db %}
### Expose database on localhost
```bash
$> kubectl port-forward deployment/{{ project_name }}-db 5432:5432
```

### Provide custom secrets for production containers and sync to Gitlab
```bash
$> $EDITOR k8s/prod/prod.env
$> devo gitlab push k8s 

```

### Troubleshoot init-containers 
If the main application fails to start due to failing init-containers check the logs
```bash
$> kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
{{ project_name }}-app-<random_string>   1/1     Running   0          36m
{{ project_name }}-app-<random_string>   0/1     Init:CrashLoopBackOff   2          70s
{{ project_name }}-db-<random_string>   0/1     Running   0          84m
# Get logs for the crashing pod
$> kubectl logs {{ project_name}}-<random_string> -c init-migrate
# ... log output
```
{% endif %}

### Customize scripts
The following scripts are called for different tasks and may have to be customized depending on the project

* `scripts/dev` - Run a development server (e.g. with auto-reloading)
* `scripts/lint` - Run a linter on the `src/` folder (default: `flake8`)
* `scripts/prod` - Run a production server for remote deployments (e.g. uvicorn, gunicorn, uwsgi)
* `scripts/test` - Run tests found in `tests/` (default: `py.test`)
{%if db %}
* `scripts/migrate` - Run database migrations (e.g. django, alembic)
{% endif %}

