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

[ ${MODE} -eq 11 ] && STMODE="whitelist (ideal to add the sysadmins and boss)";
[ ${MODE} -eq 21 ] && STMODE="whitelist (ideal to add the sysadmins and boss)";
[ ${MODE} -eq 12 ] && STMODE="blacklist (add users which you want apply the block)";
[ ${MODE} -eq 22 ] && STMODE="blacklist (add users which you want apply the block)";

fn_edit(){
	eval $(echo "sed -i '$1"s"~.*~$2~' $3")
}

case "$FORM_action" in
	delete)
		lockon_exec="$($lockonbin stratos delete $FORM_id)"
		needsave
		;;
	edit)
		lockon_exec="$($lockonbin stratos delete $FORM_id)"
		lockon_exec="$($lockonbin stratos add "$FORM_ip_address $FORM_comment")"
		needsave
	;;
	add) if [ -n "$FORM_ip_range" ]; then
		lockon_exec="$($lockonbin stratos add "$FORM_ip_address"-"$FORM_ip_range $FORM_comment")"
	else
		lockon_exec="$($lockonbin stratos add "$FORM_ip_address $FORM_comment")"
	fi
	needsave
	;;
esac

init_html

init_script
	init_function "form_delete" "id,ip"
		window_confirm "'Delete \"'+ip+'\"?'" "$(script_post "stratos.cgi" "{action:'delete',id:ip}")"
	end_function

	init_function "form_add"
		show_tr "__To"
		script_formshow "stratos" "add"
		set_form_value "stratos" "action" "'add'"
		set_form_value "stratos" "mode" "'ip'"
	end_function

	init_function "form_edit" "id,ip,comment"
		script_formshow "stratos" "edit"
		hide "__To"
		set_form_value "stratos" "action" "'edit'"
		set_form_value "stratos" "id" "id"
		set_form_value "stratos" "ip_address" "ip"   
		set_form_value "stratos" "comment" "comment"
	end_function

	init_validation "validate_form"
		add_validation "ip_address" "VALID_ISNOTNULL"
		add_validation "comment" "VALID_ALPHANUMERIC"
		add_validation "comment" "VALID_ISNOTNULL"
	end_validation
end_script

body " Lockon Stratos" "lockon.png"

init_infoitem
	infoitem_form "About Stratos:" "" "Stratos file is a list of of IP/IP_ranges or network/subnetworks."
	infoitem_form "Description:" "" "Stratos file can act in one of the following ways:
	<br> as 'black list': perfect to specify to which nets or ips the lock must be applied.
	<br> or 'friend list': its intended is to set a list of privileged ips<br>
	(perfect to declare the ip address of boss and other administrative addresses.)<br>
	<b>Lockon will decide how use the stratos list according to<br>the 'mode' and 'lck field' selected for you in the config page.</b>"
	infoitem_form "Using stratos list as:" "" "$STMODE"
end_infoitem

init_form "stratos" "470px" "$BFW0066" "stratos.cgi" "validate_form"
	init_infoitem
		input_hidden "id" ""
		input_hidden "action" ""
		infoitem_form "IP Address" "$(input_textbox "ip_address" "" "31" "103px")" "User IP or subnet address (required)"
		infoitem_form "To" "Optional: $(input_textbox "ip_range" "" "31" "103px")" "Another ip (this will be use stored as: 0.0.0.0-0.0.0.0)"
		infoitem_form "Comment" "$(input_textbox "comment" "" "25" "280px")" "Comment"
	end_infoitem
end_form

init_listview_without_comment "IP Address,160px" "Comment,250px"
	ID=1
	while read ip comment; do
		listview_add "$ID" "$ip" "$comment"
		ID=$(( $ID + 1 ))
	done < $STRATOSFILE
end_listview_without_reload

init_script
    echo "select_report('$SQUID_REPORT');"
end_script

end_body
[ ! -z "$gurenadd" ] && { init_script; alert "$gurenadd"; end_script; }
end_html
