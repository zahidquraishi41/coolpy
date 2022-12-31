from typing import List
from sklearn import neighbors
import os
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from os.path import join
from smol import menu, utils
import shutil

'''An image organizer app that uses KNN model for classifying and organizing images.'''


def train(train_dir: str = 'dataset', save_path: str = 'trained_model.pik'):
    '''Trains a knn classifier for face recognition.
    @train_dir: path to dir containing images of a person, dir name will be used as person's name'''
    x = []
    y = []

    # Loop through each person in the training set
    dirs = [join(train_dir, path)
            for path in os.listdir(train_dir) if os.path.isdir(join(train_dir, path))]
    dirs_len = len(dirs)
    if not dirs:
        print('No dataset found.')
        return

    utils.clear_screen()
    print('Training model...')
    for i, class_dir in enumerate(dirs):
        # Loop through each training image for the current person
        for img_path in image_files_in_folder(class_dir):
            print(f'Processing: {i+1}/{dirs_len} \r', end='')
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) >= 1:
                encoding = face_recognition.face_encodings(
                    image, known_face_locations=face_bounding_boxes)[0]
                x.append(encoding)
                y.append(os.path.basename(class_dir))
    print('Training complete...')
    utils.pause()

    # Determine how many neighbors to use for weighting in the KNN classifier
    n_neighbors = 2

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(
        n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(x, y)

    # Save the trained KNN classifier
    with open(save_path, 'wb') as f:
        pickle.dump(knn_clf, f)

    return knn_clf


def predict(img_path: str, knn_clf) -> List[str]:
    '''Recognizes faces in given image using a trained KNN classifier
    @img_path: path for image file.
    @knn_clf: Trained KNN model for prediction.'''

    # Load image file and find face locations
    image = face_recognition.load_image_file(img_path)
    face_locations = face_recognition.face_locations(image)

    # If no faces are found in the image, return an empty result.
    if len(face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        image, known_face_locations=face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <=
                   0.6 for i in range(len(face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [pred if rec else "unknown" for pred, _, rec in zip(knn_clf.predict(faces_encodings), face_locations, are_matches)]


def organize(trained_model: str = 'trained_model.pik'):
    utils.clear_screen()
    print('Loading trained model...')
    with open(trained_model, 'rb') as f:
        knn_clf = pickle.load(f)
    print('Load complete.')
    print('Organizing Files...')
    images = image_files_in_folder('organize')
    images_len = len(images)
    for i, img_path in enumerate(images):
        print(f'Processing: {i+1}/{images_len}\r', end='')
        names = predict(img_path, knn_clf)
        names = list(set(names))  # removing duplicate names
        name = '_'.join(names)
        dest = join('organize', name)
        if not os.path.exists(dest):
            os.mkdir(dest)
        shutil.move(img_path, join(dest, os.path.basename(img_path)))
    print()
    print('Organization complete.')
    utils.pause()


def help():
    utils.clear_screen()
    structure_help = '''STEP 1: Label your training images using following structure.
    dataset/
    ├── <person1>/
    │   ├── image1.jpeg
    │   ├── image2.jpeg
    │   ├── ...
    ├── <person2>/
    │   ├── image1.jpeg
    │   └── image2.jpeg
    └── ...
    
STEP 2: Place unorganized images into 'organize' folder.
    '''
    print(structure_help)
    utils.pause()


if __name__ == "__main__":
    items = ['Train Dataset', 'Organize Files', 'Help', 'Exit']
    commands = ('quit', 'exit')
    while True:
        choice = menu.choose(items, commands=commands)
        if choice in items:
            index = items.index(choice)
            if index == 0:
                print("Training KNN classifier...")
                train()
                print("Training complete!")
            elif index == 1:
                organize()
            elif index == 2:
                help()
            else:
                exit(0)
        else:
            exit(0)
