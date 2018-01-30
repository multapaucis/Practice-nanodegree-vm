#!/usr/bin/env python3

from catalogdb import popular_articles, popular_authors, error_days


print("The three most popular articles of all time are: ")
arts = popular_articles()
for title, views in arts:
    print(' -"{}" - {} views'.format(title, views))

print("\nThe most popular article authors of all time are: ")
auts = popular_authors()
for author, views in auts:
    print(' -"{}" - {} views'.format(author, views))


print("\nMore than 1" + "%" + " of requests lead to errors on: ")
errors = error_days()
for err_date, err_pct in errors:
    print(" -{:%B %d, %Y} - {:.1f}% errors".format(err_date, err_pct))
