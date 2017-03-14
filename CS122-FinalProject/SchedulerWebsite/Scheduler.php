<!DOCTYPE html>
<html lang="en">
<head>
    <title>The Scheduler</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="fullcalendar-3.2.0/fullcalendar.css">
    <link rel="stylesheet" media="print" href="fullcalendar-3.2.0/fullcalendar.print.css">
    <link rel="stylesheet" href="StyleSchedule.css">
    <script src="fullcalendar-3.2.0/moment.min.js"></script>
    <script src='fullcalendar-3.2.0/jquery-3.1.1.min.js'></script>
    <script src="fullcalendar-3.2.0/fullcalendar.min.js"></script>
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <!--Retreive hours gauge from Google Charts-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        
        // Credit Google Charts: 
        // https://developers.google.com/chart/interactive/docs/gallery/gauge
        var gauge = 0;

        // Allow user to set their max hours
        var max = prompt('Please put in your Max Hours!');

        google.charts.load('current', {'packages':['gauge']});
        google.charts.setOnLoadCallback(drawChart);
        function drawChart(cnum) {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Hours', 0]
        ]);

        var options = {
          width: 300, height: 600,

          // User hour input here
          greenFrom: 0, greenTo: (max*1/3),
          redFrom: (max*2/3), redTo: (max),
          yellowFrom: (max*1/3), yellowTo: (max*2/3),
          minorTicks: 5,
          max: max
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        // Global variables to allow hours addition
        var cells = document.getElementsByClassName(cnum);
        var hours = parseFloat(cells[9].innerHTML);
        data.setValue(0, 1, gauge + hours);
        gauge += hours;

        // Render gauge
        chart.draw(data, options);
        }

        $(document).ready(function(){ // Credit on AJAX usage to: 
            $('#course-form').submit(function(e) { 
                e.preventDefault();
                $.ajax({
                    beforeSend: function() { // loading gif start
                        // gif credit: https://www.feefreeticket.com/
                        // a-new-world-intimate-music-from-final-fantasy-tickets
                        $(".gif").show();
                    }, 
                    type:"POST",
                    url:"backend.php",
                    data: $("#course-form").serialize(),
                    traditional: true,
                    complete: function(){ // loading gif end
                        $(".gif").hide();
                    },
                    success: function(response){
                        $(".result").html(response);
                    }
                });

        $.get("StyleSchedule.css", function(css) {
            // append style sheet so dynamic content is stylized
            $('<style type="text/css"></style>')
                .html(css)
                .appendTo("head");
            });   
        }); 
    });
    </script>
</head>
<body>

<div id="wrapper">
<div id='calendar'></div>
</div>

    <form method="post" id="course-form">
        <h1>Class Select</h1>
