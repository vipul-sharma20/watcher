## watcher
Utility tool to trigger commands on file changes

This was built to reload development servers like flask etc. that don't support
automatic reload on code changes.

> [!NOTE]
> This is a very lightweight wrapper around [`watchdog`][watchdog] and
> most people might as well use some existing tools out there. This will be
> mostly tailored to my personal projects and to solve the problems I face.

### Installation

```
pip install https://github.com/vipul-sharma20/watcher/releases/download/v0.1.0/watcher-0.1.0-py3-none-any.whl
```

### Usage

```
watcher run --config-yml=config.yml
```

#### Sample Config

```yaml
project_path: /path/to/project/

# relative to project_path
run_command:
  - python
  - dir/main.py

# relative to project_path
excluded_paths:
  - tests/
  - localstorage/
  - data/

# relative to project_path
excluded_files:
  - .*\.log$
  - .*\.tmp$
```

### Licence

MIT

[watchdog]: https://github.com/gorakhargosh/watchdog
