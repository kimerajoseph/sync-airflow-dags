2. you can assign each worker a label and run tasks on a specific worker. Done by defineing nodeSelector in the k8s executor in the executor_config argument of your Operator
3. All pods are based on core image with airflow and dependencies pre-installed. saves time at runtime

## LINK
https://www.bhavaniravi.com/apache-airflow/deploying-airflow-on-kubernetes
https://www.clearpeaks.com/deploying-apache-airflow-on-a-kubernetes-cluster/

# create cluster 
minikube start

# create a namespace
kubectl create namespace airflow

# build image
docker build -t airflow-custom:1.0.0 .

# add image to local refistry
eval $(minikube docker-env)

# install airflow on minikube cluster
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug

# get default config file
helm show values apache-airflow/airflow > values.yaml

# expose airflow UI
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

# check providers
kubectl exec airflow-webserver-d8b87b6c8-686kf -n airflow -- airflow providers list

# TO USE gitSync, follow the procedure below
# create secret key (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

# create secret in namespace
kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshKey=/home/ec2-user/.ssh/git_key.pub -n airflow

# configure gitSync in values.yaml file
gitSync:
enabled: true
repo: ssh://git@github.com/marclamberti/airflow-2-dags.git
branch: main
rev: HEAD
root: "/git"
dest: "repo"
depth: 1
subPath: ""
sshKeySecret: airflow-ssh-git-secret

## ENABLE EXAMPLES 
extraEnv: |
- name: AIRFLOW__CORE__LOAD_EXAMPLES
    value: 'True'