#sudo uhubctl -l 2-3 -p 1 -a on
#sudo uhubctl -l 2-3 -p 2 -a on
#sudo uhubctl -l 1-2 -p 1 -a on
#sudo uhubctl -l 1-2 -p 2 -a on

#for any reason that didnt work. instead we need to fully power everything up again:
sudo uhubctl -l 1-2 -a on
sudo uhubctl -l 2-3 -a on

