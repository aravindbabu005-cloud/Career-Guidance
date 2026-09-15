import json
import pickle
from typing import List, Tuple, Dict
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

class ChatbotTrainer:
    def __init__(self, intents_file: str):
        """Initialize the chatbot trainer with the path to the intents file."""
        self.lemmatizer = WordNetLemmatizer()
        self.words: List[str] = []
        self.classes: List[str] = []
        self.documents: List[Tuple] = []
        self.ignore_words = {'?', '!', '.', ','}
        
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        # Load and process intents
        self.intents = self._load_intents(intents_file)
        
    def _load_intents(self, intents_file: str) -> Dict:
        """Load intents from JSON file."""
        with open(intents_file, 'r') as file:
            return json.load(file)
    
    def preprocess_data(self) -> None:
        """Process intent patterns and create training data."""
        # Process each pattern in the intents
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Tokenize the pattern
                words = nltk.word_tokenize(pattern)
                self.words.extend(words)
                self.documents.append((words, intent['tag']))
                
                # Add to classes list
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        
        # Lemmatize and clean words
        self.words = sorted(list(set([
            self.lemmatizer.lemmatize(word.lower())
            for word in self.words
            if word.lower() not in self.ignore_words
        ])))
        
        self.classes = sorted(list(set(self.classes)))
        
        print(f"Processed {len(self.documents)} documents")
        print(f"Found {len(self.classes)} classes: {self.classes}")
        print(f"Found {len(self.words)} unique lemmatized words")
    
    def create_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create and return training data (X and y)."""
        training = []
        output_empty = [0] * len(self.classes)
        
        # Create the training data
        for doc in self.documents:
            bag = []
            pattern_words = [self.lemmatizer.lemmatize(word.lower()) for word in doc[0]]
            
            # Create bag of words
            for word in self.words:
                bag.append(1 if word in pattern_words else 0)
            
            # Output row with '1' for current tag and '0' for other tags
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            
            training.append([bag, output_row])
        
        # Shuffle and convert to numpy array
        np.random.shuffle(training)
        training = np.array(training, dtype=object)
        
        # Split into X and y
        train_x = np.array([x for x, _ in training])
        train_y = np.array([y for _, y in training])
        
        return train_x, train_y
    
    def build_model(self, input_shape: int) -> Sequential:
        """Build and return the neural network model."""
        model = Sequential()
        
        # First layer
        model.add(Dense(128, activation='relu', input_dim=input_shape))
        model.add(Dropout(0.5))
        
        # Second layer
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        
        # Output layer
        model.add(Dense(len(self.classes), activation='softmax'))
        
        return model
    
    def save_data(self, words_file: str = 'words.pkl', classes_file: str = 'classes.pkl') -> None:
        """Save processed words and classes to pickle files."""
        with open(words_file, 'wb') as f:
            pickle.dump(self.words, f)
        with open(classes_file, 'wb') as f:
            pickle.dump(self.classes, f)
    
    def train(self, epochs: int = 200, batch_size: int = 5, model_path: str = 'chatbot_model.h5') -> None:
        """Train the chatbot model."""
        # Prepare training data
        train_x, train_y = self.create_training_data()
        
        # Build model
        model = self.build_model(len(train_x[0]))
        
        # Configure optimizer with learning rate decay
        sgd = SGD(
            learning_rate=0.01,
            momentum=0.9,
            nesterov=True
        )
        
        # Compile model
        model.compile(
            loss='categorical_crossentropy',
            optimizer=sgd,
            metrics=['accuracy']
        )
        
        # Define callbacks
        callbacks = [
            ModelCheckpoint(
                model_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            )
        ]
        
        # Train model
        history = model.fit(
            train_x,
            train_y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save the final model
        model.save(model_path)
        print("Model training completed")
        return history

def main():
    # Initialize and train the chatbot
    trainer = ChatbotTrainer('intents.json')
    trainer.preprocess_data()
    trainer.save_data()
    trainer.train()

if __name__ == "__main__":
    main()