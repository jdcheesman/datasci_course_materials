import sys
import json
import re


rx = re.compile('\W+')
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def getState(text):
    if text is None:
        return None

    result = None
    text = rx.sub(' ', text).strip()
    words = text.split(' ')
    for w in words:
        if w in states:
            return state_codes[states.index(w)]
        if len(words) > 1 and w in state_codes:
            return w

    return None



def lines(fp, sent_dict):
    state_count = {}
    state_score = {}
    for line in fp:
        score = 0
        pyresponse =  json.loads(line)
        # first filter for all English language tweets:
        if "text" in pyresponse and "lang" in pyresponse and pyresponse["lang"] == 'en':

            msg = pyresponse["text"].split(' ')
            for w in msg:
                if w in sent_dict:
                    score += sent_dict[w]

            rawLoc = None
            state = None
            if "place" in pyresponse:
                place = pyresponse["place"]
                if place is not None and "full_name" in place:
                    rawLoc = pyresponse["place"]["full_name"].encode("utf8")
                if place is not None and "country_code" in place and place["country_code"] == "US":
                    if "full_name" in place:
                        #print place["full_name"]
                        state = place["full_name"].split(',')[1]
            #     else:
            #         print "no cout"
            # if "user" in pyresponse:
            #     user = pyresponse["user"]
            #     if user is not None and "location" in user:
            #         rawLoc = user["location"].encode("utf8")
            # state = getState(rawLoc)

            if state is not None:
                if state in state_score:
                    state_score[state] += score
                    state_count[state] += 1
                else:
                    state_score[state] = score
                    state_count[state] = 1

    # print "state_count:"
    # print state_count
    # print "state_score:"
    # print state_score
    max_score = -1000.0
    happiest_state = "AZ"
    for s in state_count:
        score = float((state_score[s]*1.0) / (state_count[s]*1.0))
        if score > max_score:
            happiest_state = s
            max_score = score
    print happiest_state

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
