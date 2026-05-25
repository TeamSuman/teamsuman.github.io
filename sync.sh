#!/usr/bin/env bash

PYTHON_BIN=${PYTHON_BIN:-python}

find_available_port() {
  local port=1236
  while lsof -i:$port >/dev/null 2>&1; do
    ((port++))
    if [ $port -gt 1300 ]; then
      echo "Error: No available ports found in range 1236-1300"
      return 1
    fi
  done
  echo $port
}

restore_sync_flag() {
  sed -i "s/sync = True/sync = False/" home/views.py
}

make_export_links_relative() {
  local file="$1"

  sed -i \
    -e 's|href="/"|href="index.html"|g' \
    -e "s|href='/'|href='index.html'|g" \
    -e 's|href="/news"|href="news.html"|g' \
    -e "s|href='/news'|href='news.html'|g" \
    -e 's|href="/research"|href="research.html"|g' \
    -e "s|href='/research'|href='research.html'|g" \
    -e 's|href="/publication"|href="publication.html"|g' \
    -e "s|href='/publication'|href='publication.html'|g" \
    -e 's|href="/softwares"|href="softwares.html"|g' \
    -e "s|href='/softwares'|href='softwares.html'|g" \
    -e 's|href="/team"|href="team.html"|g' \
    -e "s|href='/team'|href='team.html'|g" \
    -e 's|href="/positions"|href="positions.html"|g' \
    -e "s|href='/positions'|href='positions.html'|g" \
    -e 's|href="/gallery"|href="gallery.html"|g' \
    -e "s|href='/gallery'|href='gallery.html'|g" \
    -e 's|href="/contacts"|href="contacts.html"|g' \
    -e "s|href='/contacts'|href='contacts.html'|g" \
    -e 's|="/static/|="static/|g' \
    -e "s|='/static/|='static/|g" \
    -e 's|url("/static/|url("static/|g' \
    -e "s|url('/static/|url('static/|g" \
    -e 's|url(/static/|url(static/|g' \
    -e 's|="/media/|="media/|g' \
    -e "s|='/media/|='media/|g" \
    -e 's|url("/media/|url("media/|g' \
    -e "s|url('/media/|url('media/|g" \
    -e 's|url(/media/|url(media/|g' \
    "$file"
}

sync() {
  port=$(find_available_port)
  if [ $? -ne 0 ]; then
    restore_sync_flag
    exit 1
  fi

  trap 'restore_sync_flag; kill -9 $(lsof -t -i:$port) 2>/dev/null' EXIT

  rm -f nohup.out ./*.html
  "$PYTHON_BIN" manage.py collectstatic --noinput

  sed -i "s/sync = False/sync = True/" home/views.py
  nohup "$PYTHON_BIN" manage.py runserver $port &
  sleep 5

  if ! lsof -i:$port >/dev/null; then
    echo "Error: Cannot run server on port $port"
    restore_sync_flag
    exit 1
  fi

  for page in "" research news positions publication gallery contacts team softwares; do
    wget -q -O /dev/null "http://127.0.0.1:$port/$page"
    file="${page:-index}.html"
    make_export_links_relative "$file"
    echo "created $file"
    sleep 3
  done

  restore_sync_flag
  kill -9 $(lsof -t -i:$port) 2>/dev/null
  trap - EXIT
}
#export local file to pythonanywhere.com
#rsync -avzhe ssh ./* teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website/ --exclude "*settings.py"
#import files from pythonanywhere to local repository
#rsync -avzhe ssh teamsuman@ssh.pythonanywhere.com:/home/teamsuman/website .

# Sync github account after files are synced..
sync
#git add . && git commit -m "message" && git push origin django
