episodescript
=============
Retrieve TV Show Scripts.


## Install

* From GitHub.

```
git clone https://github.com/kota7/episodescript
pip install -U episodescript
```

* Recommended for Conda users.

```
conda install -y beautifulsoup4 'html5lib<1'
git clone https://github.com/kota7/episodescript
pip install -U episodescript/ --no-deps
```


## Use the console command

```
episode-script the-mentalist 2 6
```
  
Or, if you want to read step by step:
  
```
episode-script the-mentalist 2 6 | less
```


## Use in a python script

```
>>> from episodescript import scrape_episode_scripts
>>> title, script = scrape_episode_scripts("the-mentalist", 2, 6)
>>> print(title)
>>> print(script)
```