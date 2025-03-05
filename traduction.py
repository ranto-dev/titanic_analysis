import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd

# Chargement des données
data = pd.read_csv("/kaggle/input/language-translation-englishfrench/eng_-french.csv")
english_sentences = data["English words/sentences"].tolist()
french_sentences = data["French words/sentences"].tolist()

# Adaptation des tokenizers aux données
tokenizer_eng = Tokenizer()
tokenizer_eng.fit_on_texts(english_sentences)
eng_seq = tokenizer_eng.texts_to_sequences(english_sentences)

tokenizer_fr = Tokenizer()
tokenizer_fr.fit_on_texts(french_sentences)
fr_seq = tokenizer_fr.texts_to_sequences(french_sentences)

# Utilisation du nombre de mots dans le tokenizer pour définir l'embedding
vocab_size_eng = len(tokenizer_eng.word_index) + 1
vocab_size_fr = len(tokenizer_fr.word_index) + 1

# Padding
max_length = max(len(seq) for seq in eng_seq + fr_seq)
eng_seq_padded = pad_sequences(eng_seq, maxlen=max_length, padding='post')
fr_seq_padded = pad_sequences(fr_seq, maxlen=max_length, padding='post')


embedding_dim = 256
units = 512

# Encoder
encoder_inputs = Input(shape=(max_length,))
enc_emb = Embedding(input_dim=vocab_size_eng, output_dim=embedding_dim)(encoder_inputs)
encoder_lstm = LSTM(units, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(enc_emb)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = Input(shape=(max_length,))
dec_emb_layer = Embedding(input_dim=vocab_size_fr, output_dim=embedding_dim)
dec_emb = dec_emb_layer(decoder_inputs)
decoder_lstm = LSTM(units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)
decoder_dense = Dense(vocab_size_fr, activation='softmax')
output = decoder_dense(decoder_outputs)

# Modèle
model = Model([encoder_inputs, decoder_inputs], output)

# Compilation du modèle
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])

X_train, X_val, y_train, y_val = train_test_split(eng_seq_padded, fr_seq_padded, test_size=0.2)
model.fit([X_train, X_train], y_train, validation_data=([X_val, X_val], y_val), epochs=5, batch_size=64)


model.save("seq2seq_translation_v3.h5")

#model = tf.keras.models.load_model("seq2seq_translation_v3.h5")

def translate_sentence(sentence):
    seq = tokenizer_eng.texts_to_sequences([sentence])
    padded = pad_sequences(seq, maxlen=max_length, padding='post')
    translated = np.argmax(model.predict([padded, padded]), axis=-1)
    
    translated_sentence = []
    for i in translated[0]:
        if i in tokenizer_fr.index_word:
            translated_sentence.append(tokenizer_fr.index_word[i])
        else:
            translated_sentence.append(' ')  # Token inconnu si l'indice n'est pas trouvé dans le tokenizer
        
    return ' '.join(translated_sentence)

input_sentence = "Hi! I am tired ."
translated_sentence = translate_sentence(input_sentence)
print(f"Input: {input_sentence}")
print(f"Translated: {translated_sentence}")
