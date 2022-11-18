import requests
import json
import markdown


def get_content(title, halo_key):
    # 文章的网址
    url_search = url_halo_main + '/api/content/posts?keyword=' + \
        title + '&api_access_key=' + halo_key
    url_get_content = url_halo_main + \
        '/api/content/posts/articleId?&api_access_key=' + halo_key

    # 查找文章清单
    s = requests.get(url_search)
    t = json.loads(s.text)
    for i in t['data']['content']:
        if i['title'] == title:
            id = i['id']
    # print(id)
    # 获取文章内容
    response = requests.get(url_get_content.replace('articleId', str(id)))
    t = json.loads(response.text)
    originalContent = t['data']['originalContent']
    # 持久化存储
    with open(title + ".md", 'w') as f:
        f.write(originalContent)

    # 将文章内相对路径改成绝对路径
    newcontent = originalContent.replace(
        '(https://www.furrydragon.top/upload/', '(' + url_halo_main + '/upload/')
    newcontent = newcontent.replace(
        '(https://www.furrydragon.top/archives/', '(' + url_halo_main + '/archives/')
    return newcontent


if __name__ == '__main__':
    # 1.halo博客主站网址
    url_halo_main = 'http://www.furrydragon.top'
    # 2.halo后台配置的api_access_key
    halo_key = 'joe2.0'
    title_list = []
    while 1:
        title = input('请输入文章标题(0 exit)：')
        if title == '0':
            break
        else:
            title_list.append(title)
    print(title_list)
    for title in title_list:
        title.encode("utf-8").decode("latin-1")
        content = get_content(title, halo_key)