<div id="form">
    <fieldset>
        <legend><h2>Course information</h2></legend>

        <label for='title'>Course Title</label><br>
        <input class="info" id="title" type="text" name="title">

        <label for='dept'>Department</label><br>
        <select class="info" id="dept" name="dept">
            <option value=""></option>
            <option value="AKKD">Akkadian</option>
            <option value="AMER">American Culture</option>
            <option value="ASLG">American Sign Language</option>
            <option value="AANL">Ancient Anatolian Languages</option>
            <option value="ANCM">Ancient Mediterranean World</option>
            <option value="ANCC">Anesthesia/Critical Care</option>
            <option value="AASR">Anthro/Sociology of Religion</option>
            <option value="ANTH">Anthropology</option>
            <option value="ARAB">Arabic</option>
            <option value="ARAM">Aramaic</option>
            <option value="ARME">Armenian</option>
            <option value="ARTH">Art History</option>
            <option value="ASTR">Astronomy/Astrophysics</option>
            <option value="BANG">Bangla</option>
            <option value="BASQ">Basque</option>
            <option value="BIBL">Biblical Studies</option>
            <option value="BPRO">Big Problems</option>
            <option value="BCMB">Biochemistry/Molecular Biology</option>
            <option value="BIOS">Biological Sciences (College)</option>
            <option value="BSDG">Biological Sciences (Graduate)</option>
            <option value="BPHS">Biophysical Sciences</option>
            <option value="BCSN">Bosnian/Croatian/Serbian</option>
            <option value="BUSN">Business</option>
            <option value="CRSH">CIC CourseShare</option>
            <option value="CABI">Cancer Biology</option>
            <option value="CATA">Catalan</option>
            <option value="CHEM">Chemistry</option>
            <option value="CCTE">Chicago Center for Teaching</option>
            <option value="CHIN">Chinese</option>
            <option value="CMST">Cinema/Media Studies</option>
            <option value="CLCV">Classical Civilization</option>
            <option value="CLAS">Classics</option>
            <option value="CCTS">Clinical/Translational Science</option>
            <option value="JWSG">Committee on Jewish Studies</option>
            <option value="CHRM">Committee on the Ministry</option>
            <option value="CAPP">Comp Analysis/Public Pol</option>
            <option value="CRES">Comp Race/Ethnic Studies</option>
            <option value="CHDV">Comparative Human Development</option>
            <option value="CMLT">Comparative Literature</option>
            <option value="CPNS">Computational Neuroscience</option>
            <option value="MACS">Computational Social Science</option>
            <option value="CMSC">Computer Science</option>
            <option value="MPCS">Computer Science Masters</option>
            <option value="CHSS">Conceptual/Hist Studies of Sci</option>
            <option value="CRWR">Creative Writing</option>
            <option value="DVBI">Developmental Biology</option>
            <option value="CDIN">Disciplinary Innovation</option>
            <option value="EALC">East Asian Languages/Civ</option>
            <option value="ECEV">Ecology/Evolution</option>
            <option value="ECON">Economics</option>
            <option value="EGPT">Egyptian</option>
            <option value="EMED">Emergency Medicine</option>
            <option value="ENGL">English Language/Literature</option>
            <option value="ENSC">Environmental Sciences</option>
            <option value="ENST">Environmental Studies</option>
            <option value="EVOL">Evolutionary Biology</option>
            <option value="FMED">Family Medicine</option>
            <option value="FINM">Financial Mathematics</option>
            <option value="KNOW">Formation of Knowledge</option>
            <option value="FREN">French</option>
            <option value="FNDL">Fundamentals: Issues/Texts</option>
            <option value="GNSE">Gender/Sexuality Studies</option>
            <option value="SLAV">General Slavic</option>
            <option value="GENE">Genetics</option>
            <option value="GEOG">Geographical Studies</option>
            <option value="GEOS">Geophysical Sciences</option>
            <option value="GRMN">German</option>
            <option value="GLST">Global Studies</option>
            <option value="GREK">Greek</option>
            <option value="HIPS">HIPS</option>
            <option value="HEBR">Hebrew</option>
            <option value="HIND">Hindi</option>
            <option value="HIST">History</option>
            <option value="HCHR">History of Christianity</option>
            <option value="HCUL">History of Culture</option>
            <option value="HIJD">History of Judaism</option>
            <option value="HREL">History of Religions</option>
            <option value="HNUT">Hum Nutrition/Nutritional Bio</option>
            <option value="HGEN">Human Genetics</option>
            <option value="HMRT">Human Rights</option>
            <option value="HUMA">Humanities</option>
            <option value="ISHU">Humanities Interdisc Studies</option>
            <option value="IMMU">Immunology</option>
            <option value="ISTP">Interdisc Scientist Training</option>
            <option value="INRE">International Relations</option>
            <option value="INST">International Studies</option>
            <option value="ISLM">Islamic Studies</option>
            <option value="ITAL">Italian</option>
            <option value="JAPN">Japanese</option>
            <option value="JWSC">Jewish Studies</option>
            <option value="KAZK">Kazak</option>
            <option value="KORE">Korean</option>
            <option value="EXAM">Language Reading Exam</option>
            <option value="LATN">Latin</option>
            <option value="LACS">Latin Amer/Caribbean Studies</option>
            <option value="LLSO">Law/Letters/Society</option>
            <option value="LAWS">Laws</option>
            <option value="LING">Linguistics</option>
            <option value="MSCA">M.S. in Analytics</option>
            <option value="MSBI">M.S. in Biomedical Informatics</option>
            <option value="MSTR">M.S. in Threat/Response Mgmt</option>
            <option value="MAPH">MAPH (MA in Humanities)</option>
            <option value="MAPS">MAPSS (MA in Social Sciences)</option>
            <option value="MDVS">MDIV Special Courses</option>
            <option value="MARA">Marathi</option>
            <option value="MLAP">Master of Liberal Arts</option>
            <option value="MATH">Mathematics</option>
            <option value="MPHY">Medical Physics</option>
            <option value="MEDC">Medicine</option>
            <option value="MICR">Microbiology</option>
            <option value="CMES">Middle Eastern Studies</option>
            <option value="MOGK">Modern Greek</option>
            <option value="MENG">Molecular Engineering</option>
            <option value="MGCB">Molecular Genetics/Cell Bio</option>
            <option value="MOMN">Molecular Metabolism/Nutrition</option>
            <option value="MPMM">Molecular Pathogenesis/Med</option>
            <option value="MUSI">Music</option>
            <option value="NEAA">Near Eastern Art/Archeology</option>
            <option value="NEHC">Near Eastern History/Civ</option>
            <option value="NELG">Near Eastern Languages</option>
            <option value="NELC">Near Eastern Languages/Civ</option>
            <option value="NPHP">Neuro/Pharma/Physio</option>
            <option value="NURB">Neurobiology</option>
            <option value="NEUR">Neurobiology Department</option>
            <option value="NURL">Neurology</option>
            <option value="NCDV">New Collegiate Division</option>
            <option value="NTEC">New Testament/ECL</option>
            <option value="NORW">Norwegian</option>
            <option value="OBGY">Obstetrics/Gynecology</option>
            <option value="OPTH">Ophthalmology/Visual Sciences</option>
            <option value="ORGB">Organismal Biology/Anatomy</option>
            <option value="ORTH">Orthopaedic Surgery/Rehab Med</option>
            <option value="PALI">Pali</option>
            <option value="PATH">Pathology</option>
            <option value="PEDS">Pediatrics</option>
            <option value="PERS">Persian</option>
            <option value="PHAR">Pharmacology/Physiological Sci</option>
            <option value="PHIL">Philosophy</option>
            <option value="DVPR">Philosophy of Religions</option>
            <option value="PHSC">Physical Science</option>
            <option value="PSMS">Physical Sciences Masters</option>
            <option value="PHYS">Physics</option>
            <option value="POLI">Polish</option>
            <option value="PLSC">Political Science</option>
            <option value="PORT">Portuguese</option>
            <option value="DVSR">Psych/Sociology of Religion</option>
            <option value="PSCR">Psychiatry</option>
            <option value="PSYC">Psychology</option>
            <option value="PBHS">Public Health Sciences</option>
            <option value="PBPL">Public Policy Studies (PBPL)</option>
            <option value="PPHA">Public Policy Studies (PPHA)</option>
            <option value="RCON">Radiation/Cellular Oncology</option>
            <option value="RADI">Radiology</option>
            <option value="RLIT">Religion/Literature</option>
            <option value="RAME">Religions in America</option>
            <option value="RETH">Religious Ethics</option>
            <option value="RLST">Religious Studies</option>
            <option value="REMS">Ren/Early Modern Studies</option>
            <option value="RLLT">Romance Languages/Literature</option>
            <option value="RUSS">Russian</option>
            <option value="REES">Russian/East European Studies</option>
            <option value="PRAC">SSA Field Practicum</option>
            <option value="SANS">Sanskrit</option>
            <option value="SOSC">Social Sciences</option>
            <option value="SSAD">Social Service Administration</option>
            <option value="SCTH">Social Thought</option>
            <option value="SOCI">Sociology</option>
            <option value="SALC">South Asian Languages/Civ</option>
            <option value="SPAN">Spanish</option>
            <option value="SPCR">Special Courses</option>
            <option value="DVSC">Special Courses in Divinity</option>
            <option value="NOND">Special Non-Degree</option>
            <option value="STAT">Statistics</option>
            <option value="SABR">Study Abroad</option>
            <option value="SUMR">Sumerian</option>
            <option value="SURG">Surgery</option>
            <option value="SWAH">Swahili</option>
            <option value="TAML">Tamil</option>
            <option value="TAPS">Theater/Performance Studies</option>
            <option value="THEO">Theology</option>
            <option value="TBTN">Tibetan</option>
            <option value="TTIC">Toyota Tech Inst at Chicago</option>
            <option value="TURK">Turkish</option>
            <option value="UGAR">Ugaritic</option>
            <option value="UTEP">Urban Teacher Education</option>
            <option value="URDU">Urdu</option>
            <option value="VIRO">Virology</option>
            <option value="ARTV">Visual Arts</option>
        </select>

        <label for='coursenum'>Course Number (e.g. 10100)</label><br>
        <input class="info" id="coursenum" type="text" name="coursenum">

        <label for='desc'>Search Course Description</label><br>
        <input class="info" id="desc" type="text" name="desc">

        <label for='profname'>Professor</label><br>
        <input class="info" id="profname" type="text" name="profname">

        <label for='radio'>Meeting Days</label><br>
        Contains
        <input id="radio" type="radio" name="daycheck" value="contain" checked>
        Only
        <input id="radio" type="radio" name="daycheck" value="only">
        <br>
        M
        <input id="M" type="checkbox" name="day[]" value="M">
        T
        <input id="T" type="checkbox" name="day[]" value="T">
        W
        <input id="W" type="checkbox" name="day[]" value="W">
        R
        <input id="R" type="checkbox" name="day[]" value="R">
        F
        <input id="F" type="checkbox" name="day[]" value="F">
        S
        <input id="S" type="checkbox" name="day[]" value="S">
    </fieldset>
    <fieldset>

        <legend><h2>Eval info</h2></legend>
        Max Average Hours per Week    
        <select class="info" id="hours" name="hours">
            <option value=""></option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="8">8</option>
            <option value="9">9</option>
            <option value="10">10</option>
            <option value="11">11</option>
            <option value="12">12</option>
            <option value="13">13</option>
            <option value="14">14</option>
            <option value="15">15</option>
            <option value="16">16</option>
            <option value="17">17</option>
            <option value="18">18</option>
            <option value="19">19</option>
            <option value="20">20</option>
            <option value="21">21</option>
            <option value="22">22</option>
            <option value="23">23</option>
            <option value="24">24</option>
            <option value="25">25</option>
            <option value="26">26</option>
            <option value="27">27</option>
            <option value="28">28</option>
            <option value="29">29</option>
            <option value="30">30</option>
        </select>
    </fieldset>
