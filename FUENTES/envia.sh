
#/bin/sh
a=(`date | sed -e 's/[:-]/ /g'`)
#echo ${a[*]}
dos=${a[2]}
tres=${a[1]}
cuatro='/mnt/flash/automata/AVISOS/'
cinco='.txt'
siete='ENVIA'
ocho='ESTADISTICAS'
archivo=$cuatro$dos$tres$cinco
final=$cuatro$dos$tres$siete$cinco
#cat $archivo

sed 's/$'"/`echo \\\r`/" $archivo > $final
sleep 15
python  /mnt/flash/automata/completo.py > $cuatro$dos$tres$ocho$cinco
sleep 25

python  /mnt/flash/automata/cuatro.py  

















