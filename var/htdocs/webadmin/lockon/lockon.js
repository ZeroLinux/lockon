/*
 * Copyright (C) 2013 Carlos Rincón <carlosrincon2005@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

var countBox = 1;
var spareDiv = new Array();
var ncount = 1;
for (i = 0; i < 20; i++){
    spareDiv[i] = ncount;
    ncount++;
}

function addInput(){
	var idn = spareDiv[0];
	var spanElement = document.getElementById('responce');
	var boxName="url"+spareDiv[0];
	var secValue="secure"+spareDiv[0];
	var dynValue="dynamic"+spareDiv[0];
	var divValue="div"+spareDiv[0];
	//create div container
	var divNew = document.createElement("div");
	divNew.id = divValue;
	//create button [-]
	var newButton = document.createElement("input");
	newButton.type = "button";
	newButton.onclick = function(){remInput(this.parentNode,idn);};
	newButton.value = "-";
	//create input [text]
	var newText = document.createElement("input");
	newText.type = "text";
	newText.className = "form";
	newText.id = boxName;
	newText.name = boxName;
	newText.style.width = "260px";
	//create input [checkbox]
	var newSecBox = document.createElement("input");
	newSecBox.type = "checkbox";
	newSecBox.id = secValue;
	newSecBox.name = secValue;
	newSecBox.value = "true";
	//create input [checkbox]
	var newDynBox = document.createElement("input");
	newDynBox.type = "checkbox";
	newDynBox.id = dynValue;
	newDynBox.name = dynValue;
	newDynBox.value = "true";
	//create text [as labels]
	var secLabel = document.createTextNode("SSL");
	var dynLabel = document.createTextNode("Balanced");
	if (spareDiv.length > 0){
		//DOM : add div to responce
		spanElement.appendChild(divNew);
		var divElement = document.getElementById(divValue);
		//DOM : fill the new div.
		divElement.appendChild(newButton);
		divElement.appendChild(newText);
		divElement.appendChild(newSecBox);
		divElement.appendChild(secLabel);
		divElement.appendChild(newDynBox);
		divElement.appendChild(dynLabel);
		countBox += 1;
		var i = spareDiv.indexOf(idn);
		spareDiv.splice(i, 1);
	}
}

function remInput(element,id){
	var parent=document.getElementById('responce');
	parent.removeChild(element);
	var i = spareDiv.length;
	spareDiv[i]=id;
}

function loadXMLDoc(layer,url){
	var xmlhttp;
	xmlhttp=new XMLHttpRequest();

	xmlhttp.onreadystatechange=function(){
  		if (xmlhttp.readyState==4 && xmlhttp.status==200){
    		document.getElementById(layer).innerHTML=xmlhttp.responseText;
    	}
  	}

	xmlhttp.open("GET",url,true);
	xmlhttp.send();
}
