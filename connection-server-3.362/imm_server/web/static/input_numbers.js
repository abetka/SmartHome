// copyright 1999 Idocs, Inc. http://www.idocs.com
// Distribute this script freely but keep this notice in place
// copied from http://www.htmlcodetutorial.com/forms/index_famsupp_158.html

function is_special_key_code(key_code) {
    /* backspace, delete, left, right */
    return ( key_code == 23 || key_code == 8   || key_code == 119
                            || key_code == 113 || key_code == 114 );
}


function block_non_numbers_v2(obj, e, allowDecimal, allowNegative) {

//<input type='text' onkeypress='validate(event)' />

  var theEvent = e || window.event;

  // Handle paste
  if (theEvent.type === 'paste')
  {
      key = event.clipboardData.getData('text/plain');
  }

  // Handle key press
  else
  {
      var key = theEvent.keyCode || theEvent.which;
      key = String.fromCharCode(key);
  }

  var regex = /[^0-9]/;
  if( regex.test(key) )
  {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}

function block_non_numbers(obj, e, allowDecimal, allowNegative) {
  var key;
  var isCtrl = false;
  var keychar;
  var reg;
    
  e = e || window.event;
  if(window.event) {
    key = e.keyCode;
    isCtrl = window.event.ctrlKey
  }else if(e.which) {
    key = e.which;
    isCtrl = e.ctrlKey;
  }
  
  if (isNaN(key)) return true;
  keychar = String.fromCharCode(key);
  // check for backspace or delete, or if Ctrl was pressed
  if (isCtrl || is_special_key_code(key)) {
    return true;
  }

  reg = /\d/;
  var isFirstN = allowNegative ? keychar == '-' && obj.value.indexOf('-') == -1 : false;
  var isFirstD = allowDecimal ? keychar == '.' && obj.value.indexOf('.') == -1 : false;

  return isFirstN || isFirstD || reg.test(keychar);
}

function count_occurence_of(s, c) {
	var count = 0;
	for (i = 0; i < s.length; ++i) {
		if (s[i] == c) ++count;
	}
	return count;
}

function allow_ip_address_chars(obj, e) {
  var key;
  var isCtrl = false;
  var keychar;
  var reg;
    
  e = e || window.event;
  if(window.event) {
    key = e.keyCode;
    isCtrl = window.event.ctrlKey
  }else if(e.which) {
    key = e.which;
    isCtrl = e.ctrlKey;
  }
  
  if (isNaN(key)) return true;
  keychar = String.fromCharCode(key);
  // check for backspace or delete, or if Ctrl was pressed
  if (key == 8 || is_special_key_code(key)) {
    return true;
  }

  if (keychar == '.' && count_occurence_of(obj.value, '.') > 2) return false;

  reg = /[\d.:a-fA-F]/;

  return reg.test(keychar);

}

