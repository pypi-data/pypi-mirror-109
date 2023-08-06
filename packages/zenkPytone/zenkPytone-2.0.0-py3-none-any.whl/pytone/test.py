import kintone
import kintone_file

kintone = kintone.Kintone(authText='bV90c3VydXlhQHplbmsuY28uanA6MjcxOG1pc3V0QQ==', domain='develfhvn', app=10)

kintone_file = kintone_file.KintoneFile(authText='bV90c3VydXlhQHplbmsuY28uanA6MjcxOG1pc3V0QQ==', domain='develfhvn')
fileKey = "20210610114308F5314C134D434CAF960734D011B964A2359"

kintone_file.downloadFile(fileKey)

# where = '$id < 101 '
# field = ['$id']
# order = 'order by $id desc'
# print((kintone.select(where=where, fields=field, order=order)))