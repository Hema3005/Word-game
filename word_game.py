from flask import Flask,render_template,url_for,request,jsonify,url_for,redirect
from nltk.corpus import wordnet as word_net
import json
import random
from logging.handlers import RotatingFileHandler

#flask object
app = Flask(__name__,template_folder="template",static_folder="static")

file_handler=RotatingFileHandler("error.log",maxBytes= 1024 * 1024 *100)
app.logger.addHandler(file_handler)

#create list 
random_list=[]
jumble_list=[]
user_list=[]
temp=[]
score=0

# to get meaning of correct words 
def meaning(temp):
    meaning=[]
    for word in temp:
        syn = word_net.synsets(word)[0]
        mean=syn.definition()
        meaning.append("Meaning of Correct word :"+mean)
    return meaning

def jumble(word):

# create a jumbled version of the word
    jumble =""
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
    
    return jumble

#to get 4 letters of words from reading the file
def read_file():
    # Opening JSON file that has 4 letter english words
    with open('./word_dic.json', 'r') as openfile:
    # Reading from json file 
        json_object = json.load(openfile)
        return json_object
   

def get_random_word(word_list):
   
# pick one word randomly from the sequence
    word = random.choice(word_list)
    random_list.append("Correct Word: "+word)
   
# append a list to use later to see if the guess is correct
     temp.append(word)
    return word

#starting page
@app.route('/')
def menu():
	return render_template("word.html")

#put jumble word into page
@app.route('/start')
def start():

    word_list=read_file()
    word=get_random_word(word_list)
    
    word_jumble=jumble(word)
    jumble_list.append("Jumble Word:"+word_jumble)
    print(word,word_jumble)
    return render_template("word1.html",jumble=word_jumble)

# used to check the user answer and increase  the score if user guess is correct
@app.route("/api/get_entity", methods=['GET'])
def get_entity():
    user_guess=request.args.get("user")
    word_list=read_file()
    global score
    if user_guess in word_list:
        user_list.append('correct :Your answer:'+user_guess)
        score+=10
        return jsonify(user_guess)
    else:
        user_list.append('wrong :Your answer:'+user_guess)
        return jsonify(" False" )


@app.route('/background_process_test')
def background_process_test():
    word_list=read_file()
    word=get_random_word(word_list)

    word_jumble=jumble(word)
    jumble_list.append("Jumble Word:"+word_jumble)
    print(word,word_jumble)
    return jsonify(word_jumble)

#return score board 
@app.route("/app")
def result():
    global score
    score=score
    j=jumble_list
    r=random_list
    u=user_list
    m=meaning(temp)
    print("Jumble word:",j)
    print("Correct word:",r)
    print("your answer:",u)
    print("Meaning of word:",m)
    z=list(zip(j,r,u,m))
    list_ans=[]
    for i in z:
        list_ans.append(list(i))
    
    return render_template("result.html",score=score,list=list_ans )



@app.errorhandler(500)
def handle_500_error(exception):
    app.logger.error(exception)
    return "Internal Server Error"

@app.errorhandler(404)
def handle_404_error(exception):
    app.logger.error(exception)
    return "Not Found"


if __name__ == '__main__':
	app.run(port=5003)
    


    