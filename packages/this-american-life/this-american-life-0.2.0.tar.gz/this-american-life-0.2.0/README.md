# this american client
[![PyPI version](https://badge.fury.io/py/this-american-life.svg)](https://badge.fury.io/py/this-american-life)

The [This American Life](https://www.thisamericanlife.org/) client library. 

Get structured data on transcripts, episodes, et c without worrying about all of the web scraping details. Intermediate
results are cached to keep it snappy.

## Install

```bash
pip install this-american-life
```

## Using the client

Everything starts with the import
```python
from thisamericanlife import ThisAmericanLife

tal = ThisAmericanLife()
```

### Get the episode and act summaries 
```python
ep_one = tal.episodes.get(episode_number=1)

print('Title       : ' + ep_one.title)
print('Date on air : ' + ep_one.date_on_air)
print('Description : ' + ep_one.description)

# the name and short description of each act
print(ep_one.act_summaries)
```

### Get the transcript of an episode
```python
ep_one_transcript = tal.transcripts.get(episode_number=1)

print(ep_one_transcript.transcript)
```