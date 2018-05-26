#!/bin/bash

# Create an HTML file in which the content is a CSV viewer to check the CSV logs
# made with the log.py module during the wiki tasks performed by CanaryBot.
# It works with "CSV to HTML Table", developed by Derek Eder (The MIT License).

# Arguments passed
# CSV file
FULLNAMELOG=$1
# CSV viewer
HTMLFILE=$2
# File to list all the logs
LOGLIST="logs/logs.html"
# Name of the script-task made
TASK=$3

# Create the file and write the content
cat > $HTMLFILE << _EOF_
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Log of $TASK</title>
    <meta name="author" content="Iván Hernández Cazorla">

    <!-- IMPORTANT NOTE: change the external CDNs to Wikimedia CDN -->
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/dataTables.bootstrap.css" rel="stylesheet">
  </head>
  <body>
    <div class="container-fluid">

      <h2>Task: $TASK</h2>
      <h3>$FULLNAMELOG</h3>

      <div id='table-container'></div>

</div><!-- /.container -->

<footer class='footer'>
  <div class='container-fluid'>
    <hr>
    <p class='pull-right'>Thank you very much to <a href='http://derekeder.com'>Derek Eder</a>,
    creator of <a href='https://github.com/derekeder/csv-to-html-table'>CSV to HTML Table</a>,
    who released it under <a href="https://github.com/derekeder/csv-to-html-table/blob/master/LICENSE">The MIT License</a></p>
  </div>
</footer>

<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>
<script type="text/javascript" src="js/jquery.csv.min.js"></script>
<script type="text/javascript" src="js/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="js/dataTables.bootstrap.js"></script>
<script type="text/javascript" src="js/csv_to_html_table.js"></script>


<script type="text/javascript">
  function format_link(link){
    if (link)
      return "<a href='" + link + "' target='_blank'>" + link + "</a>";
    else
      return "";
  }

  CsvToHtmlTable.init({
    csv_path: '$FULLNAMELOG',
    element: 'table-container',
    allow_download: true,
    csv_options: {separator: ',', delimiter: '"'},
    datatables_options: {"paging": true},
    custom_formatting: [[4, format_link]]
  });
</script>
</body>
</html>
_EOF_

sed -i "s#<ul>#<ul>\n<li><a href='$HTMLFILE'>$HTMLFILE</a></li>#g" $LOGLIST
