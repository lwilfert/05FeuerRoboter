# workflow
- run play.py on boot
	- play.py checks if config.jens has content '0\n'
- simulate the start, drive and stop process of car with main.py
	- writes '0\n' in config.jens -> play.py starts playing

# future usage:
- start play.py on boot
- write '0\n' in `config.jens` as soon as car starts driving
- write '1\n' (or anything else) in `config.jens` as soon as sound should stop
