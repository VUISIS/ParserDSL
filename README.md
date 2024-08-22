# ParserDSL

## Installation of 3D
Download the [latest release](https://github.com/project-everest/everparse/releases) of Everparse from Github and move it to `./3d` folder.

Enter `./3d` directory and unzip the file. You should expect a new folder named `everparse` and `everparse.sh` inside that folder.

```
cd 3d
tar xvf everparse_your_version
```

## Parser generation from 3D specs
```
cd everparse
bash everparse.sh ../TAR.3d --odir ../TAR
```

## Set up a Python virtual environment with pipenv
Create `.env` to store your OpenAI secret
```
OPENAI_API_KEY=sk-xxxxxxxxxxx
```

Make sure you already have `pip3` and `python` installed
```
pip3 install pipenv
```

Install dependencies
```
pipenv install
```


## Generate parser DSL 
Fire up a shell in virtual environment
```
pipenv shell
```

Run script
```
python GenParseDSL.py
```