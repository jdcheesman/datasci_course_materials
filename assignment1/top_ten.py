import sys
import json
import operator


def lines(fp):
    tags = {}
    for line in fp:
        pyresponse =  json.loads(line)
        if "entities" in pyresponse:
            entities = pyresponse["entities"]
            if "hashtags" in entities:
                hashtags = entities["hashtags"] # type: list
                for tt in hashtags:
                    t = tt["text"].encode("utf8")
                    if t in tags:
                        tags[t] += 1
                    else:
                        tags[t] = 1
    sorted_x = sorted(tags.iteritems(), key=operator.itemgetter(1))
    ind = range(len(sorted_x)-1, len(sorted_x)-11, -1)
    for i in ind:
        val, count = sorted_x[i]
        print val + " " + str(count*1.0)



def main():
    tweet_file = open(sys.argv[1])
    lines(tweet_file)

if __name__ == '__main__':
    main()
