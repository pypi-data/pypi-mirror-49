# AwesomeBuild

## Philosophy

Like a Makefile Awesomebuild is structured in rules. Each rule may depend on other rules and may include so called _triggers_ which are used to check whether the rule needs to run.

## Usage

usage: AwesomeBuild [-h] [--config CONFIG] [targets [targets ...]]

Awesome build manager to replace Makefiles. It allows very fast building!

positional arguments:
  targets          defaults to the main rule defined in the config file

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  default: awesomebuild.json

## Configuration

First of you need to create a configuration file in your projects man directory called `awesomebuild.json`.

```json
{
  "project": "TestProject",
  "import": {
    "rules": []
  },
  "main": "mainrule",
  "rules": {}
}
```
Empty fields can be omitted.

Field overview:

`project`: project name

`ìmport`: Here you can define whixh external configuration files you want to import. The currently only known import type is `rules`.

`main`: This defines which rule to run if no targets were defined by the user. This rule may be defined in an external configuration file.

`rules`: Here you can define rules.

### Rule Definition

```json
"rule-name": {
  "cmd": [
    "cmd1",
    "cmd2"
  ],
  "call":[
    "other-rule-1",
    "other-rule-2"
  ],
  "callBefore": [
    "other-rule-3",
    "other-rule-4"
  ],
  "callAfter":"other-rule-5",
  "trigger": [],
}
```
All fields may be omitted, provided as single value or list.
`"field": "hello world"` is the same as `"field": ["hello world"]` and `"field": []` is the same as omitting `field`.

`cmd`: This field handles shell commands to execute. All commands run in the main project directory.

`call`: This field handles other rules which are needed to run.

`callBefore`: This field handles all rules that need to run before.

`callAfter`: This field handles all rules that need to run after. There is a little difference to `call`. Check [Rule Execution](#rule-execution)

`trigger`: This field handles the rule´s triggers.


#### Trigger Definition
```json
{
  "type": "trigger type",
  "subtype": "trigger sub type",
  "value": "value for trigger"
}
```

Currently known triggers are:

type | subtype | value usage
--- | --- | ---
file | changed | path to file
file | exist | path to file
file | not exist | path to file
directory | changed | path to directory
directory | exist | path to directory
directory | not exist | path to directory

### Import Rules

```json
{
  "rules": "name",
  "type": "importtype",
  "value": "path"
}
```

Field overview:

`rules`: This can either be the name of a single rule `"rules": "rulename"`, a list of rules `"rules": ["rule-1", "rule-2"]` or a wildcard `"rules": "*"` to import all rules found.

`type`: This defines whether a single file or a whole directory (recursively) is imported.

`value`: This defines the path to the file or directory.

## Rule Execution
1. If `callBefore`-rules are defined, these rules will run now. If any of these were executed now the run variable will be set.
2. If `trigger`s are defined, these will be checked now. If any of these triggers was positive or no triggers were defined, the run variable will be set
3. If the run variable is set, the `cmd`s will run now.
4. If the run variable is set, the `call`-rules will run now.
5. If `callAfter`-rules are defined, these rules will run now.
