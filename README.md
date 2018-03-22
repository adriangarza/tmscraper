# tmscraper
batch download tm2-exchange tracks 

## usage
Run `tm-scraper <URL> <# TRACKS>` in your console. It will grab `# TRACKS` from the given mania-exchange url and leave them in the folder where it was run.

An example usage would be:

`tmscraper.py "https://tm.mania-exchange.com/tracksearch2?mode=5&priord=8&environments=2" 5`

This would download the first 5 tracks from that url, which happens to be the top Stadium tracks of the month. **Make sure the url is in quotes or python will complain.**

Thanks for using, I'm open to PRs if anyone wants to make one.
