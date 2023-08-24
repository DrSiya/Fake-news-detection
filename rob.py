
import re
import Long_responses as long

def message_probability(user_message, recognized_words,single_response=False,required_words=[]):
    message_certainty = 0
    has_required_words = True
    
    for word in user_message:
        if word in recognized_words:
             message_certainty =  message_certainty + 1   

    percentage = float(message_certainty)/float(len(recognized_words))
    
    for word in required_words:
        if  word not in user_message:
            has_required_words = False
            break
        
    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0
    
def check_all_messages(message):
    highest_prob_list = {}
    
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words,single_response,required_words)
    
    # Responses```````````````````````````````````
    response('Hi! How can I help you?',['hey','hi','hello','sawubona','dumela'],single_response=True)
    response('Sorry, I was not designed for small chats',['how','are','you','doing',],required_words=['how','you'])
    response('Yes, you can paste info from anywhere',['should','paste','text','where','from'],required_words=['paste','should','from'])
    response('only links from career24 & linkedin works',['which', 'links', 'work'],required_words=['links','work'])
    response('well it takes 2-3 min to verify',['how','long','does','it', 'take','to','verify'],required_words=['how','long','verify'])
    response('No, only links from career24 & linkedin works',['can','paste','any','link'],required_words=['paste','any','link','can'])
    response('No, it will not be able to detect',['will','the','system','detect','if','i','have','not','entered'],required_words=['not','will','entered'])
    

    best_match = max(highest_prob_list,key=highest_prob_list.get)
    
    if (highest_prob_list[best_match] < 1):
        return long.unknown()  
    else: 
        return best_match
    
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*',user_input.lower())
    response = check_all_messages(split_message)
    return response

