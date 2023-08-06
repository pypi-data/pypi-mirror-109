# Docker-cli
 
A straight forward tool to get information from docker command line and try to parse into json format as far as possible.

## Why not docker api?
- The api schema might change and response data might change so often.
- Docker-cli uses docker cli to get response and try to format them into json format

## Installation
`pip install docker-cli`

## Main methods
- `is_docker_set()` to verify docker installation and availability
```bash
 docker_cli.is_docker_set() 
```
- To run docker commands
```bash
 Request: docker_cli.docker("ps") 
 
 Response Structure:
 DockerResponse(command='docker ps', status='SUCCESS', type='JSON', data=[<JSON Data>])

```
- To run docker commands
```bash
 Request: docker_cli.docker_compose("up -d") 
 
 Response Structure:
 Similar as that of docker commands
```