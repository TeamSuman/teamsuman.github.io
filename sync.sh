sync ()
{
    #remove the html files
    rm nohup.out
    rm *html
    # Change sync status in views.py
    sed -i "s/sync = False/sync = True/" home/views.py
    #making the server up
    nohup python manage.py runserver 1236 & 
    # Render the pages and save them
    content=`wget -O - http://127.0.0.1:1236/`
    wait
    content=`wget -O - http://127.0.0.1:1236/research`
    wait 
    content=`wget -O - http://127.0.0.1:1236/news`
    wait
    content=`wget -O - http://127.0.0.1:1236/positions`
    wait
    content=`wget -O - http://127.0.0.1:1236/publication`
    wait
    content=`wget -O - http://127.0.0.1:1236/gallery`
    wait
    content=`wget -O - http://127.0.0.1:1236/contacts`
    wait
    content=`wget -O - http://127.0.0.1:1236/team`
    wait
    content=`wget -O - http://127.0.0.1:1236/softwares`
    wait
    #change sync status in views.py
    sed -i "s/sync = True/sync = False/" home/views.py

    #kill the server
    kill -9 $(lsof -t -i:1236)
}
#export local file to pythonanywhere.com
#rsync -avzhe ssh ./* teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website/ --exclude "*settings.py"
#import files from pythonanywhere to local repository
#rsync -avzhe ssh teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website . 

# Sync github account after files are synced..
#sync
git add . && git commit -m "message" && git push origin django
