# /logs #

In this folders is where the bot saves the logs in its different formats, even the
HTML viewers for each CSV logs.

[`createhtml.sh`](ivanhercaz/CanaryBot/createhtml.sh) create the HTML viewer and
then add one line to `logs.html`, a file structurated with `<ul>` and `<li>` tags.
Then, this file is included in [`logslist.html`](ivanhercaz/CanaryBot/logslist.html).

The structure of `logs.html` would be:
```html
<ul>
<li><a href='logs/logs/2018-05-25_01:52-fullStopsChecker-test.html'>logs/2018-05-25_01:52-fullStopsChecker-test.html</a></li>
<li><a href='logs/logs/2018-05-24_23:10-fullStopsChecker-test.html'>logs/2018-05-24_23:10-fullStopsChecker-test.html</a></li>
<li><a href='logs/logs/2018-05-24_23:10-fullStopsChecker-test.html'>logs/2018-05-24_23:10-fullStopsChecker-test.html</a></li>
<li><a href='logs/logs/2018-05-25_00:41-fullStopsChecker-test.html'>logs/2018-05-25_00:41-fullStopsChecker-test.html</a></li>
</ul>
```
