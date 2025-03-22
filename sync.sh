find_available_port() {
    local port=1236
    while lsof -i:$port > /dev/null 2>&1; do
        ((port++))
        if [ $port -gt 1300 ]; then
            echo "Error: No available ports found in range 1236-1300"
            return 1
        fi
    done
    echo $port
}

sync() {
    port=$(find_available_port)
    if [ $? -ne 0 ]; then
        sed -i "s/sync = True/sync = False/" home/views.py
        exit 1
    fi

    rm -f nohup.out *html
    sed -i "s/sync = False/sync = True/" home/views.py
    nohup python manage.py runserver $port & 
    sleep 5

    if ! lsof -i:$port > /dev/null; then
        echo "Error: Cannot run server on port $port"
        sed -i "s/sync = True/sync = False/" home/views.py
        exit 1
    fi

    for page in "" research news positions publication gallery contacts team softwares; 
    do
        content=`wget -O - "http://127.0.0.1:$port/$page"`
        echo "created $page.html"
        sleep 3
    done

    sed -i "s/sync = True/sync = False/" home/views.py
    kill -9 $(lsof -t -i:$port)
}
#export local file to pythonanywhere.com
#rsync -avzhe ssh ./* teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website/ --exclude "*settings.py"
#import files from pythonanywhere to local repository
#rsync -avzhe ssh teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website . 

# Sync github account after files are synced..
sync
#git add . && git commit -m "message" && git push origin django
