from pymysql import connect
from pymysql import cursors

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
    query = "SELECT *  FROM recsys.news_token WHERE news_id = %s" % news_id
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
    except Exception as e:
        print (e)
    finally:
        free_connection(conn, cur)
    return row

if __name__ == '__main__':
    # id = ""
    # row = get_news(20180704113527485)

    row = get_token(20180704113527485)
    print(row.keys())
    # print(get_news()["newsId"])


