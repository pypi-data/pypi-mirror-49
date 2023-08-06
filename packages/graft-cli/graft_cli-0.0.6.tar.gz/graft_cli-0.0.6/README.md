# graft-cli

A command line utitily to provide services offered by graftpress (a graft-elm web 
framework).

## Usage

### To create a new graft project 

`graft-cli init <project_name>`

eg: `graft-cli init hello`


### To build project

Move to the project directory and run `graft-cli build`  

In our example:
   
`
$ cd hello
$ graft-cli build
`

### To get server up and running

`$ graft-cli debug`  

## Development

1. Use local package:

  `
  $ pip install -e .
  `

2. use black `black graft-cli` from time to time.
3. run test: `graft-cli test`.

