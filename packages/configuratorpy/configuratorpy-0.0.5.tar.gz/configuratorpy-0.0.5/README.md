# configuratorpy 

A macro way to read configuration files

# Installation

```Bash
pip install configuratorpy
```

# Usage

## Reading the configuration

```Python
from configuratorpy import Configurator

config = Configurator('app_config.toml')
config.load() # This will trigger the load, before you trigger the load, the configurator will not start the loading automaticly
```

`Configurator` will be initialized at your current working directory, and trying to find the configuration file name you have indicated.

## Getting or querying configuration values

Let's have a consumption that your configuration file is like this:

```TOML
[a]
aa = 1
[a.b.c]
d = 1
e = 2
f = 3
```

`Configurator` will use [benedict](https://github.com/fabiocaccamo/python-benedict) for getting the values from dict for you, so you can use the way like this:

```Python
config_item = config['a.b.c.d']
```

Then you'll get `1`.

Or, you can use the XQuery way(which will implemented by [dpath](https://github.com/dpath-maintainers/dpath-python), like this:

```Python
config_item = config['a/b/c/*']
```

Then you'll get`[1,2,3]`

## Loading Environment Variables

### Load dot env file

You can load the environment variables in dot env file by using the macro like this:
```Jinja2
{% load_env 'the/path/of/your/env.file' %}
```

### Reference env variables

You can access the environment variable like this:

```Jinja2
a = {{ 'THE VARIABLE' | env }}
```

or add a default value to it:

```Jinja2
a = {{ 'THE VARIABLE' | env('default value') }}
```

# Why configuratorpy

## Configuration is Hard

If you write scripts a lot, you'll understand why a configuration file is very useful. You can separate the code logic with the variables that doomed to be changed (test environment, UAT environment, live environment and so on).

The database connection string will be different, the resource path will be different, and maybe even the process flow can be different if you have a strong configuration requirement.

As we all know, configuration is code too. For most of the time, you should version control your configuration files too.

But how can you track and deploy the scripts by [Git](https://git-scm.com/) (so all source codes are the same in all places with same version, for local, test, UAT and live), and have different configurations for each script?

Environment variables come to help.

There is a [good article](https://www.doppler.com/blog/environment-variables-in-python) for this purpose, you should check it out. And you will know how to manage the configurations by using environment variables.

But, this is the only beginning.

## Why use [TOML](https://toml.io/en/v1.0.0)

[TOML](https://toml.io/en/v1.0.0) is a good syntax for configuration, it nearly have the same functionality as [YAML](https://yaml.org/), but has less annoyments:

* It use an [INI Syntax](https://www-archive.mozilla.org/projects/cck/docs/wizardmachine/syntax) to do the configuration, which is designed to be configuration file, much better than JSON, and easier to read than [YAML](https://yaml.org/)
* It don't use indent level as data structure, believe me, this will save lots and lots of time for you, take the flowing example by TOML and YAML, and you'll understand what I'm saying:

```YAML
abcdef:
 bcdef:
  cdef:
   def:
    ef:
     f: 1
```

```TOML
[abcdef.bcdef.cdef.def.ef]
f=1

```

The data structure of the two code are the same. But for YAML, since it use a indent structure to store the dict, when the level is deep, it will be quite a mess.

Besides, since TOML as a very compact language specification, it's loader is much smaller and efficient, as for YAML, you even need to [choose the Loader that fits for you](https://pyyaml.org/wiki/PyYAMLDocumentation), in fact, if you choose the wrong loader (say the full functional loader as FullLoader, it will be about 10 times slower than the C implementation of the Loader), even you use the one that implemented in C, YAML's load performance can be a little faster than the TOML one.

That's why you should use TOML than YAML.

## Why use Macros

TOML do have some drawbacks than YAML, first, it don't have any variable definition and reference in it. This will be quite annoying. Besides, you can't do the simple operations such as:

* Iteration: This is quite useful when you have complex configurations
* Increment, Decrement: This is quite useful for generating sequence names in your configuration file
* Variables: This is very crucial for configuration files
* Include: This is useful for you to separate configuration files into modules or based on categories, and will break down the big configuration file into small ones easier for management
* Functions, Filters: This is quite useful for you to reuse the logic, say, create UUID for each item in the list

Wait, can't you see, this is just the requirements for the Macro Engine.

Yes, that's why I use a template engine like [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) for this task.
