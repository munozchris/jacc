<?php

/* ini_set('display_errors', 1);
error_reporting(E_ALL | E_STRICT); */

// connect to sqlite database
$db = new sqlite3("/home/student/Downloads/test(1).db");
$db->exec("ATTACH DATABASE '/home/student/Downloads/eval(1).db' as db2");

// set counter for styling/javascript functionality
$counter = 0;

// search different forms
$e_array = array('e_oTA', 'e_xTA', 'e_bio', 'e_lang');

// break up description input for Description query
$desc = explode(" ", $_POST['desc']);
foreach ($desc as $key => $val) {
    $desc[$key] = $val."%'";
}
$desc_string = join(" AND Description LIKE '%", $desc);

// Filter days via SQL by either 'contains' or 'only'
$dayquery = "";
if (isset($_POST['day'])) {
if ($_POST['daycheck'] === "contain") {
    $dayquery .= " LIKE '%";
    foreach ($_POST['day'] as $key => $val) {
        $_POST['day'][$key] = $val ."%'";
    }
    $dayquery .= join(" OR Days1 LIKE '%", $_POST['day']);
} else {
    $daysearch = implode($_POST['day']);
    $dayquery = " ='$daysearch'";
}
}
else {
    $dayquery = "LIKE '%'";
}

set_time_limit(45);

/* If user does not specify hours,
   return a table of classes with times, no hours */

