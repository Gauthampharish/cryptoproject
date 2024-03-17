from nltk.tokenize import sent_tokenize
'''text = input("Enter an input with three sentences: ")'''
text = '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.'''
sentence_array = []
token_text = sent_tokenize(text)

for sentence in token_text:
    sentence_array.append(sentence)
message_1 = sentence_array[0]
message_1 = message_1.encode()
message_2 = sentence_array[1]
message_2 = message_2.encode()
message_3 = sentence_array[2]
message_3 = message_3.encode()
with open('secret_message_1.txt', 'wb') as message:
    message.write(message_1)
    print("Done writing message one in secret_message_1.txt !")


with open('secret_message_2.txt', 'wb') as message:
    message.write(message_2)
    print("Done writing message one in secret_message_2.txt !")


with open('secret_message_3.txt', 'wb') as message:
    message.write(message_3)
    print("Done writing message one in secret_message_3.txt !")



