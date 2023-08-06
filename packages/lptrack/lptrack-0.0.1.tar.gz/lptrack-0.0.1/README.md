# LPTrack

LavaPlayer encoded track encoder and decoder.


## Introduction

LPTrack is a small library which allows you to interpret the encoded
track data used by LavaPlayer.

This is useful when you're dealing with standalone LavaLink instances
like [Lavalink](https://github.com/Frederikam/Lavalink) and [Andesite](https://github.com/natanbc/andesite-node),
because it allows you to interpret the track data directly.


## Installation

#### From PyPI

```shell
pip install lptrack
```


## Usage

```python
import lptrack

info = lptrack.Track(
    title="A song",
    author="Some random artist",
    duration=120,                   # duration is in seconds!
    identifier="dQw4w9WgXcQ",
    is_stream=False,
)

encoded = lptrack.encode(info)
print(encoded)
# b'QAAANAIABkEgc29uZwASU29tZSByYW5kb20gYXJ0aXN0AAAAAAAB1MAAC2RRdzR3OVdnWGNRAAA='

decoded = lptrack.decode(encoded)

assert decoded == encoded
```