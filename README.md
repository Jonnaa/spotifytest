# TEMPO- Music Streaming App

## Summary

Welcome to our Spotify Clone project! Our mission is to create a music streaming app where the music industry is more artist-centric. We are committed to paying artists their fair share and ensuring that the remaining proceeds are enough to sustain the music ecosystem.

For this demo, we are using the Spotify API to pull artists songs and information. This would eventually be replaced with our own database of songs overtime.


Here are the talented coders who contributed to this project:
TEAM NAME: The Coding Cowboys

- [Cassandra Samonte](https://github.com/Cassandra-Samonte) 
- [Jonathan Navarro](https://github.com/Jonnaa)
- [Angelica Erazo](https://github.com/amerazo)


## Technologies Used

- Django
- Python
- PostgreSQL

## Wireframe

You can view our wireframe and pitch deck [here](https://docs.google.com/presentation/d/1xWENw0HCjRm5mM1Jdd5yMoYJBEogwPoR/edit?usp=sharing&ouid=116832164001732092378&rtpof=true&sd=true).

## ERD
![ERD LAYOUT](https://i.imgur.com/k68SlSs.png)


## Trello Board

For project management and tracking progress, we use Trello. You can access our Trello board [here](https://trello.com/invite/b/GsMwIxFw/ATTIee103836c9853373da45bbe31c4500e6AFF75121/scrum-board).

## Routes Table

Here is a table of routes and their corresponding functionalities:

| Route                                      | Description                                            |
|--------------------------------------------|--------------------------------------------------------|
| `/artist/<str:artist_name>/`               | View artist information                                |
| `/seed_artists/`                           | Seed artist data                                       |
| `/player/<str:track_id>/`                  | View player for a specific track                       |
| `/callback/`                               | Callback route for some functionality                  |
| `/merch/<int:merch_id>/`                   | View details of a specific merchandise item            |
| `/merch/create/`                           | Create a new merchandise item                          |
| `/merch/<int:pk>/update/`                  | Update details of a specific merchandise item          |
| `/merch/<int:pk>/delete/`                  | Delete a specific merchandise item                     |
| `/search/`                                 | Search for artists                                     |
| `/`                                        | Login page                                             |
| `/home/`                                   | Landing page                                           |
| `/artists/`                                | Stored artists                                         |
| `/store/`                                  | View merchandise items                                 |


