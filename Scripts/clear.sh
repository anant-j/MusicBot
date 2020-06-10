while :
do 
    if [ "$(ls -b | wc -l)" -gt 50 ];
    then
    echo "Cleared"
    sleep 5
    else
    echo "done"
    sleep 1
    fi
done
