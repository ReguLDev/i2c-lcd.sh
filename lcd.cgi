#!/bin/bash
##########################################################
#i2c lcd script by Michael S. Ageev (c) midiserver@mail.ru
# Russia 2017
##########################################################
#Usage: ./lcd.sh "hello World!"
#
#sda_gpio=18
#scl_gpio=20
i2c_adres=0x3f



echo "Content-Type: text/html; charset=UTF-8;"
echo "Cache-Control: no-cache"
echo
echo $OUT_STRING
#insmod i2c-dev
#insmod i2c-gpio-custom bus0=0,$sda_gpio,$scl_gpio
print_html_head(){
#<meta http-equiv="Refresh" content="10" />
cat << END
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<HEAD>
<title>i2c LCD</title>
<link rel="shortcut icon" href="/logo/small-icon.ico" type="image/x-icon">
<META http-equiv=Content-Type content="text/html; charset=UTF-8">
<script type="text/javascript" 
src="http://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js">
</script>

</head>

<body>
<form>
    <label>TEXT</label>
<!--    <input type="text" name="str1" height="2em" width="16em" maxlength="32">--><br>
    <textarea cols="15" rows="2" name="str" maxlength="32" wrap="hard"></textarea>
    <p><input type="submit" value="Send to LCD"></p>
</form>

<pre>
END
}



led=8
ansi=48
write_CMD () {
: $((hb = $c & 240))
: $((lb = ($c << 4)  & 240 ))

		hh=$((4 + $hb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((0 + $hb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((4 + $lb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((0 + $lb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
}


print_LCD () {
: $((hb = $c & 240))
: $((lb = ($c << 4)  & 240 ))

		hh=$((5 + $hb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((1 + $hb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((5 + $lb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
		hh=$((1 + $lb + $led))
	i2cset -f -y 0 $i2c_adres $hh > /dev/null
}

##########  init LCD  #####################
init_LCD () {
c=3
write_CMD
c=3
write_CMD
c=2
write_CMD
c=40	#28
write_CMD
c=44 #2C
write_CMD
c=44 #2C
write_CMD
c=12 #0C
write_CMD
c=1
write_CMD
c=6
write_CMD
c=2
write_CMD
}
###############################


init_LCD

print_html_head
eval `echo "${QUERY_STRING}"|tr '&' ';'`
echo "<br>str=$str<br>utme=$utme"

temp_string=${str//%/\\x}
#printf '%s\n' "$temp_string"
# output: \xD1\x80\xD0\xB5\xD1\x81\xD1\x83\xD1\x80\xD1\x81\xD1\x8B
str=`echo -e $temp_string `


#echo ${#1}
now=0
str=`echo $str | sed 's/\ /_/g' | sed 's/\S/& /g'`
str=`echo $str | sed 's/\+/'_'/g'`

#str="  1 "


#echo $str > /tmp/11111

printf "\n--------------------\n"
printf "|       L C D      |"
printf "\n====================\n| "
now_pos=0
#c=0x80 # stroka - 1
#write_CMD
for all in $str
do

    c=`printf "%d\n" \'$all`
	if  [ $c -eq 95 ]; 
	then
	    c=32
	    echo -n " "
	else
		echo -n $all
	fi
	 

#    echo $all=$c $now_pos
#echo -n $all
print_LCD
    now_pos=`expr $now_pos + 1`
	if  [ $now_pos -eq 16 ]; 
	then
		printf " |\n| "
	    	c=0xC0 # stroka - 2
		write_CMD
	fi
	if  [ $now_pos -eq 32 ]; 
	then
		echo
	    	c=0x94 # stroka - 3
		write_CMD
	fi
	if  [ $now_pos -eq 48 ]; 
	then
		echo
	    	c=0xD4 # stroka - 4
		write_CMD
	fi
	if  [ $now_pos -eq 64 ]; 
	then
	    	c=0x80 # stroka - 1
		write_CMD
	fi

done



if [ "$now_pos" -lt "32" -a "$now_pos" -gt "16" ]; 
	then
	for i in `seq $now_pos 32`; do
		printf " "
	done
	printf "|\n"

fi

if [ "$now_pos" -lt "48" -a "$now_pos" -gt "32" ]; 
	then
	for i in `seq $now_pos 32`; do
		printf " "
	done
	printf "|\n"

fi


if [ $now_pos -lt 16 ];                                                                                                                               
        then                          
        for i in `seq $now_pos 16`; do     
                printf " "         
        done                          
        printf "|\n"      
                                      
fi      
printf "====================\n\n"
echo "</pre></body></html>"
