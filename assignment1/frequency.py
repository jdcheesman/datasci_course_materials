import sys
import json
import re


def lines(fp):
    unmatched_count = {}
    term_count = 0
    rx = re.compile('\W+')
    for line in fp:
        score = 0
        pyresponse =  json.loads(line)
        if "text" in pyresponse:
            msg = pyresponse["text"].split(' ')
            current_unmatched_count_words = set()
            for w in msg:
                term_count += 1

                w = rx.sub(' ', w).strip()
                if len(w) > 0:
                    clean_word = w.replace(' ', '%20').encode("utf8")
                    if not clean_word.startswith('@'):
                        if clean_word in unmatched_count:
                            unmatched_count[clean_word] += 1
                        else:
                            unmatched_count[clean_word] = 1

    for w in unmatched_count:
        val = float((unmatched_count[w]*1.0) / (term_count*1.0))
        print "%s %.9f"%(w, val) # Encode in "utf8" format


def main():
    tweet_file = open(sys.argv[1])
    lines(tweet_file)

if __name__ == '__main__':
    main()
