See https://doc.bmndr.com/transgreption

## To-do list

1. I'm not sure if this is even a problem but it seemed to break things when the metadoc contained a link to its own megadoc. I (dreev) stuck in what I've called an anti-inception hack in url_transforms.py to just make any links to transgreption itself just intentionally break. It would be nice to handle that better somehow!

2. Add a special case for accidentally linking to private google docs or dropbox docs. Currently it just shows the login screens for Google Docs / Dropbox. Would be better to see a red error, like you do if you accidentally link to a private GitHub repo, for example.

3. Should load the skeleton of the page instantly and then show spinners for each document until they were ready.

4. Dropbox links fail to load (409 error), even when they load in a normal browser.

5. Same with Evernote but even worse: it shows a green checkmark as if it loaded it.

6. Some stray html from Facebook seems to be getting rendered on https://transgreption.onrender.com/?q=doc.bmndr.com/transgreption and overlapping with transgreption's own stuff.

7. Add a footer or something with link to the repo and thanking Jake Coble for the initial implementation and Spencer Pearson for at least one improvement, I believe.

8. The icons in the sidebar with an upper-right arrow should be target-blank links to the source doc, I think.
