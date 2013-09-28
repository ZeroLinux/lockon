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

if [ -n "$FORM_bt_save" ]; then
	FILECONFIG="$CONFIG"
	setvar "$FILECONFIG" "MODE" "${FORM_MODE}${FORM_FIELD}"
	setvar "$FILECONFIG" "MIRROR" "$FORM_MIRROR"
	setvar "$FILECONFIG" "PORTAL" "$FORM_PORTAL"
	if [ -z "$FORM_TIMER" ]; then
		FORM_TIMER="false"
		sed -i '/lockon stop/d' $CRON
		sed -i '/lockon start/d' $CRON
		RSTCRON="true"
	else
		if [ "$TIMERINIT" != "$FORM_TIMERINIT" ]; then
			sed -i '/lockon stop/d' $CRON
		 	echo "${FORM_TIMERINIT##*:} ${FORM_TIMERINIT%%:*} * * * lockon stop" >> $CRON
			RSTCRON="true"
		fi
		if [ "$TIMEREND" != "$FORM_TIMEREND" ]; then
			sed -i '/lockon start/d' $CRON
			echo "${FORM_TIMEREND##*:} ${FORM_TIMEREND%%:*} * * * lockon start" >> $CRON
			RSTCRON="true"
		fi
	fi
	setvar "$FILECONFIG" "TIMER" "$FORM_TIMER"
	if [ "$DYN" != "$FORM_DYN" ]; then
		[ "$FORM_DYNMODE" = "HRS" ] && SKEL="* */${FORM_DYN} * * *" || SKEL="*/${FORM_DYN} * * * *"
		sed -i '/lockon update/d' $CRON
		echo "$SKEL lockon update --all" >> $CRON
	fi
	[ "$RSTCRON" = "true" ] && { /etc/init.d/cron restart >/dev/null 2>&1; }
	needsave
	. $FILECONFIG
fi

[ -n "$FORM_serv_start" ] && /etc/init.d/lockon start >/dev/null 2>&1
[ -n "$FORM_serv_stop" ] && /etc/init.d/lockon stop >/dev/null 2>&1
[ -n "$FORM_serv_reload" ] && /etc/init.d/lockon restart >/dev/null 2>&1

[ ${MODE:0:1} -eq 2 ] && AENABLE=1;
[ ${MODE:1:2} -eq 2 ] && BENABLE=1;

if [ "$TIMER" = "true" ]; then
	CHECKED=1
	TIMERINIT="$(grep -w 'lockon stop' /etc/brazilfw/cron.cfg | awk '{print $2":"$1}')"
	TIMEREND="$(grep -w 'lockon start' /etc/brazilfw/cron.cfg | awk '{print $2":"$1}')"
fi

varDYN="$(grep -w 'lockon update --all' /etc/brazilfw/cron.cfg | awk '{if($2=="*") {print "M"$1} else{print "H"$2}}')"
timeDYN="${varDYN:0:1}"
[ "$timeDYN" = "M" ] && hselect=1;
DYN="${varDYN##*/}"

[ -n "$FORM_mkbackup" ] && tar -zcvf /var/htdocs/webadmin/lockon/lockon_backup.tar.gz lockon -C /partition >/dev/null 2>&1
[ -n "$FORM_rmbackup" ] && rm /var/htdocs/webadmin/lockon/lockon_backup.tar.gz >/dev/null 2>&1

message() {
 echo "<script>$(alert "$1")</script>" 
}

init_html
body " Lockon Configuration" "lockon.png"

custom_form_config() {
echo "<form enctype=\"multipart/form-data\" id=\"$1\" method=\"POST\" action=\"$4\" onSubmit=\"__CL_find(this);$([ -n "$5" ] && echo "return $5(this);")\" style=\"display: block;\">"
__init_table "formview"
__header_table ",10px" "$3<label id=\"form_action\"></label>,$2" ",10px"
echo "</tr><tr class=\"listview_item\"><td class=\"bl\"></td><td>"
}

lockonstat="$($lockonbin service isactive)"

