from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.conf import settings
import PyPDF2
import re



import spacy
import pytextrank
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import pipeline

from heapq import nlargest

def consume_file(request):
    if request.method == 'POST':

        file = request.FILES['file']

        extension = file.name.split(".")
        extension[1] != "pdf"
        extension = ["sample", "pdf"]
        if(extension[1] != "pdf"):
            return HttpResponseBadRequest

        doc = PyPDF2.PdfFileReader(file)
        pages = doc.getNumPages()
        text = ""
        
        # Extract text from PDF file
        # Get each page and extract text
        for i in range(pages):
            curr_page = doc.getPage(i)
            curr_text = curr_page.extractText()
            text += curr_text

#text = """There are broadly two types of extractive summarization tasks depending on what the summarization program focuses on. The first is generic summarization, which focuses on obtaining a generic summary or abstract of the collection (whether documents, or sets of images, or videos, news stories etc.). The second is query relevant summarization, sometimes called query-based summarization, which summarizes objects specific to a query. Summarization systems are able to create both query relevant text summaries and generic machine-generated summaries depending on what the user needs. An example of a summarization problem is document summarization, which attempts to automatically produce an abstract from a given document. Sometimes one might be interested in generating a summary from a single source document, while others can use multiple source documents (for example, a cluster of articles on the same topic). This problem is called multi-document summarization. A related application is summarizing news articles. Imagine a system, which automatically pulls together news articles on a given topic (from the web), and concisely represents the latest news as a summary. Image collection summarization is another application example of automatic summarization. It consists in selecting a representative set of images from a larger set of images.[3] A summary in this context is useful to show the most representative images of results in an image collection exploration system. Video summarization is a related domain, where the system automatically creates a trailer of a long video. This also has applications in consumer or personal videos, where one might want to skip the boring or repetitive actions. Similarly, in surveillance videos, one would want to extract important and suspicious activity, while ignoring all the boring and redundant frames captured."""
#text2 = "Following the summer break, teams begin training camps in late September. Training camps allow the coaching staff to evaluate players (especially rookies), scout the team's strengths and weaknesses, prepare the players for the rigorous regular season and determine the 12-man active roster (and a 3-man inactive list) with which they will begin the regular season. Teams have the ability to assign players with less than two years of experience to the NBA G League. After training camp, a series of preseason exhibition games are held. Preseason matches are sometimes held in non-NBA cities, both in the United States and overseas. The NBA regular season begins in the last week of October. During the regular season, each team plays 82 games, 41 each home and away. A team faces opponents in its own division four times a year (16 games). Each team plays six of the teams from the other two divisions in its conference four times (24 games), and the remaining four teams three times (12 games). Finally, each team plays all the teams in the other conference twice apiece (30 games). This asymmetrical structure means the strength of schedule will vary between teams (but not as significantly as the NFL or MLB). Over five seasons, each team will have played 80 games against their division (20 games against each opponent, 10 at home, 10 on the road), 180 games against the rest of their conference (18 games against each opponent, 9 at home, 9 on the road), and 150 games against the other conference (10 games against each team, 5 at home, 5 on the road). The NBA is also the only league that regularly schedules games on Christmas Day.[92] The league has been playing games regularly on the holiday since 1947,[93] though the first Christmas Day games were not televised until 1983–84.[94] Games played on this day have featured some of the best teams and players.[92][93][94] Christmas is also notable for NBA on television, as the holiday is when the first NBA games air on network television each season.[93][94] Games played on this day have been some of the highest-rated games during a particular season. In February, the regular season pauses to celebrate the annual NBA All-Star Game. Fans vote throughout the United States, Canada, and on the Internet, and the top vote-getters in each conference are named captains. Fan votes determine the rest of the allstar starters. Coaches vote to choose the remaining 14 All-Stars. Then, the top vote-getters in each conference draft their own team from a player pool of allstars. The top vote-getter in the league earns first pick and so forth. The player with the best performance during the game is rewarded with a Game MVP award. Other attractions of the All-Star break include the Rising Stars Challenge (originally Rookie Challenge), where the top rookies and second-year players in the NBA play in a 5-on-5 basketball game, with the current format pitting U.S. players against those from the rest of the world; the Skills Challenge, where players compete to finish an obstacle course consisting of shooting, passing, and dribbling in the fastest time; the Three Point Contest, where players compete to score the highest number of three-point field goals in a given time; and the NBA Slam Dunk Contest, where players compete to dunk the ball in the most entertaining way according to the judges. These other attractions have varying names which include the names of the various sponsors who have paid for naming rights. Shortly after the All-Star break is the trade deadline, which is set to fall on the 16th Thursday of the season (usually in February) at 3 pm Eastern Time.[95] After this date, teams are not allowed to exchange players with each other for the remainder of the season, although they may still sign and release players. Major trades are often completed right before the trading deadline, making that day a hectic time for general managers. Around the middle of April, the regular season ends. It is during this time that voting begins for individual awards, as well as the selection of the honorary, league-wide, post-season teams. The Sixth Man of the Year Award is given to the best player coming off the bench (must have more games coming off the bench than actual games started). The Rookie of the Year Award is awarded to the most outstanding first-year player. The Most Improved Player Award is awarded to the player who is deemed to have shown the most improvement from the previous season. The Defensive Player of the Year Award is awarded to the league's best defender. The Coach of the Year Award is awarded to the coach that has made the most positive difference to a team. The Most Valuable Player Award is given to the player deemed the most valuable for (his team) that season. Additionally, Sporting News awards an unofficial (but widely recognized) Executive of the Year Award to the general manager who is adjudged to have performed the best job for the benefit of his franchise. The post-season teams are the All-NBA Team, the All-Defensive Team, and the All-Rookie Team; each consists of five players. There are three All-NBA teams, consisting of the top players at each position, with first-team status being the most desirable. There are two All-Defensive teams, consisting of the top defenders at each position. There are also two All-Rookie teams, consisting of the top first-year players regardless of position."
        
        #Here we will create a list of stopwords.
        stopwords = list(STOP_WORDS)

        #This will return a language object nlp containing all components and data needed to process text.
        nlp = spacy.load('en_core_web_sm')

        #Calling the nlp object on a string of text will return a processed Doc. During processing, spaCy first tokenizes the text, i.e. segments it into words, punctuation and so on.
        doc = nlp(text)

        #list of tokens
        tokens = [token.text for token in doc]
