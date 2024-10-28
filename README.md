# Actor Degrees of Separation

A command-line tool to calculate the degrees of separation between actors in the movie industry.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/pakomin/challenge2015.git 
   
## Usage
2. In the command line execute:
   ```commandline
   ./degrees <actor-url-1> <actor-url-2>"

## Typical runtimes
1. For same actor-urls: ~1 second
2. For actors 1-hop separated: ~15 seconds
3. For actors 2-hop separated: ~15 minutes
4. For actors 3-hop separated: ~50 minutes

# TODO: Future improvements
1. parallelize using asyncio
2. Reduce runtime to less than 5minutes per call for all actors

## Credits
1. Pulkit Manocha