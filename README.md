# A GUI based simple implemetation of Conway's Game of Life in Python and c++
Clone the  repo:-
```bash
git clone https://github.com/KetanMann/Conway_Game_of_Life
```
```
cd Conway_Game_of_Life
```
## Python
```bash
pip install numpy tkinter matplotlib 
```
```bash
python gui_con.py
```
## C++ 
First, install SFML package for GUI.
```bash
sudo apt-get install libsfml-dev
```
```bash
g++ -std=c++11 conway.cpp -o conway -lsfml-graphics -lsfml-window -lsfml-system
```
```bash
./conway
```
