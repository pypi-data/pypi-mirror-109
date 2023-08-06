# Seavatar

Seavatar is a python library which generates beach-MLH themed avatars

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Seavatar

```bash
pip install seavatar
```

## Usage

```python
import seavatar

svgtext=seavatar.generate_seavatar("GitHub","github.svg")
#The first argument is the string which needs to be 
#converted to an avatar ,the second argument is the filename
#where the file should be stored, by default the filename is
#seavatar.svg

print(svgtext)
```



