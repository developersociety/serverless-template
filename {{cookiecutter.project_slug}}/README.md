# {{ cookiecutter.project_name }}

## Development setup

It's recommended you use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
and [The Developer Society Dev Tools](https://github.com/developersociety/tools).

Presuming you are using those tools, getting started on this project is pretty straightforward:

```console
$ dev-clone {{ cookiecutter.project_name }}
$ workon {{ cookiecutter.project_name }}
$ make reset
```

You can now run the development server:

```console
$ make serve
```
