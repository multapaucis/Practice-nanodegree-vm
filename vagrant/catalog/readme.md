This is a Flask/SQLalchemy website written in Python 2. It creates a database and is able to hold information on Users, Genres, and Books.

To insure the website runs correctly it is recommended to run within Virtual Box with Vagrant Installed

Instructions:

1. In order to launch the website you first have to launch the virtual machine
        a. Using Terminal on Mac or Git Bash on windows, go to the the Vagrant Directory
        b. Use the Command "vagrant up" to launch the virtual machine
        c. The command "vagrant ssh" puts you into the system
        d. Then enter "cd /vagrant/catalog" to find the correct directory
2. Then launch the application by using the terminal command
        a. When in the directory use "python application.py" to launch the website
3. Visit the websit by going to http://localhost:8000 in your preffered browser
4. To view JSONs of the Database you can go to
        a. http://localhost:8000/library/JSON
            For a JSON of all Genres
        b. http://localhost:8000/genre/<int:genre_id>/JSON
            For the JSON of the genre with whichever genre_id you specify
        c. http://localhost:8000/book/<int:book_id>/JSON
            For the JSON of the book with whichever book_id you specify

