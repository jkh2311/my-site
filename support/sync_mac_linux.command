#!/bin/sh
cd "$(dirname "$0")"
python3 update_gov24_data.py
printf '\n완료. 엔터를 누르면 닫힙니다.'
read _x
