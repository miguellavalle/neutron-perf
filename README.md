# Neutron-perf

Centralized repo for EnOS based benchmarks on Neutron.
This includes a collection of scripts/examples/docs.

Currently the tests are made on vbox but having everything in this centralized
place would ease the transition to Grid'5000 in the future.

## Run on vagrant(vbox) on your local machine

Run `enos deploy`

NB: the configuration is set to use an external persistent registry. You can
start one on the host machine :

```
docker run -e "REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io" -p 0.0.0.0:4000:5000 --name registry -ti registry:2
```


## Run on vagrant(vbox) on a remote Grid'5000 machine

Rationale: bootstrap a vagrant(vbox) environment for testing/debugging purpose
on Grid'5000 (because we have bigger machine there)

Requirements:
- enoslib

## Run on Grid'5000 natively (bare metal machines)

Run `enos deploy -f reservation.yml`

## Run newest rally-openstack scenarios

Use case: run the following (unmerged) rally scenario : https://review.opendev.org/#/c/662781/

In this particular case we can't do it from EnOs directly because the patch
isn't a rally plugin (some core file seems modified --https://review.opendev.org/#/c/662781/ ).
Instead we'll have to run rally from the sources.

1. Install rally, the regular way [[0]] as a non-root user.

[0]:  https://rally.readthedocs.io/en/latest/quick_start/tutorial/step_0_installation.html

2. Install rally-openstack from the source. Checkout the right patchset:

```
source ~/rally/bin/activate
git clone https://github.com/openstack/rally-openstack
cd rally-openstack
git fetch https://review.opendev.org/openstack/rally-openstack refs/changes/81/662781/5 && git checkout FETCH_HEAD
pip install -U -e .
```

3. Add the existing deployment [[1]]

[1]: https://rally.readthedocs.io/en/latest/quick_start/tutorial/step_1_setting_up_env_and_running_benchmark_from_samples.html#id2

And run a task:

```
rally task start samples/tasks/scenarios/neutron/create-and-bind-ports.yaml
```


## Enable osprofiler in the deployment

In `reservation.yaml`:

```
kolla:
  [...]
  enable_osprofiler: true
  enable_elasticsearch: true
```

Related Rally documentation [[3]]

[3]: https://rally.readthedocs.io/en/latest/quick_start/tutorial/step_10_profiling_openstack_internals.html

Note that the HMAC key is hard-coded in EnOS:
`OSPROFILER_HMAC_KEY=79cca0a7b4fe3022077f1e1291dfccf9`. ( One can check the
`current/password.yml`)

To retrieve a trace, you need elasticsearch client installed:

```
pip install "elasticsearch>=2.0.0,<3.0.0"
```

The trace can be retrieved using:

```
osprofiler trace show --html --out trace.html 2931c692-3f37-43db-982a-692e37cc1e96 --connection-string elasticsearch://192.168.42.243:9200
```


