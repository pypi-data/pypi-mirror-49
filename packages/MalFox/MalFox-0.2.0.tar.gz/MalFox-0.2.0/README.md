#### About

A locally-run cover generator for [MyAnimeList](https://myanimelist.net) written with Python 3.7. Generates CSS files for high resolutions covers. Currently somewhat barebones.

This project is more of a fun experiment than something I expect to announce loudly to the world. It is named after Doomcat's ["MalCat"](https://myanimelist.net/forum/?topicid=1533260), even though it's function-set is rather different for the moment.

#### How To Install

*Python 3 is required.*

Launch command line and install via pip:
```
pip install MalFox
```

#### How To Use

*This script requires your MAL list to be public.*

Run via command line and pass it up to three arguments: username, list type, and CSS preset. MalFox will generate a "Results" folder wherever you run the script, so make sure to "cd" to your preferred directory.

**Command line syntax:**
```
python -m MalFox <user> <type> <preset>
```

**Valid types:** 'anime', 'manga', 'both'

**Valid presets:** 'dataimagelink', 'dataimagelinkbefore', 'dataimagelinkafter', 'datatitlelink', 'datatitlelinkbefore', 'datatitlelinkafter', 'animetitle', 'animetitlebefore', 'animetitleafter', 'more'

Only username is required. If no type or preset is provided, it defaults to 'both' + 'dataimagelinkbefore'.

Example command line prompt:
```
python -m MalFox Valerio_Lyndon both dataimagelink
```

This tutorial will be improved in the future if/when this script is also improved.

#### Plans

- **Complete** ~~Proper Python formatting, allowing easier install through pip (including module dependency direction). I'm kinda bad so I am still figuring out how to do this.~~
- (Definite) Automatic uploading of files to hosting service. Would automatically override files if they exist.
- (Definite) Add details to readme on how to have script run via .bat file, including automatically on computer start.
- (Possible) Toggle for combining anime/manga files into one output file. Not valid for 'more' preset.
- (Unlikely) Package project as an exe file for easier use.