#print(tokens)

        #punctuation contains a string of all the punctuations
        punctuation = ""
        punctuation = punctuation + '\n'
#print(punctuation)

        #number of occurrences of all the distinct words in the text which are not punctuations or stop words


        word_frequencies = {}
        for word in doc:
                if word.text.lower() not in stopwords:
                        if word.text.lower() not in punctuation:
                                if word.text not in word_frequencies.keys():
                                        word_frequencies[word.text] = 1
                                else:
                                        word_frequencies[word.text] += 1
                
#print(word_frequencies)


        max_frequency = max(word_frequencies.values())
#print(max_frequency)

        #divide each frequency value in word_frequencies with the max_frequency to normalize the frequencies.
        for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word]/max_frequency

#print(word_frequencies)

        #sentence tokenization. The entire text is divided into sentences.
        sentence_tokens = [sent for sent in doc.sents]
#print(sentence_tokens)

        # The sentence score for a particular sentence is the sum of the normalized frequencies of the words in that sentence. All the sentences will be 
        # stored with their score in the dictionary sentence_scores.
        sentence_scores = {}
        for sent in sentence_tokens:
                for word in sent:
                        if word.text.lower() in word_frequencies.keys():
                                if sent not in sentence_scores.keys():
                                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                                else:
                                        sentence_scores[sent] += word_frequencies[word.text.lower()]
                
#print(sentence_scores)

        #We want the length of summary to be 15% of the original length
        select_length = int(len(sentence_tokens)*0.15)
#print(sentence_scores)

        summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
#print(summary)

        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)

        patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' 

        urls = re.findall(patron, text)

        for u in urls:
                print(u)




        print(text)

        print(summary)

        print(len(text))

        print(len(summary))

        return HttpResponse(summary)


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
""""
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

"""


        #OR.........
"""
try:
    summary = summarizer(summarizer, text, max_length=max_len, min_length=10, do_sample=False)
    return summary
except IndexError as ex:
    return summarize_text(summarizer, text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

"""