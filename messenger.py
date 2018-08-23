import fbchat, wikipedia
from fbchat.models import *
from fbchat import Client, log


racialSlurs = ["racial slurs go here"]


class EchoBot(Client):

    who_is_ON = True
    detect_racialSlur_ON = True

    def kill(self, author_id, message, message_object, thread_id):
        if message_object.text.startswith("kill") and message_object.mentions[0].thread_id == self.uid:
            self.send(Message(text='So long world!'), thread_id=thread_id, thread_type=ThreadType.GROUP)
            self.send(Message(text='Killed by this person', mentions=[Mention(author_id, offset=10, length=11)]), thread_id=thread_id, thread_type=ThreadType.GROUP)
            self.listening = False
            self.logout()
        else:
             self.send(Message(text="sorry i can't kill people! :P"), thread_id=thread_id, thread_type=ThreadType.GROUP)


    def detect_racialSlur(self, author_id, message, message_object, thread_id, thread_type):
        response_object = message_object #copies message_objects properties
        msg = message_object.text.lower()#grabs the message from the message_object
        racialSlur_detected = False          
        for word in racialSlurs:
            if (msg.__contains__(word)) :
                racialSlur_detected = True

        if(racialSlur_detected) and (author_id != self.uid):      
            response_object.text = "Please! no racial slurs."
            self.send(response_object, thread_id=thread_id, thread_type=thread_type)

    def who_is(self, author_id, message_object,thread_id, thread_type):
        sentence = message_object.text.lower()
        if(sentence.startswith("who is")):
            person = sentence.replace("who is ","") 
            self.send(Message(text=wikipedia.summary(person, sentences=2)), thread_id=thread_id, thread_type=thread_type)
        elif (sentence.startswith("who")):
            self.send(Message(text=wikipedia.summary(sentence, sentences=2)), thread_id=thread_id, thread_type=thread_type)

        if (sentence.startswith("what is")):
            thing = sentence.replace("what is ","") 
            self.send(Message(text=wikipedia.summary(thing, sentences=2)), thread_id=thread_id, thread_type=thread_type)
        elif (sentence.startswith("what")): 
            self.send(Message(text=wikipedia.summary(sentence, sentences=2)), thread_id=thread_id, thread_type=thread_type)


    def checkSwitch(self, author_id, message_object, thread_id, thread_type):
        
        switch = message_object.text.lower()
        
        if(switch.startswith("turn on") and switch.endswith("sjw")):
            self.send(Message(text="I will detect racial slurs, but not all of course!"), thread_id=thread_id, thread_type=thread_type)
            self.detect_racialSlur_ON = True
            
        if(switch.startswith("turn off") and switch.endswith("sjw")):
            message = self.send(Message(text="I will not detect racials slurs anymore. :( Stay Toxic!", emoji_size=EmojiSize.LARGE), thread_id=thread_id, thread_type=thread_type)
            self.reactToMessage(message, MessageReaction.SAD)
            self.detect_racialSlur_ON = False

        if(switch.startswith("turn on") and switch.endswith("facts")):
            self.send(Message(text="Get your Facts! :) powered by Wikipedia because it is cheap :P"), thread_id=thread_id, thread_type=thread_type)
            self.who_is_ON = True
            
        if(switch.startswith("turn off") and switch.endswith("facts")):
            self.send(Message(text="No more facts, Stay Dumb!"), thread_id=thread_id, thread_type=thread_type)
            self.who_is_ON = False

        

    def onMessage(self, author_id, message, message_object, thread_id, thread_type, **kwargs):

        self.markAsDelivered(thread_id, message_object.uid)
        self.checkSwitch(author_id, message_object, thread_id, thread_type)
  
        # this turns/logs off the bot
        self.kill(author_id, message, message_object, thread_id)
        
        if self.detect_racialSlur_ON:
            self.detect_racialSlur(author_id, message, message_object, thread_id, thread_type)
        
        if self.who_is_ON:
            self.who_is(author_id, message_object,thread_id, thread_type)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
      
        


client = EchoBot('<email>', '<password>')

message = "Hi, i am a chatbot. ive been turned on by @Daniel Limas"
new_offset = message.__len__() - 13

if client.isLoggedIn(): 
    client.send(Message(text=message ,  mentions=[Mention(100000404707583 , offset=new_offset, length=13)] ), thread_id='2173445302727467', thread_type=ThreadType.GROUP)
    # client.send(Message(text=message ,  mentions=[Mention(100000404707583 , offset=new_offset, length=13)] ), thread_id='200231243496260', thread_type=ThreadType.GROUP)
    
client.listen()
    










 