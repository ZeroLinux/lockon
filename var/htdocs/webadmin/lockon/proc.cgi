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

fn_edit(){
	eval $(echo "sed -i '$1"s"~.*~$2~' $3")
}

fn_msg(){
	msg="<script language=\"javascript\">document.getElementById(\"myDiv\").innerHTML+=\"$1\";</script>"
	echo $msg
}

fn_post_proccess(){
	show_loading
	for index in $(seq 0 20); do
		eval url="\$FORM_url$index"
		if [ -n "$url" ]; then
			eval secure="\$FORM_secure$index"
			[ -z "$secure" ] && secure="false"
			eval dynamic="\$FORM_dynamic$index"
			[ -z "$dynamic" ] && dynamic="false"
			addURL="$($lockonbin add $url $dynamic $secure)"
			outok="Action ready for $url ($addURL new ips)<br/>"
			outerr="$addURL"
			link="<a href='manage.cgi'>Ok, continuar >></a>"
			[ $? -eq 0 ] && fn_msg "$outok" || fn_msg "$outerr"
		fi
	done
	hide_loading
	echo "<script language=\"javascript\">document.getElementById(\"myDiv\").innerHTML+=\"$link\";</script>"
}

init_html
body " LockOn" "lockon.png"

__init_table "listview"
	header_table ",130px" ",350px"
		add_item_table "<div id=\"myDiv\"></div>" ""
	bottom_table "" ""
end_table

fn_post_proccess
end_body
end_html
