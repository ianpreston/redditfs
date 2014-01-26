# redditfs

Everything is better in an 80x25 green-and-black terminal -- even Reddit! `redditfs` maps subreddits to a FUSE filesystem, so you can use your favorite shell (or GUI file browser, or SSH, or FTP) to browse Reddit.

## Example

    $ ls -l /r/programming
    total 0
    dr-xr-xr-x@ 3 root  wheel  0 Jan 16 10:30 ANN:_pandas_0130_released
    dr-xr-xr-x@ 3 root  wheel  0 Jan 18 13:08 An_evaluation_of_simple_Python_performance_tweaks
    dr-xr-xr-x@ 3 root  wheel  0 Jan 17 08:36 Anyone_have_experience_installing_Folium_for_Py_33?
    dr-xr-xr-x@ 3 root  wheel  0 Jan 18 09:48 Are_there_any_python_made_games_on_Steam?
    dr-xr-xr-x@ 3 root  wheel  0 Jan 16 20:06 Beginner:_Getting_Beyond_Syntax
    dr-xr-xr-x@ 3 root  wheel  0 Jan 18 00:53 Best_Questions_to_ask_when_hiring_a_Python_dev?
    ...
    $ ls -l /r/programming/An_evaluation_of_simple_Python_performance_tweaks
    total 16
    -r--r--r--@ 1 root  wheel  97 Jan 18 13:08 permalink
    -r--r--r--@ 1 root  wheel   0 Jan 18 13:08 selftext
    -r--r--r--@ 1 root  wheel  72 Jan 18 13:08 url
    $ cat /r/programming/Best_Questions_to_ask_when_hiring_a_Python_dev?/selftext
    I'm a long time C/C++/C# dev who is now diving into python head on, and using it
     on a project here in Seattle.  Part of this is I need to grow my team and hire 
    ...
    $ lynx $(cat /r/programming/An_evaluation_of_simple_Python_performance_tweaks/url)
    
## Howto

You'll need python 2.7 and FUSE. On OSX, you can get FUSE support is via [OSXFUSE](http://osxfuse.github.io/).

    $ git clone https://github.com/ianpreston/redditfs.git
    $ cd redditfs && virtualenv env && source env/bin/activate
    $ pip install -r reqs.txt
    $ mkdir /r
    $ python redditfs.py /r
    
## License

Available under the MIT License.