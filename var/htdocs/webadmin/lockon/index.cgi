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

init_html

echo "<script language=\"JavaScript\" src=\"lockon.js\"></script>"

body " LockOn" "lockon.png"

init_script
	init_validation "validate_form"
		add_validation "url0" "VALID_ISNOTNULL"
		for i in $(seq 0 20); do
			add_validation "url$i" "VALID_IP_OR_DOMAIN"
		done
	end_validation
end_script

addBTN="<input type=\"button\" onclick=\"addInput()\" value=\"+\" />"

init_form_config "lockon" "600px" "[New Domain]" "proc.cgi" "validate_form"
	init_infoitem
		input_hidden "id" ""
		input_hidden "action" ""
		infoitem_form "<br><center>Add new URLs</center>" "<br/>IMPORTANT!: Remember that you must check \"SSL\" only if site use httpS, and <br>\"Balanced\" only if site use more than one ip.<br/>
		<br/>${addBTN}$(input_textbox "url0" "" "" "260px") $(input_checkbox "secure0" "true" "" "SSL") $(input_checkbox "dynamic0" "true" "" "Balanced") \
		<span id=\"responce\"></span>" "<br/>example: www.facebook.com, facebook.com or es-la.facebook.com<br/>"
	end_infoitem
end_form_config

end_body
end_html
