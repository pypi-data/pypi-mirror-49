# pygamesilent

## Background

There is a mature open-source library for building multimedia applications, 
like games, called [PyGame](https://www.pygame.org).

Unfortunately, in an effort to recuit more developers, the maintainers added
some output to the library around version 1.9.4, so it now prints text similar
to this upon import:

> pygame 1.9.6  
> Hello from the pygame community. https://www.pygame.org/contribute.html

This move has been [confusing](https://stackoverflow.com/questions/51464455)
 (especially for user-facing command-line tools) and
[controversial](https://www.reddit.com/r/pygame/comments/9j86kq/pygame_infects_stdout_in_194/)
but [complaints about the behaviour have been dismissed](https://github.com/pygame/pygame/issues/542).

## Description

This package provides a shim around PyGame that turns off the unwanted printing 
behaviour with an environment variable. It is designed to be a simple drop in
replacement wherever you would use PyGame.

There are [manual alternatives](https://stackoverflow.com/questions/51464455)
which have the benefit of reducing an external dependency, but this is simpler:

1. Install both `pygame` and `pygamesilent` into your project.
2. Replace any instances of these types of statements:
  * `import pygame` &rarr; `import pygamesilent as pygame`
  * `import pygame as pg` &rarr; `import pygamesilent as pg`
  * `import xxx from pygame` &rarr; `import xxx from pygamesilent`
  
## Versions Supported
This is expected to be cross platform. It has been tested on Windows 10 and
Linux.
 
It is tested on Python 2.7, 3.5, 3.6 and 3.7.

## Note

This **has not been authorised by the PyGame team**. The author is not associated with
them.

You will still need to install and use PyGame, their documentation and 
follow their licenses. 

You might
even like to 
[contribute to their project](https://www.pygame.org/contribute.html)! Perhaps
you can then politely convince them not to put spam in stdio? 

