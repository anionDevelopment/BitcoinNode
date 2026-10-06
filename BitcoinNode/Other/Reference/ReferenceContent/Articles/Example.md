# Example

The folder `Examples/MinimalDockerComposeFile` contains a minimal docker-compose-file which runs a node and stores its data and logs in the subfolder `Volumes` of that folder.

The example uses the image `bitcoinnode:<version>`, which is available locally after building the codeunit.

To start the example run `task beu` in the repository-folder (or run `python StartExample.py` in the example-folder).
To stop the example run `task bed` in the repository-folder (or run `python StopExample.py` in the example-folder).

Note that starting the example removes an existing `Volumes`-folder of a previous run of the example, so the node always starts with an empty data-directory.
