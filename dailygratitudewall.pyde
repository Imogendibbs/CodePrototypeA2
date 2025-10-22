# create list to store entered words
user_text = []

# set current word being typed
current_word = ""

# set textbox position and size
box_x, box_y, box_w, box_h = 150, 720, 700, 50
active = False  # if the textbox has not been selected 

def setup():
    size(1000, 1000) #setting window size

# setting colour cycle for every 5 words
word_colors = [
    color(173, 151, 227),    # purple
    color(226, 151, 227),    # dark pink
    color(93, 149, 237),    # blue
    color(255, 240, 234),  # light pink
    color(255, 251, 180)   # yellow
]

font = [] # defining font variable
bg_image = None # setting background variable


def setup():
    global fonts, bg_image
    size(1000, 1000)
    
    # creating fonts for words to cycle through
    fonts = [
             loadFont ("AmericanTypewriter-20.vlw"),
             loadFont ("SnellRoundhand-20.vlw"),
             loadFont ("TimesNewRomanPSMT-20.vlw"),
             loadFont ("Baskerville-Italic-20.vlw")
]

    bg_image = loadImage("bg_image.jpg") # uploading background image

def draw():
    image(bg_image, 0, 0, width, height) # setting background as uploaded image
    
    # title properties 
    textSize(36)
    textFont(fonts[1], 36) # make font always snellroundhand
    fill(255, 252, 162)
    textAlign(CENTER, TOP)
    text("Daily Gratitude Wall", width / 2, 25)

    if active: #when the textbox has been selected (ready for user entries), textbox outline will turn pink
        stroke(245, 84, 216) 
    else:
        stroke(0)
    strokeWeight(2)
    fill(255)
    rect(box_x, box_y, box_w, box_h, 5)
    
    # show current word being typed
    fill(0)
    noStroke()
    textAlign(LEFT, CENTER)
    textFont(fonts[0])  # make textbox font always american typewritter
    textSize(20)
    text(current_word, box_x + 10, box_y + (box_h + textAscent() - textDescent()) / 2.5)
    
    for i in range(len(user_text)):
        word, pos = user_text[i]
        
        word_color = word_colors[i % len(word_colors)]  # cycle through colors
        font = fonts[i % len(fonts)] # cycle through fonts
        
        fill(word_color)
        textFont(font)
        text(word, pos[0], pos[1])

def mousePressed():
    global active
    # Activate textbox if clicked
    if box_x <= mouseX <= box_x + box_w and box_y <= mouseY <= box_y + box_h:
        active = True
    else:
        active = False

def keyPressed():
    global current_word, user_text
    if active:
        if key == BACKSPACE:
            current_word = current_word[:-1]
        elif key == ENTER or key == RETURN:
            if current_word.strip() != "":
                # finds a free, non-overlapping position
                x, y = find_free_position(current_word)
                user_text.append((current_word, (x, y)))
                current_word = ""  # Reset current word
        else:
            current_word += key
            

def find_free_position(word): 
    # finding a random x, y that is above the textbox and doesn't overlap
    max_attempts = 100 # max number of attempts to find a non-overlapping position
    for _ in range(max_attempts):
        x = random(50, width - 100)
        y = random(100, box_y - 20)  # only above the textbox

        if not check_overlap(word, x, y):
            return x, y

    return random(100, width - 100), random(50, box_y - 20)

def check_overlap(word, x, y):
    # check if (word at x,y) overlaps existing words
    word_w = textWidth(word)
    word_h = textAscent() + textDescent()

    for existing_word, (ex, ey) in user_text:
        ex_w = textWidth(existing_word)
        ex_h = textAscent() + textDescent()

        if (x < ex + ex_w and
            x + word_w > ex and
            y - word_h < ey and
            y > ey - ex_h):
            return True
    return False
