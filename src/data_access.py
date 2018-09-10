from pymysql import connect
from pymysql import cursors
import json
from setup import *

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
    """
    get news for tfidf
    :return:
    """
    query ="SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token, news.news_resource.insertDate " \
            " FROM news.news_resource " \
            " INNER JOIN recsys.news_token ON  news.news_resource.newsId = recsys.news_token.news_id" \
            " WHERE news.news_resource.insertDate >= NOW() - INTERVAL 60 DAY AND  news.news_resource.insertDate < NOW()" \
            " ORDER BY news.news_resource.insertDate " \
            " "

    print(query)
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


# def get_news_list(list) :
#     query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token, " \
#             "recsys.news_token.content_token , recsys.news_token.title_token, " \
#             "recsys.news_token.tag_token,recsys.news_token.tag_postag, " \
#             "recsys.news_token.title_postag, recsys.news_token.sapo_postag, " \
#             "recsys.news_token.content_postag, " \
#             "news.news_resource.title, news.news_resource.url " \
#             "FROM recsys.news_token " \
#             "INNER JOIN news.news_resource ON  news.news_resource.newsId = recsys.news_token.news_id " \
#             "WHERE recsys.news_token.news_id in (%s)" % ','.join(map(str, list))
#     # print(query)
#     conn = None
#     cur = None
#     row = None
#     try:
#         conn = get_connection()
#         cur = get_dict_cursor(conn)
#         cur.execute(query)
#         row = cur.fetchall()
#     except Exception as e:
#         print(e)
#     finally:
#         free_connection(conn, cur)
#     return row

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
    get news have publishDate >= last_day

    :param last_day: last date of table extract_tags
    :return: list of the news
    """

    query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
            "recsys.news_token.content_token , recsys.news_token.title_token," \
            "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
            "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
            "recsys.news_token.content_postag," \
            "news.news_resource.publishDate, news.news_resource.insertDate," \
            "news.news_resource.title, news.news_resource.url" \
            " FROM recsys.news_token ,news.news_resource " \
            " WHERE news.news_resource.newsId = recsys.news_token.news_id" \
            " AND news.news_resource.newsId in " \
            " (SELECT n.newsId FROM recsys.tag_extractor_2 t " \
            "  RIGHT JOIN news.news_resource n ON n.newsId = t.newsId " \
            "  WHERE sourceNews = 'Soha' AND t.newsId is NULL AND n.insertDate >= '2018-07-01 00:00:00' " \
            "  ORDER BY n.insertDate DESC )"

    # query = "SELECT recsys.news_token.news_id ,recsys.news_token.sapo_token," \
    #         "recsys.news_token.content_token , recsys.news_token.title_token," \
    #         "recsys.news_token.tag_token,recsys.news_token.tag_postag," \
    #         "recsys.news_token.title_postag, recsys.news_token.sapo_postag," \
    #         "recsys.news_token.content_postag," \
    #         "news.news_resource.publishDate, news.news_resource.insertDate," \
    #         "news.news_resource.title, news.news_resource.url" \
    #         " FROM recsys.news_token ,news.news_resource " \
    #         " WHERE news.news_resource.newsId = recsys.news_token.news_id" \
    #         " AND news.news_resource.insertDate >= '%s' " \
    #         " ORDER BY news.news_resource.insertDate" \
    #         " LIMIT 1000" %last_day

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
    # query = """ SELECT * FROM recsys.tag_extractor_2 t
    #             RIGHT JOIN news.news_resource n ON n.newsId = t.newsId
    #             WHERE n.sourceNews = 'Soha' AND t.publishDate >= NOW() - INTERVAL 30 DAY
    #             AND t.publishDate  < NOW() """
    query = """ SELECT nt.news_id ,nt.sapo_token, nt.content_token , nt.title_token,
                    nt.tag_token,nt.tag_postag, nt.title_postag, nt.sapo_postag,
                    nt.content_postag, n.publishDate, n.insertDate, n.title, n.url,
                    t.tags
                FROM recsys.tag_extractor_2 t 
                RIGHT JOIN news.news_resource n ON n.newsId = t.newsId
                RIGHT JOIN recsys.news_token nt ON t.newsId = nt.news_id
                WHERE n.sourceNews = 'Soha' AND t.publishDate >= NOW() - INTERVAL 30 DAY
                AND t.publishDate  < NOW()"""
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

    query = "INSERT INTO recsys.tag_extractor_2 (newsId,updateTime,publishDate,tags)" \
            " VALUES (%s, '%s','%s','%s')" %(id,updateTime,publishTime,tags)
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
        print(e,"\n")
    finally:
        free_connection(conn, cur)

def update(id,updateTime, tags) :

    query = "UPDATE recsys.tag_extractor_2 " \
            "SET tags = '%s' , updateTime = '%s' " \
            "WHERE newsId = %s" %(tags,updateTime,id)
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
        print(e,"\n")
    finally:
        free_connection(conn, cur)

# def delete_news_limit() :
#     query = "DELETE FROM recsys.tag_extractor_2 WHERE publishDate >= '2018-08-20 00:00:00' "
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

def get_all_content(id):
    query = "SELECT nt.news_id ,nt.sapo_token, nt.content_token , " \
            "nt.title_token,n.title, n.url, t.tags " \
            " FROM recsys.tag_extractor_2 t " \
            " RIGHT JOIN news.news_resource n ON n.newsId = t.newsId" \
            " RIGHT JOIN recsys.news_token nt ON t.newsId = nt.news_id " \
            " WHERE n.sourceNews = 'Soha' AND t.newsId = '%s' " %id
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


def get_tag(id):
    query = "SELECT tags FROM recsys.tag_extractor_2 WHERE newsId = %s " %id
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





