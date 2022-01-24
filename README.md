# Erisly >tower employee shuffler

Do you play `>tower`, [Erisly](https://erisly.com/)‘s Discord chat Tiny Tower demake? Do you want to micro-manage your tower to achieve maximum hourly earnings? If so, you’re in the right place.

This script shuffles your `>tower` employees to maximise tower earnings, using Python and the keyboard library.

It’s horribly inefficient at over 120 lines long, but it works :)

## Usage

Enter the total number of floors you want to populate (i.e. floors that are not under construction) in `employees.txt`, then underneath enter all of your current employees. The format is explained in the text file, but for example if you had a common rarity employee named Alexander May assigned to floor \#8, you’d enter `Alexander May C 8`.

Make sure the keyboard library is installed (`pip install keyboard`), then run `shuffle-employees.py`. Move your cursor to a Discord channel, preferably in a private server, then press the start hotkey (defaults to F7) and the script will assign, unassign and swap your employees to place your highest-rarity employees on the highest floors. It will then update `employees.txt` to reflect the changes, and tell you how much you increased your hourly earnings.
