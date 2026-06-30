from models import db, Category, Question

# Exactly 5 questions per difficulty in each category.
QUESTIONS = {
    "Anime": {
        "easy": [
            ("Which anime features the Survey Corps?", "Demon Slayer", "Attack on Titan", "Naruto", "Bleach", "B"),
            ("What is the name of Naruto's village?", "Hidden Leaf", "Hidden Sand", "Hidden Mist", "Hidden Stone", "A"),
            ("Which studio made Spirited Away?", "MAPPA", "Studio Ghibli", "Bones", "Toei", "B"),
            ("What is the hero school in My Hero Academia?", "U.A. High", "Karasuno High", "Eden Academy", "Tokyo Jujutsu High", "A"),
            ("Who is the detective chasing Kira in Death Note?", "Near", "Mello", "L", "Light", "C"),
        ],
        "medium": [
            ("In Demon Slayer, what is Nezuko's relation to Tanjiro?", "Friend", "Sister", "Cousin", "Rival", "B"),
            ("Which titan is inherited by Eren early in Attack on Titan?", "Female Titan", "Beast Titan", "Attack Titan", "Cart Titan", "C"),
            ("What is the name of Luffy's pirate crew in One Piece?", "Blackbeard Pirates", "Straw Hat Pirates", "Red Hair Pirates", "Heart Pirates", "B"),
            ("In Jujutsu Kaisen, what is Gojo's signature eye technique called?", "Sharingan", "Byakugan", "Six Eyes", "Rinnegan", "C"),
            ("Which anime follows an elf mage after the demon king is defeated?", "Vinland Saga", "Frieren", "86", "Mob Psycho 100", "B"),
        ],
        "hard": [
            ("What is the name of the world in Made in Abyss' giant pit?", "The Crater", "The Abyss", "The Chasm", "The Rift", "B"),
            ("In Fullmetal Alchemist, what is Edward's younger brother's name?", "Roy", "Alphonse", "Hughes", "Greed", "B"),
            ("Which shogi player is the protagonist of March Comes in like a Lion?", "Rei Kiriyama", "Shoya Ishida", "Kousei Arima", "Taichi Mashima", "A"),
            ("What organization employs hunters in Hunter x Hunter?", "Adventurer Guild", "Hunter Association", "Phantom Brigade", "Zoldyck Council", "B"),
            ("In Steins;Gate, what nickname does Rintaro Okabe use?", "Zero", "El Psy Kongroo", "Hououin Kyouma", "D-Mail King", "C"),
        ],
    },
    "Video Games": {
        "easy": [
            ("Which company made Portal?", "Valve", "Nintendo", "Ubisoft", "EA", "A"),
            ("Who is the main hero in The Legend of Zelda?", "Zelda", "Link", "Ganon", "Epona", "B"),
            ("What material builds a Nether portal frame in Minecraft?", "Iron", "Diamond", "Obsidian", "Redstone", "C"),
            ("Which company makes PlayStation?", "Sony", "Microsoft", "Sega", "Nintendo", "A"),
            ("What is the name of Mario's brother?", "Luigi", "Wario", "Toad", "Yoshi", "A"),
        ],
        "medium": [
            ("Which game is known for the quote 'The cake is a lie'?", "Portal", "Minecraft", "Undertale", "Halo", "A"),
            ("In Overwatch, what role is Mercy known for?", "Tank", "Support", "DPS", "Sniper", "B"),
            ("Which region is featured in Pokemon Scarlet and Violet?", "Kanto", "Sinnoh", "Paldea", "Galar", "C"),
            ("What is Kratos' son called in God of War (2018)?", "Baldur", "Atreus", "Freyr", "Thor", "B"),
            ("Which battle royale game features building structures mid-fight?", "PUBG", "Apex Legends", "Fortnite", "Warzone", "C"),
        ],
        "hard": [
            ("What is the default city in Cyberpunk 2077?", "Los Santos", "Night City", "Rapture", "Midgar", "B"),
            ("In Hollow Knight, what is the name of the setting?", "Hallownest", "Lordran", "Yharnam", "Hyrule", "A"),
            ("Which FromSoftware game introduced the Lands Between?", "Sekiro", "Bloodborne", "Elden Ring", "Dark Souls III", "C"),
            ("What is the subtitle of The Witcher 3?", "Wild Hunt", "Blood Oath", "Dragonborn", "Northern Wars", "A"),
            ("In Stardew Valley, who is the town mayor?", "Lewis", "Pierre", "Marnie", "Clint", "A"),
        ],
    },
    "Movies & TV": {
        "easy": [
            ("Which movie features a young lion named Simba?", "The Lion King", "Tarzan", "Frozen", "Madagascar", "A"),
            ("What town is Stranger Things set in?", "Hawkins", "Derry", "Riverdale", "Sunnydale", "A"),
            ("Which series has Darth Vader?", "Star Trek", "Star Wars", "Harry Potter", "The Matrix", "B"),
            ("Who manages Dunder Mifflin for much of The Office?", "Jim Halpert", "Dwight Schrute", "Michael Scott", "Pam Beesly", "C"),
            ("What school does Harry Potter attend?", "Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny", "A"),
        ],
        "medium": [
            ("Which movie is about toys that come alive?", "Cars", "Toy Story", "Inside Out", "Coco", "B"),
            ("Who plays Iron Man in the MCU?", "Chris Evans", "Chris Hemsworth", "Robert Downey Jr.", "Mark Ruffalo", "C"),
            ("What is the name of Wednesday's school in Wednesday?", "Nevermore", "Riverdale High", "Beacon Hills", "Liberty High", "A"),
            ("Which sitcom features Sheldon Cooper?", "Friends", "The Big Bang Theory", "Brooklyn Nine-Nine", "Parks and Recreation", "B"),
            ("In Avatar: The Last Airbender, who teaches Aang earthbending?", "Katara", "Toph", "Zuko", "Sokka", "B"),
        ],
        "hard": [
            ("What is the fictional metal in Black Panther's Wakanda?", "Adamantium", "Unobtanium", "Vibranium", "Kryptonite", "C"),
            ("Who directed Inception?", "Denis Villeneuve", "Christopher Nolan", "David Fincher", "Ridley Scott", "B"),
            ("Which character says 'I am the one who knocks' in Breaking Bad?", "Jesse", "Hank", "Saul", "Walter White", "D"),
            ("What is the name of the paper company in The Office?", "PaperCo", "Dunder Mifflin", "Staples", "Vance Refrigeration", "B"),
            ("In The Mandalorian, what species is Grogu?", "Yoda's species", "Ewok", "Wookiee", "Kaminoan", "A"),
        ],
    },
    "Music": {
        "easy": [
            ("Who released the album Future Nostalgia?", "Dua Lipa", "Adele", "Beyonce", "Rihanna", "A"),
            ("Which band made Bohemian Rhapsody?", "Queen", "The Beatles", "Coldplay", "Nirvana", "A"),
            ("Which instrument usually has six strings?", "Guitar", "Flute", "Trumpet", "Violin", "A"),
            ("What does tempo mean in music?", "Speed", "Volume", "Mood", "Lyrics", "A"),
            ("Which music service has an annual Wrapped summary?", "Spotify", "SoundCloud", "Pandora", "Bandcamp", "A"),
        ],
        "medium": [
            ("Who released the album 1989?", "Taylor Swift", "Olivia Rodrigo", "Billie Eilish", "Doja Cat", "A"),
            ("Which clef is commonly used for higher-pitched instruments?", "Bass clef", "Treble clef", "Alto clef", "Tenor clef", "B"),
            ("What does BPM stand for in music production?", "Beats Per Minute", "Bars Per Measure", "Bass Per Mix", "Beats Per Melody", "A"),
            ("Which artist is known as the 'King of Pop'?", "Prince", "Elvis Presley", "Michael Jackson", "Bruno Mars", "C"),
            ("Which genre did Nirvana help popularize in the 1990s?", "Disco", "Grunge", "Ska", "Country", "B"),
        ],
        "hard": [
            ("How many semitones are in a perfect fifth interval?", "5", "6", "7", "8", "C"),
            ("Which composer wrote The Four Seasons?", "Bach", "Mozart", "Vivaldi", "Beethoven", "C"),
            ("In common time, how many beats are in a measure?", "2", "3", "4", "6", "C"),
            ("What is the relative minor key of C major?", "E minor", "A minor", "D minor", "G minor", "B"),
            ("Which DAW was created by Ableton?", "FL Studio", "Logic Pro", "Pro Tools", "Ableton Live", "D"),
        ],
    },
    "Internet Culture": {
        "easy": [
            ("What does DM usually mean online?", "Direct Message", "Daily Meme", "Data Mode", "Digital Media", "A"),
            ("Which site has communities called subreddits?", "Reddit", "Pinterest", "LinkedIn", "Twitch", "A"),
            ("What does GIF stand for?", "Graphics Interchange Format", "General Image File", "Global Internet Frame", "Graphic Image Form", "A"),
            ("What is a viral image or phrase copied online called?", "A meme", "A cookie", "A server", "A browser", "A"),
            ("Which platform is famous for short vertical videos?", "TikTok", "Discord", "Wikipedia", "Twitch", "A"),
        ],
        "medium": [
            ("What does TL;DR mean?", "Too Long; Didn't Read", "Top Link; Data Report", "Time Limit; Do Read", "Text List; Direct Route", "A"),
            ("What does 'OP' usually mean in forum threads?", "Only Post", "Original Poster", "Open Platform", "Online Profile", "B"),
            ("Which app is best known for servers and voice channels?", "Discord", "Tumblr", "Pinterest", "Patreon", "A"),
            ("What does 'ratioed' often mean on social media?", "A post has many downloads", "A reply outperformed the original post", "A profile is private", "A post was deleted", "B"),
            ("What does 'IRL' stand for?", "In Random Logs", "Internet Relay Link", "In Real Life", "Image Render Layer", "C"),
        ],
        "hard": [
            ("Which protocol secures most website traffic?", "FTP", "SMTP", "HTTPS", "Telnet", "C"),
            ("What does CDN stand for?", "Central Data Node", "Content Delivery Network", "Code Distribution Net", "Cloud Download Namespace", "B"),
            ("In web addresses, what does TLD mean?", "Top-Level Domain", "Text Link Data", "Transfer Layer Directory", "Total Link Depth", "A"),
            ("What does '404' usually indicate on the web?", "Server overloaded", "Permission denied", "Page not found", "Invalid password", "C"),
            ("Which tag starts a hashtag trend discussion on social platforms?", "@", "#", "&", "$", "B"),
        ],
    },
}


def add_sample_data():
    for category_name, difficulty_map in QUESTIONS.items():
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

        for difficulty, question_list in difficulty_map.items():
            for question in question_list:
                existing_question = Question.query.filter_by(
                    category_id=category.id,
                    difficulty=difficulty,
                    question_text=question[0],
                ).first()

                if existing_question:
                    continue

                db.session.add(
                    Question(
                        category_id=category.id,
                        difficulty=difficulty,
                        question_text=question[0],
                        option_a=question[1],
                        option_b=question[2],
                        option_c=question[3],
                        option_d=question[4],
                        correct_answer=question[5],
                    )
                )

    db.session.commit()
