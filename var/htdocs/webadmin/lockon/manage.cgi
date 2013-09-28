#!/bin/sh

#  Copyright 2013 Carlos R. <carlosrincon2005@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

. /var/htdocs/functions/functions
. /partition/lockon/etc/global.cfg

[ "$FORM_action" = "delete" ] && $lockonbin delete "$FORM_domain"

init_html

echo "<script language=\"JavaScript\" src=\"lockon.js\"></script>"

body " LockOn Manager" "lockon.png"

init_script
	init_function "form_edit" "id,file,npis,sec,dyn"
		script_formshow "lockon" "edit"
		set_form_value "lockon" "action" "'edit'"
	end_function
	echo "setInterval(\"loadXMLDoc('myDiv','random.cgi')\",5000);"
	init_function "delete_domain" "domain"
		window_confirm "'Delete \"'+domain+'\" from LockOn?'" "$(script_post "manage.cgi" "{action:'delete',domain:domain}")"
	end_function
end_script

if [ "$($lockonbin portal isactive)" = "true" ]; then
	tbcolor="E9AF7A"
	advstat="<font color=\"green\">Running...</font>"
else
	tbcolor="AA2A2A"
	advstat="<font color=\"red\">Stoped...</font>"
fi

service="$($lockonbin service isactive)"
if [ "$service" = "true" ]; then
	tbcolor="E9AF7A"
	status="<font color=\"green\">Running...</font>"
elif [[ "$service" = "sleep" ]]; then
	tbcolor="3D1690"
	status="<font color=\"#3D1690\">Sleep...</font>"
else
	tbcolor="AA2A2A"
	status="<font color=\"red\">Stoped...</font>"
fi

echo "<style type=\"text/css\">table.listview tr.listview {background-color: #${tbcolor};}table.listview .bl, table.listview .br {border-color: #${tbcolor};}</style>"

__init_table "listview"
	header_table ",130px" ",200px"
		add_item_table "Portal Status" "$advstat"
		add_item_table "Lockon Status" "$status"
		add_item_table "Domains in Lockon" "$(ls $DBPATH | wc -l)"
		add_item_table "Https Domains" "$(sed -n '$=' $HELPER/ssl.db)"
		add_item_table "Dynamic Domains" "$(sed -n '$=' $HELPER/dynamic.db)"
		[ "$service" = "true" ] && add_item_table "LockOn packets" "<h3 style=\"height: 18px; background-image:url('preload.gif');background-repeat: no-repeat; padding-left: 32px;\" id=\"myDiv\">Loading...</h3>"
	bottom_table "" ""
end_table
echo "<br/>"
__init_table "listview"
	header_table "Domain,260px" "IPs,50px" "Secure,100px" "Dynamic,100px" "Action,50px"
	for file in $(ls $DBPATH); do
		nfile="${file##*/}"
		nIPs="$(sed -n '$=' $DBPATH/$file)"
		[ "$(grep -w ${nfile} $HELPER/ssl.db)" ] && secure="yes" || secure="no"
		[ "$(grep -w ${nfile} $HELPER/dynamic.db)" ] && dynamic="yes" || dynamic="no"
		add_item_table "${nfile}" "$nIPs" "$secure" "$dynamic" "$(button "Delete" "delete" "delete_domain('$nfile');" "70px")"
	done
	bottom_table ",260px" ",50px" ",100px" ",100px" ",50px"
end_table

end_body
end_html
