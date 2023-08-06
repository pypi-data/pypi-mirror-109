[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# 🏊 Jupyterpool

> Jupyterpool, instant Jupyter Kernels and Servers.

Jupyterpool maintains a pool of remote Jupyter kernels and servers living on a [Kubernetes](https://kubernetes.io) cluster.

This allows to remove the `cold-start` issue user face having when launching a notebook on [Binder](https://mybinder.org) or [JupyterHub](https://github.com/jupyterhub). While requesting a Kernel (python, julia, dask...), a user will also request datasets to be mounted.

We are building Jupyterpool on top of the [upcoming Kernel Enviroment Provisioning](https://github.com/jupyter/jupyter_client/issues/608).

```bash
# Setup your development environment.
conda deactivate && \
  make env-rm # If you want to reset your env.
make env && \
  conda activate jupyterpool
```

```bash
# Clean, install and build.
make clean
make install
make build
```

```bash
# Start the storybook.
echo open http://localhost:9001
make storybook
```