custom_form_config "guren" "650px" "General Configuration" "./config.cgi" ""
	init_infoitem
		infoitem_form "Mode: " "$(init_combobox "MODE" "70px"; combobox_add "1" "whitelist"; combobox_add "2" "blacklist" $AENABLE;end_combobox)" "
		<b>Whitelist:</b> Domains declared in lockon will be allowed<br>
		<b>Blacklist:</b> Domains declared in lockon will be blocked"
		infoitem_form "Lck Field: " "$(init_combobox "FIELD" "85px"; combobox_add "1" "All network"; combobox_add "2" "List only" $BENABLE;end_combobox)" "
		<b>All network:</b> Selected policy will be applied to all network (ports: 80,443)<br>
		<b>List only:</b> Selected policy will be applied to IP/network/ranges declared in the <a href=\"stratos.cgi\">stratos</a> section<br>"
		infoitem_form "Helper Mirror: " "$(input_textbox "MIRROR" "$MIRROR" "90" "260px")" "Mirror for lockon ip lists, <br/>this let you download ready ip lists for lockon"
		infoitem_form "Portal: " "$(input_textbox "PORTAL" "$PORTAL" "30" "160px")" "IP where the portal is running"
		infoitem_form "Enable Timer/Time: " "$(input_checkbox "TIMER" "true" "$CHECKED" "") stop at: $(input_textbox "TIMERINIT" "$TIMERINIT" "5" "40px") restart at: $(input_textbox "TIMEREND" "$TIMEREND" "5" "40px")" "Stop lockon in this time range.<br/>Please use 24 hour format<br/>Example: 13:00, 14:30, 00:00 (for midnight)."
		infoitem_form "Run dynames every: " "$(input_textbox "DYN" "$DYN" "2" "30px") $(init_combobox "DYNMODE" "70px"; combobox_add "HRS" "Hours"; combobox_add "MIN" "Minutes" $hselect; end_combobox)" "The scan time frequency for domains market as 'dynamic'.<br/>Be carefull with this field, you can compromise the performance of your server."
		[ ! "$(ls /var/htdocs/webadmin/lockon/lockon_backup.tar.gz)" ] && infoitem_form "Backup:" "$(button " Generate " "mkbackup" "submit" "")" || infoitem_form "Backup" "$(button " Generate " "mkbackup" "submit" "")<br/> <a href=\"lockon_backup.tar.gz\">Click to Download</a> ($(date -r lockon_backup.tar.gz +%F@%H:%M:%S)) $(button "Delete" "rmbackup" "submit" "")"
		infoitem_form "Restore" "Use this box to upload a backup file.tar.gz of lockon<br/><input class=\"input_file\" type=\"file\" name=\"Logo\" onchange=\"document.getElementById('uploadfile').value=basename(this.value);\">
		<div><input class=\"form\" type=\"text\" id=\"uploadfile\"><div class=\"upload_button\"><div class=\"find_text\">$BFW0201</div></div></div>"
		infoitem_form "is active?:" "$lockonstat"
		infoitem_form "$BFW0055:" "$(button_services 1 0 1 1)"
		infoitem_form "Important" "<br><b>In order to change the Lockon Configuration,<br/>you must stop lockon first to be able to change this values</b>"
	end_infoitem
end_form_config

init_script
	if [ "$lockonstat" = "true" ]; then
		disable "MODE"
		disable "FIELD"
		disable "MIRROR"
		disable "PORTAL"
		disable "TIMER"
		disable "TIMERINIT"
		disable "TIMEREND"
		disable "DYN"
		disable "DYNMODE"
		hide "__Restore"
		disable "__serv_start"
		disable "__bt_save"
	else
		disable "__serv_reload"
		disable "__serv_stop"
		hide "__Important"
	fi
end_script

if [ -n "$FORM_FILENAME" ]; then
	if [ "${FORM_FILENAME##*.}" = "gz" ]; then
		message "File detected: Lockon Backup"
		mv $FORM_FILENAME /tmp/lockon.tar.gz
		tar -zxvf /tmp/lockon.tar.gz -C /partition >/dev/null 2>&1
		[ "$?" -eq 0 ] && echo "Backup restored successful" || echo "Backup extract fail!, pls try again."
		rm /tmp/lockon.tar.gz
	else
		message "Unknow File Type."
	fi
fi

end_body
end_html
