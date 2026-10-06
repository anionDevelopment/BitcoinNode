# BitcoinNode reference

BitcoinNode is a docker-image which runs a [Bitcoin Core](https://bitcoincore.org)-node (`bitcoind`) in a docker-container.

The image contains the unmodified release-binaries of Bitcoin Core, which are downloaded from [bitcoincore.org](https://bitcoincore.org/bin) and verified against the published sha256-checksums during the build.
The used Bitcoin Core-version is stated in the [readme](https://github.com/anionDev/BitcoinNode/blob/main/BitcoinNode/ReadMe.md) of the codeunit.

## Supported platforms

The image is built for `linux/amd64` and `linux/arm64`.

## Folders in the container

| Folder in the container | Content |
| --- | --- |
| `/Workspace/Data` | The data-directory of `bitcoind` (blockchain, chainstate, wallets, `bitcoin.conf`). |
| `/Workspace/Logs` | The logfile `BitcoinLogfile.log` of `bitcoind`. |

Both folders should be mounted as volumes so that the data is kept when the container is recreated.
The size of `/Workspace/Data` grows with the blockchain, so plan the free disk-space accordingly (or enable pruning, see below).

## Configuration

`bitcoind` is started with `-datadir=/Workspace/Data`, so it reads the configuration-file `/Workspace/Data/bitcoin.conf` if it exists.
Every option of `bitcoind` can be set there, for example:

```text
# Keep only the last 10000 MiB of blocks instead of the entire blockchain.
prune=10000
```

See the [documentation of Bitcoin Core](https://github.com/bitcoin/bitcoin/blob/master/doc/bitcoin-conf.md) for the available options.

## Network

The image does not publish any port.
Without published ports the node only establishes outgoing connections to other nodes.
To accept incoming connections publish the P2P-port (`8333` on mainnet).
Only publish the RPC-port (`8332` on mainnet) if this is really required and the RPC-interface is protected appropriately.

## Shutdown

`bitcoind` runs as main-process of the container, so `docker stop` triggers a clean shutdown of the node.
A clean shutdown can take longer than the default stop-timeout of docker (10 seconds).
If the timeout elapses then docker kills the node, which can result in a time-consuming reindexing on the next start.
Therefore set a longer stop-timeout, for example with `stop_grace_period` in a docker-compose-file.

## Example

See [Example](./Articles/Example.md).
