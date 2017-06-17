UPDATE genre set is_movie_genre = false;
UPDATE genre set is_movie_genre = true where name in (
'Action','Comedy',
'Fantasy','Musical',
'Short','Adventure',
'Crime','Family',
'Mystery','Thriller',
'Adult','Documentary',
'Film-Noir','Romance',
'War','Animation',
'Drama','Horror',
'Sci-Fi','Western',
'Biography','Sport',
'History'
);
