# Span

Span is a platform that makes it easy to deploy machine learning pipelines.

An example of a Span project can be found [here](https://github.com/basisai/span-example).

## Development

### Prerequisites

- Python 3.7
- Working Google Kubernetes Engine instance, which includes a Kubernetes configuration file that must be located at `/home/$USER/.kube/config` and a Google Application Credentials (JSON) file.
- Vault CA cert and token file, which can be obtained following these [instructions](https://github.com/basisai/Just-Read-The-Instructions/blob/master/vault.md).
- [SSH tunnel](#ssh-tunnel) requires installing `sshpass` and setting up [cluster contexts](#cluster-contexts).

### Local Development with Docker

```bash
# get the source code
git clone git@github.com:basisai/span.git
cd span/

# start the application
# GOOGLE_APPLICATION_CREDENTIALS defaults to `${HOME}/.config/gcloud/application_default_credentials.json` if unset.
#   To obtain this file, please refer to https://github.com/basisai/Just-Read-The-Instructions/#application-default-authentication
# VAULT_CACERT defaults to `${HOME}/.vault-ca.pem` if unset.
# VAULT_TOKEN defaults to `${HOME}/.vault-token` if unset.
# Use -t flag to open a tunnel into Kube cluster. See "Cluster Contexts" and "SSH Tunnel" sections for more details.
./launch_dev.sh -c [-t <cluster_context>] start

# stop the application
./launch_dev.sh -c stop
```

### Cluster Contexts

The `~/.kube/config` file can be set up to facilitate working with multiple clusters and namespaces (more details [here](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)). Please use this reference config as a quick starting point for configuring your cluster contexts to work with the [SSH tunnel](#ssh-tunnel).

Notes:

- `kubectl` overwrites the kube config file when updating access tokens, changing the format in the process. Hence, please double check your indentation when merging this reference config with an existing one. A known issue is that `kubectl` does not indent the second-level lists, whereas our autoformatter does.
- `kubectl` requires full paths for `cmd-args` and `cmd-path` in the `users` section (e.g. `~` and `$USER` will not be expanded).

<details><summary>Reference ~/.kube/config</summary>
<p>

```yaml
apiVersion: v1
clusters:
  - cluster:
      certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURDekNDQWZPZ0F3SUJBZ0lRV3dCZEpSRDgyYzhFbG5VQW9VUmFPREFOQmdrcWhraUc5dzBCQVFzRkFEQXYKTVMwd0t3WURWUVFERXlSbFl6TmlNalZrTkMxa05tWmhMVFEyTlRVdE9Ua3pZUzA1TnpBM01HSTNObVE1WXpZdwpIaGNOTVRrd016QTNNRFEwTWpNd1doY05NalF3TXpBMU1EVTBNak13V2pBdk1TMHdLd1lEVlFRREV5UmxZek5pCk1qVmtOQzFrTm1aaExUUTJOVFV0T1RrellTMDVOekEzTUdJM05tUTVZell3Z2dFaU1BMEdDU3FHU0liM0RRRUIKQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUUNVNmRINEhyajdoSEZuS0gvdWlFMnBQN3lYa0oxNmJCWE9aK1hWdlp6dwowdDVsVk5pUUdWQVNNK1ZDNGJGYTd0NVRNRW1BeXZHS3YvOEpneEgrbE1ZSkp5L2x1cGYvdVphL2J3M21tblI1CnRNNnJjZUJXQ0VXU2V1ZktiY09ybWowWWJialVVV1pFOWZ6Z0hOV0VEaXF0c0VPdWs2MXUweFl0WDVZRThkancKY3lOL1FtRENOTXFzL0Z4TVN2TWp3eFdyYUhxZWNuNjg0V1BrbWQ5VmlkMTVIdkg1TmljaW4zU1I0VGUzMGZXdgoyQXNYcG96aTNUMFlTUzlTTXV5dk96NlR4bE5OSUJUS2FSOUpLcmIyNGdSVGVvb2pGcElzQm13dWpYTGJJSm56CkRhWk5lL2xhTVduMmkvMVc3N0RhVmkzbjJHVThMUmR3N2JYRFVRU0M0dVNqQWdNQkFBR2pJekFoTUE0R0ExVWQKRHdFQi93UUVBd0lDQkRBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUEwR0NTcUdTSWIzRFFFQkN3VUFBNElCQVFCbgpmRUlNUTZ4TjRTYnAyTERWZkt5ZllDN3dXejRydTlFeHZzQWRibWEvM0U3VmJuUkcrRllQZjYrUGtvbS9OSE9kCktjYjdoMmM5MEs4cDJsYTk5WGRKU2hRaTZWYWpiQ1lxazZxbEZIN21jRnM0djFSZTBkbURRRzFGTFJIcFlRRGsKcmhaN2hZcXdISHM0elRZUGw5Zy9MTzY3MTlkWUxSait1YUpPVW9KK0xGYmRIcnF5NlhVK200RFNHNE9DV2MzdQpLRGhMWVVnUVR2ZFg1b2ZHKzk1OTFpcVhtL216TWVXWGdEY2RqYmppWjBlNmJTOHBva3FBRzJrazlSZFo2K2ZHCjNvc1VBQnh2NHZLTlVTSFhFcUxKNnRRejhMVVZHVjVySUpKMGFlRGxYQllYVjgxV2Q4Q1JmTUg2NWI0V0g3U3MKeGRFSkY3VkduUnMxYVBkYUJkWkwKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
      server: https://35.197.148.156
    name: canary-dev-cluster
contexts:
  - context:
      cluster: canary-dev-cluster
      namespace: deployment
      user: canary-dev-user
    name: canary-dev-deployment
  - context:
      cluster: canary-dev-cluster
      namespace: training
      user: canary-dev-user
    name: canary-dev-training
current-context: canary-dev-training
kind: Config
preferences: {}
users:
  - name: canary-dev-user
    user:
      auth-provider:
        config:
          cmd-args: config config-helper --format=json
          cmd-path: /usr/lib/google-cloud-sdk/bin/gcloud
          expiry-key: "{.credential.token_expiry}"
          token-key: "{.credential.access_token}"
        name: gcp
```

</p>
</details>

Vault CA cert and token details [here](https://github.com/basisai/Just-Read-The-Instructions/blob/master/vault.md).

### SSH Tunnel

The SSH tunnel allows pods within a Kubernetes cluster to reach an endpoint on your local dev machine. The launch script automates these steps:

1. Start deployment of sshd using Docker image built from https://github.com/basisai/span-trojan.
2. Manage deployment using a NodePort service and a ClusterIP service. The NodePort allows connecting to port 22 on the sshd pod from a dynamically determined port on all nodes. The ClusterIP allows all other pods in the cluster to reach the sshd pod using a known service name and port (script uses `$(whoami)-tunnel:8000`).
3. Establish a reverse SSH tunnel from your local dev machine to the pod running sshd (-R flag), via the NodePort service. The first node that has "Ready" status is used. The SSH command sets up a port forwarding listener on port 8000 of the sshd pod. When other pods in the same cluster send traffic to the ClusterIP service on port 8000, this traffic will now be forwarded to port 8000 on the sshd pod, then to port 8000 on your local dev machine.
4. Delete the deployment and services when the script exits.

Notes:

- Requires installing sshpass. (Requirement will be removed once we switch to Let's Encrypt)
- No cross-cluster support. Use any one of the `canary-dev` contexts to allow pods on that cluster to reach your dev machine.

### Code formatting

Run `isort` (for sorting imports) and `black` (for general code formatting).

```bash
./test-fix.sh
```

### Application Authentication and Authorization

See the [documentation](docs/auth.md).

## Testing

```bash
# set up and activate a Python virtual environment
python3.7 -m venv venv
source venv/bin/activate

# install dependencies and dev dependencies
pip install -r requirements.txt -r requirements-dev.txt

# run all tests
./test.sh
```

## Known Issues

1. The `ephemeral_storage` setting when submitting pipeline runs is currently disabled to mitigate this [issue](https://github.com/kubernetes/autoscaler/issues/1869).
