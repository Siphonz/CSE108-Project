from models import db, Category, Question

# Starter questions for each category. Each category has 15 questions so a full quiz can use 15 questions.
QUESTIONS = {
    "Anime": [
        ("Which anime features the Survey Corps?", "Demon Slayer", "Attack on Titan", "Naruto", "Bleach", "B"),
        ("What is the name of Naruto's village?", "Hidden Leaf", "Hidden Sand", "Hidden Mist", "Hidden Stone", "A"),
        ("Which studio made Spirited Away?", "MAPPA", "Studio Ghibli", "Bones", "Toei", "B"),
        ("What is the name of the hero school in My Hero Academia?", "U.A. High", "Karasuno High", "Eden Academy", "Tokyo Jujutsu High", "A"),
        ("Who is the detective chasing Kira in Death Note?", "Near", "Mello", "L", "Light", "C"),
        ("Frieren: Beyond Journey's End follows a...", "Knight", "Mage", "Pirate", "Detective", "B"),
        ("Who is the main character of One Piece?", "Roronoa Zoro", "Monkey D. Luffy", "Sanji", "Portgas D. Ace", "B"),
        ("Which two brothers are the main characters in Fullmetal Alchemist?", "Edward and Alphonse Elric", "Gon and Killua", "Tanjiro and Zenitsu", "Sora and Shiro", "A"),
        ("What type of weapon do Demon Slayers commonly use?", "Nichirin blades", "Lightsabers", "Magic wands", "Laser rifles", "A"),
        ("What is Goku's home planet in Dragon Ball?", "Planet Namek", "Planet Vegeta", "Earth", "Planet Yardrat", "B"),
        ("What is the name of the child in Spy x Family?", "Anya Forger", "Yor Forger", "Fiona Frost", "Becky Blackbell", "A"),
        ("Which volleyball team does Hinata join in Haikyu!!?", "Nekoma High", "Aoba Johsai", "Karasuno High", "Shiratorizawa", "C"),
        ("What is Sailor Moon's civilian name?", "Rei Hino", "Ami Mizuno", "Usagi Tsukino", "Minako Aino", "C"),
        ("Which Pokémon is known as the Electric Mouse Pokémon?", "Eevee", "Pikachu", "Jigglypuff", "Meowth", "B"),
        ("In Jujutsu Kaisen, what is Yuji Itadori's first name?", "Megumi", "Satoru", "Yuji", "Kento", "C"),
    ],
    "Video Games": [
        ("Which company made Portal?", "Valve", "Nintendo", "Ubisoft", "EA", "A"),
        ("Who is the main hero in The Legend of Zelda?", "Zelda", "Link", "Ganon", "Epona", "B"),
        ("What material is used to build a Nether portal frame in Minecraft?", "Iron", "Diamond", "Obsidian", "Redstone", "C"),
        ("Which company makes PlayStation?", "Sony", "Microsoft", "Sega", "Nintendo", "A"),
        ("Which game is known for the quote 'The cake is a lie'?", "Portal", "Minecraft", "Undertale", "Halo", "A"),
        ("What is the name of Mario's brother?", "Luigi", "Wario", "Toad", "Yoshi", "A"),
        ("Which company created the Sonic the Hedgehog series?", "Capcom", "Sega", "Square Enix", "Konami", "B"),
        ("Which Microsoft console family began with the original Xbox?", "PlayStation", "Xbox", "GameCube", "Dreamcast", "B"),
        ("Which Minecraft enemy is known for exploding near players?", "Enderman", "Creeper", "Skeleton", "Villager", "B"),
        ("What is the name of Link's famous sword in The Legend of Zelda?", "Buster Sword", "Master Sword", "Energy Sword", "Monado", "B"),
        ("Which role tries to eliminate crewmates in Among Us?", "Engineer", "Impostor", "Scientist", "Guardian Angel", "B"),
        ("What genre is Fortnite best known for?", "Racing", "Battle royale", "Puzzle", "Fighting", "B"),
        ("What power-up usually makes Mario grow larger?", "Fire Flower", "Super Mushroom", "Super Star", "Koopa Shell", "B"),
        ("Which game series features the character Master Chief?", "Halo", "Mass Effect", "Destiny", "Gears of War", "A"),
        ("What is the main goal in Tetris?", "Collect coins", "Match three gems", "Clear complete lines", "Defeat a final boss", "C"),
    ],
    "Movies & TV": [
        ("Which movie features a young lion named Simba?", "The Lion King", "Tarzan", "Frozen", "Madagascar", "A"),
        ("What town is Stranger Things set in?", "Hawkins", "Derry", "Riverdale", "Sunnydale", "A"),
        ("Which series has Darth Vader?", "Star Trek", "Star Wars", "Harry Potter", "The Matrix", "B"),
        ("Who manages Dunder Mifflin in The Office for much of the show?", "Jim Halpert", "Dwight Schrute", "Michael Scott", "Pam Beesly", "C"),
        ("What school does Harry Potter attend?", "Hogwarts", "Durmstrang", "Beauxbatons", "Ilvermorny", "A"),
        ("Which movie is about toys that come alive?", "Cars", "Toy Story", "Inside Out", "Coco", "B"),
        ("Who directed Titanic?", "Steven Spielberg", "James Cameron", "Christopher Nolan", "Peter Jackson", "B"),
        ("What kind of creature is Shrek?", "Troll", "Ogre", "Goblin", "Giant", "B"),
        ("What is the name of the coffee shop in Friends?", "Central Perk", "Monk's Cafe", "The Max", "Luke's Diner", "A"),
        ("Who is the main character in Breaking Bad?", "Jesse Pinkman", "Walter White", "Saul Goodman", "Hank Schrader", "B"),
        ("Which movie takes place in a dinosaur theme park?", "Jumanji", "Jurassic Park", "King Kong", "The Lost World", "B"),
        ("What is the family name in Encanto?", "Madrigal", "Montoya", "Rivera", "Vasquez", "A"),
        ("Which superhero is played by Robert Downey Jr. in the Marvel movies?", "Captain America", "Iron Man", "Thor", "Hulk", "B"),
        ("Which movie features the quote 'May the Force be with you'?", "Star Wars", "The Matrix", "Avatar", "Dune", "A"),
        ("What fictional country is Black Panther from?", "Genovia", "Wakanda", "Latveria", "Narnia", "B"),
    ],
    "Music": [
        ("Who released the album Future Nostalgia?", "Dua Lipa", "Adele", "Beyonce", "Rihanna", "A"),
        ("Which band made Bohemian Rhapsody?", "Queen", "The Beatles", "Coldplay", "Nirvana", "A"),
        ("Which instrument usually has six strings?", "Guitar", "Flute", "Trumpet", "Violin", "A"),
        ("What does tempo mean in music?", "Speed", "Volume", "Mood", "Lyrics", "A"),
        ("Which music service has an annual Wrapped summary?", "Spotify", "SoundCloud", "Pandora", "Bandcamp", "A"),
        ("Who released the album 1989?", "Taylor Swift", "Olivia Rodrigo", "Billie Eilish", "Doja Cat", "A"),
        ("Which artist released the album Thriller?", "Prince", "Michael Jackson", "Elton John", "Bruno Mars", "B"),
        ("Which artist performs Blinding Lights?", "The Weeknd", "Post Malone", "Ed Sheeran", "Drake", "A"),
        ("Which singer released Rolling in the Deep?", "Adele", "Sia", "Lorde", "Halsey", "A"),
        ("How many keys does a standard modern piano usually have?", "61", "76", "88", "100", "C"),
        ("Which instrument is commonly played with a bow?", "Drums", "Violin", "Piano", "Saxophone", "B"),
        ("Which composer wrote Fur Elise?", "Mozart", "Beethoven", "Bach", "Chopin", "B"),
        ("What do dynamics describe in music?", "How loud or soft music is", "How fast music is", "The song title", "The instrument brand", "A"),
        ("Which awards are presented by the Recording Academy?", "Oscars", "Grammys", "Emmys", "Tonys", "B"),
        ("Which instrument has black and white keys?", "Piano", "Trumpet", "Violin", "Drum", "A"),
    ],
    "Internet Culture": [
        ("What does DM usually mean online?", "Direct Message", "Daily Meme", "Data Mode", "Digital Media", "A"),
        ("Which site has communities called subreddits?", "Reddit", "Pinterest", "LinkedIn", "Twitch", "A"),
        ("What does GIF stand for?", "Graphics Interchange Format", "General Image File", "Global Internet Frame", "Graphic Image Form", "A"),
        ("What is a viral image or phrase copied online called?", "A meme", "A cookie", "A server", "A browser", "A"),
        ("Which platform is famous for short vertical videos?", "TikTok", "Discord", "Wikipedia", "Twitch", "A"),
        ("What does TL;DR mean?", "Too Long; Didn't Read", "Top Link; Data Report", "Time Limit; Do Read", "Text List; Direct Route", "A"),
        ("What does URL stand for?", "Uniform Resource Locator", "Universal Reading Link", "User Response List", "Unified Route Language", "A"),
        ("What does HTML stand for?", "HyperText Markup Language", "High Tech Media Link", "Home Tool Markup Language", "Hyperlink Text Mode List", "A"),
        ("What symbol is commonly called a hashtag?", "@", "#", "&", "%", "B"),
        ("Which website is best known for user-uploaded videos?", "YouTube", "Wikipedia", "Discord", "Reddit", "A"),
        ("Which platform is especially known for live game streaming?", "Twitch", "Pinterest", "Tumblr", "LinkedIn", "A"),
        ("What is an emoji?", "A small digital image or icon", "A computer virus", "A web browser", "A type of password", "A"),
        ("What does LOL usually mean online?", "Lots of Luck", "Laughing Out Loud", "List of Links", "Level of Loading", "B"),
        ("What is a CAPTCHA mainly used for?", "Checking whether a user is human", "Making passwords longer", "Editing videos", "Sending direct messages", "A"),
        ("What does a browser do?", "Lets users view websites", "Builds computer hardware", "Creates Wi-Fi signals", "Edits music files", "A"),
    ],
}


def add_sample_data():
    # Add a category used to save Random Quiz scores. It does not hold questions itself.
    random_category = Category.query.filter_by(name="Random Mix").first()
    if not random_category:
        db.session.add(Category(name="Random Mix"))
        db.session.flush()

    # Add each category and only add questions that are not already in the database.
    # This lets existing projects receive the new starter questions without deleting users or scores.
    for category_name, question_list in QUESTIONS.items():
        category = Category.query.filter_by(name=category_name).first()

        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

        for question in question_list:
            existing_question = Question.query.filter_by(question_text=question[0], category_id=category.id).first()

            if not existing_question:
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
