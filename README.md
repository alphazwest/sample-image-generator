# Sample Image Generator

All images are generated and saved in a /output directory along with metadata named as such:

    x.jpg, x-meta.json (where x is a number ranging from 0-TOTAL_IMAGES)

The x-meta.json files contain traits listed as features in accordance with OpenSea standards listed here:
    
https://docs.opensea.io/docs/metadata-standards

A custom font "Volkov" is used and saved in the /fonts folder. Information about this font is available here:

https://fonts.google.com/specimen/Volkhov

## Installation

To generate images, this project needs to be setup as follows:

```bash
pip install -r requirements.txt
python images.py
```

## Notes:
1. Output directory is created if it does not exist
2. Output directory is recursively deleted before each run
3. parameters can be adjusted via constants at the top of `images.py`