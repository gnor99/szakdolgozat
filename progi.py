#/usr/bin/python
# -*- coding: utf-8 -*-
from operator import itemgetter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer





def filetotokens(name,number):
    tokenek = []
    with open('D:/én/f/szakdolgozat/szavak.txt', encoding='utf8') as f:
            tiltottszavak = [] 
            for line in f:
                tiltottszavak.append(line.replace('\n', ''))

    for i in range(1,number+1):
        verstoken=[]
        fn = "D:/én/f/szakdolgozat/versek/184" + name + f"/{i}.txt"
        with open(fn , encoding='utf8') as f:
            vers = "" 
            tisztavers = ""
            for line in f:
                vers += line + " "
                
        for i in vers.translate({ord(i): ' '  for i in ',.!?:;-"'}).lower().split() :
            if i not in tiltottszavak:
                tisztavers = tisztavers + i + " "
        tokenek.append(tisztavers)
    return tokenek



def wordcounter(verstokenek):
    
    with open('D:/én/f/szakdolgozat/szavak.txt', encoding='utf8') as f:
        tiltottszavak = [] 
        for line in f:
            tiltottszavak.append(line.replace('\n', ''))
    
    word_counts = []
    for word_list in verstokenek:
        word_count = {}
        for word in word_list:
            if word not in tiltottszavak:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
        word_counts.append(word_count)
    
    for i in word_counts:
        valogatott_szotar = dict()
        for j in i:
            valogatott_szotar[j] = i[j]
        i.clear()
        i.update(sorted(valogatott_szotar.items(), key=itemgetter(1), reverse=True))
    
    
    return word_counts
 
            
def semanticfield():
    my_dict = {}

    with open("D:/én/f/szakdolgozat/szemantikai mezok.txt", 'r', encoding='utf8') as f:
        for line in f:
            words = line.translate({ord(i): ' '  for i in ',:'}).split()
            key = words[0]
            value = words[1:]
            my_dict[key] = value
            
    return my_dict

def dictmerger(lista):
    merged = dict()
    for i in lista:
        
        for key, value in i.items():
            if key in merged:
                if key in i:
                    merged[key] += value
                else:
                    merged[key] = value
            else:
                merged.update({key : value})
            
    return merged


def semanticfieldsearcher(lista, szotar2):
    legnepszerubb = []
    for szotar1 in lista:
        tema_szavak = {}
        for tema, szavak in szotar2.items():
            szavak_osszesen = sum([szotar1.get(szo, 0) for szo in szavak])
            tema_szavak[tema] = szavak_osszesen
        legnagyobb = max(tema_szavak, key=tema_szavak.get)
        legnepszerubb.append(legnagyobb)
    return legnepszerubb

            
    


if __name__ == "__main__":
    
    sf = semanticfield()
    ftketto = filetotokens("2",14)
    ftharom = filetotokens("3",38)
    ftnegy = filetotokens("4",135)
    ftot = filetotokens("5",168)
    fthat = filetotokens("6", 145)
    fthet = filetotokens("7",160)
    ftnyolc = filetotokens("8",105)
    ftkilenc = filetotokens("9", 21)

    ftössz =  ftketto + ftharom+ ftnegy+ ftot +fthat +  fthet +ftnyolc +ftkilenc 

    df = pd.DataFrame(ftössz, columns=["versek"])
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(ftössz)
    
    
    k = 10

    model = KMeans(n_clusters = k, init = 'k-means++', max_iter=100, n_init=1)
    model.fit(features)

    df['cluster'] = model.labels_

    
    clusters = df.groupby('cluster')

    for cluster in clusters.groups:
        f = open ('cluter' + str(cluster)+'.csv','w', encoding='utf8')
        data = clusters.get_group(cluster)[['versek']]
        f.write(data.to_csv(index_label = 'id'))
        f.close

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    for i in range(k):
        print("Cluster %d:" % i)
        for j in order_centroids[i, :10]:
            print('%s' % terms [j])
        print('\n')

    # wcketto = wordcounter(ftketto)
    # wcharom = wordcounter(ftharom)
    # wcnegy = wordcounter(ftnegy)
    # wcot = wordcounter(ftot)
    # wchat = wordcounter(fthat)
    # wchet = wordcounter(fthet)
    # wcnyolc = wordcounter(ftnyolc)
    # wckilenc = wordcounter(ftkilenc)
    
    # wcössz =  wcketto + wcharom+ wcnegy+ wcot +wchat +  wchet +wcnyolc +wckilenc 

    # sfketto = semanticfieldsearcher(wcketto, sf)
    # sfharom = semanticfieldsearcher(wcharom, sf)
    # sfnegy = semanticfieldsearcher(wcnegy, sf)
    # sfot = semanticfieldsearcher(wcot, sf)
    # sfhat = semanticfieldsearcher(wchat, sf)
    # sfhet = semanticfieldsearcher(wchet, sf)
    # sfnyolc = semanticfieldsearcher(wcnyolc, sf)
    # sfkilenc = semanticfieldsearcher(wckilenc, sf)    

    #versekre megnézni nem évekre és hogy a klaszterezésben mindegyik pont egy vers legyen, a számolást pedig leosztaná a szemantikai mezok szerint
        