if (empty($_POST['hours'])){

    // table header elements (excluding avg hours)
    echo("<table id='results'>");
    echo("<thead>");
    echo("<th id='dept'> Dept </th>");
    echo("<th id='coursenum'> Course No. </th>");
    echo("<th id='sect'> Section </th>");
    echo("<th id='title'> Title </th>");
    echo("<th id='prof'> Instructor </th>");
    echo("<th id='stime'> Start </th>");
    echo("<th id='etime'> End </th>");
    echo("<th id='days'> Days </th>");
    echo("<th id='add'> Schedule! </th>");
    echo("</thead>");

    // Query only Course Database
    $results = $db->query("SELECT DISTINCT Dept, CourseNum, Title, Professor, StartTime1, EndTime1, Days1,   
    Sect, Description FROM CourseInfo JOIN SectionInfo USING('CourseId') JOIN Description USING('CourseId')
    WHERE Title LIKE '%" . $_POST['title'] . "%' AND Dept LIKE '%" . $_POST['dept'] . 
    "%' AND CourseNum LIKE '%" . $_POST['coursenum'] . "%' AND Professor LIKE '%" .
    $_POST['profname'] . "%' AND Description LIKE '%" . $desc_string .
    " AND (Days1 " .$dayquery .") LIMIT 250");

while ($row = $results->fetchArray()) {

    // table row and data elements
    echo("<tr class='" . "$counter'" . ">");
    echo("<td headers='dept' class='" ."$counter" . "'>" . $row['Dept'] . "</td>");
    echo("<td headers='coursenum' class='" ."$counter" . "'>" . $row['CourseNum'] . "</td>");
    echo("<td headers='sect' class='" ."$counter" . "'>" . $row['Sect'] . "</td>");
    $row['Title'] = str_replace("&", 'and', $row['Title']);
    echo("<td headers='title' class='" ."$counter" . "'>" . $row['Title'] . "</td>");
    $row['Professor'] = trim($row['Professor'], "]");
    $row['Professor'] = trim($row['Professor'], "[");
    echo("<td headers='prof' class='" ."$counter" . "'>" . str_replace("'", '', $row['Professor']) . "</td>");

    $stime = $row['StartTime1'];
    $etime = $row['EndTime1'];

// Time display conversion from integers (1000 -> 10:00AM)
if ($row['StartTime1'] !== "None" and $row['EndTime1'] !== "None") {
    if ($row['StartTime1'] >= 1200 and $row['StartTime1'] < 1300){
        $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
        $starttime .= "PM";
    } 
    else if ($row['StartTime1'] >= 1300) {
        $row['StartTime1'] -= 1200;
        $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
        $starttime .= "PM";
    } else {
        $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
        $starttime .= "AM";
    }

    if ($row['EndTime1'] >= 1200 and $row['EndTime1'] < 1300){
        $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
        $endtime .= "PM";
    }

    else if ($row['EndTime1'] >= 1300) {
        $row['EndTime1'] -= 1200;
        $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
        $endtime .= "PM";
    } else {
        $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
        $endtime .= "AM";
    }
} else {
    $starttime = "None";
    $endtime = "None";
}

    echo("<td headers='stime' id='$stime' class='" ."$counter" . "'>" . $starttime . "</td>");
    echo("<td headers ='etime' id='$etime' class='" ."$counter" . "'>" . $endtime . "</td>");
    echo("<td headers ='days' class='" ."$counter" . "'>" . $row['Days1'] . "</td>");
    echo("<td headers='add'><input type='button' value='Add' class=$counter onClick='eventadd(this.className);' </td>");
    echo("<td style='visibility:hidden; display: none' class='" ."$counter" . "'>" . $row['Description'] . "</td>");
    echo("</tr>");
$counter = $counter + 1;
}

} else {        /* User has now specified hours, 
                   combine evaluation and course databases */

    // table header elements (including avg hours)
    echo("<table id='results'>");
    echo("<thead>");
    echo("<th id='dept'> Dept </th>");
    echo("<th id='coursenum'> Course No. </th>");
    echo("<th id='sect'> Section </th>");
    echo("<th id='title'> Title </th>");
    echo("<th id='prof'> Instructor </th>");
    echo("<th id='stime'> Start </th>");
    echo("<th id='etime'> End </th>");
    echo("<th id='days'> Days </th>");
    echo("<th id='avg'> Hours Spent </th>");
    echo("<th id='add'> Schedule! </th>");
    echo("</thead>");

    foreach ($e_array as &$e_table) {
    $results = $db->query("SELECT CourseInfo.Dept, CourseInfo.CourseNum, CourseInfo.Title, 
        SectionInfo.Professor, SectionInfo.StartTime1, SectionInfo.EndTime1, SectionInfo.Days1,   
        SectionInfo.Sect, Description.Description, AVG(MedHrs) as avg FROM CourseInfo JOIN 
        SectionInfo USING('CourseId') JOIN Description USING('CourseId') JOIN db2.$e_table as e ON 
        CourseInfo.Title = e.CourseName WHERE CourseInfo.Title LIKE '%" . $_POST['title'] . 
        "%' AND CourseInfo.Dept LIKE '%" . $_POST['dept'] . "%' AND CourseInfo.CourseNum LIKE '%" . 
        $_POST['coursenum'] . "%' AND SectionInfo.Professor LIKE '%" .
        $_POST['profname'] . "%' AND Description.Description LIKE '%" . $desc_string .
        " AND (SectionInfo.Days1 " .$dayquery .") GROUP BY e.CourseName HAVING avg < " . 
        $_POST['hours'] . " LIMIT 500");

        // row and data elements
    while ($row = $results->fetchArray()) {
        echo("<tr class='" . "$counter'" . ">");
        echo("<td headers='dept' class='" ."$counter" . "'>" . $row['Dept'] . "</td>");
        echo("<td headers='coursenum' class='" ."$counter" . "'>" . $row['CourseNum'] . "</td>");
        echo("<td headers='sect' class='" ."$counter" . "'>" . $row['Sect'] . "</td>");
        $row['Title'] = str_replace("&", 'and', $row['Title']);
        echo("<td headers='title' class='" ."$counter" . "'>" . $row['Title'] . "</td>");
        $row['Professor'] = trim($row['Professor'], "]");
        $row['Professor'] = trim($row['Professor'], "[");
        echo("<td headers='prof' class='" ."$counter" . "'>" . str_replace("'", '', $row['Professor']) . "</td>");

        $stime = $row['StartTime1'];
        $etime = $row['EndTime1'];

    // Time display conversion from integers (1000 -> 10:00AM)
    if ($row['StartTime1'] !== "None" and $row['EndTime1'] !== "None") {
        if ($row['StartTime1'] >= 1200 and $row['StartTime1'] < 1300){
            $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
            $starttime .= "PM";
        } 
        else if ($row['StartTime1'] >= 1300) {
            $row['StartTime1'] -= 1200;
            $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
            $starttime .= "PM";
        } else {
            $starttime = substr_replace($row['StartTime1'], ":", -2, 0);
            $starttime .= "AM";
        }

        if ($row['EndTime1'] >= 1200 and $row['EndTime1'] < 1300){
            $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
            $endtime .= "PM";
        }

        else if ($row['EndTime1'] >= 1300) {
            $row['EndTime1'] -= 1200;
            $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
            $endtime .= "PM";
        } else {
            $endtime = substr_replace($row['EndTime1'], ":", -2, 0);
            $endtime .= "AM";
        }
    } else {
        $starttime = "None";
        $endtime = "None";
    }


        echo("<td headers='stime' id='$stime' class='" ."$counter" . "'>" . $starttime . "</td>");
        echo("<td headers ='etime' id='$etime' class='" ."$counter" . "'>" . $endtime . "</td>");
        echo("<td headers ='days' class='" ."$counter" . "'>" . $row['Days1'] . "</td>");
        echo("<td headers='avg' class='" ."$counter" . "'>" . round($row['avg'], 1) . "</td>");
        echo("<td headers='add'><input type='button' value='Add' class=$counter onClick='eventadd(this.className); drawChart(this.className);' </td>");
        echo("<td style='visibility:hidden; display: none' class='" ."$counter" . "'>" . $row['Description'] . "</td>");
        echo("</tr>");
    /* counter gives each table row a unique
       class for JavaScript functionality */
    $counter = $counter + 1;
    }
}
}
echo("</table>");
?>