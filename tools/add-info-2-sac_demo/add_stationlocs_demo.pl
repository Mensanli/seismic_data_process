#!/usr/bin/env perl
# last mod:2021.6 
# @msl

open(PICK,"<","phase_info.dat")||die"cannot open the file:$!\n";
open(IDDIR,"<","iddir.dat")||die"cannot open the file:$!\n";
 
#将pick.dat数组的第1/3/5列分别写入数组id,a,t0;
#(split后lines的长度会变化,不再是行数,而是被split为几份),$id[$i]=@lines[1](注意$i,而不能是i);
#BCB014,7553,26.2287,100.0115,2203,2021,150,21,16,41,24,25.5140,100.0309,1.8,13.35,Pg,24.99,Sg
$i=0;
while(<PICK>){
	@lines=split(",");
	$id[$i]=@lines[1];
	$sta[$i]=@lines[0];
	$lon[$i]=@lines[3];
	$lat[$i]=@lines[2];
	$elv[$i]=@lines[4];
	$year[$i]=@lines[5];
        $julday[$i]=@lines[6];
        $hour[$i]=@lines[7];
        $min[$i]=@lines[8];
        $sec1[$i]=@lines[9];
        $sec2[$i]=@lines[10];
        $elat[$i]=@lines[11];
	$elon[$i]=@lines[12];
	$eelv[$i]=@lines[13];
	$t1[$i]=@lines[14];
	$t2[$i]=@lines[16];
#	$a[$i]=@lines[8];
#	$t0[$i]=@lines[11];
	$i=$i+1;
}
$size=$i;
 
#将iddir.dat数组的第1/2列分别写入iddir数组的第一列和第二列;
$i=0;
while(<IDDIR>){
	@lines2=split(" ");
	$iddir[$i][0]=$lines2[0];
	$iddir[$i][1]=$lines2[1];
	print"$iddir[$i][0] $iddir[$i][1]\n";
	$i=$i+1;
}
$size2=$i;
 
$iddirr=$iddir[0][1]; #目录
$evid=$iddir[0][0]; #id
 
$dir="./wave-dir/wave_demo/2021";
#$dir="./temps-dir/test_some";
chdir $dir;
print "$dir\n";
$st=0;
#遍历pick.dat中每一行;
for($i=0;$i<$size;$i++){
	if($evid != $id[$i]){
		$node=$i;
		$dir="./$iddirr";
		chdir $dir;
		mkdir "$dir_l";
		print "$dir\n";	
	#在每个地震事件文件夹中遍历.SAC文件
	for($j=$st;$j<$node;$j++){
	print "$j\n";	
	open(SAC, "| sac") or die "Error in opening SAC\n";
	print SAC "wild echo off \n";
	
	print "$sta[$j]\n";
	print "$lat[$j],$lon[$j],$elv[$j]\n";
        
	print SAC "r $sta[$j]* \n";
	print SAC "ch  stlo $lon[$j]  \n";
	print SAC "ch   stla $lat[$j]  \n";
	print SAC "ch   stel $elv[$j] \n";
        print SAC "ch evla $elat[$j] \n ";
        print SAC "ch evlo $elon[$j]  \n";	
        print SAC "ch O GMT  $year[$j]  $julday[$j] $hour[$j] $min[$j] $sec1[$j] $sec2[$j]0  \n";
	print SAC "ch allt (0 - &1,o&) iztype IO \n";
	print SAC "ch t1 $t1[$j] \n";
	print SAC "ch t2 $t2[$j] \n";
	print SAC "ch LCALDA TRUE \n";
	print SAC "wh \n";
	print SAC "q \n";
 
	close(SAC);
	
  	}
	chdir "..";
	$st=$node;
	$evid=$id[$i];
	for($j=0;$j<$size2;$j++){
		if($iddir[$j][0] eq $evid){
			$iddirr=$iddir[$j][1];			
		}
	
	
	}
	}
}
