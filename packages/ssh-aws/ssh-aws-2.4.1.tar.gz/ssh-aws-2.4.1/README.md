awssh
----------------

SSH boto3 utility for AWS

Installation
----------------
First, install the aws-cli and boto3 libraries: 
```
pip install awscli --upgrade --user
pip install boto3
```
Next, set up credentials and default region:
```
aws configure
```
Finally, install the `awssh` utility:
```
pip install --user ssh-aws # or pip install ssh-aws
```

**Note**: The `awssh` utility is installed in `$HOME/Library/Python/2.7/bin` which may not be on PATH.
Consider adding this directory to PATH.

Version update
----------------
```
echo y | pip uninstall ssh-aws
pip install --no-cache --user ssh-aws
awssh --version
```


Requirements
----------------

- Python 2.7
- boto3
- aws-cli

Features
----------------

The `awssh` utility gives you a list of aws instances and preconfigures `ssh` with the proper key and user.
You can filter by instance name. If it matches only one instance you will be logged into it.
This utility also allows local and remote port forwarding for SSH tunneling (e.g. `ssh -L 9000:imgur.com:80 user@<ip_address>`).
By default, ssh command is executed with the -A option, which enables forwarding the authentication agent connection. 
This is particularly useful when using a single access point such as a jump server. 
In addition, if an instance without an external IP is selected, the utility attempts to find a bastion server and ssh with the -t option (e.g. `ssh -A ubuntu@<bastion> -t ssh <ip_address>`).

Usage
-----

```
usage: awssh [-h] [--users USERS [USERS ...]] [--region REGION]
             [-i KEY_PATH] [-c COMMAND] [-r REMOTE_HOST]
             [-p REMOTE_PORT] [-l LOCAL_PORT] [--keys KEYS]
             [--timeout TIMEOUT] [--console-output] [--profile PROFILE]
             [--version]
             [filter]

SSH into AWS instances.
e.g.: "awssh --profile prod-acc-2 --users fduran --region us-east-2 instance-name -c top".
The default user list is centos, ubuntu, and ec2-user:
e.g.: "awssh --profile prod-acc-2" will attempt ssh with default users.
Due to the nature of nargs, "awssh --users user1 user2 instance-name" will not be parsed properly. 
Instead try: "awssh instance-name --users user1 user2".

positional arguments:
  filter                Optional instance name or key word as a filter. If
                        only one instance is found, it will connect to it
                        directly.

optional arguments:
  -h, --help            show this help message and exit
  --users USERS [USERS ...]
                        Users to try (centos, ubuntu, and ec2-user are
                        defaults).
  --region REGION       AWS region (User default if non is provided).
  -i KEY_PATH, --key-path KEY_PATH
                        Specific key path, overrides, --keys
  -c COMMAND, --command COMMAND
                        Translates to ssh -t
  -r REMOTE_HOST, --remote-host REMOTE_HOST
                        Open a tunnel. Equivalent to ssh -L <local-port
                        >:<remote-host>:<remote-port> <selected-aws-host>
  -p REMOTE_PORT, --remote-port REMOTE_PORT
                        Port to use on the remote host (default is 5432).
  -l LOCAL_PORT, --local-port LOCAL_PORT
                        Port to use on the local host. Get overwritten by
                        remote port if not defined.
  --keys KEYS           Directory of the private keys (~/.ssh by default).
  --timeout TIMEOUT     SSH connection timeout.
  --console-output, -co
                        Display the instance console out before logging in.
  --profile PROFILE     Use a specific profile from your credentials file.
  --version, -v         Returns awssh's version.


  Examples:
    awssh --users fduran --profile prod-acc-2 --region us-east-2
    awssh --users user1 user2 --region us-east-2 --keys '~/.ssh' instance-name
    awssh instance-name --users user1 user2

```
