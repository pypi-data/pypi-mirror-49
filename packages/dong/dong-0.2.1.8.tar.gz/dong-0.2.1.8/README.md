![dong](https://raw.githubusercontent.com/libgirlenterprise/dong_mnist_example/master/dong_logo.png)

MLOps platform for real world AI engineer [dong.libgirl.com](http://bit.ly/dong_pre_alpha)

--- 

[Sign up](https://dong.libgirl.com/zh/signup/) before using dong 


---

## Installation

```bash
pip install dong
```

## Usage

```
$ dong
Usage: dong [OPTIONS] COMMAND [ARGS]...

  Universal Command Line Interface for Libgirl AI Platform

Options:
  --help  Show this message and exit.

Commands:
  Version   Print version and exit.
  endpoint  Operate on endpoint.
  help      Show this message and exit.
  init      Create a new ML project in an existing directory.
  login     Login with your credentials.
  new       Create a new ML project
  template  Generate module files from template, if not provided, the...
  train     Training job.
```

### Init
```sh
dong init #Create a new ML project in an existing directory.
```

### New
```sh
dong new [argument] #Create a new ML project
```
### Train

```
$ dong train
Usage: dong train [OPTIONS] COMMAND [ARGS]...

  Training job.

Options:
  --help  Show this message and exit.

Commands:
  exec    Execute training job.
  kill    kill running job.
  status  Retrieve training status, training message note.
```

### Endpoint
```
$ dong endpoint
Usage: dong endpoint [OPTIONS] COMMAND [ARGS]...

  Operate on endpoint.

Options:
  --help  Show this message and exit.

Commands:
  kill    kill running endpoint.
  status  Retrieve endpoint status.
  up      Bring up endpoint to serve.
```


## Author
Team Libgirl(team@libgirl.com)

## License
Licensed under the Apache License 2.0 License.

## Link 
Introduction page [dong.libgirl.com](http://bit.ly/dong_pre_alpha)
