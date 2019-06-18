# Neutron-perf

Centralized repo for EnOS based benchmarks on Neutron.
This includes a collection of scripts/examples/docs.

Currently the tests are made on vbox but having everything in this centralized
place would ease the transition to Grid'5000 in the future.

## Run on vagrant(vbox) on your local machine

Run `enos deploy`

## Run on vagrant(vbox) on a remote Grid'5000 machine

Rationale: bootstrap a vagrant(vbox) environment for testing/debugging purpose
on Grid'5000 (because we have bigger machine there)

Requirements:
- enoslib

## Run newest rally-openstack scenarios

Use case: run the following (unmerged) rally scenario : https://review.opendev.org/#/c/662781/

In this particular case we can't do it from EnOs directly because the patch
isn't a rally plugin (some core file seems modified --https://review.opendev.org/#/c/662781/ ).
Instead we'll have to run rally from the sources.

1. Install rally, the regular way [0] as a non-root user.

[0]:  https://rally.readthedocs.io/en/latest/quick_start/tutorial/step_0_installation.html

2. Install rally-openstack from the source. Checkout the right patchset:

```
source ~/rally/bin/activate
git clone https://github.com/openstack/rally-openstack
cd rally-openstack
git fetch https://review.opendev.org/openstack/rally-openstack refs/changes/81/662781/5 && git checkout FETCH_HEAD
pip install -U -e .
```

3. Add the existing deployment [1]

[1]: https://rally.readthedocs.io/en/latest/quick_start/tutorial/step_1_setting_up_env_and_running_benchmark_from_samples.html#id2

And run a task:

```
rally task start samples/tasks/scenarios/neutron/create-and-bind-ports.yaml
```
