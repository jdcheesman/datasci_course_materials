import sys
import json
import re

def lines(fp, sent_dict):
    unmatched_count = {}
    unmatched_score = {}
    rx = re.compile('\W+')
    for line in fp:
        score = 0
        pyresponse =  json.loads(line)
        if "text" in pyresponse:
            msg = pyresponse["text"].split(' ')
            current_unmatched_count_words = set()
            for w in msg:
                w = rx.sub(' ', w).strip()
                if len(w) > 0:
                    clean_word = w.replace(' ', '%20').encode("utf8")
                    if not clean_word.startswith('@'):
                        if clean_word in sent_dict:
                            score += sent_dict[clean_word]
                        else:
                            current_unmatched_count_words.add(clean_word)
            for w in current_unmatched_count_words:
                if w in unmatched_count:
                    unmatched_count[w] += 1
                else:
                    unmatched_count[w] = 1
                if w in unmatched_score:
                    unmatched_score[w] += score
                else:
                    unmatched_score[w] = score

    for w in unmatched_count:
        val = float((unmatched_score[w]*1.0) / (unmatched_count[w]*1.0))
        print "%s %.3f"%(w, val) # Encode in "utf8" format


def readSentFile(fp):
    result = {}
    for line in fp:
        segmentedLine = line.split("\t")
        if len(segmentedLine) == 2:
            result[segmentedLine[0]] = int(segmentedLine[1])
        else:
            print segmentedLine
    return result

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sentfileDict = readSentFile(sent_file)
    lines(tweet_file, sentfileDict)

if __name__ == '__main__':
    main()
