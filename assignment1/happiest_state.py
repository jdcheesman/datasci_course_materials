import sys
import json



def lines(fp, sent_dict):
    state_count = {}
    state_score = {}
    for line in fp:
        score = 0
        pyresponse =  json.loads(line)
        # first filter for all English language tweets:
        if "text" in pyresponse and "lang" in pyresponse and pyresponse["lang"] == 'en':
            if "place" in pyresponse:
                place = pyresponse["place"];
                if place is not None and "full_name" in place:
                    print pyresponse["place"]["full_name"].encode("utf8")
            msg = pyresponse["text"].split(' ')
            for w in msg:
                if w in sent_dict:
                    score += sent_dict[w]
            print score

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
