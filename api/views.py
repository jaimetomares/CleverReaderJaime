import spacy
import pytextrank
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline

text = "Deep learning (also known as deep structured learning) is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep-learning architectures such as deep neural networks, deep belief networks, deep reinforcement learning, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs, where they have produced results comparable to and in some cases surpassing human expert performance. Artificial neural networks (ANNs) were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analogue. The adjective deep in deep learning refers to the use of multiple layers in the network. Early work showed that a linear perceptron cannot be a universal classifier, but that a network with a nonpolynomial activation function with one hidden layer of unbounded width can. Deep learning is a modern variation which is concerned with an unbounded number of layers of bounded size, which permits practical application and optimized implementation, while retaining theoretical universality under mild conditions. In deep learning the layers are also permitted to be heterogeneous and to deviate widely from biologically informed connectionist models, for the sake of efficiency, trainability and understandability, whence the structured part."
text2 = "Following the summer break, teams begin training camps in late September. Training camps allow the coaching staff to evaluate players (especially rookies), scout the team's strengths and weaknesses, prepare the players for the rigorous regular season and determine the 12-man active roster (and a 3-man inactive list) with which they will begin the regular season. Teams have the ability to assign players with less than two years of experience to the NBA G League. After training camp, a series of preseason exhibition games are held. Preseason matches are sometimes held in non-NBA cities, both in the United States and overseas. The NBA regular season begins in the last week of October. During the regular season, each team plays 82 games, 41 each home and away. A team faces opponents in its own division four times a year (16 games). Each team plays six of the teams from the other two divisions in its conference four times (24 games), and the remaining four teams three times (12 games). Finally, each team plays all the teams in the other conference twice apiece (30 games). This asymmetrical structure means the strength of schedule will vary between teams (but not as significantly as the NFL or MLB). Over five seasons, each team will have played 80 games against their division (20 games against each opponent, 10 at home, 10 on the road), 180 games against the rest of their conference (18 games against each opponent, 9 at home, 9 on the road), and 150 games against the other conference (10 games against each team, 5 at home, 5 on the road). The NBA is also the only league that regularly schedules games on Christmas Day.[92] The league has been playing games regularly on the holiday since 1947,[93] though the first Christmas Day games were not televised until 1983–84.[94] Games played on this day have featured some of the best teams and players.[92][93][94] Christmas is also notable for NBA on television, as the holiday is when the first NBA games air on network television each season.[93][94] Games played on this day have been some of the highest-rated games during a particular season. In February, the regular season pauses to celebrate the annual NBA All-Star Game. Fans vote throughout the United States, Canada, and on the Internet, and the top vote-getters in each conference are named captains. Fan votes determine the rest of the allstar starters. Coaches vote to choose the remaining 14 All-Stars. Then, the top vote-getters in each conference draft their own team from a player pool of allstars. The top vote-getter in the league earns first pick and so forth. The player with the best performance during the game is rewarded with a Game MVP award. Other attractions of the All-Star break include the Rising Stars Challenge (originally Rookie Challenge), where the top rookies and second-year players in the NBA play in a 5-on-5 basketball game, with the current format pitting U.S. players against those from the rest of the world; the Skills Challenge, where players compete to finish an obstacle course consisting of shooting, passing, and dribbling in the fastest time; the Three Point Contest, where players compete to score the highest number of three-point field goals in a given time; and the NBA Slam Dunk Contest, where players compete to dunk the ball in the most entertaining way according to the judges. These other attractions have varying names which include the names of the various sponsors who have paid for naming rights. Shortly after the All-Star break is the trade deadline, which is set to fall on the 16th Thursday of the season (usually in February) at 3 pm Eastern Time.[95] After this date, teams are not allowed to exchange players with each other for the remainder of the season, although they may still sign and release players. Major trades are often completed right before the trading deadline, making that day a hectic time for general managers. Around the middle of April, the regular season ends. It is during this time that voting begins for individual awards, as well as the selection of the honorary, league-wide, post-season teams. The Sixth Man of the Year Award is given to the best player coming off the bench (must have more games coming off the bench than actual games started). The Rookie of the Year Award is awarded to the most outstanding first-year player. The Most Improved Player Award is awarded to the player who is deemed to have shown the most improvement from the previous season. The Defensive Player of the Year Award is awarded to the league's best defender. The Coach of the Year Award is awarded to the coach that has made the most positive difference to a team. The Most Valuable Player Award is given to the player deemed the most valuable for (his team) that season. Additionally, Sporting News awards an unofficial (but widely recognized) Executive of the Year Award to the general manager who is adjudged to have performed the best job for the benefit of his franchise. The post-season teams are the All-NBA Team, the All-Defensive Team, and the All-Rookie Team; each consists of five players. There are three All-NBA teams, consisting of the top players at each position, with first-team status being the most desirable. There are two All-Defensive teams, consisting of the top defenders at each position. There are also two All-Rookie teams, consisting of the top first-year players regardless of position."

        #1st way to do it would be using textrank and spacy
        #--------------------------------------------------
"""
nlp= spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
doc = nlp(text)


for line in doc._.textrank.summary(limit_sentences=5):
    print(line)
"""

        #2nd way to do it would be using pegasus tokenizer
        #-------------------------------------------------

model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
tokens = pegasus_tokenizer(text, truncation=True, padding="longest", return_tensors="pt")

encoded_summary = pegasus_model.generate(**tokens)
decoded_summary = pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)


        #3rd way is simmilar, but uses pipeline, preferable way
        #-------------------------------------------------

summarizer = pipeline("summarization", model=model_name, tokenizer=pegasus_tokenizer, framework="pt")

summary = summarizer(text, min_length=60)

print(decoded_summary)




        #OR.........
"""
try:
    summary = summarizer(summarizer, text, max_length=max_len, min_length=10, do_sample=False)
    return summary
except IndexError as ex:
    return summarize_text(summarizer, text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

"""