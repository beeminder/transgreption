Originally developed here:
https://replit.com/@jakecoble/transgreption
But this is the master copy now.

See the original spec at http://doc.bmndr.com/transgreption

## To-do list

1. I'm not sure if this is even a problem but it seemed to break things when the metadoc contained a link to its own megadoc. I (dreev) stuck in what I've called an anti-inception hack in url_transforms.py to just make any links to transgreption itself just intentionally break. It would be nice to handle that better somehow!

2. maybe a special case for accidentally linking to private google docs or dropbox docs? currently it just shows the login screens for google docs / dropbox. would be better to see a red error, like you do if you accidentally link to a private github repo.

3. and then pie in the sky that probably isn't worth it but, like, if it loaded the skeleton of the page instantly and then showed spinners for each document until they were ready, that'd be kind of amazing...

4. dropbox links fail to load, even when they load in a normal browser

5. same with evernote but even worse: it shows a green checkmark as if it loaded it.

6. remember to add my standard AGENTS.md from the road repo

7. some stray html from facebook seems to be getting rendered on https://transgreption.replit.app/?q=doc.bmndr.com/transgreption and overlapping with transgreption's own stuff

8. add a footer or something with link to the repo and thanking jake coble for the initial implementation and spencer pearson for at least one improvement, i believe.

9. the icons in the sidebar with an upper-right arrow should be target-blank links to the source doc, i think.
