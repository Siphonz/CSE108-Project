from models import db, Category, Question

#Sample generated questions
QUESTIONS = {
    "Anime": [
        ("Which anime features the Survey Corps?", "Demon Slayer", "Attack on Titan", "Naruto", "Bleach", "B"),
        ("What is the name of Naruto's village?", "Hidden Leaf", "Hidden Sand", "Hidden Mist", "Hidden Stone", "A"),
        ("Which studio made Spirited Away?", "MAPPA", "Studio Ghibli", "Bones", "Toei", "B"),
        ("What is the name of the hero school in My Hero Academia?", "U.A. High", "Karasuno High", "Eden Academy", "Tokyo Jujutsu High", "A"),
        ("Who is the detective chasing Kira in Death Note?", "Near", "Mello", "L", "Light", "C"),
        ("Frieren: Beyond Journey's End follows a...", "Knight", "Mage", "Pirate", "Detective", "B"),
    ],
    "Video Games": [
        ("Which company made Portal?", "Valve", "Nintendo", "Ubisoft", "EA", "A"),
        ("Who is the main hero in The Legend of Zelda?", "Zelda", "Link", "Ganon", "Epona", "B"),
        ("What material is used to build a Nether portal frame in Minecraft?", "Iron", "Diamond", "Obsidian", "Redstone", "C"),
        ("Which company makes PlayStation?", "Sony", "Microsoft", "Sega", "Nintendo", "A"),
        ("Which game is known for the quote 'The cake is a lie'?", "Portal", "Minecraft", "Undertale", "Halo", "A"),
        ("What is the name of Mario's brother?", "Luigi", "Wario", "Toad", "Yoshi", "A"),
    ],
    "Movies & TV": [
        ("Which movie features a young lion named Simba?", "The Lion King", "Tarzan", "Frozen", "Madagascar", "A"),
        ("What town is Stranger Things set in?", "Hawkins", "Derry", "Riverdale", "Sunnydale", "A"),
        ("Which series has Darth Vader?", "Star Trek", "Star Wars", "Harry Potter", "The Matrix", "B"),
        ("Who manages Dunder Mifflin in The Office for much of the show?", "Jim Halpert", "Dwight Schrute", "Michael Scott", "Pam Beesly", "C"),
        ("What school does Harry Potter attend?", "Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny", "A"),
        ("Which movie is about toys that come alive?", "Cars", "Toy Story", "Inside Out", "Coco", "B"),
    ],
    "Music": [
        ("Who released the album Future Nostalgia?", "Dua Lipa", "Adele", "Beyonce", "Rihanna", "A"),
        ("Which band made Bohemian Rhapsody?", "Queen", "The Beatles", "Coldplay", "Nirvana", "A"),
        ("Which instrument usually has six strings?", "Guitar", "Flute", "Trumpet", "Violin", "A"),
        ("What does tempo mean in music?", "Speed", "Volume", "Mood", "Lyrics", "A"),
        ("Which music service has an annual Wrapped summary?", "Spotify", "SoundCloud", "Pandora", "Bandcamp", "A"),
        ("Who released the album 1989?", "Taylor Swift", "Olivia Rodrigo", "Billie Eilish", "Doja Cat", "A"),
    ],
    "Internet Culture": [
        ("What does DM usually mean online?", "Direct Message", "Daily Meme", "Data Mode", "Digital Media", "A"),
        ("Which site has communities called subreddits?", "Reddit", "Pinterest", "LinkedIn", "Twitch", "A"),
        ("What does GIF stand for?", "Graphics Interchange Format", "General Image File", "Global Internet Frame", "Graphic Image Form", "A"),
        ("What is a viral image or phrase copied online called?", "A meme", "A cookie", "A server", "A browser", "A"),
        ("Which platform is famous for short vertical videos?", "TikTok", "Discord", "Wikipedia", "Twitch", "A"),
        ("What does TL;DR mean?", "Too Long; Didn't Read", "Top Link; Data Report", "Time Limit; Do Read", "Text List; Direct Route", "A"),
    ],
}


def add_sample_data():
    # Do not add duplicates if the app is started again.
    if Category.query.first():
        return

    for category_name, question_list in QUESTIONS.items():
        category = Category(name=category_name)
        db.session.add(category)
        db.session.flush()  # Gives category an id before questions are added.

        for question in question_list:
            db.session.add(
                Question(
                    category_id=category.id,
                    question_text=question[0],
                    option_a=question[1],
                    option_b=question[2],
                    option_c=question[3],
                    option_d=question[4],
                    correct_answer=question[5],
                )
            )

    db.session.commit()
