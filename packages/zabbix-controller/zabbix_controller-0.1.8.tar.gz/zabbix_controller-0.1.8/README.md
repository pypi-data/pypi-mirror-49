# Zabbix CLI
This software is released under the MIT License, see LICENSE.txt.
## Example
### Valid Command
`zabbix_controller -u username -p password hosts list`

`zabbix_controller -u username -p password hosts -m name:^server$ list`
### Invalid Command
`zabbix_controller hosts -u username -p password list`

`zabbix_controller -u username -p password hosts list -m name:^server$ `

## zabbixctl [options] command ...
### Options
These options are only set at `zabbixctl [options] command ...`.
`zabbixctl command [options] ...` is not accepted.
#### --help
```bash
zabbixctl --help
```
#### --apiserver-address, -aa
```bash
zabbixctl -aa http://localhost:8081
```
#### --username, -u, --password, -p
Used for zabbix login
```bash
zabbixctl --username Admin --password zabbix_password
```
#### --basicauth_username, -bu, --basicauth_password, -bp
Used for basic authentication
```bash
zabbixctl -bu alis -bp alis_password
```
#### --dry-run
If you set `--dry-run`, only get API is executed, then ZabbixCTL state is printed.
Create, update, delete like API is not executed.
```bash
zabbixctl --dry-run
```

## zabbixctl host `Options` `Command` ...
### Options
#### `-m, --match`
Search host using json like object.
Search key, then apply value.
In the example below, 
hosts which name key is including `some_name` is listed.
```bash
zabbixctl hosts -m '{"name": "some_name"}' list
zabbixctl hosts -m '[{"name": "some_name"}]' list
```
Each key, value pairs are chained by `and operator`.
Each dicts are chained by `or operator`.

This command mean `("name": "some_name" and "hostid": "^1") or "name": "other_name"`.
```bash
zabbixctl hosts -m '[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]' list
```

#### `-tr, --time-range`
This option is able to specify time range.
If you use --match at the same time, used by "and operator".
```
key:[from]-[to]
```
`from` and `to` must be unixtime and can be omitted.
These commands are same and print host which disable property is included from 0 to now.
```bash
zabbixctl hosts -tr disable:0- list
zabbixctl hosts -tr disable:- list
```
This command mean `(("name": "some_name" and "hostid": "^1") or "name": "other_name") and (0 <= disable_until <= now)`.
```bash
zabbixctl hosts -m '[{"name": "some_name", "hostid": "^1"}, {"name": "other_name"}]' -tr 'disable_until:-' list
```


### Commands
#### `list`
list up host
#### `delete`
delete host
- options
    - `-y, --yes`
```bash
zabbixctl hosts -m '{"name": "some_name"}' delete -y
```
#### `disable`
disable host
- options
    - `-y, --yes`
```bash
zabbixctl hosts -m '{"name": "some_name"}' disable -y
```
#### `update`
update host
- options
    - `-d, --data`
    - `-y, --yes`

These are same command.
```bash
zabbixctl hosts -m '{"name": "some_name"}' update -d '{"state": 1}' -y
zabbixctl hosts -m '{"name": "some_name"}' update -d '{"state": "1"}' -y
zabbixctl hosts -m '{"name": "some_name"}' disable -y
```

## zabbixctl host graphs `Options` `Command`
### Command
#### `list`
#### `delete`
- options
    - `-y, --yes`
### Options
#### `-m, --match`

This command delete graphs which is in hosts which is matched regex.
```bash
zabbixctl hosts -m '{"name": "some_name"}' graphs delete -y
```

## zabbixctl host interfaces `Options` `Command`
### Command
#### `list`
#### `usedns`
Use dns, not ipaddress
- options
    - `-y, --yes`

#### `update`
These are same command.
- options
    - `-y, --yes`
```bash
zabbixctl hosts update -d '{"useip": 0}' -y
zabbixctl hosts update -d '{"useip": "0"}' -y
zabbixctl hosts usedns -y
```
