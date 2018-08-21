from pymysql import connect
from pymysql import cursors
import json
from pyvi import *

config_path = "../config.json"

def init():
    with open(config_path) as config_buffer:
        config = json.loads(config_buffer.read())
    return config['HOST'],config['DB_NAME'],config['USER_NAME'],config['PASSWORD']

def get_connection():
    HOST,DB_NAME,USER_NAME, PASSWORD = init()
    conn = connect(host=HOST, user=USER_NAME, passwd=PASSWORD, db=DB_NAME, charset='utf8')
    conn.autocommit(False)
    return conn


def get_cursor(conn):
    """

    :rtype: pymysql.cursors.Cursor
    :param conn:
    :return:
    """
    cur = conn.cursor()
    return cur


def get_dict_cursor(conn):
    """

    :rtype: pymysql.cursors.Cursor
    :param conn:
    :return:
    """
    cur = conn.cursor(cursors.DictCursor)
    return cur


def free_connection(conn, cur):
    """

    :param conn:
    :param cur:
    :return:
    """
    try:
        cur.close()
        conn.close()
    except:
        pass
    

def get_token(news_id):
    query = "SELECT * FROM recsys.news_token WHERE news_id = %s" % news_id
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchone()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row


def get_news(news_id):
    query = "SELECT * FROM news.news_resource WHERE newsId = %s" % news_id
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchone()
    except Exception as e :
        print (e)
    finally:
        free_connection(conn, cur)
    return row


def get_news_update():
    query ="SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
            "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
            "recsys.news_token.content_postag," \
            "news.news_resource.title, news.news_resource.url" \
            "   FROM news.news_resource " \
            "   INNER JOIN recsys.news_token ON  news.news_resource.newsId = recsys.news_token.news_id" \
            "   WHERE news.news_resource.publishDate >= NOW() - INTERVAL 30 DAY AND  news.news_resource.publishDate < NOW() " \
           "    LIMIT 10000"

    print(query)
    conn = None
    cur = None
    row = None #ORDER BY publishDate DESC LIMIT 10000


    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row


def get_news_list(list) :
    query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
            "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
            "recsys.news_token.content_postag," \
            "news.news_resource.title, news.news_resource.url " \
            "   FROM recsys.news_token " \
            "   INNER JOIN news.news_resource ON  news.news_resource.newsId = recsys.news_token.news_id" \
            "   WHERE recsys.news_token.news_id in (%s)" % ','.join(map(str, list))
    # print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        free_connection(conn, cur)
    return row

def get_new(id) :
    query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
            "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
            "recsys.news_token.content_postag," \
            "news.news_resource.title, news.news_resource.url" \
            " FROM recsys.news_token " \
            " INNER JOIN news.news_resource ON  news.news_resource.newsId = recsys.news_token.news_id" \
            " WHERE recsys.news_token.news_id = %s" %id
    # print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        free_connection(conn, cur)
    return row

def get_new_nearly(last_day) :
    """
    get news have publishDate > last_day

    :param last_day: last date of table extract_tags
    :return: list of the news
    """
    query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
            "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
            "recsys.news_token.content_postag," \
            "news.news_resource.publishDate,news.news_resource.insertDate," \
            "news.news_resource.title, news.news_resource.url" \
            " FROM recsys.news_token " \
            " INNER JOIN news.news_resource ON  news.news_resource.newsId = recsys.news_token.news_id" \
            " WHERE news.news_resource.publishDate > '%s'" \
            " LIMIT 1000" %last_day

    # print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        free_connection(conn, cur)
    return row


def get_tags_limit_day():
    """
    recsys.tag_extractor_2
    :return:
    """
    query = """SELECT * FROM recsys.tag_extractor_2
                WHERE `publishDate` >= NOW() - INTERVAL 30 DAY
                AND `publishDate`  < NOW();"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row


def get_last_day():
    query = """SELECT MAX(publishDate) as last_date FROM recsys.tag_extractor_2"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchone()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

def insert(id ,updateTime, publishTime,tags) :

    query = "INSERT INTO recsys.tag_extractor_2 (newsId,updateTime,publishDate,tags) VALUES (%s, '%s','%s','%s')" %(id,updateTime,publishTime,tags)
    # print(query)
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        free_connection(conn, cur)
    return row


def delete_news_limit() :
    query = "DELETE FROM recsys.tag_extractor_2  LIMIT  46"
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        free_connection(conn, cur)

def get_all():
    query = """SELECT * FROM recsys.tag_extractor_2"""
    conn = None
    cur = None
    row = None
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(query)
        row = cur.fetchall()
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row



if __name__ == '__main__':

#     list =["20180815110622475"]
#     row = get_last_day()
#     print(row)
#     date = row['last_date']
#     print(date)
#     row = get_new_nearly(date)
#     print(len(row),row[0].keys())
# #     row = get_all()
#     print(len(row))
    # delete_news_limit()
    # row = get_last_day()
    # print(len(row))

    row = get_news_update()

    print(len(row))


