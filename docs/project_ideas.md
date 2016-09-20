# Proposed Projects

Below is a list of proposed project ideas (in no order) and a little information about what they will entail



 #### IRC Client
 This is probaby harder to implement that you think without using a library to do most of the work for us. If we want to go hardmode we can work with python sockets and implement it from scratch following the RFC's with lots of trial/error
 
 A few useful resources
 * [RFC7194](https://tools.ietf.org/html/rfc7194)
 * [RFC1459](https://tools.ietf.org/html/rfc1459)
 * [RFC2812](https://tools.ietf.org/html/rfc2812)
 * [Python Socket Programming](https://docs.python.org/3.5/howto/sockets.html)
  
 #### Web Base Torrent Client
  This is actually my favorite and is something I have been brainstorming about on my own. It would involve a web front-end consisting of mostly a search page written in HTML, CSS, & Javascript. The  backend would consist a web framework leveraging a modular plugin system that can be implemented by anyone. A number of things would need take into consideration.
  * Web Frameworks - [Django](https://www.djangoproject.com/) and [Flask](http://flask.pocoo.org/) are the popular ones
  * A webserver - [nginx](https://www.nginx.com/resources/wiki/) is my preference
  * A database - Pretty much any relation database should work I have no strong preferences
  * An authentication module
  * A framework for downloading torrents
  * Possible a torrent api so we can implement a sample plugin [examples](http://www.programmableweb.com/category/torrents/api)
  
 #### Write Memory Patcher for a Game
 This would involve low level C programming and knowledge of x86 and OS internals. We would also need to target a specific OS below are something of the things you would need to be comfortable with
 * C & x86 Assembly
 * How functions exist in memory
 * How the call stack works
 * Knowedge of how the target OS loads executables into memory and what tools are available to modify memory after the fact
 * Knowledge of a debugger and static disassembler
 
 #### Game Stats/Analysis Front-End
 This is what has been mostly discussed and there are a lot of ways it could go. So I'll fill this out once we have a better idea of what we want
 
 #### Write a Reddit bot
 Last second thought - we can make a reddit bot using the [praw](https://praw.readthedocs.io/en/stable/) library - what we want the bot to do could be a topic of discussion or could tie into any of the other projects.

