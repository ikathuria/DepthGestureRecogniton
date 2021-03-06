"""Visualizing the trained model."""

print('loading imports...', end="")
from visualize_functions import *
import numpy as np
import cv2
print('imports loaded')


if __name__ == '__main__':
    MODEL_DATA = {4: [['Swiping Right',
                       'Sliding Two Fingers Left',
                       'No gesture',
                       'Thumb Up'],
                      r'weights\4_classes\path_to_my_weights'],
                  6: [['No gesture',
                       'Stop Sign',
                       'Swiping Left',
                       'Swiping Right',
                       'Thumb Down',
                       'Thumb Up'],
                      r'weights\6_classes1\path_to_my_weights'],
                  8: [['No gesture',
                       'Sliding Two Fingers Down',
                       'Sliding Two Fingers Left',
                       'Sliding Two Fingers Right',
                       'Sliding Two Fingers Up',
                       'Thumb Down',
                       'Thumb Up'],
                      r'weights\8_classes\path_to_my_weights']}
    MODE = 6
    CLASSES = MODEL_DATA[MODE][0]
    PATH = MODEL_DATA[MODE][1]

    # load model
    print('loading model...', end="")
    model = Conv3DModel(8)
    model.compile(loss='sparse_categorical_crossentropy',
                      optimizer=RMSprop())
    model.load_weights(PATH)
    print('model loaded')
    to_predict = []
    num_frames = 0
    text = ''

    print('loading OpenCV...')
    cap = cv2.VideoCapture(0)

    while True:
        # capture frame-by-frame
        ret, frame = cap.read()
        # processing the frames
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        to_predict.append(cv2.resize(gray, (64, 64)))

        if len(to_predict) == 30:
            frame_to_predict = np.array(to_predict, dtype=np.float32)
            frame_to_predict = normalize_data(frame_to_predict)

            predict = model.predict(frame_to_predict)
            predicted_class = CLASSES[np.argmax(predict)]

            text = 'Class=%s Precision=%.2f %%' % (
                predicted_class, np.amax(predict)*100)

            to_predict = []

        cv2.putText(frame, text, (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 0), 1, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Hand Gesture Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
