import psycopg2


def popular_articles():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''SELECT title, count(log.id) AS num
        FROM log, articles
        WHERE log.path = CONCAT('/article/', articles.slug)
        GROUP BY title ORDER BY num DESC
        LIMIT 3;''')
    results = c.fetchall()
    db.close()
    return results


def popular_authors():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''SELECT name, count(log.id) AS num
        FROM authors, log, articles
        WHERE log.path = CONCAT('/article/', articles.slug)
        AND authors.id = articles.author
        GROUP BY name ORDER BY num DESC;''')
    results = c.fetchall()
    db.close()
    return results


def error_days():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute('''CREATE OR REPLACE VIEW error_percents AS
        SELECT CAST(time AS date) as day,
        (100.0 * (CAST(SUM(CASE WHEN status LIKE '404%' THEN 1 ELSE 0 END)
        AS real) / COUNT(status))) as percent
        FROM log
        GROUP BY day;
        ''')
    c.execute('''
        SELECT day, percent
        FROM error_percents
        where percent >=1;
        ''')
    results = c.fetchall()
    db.close()
    return results
