# Kamiko Save File Editor
A save file decompiler/recompiler for Kamiko for PC

## Requirements
To use the Kamiko Save File Editor, Python is required. This is written for Python 3 (3.6+ recommended).

## Usage
Place `save_loader.py` in the same folder as the Kamiko save data. This is usually placed at `C:\Users\<user name>\AppData\LocalLow\Flyhigh works\Kamiko\`.

To run the script, open a command line in this folder.

#### Decompiling
Any of the following can be used:
```
python save_loader.py -l
python save_loader.py -load
python save_loader.py -l -p path_to_SaveData
```

When decompiling a save file, if you provide no path using the `-p` command line argument, it will default to `SaveData` in the same folder as the python script. This mode will generate the file `SaveData.json`, overwriting any existing file with this name.

#### Recompiling
Any of the following can be used:
```
python save_loader.py -s
python save_loader.py -save
python save_loader.py -s -p path_to_SaveData.json
```

When recompiling save data, if you provide no path using the `-p` command line argument, it will default to `SaveData.json` in the same folder as the python script. This mode will generate the file `SaveData`. This will overwrite any existing file. If there is no backup of the save data file, a backup will be created to ensure that the original save data isn't overwritten. This backup will have the name `SaveData.bak`.

## Tips relating to modifying `SaveData.json`
`_saveDataUnitList` contains a list of 3 save data "units". Each unit contains 3 "jobs".
Each of these jobs contains `PlayerData`, `MapData` and a number of pieces of information relating to timing and other properties.

#### `PlayerData`
`Status` values are quite self-explanatory. The max HP and SP values can be set above the maximum values you can normally obtain in the game. If HP > 12, the UI will not display the extra icons, however the functionality will still be there. If SP > 400, the bar will just extend out of the usual area, which looks quite bad.
`Position` should probably not be messed with. Setting it to a value which causes the character to not be on land you can stand on causes the game to not function properly (movement is weird and restricted).

#### `MapData`
`MapKey` has the format `kamiko_map_XY` where `X` = (1, 2, 3, 4), and `Y` = (1, 2). `X` is the level, and `Y` is 1 if it's the main level, and 2 if it's the boss level.
The other values probably shouldn't be messed with or don't really need to be.

#### Other values

`_playTimeForMap` is the current amount of time spent on the particular map. Set this to 0 to have a timer starting at 0 for the map.
`_clearTimeEachMapList` is a list of the clear times for each level.
