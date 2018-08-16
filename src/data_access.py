from pymysql import connect
from pymysql import cursors

import datetime
HOST = "192.168.23.191"
DB_NAME = "news"
USER_NAME = "recommender"
PASSWORD = "lga5QenoQEuksNy"



def get_connection():
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

# def get_news_update():
#     query = """SELECT * FROM news.news_resource
#                 WHERE sourceNews = 'Soha' ORDER BY publishDate DESC LIMIT 10000"""
#     conn = None
#     cur = None
#     row = None
#     try:
#         conn = get_connection()
#         cur = get_dict_cursor(conn)
#         cur.execute(query)
#         row = cur.fetchall()
#     except Exception as e:
#         print (e)
#     finally:
#         free_connection(conn, cur)
#     return row


# def get_tags_all():
#     query = "SELECT * FROM recsys.tag_extractor_2"
#     conn = None
#     cur = None
#     row = None
#     try:
#         conn = get_connection()
#         cur = get_dict_cursor(conn)
#         cur.execute(query)
#         row = cur.fetchall()
#     except Exception as e:
#         print (e)
#     finally:
#         free_connection(conn, cur)
#     return row

def get_tags_list(list) :
    query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token, recsys.news_token.content_token , recsys.news_token.title_token," \
            "       news.news_resource.title, news.news_resource.url" \
            " FROM recsys.news_token " \
            " INNER JOIN news.news_resource ON  news.news_resource.newsId = recsys.news_token.news_id" \
            " WHERE recsys.news_token.news_id in %s" %str(tuple(list))
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

def get_tags_limit_30day():
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


def insert(id ,updateTime, publishTime,tags) :

    query = "INSERT INTO recsys.tag_extractor_2 (newsId,updateTime,publishDate,tags) VALUES (%s, '%s','%s','%s')" %(id,updateTime,publishTime,tags)
    print(query)
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

# def delete_news(news_id) :
#     query = "DELETE FROM recsys.tag_extractor_2 WHERE newsId = %s" % news_id
#     conn = None
#     cur = None
#
#     try:
#         conn = get_connection()
#         cur = get_dict_cursor(conn)
#         cur.execute(query)
#         conn.commit()
#     except Exception as e:
#         print(e)
#     finally:
#         free_connection(conn, cur)
#
# def delete_news_limit() :
#     query = "DELETE FROM recsys.tag_extractor_2  LIMIT  1"
#     conn = None
#     cur = None
#
#     try:
#         conn = get_connection()
#         cur = get_dict_cursor(conn)
#         cur.execute(query)
#         conn.commit()
#     except Exception as e:
#         print(e)
#     finally:
#         free_connection(conn, cur)




if __name__ == '__main__':
    list =[201807160824365, 2018071613400603,2018071710394128,2018071809285878,2018071814084838]
    # insert(99999,"2018-08-12 13:12:14","2018-08-09 12:34:45", "tag1;tag2;tag3;tag4")
    row = get_token(20180617093030)
    print(row.keys())

    row = get_news(20180617093030)
    print(row.keys())

    # print(row['update_time'])
    # row = get_tags_limit_30day()
    row = get_tags_list(list)
    print(len(row),row)

    # row = get_tags_all()
    # print(len(row),row)
    # delete_news_limit()

    # row = get_tags_all()
    # print(len(row), row)