</form>
<button id="submit-button">Submit</button>
</div>

<div id="chart_div" style="float:right; display:inline-block; width: 400px; height: 120px;"></div>

<script>

// Begin FullCalendar.io JQuery
    $(document).ready(function() {
        // establish calendar dimensions, functionality, and display
        var $calendar = $('#calendar').fullCalendar({
            header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaDay,agendaWeek,month',
            },
            height: 580,
            defaultView: 'agendaWeek',
            selectable: true,
            editable: true,
            fixedWeekCount: false,
            url:'#',
            aspectRatio: 2,
            eventClick: function(event) {
            if (confirm("Delete event (" + event.title + ") ?")) {
            // delete event from frontend
            $calendar.fullCalendar('removeEvents', event.id);
            }},
            eventRender: function(event, element, view){
            console.log(event.start.format());
            return (event.ranges.filter(function(range){
                return (event.start.isBefore(range.end) &&
                        event.end.isAfter(range.start));
            }).length)>0;
            },
        });
    });

    /* initialize event information
     - Global scope to be referenced by two functions*/
    var coursename;
    var stime;
    var etime;
    var dw = [];
    var count = 0;
    var event1;

    function eventadd(cnum){
        eventget(cnum);

        // Credit: http://stackoverflow.com/questions/5092808/how-do-i-randomly-generate-html-hex-color-codes-using-javascript
        var randColor = "#000000".replace(/0/g,function(){
                            return (~~(Math.random()*16)).toString(16);
                        }
                    );
           
           event1 = [{
                title: coursename,
                id: count,
                start: stime, // a start time
                end: etime, // an end time 
                dow: dw, // Repeat specified days, an array -> [1, 3, 5] = MWF
                color: randColor,

                /* Assistance on recurring events credit:
                http://stackoverflow.com/questions/15161654/recurring-events-in-fullcalendar */

                ranges: [{ //repeating events are only displayed if they are within one of the following ranges.
                    start: moment().startOf('week'), //next two weeks
                    end: moment().endOf('week').add(7,'d'),
                    },
                    {
                    start: moment('2017-01-03','YYYY-MM-DD'), // Winter Quarter dates
                    end: moment('2017-03-18','YYYY-MM-DD')
                    }],
              }];

            var getEvents = function( start, end ){
                    return event1;
                }

         $calendar = $('#calendar').fullCalendar({
                    events: function( start, end, timezone, callback ){
                    var events = getEvents(start,end);
                    callback(events);
                    }
                });

         // add event
         $calendar = $('#calendar').fullCalendar('addEventSource', event1, false);
    }

    function eventget(cnum){
        dw = [];

        // add count for calendar event unique IDs
        count ++;

        dayNums = {
            "M": 1,
            "T" : 2,
            "W" : 3,
            "R" : 4,
            "F" : 5,
            "S" : 6
        }

        // retrieve table row of information
        var cells = document.getElementsByClassName(cnum);
        coursename = cells[4].innerHTML;
        stime = cells[6].id;
        console.log(stime);
        etime = cells[7].id;
        var days = cells[8].innerHTML;

        // convert time for FullCalendar military time conventions (2pm = '14:00')
        if (stime >= 1000) {
            stime = stime.substr(0, 2) + ":" + stime.substr(-2);

        } else if (stime < 1000) {
            stime = stime.substr(0, 1) + ":" + stime.substr(-2);
        } else {
            stime = "0:00";
        }

        if (etime >= 1000) {
            etime = etime.substr(0, 2) + ":" + etime.substr(-2);

        } else if (stime < 1000) {
            etime = etime.substr(0, 1) + ":" + etime.substr(-2);
        } else {
            etime = "1:00";
        }

        if (days.length > 0) {
            for (var i = 0; i < days.length; i++) {
                dw.push(dayNums[days[i]]);
            }
        } else{
            dw = [6];
        }

    }
</script>

<!--Loading gif and placement of results table-->
<img class="gif" src="s.gif" style="display:none;">
<div class='result'></div>

</body>
</html>

