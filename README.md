# TelegramExportAnalyzer
A set of python scripts to analyze the exported JSON file from a Telegram client

**Disclaimer**: The Big-O of many algorithms in this project are currently as bad as n^2, which could probably be optimized,
this code is not suitable for production environment or for use on datasets too large, it produces a result within a second with my
~30MB dataset.

## Usage
Export a chat or an account through your Telegram client, then use the distribution module to get a CSV output of the distributions.

You can use Google Docs to plot the data.

```bash
python3 /path/to/project/distribution.py -f /path/to/export/result.json
```