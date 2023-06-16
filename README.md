# configuration files

This repo houses my configurations, personal scripts, etc.

## usage

The installation/bootstrap script requires Python, but otherwise there are no
prerequisites to using this. However, you'll get the best results if you have at
least set up 1Password (for SSH key) and Homebrew (to install all the packages).

1. clone this repo
2. make a copy of the context file:

    ```sh
    cp context.template.yaml context.yaml
    ```

3. fill in the context file
4. install `nox` and run the bootstrap script:

    ```sh
    VENV = /tmp/config-files-bootstrap
    python -m venv $VENV
    $VENV/bin/python -m pip install nox
    $VENV/bin/python -m nox -s bootstrap
    ```

### overwriting files

Existing files will not be overwritten by default. To overwrite files that
already exist, pass the `--force` argument:

```sh
nox -s config_files -- --force
```

You can see the changes that will be made with the `diff` session:

```sh
nox -s diff
```

### scripts/executables

Any file in the `bin/` directory will be copied to `$HOME/.local/bin/` with the
`bin` session. Any `.py` files in that directory will be automatically converted
to kebab-case and the file extension removed.

The Python scripts in the `bin/` directory can be tested with:

```sh
nox -s test_bin
```

## history

I used to keep these files in [another repo](https://github.com/samueljsb/qaz),
but I grew to dislike that tool for a few reasons:

- it used symlinks, so I could not separate code changes from applying new
  config
- it was untested
- it tried to be a sort of package manager, which is more than I need
- the configuration was confusing and in code

I have not copied over the git history for those files, but the repo is still
there for reference.
