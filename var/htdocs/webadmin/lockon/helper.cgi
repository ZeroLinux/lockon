#!/bin/sh

# Copyright (C) 2012 Carlos D. Rincon Velasquez <carlosrincon2005@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

. /var/htdocs/functions/functions
. /partition/lockon/etc/global.cfg

repo="$MIRROR"
filedb="/tmp/lckhelper.lst"
path="$DBPATH"
img_up="<img src='/icons/speedtest.png' style=\"vertical-align:middle\"/>"
img_dl="<img src='/icons/downitem.png' style=\"vertical-align:middle\" title='Download Plugin'/>"

fn_install(){
	curl $repo/library/$FORM_site -o $path/$FORM_site
	if [ "$?" -eq 0 ]; then
		if [ "$FORM_ssl" = "Y" ]; then
			[ ! "$(grep "$FORM_site" $HELPER/ssl.db)" ] && { echo "$FORM_site" >> $HELPER/ssl.db; }
		fi
		if [ "$FORM_dynamic" = "Y" ]; then
			[ ! "$(grep "$FORM_site" $HELPER/dynamic.db)" ] && { echo "$FORM_site" >> $HELPER/dynamic.db; }
		fi
	fi
}

[ ! -e "$filedb" ] && curl $repo/sites.lst -o $filedb
[ "$(ls -l $filedb | cut -d' ' -f 23)" -ne "$(date +%d)" ] && update="<a href=\"javascript:fn_updatedb();\">$img_up Search for updates</a>" || update="Up to Date <a href=\"javascript:fn_updatedb();\">$img_up</a>"

if [ "$FORM_action" = "install" ]; then 
	wget --spider $repo/library/$FORM_site && fn_install
else
	msg="Sorry, plugin is not installed because was impossible to find or connect to lockon repository"
fi

[ "$FORM_action" = "fn_updatedb" ] && curl $repo/sites.lst -o $filedb

init_script
	init_function "install" "site,ssl,dynamic"
		window_confirm "'Install \"'+site+'\" with ssl: \"'+ssl+'\" and dynamic: \"'+dynamic+'\"?'" "$(script_post "helper.cgi" "{action:'install',site:site,ssl:ssl,dynamic:dynamic}")"
		echo "document.getElementById('hidden').style.display=\"block\";"
		echo "$(script_post "helper.cgi" "{action:'install',site:site,ssl:ssl,dynamic:dynamic}")"
	end_function
	init_function "fn_updatedb"
		echo "$(script_post "helper.cgi" "{action:'fn_updatedb'}")"
	end_function
	init_function "fn_modify"
		echo "$(script_post "helper.cgi" "{action:'fn_modify'}")"
	end_function
end_script

init_html
body " Lockon Helper" "/images/add_addon.png"
	init_infoitem
		infoitem "Lockon Helper DB:" "<font color=#009A2A>$update</font>"
	end_infoitem
	echo "<p id='ctrltop'><img src=\"/images/package.png\" style=\"vertical-align:middle\" /> Lockon Helper:</p>"
	echo "<div id=\"hidden\" style=\"display: none; width: 280px; height: 130px; background-color: #FFFFFF; position:absolute; left: 50%; top: 50%; margin-left: -250px; margin-top: -50px;\"><center><br/><p>Please wait, downloading list...</p><br/><img src=\"/images/loading.gif\"></center></div>"

lockonstat="$($lockonbin service isactive)"

if [ "$lockonstat" = "true" ]; then
	infoitem "<br>NOTE: <font color=#009A2A>You must stop lockon service before proceed to use this feature</font>"
else
	__init_table "listview"
	header_table "IPs,30px" "Site,110px" "SSL,50px" "Dynamic,50px" "<center>Actions</center>,100px"
	while read ips site ssl dynamic; do
		[ ! $(ls $path/$site) ] && add_item_table "$ips" "$site" "$ssl" "$dynamic" "<center>
			<a href=\"javascript:install('$site','$ssl','$dynamic');\"> Download $img_dl </a>
			</center>"
	done < $filedb
	bottom_table ",30px" ",110px" ",50px" ",50px" ",100px"
end_table
fi
end_body
end_html
