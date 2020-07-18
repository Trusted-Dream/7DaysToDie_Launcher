#!/bin/bh
DIR=$(cd $(dirname $0); pwd)
PID=$(ps x |grep sdtd_run.py |grep -v grep |awk '{print $1}')

case "$1" in
  "start" )
        if [[ $PID == "" ]]; then
            env python $DIR/sdtd_run.py > /dev/null &
            sleep 3
            PID=$(ps x |grep sdtd_run.py |grep -v grep |awk '{print $1}')
            date +"%Y-%m-%d %H:%M:%S --- [$PID] start"
        else
            echo "pid already exists.[$PID]"
        fi
        ;;

  "restart" )
        if [[ $PID != "" ]]; then
            kill -9 $PID
            sleep 2
            date +"%Y-%m-%d %H:%M:%S --- [$PID] kill ok"
        fi
        env python $DIR/sdtd_run.py > /dev/null &
        sleep 3
        PID=$(ps x |grep sdtd_run.py |grep -v grep |awk '{print $1}')
        date +"%Y-%m-%d %H:%M:%S ---[$PID] start"
        ;;

  "stop" )
        if [[ $PID != "" ]]; then
            kill -9 $PID
            sleep 2
            date +"%Y-%m-%d %H:%M:%S --- [$PID] kill ok"
        else
            echo "pid does not exist."
        fi
        ;;

  "status" )
        if [[ $PID != "" ]]; then
            echo "running PID:"$PID
        else
            echo "not running."
        fi
        ;;

  * )
        if [[ $PID != "" ]]; then
            kill -9 $PID
            sleep 2
            date +"%Y-%m-%d %H:%M:%S --- [$PID] kill ok"
        fi
        env python $DIR/sdtd_run.py > /dev/null &
        sleep 3
        PID=$(ps x |grep sdtd_run.py |grep -v grep |awk '{print $1}')
        date +"%Y-%m-%d %H:%M:%S --- [$PID] start"
esac
