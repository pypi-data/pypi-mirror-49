# graftpress-cli

A command line utitily to provide services offered by graftpress (a graftpress web 
framework).

## Usage

### To create a new graft project 

`graftpress-cli init <project_name>`

eg: `graftpress-cli init hello`


### To build project

Move to the project directory and run `graftpress-cli build`  

In our example:
   
`
$ cd hello
$ graftpress-cli build
`

### To get server up and running

`$ graftpress-cli debug`  

## Development

1. Use local package:

  `
  $ pip install -e .
  `

2. use black `black graftpress-cli` from time to time.
3. run test: `graftpress-cli test`.

