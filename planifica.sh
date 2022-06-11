#/bin/sh

lanza(){
pacientes=80
contador=2


     while(($pacientes>0))
          do
            python /mnt/flash/automata/envia.py $(head -$contador  /mnt/flash/automata/direcciones.txt | tail -1) & 
            echo " EJECUTANDO PACIENTE.......$pacientes "
            pacientes=$(( pacientes-1 ))
            contador=$(( contador+1 )) 
          done
        }

fork(){
    count=0
    while (($count<1))
    do
      lanza &
      count=$(( count+1))
    done
}

fork



