# CTF-590A
CTF built for UMass CS 590A - Spring 2021

## Running the system

- Build - `docker build -f deploy/dockerfile --tag ctf-590-ag:latest .`
- Run - `docker run -it --network host --rm --name ctf ctf-590-ag:latest`