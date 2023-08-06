# RunCommands

RunCommands is a preprocessor that allows to execute a sequence of arbitrary external commands.

## Installation

```bash
$ pip install foliantcontrib.runcommands
```

## Usage

To enable the preprocessor, add `runcommands` to `preprocessors` section in the project config, and specify the commands to run:

```yaml
preprocessors:
    - runcommands:
        commands:
            - ./build.sh
            - echo "Hello World" > ${WORKING_DIR}/hello.txt
        targets:
            - pre
            - tex
            - pdf
            - docx
```

`commands`
:   Sequence of system commands to execute one after the other.

`targets`
:   Allowed targets for the preprocessor. If not specified (by default), the preprocessor applies to all targets.

### Supported environment variables

You may use the following environment variables in your commands:

* `${PROJECT_DIR}` — full path to the project directory, e.g. `/usr/src/app`;
* `${SRC_DIR}` — full path to the directory that contains Markdown sources, e.g. `/usr/src/app/src`;
* `${WORKING_DIR}` — full path to the temporary directory that is used by preprocessors, e.g. `/usr/src/app/__folianttmp__`;
* `${BACKEND}` — currently used backend, e.g. `pre`, `pandoc`, or `mkdocs`;
* `${TARGET}` — current target, e.g. `site`, or `pdf`.
