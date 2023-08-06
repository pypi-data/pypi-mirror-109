
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/NoPantsCrash/ffenmass">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">FFenmass</h3>

  <p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/ffenmass"> <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/ffenmass"> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/ffenmass"> <img alt="PyPI - License" src="https://img.shields.io/pypi/l/ffenmass"> <img alt="PyPI - Format" src="https://img.shields.io/pypi/format/ffenmass"> <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/ffenmass">
  <br />
    CLI Utility to encode and recursively recreate directories with ffmpeg. 
    <br />
    <a href="https://github.com/NoPantsCrash/ffenmass/issues">Report Bug</a>
    ·
    <a href="https://github.com/NoPantsCrash/ffenmass/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="/CHANGELOGS.md">Changelogs & TODOs</a></li>
    <li><a href="/LICENCE">License (MIT)</a></li>
  </ol>
</details>

<br>

### Features
 - Proccecing whole directories from the CLI interface.
 - Recreating directories with identical foldernames/filenames on the output.

<br>

<!-- GETTING STARTED -->
### Getting Started

FFenmass is an ffmpeg wrapper, adding the ability to manipulate media files in directories and recreate them recursively.
Currently works in **Linux** folder structures only.
**Windows** support is planned.



### Prerequisites

FFenmass only requires **ffmpeg** and **python3**.



### Installation

Using `pip`
   ```bash
   pip3 install ffenmass
   ```

<br>

<!-- USAGE EXAMPLES -->
## Usage

**FFenmass** is transparent above **ffmpeg**, this means **most ffmpeg syntax can be used with ffenmass as is**.

The only **differences being** the **input** `(-i)` and the **output** being **directories instead of files**.

Also **ffenmass ignores file extensions**, you will need to **specify container using ffmpeg's `-f` argument**.

The result is ffenmass will **encode all media files detected under the input directory** with the provided ffmpeg arguments and output them with the **same folder structure and filenames** in the **output directory**.

<br>

### Example compared to standard ffmpeg syntax
```bash
ffmpeg -i input.mkv -acodec copy -vcodec libx265 -b:v 2M -minrate 1M -maxrate 3M -preset medium out.mp4


ffenmass -i /path/to/folder/ -acodec copy -vcodec libx265 -b:v 2M -minrate 1M -maxrate 3M -preset medium -f mp4 /output/directory/
```
<br>
<br>

**Directory Tree visualization** of what is going on when you run the **command from the example above**.
```
path/to/folder/                           /output/directory/
├── givemefolders                         ├── givemefolders      
│   ├── somefolder                        │   ├── somefolder
│   │   └── example_movie.mkv             │   │   └── example_movie.mp4
│   ├── myfavvideo.mkv                    │   ├── myfavvideo.mp4  
│   ├── example_movie.m2ts                │   ├── example_movie.mp4
│   ├── another_example.mkv         →     │   ├── another_example.mp4
│   ├── morefolders                       │   ├── morefolders
│   │   └── a_lot_of_examples.ts          │   │   └── a_lot_of_examples.mp4  
│   └── documentary.mkv                   │   └── documentary.mp4
├── another_example.mkv                   ├── another_example.mp4
├── more-examples.mp4                     ├── more-examples.mp4 
└── examples_and_examples.ts              └── examples_and_examples.mp4

```



<br>

<!-- CONTRIBUTING -->
## Contributing
Any contributions you make are **greatly appreciated**.

## License

Distributed under the MIT License. See `LICENSE` for more information.

