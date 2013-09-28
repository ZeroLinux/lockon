<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <?php
            if(!file_exists("/tmp/lockon")){
                echo "<script language=\"Javascript\">location.reload(true);</script>";
                echo "<meta http-equiv=\"refresh\" content=\"0;\"/>";
            }
        ?>
        <title>lockon</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <meta http-equiv=Cache-Control content=no-cache, no-store, must-revalidate />
        <meta http-equiv=Pragma content=no-cache />
        <meta http-equiv=Expires content=-1 />
        <link rel="stylesheet" href="css/normalize.min.css">
        <link rel="stylesheet" href="css/main.css">
        <link rel="shortcut icon" href="favicon.ico" />

        <!--[if lt IE 9]>
            <script src="js/vendor/html5-3.6-respond-1.1.0.min.js"></script>
        <![endif]-->
    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <div class="header-container">
            <header class="wrapper clearfix">
                <h1 class="title">This site has been blocked</h1>
            </header>
        </div>

        <div class="main-container">
            <div class="main wrapper clearfix">

                <article>
                    <section>
                        <h1>Details:</h1>
                        <?php
                            $OUTPUT = exec("/usr/bin/lockon timer");
                            if ($OUTPUT == "false") {
                                // Message if the TIMER is not enabled:
                                echo "<p>The site is blocked.</p>";
                            }else{
                                $TimerHour = exec("grep -w 'lockon stop' /etc/brazilfw/cron.cfg | awk '{print $2}'");
                                $sysHour = exec("date +%H");
                                $sysMin = exec("date +%M");
                                $evtime = $TimerHour-$sysHour;
                                $TIMER = exec("grep -w 'lockon stop' /etc/brazilfw/cron.cfg | awk '{print $2\":\"$1}'");
                                $systemdate = $sysHour . ":" . $sysMin;
                                $datetime1 = new DateTime($systemdate);
                                $datetime2 = new DateTime($TIMER);
                                $interval = $datetime1->diff($datetime2);
                                // Message if the TIMER is enabled:
                                echo "<p>The site is blocked temporaly, and this will be avaliable soon.</p>";
                                if ($evtime <= 0) {
                                    echo "<h3>About " . (23-$interval->h) . " hours and " . (60-$interval->i) . " minutes remain to unlock this site...</h3>";
                                }else{
                                    echo "<h3>About " . $interval->h . " hours and " . $interval->i . " minutes remain to unlock this site...</h3>";
                                }
                            }                  
                        ?>
                    </section>
                    <section>
                        <p>If you believe that this site is blocked by error because this site don't comply with the lock policy of this organization, please contact the issue to your network admin: sysadmin@mycompany.org.</p>
                    </section>
                </article>

                <aside>
                    <center><h3>Powered by LockOn</h3></center>
                    <center><p><img src="img/y_shield.png"></p></center>
                    <center><h3>a GNU/GPL Software Solution</h3></center>
                </aside>

            </div> <!-- #main -->
        </div> <!-- #main-container -->

<!--         <div class="footer-container">
            <footer class="wrapper">
                <h3>footer</h3>
            </footer>
        </div> -->

        <script src="js/jquery.min.js"></script>

        <script src="js/main.js"></script>
    </body>
</html>
