import chromadb

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

#embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, chunk_overlap = 50)

db = chromadb.PersistentClient(path="./my_chroma_db")

collection =  db.get_or_create_collection(name="demo")

chunks = text_splitter.split_text(
     """
Association football, more commonly known as football or soccer,[a] is a team sport played between two teams of 11 players who almost exclusively use their feet to propel a ball around a rectangular field called a pitch.

The objective of the game is to score more goals than the opposing team by moving the ball beyond the goal line into a rectangular-framed goal defended by the opponent. Traditionally, the game has been played over two 45-minute halves, for a total match time of 90 minutes. With an estimated 250 million players active in over 200 countries and territories, it is the world's most popular sport.

Association football is played in accordance with the Laws of the Game, a set of rules that has been in effect since 1863 and maintained by the IFAB since 1886. The game is played with a football that is 68–70 cm (27–28 in) in circumference. The two teams compete to score goals by getting the ball into the other team's goal (between the posts, under the bar, and fully across the goal line). When the ball is in play, the players mainly use their feet, but may also use any other part of their body, except for their hands or arms, to control, strike, or pass the ball; the head, chest, and thighs are commonly used. Only the goalkeepers may use their hands and arms, but they may use their hands only within their own penalty area. The team that has scored more goals at the end of the game is the winner. Depending on the format of the competition, an equal number of goals scored may result in a draw being declared with 1 point awarded to each team, or the game may go into extra time or a penalty shoot-out.[4]

Internationally, association football is governed by FIFA. Under FIFA, there are six continental confederations: AFC, CAF, CONCACAF, CONMEBOL, OFC, and UEFA. National associations (e.g. the FA in England, U.S. Soccer in the United States, etc.) are responsible for managing the game in their own countries both professionally and at an amateur level, and coordinating competitions in accordance with the Laws of the Game. The most prestigious senior international competition is the FIFA World Cup. The men's World Cup is the most-viewed sporting event in the world, surpassing the Olympic Games.[5] The most prestigious competition in European club football is the UEFA Champions League, which attracts an extensive television audience worldwide. The final of the men's Champions League is the most-watched annual sporting event in the world.[6][7]


Name
Main article: Names for association football
Association football is part of a family of football codes that emerged from various ball games played worldwide since antiquity. The word "association" in this term refers to the Football Association (the FA), founded in London in 1863, which published the first set of rules for the sport that same year.[8] The term was coined to distinguish the type of football played in accordance with the FA rules from other types that were gaining popularity at the time, particularly rugby football.[9]


The term soccer comes from Oxford "-er" slang, which was prevalent at the University of Oxford in England from about 1875, and is thought to have been borrowed from the slang of Rugby School. Initially spelt assoccer (a shortening of "association"), it was later reduced to the modern spelling.[10][11] Early alternative spellings included socca and socker.[9] This form of slang also gave rise to rugger for rugby football, fiver and tenner for five pound and ten pound notes, and the now-archaic footer that was also a name for association football.[12]

Within the English-speaking world, association football is now usually called simply "football" in Great Britain and most of Ulster in the north of Ireland,[13] whereas people usually call it "soccer" in regions and countries where other codes of football are prevalent, such as Australia,[14] Canada, South Africa, most of Ireland (excluding Ulster),[15] and the United States. A notable exception is New Zealand, where in the first two decades of the 21st century, under the influence of international television, "football" has been gaining prevalence, despite the dominance of other codes of football, namely rugby union and rugby league.[16]

History
Main article: History of association football
For a chronological guide, see Timeline of association football.
Association football in itself does not have a classical history.[17] Notwithstanding any similarities to other ball games played around the world, FIFA has described that no historical connection exists with any game played in antiquity outside Europe.[3] The history of football in England dates back to at least the eighth century.[18] The modern rules of association football are based on the mid-19th century efforts to standardise the widely varying forms of football played in the public schools of England.[19]
"""
)

embeddings = embed_model.embed_documents(chunks)

ids = [f"doc_{i}" for i in range(len(chunks))]

metadatas = [{"source" : "exaple.txt" , "chunk_id" : i} for i in range(len(chunks))]

collection.add(
    ids = ids,
    embeddings = embeddings,
    metadatas = metadatas,
    documents = chunks
)


query = "give me history of soccer"
query_embedding = embed_model.embed_query(query)

results =  collection.query(
    query_embeddings = [query_embedding],
    n_results = 3

)

for doc, meta in zip (results["documents"] [0], results["metadatas"][0] ):
    print(meta, "->" , doc)



